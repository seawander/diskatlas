#!/usr/bin/env python3
"""Fill data/coords_cache.json from the HYG star database (exact J2000, bright/HD stars).

Usage: python3 coords_from_hyg.py /path/to/hygdata.csv
HYG: https://github.com/astronexus/HYG-Database (CC BY-SA; ra in decimal HOURS).
Only adds entries not already present from SIMBAD (SIMBAD entries win).
Matching: HD number, HIP number, HR number, or proper/Bayer name.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "coords_cache.json"
SYS = ROOT / "data" / "systems"

# name-in-catalog -> catalog key ("hd", number) etc. for systems whose display
# name is not an HD id.
SPECIAL = {
    "Fomalhaut": ("hd", 216956), "Vega": ("hd", 172167), "beta Pic": ("hd", 39060),
    "AU Mic": ("hd", 197481), "HR 8799": ("hd", 218396), "49 Cet": ("hd", 9672),
    "eta Crv": ("hd", 109085), "HD 10647": ("hd", 10647), "eps Ind": ("hd", 209100),
    "kappa And": ("hd", 222439), "51 Eri": ("hd", 29391), "GJ 504": ("hd", 115383),
    "HR 4796": ("hd", 109573), "AF Lep": ("hd", 35850), "eps Eri": ("hd", 22049),
    "HIP 65426": ("hip", 65426), "HIP 99770": ("hip", 99770),
    "14 Her": ("hd", 145675), "GJ 758": ("hd", 182488), "MWC 480": ("hd", 31648),
    "MWC 758": ("hd", 36112), "51 Oph": ("hd", 158643), "AB Aur": ("hd", 31293),
    "CQ Tau": ("hd", 36910), "T Tau": ("hd", 284419), "SU Aur": ("hd", 282624),
    "RY Tau": ("hd", 283571),
}


def wanted_names():
    names = set()
    for f in SYS.glob("*.json"):
        s = json.loads(f.read_text())
        if s.get("ra_deg") is None:
            names.add(s.get("simbad") or s["name"])
            names.add(s["name"])
            for a in s.get("alt_names", []):
                names.add(a)
    return names


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: coords_from_hyg.py hygdata.csv")
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    names = wanted_names()

    by_hd, by_hip, by_hr = {}, {}, {}
    with open(sys.argv[1], newline="", encoding="utf-8", errors="replace") as fh:
        for row in csv.DictReader(fh):
            for key, d in (("hd", by_hd), ("hip", by_hip), ("hr", by_hr)):
                v = row.get(key)
                if v:
                    try:
                        d[int(float(v))] = row
                    except ValueError:
                        pass

    def entry(row):
        e = {"ra": round(float(row["ra"]) * 15.0, 6), "dec": round(float(row["dec"]), 6),
             "source": "HYG"}
        try:
            dist = float(row.get("dist", 0))
            if 0 < dist < 9000:
                e["plx_mas"] = round(1000.0 / dist, 3)
        except ValueError:
            pass
        if row.get("spect"):
            e["sptype"] = row["spect"]
        return e

    added = 0
    for n in sorted(names):
        if n in cache and not cache[n].get("approx"):
            continue
        row = None
        if n in SPECIAL:
            k, num = SPECIAL[n]
            row = {"hd": by_hd, "hip": by_hip, "hr": by_hr}[k].get(num)
        else:
            m = re.match(r"^HD ?(\d+)$", n)
            if m:
                row = by_hd.get(int(m.group(1)))
            m = re.match(r"^HIP ?(\d+)$", n)
            if m and not row:
                row = by_hip.get(int(m.group(1)))
            m = re.match(r"^HR ?(\d+)$", n)
            if m and not row:
                row = by_hr.get(int(m.group(1)))
        if row:
            cache[n] = entry(row)
            added += 1

    CACHE.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
    print(f"HYG matched {added} names -> {CACHE}")


if __name__ == "__main__":
    main()
