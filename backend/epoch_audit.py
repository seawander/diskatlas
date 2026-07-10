#!/usr/bin/env python3
"""Audit observation-epoch coverage of image records.

The paper claims instrument- AND epoch-level records, so every image record should
carry an `epoch` field (observation date, or observation year at minimum; 'unknown'
where the source paper does not state it). This reports the recovered fraction and
lists records still missing an epoch, so the source-verified backfill can be worked
down over time.

Usage:  python3 backend/epoch_audit.py [--list]
"""
import argparse, glob, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="print records missing an epoch")
    a = ap.parse_args()
    tot = have = unknown = 0
    missing = []
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        for im in d.get("images", []):
            tot += 1
            e = (im.get("epoch") or "").strip()
            if e and e.lower() != "unknown":
                have += 1
            elif e.lower() == "unknown":
                unknown += 1
            else:
                missing.append((d["id"], im.get("image_id")))
    print(f"records: {tot}")
    print(f"  with a recovered epoch:      {have} ({100*have/tot:.1f}%)")
    print(f"  explicitly 'unknown':        {unknown}")
    print(f"  missing the epoch field:     {len(missing)} ({100*len(missing)/tot:.1f}%)")
    print(f"  -> epoch coverage (recovered + explicit-unknown): {100*(have+unknown)/tot:.1f}%")
    if a.list:
        for sid, iid in missing:
            print(f"    {sid}/{iid}")


if __name__ == "__main__":
    main()
