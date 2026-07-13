# AGENTS.md — brief for AI coding agents

This file orients any agent/harness (Claude Code, OpenCode, Cursor, Codex, Aider, …)
working in a clone of **diskatlas**. Claude Code also auto-loads `CLAUDE.md` (same rules,
more detail); the complete handbook is `HANDOFF.md`. Human contributors: see
`CONTRIBUTING.md`.

## What this repo is

An offline, static, double-click-`index.html` all-sky atlas of resolved circumstellar
disks, directly imaged companions, and coronagraphically imaged quasar hosts. Ground
truth is `data/systems/*.json`; **`frontend/data.js` is GENERATED** by
`backend-data/build.py`. `python3 backend-data/build.py` prints the live statistics.

## Orient yourself first (token discipline — do NOT read everything)

1. Read `CLAUDE.md` (rules + a task→doc routing table). Then read ONLY the one doc your
   task needs: records/crops → `HANDOFF.md`; record schema → `data/README.md`; frontend →
   `frontend/README.md`; pipeline scripts → `backend-data/README.md`.
2. Never load into context: `frontend/data.js`, `data/paper_finder/candidates.*`,
   `data/simbad_raw.txt`, or `docs/HISTORY.md` (grep it). Prefer running the local scripts
   over reading data files.
3. Run `python3 backend-data/validate.py && python3 backend-data/build.py`; confirm 0 errors.

## Hard rules (non-negotiable — a PR that breaks any of these will be rejected)

1. **`validate.py` + `build.py` after every data edit; keep 0 errors / 0 warnings.**
2. **VIEW (open) every crop and every source figure** — panel labels are the only ground
   truth; metadata and memory lie.
3. **Verify every arXiv id / bibcode from the source or ADS, never from memory.**
4. Every new image record carries `epoch` (the OBSERVATION date, read from the paper's
   observing log — not the publication year). One record per wavelength band; re-crop each
   panel from the source; **panel-only** crops (axes/margins trimmed), ≤480 px / ≤300 KB;
   **no press-release images** — only crops from the authors' own arXiv source figures.
5. **Never hand-edit `frontend/data.js`** (generated) — edit `data/systems/*.json` and
   rebuild. Every image needs a `credit` line + citation links.

## To contribute (task template)

Give your agent a one-line task, e.g.:

```
Ingest arXiv:2506.09201 into diskatlas: add/verify the system record + full citation,
fetch the source, crop the figure I name (VIEW it to confirm the panel), record the
observation epoch, then `python3 backend-data/validate.py && python3 backend-data/build.py`
(0 errors), and open a PR. Follow AGENTS.md hard rules and CONTRIBUTING.md.
```

Other entry points: `python3 backend-data/fresh_papers.py` (weekly new-paper digest),
`backend-data/system_audit.py` (per-system instrument-gap audit), or the bundled
`diskatlas-paper-finder` Skill for citation-graph crawling. Full workflow: `CONTRIBUTING.md`.
Open the PR with `gh pr create` and fill in the checklist in the PR template.
