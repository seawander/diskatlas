#!/usr/bin/env python3
"""Per-panel imagery licensing manifest (inventory + documentation only).

For every cropped panel in data/systems/*.json records, from its bibliographic
block, the source journal + publisher, a coarse open-access flag, a license class,
whether the source venue is restrictive (Nature / Science / Nature Astronomy /
Nature Communications), and a permission status. NOTHING is deleted -- this is an
audit that feeds the paper's permissions bookkeeping.

license_class:
  archive-product        official archive preview (ALICE / MAST / archive credit)
  arxiv-preprint-figure  cropped from the arXiv source figure package (has arXiv id)
  publisher-pdf          cropped from the publisher PDF (no arXiv; e.g. pre-2000 classics)

permission_status: not-needed | pending | granted. Panels are only *reproduced* in
the atlas paper's figures for a handful of demo systems; the TWA 7 JWST/MIRI panel
(Lagrange et al. 2025, Nature) is marked `pending` (author permission requested).
All restrictive-venue panels are flagged so permission can be sought if a figure is
later reproduced.

Output: data/paper_finder/licensing_manifest.csv

Usage:  python3 backend-data/licensing_manifest.py
"""
import csv, glob, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PUBLISHER = [
    (r'Nature Astronomy|Nature Communications|Nature', "Springer Nature", "restrictive"),
    (r'Science',                                       "AAAS",            "restrictive"),
    (r'A&A|Astronomy and Astrophysics|Astronomy &',    "EDP Sciences",    "hybrid"),
    (r'MNRAS|Monthly Notices',                          "OUP",             "hybrid"),
    (r'PASJ',                                           "OUP",             "hybrid"),
    (r'PASP|ApJ|ApJL|AJ|ApJS|The Astrophysical|The Astronomical', "AAS/IOP", "green-oa"),
    (r'PRL|Physical Review',                            "APS",             "hybrid"),
    (r'AAS Meeting',                                    "AAS (abstract)",  "green-oa"),
    (r'arXiv',                                          "arXiv preprint",  "preprint"),
]

# panels reproduced in the atlas paper -> explicit permission status
PERMISSION = {"twa-7_jwst2025": "pending"}   # Lagrange+2025 Nature 642, 905


def classify_pub(journal):
    for rx, pub, oa in PUBLISHER:
        if re.search(rx, journal, re.I):
            return pub, oa, bool(oa == "restrictive")
    return "unknown", "unknown", False


def license_class(im, arxiv):
    blob = (str(im.get("credit", "")) + " " + str(im.get("survey", ""))).lower()
    if re.search(r"alice|\barchive\b|\bmast\b|preview", blob):
        return "archive-product"
    return "arxiv-preprint-figure" if arxiv else "publisher-pdf"


def main():
    rows = []
    for f in sorted(glob.glob(str(ROOT / "data" / "systems" / "*.json"))):
        d = json.loads(Path(f).read_text())
        for im in d.get("images", []):
            p = im.get("paper", {}) or {}
            journal = (p.get("journal") or "").strip()
            arxiv = (p.get("arxiv") or "").strip()
            pub, oa, restrictive = classify_pub(journal)
            iid = im.get("image_id", "")
            perm = PERMISSION.get(iid, "pending" if False else "not-needed")
            rows.append({
                "system_id": d["id"], "image_id": iid, "file": im.get("file", ""),
                "first_author": p.get("first_author", ""), "year": p.get("year", ""),
                "source_journal": journal, "publisher": pub,
                "open_access": oa, "arxiv": arxiv, "bibcode": p.get("bibcode", ""),
                "license_class": license_class(im, arxiv),
                "restrictive_venue": "Y" if restrictive else "",
                "permission_status": perm,
            })

    out = ROOT / "data" / "paper_finder" / "licensing_manifest.csv"
    cols = ["system_id", "image_id", "file", "first_author", "year", "source_journal",
            "publisher", "open_access", "arxiv", "bibcode", "license_class",
            "restrictive_venue", "permission_status"]
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

    from collections import Counter
    lc = Counter(r["license_class"] for r in rows)
    pub = Counter(r["publisher"] for r in rows)
    restr = [r for r in rows if r["restrictive_venue"]]
    pend = [r for r in rows if r["permission_status"] == "pending"]
    print(f"{len(rows)} panels -> {out}")
    print("license_class:", dict(lc))
    print("publisher:", dict(pub.most_common()))
    print(f"restrictive-venue panels (flagged): {len(restr)}")
    print(f"permission pending: {[r['image_id'] for r in pend]}")


if __name__ == "__main__":
    main()
