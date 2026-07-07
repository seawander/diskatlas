#!/usr/bin/env python3
"""Crop survey-figure panels into per-target thumbnails + staging records.

  python3 crop_panels.py manifests/dsharp.json [--dry-run]

Manifest schema: see backend/README.md. Outputs:
  images/<system_id>/<image_id>.png       (<= --max-px on long side, default 560)
  data/staging/<survey>.json              (image records for merge_staging.py)
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def rasterize_pdf(pdf: Path, page: int, dpi: int = 220) -> Image.Image:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "pg"
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-f", str(page),
                        "-l", str(page), str(pdf), str(out)], check=True,
                       capture_output=True)
        files = sorted(Path(td).glob("pg*.png"))
        if not files:
            raise RuntimeError(f"pdftoppm produced nothing for {pdf} p{page}")
        return Image.open(files[0]).convert("RGB").copy()


def load_source(man) -> Image.Image:
    src = ROOT / man["source_image"]
    if src.suffix.lower() == ".pdf":
        return rasterize_pdf(src, man.get("pdf_page") or 1, man.get("dpi", 220))
    return Image.open(src).convert("RGB")


def panels_from_grid(man, W, H):
    g = man["grid"]
    t = g.get("trim_frac", [0, 0, 0, 0])
    x0, y0 = W * t[0], H * t[1]
    gw, gh = W * (1 - t[0] - t[2]), H * (1 - t[1] - t[3])
    rows, cols = g["rows"], g["cols"]
    out = []
    for i, sid in enumerate(g["order"]):
        if sid is None:
            continue
        r, c = divmod(i, cols)
        out.append({
            "id": sid,
            "image_id": g.get("image_id_pattern", "{id}_" + man["survey"]).format(id=sid),
            "bbox": (x0 + c * gw / cols, y0 + r * gh / rows,
                     x0 + (c + 1) * gw / cols, y0 + (r + 1) * gh / rows)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--max-px", type=int, default=560)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    man = json.loads(Path(a.manifest).read_text())
    im = load_source(man)
    W, H = im.size
    plist = []
    if man.get("panels"):
        for p in man["panels"]:
            b = p["bbox_frac"]
            plist.append({"id": p["id"],
                          "image_id": p.get("image_id", f'{p["id"]}_{man["survey"]}'),
                          "bbox": (b[0] * W, b[1] * H, b[2] * W, b[3] * H)})
    elif man.get("grid"):
        plist = panels_from_grid(man, W, H)
    else:
        sys.exit("manifest needs 'panels' or 'grid'")

    staging = []
    for p in plist:
        crop = im.crop(tuple(int(round(v)) for v in p["bbox"]))
        if max(crop.size) > a.max_px:
            f = a.max_px / max(crop.size)
            crop = crop.resize((max(1, int(crop.width * f)),
                                max(1, int(crop.height * f))), Image.LANCZOS)
        rel = f'images/{p["id"]}/{p["image_id"]}.png'
        if not a.dry_run:
            out = ROOT / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            crop.save(out, optimize=True)
        rec = dict(man.get("image_defaults", {}))
        rec.update({"system_id": p["id"], "image_id": p["image_id"], "file": rel,
                    "survey": man.get("survey_name", man["survey"]),
                    "credit": man.get("credit"), "paper": man.get("paper")})
        staging.append(rec)
        print(("DRY " if a.dry_run else "") + rel, crop.size)

    if not a.dry_run:
        st = ROOT / "data" / "staging" / f'{man["survey"]}.json'
        st.parent.mkdir(parents=True, exist_ok=True)
        st.write_text(json.dumps(staging, indent=1, ensure_ascii=False))
        print("staging ->", st)


if __name__ == "__main__":
    main()
