#!/usr/bin/env python3
"""Validate data/systems/*.json against the schema in data/README.md.

Exit code 1 on ERRORS; warnings (missing coords, unverified papers, missing
image files) are informational. Run before build.py.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / "data" / "systems"

CATS = {"protoplanetary", "debris", "quasar"}
TYPES = {"disk_mm", "disk_scattered", "planet", "quasar"}
PSTAT = {"confirmed", "candidate", "disputed", "dust-cloud", "refuted"}


def main():
    errors, warns = [], []
    ids = {}
    n_img = n_file = 0
    for f in sorted(SYS.glob("*.json")):
        try:
            s = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"{f.name}: bad JSON ({e})")
            continue
        sid = s.get("id")
        if sid != f.stem:
            errors.append(f"{f.name}: id '{sid}' != filename")
        if sid in ids:
            errors.append(f"duplicate id {sid}")
        ids[sid] = 1
        if not s.get("name"):
            errors.append(f"{sid}: missing name")
        if s.get("ra_deg") is None or s.get("dec_deg") is None:
            warns.append(f"{sid}: no coordinates (won't appear on the sky map)")
        elif not (0 <= s["ra_deg"] < 360 and -90 <= s["dec_deg"] <= 90):
            errors.append(f"{sid}: RA/Dec out of range")
        for c in s.get("categories", []):
            if c not in CATS:
                errors.append(f"{sid}: bad category '{c}'")
        for p in s.get("planets", []):
            if p.get("status", "confirmed") not in PSTAT:
                errors.append(f"{sid}: bad planet status '{p.get('status')}'")
        seen_img = set()
        for im in s.get("images", []):
            n_img += 1
            iid = im.get("image_id")
            if not iid or iid in seen_img:
                errors.append(f"{sid}: missing/duplicate image_id '{iid}'")
            seen_img.add(iid)
            if im.get("type") not in TYPES:
                errors.append(f"{sid}/{iid}: bad type '{im.get('type')}'")
            if not isinstance(im.get("wavelength_um"), (int, float)):
                errors.append(f"{sid}/{iid}: wavelength_um must be a number")
            p = im.get("paper") or {}
            if not p.get("arxiv") and not p.get("bibcode"):
                warns.append(f"{sid}/{iid}: paper has neither arxiv nor bibcode")
            if p.get("_verify"):
                warns.append(f"{sid}/{iid}: paper metadata marked _verify")
            if p.get("arxiv") and not re.match(r"^(\d{4}\.\d{4,5}|[a-z-]+/\d{7})$",
                                               p["arxiv"]):
                errors.append(f"{sid}/{iid}: malformed arxiv id '{p['arxiv']}'")
            fl = im.get("file")
            if fl:
                fp = ROOT / fl
                if not fp.exists():
                    errors.append(f"{sid}/{iid}: file missing on disk: {fl}")
                else:
                    n_file += 1
                    if fp.stat().st_size > 400_000:
                        warns.append(f"{sid}/{iid}: file > 400 KB")

    print(f"systems: {len(ids)}, image records: {n_img}, with local file: {n_file}")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} errors, {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
