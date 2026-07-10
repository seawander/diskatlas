# Crop-agent briefs (for AI agents doing image ingestion)

## Concurrency protocol (when several agents run in parallel)
- You ONLY: crop images (`crop_panels.py`), write `data/staging/<survey>.json`,
  edit YOUR batch's seed file, and write `data/staging/_report_<batch>.md`.
- Do NOT run `merge_staging.py` / `build.py`; do NOT edit `data/systems/*.json`,
  `data/ingestion_status.json`, or other batches' files. The orchestrator merges.
- New systems discovered from panel labels: append their SIMBAD-resolvable names
  (one per line, `# comment` allowed) to `data/coords_todo_<batch>.txt`, and list
  them with region/category in your report.
- Repo path: the orchestrator substitutes the clone's ABSOLUTE path into every
  agent prompt (file tools + bash share it). Rasterize figures into
  `images/_sources/_views/` and Read them; clean that dir when done.
- MODERN METHOD: this manual protocol is automated by the **Workflow tool** — one
  crop-agent per source figure that renders → VIEWs → crops → self-verifies → returns a
  structured record; the orchestrator collects the ok crops, writes one staging file,
  and merges. See HANDOFF.md "Ingesting via the Workflow tool" for the pattern + gotchas
  (hardcode paths — `args` doesn't propagate; reconcile crops against the PNGs on disk).

General rules for every batch:
1. Sources live in `images/_sources/extracted/<arxivid>/`. Find the gallery figure
   file(s) (often `f3.pdf`, `fig_gallery.png`, per-target `*.pdf` ...). If figures are
   inside a full-paper PDF, use `pdf_page` in the manifest to rasterize the right page.
2. Identify the panel layout & panel labels BY LOOKING at the rasterized image
   (Read tool on a PNG). Panel labels in the figure are the ground truth for target
   names — never guess from memory.
3. Write `backend/manifests/<survey>.json` (schema in backend/README.md), run
   `python3 backend/crop_panels.py manifests/<survey>.json`, then VIEW at least
   3 random outputs to confirm label↔file match. Iterate until clean.
4. If a target is new (not in `data/systems/`), staging will auto-create it —
   afterwards add its `simbad` name to the follow-up coordinate list and note it
   in `data/ingestion_status.json`.
5. `python3 backend/merge_staging.py && python3 backend/validate.py && python3 backend/build.py`.
6. Update `data/ingestion_status.json` (images: done/partial + notes).
7. If paper metadata in seeds carries `_verify`, confirm title/journal/arXiv id
   from the actual source (its .tex or first PDF page) and fix `data/systems/*.json`.

## Batch A — ALMA protoplanetary
- 1812.04040 DSHARP: 20-panel continuum gallery (Andrews+2018 Fig. 3?). image_id `<id>_dsharp`.
- 1810.06044 Long+2018: 12-disk gallery. `<id>_taurus-long2018`.
- 1906.10809 Long+2019: full-sample mosaic incl. compact disks -> ADD missing systems. `<id>_taurus-long2019`.
- 2504.18725 exoALMA IV: 15-disk continuum gallery. `<id>_exoalma`.
- Singles: 1503.02649 (HL Tau), 1603.09352 (TW Hya), 2108.07123 (PDS 70),
  2012.00189 (ODISEA top-10; add systems), plus any single-target figures listed
  in systems JSONs with matching arXiv ids.

## Batch B — ALMA/mm debris
- 2501.09058 REASONS: gallery of 74 belts (appendix figs, multi-page). Panel labels
  -> complete membership (add ~54 new systems). image_id `<id>_reasons`.
- 2601.11708 ARKS I: 24-belt overview gallery. `<id>_arks`.
- Singles: Fomalhaut (1705.05867 + JWST 2305.03789), AU Mic (1211.5148),
  beta Pic (bibcode-only Dent+2014 — SKIP crop if no source), HR 8799 (1603.04853),
  Vega JWST (2410.23636), eta Crv (1611.02196), HD 107146 (1410.8265), HD 95086 (1703.10893).

## Batch C — scattered light
- 2004.13722 Esposito+2020 GPIES: per-target Qphi galleries; 26 debris + 3 PPD.
  Complete membership. `<id>_gpies-debris`.
- 2206.05815 Rich+2022 Gemini-LIGHTS: gallery; detections only. `<id>_gemini-lights`.
- 1803.10882 DARTTS-S: 8 disks. `<id>_dartts-s`.
- 2403.02158 Garufi+2024 SPHERE Taurus census: detections only; add systems. `<id>_sphere-taurus`.
- 1406.7303 Schneider+2014 STIS: 10 disks. `<id>_stis-schneider14`.
- Singles per systems JSONs (HR 4796A trio, TW Hya SPHERE/STIS, AB Aur, MWC 758,
  Fomalhaut ACS, AU Mic ACS/SPHERE, HD 141569, HD 34700, GG Tau, SU Aur, ...).

## Batch D — imaged planets
Discovery figures are small single panels; crop generously (planet + star + scale).
- 0811.2606 & 1011.4918 (HR 8799), 1006.3314 (beta Pic b), 1806.11568 + 1906.01486
  (PDS 70 b,c), 1508.03084 (51 Eri b), 1707.01413 + 2208.14990 (HIP 65426 b),
  astro-ph/0409323 (2M1207 b), 2302.05420 (AF Lep b), 2212.00034 (HIP 99770 b),
  2007.10991 (YSES-1 bc), 2103.05657 (YSES-2 b), 1305.7428 (HD 95086 b),
  1307.2886 (GJ 504 b), 1211.3744 (kappa And b), 1312.1265 (HD 106906 b),
  0811.1994 (Fomalhaut b), 2407.15453 (eps Ind Ab), 2506.21857 (TWA 7 b),
  2204.00633 (AB Aur b), older NACO/Subaru singles per systems JSONs.
- 14 Her c: identify the 2025 JWST paper (WebSearch), fix the placeholder record.

## 2026-07-07 additions

- **Panel-only crops**: trim axes, tick labels, and white margins — deliver just the image
  panel (attached colorbars may stay). Reason: the atlas UI shows crops edge-to-edge and
  external axis text reads as "white edges".
- **Crop QA rules (2026-07-07, after the HD 145718 mosaic-offset bug):**
  (1) the four cropped edges should each be near-uniform in color — heterogeneous edges
  mean the crop cuts through content or a neighboring panel; (2) OCR the crop (tesseract
  is installed): a target-name label at the CENTER means the grid was offset (labels
  belong near a corner), and axis numbers/units near the edges mean the trim failed;
  (3) uniform resolution: cap the longest side at **480 px** (≈150 dpi for a typical
  published panel) — render figures at 250–300 dpi for the cut, then downscale.
- **Record format**: staging records now may carry `fac_keys`/`instr_key`-friendly
  free text — use facility names that `backend/facility_map.py` already knows (check its
  `FAC_TABLE`) or extend the table in the same change.
- **Fleet reliability**: verify ids via `arxiv.org/abs/<id>` meta tags when the export API
  429s; check PDFs with `pdfinfo` (parallel downloads truncate); if you are an orchestrator,
  reconcile agent output against the PNGs on disk, and resume agents that stopped after
  delegating to their own background children ("do it yourself synchronously").
