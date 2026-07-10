#!/usr/bin/env python3
"""Score a completed diskatlas QA sample sheet.

Reads data/paper_finder/qa_sample.csv after a human has filled the verdict
columns (target_ok, instrument_ok, wavelength_ok, reference_ok, crop_clean) with
Y / N (blank rows are treated as un-reviewed and skipped). Reports, per field and
overall, the number reviewed, the error rate, and a 95% Wilson-score binomial
confidence interval — the numbers to quote in the paper's QA section.

Usage:  python3 backend/qa_score.py [--csv data/paper_finder/qa_sample.csv]
"""
import argparse, csv, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["target_ok", "instrument_ok", "wavelength_ok", "reference_ok", "crop_clean"]


def wilson(k, n, z=1.96):
    """95% Wilson score interval for k successes in n trials."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - half) / d, (c + half) / d)


def yn(v):
    v = (v or "").strip().lower()
    if v in ("y", "yes", "1", "true", "ok"):
        return True
    if v in ("n", "no", "0", "false"):
        return False
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(ROOT / "data" / "paper_finder" / "qa_sample.csv"))
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.csv)))
    reviewed = [r for r in rows if any(yn(r.get(f)) is not None for f in FIELDS)]
    print(f"{len(rows)} sampled records; {len(reviewed)} reviewed\n")
    print(f"{'field':16s} {'reviewed':>8} {'errors':>7} {'err_rate':>9}  95% CI (Wilson)")
    tot_n = tot_err = 0
    for f in FIELDS:
        vals = [yn(r.get(f)) for r in reviewed]
        vals = [v for v in vals if v is not None]
        n = len(vals); err = sum(1 for v in vals if v is False)
        tot_n += n; tot_err += err
        lo, hi = wilson(err, n)
        rate = err / n if n else 0
        print(f"{f:16s} {n:8d} {err:7d} {rate:9.1%}  [{lo:.1%}, {hi:.1%}]")
    lo, hi = wilson(tot_err, tot_n)
    print(f"{'OVERALL (fields)':16s} {tot_n:8d} {tot_err:7d} {(tot_err/tot_n if tot_n else 0):9.1%}"
          f"  [{lo:.1%}, {hi:.1%}]")
    # per-record clean (all reviewed fields correct)
    clean = sum(1 for r in reviewed
                if all(yn(r.get(f)) is not False for f in FIELDS)
                and any(yn(r.get(f)) is not None for f in FIELDS))
    lo, hi = wilson(len(reviewed) - clean, len(reviewed))
    print(f"\nrecords with >=1 error: {len(reviewed)-clean}/{len(reviewed)} "
          f"({(len(reviewed)-clean)/max(1,len(reviewed)):.1%}, 95% CI [{lo:.1%}, {hi:.1%}])")


if __name__ == "__main__":
    main()
