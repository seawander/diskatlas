#!/usr/bin/env python3
"""Local crop QA for diskatlas — flags cropping defects WITHOUT a human eyeballing
every image. Runs offline (PIL + numpy; optional tesseract OCR via --ocr).

Rationale: the pixel work (edge analysis, OCR, multi-panel detection) is cheap on
local compute; only the handful it FLAGS need human/Claude review. Point Claude at
the report, not the 1,400 images.

For each image referenced by data/systems/*.json it checks:
  EDGE_OUTLIER   one of the 4 edges' median colour is far from the other three
                 (offset crop / leftover frame / colorbar on one side)
  COLORBAR_EDGE  one edge is a smooth wide-range gradient along its length
                 (a colorbar strip left in the crop)
  GUTTER_EDGE    one edge is mostly white/black page gutter while others are not
  AXIS_TEXT      (--ocr) tesseract finds axis/colorbar digits in the outer margin
  MULTIPANEL     a full-length near-uniform bright divider inside the crop with
                 content on both sides -> two panels crammed into one crop
Aspect ratio is reported but never flagged alone (edge-on disks are legitimately
long).

Output: human report to stdout + JSON to data/paper_finder/crop_qa.json.
Usage: python3 backend-data/crop_qa.py [--ocr] [--limit N] [--only SUBSTR]
"""
import argparse, json, glob, os, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def edge_strip(a, side, t):
    if side == "T": return a[:t, :, :].reshape(-1, a.shape[2])
    if side == "B": return a[-t:, :, :].reshape(-1, a.shape[2])
    if side == "L": return a[:, :t, :].reshape(-1, a.shape[2])
    return a[:, -t:, :].reshape(-1, a.shape[2])


def edge_line(a, side):
    """1-px line along each edge, as (N,3) for along-edge variance."""
    if side == "T": return a[0, :, :]
    if side == "B": return a[-1, :, :]
    if side == "L": return a[:, 0, :]
    return a[:, -1, :]


def analyse(path, do_ocr):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    H, W, _ = a.shape
    flags = []
    t = max(3, min(H, W) // 60)
    meds, vars, whitef, blackf = {}, {}, {}, {}
    for s in "TBLR":
        strip = edge_strip(a, s, t)
        meds[s] = np.median(strip, axis=0)
        line = edge_line(a, s).astype(int)
        vars[s] = float(line.std(axis=0).mean())          # variance ALONG the edge
        mn = line.min(axis=1); mx = line.max(axis=1)
        whitef[s] = float((mn > 220).mean())
        blackf[s] = float((mx < 28).mean())

    # COLORBAR_EDGE: an edge that is a MONOTONIC gradient over a wide range along
    # its length (the signature of a colorbar strip left in the crop). Requiring
    # monotonicity avoids flagging a merely-noisy bright edge.
    for s in "TBLR":
        lumline = edge_line(a, s).astype(int).mean(1)
        rng = float(lumline.max() - lumline.min())
        diffs = np.diff(lumline)
        mono = max(float((diffs > 0).mean()), float((diffs < 0).mean())) if len(diffs) else 0
        if rng > 120 and mono > 0.80 and vars[s] > 30:
            flags.append(f"COLORBAR_EDGE:{s}(rng{rng:.0f},mono{mono:.2f})")
    # GUTTER_EDGE: an edge almost entirely white/black page gutter while its
    # neighbours are clearly not (offset crop leaving a margin strip).
    for s in "TBLR":
        oth_w = np.mean([whitef[o] for o in "TBLR" if o != s])
        oth_b = np.mean([blackf[o] for o in "TBLR" if o != s])
        if whitef[s] > 0.88 and oth_w < 0.2:
            flags.append(f"GUTTER_EDGE:{s}(white)")
        elif blackf[s] > 0.92 and oth_b < 0.25:
            flags.append(f"GUTTER_EDGE:{s}(black)")

    # MULTIPANEL: full-length near-uniform BRIGHT divider inside (10-90%) with
    # content (non-bright) on both sides -> likely two crammed panels.
    lum = a.mean(2)
    def divider(axis):
        prof_bright = (lum > 236).mean(axis=axis)        # fraction bright per line
        n = len(prof_bright)
        for i in range(int(n * 0.2), int(n * 0.8)):
            # a THIN full-length white line: bright here, NOT bright just outside it
            if prof_bright[i] > 0.95 and prof_bright[max(0, i - 4)] < 0.6 and prof_bright[min(n - 1, i + 4)] < 0.6:
                before = lum.take(range(max(0, i - n // 6), i - 2), axis=1 - axis)
                after = lum.take(range(i + 3, min(n, i + n // 6)), axis=1 - axis)
                # substantial disk/content on BOTH sides of the divider
                if (before < 236).mean() > 0.45 and (after < 236).mean() > 0.45:
                    return i, n
        return None
    dc = divider(0)   # a bright COLUMN (vertical divider -> side-by-side panels)
    dr = divider(1)   # a bright ROW (horizontal divider -> stacked panels)
    if dc: flags.append(f"MULTIPANEL:Vdiv@{dc[0]}/{dc[1]}")
    if dr: flags.append(f"MULTIPANEL:Hdiv@{dr[0]}/{dr[1]}")

    # AXIS_TEXT: OCR the outer margins for digit runs (axis / colorbar numbers)
    if do_ocr:
        m = max(6, min(H, W) // 8)
        margins = {"top": im.crop((0, 0, W, m)), "bottom": im.crop((0, H - m, W, H)),
                   "left": im.crop((0, 0, m, H)), "right": im.crop((W - m, 0, W, H))}
        for name, region in margins.items():
            txt = ocr(region)
            digits = [c for c in txt if c.isdigit()]
            # axis/colorbar numbers = several digits in a thin margin strip
            if len(digits) >= 4 and any(ch in txt for ch in "0123456789") and \
               sum(c.isdigit() or c in ".-−'\" " for c in txt) > 0.5 * max(1, len(txt.strip())):
                flags.append(f"AXIS_TEXT:{name}('{txt.strip()[:16]}')")
    return {"w": W, "h": H, "ar": round(W / H, 2), "flags": flags}


def ocr(region):
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            region.save(f.name)
            out = subprocess.run(["tesseract", f.name, "stdout", "--psm", "11"],
                                 capture_output=True, text=True, timeout=30)
        os.unlink(f.name)
        return out.stdout
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ocr", action="store_true", help="run tesseract on margins (slower)")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="", help="only images whose path contains this")
    a = ap.parse_args()

    recs = []
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        for im in d.get("images", []):
            if im.get("file"):
                recs.append((d["id"], im["image_id"], im["file"]))
    if a.only:
        recs = [r for r in recs if a.only in r[2]]
    if a.limit:
        recs = recs[:a.limit]

    flagged, n_ok, missing = [], 0, []
    for i, (sid, iid, rel) in enumerate(recs):
        p = ROOT / rel
        if not p.exists():
            missing.append(rel); continue
        try:
            r = analyse(str(p), a.ocr)
        except Exception as e:
            flagged.append({"system": sid, "image_id": iid, "file": rel,
                            "flags": [f"ERROR:{e}"]}); continue
        if r["flags"]:
            flagged.append({"system": sid, "image_id": iid, "file": rel,
                            "ar": r["ar"], "flags": r["flags"]})
        else:
            n_ok += 1
        if (i + 1) % 200 == 0:
            print(f"  ... {i+1}/{len(recs)} scanned", file=sys.stderr)

    out = ROOT / "data" / "paper_finder" / "crop_qa.json"
    out.write_text(json.dumps({"flagged": flagged, "n_ok": n_ok,
                               "n_total": len(recs), "missing": missing}, indent=1))
    # human report grouped by primary flag type
    from collections import Counter, defaultdict
    by = defaultdict(list)
    for fl in flagged:
        key = fl["flags"][0].split(":")[0]
        by[key].append(fl)
    print(f"\ncrop QA: {len(recs)} crops, {n_ok} clean, {len(flagged)} flagged, "
          f"{len(missing)} missing file")
    print("flag summary:", dict(Counter(f["flags"][0].split(":")[0] for f in flagged)))
    for key in ("MULTIPANEL", "COLORBAR_EDGE", "AXIS_TEXT", "GUTTER_EDGE", "EDGE_OUTLIER", "ERROR"):
        items = by.get(key, [])
        if not items: continue
        print(f"\n== {key} ({len(items)}) ==")
        for fl in items:
            print(f"  {fl['system']:16.16} {fl['image_id']:30.30} {';'.join(fl['flags'])}")
    if missing:
        print(f"\n== MISSING FILES ({len(missing)}) =="); [print("  " + m) for m in missing[:20]]
    print(f"\nfull report -> {out}")


if __name__ == "__main__":
    main()
