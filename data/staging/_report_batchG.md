# Batch G report — final-g crops + planets.py metadata

Date: 2026-07-06. Scope per brief: TWA 7 trio, TWA 7 b, 14 Her c, YSES-2 b,
HD 135344 Ab, HD 110058, eta Crv, HD 95086, V1247 Ori, AF Lep metadata, exoALMA I check.

## Crops produced (10, all VIEWed, all trimmed via trim_borders.py)

| staging file (data/staging/) | image_id | source | panel | px / KB |
|---|---|---|---|---|
| g-twa7-nicmos2021.json | twa-7_nicmos2021 (NEW) | 2105.09949 fig1.pdf | (a) | 560x551 / 217 |
| g-twa7-sphere2021.json | twa-7_sphere2021 (NEW) | 2105.09949 fig1.pdf | (b) | 560x547 / 236 |
| g-twa7-stis2021.json | twa-7_stis2021 | 2105.09949 fig1.pdf | (c) | 560x559 / 206 |
| g-14her-jwst2025.json | 14-her_jwst2025 | 2506.09201 Fig. 1 | middle (F444W, "c" arrow incl.) | 560x553 / 143 |
| g-yses2-sphere2021.json | yses-2_sphere2021 | 2104.08285 Fig. 2 | left (SPHERE/H 2018-04-30, arrow) | 558x558 / 292 |
| g-hd135344a-sphere2025.json | hd-135344-a_sphere2025 | 2507.06206 Fig. 1 | row2-col1 (IRDIS H2, 2021-07-16) | 410x407 / 41 |
| g-hd110058-sphere2023.json | hd-110058_sphere2023 | 2308.05613 Fig. 2 | right (IRDIS/H23) | 559x560 / 241 |
| g-etacrv-alma2017.json | eta-crv_alma2017 | 1611.01168 Fig. 1 | full map | 558x560 / 208 |
| g-hd95086-alma2017.json | hd-95086_alma2017 | 1709.10129 Fig. 1 | (c) "Combined" | 410x410 / 55 |
| g-v1247ori-alma2017.json | v1247-ori_alma2017 | 1710.05028 Fig. 1 | left (labeled ALMA 870um) | 461x462 / 228 |

Manifests: backend/manifests/final-g/g-*.json (10). twa-7_sphere2021 + twa-7_stis2021
were PNG-quantized (256 colors, FS dither) to get under ~300 KB; visually checked.
V1247 fig1a.eps converted with gs -> images/_sources/_views/g_v1247_fig1a.png (manifest source).

## Ground-truth corrections baked into the staging records
- **eta Crv**: figure caption says "0.88 mm (Band 7)" — old record said Band 6 / 1.3 mm.
  Staging sets instrument "Band 7", wavelength_um 880, label "0.88 mm continuum ring";
  full title restored ("...by a chain of 3-30 M_Earth planets?"), bibcode kept.
- **HD 95086 (Su+2017)**: title verified from hd95.tex; journal fixed "ApJ (2017)" ->
  "AJ 154, 225", bibcode 2017AJ....154..225S added.
- **V1247 Ori (Kraus+2017)**: title verified from v1247ori.tex; bibcode
  2017ApJ...848L..11K added; merge will drop the old `_verify` (staging paper replaces it).
- **YSES-2 (Bohn+2021)**: title verified from tex; staging paper carries bibcode
  2021A&A...648A..73B and clears `_verify` in the systems file on merge.
  (seeds/planets.py YSES-2 entry already had bibcode + no verify — nothing to change there.)
- **HD 110058**: cropped image is the RDI-PCA H23 reduction (Fig. 2), so technique
  ADI -> RDI, label "H band (H23); warped edge-on disk (RDI-PCA)". Kept the existing
  published title incl. "and HST/STIS" (arXiv tex title is the shorter pre-referee one).
- **TWA 7 NICMOS**: brief said 1.1 um, but Fig. 1a is **F160W (1998)** per caption ->
  wavelength_um 1.6, technique RDI (archival re-reduction). Existing twa-7_alice
  (Choquet+2016, file null) left untouched — distinct record.
- **TWA 7 SPHERE**: credit reads "SPHERE data from Olofsson+2018, figure from
  Ren+2021 (Fig. 1b crop)" as instructed; technique PDI (Q_phi).

## planets.py (seeds) edits — MY file per brief
1. **TWA 7 b / twa-7_jwst2025**: the DB arXiv id **2506.21857 was WRONG** — that tarball
   contains an unrelated pathology/ML manuscript (elsarticle, TCGA-CRC figures; checked
   00README.json + main.tex). WebSearch: real id is **2502.15081**, Nature 642, 905 (2025),
   bibcode 2025Natur.642..905L. planets.py fixed (id/journal/bibcode, verify flag removed).
   **No crop possible** — 2502.15081 is not in _sources; twa-7_jwst2025 stays file:null.
   ACTION for orchestrator: add 2502.15081 to the fetch list; systems/twa-7.json still
   carries the wrong id until make_systems/manual sync (I don't edit systems files).
2. **HD 135344 Ab**: 2507.06206.tar was present but unextracted — extracted it to
   images/_sources/extracted/2507.06206/ myself. From aa55064-25.tex: **Stolker et al. 2025,
   "Direct imaging discovery of a young giant planet orbiting on Solar System scales"**,
   A&A. planets.py "(TBD)"+verify fixed; same paper dict in the staging record clears
   `_verify` in the systems file on merge.
3. **AF Lep — 4 new file-pending records** added under the existing system:
   - af-lep_sphere2023-mesa: Mesa+2023, "AF Lep b: The lowest-mass planet detected by
     coupling astrometric and direct imaging data", A&A 672, A93, 2302.06213.
   - af-lep_sphere2023-derosa: De Rosa+2023, "Direct imaging discovery of a super-Jovian
     around the young Sun-like star AF Leporis", A&A 672, A94, **2302.06332**.
     **NOTE: brief asked for id af-lep_gpi2023-derosa, but De Rosa+2023 used VLT/SPHERE
     (star-hopping RDI), not GPI** — verified from the arXiv abstract ("We used the SPHERE
     instrument on the VLT... observations of a nearby star interleaved..."). Named the
     record af-lep_sphere2023-derosa to keep facility/id consistent.
   - af-lep_gravity2024: Balmer+2024, "VLTI/GRAVITY Observations of AF Lep b: Preference
     for Circular Orbits, Cloudy Atmospheres, and a Moderately Enhanced Metallicity",
     2411.05917, wl 2.2, technique interferometry, journal "AJ (2025)" (bibcode unconfirmed -> null).
   - af-lep_jwst2024: Franson+2024, "JWST/NIRCam 4-5 um Imaging of the Giant Planet
     AF Lep b", ApJL 974, L11, 2406.09528, bibcode 2024ApJ...974L..11F, wl 4.4 F444W.
   - AF Lep notes updated (three 2023 groups; af-lep_sphere2023 = Keck image, historical id).
   - Tarballs 2411.05917 / 2406.09528 absent as the brief said -> no crops (file pending).
4. 14 Her c: title verified from main_14Her_accepted_arxiv.tex — matches seeds; no edit.

## Item 11 — exoALMA I
images/_sources/extracted/2504.18688 does NOT exist (no tar in _sources/arxiv either).
Skipped; backend/seeds/alma_proto.py untouched; P_EXOALMA1 verify flag still open.

## Budget / protocol
- WebSearch 4/4: TWA7b id, 2411.05917, 2406.09528, Mesa/De Rosa. Plus one arxiv-abs
  web_fetch (2302.06332) to settle the De Rosa instrument (SPHERE, not GPI).
- Touched only: backend/manifests/final-g/*, backend/seeds/planets.py, images/<sysid>/*,
  images/_sources/_views/g_*.png, images/_sources/extracted/2507.06206/ (extraction),
  data/staging/g-*.json + this report, data/coords_todo_batchG.txt.
- No merge/build run. No new systems (coords_todo_batchG.txt is a no-op comment).
