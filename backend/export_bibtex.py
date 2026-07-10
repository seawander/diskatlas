#!/usr/bin/env python3
"""Export the atlas bibliography to BibTeX, exclusively from NASA ADS.

Collects every paper block referenced by data/systems/*.json
(images[].paper, planets[].paper, planets[].extra_papers), dedups by
arXiv id / bibcode, resolves every paper to an ADS bibcode (stored
bibcode, else ADS identifier search on the arXiv id), then fetches the
official ADS BibTeX export for all of them. Entry contents are kept
byte-for-byte as ADS provides them (the format used by Ren et al. 2024
and the aastex_pwned aasjournal.bst); only the citation keys are
rewritten from bibcodes to stable ASCII keys (FirstauthorYear with
a/b/c disambiguation) so they can be cited from the manuscript.

The output refs.bib has two parts. Everything above the hand-section
marker is regenerated on every run. Everything below the marker is
hand-maintained and kept verbatim, and any auto entry whose citation key
already appears in the hand section is omitted, so that a paper that is
both an atlas record and a hand-added reference (e.g. a survey's
series-I paper) is not emitted twice.

Verification: each exported entry's first-author family name and year
must match the atlas record, and its eprint (when present) must match
the stored arXiv id. Mismatches are reported and the script exits
non-zero.

Auth: uses an ADS API token from --token / $ADS_TOKEN when available,
otherwise bootstraps the same anonymous session token the ADS website
uses for its own export function.

Usage:
    python3 backend/export_bibtex.py [-o OUT.bib] [--cache CACHE.json]
"""
import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.adsabs.harvard.edu/v1"

# ---------------------------------------------------------------- collect

def collect_papers():
    """Return list of merged unique paper dicts, linked by arxiv/bibcode."""
    recs = []
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        for im in d.get("images", []):
            if im.get("paper"):
                recs.append(im["paper"])
        for pl in d.get("planets", []):
            if pl.get("paper"):
                recs.append(pl["paper"])
            recs += [p for p in pl.get("extra_papers", []) if p]
    arx2g, bib2g, groups = {}, {}, []
    for p in recs:
        a = (p.get("arxiv") or "").strip()
        b = (p.get("bibcode") or "").strip()
        g = arx2g.get(a) if a else None
        if g is None and b:
            g = bib2g.get(b)
        if g is None:
            g = len(groups)
            groups.append([])
        groups[g].append(p)
        if a:
            arx2g[a] = g
        if b:
            bib2g[b] = g
    merged = []
    for grp in groups:
        if not grp:
            continue
        m = {}
        for p in grp:
            for k in ("first_author", "year", "title", "journal", "arxiv", "bibcode"):
                if p.get(k) and not m.get(k):
                    m[k] = p[k]
        merged.append(m)
    return merged

# ------------------------------------------------------------------- ADS

def http(url, token, payload=None):
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}",
                      "Content-Type": "application/json",
                      "User-Agent": "diskatlas-bibtex"},
        data=json.dumps(payload).encode() if payload is not None else None)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if attempt == 2:
                raise
            print(f"  retry after error: {e}", file=sys.stderr)
            time.sleep(8)


def get_token(args):
    if args.token:
        return args.token
    if os.environ.get("ADS_TOKEN"):
        return os.environ["ADS_TOKEN"]
    # anonymous session token, as used by the ADS web UI itself
    with urllib.request.urlopen("https://ui.adsabs.harvard.edu/v1/accounts/bootstrap",
                                timeout=60) as r:
        return json.loads(r.read().decode())["access_token"]


def resolve_bibcodes(ids, token, cache):
    """Fill cache['arx2bib'] mapping arXiv id -> ADS bibcode."""
    a2b = cache.setdefault("arx2bib", {})
    todo = sorted({a for a in ids if a and a not in a2b})
    for i in range(0, len(todo), 40):
        batch = todo[i:i + 40]
        q = "identifier:(" + " OR ".join(f'"arXiv:{a}"' for a in batch) + ")"
        url = (f"{API}/search/query?q={urllib.parse.quote(q)}"
               f"&fl=bibcode,identifier&rows={4 * len(batch)}")
        print(f"ADS search: resolving {len(batch)} arXiv ids ...", file=sys.stderr)
        docs = http(url, token)["response"]["docs"]
        for d in docs:
            idents = [x.lower() for x in d.get("identifier", [])]
            for a in batch:
                if f"arxiv:{a.lower()}" in idents or a.lower() in idents:
                    a2b[a] = d["bibcode"]
        time.sleep(1)
    return a2b


def fetch_export(bibcodes, token, cache):
    """Fetch ADS BibTeX for all bibcodes; cache maps bibcode -> entry text."""
    ent = cache.setdefault("export", {})
    todo = [b for b in bibcodes if b not in ent]
    for i in range(0, len(todo), 400):
        batch = todo[i:i + 400]
        print(f"ADS export: fetching {len(batch)} BibTeX entries ...", file=sys.stderr)
        out = http(f"{API}/export/bibtex", token, {"bibcode": batch})["export"]
        for block in re.split(r"\n(?=@)", out):
            block = block.strip()
            m = re.match(r"@[A-Za-z]+\{([^,]+),", block)
            if m:
                ent[m.group(1)] = block
        time.sleep(1)
    return ent

# ------------------------------------------------------------ verification

def ascii_fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if not unicodedata.combining(c)).lower().replace("-", " ").strip()


def fold(s):
    """Loose comparison: accents stripped, TeX accents dropped, ae/oe/ue folded."""
    s = re.sub(r"\\[`'^\"~=.uvHckro]\s?", "", s or "")   # TeX accent macros
    s = re.sub(r"[{}\\]", "", s)
    s = ascii_fold(s)
    for a, b in (("ae", "a"), ("oe", "o"), ("ue", "u")):
        s = s.replace(a, b)
    return s


def entry_first_author_year(block):
    au = re.search(r"author\s*=\s*\{(.*?)\}\s*,\s*\n", block, re.S)
    first = au.group(1).split(" and ")[0] if au else ""
    fam = first.split(",")[0] if "," in first else first
    yr = re.search(r"year\s*=\s*\{?\"?(\d{4})", block)
    return fam, int(yr.group(1)) if yr else None


def verify(p, block, label):
    problems = []
    fam, yr = entry_first_author_year(block)
    # record first_author may be "Liu, W. M." -- keep only the family part
    rec_fam = fold(p.get("first_author", "").split(",")[0])
    if rec_fam and "collaboration" not in rec_fam:
        if rec_fam.split()[-1] not in fold(fam):
            problems.append(f"first-author mismatch {label}: record "
                            f"'{p.get('first_author')}' vs ADS '{fam}'")
    if yr and abs(int(p["year"]) - yr) > 1:
        problems.append(f"year mismatch {label}: record {p['year']} vs ADS {yr}")
    ep = re.search(r"eprint\s*=\s*\{([^}]+)\}", block)
    if ep and p.get("arxiv") and ep.group(1).strip() != p["arxiv"].strip():
        problems.append(f"eprint mismatch {label}: record {p['arxiv']} "
                        f"vs ADS {ep.group(1)}")
    return problems


HAND_MARKER = "%% Hand-maintained entries below this marker"


def hand_section(path):
    """Return (keys, text) of the hand-maintained tail of refs.bib, found by
    HAND_MARKER. Auto entries with these keys are skipped so nothing is
    emitted twice, and the tail is re-appended verbatim after regeneration."""
    if not path.exists():
        return set(), ""
    text = path.read_text(errors="replace")
    i = text.find(HAND_MARKER)
    if i < 0:
        return set(), ""
    start = text.rfind("%% ====", 0, i)
    tail = text[start if start >= 0 else i:]
    keys = {m.group(1).strip() for m in
            re.finditer(r"@[A-Za-z]+\s*\{\s*([^,]+?)\s*,", tail)}
    return keys, tail

# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(ROOT / "paper_Overleaf" / "refs.bib"))
    ap.add_argument("--cache", default=None, help="JSON cache for ADS responses")
    ap.add_argument("--token", default=None, help="ADS API token (else $ADS_TOKEN, "
                                                  "else anonymous session token)")
    args = ap.parse_args()

    papers = collect_papers()
    print(f"{len(papers)} distinct papers", file=sys.stderr)

    cache = {}
    if args.cache and Path(args.cache).exists():
        cache = json.loads(Path(args.cache).read_text())

    token = get_token(args)
    a2b = resolve_bibcodes([p["arxiv"].strip() for p in papers
                            if p.get("arxiv") and not p.get("bibcode")],
                           token, cache)
    if args.cache:
        Path(args.cache).write_text(json.dumps(cache))

    problems, resolved = [], []
    for p in papers:
        bib = (p.get("bibcode") or "").strip() or a2b.get((p.get("arxiv") or "").strip())
        if not bib:
            problems.append(f"unresolved on ADS: {p.get('first_author')} "
                            f"{p.get('year')} arXiv:{p.get('arxiv')}")
            continue
        resolved.append((p, bib))

    entries = fetch_export([b for _, b in resolved], token, cache)

    # retry pass: stored/stale bibcodes ADS no longer exports (e.g. arXiv
    # bibcodes merged into the published record) -- re-resolve via arXiv id
    stale = [(p, bib) for p, bib in resolved
             if bib not in entries and p.get("arxiv")]
    if stale:
        for a in [p["arxiv"].strip() for p, _ in stale]:
            cache.get("arx2bib", {}).pop(a, None)
        a2b = resolve_bibcodes([p["arxiv"].strip() for p, _ in stale], token, cache)
        remap = {old: a2b.get(p["arxiv"].strip()) for p, old in stale}
        resolved = [(p, remap.get(b) or b) for p, b in resolved]
        fetch_export([b for _, b in resolved if b not in entries], token, cache)
    if args.cache:
        Path(args.cache).write_text(json.dumps(cache))

    out_entries = []
    for p, bib in resolved:
        block = entries.get(bib)
        if not block:
            problems.append(f"no ADS export for {bib} ({p.get('first_author')} "
                            f"{p.get('year')} arXiv:{p.get('arxiv')})")
            continue
        problems += verify(p, block, bib)
        out_entries.append({"paper": p, "bibcode": bib, "block": block})

    # stable ASCII citekeys: FirstauthorYear with a/b/c disambiguation
    from collections import defaultdict
    bykey = defaultdict(list)
    for e in out_entries:
        fam = ascii_fold(e["paper"].get("first_author", "anon")
                         .split(",")[0]).split()[-1]
        key = "".join(c for c in fam.capitalize() if c.isalnum()) \
            + str(e["paper"].get("year", ""))
        bykey[key].append(e)
    for key, grp in sorted(bykey.items()):
        grp.sort(key=lambda e: e["bibcode"])
        for i, e in enumerate(grp):
            e["key"] = key + ("abcdefghij"[i] if len(grp) > 1 else "")

    # entries already defined in the hand-maintained tail of refs.bib are
    # its responsibility; skip them so nothing is emitted (and cited) twice.
    local_keys, hand_tail = hand_section(Path(args.out))

    lines = ["%% Auto-generated by backend/export_bibtex.py -- do not edit by hand.",
             "%% Entries are the official NASA ADS BibTeX export, verbatim except",
             "%% for the citation keys (rewritten from bibcodes to Author+Year).",
             "%% Keys also present in the hand-maintained section are omitted here.", ""]
    skipped, written = [], 0
    for e in sorted(out_entries, key=lambda e: e["key"]):
        if e["key"] in local_keys:
            skipped.append(e["key"])
            continue
        block = re.sub(r"^(@[A-Za-z]+)\{[^,]+,", r"\1{" + e["key"] + ",",
                       e["block"], count=1)
        lines.append(block + "\n")
        written += 1
    Path(args.out).write_text("\n".join(lines) + hand_tail)
    print(f"wrote {args.out}: {written} auto entries "
          f"(+ hand section kept verbatim)", file=sys.stderr)
    if skipped:
        print(f"  skipped {len(skipped)} already hand-maintained: "
              f"{', '.join(sorted(skipped))}", file=sys.stderr)

    if problems:
        print(f"\n{len(problems)} verification problems:", file=sys.stderr)
        for pr in problems:
            print("  " + pr, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
