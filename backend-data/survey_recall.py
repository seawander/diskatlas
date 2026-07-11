#!/usr/bin/env python3
"""Survey-recall audit: how complete is the atlas against published survey samples.

For each survey it fetches the paper's arXiv source, extracts the target list from
the named sample table, matches each target to data/systems/*.json by normalized
identifier (name / alias / simbad / id, with an IRS-suffix fallback so 'BHR71'
matches 'bhr71-irs1'), and reports per survey:
  sample            targets in the published sample table
  with_record       in the atlas AND carrying this survey's image record
  missing_record    in the atlas but lacking this survey's record  (ingestion queue)
  absent            not in the atlas at all                        (ingestion queue)

CONFIDENCE: table layouts are heterogeneous. Surveys whose sample table is a clean
deluxetable with the source name in a detectable column parse reliably ("high");
label-first or citation-laden tables under-parse and are flagged "partial" — their
denominators must be curated by hand before quoting. Output -> data/paper_finder/
survey_recall.json and a markdown summary on stdout.

Usage:  python3 backend-data/survey_recall.py [--src <dir of extracted arXiv sources>]
"""
import argparse, glob, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (label, source-dir key, survey arXiv, sample-table caption keyword, atlas survey tag, confidence)
SURVEYS = [
    ("DSHARP",       "dsharp",  "1812.04040", "Sample: Host Star",                 "DSHARP",           "high"),
    ("exoALMA",      "exoalma", "2504.18688", "exoALMA Sample",                    "exoALMA",          "high"),
    ("MAPS",         "maps",    "2109.06268", "Stellar and Disk Properties",       "MAPS",             "partial"),
    ("eDisk",        "edisk",   "2306.15406", "eDisk sample",                      "eDisk",            "partial"),
    ("AGE-PRO",      "agepro",  "2506.10719", "AGE-PRO Sample: Host Star",         "AGE-PRO",          "partial"),
    ("Long2018",     "long2018","1810.06044", "Source Properties and observation", "Taurus-Long2018",  "partial"),
    ("DARTTS-S",     "dartts",  "1803.10882", "Target overview",                   "DARTTS-S",         "partial"),
    ("GPIES-debris", "gpies",   "2004.13722", "GPIES Disk Observations by Target", "GPIES-debris",     "partial"),
    ("REASONS",      "reasons", "2501.09058", "REASONS newly observed",            "REASONS",          "partial"),
]

ASTRO = re.compile(r'\b('
  r'HD ?\d{3,6}|HR ?\d+|HIP ?\d+|2MASS ?J\d{6,8}[+-]\d{6,7}|IRAS ?\d{5}[+-]\d{4}|'
  r'Sz ?\d+|ISO[- ]?Oph ?\d+|Elias ?2?[- ]?\d+|DoAr ?\d+|AS ?\d{2,4}|WSB ?\d+|WaOph ?\d+|'
  r'GSS ?\d+|SR ?\d+|MWC ?\d+|Ced ?\d+|BHR ?\d+|LkCa ?\d+|CI ?Tau|DL ?Tau|IM ?Lup|GM ?Aur|'
  r'RX ?J\d{4}[.\d]*[+-]\d{3,4}|V\d{3,4} ?[A-Z][a-z]{2}|PDS ?\d+|Haro ?\d+[- ]?\d*|'
  r'[A-Z]{2} ?(?:Tau|Lup|Cha|Ori|Aur|Sgr|Sco|Mon|Ser|Peg|Cyg|Pic|Hya|CrA)\b)')
BAD = re.compile(r'\b(19|20)\d\d\b|et al|Krautter|Comeron|Torres|Luhman')


def clean(s):
    s = re.sub(r'\\tablenotemark\{[^}]*\}', '', s)
    s = re.sub(r'\\[a-zA-Z]+\*?', '', s)
    s = re.sub(r'[{}$~\\^]', '', s)
    return re.sub(r'\s+', ' ', s).strip(' *.,')


def table_body(t, kw):
    i = t.find(kw)
    if i < 0:
        return ""
    j = t.find('\\startdata', i)
    if 0 <= j < i + 5000:
        return t[j + 10:t.find('\\enddata', j)]
    for beg, end in (('\\begin{tabular', '\\end{tabular}'), ('\\begin{longtable', '\\end{longtable}')):
        b = t.find(beg, i)
        if 0 <= b < i + 5000:
            return t[b:t.find(end, b)]
    return ""


def sample_targets(body):
    out, seen = [], set()
    for row in re.split(r'\\\\', body):
        if '&' not in row:
            continue
        for cell in row.split('&'):
            c = clean(cell)
            if BAD.search(c):
                continue
            m = ASTRO.search(c)
            if m:
                nm = re.sub(r'\s+', ' ', m.group(1)).strip()
                key = re.sub(r'[^a-z0-9]', '', nm.lower())
                if key not in seen:
                    seen.add(key); out.append(nm)
                break
    return out


def build_index():
    idx, base = {}, {}
    norm = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower())
    for f in glob.glob(str(ROOT / 'data' / 'systems' / '*.json')):
        d = json.loads(Path(f).read_text())
        for key in [d.get('name'), d.get('simbad'), d['id']] + (d.get('alt_names') or []):
            if key:
                idx.setdefault(norm(key), d)
                base.setdefault(re.sub(r'irs\d.*$', '', norm(key)), d)
    return idx, base, norm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="", help="dir with extracted arXiv sources (<key>/*.tex)")
    a = ap.parse_args()
    src = Path(a.src) if a.src else None
    idx, base, norm = build_index()

    def lookup(tg):
        n = norm(tg)
        return idx.get(n) or base.get(re.sub(r'irs\d.*$', '', n))

    def hasrec(d, tag, ax):
        return any(im.get('survey') == tag or im.get('paper', {}).get('arxiv') == ax
                   for im in d.get('images', []))

    report = {}
    print("| survey | conf | sample | +record | missing-record | absent |")
    print("|---|---|---|---|---|---|")
    for name, key, ax, kw, tag, conf in SURVEYS:
        smp = []
        if src:
            texs = glob.glob(str(src / key / "*.tex"))
            if texs:
                t = Path(texs[0]).read_text(errors='ignore')
                smp = sample_targets(table_body(t, kw))
        wr, miss, ab = [], [], []
        for tg in smp:
            d = lookup(tg)
            if d is None:
                ab.append(tg)
            elif hasrec(d, tag, ax):
                wr.append(tg)
            else:
                miss.append({"target": tg, "system": d['id']})
        report[name] = {"arxiv": ax, "confidence": conf, "sample": len(smp),
                        "with_record": len(wr), "missing_record": miss, "absent": ab}
        print(f"| {name} | {conf} | {len(smp)} | {len(wr)} | {len(miss)} | {len(ab)} |")

    (ROOT / "data" / "paper_finder" / "survey_recall.json").write_text(json.dumps(report, indent=1))
    print("\nActionable gaps (ingestion queue):")
    for name, r in report.items():
        if r["missing_record"] or r["absent"]:
            print(f"  {name}: missing-record={[m['system'] for m in r['missing_record']]}  absent={r['absent']}")
    print("\nNOTE: 'partial'-confidence samples under-parse heterogeneous tables; curate their "
          "denominators by hand before quoting. 'high' (DSHARP, exoALMA) are reliable.")


if __name__ == "__main__":
    main()
