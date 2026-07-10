# diskatlas — agent quick context

Offline all-sky atlas of resolved circumstellar disks, imaged companions, and
quasar hosts. Static files; `data/systems/*.json` is ground truth,
`frontend/data.js` is GENERATED (never hand-edit).

## Read only what your task needs (token discipline)

| Task | Read |
|---|---|
| Any edit to records/images | `HANDOFF.md` (method + gotchas, ~3k tokens) |
| Record schema question | `data/README.md` |
| Crop protocol for agents | `backend/AGENT_BRIEFS.md` |
| Pipeline script details | `backend/README.md` |
| Frontend/UI work | `frontend/README.md` |
| What happened on date X | `grep` (not read!) `docs/HISTORY.md` |
| What's queued | `data/ingestion_status.json` |

**NEVER load into context**: `data/paper_finder/candidates.md` (~330k tokens,
machine-generated), `frontend/data.js` (generated, ~MB), `data/simbad_raw.txt`,
`data/coverage_todo.md`, `data/staging/_report_*.md` (archives),
`docs/HISTORY.md` in full (grep it). Prefer running local scripts
(`validate.py`, `build.py`, `epoch_audit.py`, `crop_qa.py`) over reading data
files — this machine has live internet + full Python; compute locally, spend
tokens on judgement.

## Ironclad rules

1. `python3 backend/validate.py && python3 backend/build.py` after every data
   edit; keep 0 errors / 0 warnings.
2. VIEW (Read tool) every crop and every source figure — panel labels are the
   only ground truth; metadata and memory lie.
3. Verify arXiv ids / bibcodes from the source or ADS, never from memory.
4. Every new image record carries `epoch` (OBSERVATION date, not publication
   year) read from the paper's observing log at ingestion.
5. One record per wavelength band; re-crop panels from source; panel-only crops
   ≤480 px / ≤300 KB; no press-release images.
6. Commit to `master` directly (no PRs); push only when the user says "gp";
   review-fix commits say "internal review fix", never "referee".
7. Ledger updates: one short dated line in `data/ingestion_status.json`
   `updated`; narrative details are APPENDED to `docs/HISTORY.md`.
8. `paper_Overleaf/` is gitignored (Overleaf-bound); paper & source PDFs stay
   off GitHub.
9. Reply in English.
