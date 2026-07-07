# Batch S report — finale crops (PDS 70 Keck, Keck-vortex-2024, 3C 273, eprint singles, quasar expansion)

Date: 2026-07-06. All work per AGENT_BRIEFS concurrency protocol: crops + staging
+ my seed stub + this report only. NO merge/validate/build was run (orchestrator's job).

## Deliverables

| Job | image_id(s) | file | staging |
|---|---|---|---|
| 1 PDS 70 Wang+2020 | `pds-70_keck2020` | 558x249, 182 KB | `s-pds70-keck2020.json` |
| 2 Keck vortex Fig. 4 | 8x `<sid>_keck-vortex-2024` | ~540x540, 132-226 KB | `s-keck-vortex-2024.json` |
| 3 3C 273 Ren+2024 | `3c-273_stis2024` | 560x560, 276 KB | `s-3c273-stis2024.json` |
| 4 quasar expansion | 5 pending records (no crops, per brief) | file:null | `s-quasar-expansion.json` + 3 NEW system files |
| 5 HD 32297 Schneider+2005 | `hd-32297_stis2005` | 559x552, 244 KB | `s-hd32297-stis2005.json` |
| 6 HD 100546 Walsh+2014 | `hd-100546_alma2014` | 496x558, 221 KB | `s-hd100546-alma2014.json` |

Every crop was VIEWED and its in-panel label checked; all trimmed with
`trim_borders.py`; PNGs >300 KB were palette-quantized (median-cut 256 + dither,
re-viewed: no visible banding). Manifests in `backend/manifests/batch-s/`
(manifest "survey" = staging filename `s-*`; record survey via `survey_name`).

## Job 1 — pds-70_keck2020 (Wang+2020 Keck/NIRC2 L')

- Source `images/_sources/extracted/2004.09597/lp_pds70_image.pdf` = Fig. 1 (verified in
  pds70_clean.tex, label `fig:image`). Cropped the user-specified pair: LEFT (PSF-subtracted)
  + MIDDLE (disk-subtracted) panels together; b & c arrows visible in both.
- Metadata verified: title from the .tex ("Keck/NIRC2 L'-Band Imaging of Jovian-Mass
  Accreting Protoplanets around PDS 70"); journal AJ 159, 263 confirmed from the
  references.bib of 2408.04048 (eprint field matches 2004.09597). `_verify` cleared,
  bibcode 2020AJ....159..263W added. Staging overwrites the stub record (same image_id).

## Job 2 — Keck-vortex-2024 (Wallack+2024, 2408.04048)

- Paper verified: **Wallack** et al. 2024, "A Survey of Protoplanetary Disks Using the
  Keck/NIRC2 Vortex Coronagraph", **AJ 168, 78** (main.tex title/shortauthors + web search:
  DOI 10.3847/1538-3881/ad390c, bibcode 2024AJ....168...78W). Seed stub in
  `backend/seeds/scattered3.py` fixed (paper + 8 members; `_verify` removed).
- Fig. 4 = `disks.pdf`, 2x4 grid, panel labels (ground truth, row-major):
  2MJ1604 (RDI), LkHa 330 (RDI), LkCa15 (RDI), MWC758 (RDI) / PDS 70 (RDI), RY Tau (RDI),
  HD 34282 (RDI), CQ Tau (ADI). One crop per disk, image_id `<sysid>_keck-vortex-2024`,
  survey "Keck-vortex-2024" (staging file `s-keck-vortex-2024.json`).
- **All 8 systems already exist** (2MJ1604 = `rx-j1604-3-2130`, simbad
  2MASS J16042165-2130284) -> no new systems, nothing for coords_todo from this job.
- Technique RDI by default; CQ Tau record set to ADI in staging (matches its panel label).
  L' 3.8 um; ALMA contours are overlaid in every panel (noted in wavelength_label).

## Job 3 — 3c-273_stis2024 (Ren+2024)

- Fig. 1 = `fig-3C273.pdf` (single panel + colorbar): host galaxy 60"->0.2" with the
  optical jet to the SW. Cropped the sky map (axes/colorbar excluded; 10 kpc bar +
  compass kept). 276 KB after quantization.
- Metadata verified: title from ms.tex; journal **A&A 683, L5** via web search
  (ADS bibcode 2024A&A...683L...5R). Staging replaces journal "(verify)" and clears `_verify`.

## Job 4 — quasar expansion (intro 1st paragraph of 2402.09505)

Citations in the first Introduction paragraph for prior high-contrast/host imaging of
quasars/AGN (`\citep[e.g.,][]{martel03, gratadour15, metis, moustakas19, Rouan19,
Grosset21, Ding2023}` + context cites), target + paper pairs:

| cite key | target | paper |
|---|---|---|
| martel03 | **3C 273** | Martel et al. 2003, AJ 125, 2964 — HST/ACS coronagraphy; host outside ~1.5" (context corroborated in Sec. 1-2 of ms.tex) |
| gratadour15 | **NGC 1068** | Gratadour et al. 2015, A&A 581, L8 — SPHERE H+Ks polarimetry; extended nuclear torus |
| Rouan19 | **NGC 1068** | Rouan et al. 2019, A&A 625, A100 — SPHERE; stellar cusp + warm dust at the torus wall |
| Grosset21 | **NGC 1068** | Grosset et al. 2021, A&A 648, A42 (arXiv 2102.06339) — SPHERE polarimetric imaging of the nucleus |
| Ding2023 | **HSC J2236+0032, HSC J2255+0251** | Ding et al. 2023, Nature 621, 51 (arXiv 2211.14329) — JWST/NIRCam starlight of z>6 quasar hosts |
| metis | (none — Brandl et al. 2008, Proc. SPIE 7014: ELT/METIS instrument concept; not an imaging result) |
| moustakas19 | (none — Moustakas et al. 2019, BAAS 51, 487: Astro2020 white paper) |
| ford94 (context) | M87 | Ford et al. 1994, ApJL 435, L27 — HST narrowband imaging of the ionized nuclear gas disk (not quasar-host coronagraphy; listed for completeness, not added) |
| ford14 (context) | (none — Ford et al. 2014, ApJ 783, 73: JWST aperture-masking AGN forecast) |

Concrete prior imaging results ingested (4, per budget; all pending file:null, no crops):
- **NEW** `data/systems/ngc-1068.json` — categories ["quasar"], sptype "Sy2 (z=0.0038)",
  3 pending type-"quasar" images (sphere2015 / sphere2019 / sphere2021, papers above).
  Gratadour+2015 and Rouan+2019 have **no arXiv posting found** (searched); records use
  bibcodes (ADS links work per data/README link rules).
- **NEW** `data/systems/hsc-j2236-0032.json` — "QSO (z=6.40)", pending `_jwst2023` (Ding+2023).
- **NEW** `data/systems/hsc-j2255-0251.json` — "QSO (z=6.34)", pending `_jwst2023` (Ding+2023).
- 3C 273 already exists -> Martel+2003 entered as pending image record
  `3c-273_acs2003` via `data/staging/s-quasar-expansion.json` (new image_id, file:null).

Coordinates: NGC 1068 literature position; HSC quasars derived from their IAU
designations (J223644.58+003256.9 / J225538.04+025126.6). SIMBAD names appended to
`data/coords_todo_batchS.txt` (3 entries) for the host pass (plx/mags refinement).

## Job 5 — hd-32297_stis2005 (Schneider+2005 NICMOS discovery)

- `images/_sources/extra/schneider2005_hd32297.pdf` p.11 = Fig. 1 (a-d). Cropped
  **panel b** (log-stretch colour display: edge-on disk wings, 2" bar, occulted hole).
- PDF is arXiv **astro-ph/0507355** (title page) -> arxiv id added to the record
  (title/journal ApJL 629, L117/bibcode already correct in the seed record).
- Note: image_id keeps the historical (misnamed) `_stis2005` stem per "reuse exact
  image_ids"; instrument metadata says NICMOS correctly.

## Job 6 — hd-100546_alma2014 (Walsh+2014 ApJL)

- **Seeded title was wrong** ("ALMA Reveals the Anatomy of the mm-sized Dust..." does not
  exist). Real paper from the PDF: "ALMA Hints at the Presence of Two Companions in the
  Disk around HD 100546", arXiv **1405.6542**, ApJL 791, L6 (existing bibcode
  2014ApJ...791L...6W consistent). Fixed via staging.
- The paper has NO standalone continuum-image figure (checked all 5 figures): the 870 um
  continuum appears as black contours over the CO J=3-2 first-moment map in **Fig. 1**
  (p.17) -> cropped that map panel; wavelength_label now says
  "870 um continuum (black contours) over the CO J=3-2 velocity map".

## Files touched (mine only)

- `backend/manifests/batch-s/` (5 manifests)
- `backend/seeds/scattered3.py` (Keck-vortex-2024 stub only)
- `images/{pds-70,rx-j1604-3-2130,lkha-330,lkca-15,mwc-758,ry-tau,hd-34282,cq-tau,3c-273,hd-32297,hd-100546}/*` (12 new PNGs)
- `images/_sources/_views/s_*.png` (working views)
- `data/staging/s-*.json` (6 files) + this report
- `data/coords_todo_batchS.txt`
- NEW `data/systems/{ngc-1068,hsc-j2236-0032,hsc-j2255-0251}.json` (job 4 only)

## Notes for the orchestrator

- Merging `s-*.json` will overwrite the 4 pre-existing stub records (same image_id;
  staging wins for non-null fields) and drop their `_verify` flags as intended.
- Bibcodes 2020AJ....159..263W / 2024AJ....168...78W constructed from verified
  journal refs (standard format); Martel+2003 bibcode 2003AJ....125.2964M is from
  Ren+2024's own .bbl, its title from memory corroborated by the ms.tex description
  (HST/ACS coronagraphy of 3C 273) — spot-check welcome.
- WebSearch budget: 6/6 used (Wallack journal; Ren journal; Gratadour15; Rouan19;
  Ding2023 targets; combined arXiv-id sweep for the two A&A NGC 1068 papers -> none exist).
- After the host SIMBAD pass, ngc-1068 / hsc-j2236-0032 / hsc-j2255-0251 will pick up
  plx/mags; their RA/Dec are already valid for the sky map.
