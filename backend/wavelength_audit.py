#!/usr/bin/env python3
"""All-figures / all-papers wavelength audit.

`panel_audit.py` only inspects the ONE figure named in each record's credit, so
it misses the case the maintainer hit twice (HH 80-81 Carrasco 2012; HD 98800
Ribas 2018): a paper whose *other* figures show the same target at DIFFERENT
wavelengths that were never ingested.

This scans EVERY figure caption of every paper cited in the atlas (using the
local arXiv tex in images/_sources/extracted/<arxiv>/), extracts the
wavelength(s) each image-figure shows, and flags any wavelength a paper images
that the atlas does NOT already hold for that system+paper.

Heuristic → a REVIEW worklist, not auto-action. VIEW each flagged figure and
decide (models / residuals / SEDs / PV-diagrams / non-detections are excluded
best-effort but slip through). Usage: python3 backend/wavelength_audit.py [--arxiv ID]
"""
import argparse, glob, json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "_sources" / "extracted"

# caption keywords that mean "not a resolved-image figure" -> skip the figure
NON_IMAGE = re.compile(r"\bSED\b|spectral energy|radial (?:profile|intensity)|"
                       r"\bP[-\s]?V\b|position[-\s]velocity|posterior|MCMC|corner plot|"
                       r"histogram|visibilit|\buv[-\s]?plane\b|light ?curve|"
                       r"spectrum|spectra\b|best[-\s]?fit model|schematic", re.I)
IMAGE_HINT = re.compile(r"\bimage|\bmap\b|continuum|scattered|polari|emission|"
                        r"coronagraph|contour|mosaic|observ", re.I)


def wl_um(num, unit):
    """convert a (number, unit) to microns."""
    num = float(num)
    unit = unit.lower()
    if unit in ("um", "µm", "μm", "micron", "microns"):
        return num
    if unit == "nm":
        return num / 1000.0
    if unit == "mm":
        return num * 1000.0
    if unit == "cm":
        return num * 1e4
    if unit == "ghz":
        return 2.99792458e5 / num          # c/nu in um  (c=3e8 m/s, um)
    return None


WL_RE = re.compile(r"(\d+(?:\.\d+)?)\s*\\?,?\s*(?:\$?\\?(?:mu|micron)\$?\s*m|"
                   r"\bum\b|µm|μm|nm|mm|cm|GHz)", re.I)
# capture the unit token cleanly
UNIT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*\\?,?\s*"
                     r"(um|µm|μm|micron|microns|nm|mm|cm|GHz|(?:\$?\\?mu\$?\s*m))", re.I)
FILT_RE = re.compile(r"\bF\d{3,4}[A-Z]{1,2}\b")


def caption_wls(cap):
    """set of wavelengths (um) mentioned in a caption, plus HST filter tokens."""
    wls = set()
    for m in UNIT_RE.finditer(cap):
        num, unit = m.group(1), m.group(2)
        unit = re.sub(r"[\\$,]|mu\s*m", lambda x: "um" if "mu" in x.group(0) else "", unit)
        v = wl_um(num, unit or "um")
        if v and 0.05 <= v <= 1e8:
            wls.add(round(v, 2))
    filts = set(FILT_RE.findall(cap))
    return wls, filts


def captions(ax):
    d = SRC / ax
    if not d.is_dir():
        return None
    txt = ""
    for f in sorted(d.glob("*.tex")):
        try:
            txt += "\n" + f.read_text(errors="ignore")
        except Exception:
            pass
    if not txt:
        return None
    txt = re.sub(r"(?<!\\)%[^\n]*", "", txt)
    caps = []
    for m in re.finditer(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", txt, re.S):
        block = m.group(1)
        cm = re.search(r"\\caption\{", block)
        if not cm:
            caps.append("")
            continue
        i = cm.end(); depth = 1; buf = []
        while i < len(block) and depth:
            c = block[i]
            if c == "{": depth += 1
            elif c == "}": depth -= 1
            if depth: buf.append(c)
            i += 1
        caps.append(re.sub(r"\s+", " ", "".join(buf)))
    return caps


def close(a, b):
    """same band? within 12% in log space (so 1.25 vs 1.3 mm match; 70 vs 100 don't)."""
    return abs(a - b) <= 0.12 * max(a, b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arxiv", default=None)
    ap.add_argument("--min-extra", type=int, default=1)
    a = ap.parse_args()

    # (arxiv) -> system -> held wavelengths(um) + filters
    held = defaultdict(lambda: defaultdict(lambda: {"wl": set(), "filt": set()}))
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        for im in d.get("images", []):
            ax = (im.get("paper") or {}).get("arxiv")
            if not ax:
                continue
            wl = im.get("wavelength_um")
            if wl:
                held[ax][d["id"]]["wl"].add(float(wl))
            lab = im.get("wavelength_label", "") or ""
            held[ax][d["id"]]["filt"] |= set(FILT_RE.findall(lab))

    flags = []
    for ax, sysmap in sorted(held.items()):
        if a.arxiv and ax != a.arxiv:
            continue
        caps = captions(ax)
        if not caps:
            continue
        # union of all wavelengths any image-figure in this paper shows
        for i, cap in enumerate(caps, 1):
            if not cap or NON_IMAGE.search(cap) or not IMAGE_HINT.search(cap):
                continue
            wls, filts = caption_wls(cap)
            if not wls and not filts:
                continue
            # for each system citing this paper, is any figure-wavelength unheld?
            for sid, h in sysmap.items():
                miss_wl = [w for w in wls if not any(close(w, hv) for hv in h["wl"])]
                miss_f = [ff for ff in filts if ff not in h["filt"]]
                if miss_wl or miss_f:
                    flags.append((ax, i, sid, sorted(miss_wl), sorted(miss_f), cap[:120]))

    # collapse duplicate (ax, fig) across systems for readability
    print(f"{len(flags)} figure×system flags (paper images a wavelength the atlas lacks):\n")
    for ax, fig, sid, mw, mf, snip in flags:
        bands = ", ".join([f"{w:g}um" if w < 1000 else f"{w/1000:g}mm" for w in mw] + mf)
        print(f"[{ax} Fig{fig} -> {sid}] missing: {bands}\n    {snip}")
    print(f"\nVIEW each before ingesting (models/residuals/reference-PSF panels slip "
          f"through). Sources: images/_sources/extracted/<arxiv>/")


if __name__ == "__main__":
    main()
