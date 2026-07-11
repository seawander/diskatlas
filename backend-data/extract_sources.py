#!/usr/bin/env python3
"""Unpack images/_sources/arxiv/*.tar into images/_sources/extracted/<id>/.

Handles the three shapes arXiv e-prints come in:
  - tar (usually gzipped) with TeX + figure files  -> extracted as-is
  - single gzipped TeX file                        -> <id>.tex
  - raw PDF (%PDF magic)                           -> <id>.pdf
Also lists candidate figure files per paper (pdf/png/jpg/eps) to help croppers.
"""
import gzip
import shutil
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "_sources" / "arxiv"
DST = ROOT / "images" / "_sources" / "extracted"

FIG_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".eps", ".ps"}


def kind(fp: Path) -> str:
    head = fp.open("rb").read(4)
    if head[:4] == b"%PDF":
        return "pdf"
    if head[:2] == b"\x1f\x8b":
        return "gz"
    return "tar"


def extract_one(fp: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    k = kind(fp)
    if k == "pdf":
        shutil.copy(fp, out / f"{fp.stem}.pdf")
        return "pdf-only"
    try:
        with tarfile.open(fp) as tf:            # handles .tar and .tar.gz
            tf.extractall(out, filter="data")
        return "tar"
    except tarfile.ReadError:
        pass
    if k == "gz":                                # single gzipped file
        with gzip.open(fp, "rb") as g:
            data = g.read()
        suffix = ".pdf" if data[:4] == b"%PDF" else ".tex"
        (out / f"{fp.stem}{suffix}").write_bytes(data)
        return f"gz-single{suffix}"
    return "unknown"


def main():
    if not SRC.exists():
        print("no tarballs yet — run fetch_sources.sh on the host first")
        return
    for fp in sorted(SRC.glob("*.tar")):
        out = DST / fp.stem
        if out.exists() and any(out.iterdir()):
            continue
        try:
            how = extract_one(fp, out)
        except Exception as e:      # in-flight download / corrupt file: skip, retry later
            print(f"{fp.stem}: SKIP ({type(e).__name__}: {e})")
            shutil.rmtree(out, ignore_errors=True)
            continue
        figs = [p.relative_to(out) for p in out.rglob("*") if p.suffix.lower() in FIG_EXT]
        print(f"{fp.stem}: {how}, {len(figs)} figure-ish files")
    print("done ->", DST)


if __name__ == "__main__":
    main()
