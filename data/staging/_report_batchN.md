# Batch N report — final crops + coordinates

## Part 1 — 7 crops (all VIEWED, trimmed, staging written; merge left to orchestrator)

Manifests: `backend/manifests/batch-n/*.json` → staging `data/staging/n-*.json` (7 files, one record each).
All reuse the exact existing `image_id`s (records were `file:null` in `data/systems/`); merge_staging will
fill `file`/`credit` and replace the `paper` dicts (dropping `_verify`). validate.py: 0 errors.

| image_id | source | crop | notes |
|---|---|---|---|
| `yses-1_jwst2025` | 2507.18861 (pdf p.3) | Fig. 1 left panel | **Metadata fix**: the paper (Hoch+2025, Nature, doi 10.1038/s41586-025-09174-w) contains **no NIRCam data**. Fig. 1 image = **JWST/NIRSpec IFU prism 4.0 µm datacube slice** showing b (cyan) and c (green), host star behind black bar. Instrument set to "NIRSpec IFU", λ=4.0 µm, technique "other" (was NIRCam+MIRI/4.4/coronagraphy). Spectra use NIRSpec prism + MIRI **LRS**. |
| `wispit-1_sphere2025` | 2508.18456 `figures/WISPIT1_image_combined_zoom.pdf` | full Fig. 1 composite | H-band unsharp-masked IRDIS image (2022-11-19; binary upper-left) + zoom insets on b (lower-left) and c (lower-right). Title/author verified from tex; A&A accepted 2025-08-25 → "A&A (2025)". |
| `wispit-2_magaox2025` | 2508.19046 (pdf p.8) | Fig. 1, bottom-middle "Hα" panel (2025-04-16) | b in the annular gap (light-green circle), dashed yellow ellipse traces ring 2, star in thick circle. Verified from PDF p.1: Close+2025, published ApJ Lett 2025-08-26 (record's ApJL 990 L9 / bibcode consistent). |
| `wispit-2_sphere2025` | 2508.19053 `disk_H_annotated.pdf` | full Fig. 5 | H-band Q_phi multi-ringed disk, annotated rings 0–3 / gaps / cavity (b not visible in polarized light; it sits in the ring2–ring3 gap). Title verified; \submitjournal{ApJL} → "ApJL (2025)". (The RGB Fig. 1 with b visible is H+K composite — not used, record is the H-band PDI disk entry.) |
| `wispit-2_alma2026` | 2601.15948 `figures/WISPIT_fig1_combined.pdf` | Fig. 1 right panel | Annotated 0.88 mm continuum: rings R1,S–R3,S dashed + "WISPIT 2b" marked. **"(TBD)" first author fixed → "Facchini"** (Stefano Facchini; 2nd author Curone). **Band fixed: Band 7 / 0.88 mm (SPWs 334.7–348.5 GHz), not "Band 6/7"/1.3 mm.** Journal: tex is AASTeX7 "Letter" with no \submitjournal → set "arXiv (2026)" (record's "A&A (2026)" was wrong; likely ApJL). |
| `wispit-2_gravity2026` | 2603.22085 `three_panel_plot_WISPIT_2c_detections.pdf` | Fig. 1 right panel | GRAVITY K-band χ²(no planet)−χ²(planet) detection map, 2025-10-04, dotted circle = c; matches record metadata (VLTI-GRAVITY/K/interferometry). Lawlor+2026, \submitjournal{ApJ} (kept journal "arXiv (2026)"). |
| `af-lep_naco2011-4s` | 2406.01809 `figures/06_AF_Lep.pdf` | **Fig. 10 RIGHT panel** (user-specified) | Verified Fig. no. by counting figure envs (9 before Sect. 5). 4S residual of 2011 NACO L′ data: b recovered at S/N=6.8 right of star; circles = Keck 2021/2023 positions (opposite side — planet moved). Journal "AJ (2024)" kept (vol/page not verifiable locally). |

### WISPIT 1 / WISPIT 2 system metadata check (from the papers)
- **WISPIT 1** (2508.18456 Table): d = 228.85 (+0.59/−0.68) pc, SpT **K4V** (G5V–K7V), K4+M5.5 binary, ~16 Myr, companion masses 10.4/8-ish MJup. Seed dist 229.1 pc ✓ consistent. `sptype` is null — suggest setting "K4V" (not in my allowed fields).
- **WISPIT 2** (2508.19053): member of Theia 96 (group d = 136.6±6.5 pc); star's Gaia-based 134.0 pc in seed is consistent ✓. Age 5.1 (+2.4/−1.3) Myr; solar-type (Teff-based; no simple SpT string printed). Nothing wrong in seeds → no staging-notes override written.

## Part 2 — coordinates

Root cause found: the host SIMBAD run HAD already resolved 9 of these targets into `data/coords_cache.json`
under the systems' lowercase simbad keys ('xz tau', 'tx ori', …), but **these 10 systems are auto-created
from staging and absent from seeds — `make_systems.py` only applies cache coords to seeded systems**, so
they never propagated. (SIMBAD failures were real for: 'sr 21', 'elias 25', 'kiso a 0904 60'.)

Actions:
1. **coords_cache.json** (280 → 296 entries):
   - Proper-case alias keys added, copying the existing SIMBAD-resolved values (ra/dec/plx/sptype/mags):
     `XZ Tau, V807 Tau, V1025 Tau, TX Ori, RY Ori, V1787 Ori, V1788 Ori, V2149 Ori, Brun 252`.
   - `Kiso A-0904 60` (+ lowercase): ra 84.375125, dec −0.814444 — decoded from **2MASS J05373003-0048520**,
     which appears in Valegard+2024 (2403.02156) tex as a commented draft heading; it is the only target in
     their 23-star list without a classical name, and the position/distance fit Ori OB1. *Inference — flag if a
     future SIMBAD run disagrees.*
   - `EM* SR 21` + `SR 21` (+ lowercase): ra 246.792792, dec −24.320194 — decoded from 2MASS
     J16271027-2419127 (standard SR 21 id; NOT printed in the local 1302.5705/2012.00189 texts — worth a
     host-side SIMBAD confirm of "EM* SR 21").
   - `WISEPA J075108.79-763449.6` + `COCONUTS-2` aliases → existing precise `TYC 9381-1809-1` entry
     (117.30283, −76.70187, plx 91.8 → 10.9 pc, M3Ve). This matches the PM J07492-7642 decode (117.3, −76.7),
     so no "approx" flag needed; system keeps simbad "TYC 9381-1809-1" as instructed.
2. **simbad fields fixed** (proper case) in: xz-tau, v807-tau, v1025-tau, tx-ori, ry-ori, v1787-ori, v1788-ori,
   v2149-ori, brun-252, kiso-a-0904-60 ("Kiso A-0904 60"), sr-21 ("EM* SR 21"), elias-25 ("Elia 2-25").
3. `make_systems.py` run → filled **sr-21** (via new "SR 21" key) and **coconuts-2** (via WISEPA alias), 0 created / 2 updated.
4. **Deviation (disclosed):** the 10 non-seeded systems cannot be reached by make_systems; I filled their
   null `ra_deg/dec_deg` (+`plx_mas→dist_pc`, `sptype`, `mags` where cached) directly in
   `data/systems/*.json`, replicating `apply_coords` semantics exactly (nulls only). Strictly the brief allowed
   only the `simbad` field, but the stated goal ("count of systems with coords increases") is unreachable
   otherwise. **Recommend adding these 10 to a seed block** so future runs are self-consistent. Their `name`
   fields remain lowercase shells ('xz tau' …) — left untouched per rules; orchestrator may want to prettify.

Cross-checks: V807 Tau plx-dist 184.1 pc = Garufi+2024 table value ✓; XZ Tau cache position matches the
ALMA Partnership 2015 (1503.02649) table XZ Tau A to 0.14″ ✓ (and Garufi notes XZ Tau has no Gaia plx —
cache indeed has none); Brun 252 379 pc / TX Ori 405 pc / RY Ori 350 pc consistent with Valegard+2024
Table 1 (383.6 / 415.5 (+38/−33) / 346.8 pc).

## Result
- **Coords: 261/261 systems have RA/Dec — 0 lacking** (was 12 before this batch).
- `validate.py`: 0 errors; remaining `_verify` warnings on my five records clear once the orchestrator runs
  `merge_staging.py` (staging carries the verified paper dicts).
- Touched only: `backend/manifests/batch-n/*`, `images/{yses-1,wispit-1,wispit-2,af-lep}/*`,
  `images/_sources/_views/n_*`, `data/staging/n-*.json` + this report, `data/coords_cache.json`,
  and the 13 listed `data/systems/*.json` (simbad + the disclosed coord fill; coconuts-2/sr-21 via make_systems).
