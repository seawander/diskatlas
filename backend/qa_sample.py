#!/usr/bin/env python3
"""Generate a stratified random human-QA sample of image records.

Draws N records (default 100) stratified by wavelength band x ingestion route, so
every band and route is represented for manual verification. Writes two files to
data/paper_finder/:
  qa_sample.csv   one row per record + empty verdict columns (fill by hand)
  qa_sample.html  the same as a clickable checklist with the panel thumbnail

Route proxy (the per-record ingestion route is not stored, so we infer it):
  survey   -> record carries a non-null `survey` field (a survey-gallery crop)
  targeted -> everything else (per-system sweep or snowball-discovered paper)

Verdict columns are LEFT BLANK for a human. Feed the completed CSV to
backend/qa_score.py to get per-field error rates with binomial confidence
intervals for the paper's QA section.

Usage:  python3 backend/qa_sample.py [--n 100] [--seed 20260709]
"""
import argparse, csv, json, random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "paper_finder"

VERDICTS = ["target_ok", "instrument_ok", "wavelength_ok", "reference_ok", "crop_clean"]


def band(um):
    if um is None:
        return "nir"
    return "vis" if um < 1 else "nir" if um < 5 else "mir" if um < 300 else "mm"


def collect():
    recs = []
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        for im in d.get("images", []):
            p = im.get("paper", {}) or {}
            recs.append({
                "system": d.get("name"), "system_id": d["id"],
                "image_id": im.get("image_id"),
                "thumbnail": im.get("file", ""),
                "claimed_instrument": f'{im.get("facility","")} / {im.get("instrument","")}',
                "claimed_wavelength": im.get("wavelength_label", ""),
                "wavelength_um": im.get("wavelength_um"),
                "claimed_source_figure": im.get("credit", ""),
                "bibcode": p.get("bibcode", ""), "arxiv": p.get("arxiv", ""),
                "band": band(im.get("wavelength_um")),
                "route": "survey" if im.get("survey") else "targeted",
            })
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20260709)
    a = ap.parse_args()
    random.seed(a.seed)

    recs = collect()
    strata = defaultdict(list)
    for r in recs:
        strata[(r["band"], r["route"])].append(r)

    # proportional allocation with >=1 per non-empty stratum, then top up to n
    total = len(recs)
    sample, picked = [], set()
    for key, group in strata.items():
        k = max(1, round(a.n * len(group) / total))
        for r in random.sample(group, min(k, len(group))):
            sample.append(r); picked.add(r["image_id"])
    pool = [r for r in recs if r["image_id"] not in picked]
    random.shuffle(pool)
    while len(sample) < a.n and pool:
        r = pool.pop()
        sample.append(r); picked.add(r["image_id"])
    sample = sample[:a.n]
    random.shuffle(sample)

    cols = ["system", "system_id", "image_id", "band", "route", "thumbnail",
            "claimed_instrument", "claimed_wavelength", "claimed_source_figure",
            "bibcode", "arxiv"] + VERDICTS + ["notes"]
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "qa_sample.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sample:
            w.writerow({**{c: r.get(c, "") for c in cols}, **{v: "" for v in VERDICTS}, "notes": ""})

    # HTML checklist (thumbnails clickable, verdict cells editable-looking)
    rows = []
    for i, r in enumerate(sample, 1):
        thumb = f'<img src="../../{r["thumbnail"]}" style="height:64px">' if r["thumbnail"] else ""
        ref = r["arxiv"] or r["bibcode"]
        rows.append(
            f'<tr><td>{i}</td><td><b>{r["system"]}</b><br><small>{r["image_id"]}</small></td>'
            f'<td>{thumb}</td><td>{r["claimed_instrument"]}</td><td>{r["claimed_wavelength"]}</td>'
            f'<td><small>{r["claimed_source_figure"]}</small><br><small>{ref}</small></td>'
            + "".join('<td class="v"></td>' for _ in VERDICTS) + "<td></td></tr>")
    head = ("<th>#</th><th>system</th><th>panel</th><th>claimed instrument</th>"
            "<th>claimed &lambda;</th><th>source fig / ref</th>"
            + "".join(f"<th>{v}</th>" for v in VERDICTS) + "<th>notes</th>")
    html = (f"<!doctype html><meta charset=utf-8><title>diskatlas QA sample "
            f"({len(sample)})</title><style>body{{font:13px sans-serif}}table{{border-collapse:collapse}}"
            f"td,th{{border:1px solid #ccc;padding:4px;vertical-align:top}}td.v{{width:34px;background:#ffe}}"
            f"</style><h3>diskatlas human-QA sample — {len(sample)} records (seed {a.seed})</h3>"
            f"<p>Verdict cells: put Y / N. Feed the completed CSV to <code>backend/qa_score.py</code>.</p>"
            f"<table><tr>{head}</tr>{''.join(rows)}</table>")
    (OUT / "qa_sample.html").write_text(html)

    by = defaultdict(int)
    for r in sample:
        by[(r["band"], r["route"])] += 1
    print(f"wrote qa_sample.csv + qa_sample.html: {len(sample)} records from {total}")
    print("strata (band, route): " + ", ".join(f"{k}={v}" for k, v in sorted(by.items())))


if __name__ == "__main__":
    main()
