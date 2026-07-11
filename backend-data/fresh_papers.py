#!/usr/bin/env python3
"""Forward-looking literature sweep for diskatlas.

Everything else in backend-data/ is retrospective (citation snowball, backward
references, per-target ADS audit) — and saturated. This tool watches the
literature going FORWARD: it pulls the last N days of astro-ph.EP + astro-ph.SR
submissions from the arXiv API and flags papers that either

  (a) mention an atlas target by name (exact word-boundary match against every
      system's name + alt_names — our own literal matching, so the ADS stemming
      trap "T Tau"->"T Tauri" does not apply), or
  (b) look like a NEW resolved-imaging result (imaging phrase + disk/companion
      context + named facility — same gate philosophy as system_audit.py).

Already-dispositioned papers are skipped via the two ledgers (arXiv ids cited in
data/systems/*.json, and data/paper_finder_state.json). Output is a ranked,
human-reviewable report — every hit still needs the VIEW-the-figure check before
ingestion.

Recent submissions come from the anonymous ADS API (arxiv_class + entdate),
NOT the arXiv API — arXiv's export endpoint hard-429s this host, while ADS
ingests arXiv daily and has been reliable (same bootstrap-token access used by
system_audit.py / audit_bibcodes.py).

Intended cadence: run weekly (cron or by hand).

Usage:
  python3 backend-data/fresh_papers.py                # last 14 days
  python3 backend-data/fresh_papers.py --days 30
"""
import argparse, json, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "paper_finder" / "fresh_papers.json"
ADS = "https://api.adsabs.harvard.edu/v1/search/query"

POS = re.compile(
    r"\b(resolved|scattered[- ]?light|coronagraph|polarimetr|polarized|"
    r"direct(ly)?[- ]imag|high[- ]contrast|continuum (image|emission|map|observation)|"
    r"angular differential|reference[- ]?differential|Q_?phi|dust continuum|"
    r"milli(meter|metre) (image|continuum|emission)|we (present|report) .{0,40}imag)\b", re.I)
CTX = re.compile(
    r"\b(circumstellar|protoplanetary|planet-?forming|transition(al)? dis[ck]|"
    r"debris dis[ck]|dis[ck] around|young stellar object|YSO|T Tauri|Herbig|"
    r"pre-main[- ]sequence|protostar|substellar companion|directly imaged)\b", re.I)
FAC = re.compile(
    r"\b(SPHERE|GPI|ALMA|NIRC2|JWST|NIRCam|MIRI|SCExAO|CHARIS|VAMPIRES|VISIR|NACO|"
    r"LBTI?|MagAO(-X)?|NICMOS|STIS|WFC3|SMA|VLA|Keck|Subaru|Gemini|VLTI?|GRAVITY|"
    r"MATISSE|ERIS|HiCIAO|NIRI|ZIMPOL|IRDIS)\b")


def load_ledgers():
    """arXiv ids already handled -> skip."""
    done = set()
    for f in (ROOT / "data" / "systems").glob("*.json"):
        d = json.loads(f.read_text())
        blocks = [im.get("paper") for im in d.get("images", [])]
        for pl in d.get("planets", []):
            blocks.append(pl.get("paper")); blocks += pl.get("extra_papers", []) or []
        for p in blocks:
            if p and p.get("arxiv"):
                done.add(p["arxiv"].lower())
    state = ROOT / "data" / "paper_finder_state.json"
    if state.exists():
        # flat dict; keys are Semantic Scholar hashes (from find_papers.py) OR
        # arXiv ids (added by fresh_papers reviews) -- only the latter match here
        for k in json.loads(state.read_text()):
            if re.match(r"^\d{4}\.\d{4,5}$|^astro-ph/\d{7}$", k):
                done.add(k.lower())
    return done


def load_names():
    """(system_id, compiled word-boundary regex) for every usable name/alias."""
    pats = []
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        names = [d.get("name") or ""] + (d.get("alt_names") or [])
        for n in names:
            n = (n or "").strip()
            # too short / too generic to match safely
            if len(n) < 4 or n.lower() in {"vega"} and False:
                continue
            if len(n) < 4:
                continue
            # allow flexible whitespace/hyphen between tokens (HD 34700 == HD34700)
            body = r"[\s\-]?".join(re.escape(t) for t in re.split(r"[\s\-]+", n))
            pats.append((d["id"], n, re.compile(r"(?<![A-Za-z0-9])" + body + r"(?![A-Za-z0-9])")))
    return pats


def ads_token():
    return json.loads(urllib.request.urlopen(
        "https://ui.adsabs.harvard.edu/v1/accounts/bootstrap", timeout=60
    ).read())["access_token"]


def fetch_recent(days):
    tok = ads_token()
    since = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
    q = f'arxiv_class:("astro-ph.EP" OR "astro-ph.SR") entdate:["{since}" TO *]'
    entries, start = [], 0
    while True:
        p = {"q": q, "fl": "bibcode,identifier,title,abstract,first_author,entry_date",
             "rows": "200", "start": str(start), "sort": "entry_date desc"}
        url = ADS + "?" + urllib.parse.urlencode(p)
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}",
                                                   "User-Agent": "diskatlas-fresh"})
        for attempt in range(4):
            try:
                resp = json.loads(urllib.request.urlopen(req, timeout=90).read())["response"]
                break
            except Exception as e:
                if attempt == 3:
                    raise
                print(f"  ADS retry ({e})", file=sys.stderr); time.sleep(15)
        for d in resp["docs"]:
            ids = [i.split(":", 1)[1] for i in d.get("identifier", []) if i.lower().startswith("arxiv:")]
            if not ids:
                continue
            entries.append({
                "arxiv": ids[0],
                "published": (d.get("entry_date") or "")[:10],
                "title": (d.get("title") or [""])[0],
                "abstract": d.get("abstract") or "",
                "first_author": d.get("first_author") or "",
            })
        n = resp["numFound"]
        print(f"  fetched {min(start+200, n)}/{n} (kept {len(entries)} arXiv entries)", file=sys.stderr)
        start += 200
        if start >= n:
            break
        time.sleep(0.5)
    return entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    a = ap.parse_args()

    done = load_ledgers()
    names = load_names()
    print(f"ledger: {len(done)} arXiv ids dispositioned; {len(names)} name patterns", file=sys.stderr)
    entries = fetch_recent(a.days)
    print(f"{len(entries)} astro-ph.EP/SR submissions in the last {a.days} days", file=sys.stderr)

    target_hits, keyword_hits = [], []
    for e in entries:
        if e["arxiv"].lower() in done:
            continue
        blob = e["title"] + " " + e["abstract"]
        hits = sorted({sid for sid, n, rx in names if rx.search(blob)})
        imaging = bool(POS.search(blob) and FAC.search(blob))
        if hits and (imaging or CTX.search(blob)):
            target_hits.append({**e, "systems": hits, "imaging": imaging})
        elif imaging and CTX.search(blob):
            keyword_hits.append({**e, "systems": [], "imaging": True})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"generated": datetime.now(timezone.utc).isoformat(),
                               "days": a.days, "n_scanned": len(entries),
                               "target_hits": target_hits,
                               "keyword_hits": keyword_hits}, indent=1, ensure_ascii=False))

    print(f"\n==== {len(target_hits)} papers mentioning atlas targets ====")
    for h in target_hits:
        tag = "IMG" if h["imaging"] else "   "
        print(f"  {h['published']} {h['arxiv']:13s} {tag} [{','.join(h['systems'])[:38]:38s}] "
              f"{h['first_author'].split(',')[0][:14]:14s} {h['title'][:56]}")
    print(f"\n==== {len(keyword_hits)} possible NEW resolved-imaging papers (no known target) ====")
    for h in keyword_hits:
        print(f"  {h['published']} {h['arxiv']:13s}     {h['first_author'].split(',')[0][:14]:14s} {h['title'][:70]}")
    print(f"\nreport -> {OUT}   (every hit still needs the VIEW-the-figure check)")


if __name__ == "__main__":
    main()
