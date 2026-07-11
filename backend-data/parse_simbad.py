#!/usr/bin/env python3
"""Parse data/simbad_raw.txt (sim-script output) -> merge into data/coords_cache.json.

simbad_script.txt emits 'echodata ###NAME' before each query, so the ::data::
section looks like:
  ###HL Tau
  V* HL Tau|67.9102 18.2325|...|K5
A failed query yields a marker with no result line before the next marker —
robust to failures. Unresolved names are listed at the end; fix their
`simbad=` field in seeds and re-run the host fetch for just those.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "simbad_raw.txt"
CACHE = ROOT / "data" / "coords_cache.json"


def main():
    if not RAW.exists():
        sys.exit("data/simbad_raw.txt not found — run fetch_sources.sh on the host first.")
    text = RAW.read_text(errors="replace")
    data_part = text.split("::data::", 1)[-1]

    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    current = None
    good, missing = 0, []
    pending = set()
    for line in data_part.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("###"):
            if current is not None:
                missing.append(current)
            current = line[3:].strip()
            continue
        if current is None or "|" not in line:
            continue
        parts = line.split("|")
        m = re.match(r"\s*([\d.+-]+)\s+([\d.+-]+)", parts[1]) if len(parts) > 1 else None
        if m:
            entry = {"ra": float(m.group(1)), "dec": float(m.group(2)),
                     "main_id": re.sub(r"\s+", " ", parts[0]).strip()}
            if len(parts) > 2:
                try:
                    entry["plx_mas"] = float(parts[2].strip())
                except ValueError:
                    pass
            if len(parts) > 3 and parts[3].strip() not in ("", "~"):
                entry["sptype"] = parts[3].strip()
            if len(parts) > 4:                      # V=6.99,G=6.71,... from %FLUXLIST
                mags = {}
                for tok in parts[4].split(","):
                    mm = re.match(r"\s*([UBVGRIJHK])\s*=\s*(-?[\d.]+)", tok)
                    if mm:
                        mags[mm.group(1)] = float(mm.group(2))
                if mags:
                    entry["mags"] = mags
            cache[current] = entry
            good += 1
            current = None
    if current is not None:
        missing.append(current)

    CACHE.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
    print(f"resolved {good} names -> {CACHE}")
    if missing:
        print(f"UNRESOLVED ({len(missing)}): " + "; ".join(missing))
        print("Fix simbad= names in seeds, regenerate (gen_fetch_script.py), re-run host script.")


if __name__ == "__main__":
    main()
