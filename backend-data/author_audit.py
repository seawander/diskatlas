#!/usr/bin/env python3
"""Author-axis completeness audit.

The discovery machinery is target- and citation-based (snowball, fresh_papers,
system_audit). This sweeps the THIRD axis the 2026-07-10 session showed was
leaking: prolific first-authors. If someone has N papers in the atlas, their
other imaging papers are prime candidates (the HD 32297/Olofsson 2022 gap was
found exactly this way, after the user asked "try his papers on ADS").

For every first-author with >= --min-records in-atlas records (plus any names in
EXTRA), query anonymous ADS for their first-author refereed papers, drop what
the two ledgers already cover, keep titles that smell like resolved imaging,
and print a per-author triage list. Dispositions belong in
data/paper_finder_state.json as usual.

Usage: python3 backend-data/author_audit.py [--min-records 8] [--year-from 2003]
"""
import argparse, glob, json, re, time, urllib.parse, urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# always sweep these names regardless of record count (maintainer + close
# collaborators whose papers the user keeps supplying by hand)
EXTRA = ["Ren", "Xie", "Olofsson", "Milli", "Benisty", "Ginski", "Perrot",
         "Boccaletti", "Lagrange", "Currie", "Wagner"]

IMG_KW = re.compile(r"imag|disk|disc|ring|companion|planet|polari|scattered|"
                    r"coronagraph|resolved|spiral|belt|dust|debris|proto", re.I)
SKIP_KW = re.compile(r"spectroscop|radial velocit|transit(ing|s)?\b|photometric survey|"
                     r"catalog|asteroseism|abundanc|atmospher.*retriev|interior|"
                     r"population synthesis|simulat|N-body|review", re.I)


def ads_token():
    req = urllib.request.Request("https://ui.adsabs.harvard.edu/v1/accounts/bootstrap",
                                 headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())["access_token"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-records", type=int, default=8)
    ap.add_argument("--year-from", type=int, default=2003)
    a = ap.parse_args()

    fa = Counter()
    atlas_ids = set()
    for f in glob.glob(str(ROOT / "data" / "systems" / "*.json")):
        d = json.load(open(f))
        papers = [im.get("paper") for im in d.get("images", [])]
        for pl in d.get("planets", []):
            papers.append(pl.get("paper"))
            papers += pl.get("extra_papers", [])
        for p in papers:
            if not p:
                continue
            if p.get("first_author"):
                fa[p["first_author"]] += 1
            for k in ("arxiv", "bibcode"):
                if p.get(k):
                    atlas_ids.add(p[k])
    state = set(json.load(open(ROOT / "data" / "paper_finder_state.json")))
    names = sorted({n for n, c in fa.items() if c >= a.min_records} | set(EXTRA))
    print(f"sweeping {len(names)} first-authors (>= {a.min_records} records or EXTRA)\n")

    tok = ads_token()
    total_flag = 0
    for name in names:
        # abs-level disk context kills same-surname strangers (geology Zhangs,
        # lensing Wagners...) that a bare surname query drags in
        q = urllib.parse.quote(
            f'author:"^{name}" collection:astronomy property:refereed '
            f'year:{a.year_from}-2026 '
            f'abs:("circumstellar disk" OR "protoplanetary disk" OR "debris disk" '
            f'OR "direct imaging" OR coronagraph OR "scattered light")')
        url = (f"https://api.adsabs.harvard.edu/v1/search/query?q={q}"
               f"&fl=bibcode,title,year,identifier&rows=200&sort=date+desc")
        try:
            r = json.loads(urllib.request.urlopen(
                urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"}),
                timeout=40).read())
        except Exception as e:
            print(f"[{name}] ADS error: {e}")
            time.sleep(2)
            continue
        flags = []
        for doc in r["response"]["docs"]:
            ax = next((i[6:] for i in doc.get("identifier", []) if i.startswith("arXiv:")), None)
            if (ax and ax in atlas_ids) or doc["bibcode"] in atlas_ids:
                continue
            if ax and ax in state:
                continue
            title = (doc.get("title") or [""])[0]
            if not IMG_KW.search(title) or SKIP_KW.search(title):
                continue
            flags.append((doc["year"], ax or doc["bibcode"], title[:90]))
        if flags:
            print(f"[{name}] ({fa.get(name, 0)} in-atlas records) — {len(flags)} candidates:")
            for y, i, t in flags[:12]:
                print(f"    {y}  {i:22s}  {t}")
            total_flag += len(flags)
        time.sleep(0.5)
    print(f"\ntotal candidates: {total_flag} — VIEW figures before ingesting (titles lie);"
          f" record dispositions in paper_finder_state.json")


if __name__ == "__main__":
    main()
