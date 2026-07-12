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

## Running locally

```sh
python3 backend-infra/check_data_sync.py
python3 backend-infra/check_images.py
node    backend-infra/check_i18n.js
node    backend-data/test_frontend_logic.js   # pure-function tests (owned by the data track)
```

All four run in CI on every push/PR to `master` — see `.github/workflows/ci.yml`.

## Deploy

`.github/workflows/pages.yml` builds the repo as a GitHub Pages artifact and
deploys it, **gated on the CI job passing**. It is currently `workflow_dispatch`
only (manual) because the repo's Pages source is still "Deploy from a branch"
(`build_type: legacy`). To make it the live, CI-gated deploy path:

1. Repo → Settings → Pages → **Source: GitHub Actions**
   (or `gh api -X POST repos/OWNER/REPO/pages -f build_type=workflow`).
2. Change `pages.yml`'s trigger from `workflow_dispatch` to `push` on `master`.

See `backend-infra/data-split-proposal.md` for a cross-track first-paint
optimization flagged to the data track.
