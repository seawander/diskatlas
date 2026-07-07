# frontend/

Single-page, zero-dependency, fully offline. Root `index.html` loads:

- `frontend/style.css`
- `frontend/data.js`  — **GENERATED** by `backend/build.py`. Never hand-edit.
- `frontend/app.js`   — all logic (vanilla JS, no build step, no CDN, system fonts).

`data.js` sets `window.ATLAS = { generated, stats, systems:[...] }` (schema = `data/README.md`
with image `file` paths relative to the repo root). Using a `<script>` include instead of
`fetch()` is what makes `file://` (double-click) work — do not "modernize" this into fetch/modules.

## Features & where they live in app.js

| Feature | Functions |
|---|---|
| Equirectangular all-sky canvas, RA increasing leftward, pan/zoom (wheel & drag, 1×–400×) | `SkyView`, `project()`, `unproject()`, `draw()` |
| Markers: SHAPE per category (● proto / ▲ debris / ◆ planet-only / ■ quasar), ★ overlay = imaged-planet host, uniform size (image count sets fill opacity) | `drawMarkers()`, `sysShape()` |
| Views: Sky / Coverage matrix / Tonight (observability + per-target airmass.org chart links, CSV) | `buildTonight()`, `airmassOrgUrl()`, matrix code |
| Facets: band / missing / Facility (`fac_keys`, AAS keywords; VLT⊃VLTI rule) / Instrument (`instr_key`, top-8-by-usage first) | `chipGroup()`, `filterSystems()` |
| Light/dark theme toggle (persisted; canvas re-colors via `refreshCOL()` + `--sky`) | `initTheme()` |
| i18n EN/中文/FR/ES (`i18n.js`, `t()`/`data-i18n`) | `applyStaticI18n()` |
| Citation links arXiv + SciX; notes auto-linkify "Author+Year" → SciX search; `extra_papers` rendered per companion | `linkifyCitations()`, `adsUrl()` |
| SIMBAD link per system; explicit `simbad: null` → coordinate-search fallback | `openDetail()` |
| Galactic plane + ecliptic curves, RA/Dec grid with labels | `galacticPlanePath()`, `eclipticPath()`, `drawGrid()` |
| Hover tooltip, click → detail panel | `hitTest()`, `openDetail()` |
| Detail panel: image viewer + wavelength-sorted slider, prev/next, keyboard arrows, per-image caption + facility/λ chips + citation links (arXiv/ADS) | `renderDetail()`, `renderImage()` |
| Search box (name/alt names, live), filters (category, facility, survey, has-planet, has-image), stats bar | `applyFilters()`, `buildFilterBar()` |
| URL hash deep-links `#s=hd-163296` | `syncHash()` |

## Conventions

- No external network calls anywhere. Placeholder SVG (inline data-URI) for `file: null` images.
- Colors/sizes: CSS vars at top of `style.css`.
- Keep everything ES2018-compatible (runs from file:// in old-ish browsers too).

## Testing

`node backend/test_frontend_logic.js` exercises the pure functions (projection round-trip,
hit-testing, filtering) by loading app.js in a DOM-less shim. Run after any app.js change.
