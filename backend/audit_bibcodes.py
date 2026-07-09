#!/usr/bin/env python3
"""Audit every stored ADS `bibcode` against the record's `arxiv` id via NASA ADS.

For each paper block in data/systems/*.json (images[].paper, planets[].paper,
planets[].extra_papers):
  - resolve arxiv id -> canonical ADS bibcode  (identifier:("arXiv:<id>"))
  - look up the stored bibcode's own record    (bibcode:(...))
and classify:
  OK            stored bibcode == canonical, or stored bibcode resolves to the
                same arXiv id (alternate/eprint form of the same paper -> keep)
  HALLUCINATED  stored bibcode does not exist in ADS            -> fix to canonical
  WRONG_PAPER   stored bibcode exists but points to a different paper -> fix to canonical
  NO_BIB        no stored bibcode and none resolvable
  BIBONLY_BAD   record has a bibcode but no arxiv, and the bibcode is absent from ADS

--fix rewrites the stored bibcode in place (only HALLUCINATED / WRONG_PAPER with a
known canonical). Auth: anonymous ADS session token (no key needed).

Usage: python3 backend/audit_bibcodes.py [--fix]
"""
import argparse, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.adsabs.harvard.edu/v1"


def token():
    with urllib.request.urlopen("https://ui.adsabs.harvard.edu/v1/accounts/bootstrap", timeout=60) as r:
        return json.loads(r.read().decode())["access_token"]


def http(url, tok):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}",
                                               "User-Agent": "diskatlas-bibaudit"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if attempt == 3:
                raise
            print(f"  retry: {e}", file=sys.stderr); time.sleep(8)


def ads_query(tok, q, fl, rows):
    url = f"{API}/search/query?q={urllib.parse.quote(q)}&fl={fl}&rows={rows}"
    return http(url, tok)["response"]["docs"]


def resolve_arxiv(tok, ids):
    """arxiv id -> canonical bibcode."""
    out = {}
    ids = sorted(set(ids))
    for i in range(0, len(ids), 40):
        b = ids[i:i + 40]
        q = "identifier:(" + " OR ".join(f'"arXiv:{a}"' for a in b) + ")"
        for d in ads_query(tok, q, "bibcode,identifier", 6 * len(b)):
            idl = [x.lower() for x in d.get("identifier", [])]
            for a in b:
                if f"arxiv:{a.lower()}" in idl or a.lower() in idl:
                    out[a] = d["bibcode"]
        print(f"  resolved arxiv {min(i+40,len(ids))}/{len(ids)}", file=sys.stderr); time.sleep(1)
    return out


def lookup_bibcodes(tok, bibs):
    """stored bibcode -> {exists, arxiv, first_author, year} from ADS."""
    out = {}
    bibs = sorted(set(bibs))
    for i in range(0, len(bibs), 40):
        b = bibs[i:i + 40]
        q = "bibcode:(" + " OR ".join(f'"{x}"' for x in b) + ")"
        for d in ads_query(tok, q, "bibcode,identifier,author,year", 6 * len(b)):
            idl = [x for x in d.get("identifier", []) if x.lower().startswith("arxiv:")]
            ax = idl[0].split(":", 1)[1] if idl else None
            au = (d.get("author") or [""])[0]
            out[d["bibcode"]] = {"exists": True, "arxiv": ax,
                                 "first_author": au.split(",")[0], "year": d.get("year")}
        print(f"  looked up bibcodes {min(i+40,len(bibs))}/{len(bibs)}", file=sys.stderr); time.sleep(1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true")
    a = ap.parse_args()

    files = sorted((ROOT / "data" / "systems").glob("*.json"))
    # collect every (arxiv, bibcode) referenced, with a back-pointer to fix in place
    papers = []
    for f in files:
        d = json.loads(f.read_text())
        blocks = [im.get("paper") for im in d.get("images", [])]
        for pl in d.get("planets", []):
            blocks.append(pl.get("paper")); blocks += pl.get("extra_papers", [])
        for p in blocks:
            if p:
                papers.append(p)
    arxs = [(p.get("arxiv") or "").strip() for p in papers if (p.get("arxiv") or "").strip()]
    bibs = [(p.get("bibcode") or "").strip() for p in papers if (p.get("bibcode") or "").strip()]
    print(f"{len(papers)} paper blocks; {len(set(arxs))} arxiv ids, {len(set(bibs))} stored bibcodes", file=sys.stderr)

    tok = token()
    arx2bib = resolve_arxiv(tok, arxs)
    bibinfo = lookup_bibcodes(tok, bibs)

    findings = defaultdict(list)   # class -> list of (arxiv, stored_bib, canonical)
    fixes = {}                     # stored_bib -> canonical  (unique corrections)
    seen = set()
    for p in papers:
        ax = (p.get("arxiv") or "").strip()
        sb = (p.get("bibcode") or "").strip()
        key = (ax, sb)
        if key in seen:
            continue
        seen.add(key)
        canon = arx2bib.get(ax)
        if not sb:
            if not canon:
                findings["NO_BIB"].append((ax, sb, canon))
            continue
        if not ax:
            if not bibinfo.get(sb, {}).get("exists"):
                findings["BIBONLY_BAD"].append((ax, sb, None))
            continue
        if not canon:
            findings["ARXIV_UNRESOLVED"].append((ax, sb, None))
            continue
        if sb == canon:
            continue                                   # perfect
        is_eprint = lambda b: bool(re.search(r"arxiv|astro\.ph", b or "", re.I))
        if is_eprint(canon) and not is_eprint(sb):
            continue          # ADS returned the eprint form; keep the published stored bibcode
        info = bibinfo.get(sb)
        if info and info.get("arxiv") and info["arxiv"].lower() == ax.lower():
            continue                                   # alt/eprint form of same paper -> keep
        if not (info and info.get("exists")):
            findings["HALLUCINATED"].append((ax, sb, canon)); fixes[sb] = canon
        else:
            findings["WRONG_PAPER"].append((ax, sb, canon)); fixes[sb] = canon

    for cls in ("HALLUCINATED", "WRONG_PAPER", "BIBONLY_BAD", "ARXIV_UNRESOLVED", "NO_BIB"):
        items = findings.get(cls, [])
        if not items:
            continue
        print(f"\n== {cls} ({len(items)}) ==")
        for ax, sb, canon in items:
            print(f"  arXiv:{ax or '-':<14} stored={sb or '-':<22} -> canonical={canon or '?'}")

    if a.fix and fixes:
        n = 0
        for f in files:
            d = json.loads(f.read_text()); changed = False
            blocks = [im.get("paper") for im in d.get("images", [])]
            for pl in d.get("planets", []):
                blocks.append(pl.get("paper")); blocks += pl.get("extra_papers", [])
            for p in blocks:
                if p and (p.get("bibcode") or "").strip() in fixes:
                    old = p["bibcode"].strip()
                    # only rewrite when the arxiv matches (safety against shared bibcode strings)
                    if fixes[old]:
                        p["bibcode"] = fixes[old]; changed = True; n += 1
            if changed:
                f.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
        print(f"\nfixed {n} record bibcode(s)", file=sys.stderr)
    elif fixes:
        print(f"\n{len(fixes)} correctable bibcode(s) -- rerun with --fix to apply", file=sys.stderr)


if __name__ == "__main__":
    main()
