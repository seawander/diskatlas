#!/usr/bin/env python3
"""Missing-panel audit: find figures where the atlas ingested fewer panels than
the figure has.

Multi-panel source figures (a/b/c, left/middle/right, top-left/... ) often carry
several atlas-worthy images, but only one was cropped. This scans every record's
credit line ("... Fig. N ..."), reads that figure's caption from the local arXiv
TeX source, estimates the panel count from the caption's panel language, and
flags figures where estimated-panels > records-the-atlas-has-from-that-figure.

Output is a REVIEW list, not an auto-action: many extra panels are models,
residuals, radial profiles, SEDs, or U_phi noise maps that must NOT be ingested.
VIEW each flagged figure and decide (see the ingestion-completeness rules in
HANDOFF.md).

Usage: python3 backend/panel_audit.py [--min-extra 1] [--arxiv <id>]
"""
import argparse, glob, json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "_sources" / "extracted"

CREDIT_FIG = re.compile(r"Fig(?:ure|\.)?\s*(?:([A-Z])\.)?\s*(\d+)\s*([a-z])?", re.I)

# panel-count signals in a caption (strip TeX first)
PANEL_ABC = re.compile(r"(?<![A-Za-z])\(?([a-h])\)")           # (a) (b) ...
LMR = [r"\bleft\b", r"\b(?:middle|center|centre)\b", r"\bright\b"]
TB = [r"\btop\b", r"\bbottom\b"]
ENUM = re.compile(r"from left to right|left to right|top to bottom|clockwise from")
NEG_PANEL = re.compile(r"color\s*bar|colour\s*bar|scale\s*bar|left color|right color|"
                       r"lower[- ]left|upper[- ]right|bottom[- ]left|top[- ]right|"
                       r"corner|inset|arrow|dashed|contour", re.I)


def detex(s):
    s = re.sub(r"\\(?:textit|textbf|emph|rev|mbox|text)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = re.sub(r"[{}$~\\]", " ", s)
    return re.sub(r"\s+", " ", s)


def captions(ax):
    """ordered list of figure captions from the paper's tex (best-effort:
    figure environments in document order -> Fig 1, 2, ...)."""
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
        # brace-match the caption
        i = cm.end(); depth = 1; buf = []
        while i < len(block) and depth:
            c = block[i]
            if c == "{": depth += 1
            elif c == "}": depth -= 1
            if depth: buf.append(c)
            i += 1
        caps.append("".join(buf))
    return caps


def panel_estimate(caption):
    """estimate how many distinct image panels a caption describes."""
    c = detex(caption)
    cl = c.lower()
    # count distinct (a)..(h) letters, but only if at least (a) and (b) appear
    letters = set(m.group(1).lower() for m in PANEL_ABC.finditer(c))
    n_abc = 0
    if "a" in letters and "b" in letters:
        # keep the contiguous run a,b,c,...
        run = 0
        for ch in "abcdefgh":
            if ch in letters:
                run += 1
            else:
                break
        n_abc = run
    n_lmr = sum(1 for p in LMR if re.search(p, cl))
    n_tb = sum(1 for p in TB if re.search(p, cl))
    grid = (n_lmr * n_tb) if (n_lmr >= 2 and n_tb == 2) else 0
    est = max(n_abc, n_lmr if n_lmr >= 2 else 0, grid, 2 if ENUM.search(cl) else 0)
    return est, c[:150]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-extra", type=int, default=1)
    ap.add_argument("--arxiv", default=None)
    a = ap.parse_args()

    # atlas records grouped by (arxiv, figure-number-string)
    by_fig = defaultdict(list)   # (ax, fignum) -> [image_id]
    caps_cache = {}
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        for im in d.get("images", []):
            ax = (im.get("paper") or {}).get("arxiv")
            cr = im.get("credit") or ""
            if not ax:
                continue
            m = CREDIT_FIG.search(cr)
            if not m:
                continue
            fignum = (m.group(1) or "") + m.group(2)   # e.g. "A1" or "1"
            by_fig[(ax, fignum)].append((d["id"], im.get("image_id"), cr))

    flags = []
    for (ax, fignum), recs in sorted(by_fig.items()):
        if a.arxiv and ax != a.arxiv:
            continue
        if ax not in caps_cache:
            caps_cache[ax] = captions(ax)
        caps = caps_cache[ax]
        if not caps:
            continue
        # map fignum -> caption index (plain integers only; skip appendix A.N)
        if not fignum.isdigit():
            continue
        idx = int(fignum) - 1
        if idx < 0 or idx >= len(caps):
            continue
        est, snippet = panel_estimate(caps[idx])
        have = len(recs)
        if est - have >= a.min_extra and est >= 2:
            flags.append((est - have, ax, fignum, est, have, snippet, recs))

    flags.sort(reverse=True)
    print(f"{len(flags)} figures flagged (est. panels > atlas records):\n")
    for extra, ax, fignum, est, have, snippet, recs in flags:
        print(f"[+{extra}] {ax} Fig {fignum}: ~{est} panels, {have} in atlas "
              f"({recs[0][0]}) | {snippet}")
    print(f"\nVIEW each before ingesting; many extra panels are models/residuals/"
          f"profiles/SEDs/U_phi. Sources: images/_sources/extracted/<arxiv>/")


if __name__ == "__main__":
    main()
