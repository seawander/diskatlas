#!/usr/bin/env python3
"""Validate data/systems/*.json against the schema in data/README.md.

Exit code 1 on ERRORS; warnings (missing coords, unverified papers, missing
image files) are informational. Run before build.py.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / "data" / "systems"

CATS = {"protoplanetary", "debris", "quasar", "evolved"}
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
        # census-consistency audits (these also FAIL build.py):
        # a disk-typed record demands a category; a planet-typed record demands
        # a planets[] entry — otherwise the census misclassifies the system
        img_types = {im.get("type") for im in s.get("images", [])}
        if any(str(t).startswith("disk_") for t in img_types) and not s.get("categories"):
            errors.append(f"{sid}: disk-typed image record(s) but empty categories "
                          f"(adjudicate: resolved disk -> set category; companion-only -> retype record)")
        if "planet" in img_types and not s.get("planets"):
            errors.append(f"{sid}: planet-typed image record(s) but empty planets list "
                          f"(add the companion with name/status/discovery reference)")
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
            # content: continuum vs spectral-line data product. Required on
            # disk_mm (where per-line moment-map records exist); optional on
            # other types (set where meaningful, e.g. Halpha/[SII] jets).
            c = im.get("content")
            if c is not None and c not in ("continuum", "line"):
                errors.append(f"{sid}/{iid}: bad content '{c}' (continuum|line)")
            if im.get("type") == "disk_mm" and c is None:
                errors.append(f"{sid}/{iid}: disk_mm record missing content field")
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
            # credit line must cite the SAME paper as the paper block
            # (catches copy-paste mis-attributions and placeholder credits;
            #  archive-product credits like the ALICE HLSP are exempt)
            cr = im.get("credit") or ""
            fa = p.get("first_author") or ""
            if cr and fa and "HLSP" not in cr and "archive" not in cr.lower():
                deacc = lambda t: unicodedata.normalize("NFKD", t).encode(
                    "ascii", "ignore").decode().lower()
                surname = deacc(fa.split(",")[0].strip())
                cyears = re.findall(r"(?:19|20)\d{2}", cr)
                if surname not in deacc(cr):
                    errors.append(f"{sid}/{iid}: credit does not name paper "
                                  f"first author '{fa}': '{cr[:60]}'")
                elif cyears and str(p.get("year") or "") not in cyears:
                    errors.append(f"{sid}/{iid}: credit year(s) {cyears} != "
                                  f"paper year {p.get('year')}")
            # cited year must match the bibcode's publication year
            bib = p.get("bibcode") or ""
            m = re.match(r"^(\d{4})", bib)
            if m and "arXiv" not in bib and p.get("year") and \
                    int(m.group(1)) != int(p["year"]):
                errors.append(f"{sid}/{iid}: paper year {p['year']} != "
                              f"bibcode year {m.group(1)} ({bib})")

    print(f"systems: {len(ids)}, image records: {n_img}, with local file: {n_file}")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} errors, {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
