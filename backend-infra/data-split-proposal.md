# Proposal (infra → data track): split data.js for faster first paint

**Status:** flagged, not implemented. This touches `backend-data/build.py`, which
is the **data track**'s to own — the infra track will do the frontend-side
consumption once/if the data track adopts the split.

## Why

`frontend/data.js` is one ~1.6 MB blob loaded as a synchronous `<script>` before
`app.js` runs. Over the wire it's already small (~253 KB gzipped, and Pages
auto-gzips), so this is **not** a network problem — it's a **parse + first-paint**
cost on low-end mobile: the whole 1.6 MB JSON is parsed before the sky map can
draw its first frame.

The sky map + search only need a *small* slice of each system: `id`, `name`,
`alt_names`, `ra_deg`, `dec_deg`, `categories`, planet/image *presence* flags,
and the faceting keys. The heavy part — every image record's `paper`, `credit`,
`wavelength_label`, `notes`, `epoch`, etc. — is only read when a detail card
opens. That's ~80–90% of the bytes, needed by ~0% of first paints.

## Constraint (do not break)

`file://` (double-click) use is a hard requirement, which is why the site uses
`<script>` includes, not `fetch()`/ES-modules (see `frontend/README.md`).
`fetch()` is blocked under `file://` — **but dynamically injecting a `<script>`
element is not.** So the lazy tier must remain a plain JS file loaded via an
injected `<script>`, never `fetch`.

## Proposed shape

`build.py` emits two files instead of one:

- `frontend/data-core.js` (eager, loaded in `index.html` as today): the light
  per-system fields above + `stats` + `generated`. Sets `window.ATLAS` with the
  systems array, but each system's `images[]` carries only what markers/facets
  need (or a compact `img_summary`), plus its `id` for the detail lookup.
- `frontend/data-detail.js` (lazy): `window.ATLAS_DETAIL = { "<system-id>":
  { images:[...full records...], notes, planets:[...] }, ... }`. Injected by
  `app.js` right after first paint (`requestIdleCallback` / a `load` handler).

`app.js` (infra side) then: renders the map from `data-core.js` immediately;
when a detail card opens, reads from `window.ATLAS_DETAIL` if present, else
injects `data-detail.js` on demand and opens once it loads.

## Payoff vs. cost

- **Payoff:** first paint parses only the light core (a fraction of 1.6 MB);
  the heavy tier loads off the critical path. Most visible on phones.
- **Cost:** two generated files + a second `<script>` injection path; the CI
  sync-check (`backend-infra/check_data_sync.py`) must learn about both files;
  a slightly more complex detail-open path. Modest, since the wire cost is
  already tiny — worth doing only if mobile first-paint becomes a real concern.

## If adopted

1. Data track: teach `build.py` to emit the two files; keep `stats`/`generated`
   in the core.
2. Infra track: update `index.html` (core `<script>`), `app.js` (lazy inject +
   detail lookup), `sw.js` precache list (add both files), and
   `check_data_sync.py` (compare both).
