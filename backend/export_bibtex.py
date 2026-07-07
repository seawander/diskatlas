#!/usr/bin/env python3
"""Export the atlas bibliography to BibTeX.

Collects every paper block referenced by data/systems/*.json
(images[].paper, planets[].paper, planets[].extra_papers), dedups by
arXiv id / bibcode, fetches verified metadata (titles, full author
lists, DOIs) from the arXiv API -- which simultaneously validates every
arXiv id -- and from Crossref for the pre-arXiv papers, then writes one
@article entry per paper.

Journal / volume / page fields are parsed from the ADS bibcode when one
is stored (the most reliable source), falling back to the free-text
"journal" string in the record or the arXiv journal_ref.

Usage:
    python3 backend/export_bibtex.py [-o OUT.bib] [--cache CACHE.json]

The cache file stores raw arXiv/Crossref responses so reruns are
offline. Exit status is non-zero if any record fails verification
(first-author or year mismatch against the fetched metadata).
"""
import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAILTO = "diskatlas@example.org"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

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

# ------------------------------------------------------------------ fetch

def http_get(url, retries=2):
    req = urllib.request.Request(url, headers={"User-Agent": f"diskatlas-bibtex ({MAILTO})"})
    for i in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8")
        except Exception as e:
            if i == retries:
                raise
            print(f"  retry after error: {e}", file=sys.stderr)
            time.sleep(5)


def fetch_arxiv(ids, cache):
    """Fetch title/authors/doi/journal_ref for each arXiv id via the API."""
    todo = [i for i in ids if i not in cache]
    for i in range(0, len(todo), 100):
        batch = todo[i:i + 100]
        url = ("https://export.arxiv.org/api/query?id_list="
               + urllib.parse.quote(",".join(batch)) + f"&max_results={len(batch)}")
        print(f"arXiv API: fetching {len(batch)} ids ...", file=sys.stderr)
        feed = ET.fromstring(http_get(url))
        for entry in feed.findall(ATOM + "entry"):
            eid = entry.findtext(ATOM + "id") or ""
            m = re.search(r"arxiv\.org/abs/(.+?)(v\d+)?$", eid)
            if not m:
                continue  # error placeholder entry
            aid = m.group(1)
            cache[aid] = {
                "title": re.sub(r"\s+", " ", entry.findtext(ATOM + "title") or "").strip(),
                "authors": [a.findtext(ATOM + "name") for a in entry.findall(ATOM + "author")],
                "published": entry.findtext(ATOM + "published") or "",
                "doi": entry.findtext(ARXIV_NS + "doi"),
                "journal_ref": entry.findtext(ARXIV_NS + "journal_ref"),
            }
        time.sleep(3)  # arXiv API rate-limit etiquette
    return cache


def fetch_crossref_doi(doi, cache):
    """Resolve journal/volume/page for a known DOI (upgrade in-press entries)."""
    if doi in cache:
        return cache[doi]
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}"
    print(f"Crossref DOI: {doi} ...", file=sys.stderr)
    try:
        it = json.loads(http_get(url, retries=1))["message"]
    except Exception:
        cache[doi] = None
        time.sleep(1)
        return None
    res = {
        "container": (it.get("container-title") or [None])[0],
        "volume": it.get("volume"),
        "page": it.get("article-number") or it.get("page"),
        "family": (it.get("author") or [{}])[0].get("family", ""),
        "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
    }
    cache[doi] = res
    time.sleep(1)
    return res


def fetch_crossref(paper, cache):
    """Look up a non-arXiv paper on Crossref; verify before accepting."""
    key = paper.get("bibcode") or paper.get("title")
    if key in cache:
        return cache[key]
    bc = parse_bibcode(paper.get("bibcode") or "")
    terms = [paper.get("first_author", ""), str(paper.get("year", ""))]
    if paper.get("title"):
        terms.append(paper["title"])
    elif bc:
        terms += [bc["journal_raw"], bc["volume"], bc["page"]]
    q = urllib.parse.quote(" ".join(t for t in terms if t))
    url = (f"https://api.crossref.org/works?query.bibliographic={q}&rows=5"
           "&select=DOI,title,author,container-title,volume,page,issued"
           f"&mailto={MAILTO}")
    print(f"Crossref: {paper.get('first_author')} {paper.get('year')} ...", file=sys.stderr)
    items = json.loads(http_get(url))["message"]["items"]
    fam = fold(paper.get("first_author", ""))
    for it in items:
        auth = it.get("author") or []
        if not auth or fold(auth[0].get("family", "")) != fam:
            continue
        yr = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
        if yr is None or abs(int(yr) - int(paper["year"])) > 1:
            continue
        if bc and it.get("volume") and it["volume"] != bc["volume"]:
            continue
        res = {
            "title": (it.get("title") or [None])[0],
            "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in auth],
            "doi": it.get("DOI"),
        }
        cache[key] = res
        time.sleep(1)
        return res
    cache[key] = None
    time.sleep(1)
    return None

# ------------------------------------------------------------- formatting

# ADS bibcode journal code -> BibTeX journal field (AASTeX macros where defined)
BIBCODE_JOURNALS = {
    "ApJ": "\\apj", "ApJS": "\\apjs", "AJ": "\\aj", "A&A": "\\aap",
    "MNRAS": "\\mnras", "PASJ": "\\pasj", "PASP": "\\pasp",
    "Natur": "\\nat", "Sci": "Science", "NatAs": "Nature Astronomy",
    "SciA": "Science Advances", "PJAB": "Proceedings of the Japan Academy, Series B",
    "ARA&A": "\\araa", "Icar": "\\icarus", "ApL": "\\aplett",
}
# free-text journal names -> (bibtex journal, is_letters)
TEXT_JOURNALS = {
    "apj": ("\\apj", False), "the astrophysical journal": ("\\apj", False),
    "astrophysical journal": ("\\apj", False),
    "apjl": ("\\apjl", True), "apj letters": ("\\apjl", True),
    "apj (letters)": ("\\apjl", True),
    "the astrophysical journal letters": ("\\apjl", True),
    "apjs": ("\\apjs", False),
    "aj": ("\\aj", False), "the astronomical journal": ("\\aj", False),
    "a&a": ("\\aap", False), "astronomy & astrophysics": ("\\aap", False),
    "astronomy and astrophysics": ("\\aap", False),
    "a&a letters": ("\\aap", True), "astronomy & astrophysics (letters)": ("\\aap", True),
    "mnras": ("\\mnras", False), "pasj": ("\\pasj", False), "pasp": ("\\pasp", False),
    "nature": ("\\nat", False), "science": ("Science", False),
    "nature astronomy": ("Nature Astronomy", False),
    "proc. japan acad. ser. b": ("Proceedings of the Japan Academy, Series B", False),
    "the astrophysical journal supplement series": ("\\apjs", False),
    "the astrophysical journal supplement": ("\\apjs", False),
    "monthly notices of the royal astronomical society": ("\\mnras", False),
    "publications of the astronomical society of japan": ("\\pasj", False),
    "publications of the astronomical society of the pacific": ("\\pasp", False),
}


def parse_bibcode(bc):
    """YYYYJJJJJVVVVMPPPPA -> journal/volume/page (ADS bibcode spec)."""
    if len(bc) != 19:
        return None
    jr = bc[4:9].strip(".")
    vol = bc[9:13].lstrip(".")
    qual = bc[13]
    page = bc[14:18].lstrip(".")
    if not (vol.isdigit() and jr):
        return None
    letters = False
    if qual == "L":
        letters = True
        page = "L" + page
    elif qual.isdigit():          # most-significant digit of a 5-digit page
        page = qual + page
    elif qual != ".":             # e.g. 'A' for A&A article ids
        page = qual + page
    journal = BIBCODE_JOURNALS.get(jr, jr)
    if letters and jr == "ApJ":
        journal = "\\apjl"
    return {"journal": journal, "journal_raw": jr, "volume": vol, "page": page}


def parse_journal_text(s):
    """Parse strings like 'A&A 693, A151' or 'ApJL (accepted)'."""
    if not s:
        return None
    s = re.sub(r"\s*\(.*?\)\s*$", "", s.strip())  # drop trailing '(2025)', '(accepted)'
    m = re.match(r"^([A-Za-z&.()\s]+?)\s+(\d+),\s*([A-Za-z]?\d+)\.?$", s)
    name, vol, page = (m.group(1), m.group(2), m.group(3)) if m else (s, None, None)
    jt = TEXT_JOURNALS.get(name.strip().rstrip(".").lower())
    if jt is None:
        return None
    journal, letters = jt
    if letters and page and not page[0].isalpha():
        page = "L" + page
    return {"journal": journal, "volume": vol, "page": page}


COMBINING = {
    "̀": "\\`", "́": "\\'", "̂": "\\^", "̃": "\\~",
    "̄": "\\=", "̆": "\\u", "̇": "\\.", "̈": "\\\"",
    "̊": "\\r", "̋": "\\H", "̌": "\\v", "̧": "\\c",
    "̨": "\\k",
}
SPECIAL = {"ø": "{\\o}", "Ø": "{\\O}", "æ": "{\\ae}", "Æ": "{\\AE}",
           "ß": "{\\ss}", "ł": "{\\l}", "Ł": "{\\L}", "ð": "{\\dh}",
           "þ": "{\\th}", "œ": "{\\oe}", "Œ": "{\\OE}", "ı": "{\\i}",
           "\u2013": "--", "\u2014": "---", "\u2019": "'", "\u2018": "'",
           "\u201c": "``", "\u201d": "''", "\u00a0": "~"}


def latexify(s):
    """Transliterate unicode to LaTeX-safe ASCII and escape specials."""
    if s is None:
        return ""
    out = []
    for ch in s:
        if ch in SPECIAL:
            out.append(SPECIAL[ch])
            continue
        if ord(ch) < 128:
            out.append(ch)
            continue
        dec = unicodedata.normalize("NFD", ch)
        if len(dec) >= 2 and dec[1] in COMBINING:
            out.append("{" + COMBINING[dec[1]] + dec[0] + "}")
        else:
            out.append(unicodedata.normalize("NFKD", ch).encode("ascii", "ignore").decode() or "?")
    s = "".join(out)
    s = re.sub(r"(?<!\\)([&%#_])", r"\\\1", s)
    return s


def ascii_fold(s):
    """Accent- and case-insensitive form (for citekeys)."""
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if not unicodedata.combining(c)).lower().replace("-", " ").strip()


def fold(s):
    """Looser comparison form: additionally folds German transliterations
    ae/oe/ue so 'Neuhauser' matches 'Neuhaeuser'. Never use for citekeys
    (it would turn 'Bae' into 'Ba')."""
    s = ascii_fold(s)
    for a, b in (("ae", "a"), ("oe", "o"), ("ue", "u")):
        s = s.replace(a, b)
    return s


def author_field(names, cap=20):
    names = [n for n in names if n]
    if len(names) > cap:
        names = names[:cap] + ["others"]
    fixed = []
    for n in names:
        # Crossref sometimes returns all-caps family names ("TAMURA")
        toks = [t.capitalize() if t.isalpha() and t.isupper() and len(t) > 3 else t
                for t in n.split()]
        fixed.append(" ".join(toks))
    # BibTeX parses natural "First von Last" order, so no reordering needed.
    return " and ".join(latexify(n) for n in fixed)

# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=str(ROOT / "paper_Overleaf" / "references.bib"))
    ap.add_argument("--cache", default=None, help="JSON cache for API responses")
    args = ap.parse_args()

    papers = collect_papers()
    print(f"{len(papers)} distinct papers", file=sys.stderr)

    cache = {"arxiv": {}, "crossref": {}}
    if args.cache and Path(args.cache).exists():
        cache = json.loads(Path(args.cache).read_text())

    arxiv_ids = [p["arxiv"].strip() for p in papers if p.get("arxiv")]
    fetch_arxiv(arxiv_ids, cache["arxiv"])
    if args.cache:
        Path(args.cache).write_text(json.dumps(cache))

    problems = []
    entries = []
    for p in papers:
        aid = (p.get("arxiv") or "").strip()
        meta = cache["arxiv"].get(aid) if aid else None
        if aid and not meta:
            problems.append(f"arXiv id NOT FOUND on arXiv: {aid} ({p.get('first_author')} {p.get('year')})")
            continue
        if not aid:
            meta = fetch_crossref(p, cache["crossref"])
            if args.cache:
                Path(args.cache).write_text(json.dumps(cache))
        # --- verification against fetched metadata
        bad_id = False
        if meta and meta.get("authors") and "collaboration" not in fold(p.get("first_author", "")):
            fam = fold(p.get("first_author", ""))
            if fam and fam.split()[-1] not in fold(meta["authors"][0]):
                problems.append(f"first-author mismatch {aid or p.get('bibcode')}: "
                                f"record '{p.get('first_author')}' vs fetched '{meta['authors'][0]}'"
                                " -- fetched metadata discarded, fix the record")
                bad_id = True
                meta = None  # do not attach the wrong paper's metadata
        if meta and meta.get("published"):
            v1_year = int(meta["published"][:4])
            if abs(int(p["year"]) - v1_year) > 1:
                problems.append(f"year mismatch {aid}: record {p['year']} vs arXiv v1 {v1_year}")
        # --- assemble fields
        title = p.get("title") or (meta or {}).get("title")
        struct = parse_bibcode((p.get("bibcode") or "").strip())
        if not struct:
            struct = parse_journal_text(p.get("journal"))
        if not struct and meta and meta.get("journal_ref"):
            struct = parse_journal_text(meta["journal_ref"])
        if not struct and meta and meta.get("doi"):
            # published (has a DOI) but no bibcode/journal_ref yet: ask Crossref
            cx = fetch_crossref_doi(meta["doi"], cache.setdefault("crossref_doi", {}))
            if args.cache:
                Path(args.cache).write_text(json.dumps(cache))
            if cx and cx.get("container"):
                ok_fam = fold(p.get("first_author", "")) in fold(cx.get("family", "")) \
                    or "collaboration" in fold(p.get("first_author", ""))
                ok_year = cx.get("year") and abs(int(cx["year"]) - int(p["year"])) <= 1
                jt = TEXT_JOURNALS.get(cx["container"].strip().lower())
                if ok_fam and ok_year and jt:
                    struct = {"journal": jt[0], "volume": cx.get("volume"),
                              "page": cx.get("page")}
        if not struct:
            struct = {"journal": "arXiv e-prints", "volume": None, "page": None}
        entries.append({
            "paper": p, "meta": meta or {}, "title": title, "struct": struct,
            "bad_id": bad_id,
            "authors": (meta or {}).get("authors") or [p.get("first_author", "") + " and others"],
        })

    # --- citekeys: FirstauthorYear with a/b/c disambiguation
    def base_key(e):
        fam = ascii_fold(e["paper"].get("first_author", "anon")).split()[-1]
        return "".join(c for c in fam.capitalize() if c.isalnum()) + str(e["paper"].get("year", ""))
    from collections import defaultdict
    bykey = defaultdict(list)
    for e in entries:
        bykey[base_key(e)].append(e)
    for k, grp in bykey.items():
        if len(grp) == 1:
            grp[0]["key"] = k
        else:
            grp.sort(key=lambda e: (e["paper"].get("arxiv") or "", e["paper"].get("bibcode") or ""))
            for i, e in enumerate(grp):
                e["key"] = k + "abcdefghij"[i]

    lines = ["%% Auto-generated by backend/export_bibtex.py -- do not edit by hand.",
             "%% Metadata verified against the arXiv API (titles, authors, DOIs)",
             "%% and Crossref; journal/volume/page parsed from ADS bibcodes.", ""]
    for e in sorted(entries, key=lambda e: e["key"]):
        p, s = e["paper"], e["struct"]
        f = [("author", author_field(e["authors"]))]
        if e["title"]:
            f.append(("title", "{" + latexify(e["title"]) + "}"))
        f += [("journal", s["journal"]),
              ("year", str(p.get("year", "")))]
        if s.get("volume"):
            f.append(("volume", s["volume"]))
        if s.get("page"):
            f.append(("pages", s["page"]))
        doi = e["meta"].get("doi")
        if doi:
            f.append(("doi", doi))
        if p.get("arxiv") and not e["bad_id"]:
            f.append(("archivePrefix", "arXiv"))
            f.append(("eprint", p["arxiv"].strip()))
        if p.get("bibcode"):
            f.append(("adsurl", "https://ui.adsabs.harvard.edu/abs/" + p["bibcode"].strip()))
        body = ",\n".join(f"  {k} = {{{v}}}" for k, v in f)
        lines.append(f"@article{{{e['key']},\n{body}\n}}\n")

    Path(args.out).write_text("\n".join(lines))
    print(f"wrote {args.out}: {len(entries)} entries", file=sys.stderr)
    if problems:
        print(f"\n{len(problems)} verification problems:", file=sys.stderr)
        for pr in problems:
            print("  " + pr, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
