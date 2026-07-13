<!-- Thanks for contributing to diskatlas! See CONTRIBUTING.md and AGENTS.md. -->

## What this PR does

<!-- e.g. "Add SPHERE Ks Qphi panel for HD 34700 from Ren et al. 2023 Fig. 2", or
"Ingest arXiv:2506.09201 (14 Her c, JWST/NIRCam)". Name the paper + figure. -->

## Checklist

Tick every box (delete rows that truly don't apply, e.g. a frontend-only PR):

- [ ] `python3 backend-data/validate.py` reports **0 errors / 0 warnings**
- [ ] `frontend/data.js` was **regenerated** with `python3 backend-data/build.py`, not hand-edited
- [ ] Every new image crop was **VIEWed** to confirm the panel matches its metadata
- [ ] Crops are **panel-only** (axes/margins trimmed), ≤ 480 px and ≤ 300 KB, one record per band
- [ ] Images are crops of the **authors' own arXiv source figures** — no press-release / journal-typeset images
- [ ] Every image record has a `credit` line and citation links (arXiv / SciX / DOI)
- [ ] Each new record carries the **observation `epoch`** (from the paper's observing log, not the publication year)
- [ ] arXiv ids / bibcodes were **verified from the source or ADS** (not from memory)
- [ ] Ledgers updated if relevant: `data/ingestion_status.json` and/or `data/paper_finder_state.json`

## Notes for the reviewer

<!-- Anything non-obvious: distance/parallax choices, disputed companion status, why a
borderline object is in scope, etc. -->
