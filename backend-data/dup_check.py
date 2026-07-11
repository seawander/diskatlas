#!/usr/bin/env python3
"""Duplicate-crop detector for diskatlas.

Default (reliable, no false positives): report byte-identical (md5) crops shared
by 2+ records — an actual duplicate (same figure ingested twice, or a split panel
saved to two records).

--near: additionally run a DCT perceptual-hash near-duplicate pass, all-pairs
Hamming distance on the GPU (torch.cuda / the GB10 if available). CAVEAT: pHash is
NOISY on this dataset — faint interferometric/radio crops (a tiny source on empty
background) and legitimately-similar multi-band records of the same disk both
collide, so --near is mostly false positives here. Kept for scale/other datasets.

Usage: python3 backend-data/dup_check.py [--near] [--maxdist 2]
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

try:
    import torch
    DEV = "cuda" if torch.cuda.is_available() else "cpu"
except Exception:
    torch = None
    DEV = "cpu"


def dct2(a):
    """2D DCT-II via numpy (small 32x32, plenty fast on CPU)."""
    from numpy.fft import rfft
    N = a.shape[0]
    # separable DCT through the standard cosine basis
    k = np.arange(N)
    basis = np.cos(np.pi * (2 * k[:, None] + 1) * k[None, :] / (2 * N))
    return basis @ a @ basis.T


def phash(path, hz=32, keep=8):
    im = Image.open(path).convert("L").resize((hz, hz), Image.BILINEAR)
    a = np.asarray(im, dtype=np.float64)
    d = dct2(a)[:keep, :keep]            # low-freq block
    d[0, 0] = 0                          # drop DC
    bits = (d > np.median(d)).flatten()  # keep-1 length after DC? use full block
    return bits.astype(np.uint8)


def main():
    import hashlib
    from collections import defaultdict
    ap = argparse.ArgumentParser()
    ap.add_argument("--near", action="store_true", help="also run GPU pHash near-dup (noisy)")
    ap.add_argument("--maxdist", type=int, default=2, help="max Hamming distance (of 64 bits)")
    a = ap.parse_args()

    recs = []
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        for im in d.get("images", []):
            if im.get("file") and (ROOT / im["file"]).exists():
                recs.append((d["id"], im["image_id"], im["file"]))

    # reliable exact-duplicate pass (md5)
    h2 = defaultdict(list)
    for sid, iid, p in recs:
        h2[hashlib.md5((ROOT / p).read_bytes()).hexdigest()].append((sid, iid, p))
    exact = [g for g in h2.values() if len(g) > 1]
    print(f"{len(recs)} crops; {len(exact)} byte-identical duplicate group(s)")
    for g in exact:
        print("  EXACT DUP:  " + "  <->  ".join(f"{s}/{i}" for s, i, _ in g))
    if not a.near:
        print("(run with --near for the GPU pHash pass; note it is noisy on faint crops)")
        return

    print(f"\nhashing {len(recs)} crops for near-dup (device={DEV}) ...", file=sys.stderr)
    H = np.stack([phash(str(ROOT / r[2])) for r in recs])   # (N, 64) uint8 bits
    N, B = H.shape

    # all-pairs Hamming distance on GPU: pack bits, XOR, popcount
    if torch is not None:
        bits = torch.tensor(H, device=DEV, dtype=torch.float32)      # (N,B)
        # hamming(i,j) = sum |bi - bj| = |bi|+|bj| - 2 bi.bj  (bits in {0,1})
        ones = bits.sum(1, keepdim=True)                             # (N,1)
        dot = bits @ bits.T                                          # (N,N)
        ham = ones + ones.T - 2 * dot
        ham = ham.cpu().numpy()
    else:
        ham = (H[:, None, :] != H[None, :, :]).sum(2)

    pairs = []
    for i in range(N):
        for j in range(i + 1, N):
            if ham[i, j] <= a.maxdist:
                pairs.append((int(ham[i, j]), recs[i], recs[j]))
    pairs.sort(key=lambda p: p[0])

    same = [p for p in pairs if p[1][0] == p[2][0]]
    cross = [p for p in pairs if p[1][0] != p[2][0]]
    out = ROOT / "data" / "paper_finder" / "dup_check.json"
    out.write_text(json.dumps({
        "cross_system": [{"dist": d, "a": {"system": ai, "image_id": aj, "file": af},
                          "b": {"system": bi, "image_id": bj, "file": bf}}
                         for d, (ai, aj, af), (bi, bj, bf) in cross],
        "same_system": [{"dist": d, "system": ai, "a": aj, "b": bj}
                        for d, (ai, aj, af), (bi, bj, bf) in same],
    }, indent=1))

    print(f"\n{len(recs)} crops, {len(pairs)} near-dup pairs (Hamming<= {a.maxdist})")
    print(f"  cross-system (likely real duplicates): {len(cross)}")
    print(f"  same-system  (often legit epochs/bands): {len(same)}")
    if cross:
        print("\n== CROSS-SYSTEM near-duplicates (review these) ==")
        for d, (ai, aj, _), (bi, bj, _) in cross:
            print(f"  dist={d:2d}  {ai}/{aj}  <->  {bi}/{bj}")
    if same:
        print("\n== SAME-SYSTEM near-duplicates ==")
        for d, (ai, aj, _), (_, bj, _) in same[:40]:
            print(f"  dist={d:2d}  {ai}: {aj}  <->  {bj}")
    print(f"\nfull report -> {out}")


if __name__ == "__main__":
    main()
