#!/usr/bin/env python3
"""Generate frontend/constellations.js from d3-celestial data (one-off).

Source: https://github.com/ofrohn/d3-celestial (BSD-3) — data/constellations.lines.json
(GeoJSON MultiLineString per constellation, lon in [-180,180]) and
data/constellations.json (names + label positions).

Usage: python3 gen_constellations.py /path/to/d3-celestial/data
"""
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "frontend" / "constellations.js"


def to_ra(lon):
    return round(lon % 360.0, 2)


def main():
    d = Path(sys.argv[1])
    lines_gj = json.loads((d / "constellations.lines.json").read_text())
    names_gj = json.loads((d / "constellations.json").read_text())

    lines = []
    for feat in lines_gj["features"]:
        for seg in feat["geometry"]["coordinates"]:
            pts = [[to_ra(p[0]), round(p[1], 2)] for p in seg]
            if len(pts) >= 2:
                lines.append(pts)

    names = []
    for feat in names_gj["features"]:
        lon, lat = feat["geometry"]["coordinates"]
        props = feat.get("properties", {})
        nm = props.get("name") or props.get("n") or feat.get("id", "")
        names.append({"ra": to_ra(lon), "dec": round(lat, 2), "name": nm})

    OUT.write_text("window.CONSTELLATIONS = " +
                   json.dumps({"lines": lines, "names": names},
                              separators=(",", ":")) +
                   ";\n// Data: d3-celestial (github.com/ofrohn/d3-celestial), BSD-3-Clause.\n")
    print(f"{OUT}: {len(lines)} segments, {len(names)} labels")


if __name__ == "__main__":
    main()
