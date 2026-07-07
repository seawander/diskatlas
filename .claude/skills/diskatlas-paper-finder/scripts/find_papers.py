#!/usr/bin/env python3
"""diskatlas paper finder — citation-chase new resolved-image papers.

Seeds = every arXiv id cited anywhere in data/systems/*.json.
For each seed, fetch the papers that CITE it (Semantic Scholar Graph API,
no key needed; cached + resumable). Candidates that are not yet cited in the
atlas and look like imaging papers are ranked by how many distinct seeds they
cite ("hub score") and written to data/paper_finder/candidates.{json,md}.

Dispositions live in data/paper_finder_state.json:
    {"<arxiv or s2 id>": {"status": "ingested|excluded", "reason": "...", "date": "..."}}

Usage:
  find_papers.py --repo <path> [--max-seeds N] [--min-year 2015]
  find_papers.py --repo <path> --mark <arxiv_id> ingested|excluded "reason"
"""
import argparse, json, glob, os, re, sys, time, urllib.request, urllib.parse
from collections import defaultdict
from datetime import date

API = "https://api.semanticscholar.org/graph/v1/paper/arXiv:{}/citations"
FIELDS = "externalIds,title,year,abstract,venue"

KEY_POS = re.compile(
    r"resolv|imag|coronagraph|polarimetr|interferometr|scattered.light|continuum|"
    r"ring|gap|spiral|cavity|substructure|companion|protoplanet|direct.detect|"
    r"high.contrast|host.galaxy", re.I)
KEY_DOM = re.compile(r"\bdisk|\bdisc|planet|companion|quasar|protostar|debris|YSO", re.I)


def load_seeds(repo):
    seeds = set()
    for f in glob.glob(os.path.join(repo, "data/systems/*.json")):
        d = json.load(open(f))
        papers = [i.get("paper") for i in d.get("images", [])]
        for p in d.get("planets", []):
            papers.append(p.get("paper"))
            papers += p.get("extra_papers", [])
        for p in papers:
            if p and p.get("arxiv"):
                seeds.add(p["arxiv"].strip())
    return sorted(seeds)


def fetch_citations(aid, cache_dir):
    """All citing papers of one seed, cached on disk."""
    cf = os.path.join(cache_dir, aid.replace("/", "_") + ".json")
    if os.path.exists(cf):
        return json.load(open(cf))
    out, offset = [], 0
    while True:
        url = API.format(urllib.parse.quote(aid)) + \
            f"?fields={FIELDS}&limit=100&offset={offset}"
        for attempt in range(6):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "diskatlas-paper-finder"})
                data = json.load(urllib.request.urlopen(req, timeout=60))
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(5 * (attempt + 1)); continue
                if e.code == 404:          # seed unknown to S2
                    data = {"data": []}; break
                raise
        else:
            print(f"  ! giving up on {aid} (rate limited)", file=sys.stderr)
            return None                    # do NOT cache failures
        out += data.get("data", [])
        if "next" not in data or not data.get("data"):
            break
        offset = data["next"]
        time.sleep(1.1)
    json.dump(out, open(cf, "w"))
    time.sleep(1.1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--max-seeds", type=int, default=0, help="0 = all")
    ap.add_argument("--min-year", type=int, default=2010)
    ap.add_argument("--mark", nargs=3, metavar=("ARXIV", "STATUS", "REASON"))
    a = ap.parse_args()

    state_f = os.path.join(a.repo, "data/paper_finder_state.json")
    state = json.load(open(state_f)) if os.path.exists(state_f) else {}

    if a.mark:
        aid, status, reason = a.mark
        state[aid] = {"status": status, "reason": reason, "date": str(date.today())}
        json.dump(state, open(state_f, "w"), indent=1)
        print(f"marked {aid}: {status} ({reason})")
        return

    outdir = os.path.join(a.repo, "data/paper_finder")
    cache = os.path.join(outdir, "cache")
    os.makedirs(cache, exist_ok=True)

    seeds = load_seeds(a.repo)
    if a.max_seeds:
        seeds = seeds[:a.max_seeds]
    seedset = set(seeds)
    print(f"{len(seeds)} seed papers")

    hits = defaultdict(lambda: {"cites": set(), "meta": None})
    done = failed = 0
    for i, s in enumerate(seeds):
        rows = fetch_citations(s, cache)
        if rows is None:
            failed += 1; continue
        done += 1
        for r in rows:
            p = r.get("citingPaper") or {}
            ext = p.get("externalIds") or {}
            aid = ext.get("ArXiv")
            key = aid or p.get("paperId")
            if not key:
                continue
            hits[key]["cites"].add(s)
            hits[key]["meta"] = p
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(seeds)} seeds processed ({len(hits)} candidates so far)")

    cands = []
    for key, v in hits.items():
        p = v["meta"]; ext = p.get("externalIds") or {}
        aid = ext.get("ArXiv")
        if aid and aid in seedset:            # already cited in atlas
            continue
        if key in state or (aid and aid in state):
            continue                          # already dispositioned
        if (p.get("year") or 0) < a.min_year:
            continue
        text = (p.get("title") or "") + " " + (p.get("abstract") or "")
        if not (KEY_POS.search(text) and KEY_DOM.search(text)):
            continue
        cands.append({
            "arxiv": aid, "s2": p.get("paperId"), "title": p.get("title"),
            "year": p.get("year"), "venue": p.get("venue"),
            "n_seed_citations": len(v["cites"]),
            "seeds_cited": sorted(v["cites"])[:12],
            "abstract": (p.get("abstract") or "")[:600],
        })
    cands.sort(key=lambda c: (-c["n_seed_citations"], -(c["year"] or 0)))

    json.dump(cands, open(os.path.join(outdir, "candidates.json"), "w"), indent=1)
    with open(os.path.join(outdir, "candidates.md"), "w") as fh:
        fh.write(f"# paper-finder candidates ({date.today()}) — "
                 f"{done}/{len(seeds)} seeds fetched ({failed} failed), "
                 f"{len(cands)} candidates\n\n")
        for c in cands:
            fh.write(f"- **{c['n_seed_citations']}× cited-seeds** | "
                     f"arXiv {c['arxiv'] or '—'} | {c['year']} | {c['title']}\n")
    print(f"done: {done} seeds fetched, {failed} failed/skipped, "
          f"{len(cands)} candidates -> {outdir}/candidates.json")


if __name__ == "__main__":
    main()
