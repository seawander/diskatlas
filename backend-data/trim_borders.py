#!/usr/bin/env python3
"""Trim uniform borders (white/gray/black margins) from cropped panel PNGs.

A border row/column is 'uniform' if its pixel std is tiny and its mean is either
very bright (paper background) or matches the corner color. Trims at most 25% per
side (safety). Usage:
  python3 trim_borders.py            # all images/<sys>/*.png
  python3 trim_borders.py PATH...    # specific files
Prints files actually trimmed. Idempotent.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def trim_one(path: Path) -> bool:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape

    def uniform_line(line):          # line: (n,3)
        if line.std(axis=0).max() >= 6:
            return False
        m = line.mean()
        if m > 235 or m < 8:                       # white or black margin
            return True
        chan = line.mean(axis=0)                   # gray margin (low saturation)
        return (chan.max() - chan.min()) < 10 and 40 < m < 235

    top = 0
    while top < h * 0.25 and uniform_line(a[top]):
        top += 1
    bot = h
    while bot > h * 0.75 and uniform_line(a[bot - 1]):
        bot -= 1
    left = 0
    while left < w * 0.25 and uniform_line(a[:, left]):
        left += 1
    right = w
    while right > w * 0.75 and uniform_line(a[:, right - 1]):
        right -= 1

    if (top, left, bot, right) == (0, 0, h, w):
        return False
    im.crop((left, top, right, bot)).save(path, optimize=True)
    return True


def main():
    targets = [Path(p) for p in sys.argv[1:]] or [
        p for p in (ROOT / "images").glob("*/*.png") if "_sources" not in str(p)]
    n = 0
    for p in targets:
        try:
            if trim_one(p):
                n += 1
                print("trimmed", p.relative_to(ROOT))
        except Exception as e:
            print("SKIP", p, e)
    print(f"{n}/{len(targets)} trimmed")


if __name__ == "__main__":
    main()
