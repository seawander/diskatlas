# Task: publish the diskatlas repository to GitHub

You are working in `/home/brinen2spark/Developments/diskatlas`. Your job is to put this
project on GitHub cleanly (create the remote repo, push, and optionally enable GitHub
Pages). Read this whole brief first — it tells you what the project is, what is safe to
push, and which decisions you must ask the user about instead of deciding yourself.

## What this project is

An **offline, interactive all-sky atlas** of every system with a resolved circumstellar
disk (mm/submm interferometry, scattered light, thermal IR), a directly imaged
planet/companion, or a coronagraphically imaged quasar host. ~462 systems / ~1420 image
records, each image a small cropped panel from the discovery/characterization paper with
full arXiv/SciX citation links. Built and curated by the user (an astronomer) with
Claude Code across many sessions; it accompanies a paper in preparation (Overleaf dir is
gitignored).

**The whole app is static**: double-click `index.html` and it works from `file://` — no
server, no build step, no CDN, vanilla ES2018 JS. This makes it a perfect GitHub Pages
candidate with zero configuration.

## Repository layout (already documented in README.md — read it)

- `index.html` + `frontend/` — the app (app.js, style.css, i18n.js with 12 languages,
  and **`frontend/data.js` which is GENERATED** by `backend/build.py` from
  `data/systems/*.json`; never hand-edit it).
- `data/systems/*.json` — one file per system: the scientific database.
- `data/paper_finder/`, `data/staging/`, ledgers — internal literature-crawl pipeline
  state (~500 tracked files, largest 8.7 MB `candidates.json`).
- `backend/` — Python build/validate/ingestion tooling. `python3 backend/validate.py`
  must report 0 errors after any data change.
- `images/` — 1421 tracked cropped PNGs (~122 MB). `images/_sources/` (3 GB of
  downloaded source figures) is **gitignored — never force-add it**.
- `HANDOFF.md`, `CONTINUATION_PROMPTS.md`, `.claude/skills/…` — internal agent docs and
  a custom skill; harmless but ask the user if they want them public.

## Git facts you need

- Canonical branch: **`master`** (in this main checkout). Everything user-facing is
  merged there. Total tracked payload ≈ **216 MB**, largest file 8.7 MB → **no LFS
  needed**, first push will be a few hundred MB with history (.git ≈ 209 MB).
- There are ~8 `claude/*` branches — session worktree branches (some registered as git
  worktrees under `.claude/worktrees/`). **Push only `master`** unless told otherwise.
  Do not delete branches or worktrees without asking: other Claude sessions may be
  using them.
- **Multiple Claude sessions commit to `master` concurrently** (data ingestion, frontend
  fixes). Before any operation that needs a clean tree, run `git status` — if there are
  uncommitted *tracked* changes, another session is mid-work: do NOT stash or revert
  its files; wait or ask.
- No remote is configured yet. Use the `gh` CLI (`gh repo create`), confirm with the
  user before creating anything public.
- Commits are authored as `brinen2spark <rbb@xmu.edu.cn>` (academic email). Pushing
  publishes this in the history — confirm the user is fine with that (rewriting history
  to hide it is possible but invasive; likely they'll say it's fine).

## Decisions that belong to the user — ASK, don't assume

1. **Repo name & visibility** (suggest `diskatlas`, public — but ask).
2. **License.** None exists. Code (frontend/backend) vs data (`data/systems`) vs images
   are different questions. The images are **crops of figures from copyrighted journal
   papers** (A&A, ApJ, MNRAS…), each with a credit line in its record. Redistribution
   judgment is the user's call as the domain expert — do not slap MIT on the whole repo.
   A reasonable menu: MIT/BSD for code, CC BY for the compiled database, and an explicit
   README note that image cutouts remain © the original publishers, reproduced with
   credit for scholarly purposes. Let the user choose.
3. **Internal pipeline state** (`data/paper_finder/`, `data/staging/`, `HANDOFF.md`,
   `CONTINUATION_PROMPTS.md`, this file): publish as-is (reproducibility) or exclude?
   Note: excluding means either .gitignore + `git rm --cached` (keeps history) or
   history rewrite (do NOT rewrite without explicit approval).
4. **GitHub Pages**: enable from `master` root? The app works as-is (site would be
   `https://<user>.github.io/<repo>/`). Also suggest repo topics
   (`astronomy`, `exoplanets`, `protoplanetary-disks`, `dataviz`) and a `CITATION.cff`
   once the paper has a reference — ask if they want a placeholder now.

## Suggested procedure

1. `git status` in the main checkout — confirm no other session is mid-work.
2. Ask the user the four decision questions above (one round of questions).
3. `gh auth status` → `gh repo create <name> --source . --push` (or add remote + push
   `master` only). Never `git push --all` (that would publish the 8 session branches).
4. If Pages requested: `gh api` or `gh repo edit` to enable Pages from master `/ (root)`,
   then fetch the URL and verify the atlas loads (sky map canvas renders, a detail
   panel opens).
5. Post-push verification: `gh repo view --web`-level sanity, plus a fresh
   `git clone` into /tmp and double-click-equivalent check (`python3 -m http.server` +
   curl the index, or open in browser) to prove the published tree is self-contained.
6. Report the repo URL, what was pushed (branch, commit), and any follow-ups (license
   file added? Pages URL? CITATION.cff?).

## Hard rules

- Never hand-edit `frontend/data.js`; regenerate via `python3 backend/build.py`.
- Keep `python3 backend/validate.py` at 0 errors.
- Don't touch `images/_sources/` or `paper_Overleaf/` (both gitignored, both huge or
  private).
- Don't rewrite history, delete branches, or force-push without explicit user approval.
- If port 8123 is busy (another session's preview server), use a different port.
