# diskatlas — agent quick context

Offline all-sky atlas of resolved circumstellar disks, imaged companions, and
quasar hosts. Static files; `data/systems/*.json` is ground truth,
`frontend/data.js` is GENERATED (never hand-edit).

## Two work tracks — split by concern (2026-07-11)

Work is split so parallel sessions don't collide:
- **`backend-data/`** (THIS track) — the SCIENTIFIC pipeline: seed → coords →
  crop → validate → build, plus ADS/arXiv/SIMBAD ingestion & audit tooling.
  Owns `data/` (systems, ledger, provenance) and all image ingestion. Scientific
  correctness lives here.
- **`backend-infra/`** — INFRASTRUCTURE & app development (a SEPARATE session):
  the `frontend/` viewer (index.html, app.js, styles, i18n), the build/deploy
  path (GitHub Pages), performance, search/faceting, offline packaging, tests.

`frontend/data.js` is the contract between them: `backend-data/build.py`
GENERATES it from `data/systems/*.json`; the infra track CONSUMES it and never
hand-edits it. On a shared checkout, keep each change on the side that owns it
and rebuild before committing — do not let `git add -A` sweep the other track's
work (shared-checkout race).

## Read only what your task needs (token discipline)

| Task | Read |
|---|---|
| Any edit to records/images | `HANDOFF.md` (method + gotchas, ~3k tokens) |
| Record schema question | `data/README.md` |
| Crop protocol for agents | `backend-data/AGENT_BRIEFS.md` |
| Pipeline script details | `backend-data/README.md` |
| Frontend/UI work | `frontend/README.md` |
| What happened on date X | `grep` (not read!) `docs/HISTORY.md` |
| What's queued | `data/ingestion_status.json` |
| Contributing / opening a PR | `CONTRIBUTING.md` (human + agent recipe) |
| On a non-Claude harness (OpenCode/Cursor/…) | `AGENTS.md` (vendor-neutral mirror of this file) |

**NEVER load into context**: `data/paper_finder/candidates.md` (~330k tokens,
machine-generated), `frontend/data.js` (generated, ~MB), `data/simbad_raw.txt`,
`data/coverage_todo.md`, `data/staging/_report_*.md` (archives),
`docs/HISTORY.md` in full (grep it). Prefer running local scripts
(`validate.py`, `build.py`, `epoch_audit.py`, `crop_qa.py`) over reading data
files — compute locally, spend tokens on judgement.

**Environment**: reference platform is the maintainer's NVIDIA DGX Spark, but
any platform with Python 3 works. **Live internet from the shell is REQUIRED**
(arXiv, SIMBAD, ADS, observatory archives — the agents' parsing work depends
on it). Verify first: `curl -sI https://arxiv.org`.

## Ironclad rules

1. `python3 backend-data/validate.py && python3 backend-data/build.py` after every data
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
