#!/usr/bin/env python3
"""Per-system completeness audit for diskatlas.

The citation-graph snowball (find_papers.py) finds papers *near* what we already
have; it is blind to landmark/discovery papers a seed happens not to cite, and to
whole instruments a famous target was imaged with but we never ingested. This tool
attacks the gap from the *target* side instead of the citation graph:

  for each atlas system:
    ask ADS for every refereed paper whose ABSTRACT mentions the system
    (`abs:"<name>"`, i.e. substantively about it), newest-cited first;
    drop the ones already in the atlas;
    keep only those that (a) use a resolved-imaging phrase AND (b) name a
    facility/instrument  -- the "gate";
    score by citations, boosted when the paper names an instrument the system
    does NOT yet have in the atlas (novelty) and penalised for theory/spectroscopy.

The highest-value output is the NEW-INSTR list: famous systems missing an entire
facility. Those cannot be duplicates and directly advance instrument-level
coverage. Everything else is a ranked worklist to VIEW-verify.

ADS is reached with the anonymous bootstrap token (no key needed). Results cache
per system so re-runs and interrupts are cheap.

Usage:
  python3 backend/system_audit.py                    # sweep all systems
  python3 backend/system_audit.py --systems hr-8799,hd-100453
  python3 backend/system_audit.py --top 8 --min-cites 20 --refresh
"""
import argparse, json, re, sys, time, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / "data" / "systems"
OUT = ROOT / "data" / "paper_finder"
CACHE = OUT / "system_audit_cache"

# facility / instrument vocabulary (also used to read a system's existing coverage)
FAC = (r"SPHERE|GPI|ALMA|NIRC2|JWST|NIRCam|MIRI|SCExAO|CHARIS|VISIR|NEAR|NACO|"
       r"LBTI|LBT|MagAO|VisAO|NICMOS|STIS|ACS|WFPC|WFC3|SMA|VLA|Keck|Subaru|"
       r"Gemini|NIRI|NICI|GRAVITY|ERIS|Palomar|P1640|IRDIS|ZIMPOL|Herschel|PACS")
FACRE = re.compile(r"\b(" + FAC + r")\b")
POS = re.compile(
    r"\b(we (present|report|obtain|show|image|resolve)|resolved|scattered[- ]?light|"
    r"coronagraph|polarimetr|polarized|direct(ly)?[- ]imag|high[- ]contrast|"
    r"continuum (image|emission|map)|angular differential|reference[- ]?differential|"
    r"Q_?phi|dust continuum|milli(meter|metre) (image|continuum|emission))\b", re.I)
NEG = re.compile(
    r"\b(retriev|atmospher|abundance|equilibrium chemistr|radial[- ]velocit|"
    r"spectroscop|spectrum|spectra\b|\bSED\b|photometr|light[- ]curve|simulation|"
    r"hydrodynamic|N-?body|population|occurrence|frequency|census|isochrone|"
    r"moving group|membership|kinematic|asteroseismolog|software|package|algorithm|"
    r"pipeline|data reduction)\b", re.I)
# hard-exclude on the TITLE: name-collision / survey-statistics papers that name a
# facility but never image *this* target (beta Pic moving-group L dwarfs, NICI/GPIES
# "frequency" campaigns, brown-dwarf samples, ...).
TITLE_NEG = re.compile(
    r"\b(moving group|field (L|T|brown) dwarf|(L|T) dwarf|brown dwarf|census|"
    r"sample of|planet-finding campaign|frequency of|occurrence|demographics|"
    r"population|orbit(al)? (fit|analysis|distribution)|dynamical mass)\b", re.I)
# far-IR facilities that almost never *resolve* a disk -> don't treat as a headline
# instrument gap (still listed, just not boosted/flagged as NEW-INSTR).
LOWRES = {"HERSCHEL", "PACS", "SPITZER"}
# disk/companion context REQUIRED in title+abstract. Short catalog names (DO Tau,
# T Tau, AS 205, SO 844...) collide with cosmology/quasar/RV-survey abstracts in
# ADS abs: search -- e.g. abs:"DO Tau" matched Planck 2018. Those never pass this.
DISK_CTX = re.compile(
    r"\b(circumstellar|protoplanetary|planet-?forming|transition(al)? dis[ck]|"
    r"debris dis[ck]|dis[ck] around|the dis[ck]|young stellar object|YSO|"
    r"T Tauri|Herbig|pre-main[- ]sequence|protostar|companion|substellar|"
    r"brown dwarf|(exo)?planet|jet|outflow|envelope)\b", re.I)


def ads_token():
    return json.loads(urllib.request.urlopen(
        "https://ui.adsabs.harvard.edu/v1/accounts/bootstrap", timeout=60
    ).read())["access_token"]


def ads_query(tok, q, fl, rows=120, sort="citation_count desc", tries=4):
    p = {"q": q, "fl": fl, "rows": str(rows), "sort": sort}
    url = "https://api.adsabs.harvard.edu/v1/search/query?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    for i in range(tries):
        try:
            return json.loads(urllib.request.urlopen(req, timeout=90).read())["response"]["docs"]
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < tries - 1:
                time.sleep(2 * (i + 1)); continue
            raise


def system_names(d):
    names = [d.get("name") or d["id"]]
    for a in d.get("aliases", []) or []:
        names.append(a)
    # add a de-spaced variant (HD 100453 -> HD100453) which abstracts often use
    extra = set()
    for n in names:
        c = re.sub(r"([A-Za-z]+)\s+(\d)", r"\1\2", n)
        if c != n:
            extra.add(c)
    return list(dict.fromkeys(names + list(extra)))


def covered(d):
    inst = set()
    for im in d.get("images", []):
        for k in (im.get("facility", ""), im.get("instrument", "")):
            for m in FACRE.findall(str(k)):
                inst.add(m.upper())
    return inst


def audit_system(tok, f, top, min_cites, refresh):
    d = json.loads(f.read_text())
    sid = d["id"]
    cf = CACHE / f"{sid}.json"
    if cf.exists() and not refresh:
        raw = json.loads(cf.read_text())
    else:
        names = system_names(d)
        qexpr = "(" + " OR ".join(f'abs:"{n}"' for n in names) + ") property:refereed"
        raw = ads_query(tok, qexpr, "bibcode,title,citation_count,year,identifier,abstract")
        CACHE.mkdir(parents=True, exist_ok=True)
        cf.write_text(json.dumps(raw))
        time.sleep(0.34)

    bib = {im["paper"]["bibcode"] for im in d.get("images", [])
           if im.get("paper", {}).get("bibcode")}
    arx = {im["paper"]["arxiv"].lower() for im in d.get("images", [])
           if im.get("paper", {}).get("arxiv")}
    inst = covered(d)

    cands = []
    for x in raw:
        if x["bibcode"] in bib:
            continue
        ids = [i.split(":")[-1].lower() for i in x.get("identifier", []) if i.startswith("arXiv:")]
        if any(a in arx for a in ids):
            continue
        title = x["title"][0]
        if TITLE_NEG.search(title):                 # hard drop: collisions / surveys
            continue
        blob = title + " " + x.get("abstract", "")
        facs = {m.upper() for m in FACRE.findall(blob)}
        if not (POS.search(blob) and facs and DISK_CTX.search(blob)):   # the gate
            continue
        cites = x.get("citation_count", 0) or 0
        if cites < min_cites:
            continue
        novel = sorted(facs - inst)
        novel_hi = [n for n in novel if n not in LOWRES]   # resolving-instrument gaps only
        neg = bool(NEG.search(blob))
        score = cites * (1 - 0.6 * neg) * (1.8 if novel_hi else 1.0)
        cands.append({"bibcode": x["bibcode"], "arxiv": (ids[0] if ids else None),
                      "year": x["year"], "citations": cites, "title": title,
                      "facilities": sorted(facs), "novel_instruments": novel_hi,
                      "novel_lowres": [n for n in novel if n in LOWRES],
                      "neg": neg, "score": round(score, 1)})
    cands.sort(key=lambda c: -c["score"])
    return {"id": sid, "name": d.get("name"), "covered_instruments": sorted(inst),
            "n_raw": len(raw), "candidates": cands[:top]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systems", help="comma-separated system ids (default: all)")
    ap.add_argument("--top", type=int, default=8, help="candidates kept per system")
    ap.add_argument("--min-cites", type=int, default=15)
    ap.add_argument("--refresh", action="store_true", help="ignore cache")
    a = ap.parse_args()

    files = sorted(SYS.glob("*.json"))
    if a.systems:
        want = set(a.systems.split(","))
        files = [f for f in files if json.loads(f.read_text())["id"] in want]

    tok = ads_token()
    report, newinstr = {}, []
    for i, f in enumerate(files, 1):
        try:
            r = audit_system(tok, f, a.top, a.min_cites, a.refresh)
        except Exception as e:
            print(f"  ! {f.stem}: {e}", file=sys.stderr); continue
        report[r["id"]] = r
        for c in r["candidates"]:
            if c["novel_instruments"]:
                newinstr.append((c["citations"], r["id"], c))
        print(f"[{i}/{len(files)}] {r['id']:22s} raw={r['n_raw']:3d} "
              f"gaps={len(r['candidates'])}"
              + (f"  NEW-INSTR:{','.join(sorted({j for c in r['candidates'] for j in c['novel_instruments']}))}"
                 if any(c['novel_instruments'] for c in r['candidates']) else ""),
              file=sys.stderr)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "system_gaps.json").write_text(json.dumps(report, indent=1))

    newinstr.sort(key=lambda t: -t[0])
    print("\n==== NEW-INSTRUMENT GAPS (famous systems missing a whole facility) ====")
    print(f"{'cites':>5} {'system':22s} {'missing':16s} {'year':4s} paper")
    for cites, sid, c in newinstr[:40]:
        print(f"{cites:5d} {sid:22s} {','.join(c['novel_instruments'])[:16]:16s} "
              f"{c['year']:4s} {c['bibcode']}  {c['title'][:48]}")
    print(f"\nfull per-system worklist -> {OUT/'system_gaps.json'}")


if __name__ == "__main__":
    main()
