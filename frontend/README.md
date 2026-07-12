# frontend/

Single-page, zero-dependency, fully offline. Root `index.html` loads, in order:

- `frontend/style.css`
- `frontend/data.js`         — **GENERATED** by `backend-data/build.py`. Never hand-edit.
- `frontend/constellations.js` — **GENERATED** by `backend-data/gen_constellations.py`. Never hand-edit.
- `frontend/i18n.js`         — UI translations (hand-edited).
- `frontend/app.js`          — all logic (vanilla JS, no build step, no CDN, system fonts).

`data.js` sets `window.ATLAS = { generated, stats, systems:[...] }` (schema = `data/README.md`,
with image `file` paths relative to the repo root). Using `<script>` includes instead of
`fetch()` is what makes `file://` (double-click) work — **do not** "modernize" this into
fetch/ES-modules, and keep everything **ES2018-compatible**.

## Features & where they live in app.js

| Feature | Functions |
|---|---|
| Equirectangular all-sky canvas, RA increasing leftward; pan/zoom, galactic-plane + ecliptic curves, RA/Dec grid | `draw()`, `project()`, `unproject()`, `clampView()` |
| Mouse: drag=pan, wheel=zoom, click=details, dbl-click=zoom-in | `mousedown`/`wheel`/`dblclick` handlers |
| **Touch (phones/tablets): one-finger pan, two-finger pinch-zoom (anchored at midpoint), double-tap zoom.** `#sky` has `touch-action:none` | `touchstart`/`touchmove`/`touchend` handlers |
| Markers: SHAPE per category (● proto / ▲ debris / ◆ planet-only / ■ quasar / ⬢ evolved), ★ overlay = imaged-**companion** host; image count sets fill opacity | `draw()`, `sysShape()`, `sysGlyph()`, `sysColorKey()` |
| Constellation lines + **translated** names (`I18N_CONST`, Latin IAU fallback) | `drawConstellations()` |
| Views via top switcher: Sky / Coverage matrix / Tonight. **Re-clicking the active Coverage/Tonight tab returns to Sky; re-clicking Sky collapses the facets** | `setView()`, `buildMatrix()`, `buildTonight()`/`computeTonight()` |
| Coverage matrix + Tonight: **sticky header row + sticky first column** (the `.mscroll` box is the scroller); category down-select chips; sortable; CSV export (Tonight) | `buildMatrix()`, `renderTonight()`, `.mscroll` CSS |
| Facets (Sky only, collapsible; **collapsed by default on phones ≤640px**): Band / Content (continuum⧸line from the record `content` field; mirrored as down-select chips in the Coverage matrix + Tonight) / Missing / Facility (`fac_keys`, VLT⊃VLTI) / Instrument (`instr_key`, parent⊇children so `SPHERE`⊇`SPHERE/IRDIS`, likewise `SCExAO/*`) | `chipGroup()`, `filterSystems()`, `updateFacetVisibility()`, `catChipsHTML()` |
| Facility↔instrument **relationship highlight** (`.rel`): selecting a facility lights its instruments and vice-versa; selecting parent `SPHERE` lights its sub-instruments | `updateRelHighlights()` |
| Light/dark theme toggle (persisted; canvas re-colors via `refreshCOL()`; icon shows current theme; light-mode selected/related chips use `--chipon`/`--chiprel`) | `initTheme()` |
| **i18n: 12 languages** — en zh fr es de it ja pt ru ko hi ar — via `i18n.js` `t()`/`data-i18n`. **Arabic is RTL**: `<html dir>` is set from `I18N_RTL`, and scientific-data containers are forced back to `direction:ltr` (see below) | `applyStaticI18n()`, `setLang()` |
| Wavelength formatting: ≥300 µm renders as **mm** (matches the `WL_BANDS` "mm" band) | `fmtWl()` |
| Citations: arXiv + SciX links; notes auto-linkify "Author+Year". A mention **links to the real abstract** when the paper is recorded in that system (image/planet/`extra_papers`), else falls back to a SciX author search | `linkifyCitations()`, `citeIndex()`, `adsUrl()` |
| Detail panel: wavelength-sorted image slider, prev/next, per-image caption + facility/λ chips. Opening with a Facility **or** Instrument facet active starts on that facility/instrument's first image | `openDetail()`, `buildSlider()`, `showImg()` |
| SIMBAD link per system; explicit `simbad:null` → coordinate-search fallback | `openDetail()` |
| Search box (name/`id`/`alt_names` **plus recorded papers** — author, year, arXiv id, bibcode — so "is paper X in the atlas, and where?" is answerable; a paper-matched row shows 📄 Author Year; survey papers list every target they cover. Substring; dropdown lives **inside** `#topbar` so phone keyboards can't cover it; **↑/↓/Enter keyboard nav**) | `searchEl` handlers, `sysHay()`/`sysPapers()`/`matchedPaper()`, `filterSystems()` |
| Category filters + literature-progress readout collapsed behind an **ⓘ** icon; **GitHub badge** (bottom corner, "contributions welcome", localized, RTL-aware) | filter chips, `#litbar`, `#ghlink` |
| URL hash deep-links `#s=hd-163296&i=3` — system **and** image index (`&i` omitted for the first image; the hash tracks arrow/swipe navigation, so the current view is always shareable; read at boot) | `showImg()` (writes) + boot hash parse (restores) |
| Detail image `alt` = "name — wavelength label"; a 404 (stale cached `data.js` after an id rename, missing offline file) swaps in a translated `d_imgerr` notice instead of a broken-image icon | `showImg()` |
| Pages deploy stamps asset URLs `?v=<commit sha>` (artifact-only; the repo copy stays clean for offline `file://` use) so cached `app.js` can never mix with fresh `data.js` | `.github/workflows/pages.yml` |

## Terminology

Scientific data (names, credits, notes, facilities, techniques) is **never translated**;
it stays in its published form. Directly imaged objects are called **"companions"**, not
"planets", throughout the UI (their planetary nature is often debated) — only
`tag_transiting` keeps "planet" (transit detections are uncontested). Internal keys/ids
(`band_planet`, `col_planet`, data field `planets`) are unchanged; this is display-only.

## Adding / changing UI text (i18n.js)

- Add the key to **all 12 language blocks** (`en zh fr es de it ja pt ru ko hi ar`).
  `t()` falls back to English for any missing key, but aim for full coverage.
- Static elements use `data-i18n="key"` (or `data-i18n-ph` for placeholders); dynamic
  strings call `t("key")`. `applyStaticI18n()` runs on load and on every language switch.
- **RTL (Arabic):** `applyStaticI18n()` sets `document.documentElement.dir` from
  `window.I18N_RTL`. A `[dir="rtl"]` CSS block mirrors the layout, but scientific-data
  containers (`#d_slider`, `#d_caption`, `#d_sub`, `#tooltip`) are forced `direction:ltr`
  so numeric/Latin tokens like "1.6 µm NICI" don't get reordered by the bidi algorithm.
- Constellation names live separately in `window.I18N_CONST` (keyed by Latin IAU name).

## Conventions

- **No external network calls anywhere.** `file://`-safe, ES2018, system fonts only.
- Colors/sizes are CSS variables at the top of `style.css`; light theme overrides them
  under `body.light`. Mobile tweaks live in the `@media (max-width: 640px)` block.
- Scientific-token display uses `dir=ltr` even under RTL (see above).

## Testing / verifying

- `node backend-data/test_frontend_logic.js` exercises the pure functions (projection
  round-trip, hit-testing, filtering, `fmtWl`) via a DOM-less shim. Run after any
  `app.js` change. (Node runs the test; the **app itself** needs no Node.)
- To eyeball changes: serve the repo root (`python3 -m http.server`) and open
  `index.html` — the app is static, so any static server or a plain double-click works.
- After editing `app.js`/`style.css`/`i18n.js`, browsers cache them: hard-refresh
  (Ctrl/Cmd+Shift+R) or bust the cache before re-checking.

## Gotchas (hard-won)

- **Never hand-edit `data.js` / `constellations.js`** — change the source
  (`data/systems/*.json` or the generator) and re-run `backend-data/build.py`.
- **Concurrent sessions / worktrees:** data edits + `data.js` are committed to `master`;
  multiple checkouts commit to `master` at once, so `git fetch` before assuming
  ahead/behind. When a `data.js` conflict appears on rebase, **regenerate it**
  (`python3 backend-data/build.py`) rather than resolving the diff by hand.
- **Bibcode audits:** verify bibcodes via **ADS** (anonymous bootstrap token — see
  `backend-data/system_audit.py`), not arXiv (which rate-limits hard).
