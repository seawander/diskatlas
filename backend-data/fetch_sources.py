#!/usr/bin/env python3
"""Fetch missing arXiv source packages (e-print tarballs) into images/_sources/extracted/.

Only .tex/.bbl/.txt members are kept (we parse text, not figures). Papers whose
e-print is a bare PDF get a <id>/SOURCE_IS_PDF marker so we don't refetch.
Polite: 3 s between fetches. Writes progress to stderr; safe to re-run.

Usage: python3 backend-data/fetch_sources.py [--only-missing-epoch]
"""
import glob, io, json, os, sys, tarfile, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "images" / "_sources" / "extracted"


def wanted_papers():
    axs = set()
    for f in glob.glob(str(ROOT / "data" / "systems" / "*.json")):
        d = json.load(open(f))
        for im in d.get("images", []):
            if im.get("epoch"):
                continue
            ax = (im.get("paper") or {}).get("arxiv")
            if ax:
                axs.add(ax)
    return axs


def main():
    todo = sorted(ax for ax in wanted_papers() if not (DEST / ax).exists())
    print(f"fetching {len(todo)} source packages", file=sys.stderr)
    ok = pdf = err = 0
    for n, ax in enumerate(todo, 1):
        url = f"https://arxiv.org/e-print/{ax}"
        outdir = DEST / ax
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "diskatlas-epoch-harvest (mailto:renrenbinbin@gmail.com)"})
            data = urllib.request.urlopen(req, timeout=90).read()
            outdir.mkdir(parents=True, exist_ok=True)
            if data[:4] == b"%PDF":
                (outdir / "SOURCE_IS_PDF").write_bytes(b"")
                (outdir / f"{ax}.pdf").write_bytes(data)
                pdf += 1
            else:
                try:
                    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
                        for m in tf.getmembers():
                            if m.isfile() and m.name.lower().endswith((".tex", ".bbl", ".txt")) and m.size < 20_000_000:
                                base = os.path.basename(m.name)
                                (outdir / base).write_bytes(tf.extractfile(m).read())
                    ok += 1
                except tarfile.TarError:
                    # single gzipped tex file
                    import gzip
                    try:
                        (outdir / "main.tex").write_bytes(gzip.decompress(data))
                        ok += 1
                    except Exception:
                        (outdir / "main.tex").write_bytes(data)  # plain tex
                        ok += 1
        except Exception as e:
            err += 1
            print(f"  ERR {ax}: {e}", file=sys.stderr)
        if n % 20 == 0:
            print(f"  [{n}/{len(todo)}] ok={ok} pdf={pdf} err={err}", file=sys.stderr)
        time.sleep(3)
    print(f"done: ok={ok} pdf-only={pdf} err={err}", file=sys.stderr)


if __name__ == "__main__":
    main()
