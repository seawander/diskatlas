# backend/ — scripts (pure Python 3, stdlib + Pillow only)

No server. The "backend" is a build pipeline: seeds → systems JSON → cropped images → `frontend/data.js`.

## Scripts

| Script | Purpose |
|---|---|
| `seeds/` | Master target lists + paper metadata per survey (Python dicts). Edit to add batches. |
| `make_systems.py` | seeds + `data/coords_cache.json` → `data/systems/*.json` (non-destructive merge: hand edits in systems files win unless `--force-seed`). `--missing-coords` prints names lacking coordinates + a ready-to-run SIMBAD script. |
| `gen_fetch_script.py` | Collects every arXiv id referenced by seeds/systems → writes `fetch_sources.sh` (run OUTSIDE the sandbox) + `simbad_script.txt`. |
| `crop_panels.py` | `python3 crop_panels.py manifests/<m>.json` — cuts survey figures into per-target panels, downsizes to ≤640 px, writes `images/<id>/<image_id>.png`. |
| `merge_staging.py` | Folds `data/staging/*.json` image records into `data/systems/*.json`. |
| `validate.py` | Schema check, id/file consistency, duplicate detection, link fields, image sizes. |
| `build.py` | Validates then emits `frontend/data.js` + prints coverage stats. Enriches every image record with `fac_keys` (AAS facility keywords) + `instr_key` (instrument family) via `facility_map.py`. |
| `facility_map.py` | Free-text facility/instrument → canonical facet keys (AAS keyword table + heuristics). Extend `FAC_TABLE`/`INSTR_RULES` when new strings appear. |

Typical full run: `make_systems.py` → `crop_panels.py …` → `merge_staging.py` → `build.py`.

## Network reality (IMPORTANT for agents)

The usual DGX checkout (`/home/brinen2spark/Developments/diskatlas`) **has live internet
from bash** — arxiv.org, SIMBAD, aanda.org are directly reachable:

```bash
cd backend && bash fetch_sources.sh      # → images/_sources/arxiv/<id>.tar + SIMBAD results
```

Two rate-limit lessons (2026-07-07): `export.arxiv.org`'s API 429s hard when many parallel
agents share the IP — fall back to `arxiv.org/abs/<id>` meta tags / `arxiv.org/pdf/<id>` /
Semantic Scholar; and parallel curl PDF downloads get silently truncated — verify with
`pdfinfo`, re-fetch sequentially on failure. (If ever run in a network-isolated sandbox,
run `fetch_sources.sh` on a networked host instead; everything else is identical.)

`fetch_sources.sh` is idempotent (skips files already present).

## SIMBAD coordinates

`gen_fetch_script.py` also writes `simbad_script.txt`. On the host:

```bash
curl -s "https://simbad.cds.unistra.fr/simbad/sim-script" \
     --data-urlencode "script@simbad_script.txt" > ../data/simbad_raw.txt
python3 parse_simbad.py        # → merges into data/coords_cache.json
```

(This is already inside `fetch_sources.sh`.) For a handful of objects you can instead paste
coordinates by hand into `data/coords_cache.json`:
`{"HL Tau": {"ra": 67.9102, "dec": 18.2326, "plx_mas": 6.8, "sptype": "K5"}}`.

## Extracting figures from arXiv source tarballs

```bash
python3 extract_sources.py            # unpacks images/_sources/arxiv/*.tar → _sources/extracted/<id>/
```

Handles: tar.gz of TeX+figures (typical), single gzipped TeX, raw PDF (`%PDF` magic → saved as <id>.pdf).
PDF figures → PNG via `pdftoppm -png -r 200`. EPS → `convert`. Then crop with a manifest.

## Crop manifests (`manifests/*.json`)

```jsonc
{
  "survey": "dsharp",
  "source_image": "images/_sources/extracted/1812.04040/figures/gallery.png",
  "pdf_page": null,            // if source is a PDF: 1-based page to rasterize first
  "grid": {                    // EITHER a regular grid...
    "rows": 4, "cols": 5,
    "order": ["ht-lup","gw-lup", "...20 ids row-major; null = skip cell"],
    "trim_frac": [0.0, 0.0, 0.0, 0.0]      // optional [left,top,right,bottom] pre-trim of the full image
  },
  "panels": [                  // ...OR explicit fractional boxes (overrides grid)
    { "id": "as-209", "image_id": "as-209_dsharp", "bbox_frac": [0.61, 0.52, 0.79, 0.75] }
  ],
  "image_defaults": { "type": "disk_mm", "facility": "ALMA", "...": "merged into every record" },
  "paper": { "first_author": "Andrews", "year": 2018, "arxiv": "1812.04040", "...": "..." }
}
```

`crop_panels.py` writes PNGs **and** a staging file `data/staging/<survey>.json` with one
image record per panel (schema = `images[]` element + `"system_id"` field).

**Workflow discipline for agents:** after cropping, VIEW a few output PNGs (Read tool) to
verify panel↔target assignment (off-by-one errors are the classic failure). Panel labels
are usually printed inside the panels — check them against the manifest order. Fix bboxes,
re-run, only then `merge_staging.py`.

## Adding a brand-new survey (agent checklist)

1. Read the paper (ar5iv/arxiv-html via web_fetch) → target list, figure numbers, band, survey name.
2. Append a block to `seeds/<appropriate file>.py` (follow existing patterns; simbad names!).
3. `make_systems.py` → `--missing-coords` → host SIMBAD run if needed.
4. Add arXiv id to fetch list → host `fetch_sources.sh` run → `extract_sources.py`.
5. Locate the gallery figure file, write a manifest, `crop_panels.py`, VIEW, iterate.
6. `merge_staging.py` → `validate.py` → `build.py` → update `data/ingestion_status.json`.

## Paper discovery

Literature snowballing lives in the project Skill
`.claude/skills/diskatlas-paper-finder/` (see `HANDOFF.md` → "The paper-finder Skill");
its `scripts/find_papers.py` writes candidates + citation cache under `data/paper_finder/`
and per-paper dispositions to `data/paper_finder_state.json`.
