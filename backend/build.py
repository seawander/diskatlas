#!/usr/bin/env python3
"""Compile data/systems/*.json -> frontend/data.js (+ ingestion stats).

frontend/data.js:  window.ATLAS = {generated, stats, systems:[...]};
Image 'file' paths are kept relative to repo root (index.html lives at root).
Systems without coordinates are included but flagged (frontend lists them
in search but cannot plot them).
"""
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / "data" / "systems"
OUT = ROOT / "frontend" / "data.js"


def main():
    from facility_map import fac_keys, instr_key
    systems = []
    for f in sorted(SYS.glob("*.json")):
        s = json.loads(f.read_text())
        for im in s.get("images", []):
            p = im.get("paper") or {}
            p.pop("_verify", None)
            im["fac_keys"] = fac_keys(im.get("facility"), im.get("instrument"))
            im["instr_key"] = instr_key(im.get("facility"), im.get("instrument"))
        systems.append(s)

    n_coord = sum(1 for s in systems if s.get("ra_deg") is not None)
    n_img = sum(len(s.get("images", [])) for s in systems)
    n_file = sum(1 for s in systems for im in s.get("images", []) if im.get("file"))
    n_planet = sum(1 for s in systems
                   if any(p.get("status") != "refuted" for p in s.get("planets", [])))

    # literature-exploration progress (three ledgers -> one bar in the frontend)
    atlas_ids = set()
    for s in systems:
        papers = [i.get("paper") for i in s.get("images", [])]
        for pl in s.get("planets", []):
            papers.append(pl.get("paper"))
            papers += pl.get("extra_papers", [])
        for pp in papers:
            if pp and pp.get("arxiv"):
                atlas_ids.add(pp["arxiv"].strip())
    state_f = ROOT / "data" / "paper_finder_state.json"
    state = json.loads(state_f.read_text()) if state_f.exists() else {}
    cand_f = ROOT / "data" / "paper_finder" / "candidates.json"
    cands = json.loads(cand_f.read_text()) if cand_f.exists() else []
    cand_ids = {(c.get("arxiv") or c.get("s2")) for c in cands if (c.get("arxiv") or c.get("s2"))}
    universe = cand_ids | set(state) | atlas_ids
    explored = atlas_ids | set(state)
    paper_stats = {"papers_known": len(universe), "papers_explored": len(explored),
                   "papers_in_atlas": len(atlas_ids)}
    stats = {"systems": len(systems), "with_coords": n_coord,
             "image_records": n_img, "with_local_image": n_file,
             "planet_hosts": n_planet, **paper_stats}

    payload = {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
               "stats": stats, "systems": systems}
    OUT.write_text("window.ATLAS = " +
                   json.dumps(payload, ensure_ascii=False, separators=(",", ":")) +
                   ";\n")
    print("wrote", OUT)
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
