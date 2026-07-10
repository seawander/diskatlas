#!/usr/bin/env python3
"""Harvest OBSERVATION epochs from paper sources and archives.

The `epoch` field is the observation date, never the publication date. This tool
recovers it at scale with per-record confidence gating:

  tex    parse local arXiv tex sources (images/_sources/extracted/<id>/)
         - TeX comments are stripped (commented-out table rows poisoned earlier runs)
         - multi-target papers: a date only counts for a record when the record's
           target alias sits in the same table row / sentence window
         - multi-instrument papers: the record's instrument keyword must appear in
           the window when the paper has several dated instruments
  apply  write gated candidates into data/systems/*.json + provenance sidecar

Confidence tiers (stored per candidate):
  row    alias + date in one observing-log table row       -> auto-apply
  ctx    single-target paper, unique obs-context date       -> auto-apply
  instr  date window names the record's instrument          -> auto-apply
  year   several dates, all in one calendar year            -> apply year only
  ambig  several dates, several years                       -> NOT applied (listed)

Usage:
  python3 backend/epoch_harvest.py tex   [--json OUT] [--review OUT]
  python3 backend/epoch_harvest.py apply [--json IN] [--tiers row,ctx,instr,year]
"""
import argparse, glob, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "_sources" / "extracted"
PROV = ROOT / "data" / "paper_finder" / "epoch_provenance.json"

MON = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
YR = r"(?:19[89]\d|20[0-2]\d)"
DATES = [
    (re.compile(rf"\b({YR})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b"),
     lambda m: f"{m.group(1)}-{m.group(2)}-{m.group(3)}"),
    (re.compile(rf"\b({YR})\s+({MON})\.?\s+(\d{{1,2}})\b"),
     lambda m: f"{m.group(1)} {m.group(2)[:3]} {int(m.group(3))}"),
    (re.compile(rf"\b(\d{{1,2}})\s+({MON})\.?,?\s+({YR})\b"),
     lambda m: f"{m.group(3)} {m.group(2)[:3]} {int(m.group(1))}"),
    (re.compile(rf"\b({MON})\.?\s+(\d{{1,2}})(?:\s*[-–]+\s*\d{{1,2}})?,?\s+({YR})\b"),
     lambda m: f"{m.group(3)} {m.group(1)[:3]} {int(m.group(2))}"),
    (re.compile(rf"\b({MON})\.?\s+({YR})\b"),
     lambda m: f"{m.group(2)} {m.group(1)[:3]}"),
]
OBS_CTX = re.compile(r"observ|\bUT\b|night|acquired|obtained|taken|carried out|"
                     r"performed|imag|data were|executed|epoch", re.I)
BAD_CTX = re.compile(r"receiv|accept|publish|submitt|revis|in press|copyright|"
                     r"\bDOI\b|arXiv|©|in prep|press release|priv.*comm", re.I)
NEG_CTX = re.compile(r"radial velocit|\bRV\b|spectrograph|spectroscop|spectrum|spectra\b|"
                     r"bar report|reference (?:star|PSF)|PSF (?:star|reference)|calibrat|"
                     r"proposal|scheduled|will be observed|to be observed|photometr|"
                     r"light ?curve|transit|monitoring|astrometric catalog|Gaia|Hipparcos|"
                     r"2MASS survey|parallax|failure|archiv|Bulletin|Catalog", re.I)

# instrument keywords per record: record-instrument string -> regex to find in window
def instr_rx(instr, facility):
    s = f"{instr or ''} {facility or ''}"
    keys = []
    for pat, rx in [
        ("NIRCam", r"NIRCam"), ("MIRI", r"MIRI"), ("NIRSpec", r"NIRSpec"),
        ("IRDIS", r"IRDIS"), ("ZIMPOL", r"ZIMPOL"), ("IFS", r"\bIFS\b"),
        ("SPHERE", r"SPHERE"), ("GPI", r"\bGPI\b"), ("NACO", r"NACO|NaCo"),
        ("NICMOS", r"NICMOS"), ("STIS", r"STIS"), ("ACS", r"\bACS\b"),
        ("WFC3", r"WFC3"), ("WFPC2", r"WFPC2"), ("NIRC2", r"NIRC2"),
        ("HiCIAO", r"HiCIAO"), ("CHARIS", r"CHARIS"), ("VAMPIRES", r"VAMPIRES"),
        ("MUSE", r"MUSE"), ("GRAVITY", r"GRAVITY"), ("MATISSE", r"MATISSE"),
        ("VISIR", r"VISIR"), ("NICI", r"NICI"), ("NIRI", r"NIRI"),
        ("LMIRCam", r"LMIR[Cc]am|LBTI"), ("MagAO", r"MagAO"), ("Clio", r"Clio"),
        ("ALMA", r"ALMA"), ("SMA", r"\bSMA\b"), ("NOEMA", r"NOEMA"),
        ("PdBI", r"PdBI|Plateau de Bure"), ("CARMA", r"CARMA"), ("VLA", r"\bVLA\b|Very Large Array"),
        ("ATCA", r"ATCA"), ("PACS", r"PACS"), ("MIPS", r"MIPS"), ("IRAC", r"IRAC"),
        ("SCUBA", r"SCUBA"), ("T-ReCS", r"T-?ReCS"), ("COMICS", r"COMICS"),
        ("Band", r"ALMA"),   # "Band N" records are ALMA; generic 'band' matches prose
    ]:
        if pat.lower() in s.lower():
            keys.append(rx)
    return re.compile("|".join(keys), re.I) if keys else None


# any instrument/facility token; a window naming an instrument OTHER than the
# record's is "foreign" and must not vote for that record's epoch
ALL_INSTR_RX = re.compile(
    r"NIRCam|MIRI|NIRSpec|IRDIS|ZIMPOL|\bIFS\b|SPHERE|\bGPI\b|NACO|NaCo|NICMOS|STIS|"
    r"\bACS\b|WFC3|WFPC2|NIRC2|HiCIAO|CHARIS|VAMPIRES|MUSE|GRAVITY|MATISSE|VISIR|"
    r"NICI|NIRI|LMIR[Cc]am|LBTI|MagAO|Clio|ALMA|\bSMA\b|NOEMA|PdBI|Plateau de Bure|"
    r"CARMA|\bVLA\b|ATCA|PACS|MIPS|IRAC|SCUBA|T-?ReCS|COMICS|Palomar|Spitzer|"
    r"Herschel|WISE\b|IRAS\b|Keck|Gemini|Subaru", re.I)


def win_class(win, irx):
    """'match' if window names the record's instrument, 'foreign' if it names a
    different one, 'neutral' if it names none."""
    if irx and irx.search(win):
        return "match"
    toks = ALL_INSTR_RX.findall(win)
    if not toks:
        return "neutral"
    if irx is None:
        return "neutral"    # record has no instrument keyword to contradict
    return "foreign"


# Candidates rejected on manual review (window quoted a different instrument's
# date, a calibration target, an instrument-failure date, or a mission-impossible
# year). Never emit these again.
BLOCKLIST = {
    "eta-crv_herschel2014",        # 2005 date = Spitzer row (Herschel launched 2009)
    "hd-100546_atca2015",          # 3mm log date for the 7mm record
    "hd-107146_carma2008",         # CARMA runs span 2007-2008
    "vhs-j1256-1257_vista2015-y", "vhs-j1256-1257_vista2015-j",
    "vhs-j1256-1257_vista2015-h", "vhs-j1256-1257_vista2015-ks",
                                   # 2014 dates are follow-ups, not the VHS tiles
    "coconuts-1_discovery2020",    # 2018 dates are spectroscopy; PS1 stack 2010-14
    "lkha-330_alma2022",           # window quoted the SPHERE PDI date
    "au-mic_arks", "hd-10647_arks",# ARKS mixes new + archival executions
    "t-cha_sphere2017",            # 2000 Mar = archival HST epoch, not SPHERE
    "cs-cha_sphere-ginski2018",    # date from the Ceres astrometric calibration
    "v807-tau_alma2019",           # date from a 'high rms; data not used' table row
    "hd-32297_hiciao-pdi2014",     # window described the full-intensity (ADI) set
    "hd-113337_herschel2019",      # 2015 impossible for PACS (Herschel died 2013)
    "cy-tau_vla-7.1mm",            # 2009 window is CARMA; VLA Q-band ran later
}


def norm(s):
    """normalize names for alias matching: drop tex escapes, spaces, dashes, case"""
    s = re.sub(r"\\[a-zA-Z]+|[~{}$\\]", "", s)
    return re.sub(r"[\s\-_.]+", "", s).lower()


def sys_aliases(d):
    names = [d.get("name", ""), d.get("simbad") or "", d["id"]] + list(d.get("alt_names", []))
    out = set()
    for n in names:
        k = norm(n)
        if len(k) >= 4:
            out.add(k)
        # "HD 143811" -> also "hd143811b"-safe prefix match handled by 'in'
    return out


def strip_comments(t):
    # remove unescaped % to end-of-line (keeps \%)
    return re.sub(r"(?<!\\)%[^\n]*", "", t)


def source_text(ax):
    d = SRC / ax
    if not d.is_dir():
        return None
    parts = []
    for f in sorted(d.glob("*.tex")) + sorted(d.glob("*.txt")):
        try:
            parts.append(f.read_text(errors="ignore"))
        except Exception:
            pass
    if not parts and (d / f"{ax}.pdf").exists():
        try:
            import fitz
            parts.append("".join(p.get_text() for p in fitz.open(str(d / f"{ax}.pdf"))))
        except Exception:
            pass
    return strip_comments("\n".join(parts)) if parts else None


def find_dates(text):
    """[(pos, normdate)] first-match-wins per position"""
    hits, taken = [], set()
    for rx, fmt in DATES:
        for m in rx.finditer(text):
            span = (m.start(), m.end())
            if any(a <= span[0] < b for a, b in taken):
                continue
            taken.add(span)
            hits.append((m.start(), m.end(), fmt(m)))
    hits.sort()
    return hits


def harvest_tex():
    # collect records missing epoch, grouped by paper
    by_ax = defaultdict(list)   # ax -> [(sysfile, idx, sysid, aliases, instr_rx, instr_str)]
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        al = sys_aliases(d)
        for i, im in enumerate(d.get("images", [])):
            if im.get("epoch"):
                continue
            ax = (im.get("paper") or {}).get("arxiv")
            if ax:
                by_ax[ax].append((str(f), i, d["id"], al,
                                  instr_rx(im.get("instrument"), im.get("facility")),
                                  im.get("instrument") or "", im["image_id"]))

    out = {}      # image_id -> candidate dict
    stats = defaultdict(int)
    review = []
    for ax, recs in sorted(by_ax.items()):
        text = source_text(ax)
        if not text:
            stats["no_source"] += len(recs)
            continue
        lines = text.split("\n")
        # precompute: per line, dates + normalized form
        line_dates = []
        for ln in lines:
            ds = find_dates(ln)
            line_dates.append(ds)
        nsys = len({r[2] for r in recs})
        # global obs-context dates (for ctx tier)
        all_hits = find_dates(text)
        obs_hits = []
        for a, b, dt in all_hits:
            win = text[max(0, a - 120):b + 120]
            if BAD_CTX.search(win) or NEG_CTX.search(win):
                continue
            if OBS_CTX.search(win):
                obs_hits.append((a, b, dt, win))

        for sysfile, i, sid, aliases, irx, istr, iid in recs:
            cand = None
            # --- tier 1: table-row alias match ------------------------------
            row_dates = []
            for ln, ds in zip(lines, line_dates):
                if not ds or "&" not in ln:
                    continue
                nln = norm(ln)
                if any(a in nln for a in aliases):
                    if BAD_CTX.search(ln) or NEG_CTX.search(ln):
                        continue
                    # instrument column check when possible
                    ok_instr = (irx.search(ln) is not None) if irx else False
                    for _, _, dt in ds:
                        row_dates.append((dt, ok_instr, ln.strip()[:110]))
            if row_dates:
                with_instr = [r for r in row_dates if r[1]]
                pick = with_instr or row_dates
                years = {re.match(r"\d{4}", p[0]).group(0) for p in pick}
                if len({p[0] for p in pick}) == 1 or (with_instr and len({p[0] for p in with_instr}) == 1):
                    dt, _, snip = pick[0]
                    cand = dict(epoch=dt, tier="row", snippet=snip)
                elif len(years) == 1:
                    cand = dict(epoch=years.pop(), tier="year",
                                snippet=f"{len(pick)} row dates, same year: " + "; ".join(sorted({p[0] for p in pick})[:4]))
                else:
                    cand = dict(epoch=None, tier="ambig",
                                snippet="row dates span years: " + "; ".join(sorted({p[0] for p in pick})[:5]))
            # --- tier 1b: instrument-row match (single-target obs-log tables)
            if cand is None and nsys == 1 and irx is not None:
                irow = []
                for ln, ds in zip(lines, line_dates):
                    if not ds or "&" not in ln:
                        continue
                    if BAD_CTX.search(ln) or NEG_CTX.search(ln):
                        continue
                    if irx.search(ln):
                        for _, _, dt in ds:
                            irow.append((dt, ln.strip()[:110]))
                if irow and len({r[0] for r in irow}) == 1:
                    cand = dict(epoch=irow[0][0], tier="irow", snippet=irow[0][1])
            # --- tier 2/3: context match ------------------------------------
            if cand is None and obs_hits:
                # multi-system papers require the alias inside the window;
                # windows naming a DIFFERENT instrument are dropped ("foreign")
                pool = []
                for a, b, dt, win in obs_hits:
                    nwin = norm(win)
                    alias_ok = any(al in nwin for al in aliases)
                    if nsys > 1 and not alias_ok:
                        continue
                    wc = win_class(win, irx)
                    if wc == "foreign":
                        continue
                    pool.append((dt, wc == "match", alias_ok, win))
                if pool:
                    w_instr = [p for p in pool if p[1]]
                    uniq = sorted({p[0] for p in pool})
                    uniq_i = sorted({p[0] for p in w_instr})
                    if len(uniq_i) == 1:
                        p = w_instr[0]
                        cand = dict(epoch=p[0], tier="instr",
                                    snippet=re.sub(r"\s+", " ", p[3])[:110])
                    elif len(uniq) == 1 and irx is None:
                        # pure-ctx only allowed when the record has no instrument
                        # keyword to demand (else other-instrument dates leak in)
                        p = pool[0]
                        cand = dict(epoch=p[0], tier="ctx",
                                    snippet=re.sub(r"\s+", " ", p[3])[:110])
                    else:
                        # instrument-matched windows dominate; neutral windows may
                        # only vote for a year
                        years = {re.match(r"\d{4}", u).group(0) for u in (uniq_i or uniq)}
                        if len(years) == 1:
                            cand = dict(epoch=years.pop(), tier="year",
                                        snippet="ctx dates same year: " + "; ".join((uniq_i or uniq)[:4]))
                        else:
                            cand = dict(epoch=None, tier="ambig",
                                        snippet="ctx dates span years: " + "; ".join((uniq_i or uniq)[:5]))
            if cand is None:
                stats["nothing"] += 1
                continue
            if iid in BLOCKLIST:
                stats["blocked"] += 1
                continue
            cand.update(arxiv=ax, system=sid, file=sysfile, idx=i, instrument=istr)
            out[iid] = cand
            stats[cand["tier"]] += 1
            review.append(f"[{cand['tier']:5s}] {sid:28s} {iid:44s} {str(cand['epoch']):14s} | {ax} | {istr[:18]:18s} | {cand['snippet']}")
    return out, stats, review


def cmd_apply(args):
    cands = json.loads(Path(args.json).read_text())
    tiers = set(args.tiers.split(","))
    prov = json.loads(PROV.read_text()) if PROV.exists() else {}
    by_file = defaultdict(list)
    for iid, c in cands.items():
        if c["tier"] in tiers and c["epoch"]:
            by_file[c["file"]].append((c["idx"], c["epoch"], iid, c))
    n = 0
    for f, items in by_file.items():
        d = json.loads(Path(f).read_text())
        for idx, e, iid, c in items:
            im = d["images"][idx]
            assert im["image_id"] == iid, f"index drift {iid}"
            if im.get("epoch"):
                continue
            im["epoch"] = e
            prov[iid] = {"epoch": e, "source": f"{c.get('src', 'tex')}:{c['tier']}",
                         "arxiv": c["arxiv"], "snippet": c["snippet"]}
            n += 1
        Path(f).write_text(json.dumps(d, indent=1, ensure_ascii=False))
    PROV.write_text(json.dumps(prov, indent=1, ensure_ascii=False))
    print(f"applied {n} epochs (tiers: {sorted(tiers)}); provenance -> {PROV.name}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tex")
    t.add_argument("--json", default=str(ROOT / "data" / "paper_finder" / "epoch_tex_candidates.json"))
    t.add_argument("--review", default="/dev/stdout")
    a = sub.add_parser("apply")
    a.add_argument("--json", default=str(ROOT / "data" / "paper_finder" / "epoch_tex_candidates.json"))
    a.add_argument("--tiers", default="row,ctx,instr,year")
    args = ap.parse_args()
    if args.cmd == "tex":
        out, stats, review = harvest_tex()
        Path(args.json).write_text(json.dumps(out, indent=1, ensure_ascii=False))
        Path(args.review).write_text("\n".join(review) + "\n")
        print(f"candidates: {len(out)}  stats: {dict(stats)}", file=sys.stderr)
    else:
        cmd_apply(args)


if __name__ == "__main__":
    main()
