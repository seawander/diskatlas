# backend-infra/ — infrastructure & CI tooling

Home for the **infra track**'s scripts: CI guards, deploy helpers, and
frontend checks. Kept separate from `backend-data/` (the scientific pipeline)
so the two tracks don't collide (see `CLAUDE.md`, "Two work tracks").

Nothing here is loaded by the site at runtime — these are developer/CI tools.

## Contents

| File | What it does | Runtime |
|---|---|---|
| `check_data_sync.py` | Fails if `frontend/data.js` is out of sync with `data/systems/*.json` (someone edited a record without re-running `build.py`, or hand-edited `data.js`). Compares only the deterministic, data-derived parts — ignores the `generated` timestamp and the paper-count stats that depend on the gitignored `candidates.json`. Side-effect-free (restores `data.js`). | Python 3, stdlib only |
| `check_images.py` | Fails if any non-null image `file` referenced by `data.js` is missing on disk or over the ≤640 px hard cap; warns on crops over ~300 KB. Gates the *deployed* image contract (no broken `<img>` on the live site). | Python 3, stdlib only |
| `check_i18n.js` | Fails if any of the 12 UI languages is missing a key present in `en` (keeps `i18n.js` complete). Reports the missing keys per language. | Node (no deps) |
| `check_all.sh` | One-shot runner for all of the above + the frontend logic tests — mirrors CI locally (~0.3 s; node steps skipped with a warning if node is absent). Intended as a `.git/hooks/pre-push` hook on the shared checkout so neither track can push a commit CI would reject: `printf '#!/usr/bin/env bash\nexec bash backend-infra/check_all.sh\n' > .git/hooks/pre-push && chmod +x .git/hooks/pre-push` | bash |

## Running locally

```sh
python3 backend-infra/check_data_sync.py
python3 backend-infra/check_images.py
node    backend-infra/check_i18n.js
node    backend-data/test_frontend_logic.js   # pure-function tests (owned by the data track)
```

All four run in CI on every push/PR to `master` — see `.github/workflows/ci.yml`.

## Deploy

`.github/workflows/pages.yml` is the **live deploy path** (2026-07-11): the
repo's Pages source is set to "GitHub Actions" (`build_type: workflow`), and
every push to `master` re-runs the guards (`validate` + `check_data_sync` +
`check_images`) and only publishes the site if they pass. `workflow_dispatch`
is kept so a deploy can also be triggered by hand. `.nojekyll` disables Jekyll
so dotfiles and `_`-prefixed paths are served verbatim.

Note: the Pages artifact (`actions/upload-pages-artifact`, `path: .`) does **not
publish `.github/`** — put any served asset (e.g. the OG card image) under a
normal directory like `frontend/`, not `.github/`.

See `backend-infra/data-split-proposal.md` for a cross-track first-paint
optimization flagged to the data track.
