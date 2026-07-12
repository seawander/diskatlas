#!/usr/bin/env python3
"""Recover observation epochs from observatory archives (ALMA TAP / MAST / ESO TAP).

Same candidate-JSON shape as epoch_harvest.py, applied with the same gate:

  alma  For each ALMA record still missing an epoch: grep the paper tex for the
        ALMA project code(s) (####.#.#####.S/L/T) and TAP-query ivoa.obscore for
        those codes; match the record by sky position (15" cone) and band; else
        fall back to a position+band cone query bounded by the paper date.
  mast  HST records (ALICE + other HST surveys): query MAST CAOM by position,
        filter instrument + (when stated) filter name, bound by paper year.
  eso   SPHERE records: ESO TAP ivoa.ObsCore by position, instrument SPHERE,
        bound by paper year.

Date policy per record (honest precision):
  all matched executions within 45 d  -> first execution date  YYYY-MM-DD
  within one calendar year            -> YYYY
  spanning years                      -> YYYY-YYYY (range; viewer chips show 1st)
"""
import argparse, glob, json, re, sys, time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "_sources" / "extracted"
CODE_RX = re.compile(r"\b(20\d\d\.[12A]\.\d{5}\.[SLT])\b")

# ALMA band -> wavelength range (um), generous edges
BANDS = {"3": (2400, 3600), "4": (1700, 2400), "5": (1400, 1700), "6": (1050, 1420),
         "7": (780, 1100), "8": (580, 780), "9": (390, 500), "10": (300, 390)}


def mjd_date(mjd):
    from datetime import datetime, timedelta
    return (datetime(1858, 11, 17) + timedelta(days=float(mjd))).strftime("%Y-%m-%d")


def summarize(dates):
    """list of 'YYYY-MM-DD' -> epoch string per the precision policy"""
    if not dates:
        return None
    ds = sorted(set(dates))
    from datetime import date
    def p(s): y, m, d = map(int, s.split("-")); return date(y, m, d)
    if (p(ds[-1]) - p(ds[0])).days <= 45:
        return ds[0]
    years = sorted({s[:4] for s in ds})
    return years[0] if len(years) == 1 else f"{years[0]}-{years[-1]}"


def missing_records(pred):
    out = []
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        for i, im in enumerate(d.get("images", [])):
            if im.get("epoch"):
                continue
            if pred(im):
                out.append((str(f), i, d, im))
    return out


def paper_year(im):
    return (im.get("paper") or {}).get("year") or 2100


def tex_codes(ax):
    d = SRC / (ax or "_none_")
    if not d.is_dir():
        return set()
    txt = ""
    for f in list(d.glob("*.tex")) + list(d.glob("*.txt")):
        try:
            txt += f.read_text(errors="ignore")
        except Exception:
            pass
    return set(CODE_RX.findall(txt))


# ---------------------------------------------------------------- ALMA ------
def cmd_alma(args):
    from astroquery.alma import Alma
    recs = missing_records(lambda im: "ALMA" in (im.get("facility") or ""))
    print(f"ALMA records missing epoch: {len(recs)}", file=sys.stderr)
    # one cone query per system. The queries are pure I/O wait on the TAP
    # service, so they run CONCURRENTLY (6 workers is polite to the archive
    # and turns the ~35-min serial sweep into a few minutes); the matching
    # logic below stays serial and unchanged.
    by_sys = defaultdict(list)
    for f, i, d, im in recs:
        by_sys[d["id"]].append((f, i, d, im))

    def fetch_obs(sid_items):
        sid, items = sid_items
        d = items[0][2]
        ra, dec = d.get("ra_deg"), d.get("dec_deg")
        if ra is None:
            return sid, None
        q = (f"SELECT proposal_id, band_list, t_min, t_max, target_name "
             f"FROM ivoa.obscore WHERE science_observation='T' AND "
             f"CONTAINS(POINT('ICRS',s_ra,s_dec),CIRCLE('ICRS',{ra},{dec},0.005))=1")
        for attempt in (1, 2):
            try:
                rows = Alma.query_tap(q).to_table()
                return sid, [(str(r["proposal_id"]), str(r["band_list"]),
                              float(r["t_min"])) for r in rows]
            except Exception as e:
                if attempt == 2:
                    print(f"  ERR {sid}: {e}", file=sys.stderr)
                    return sid, None
                time.sleep(2)

    from concurrent.futures import ThreadPoolExecutor
    obs_by_sys = {}
    with ThreadPoolExecutor(max_workers=6) as pool_ex:
        for n, (sid, obs) in enumerate(
                pool_ex.map(fetch_obs, sorted(by_sys.items())), 1):
            obs_by_sys[sid] = obs
            if n % 15 == 0:
                print(f"  [fetched {n}/{len(by_sys)}]", file=sys.stderr)

    out = {}
    for n, (sid, items) in enumerate(sorted(by_sys.items()), 1):
        obs = obs_by_sys.get(sid)
        if obs is None:
            continue
        for f, i, dd, im in items:
            wl = im.get("wavelength_um") or 0
            want_bands = {b for b, (lo, hi) in BANDS.items() if lo <= wl <= hi}
            py = paper_year(im)
            codes = tex_codes((im.get("paper") or {}).get("arxiv"))
            # band + before-paper filter
            cand = [(pid, mjd_date(t)) for pid, bl, t in obs
                    if (not want_bands or any(b in bl.split() for b in want_bands))
                    and int(mjd_date(t)[:4]) <= py]
            if not cand:
                continue
            in_code = [(pid, dt) for pid, dt in cand if pid in codes]
            pool = in_code if in_code else cand
            pids = {p for p, _ in pool}
            tier = "code" if in_code else ("cone1" if len(pids) == 1 else "cone")
            if tier == "cone":     # several proposals, none confirmed by tex
                e = summarize([dt for _, dt in pool])
                if e and "-" not in e[4:]:   # only accept year / year-range? no: only exact year
                    pass
                # too ambiguous unless everything collapses to one year
                if e and len(e) == 4:
                    out[im["image_id"]] = dict(epoch=e, tier="alma-year",
                        snippet=f"{len(pids)} proposals, all {e}", file=f, idx=i,
                        arxiv=(im.get("paper") or {}).get("arxiv"), system=sid,
                        instrument=im.get("instrument"), src="alma")
                continue
            e = summarize([dt for _, dt in pool])
            if e:
                out[im["image_id"]] = dict(epoch=e, tier=f"alma-{tier}",
                    snippet=f"proposals {sorted(pids)[:2]}",
                    file=f, idx=i, arxiv=(im.get("paper") or {}).get("arxiv"),
                    system=sid, instrument=im.get("instrument"), src="alma")
        if n % 15 == 0:
            print(f"  [{n}/{len(by_sys)}] candidates so far: {len(out)}", file=sys.stderr)
    Path(args.json).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    from collections import Counter
    print(f"ALMA candidates: {len(out)} {Counter(v['tier'] for v in out.values())}")


# ---------------------------------------------------------------- MAST ------
def cmd_mast(args):
    from astroquery.mast import Observations
    coll = getattr(args, "collection", "HST")
    def is_coll(im):
        return (im.get("facility") or "").startswith(coll)
    recs = missing_records(is_coll)
    print(f"{coll} records missing epoch: {len(recs)}", file=sys.stderr)
    by_sys = defaultdict(list)
    for f, i, d, im in recs:
        by_sys[d["id"]].append((f, i, d, im))
    out = {}
    for n, (sid, items) in enumerate(sorted(by_sys.items()), 1):
        d = items[0][2]
        ra, dec = d.get("ra_deg"), d.get("dec_deg")
        if ra is None:
            continue
        try:
            t = Observations.query_criteria(
                coordinates=f"{ra} {dec}", radius="0.005 deg",
                obs_collection=coll, dataproduct_type="image")
        except Exception as e:
            print(f"  ERR {sid}: {e}", file=sys.stderr)
            time.sleep(2)
            continue
        import math
        rows = []
        for r in t:
            try:
                tm = float(r["t_min"])
                if not math.isnan(tm):
                    rows.append((str(r["instrument_name"]), str(r["filters"]), tm))
            except (TypeError, ValueError):
                pass
        for f, i, dd, im in items:
            instr = (im.get("instrument") or "").upper()
            key = next((k for k in ("NICMOS", "STIS", "ACS", "WFC3", "WFPC2", "FOC",
                                    "NIRCAM", "MIRI", "NIRSPEC")
                        if k in instr), None)
            if key is None:
                continue
            py = paper_year(im)
            # filter-name hint from the record (F110W etc.)
            fm = re.search(r"F\d{3}[WMN]", (im.get("wavelength_label") or "") + " " + instr)
            cand = [mjd_date(t) for ins, filt, t in rows
                    if key in ins.upper() and int(mjd_date(t)[:4]) <= py
                    and (not fm or fm.group(0) in filt)]
            e = summarize(cand)
            if e:
                tier = "mast-exact" if len(e) == 10 else ("mast-year" if len(e) == 4 else "mast-range")
                out[im["image_id"]] = dict(epoch=e, tier=tier,
                    snippet=f"{len(cand)} {key} obs" + (f" [{fm.group(0)}]" if fm else ""),
                    file=f, idx=i, arxiv=(im.get("paper") or {}).get("arxiv"),
                    system=sid, instrument=im.get("instrument"), src="mast")
        if n % 15 == 0:
            print(f"  [{n}/{len(by_sys)}] candidates so far: {len(out)}", file=sys.stderr)
        time.sleep(0.4)
    Path(args.json).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    from collections import Counter
    print(f"MAST candidates: {len(out)} {Counter(v['tier'] for v in out.values())}")


# ----------------------------------------------------------------- ESO ------
def cmd_eso(args):
    import urllib.parse, urllib.request
    def is_sphere(im):
        return "SPHERE" in (im.get("facility") or "") or "SPHERE" in (im.get("instrument") or "")
    recs = missing_records(is_sphere)
    print(f"SPHERE records missing epoch: {len(recs)}", file=sys.stderr)
    by_sys = defaultdict(list)
    for f, i, d, im in recs:
        by_sys[d["id"]].append((f, i, d, im))
    out = {}
    for n, (sid, items) in enumerate(sorted(by_sys.items()), 1):
        d = items[0][2]
        ra, dec = d.get("ra_deg"), d.get("dec_deg")
        if ra is None:
            continue
        q = (f"SELECT t_min, instrument_name FROM ivoa.ObsCore WHERE "
             f"instrument_name LIKE 'SPHERE%' AND "
             f"CONTAINS(POINT('ICRS',s_ra,s_dec),CIRCLE('ICRS',{ra},{dec},0.005))=1")
        url = "https://archive.eso.org/tap_obs/sync?" + urllib.parse.urlencode(
            dict(REQUEST="doQuery", LANG="ADQL", FORMAT="json", QUERY=q))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "diskatlas-epoch"})
            data = json.loads(urllib.request.urlopen(req, timeout=90).read())
            rows = [float(r[0]) for r in data.get("data", []) if r[0] is not None]
        except Exception as e:
            print(f"  ERR {sid}: {e}", file=sys.stderr)
            time.sleep(2)
            continue
        for f, i, dd, im in items:
            py = paper_year(im)
            cand = [mjd_date(t) for t in rows if int(mjd_date(t)[:4]) <= py]
            e = summarize(cand)
            if e:
                tier = "eso-exact" if len(e) == 10 else ("eso-year" if len(e) == 4 else "eso-range")
                out[im["image_id"]] = dict(epoch=e, tier=tier,
                    snippet=f"{len(cand)} SPHERE obs at ESO",
                    file=f, idx=i, arxiv=(im.get("paper") or {}).get("arxiv"),
                    system=sid, instrument=im.get("instrument"), src="eso")
        if n % 15 == 0:
            print(f"  [{n}/{len(by_sys)}] candidates so far: {len(out)}", file=sys.stderr)
        time.sleep(0.5)
    Path(args.json).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    from collections import Counter
    print(f"ESO candidates: {len(out)} {Counter(v['tier'] for v in out.values())}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in [("alma", cmd_alma), ("mast", cmd_mast), ("eso", cmd_eso)]:
        p = sub.add_parser(name)
        p.add_argument("--json", default=str(ROOT / "data" / "paper_finder" / f"epoch_{name}_candidates.json"))
        if name == "mast":
            p.add_argument("--collection", default="HST")
        p.set_defaults(fn=fn)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
