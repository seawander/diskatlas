# Batch H report — comprehensiveness curator (metadata-only expansion)

Date: 2026-07-06. No crops, no merge/build. Files touched:
`backend/seeds/planets2.py`, `backend/seeds/scattered3.py`, `backend/fetch_extra.txt`, this report.
Seed import check: `len(ALL_SYSTEMS) == 96`, image_id collision check vs `data/systems/*.json`: NONE.
All records are `file: null` (pending); a host `fetch_sources.sh` run (gen_fetch_script picks up the
new arXiv ids automatically) + a later crop pass completes them.

## Workstream A — imaged-planet epochs (backend/seeds/planets2.py)

| system | image_id | paper | arxiv | bibcode |
|---|---|---|---|---|
| beta Pic | beta-pic_gravity2020 | GRAVITY Collab. 2020, A&A 633, A110 (beta Pic b K-band interferometry) | 1912.04651 | (not set) |
| beta Pic | beta-pic_gravity2020c | Nowak+2020, A&A 642, L2 (first direct confirmation of RV planet c) | 2010.04442 | (not set) |
| HR 8799 | hr-8799_gravity2019 | GRAVITY Collab. 2019, A&A 623, L11 (e; first exoplanet by optical interferometry) | 1903.11903 | 2019A&A...623L..11G |
| HR 8799 | hr-8799_jwst2025 | Balmer+2025, AJ 169, 209 (NIRCam bar coronagraphy; CO2 in HR 8799 + 51 Eri) | 2503.13608 | 2025AJ....169..209B |
| PDS 70 | pds-70_jwst2024 | Christiaens+2024, A&A 685, L1 (MINDS NIRCam; spiral stream + candidate d) | 2403.04855 | (not set) |
| 51 Eri | 51-eri_jwst2025 | Balmer+2025, AJ 169, 209 (same paper as hr-8799_jwst2025) | 2503.13608 | 2025AJ....169..209B |
| GJ 504 | gj-504_sphere2018 | Bonnefoy+2018, A&A 618, A63 (GJ 504 system revisited; SPHERE re-detections) | 1807.00657 | 2018A&A...618A..63B |
| kappa And | kappa-and_scexao2018 | Currie+2018, AJ 156, 291 (SCExAO/CHARIS JHK IFS of b) | 1810.09457 | (not set) |
| HD 95086 | hd-95086_naco2013b | Rameau+2013, ApJL 779, L26 (confirmation of b) | 1310.7483 | 2013ApJ...779L..26R |
| 1RXS J1609 | 1rxs-j1609_gemini2010 | Lafreniere+2010, ApJ 719, 497 (CPM confirmation; HAS figure) | 1006.3070 | 2010ApJ...719..497L |

Skipped deliberately (brief: "skip if unsure"): **GQ Lup** and **HIP 99770** later-epoch papers —
no single canonical confirmation-imaging paper verified within budget.
Note: the JWST "HR 8799 imaging paper" search converged on Balmer+2025 (NIRCam, first detection of
e at 4.6 um), which also covers 51 Eri — one paper, two records. Boccaletti+2024 MIRI (2310.13414)
exists but was not added (budget; NIRCam paper satisfies the brief).

## Workstream B — classic disk images 1984-2003 (backend/seeds/scattered3.py)

| system | image_id | paper | arxiv | bibcode |
|---|---|---|---|---|
| beta Pic | beta-pic_smith1984 | Smith & Terrile 1984, Science 226, 1421 (first circumstellar disk image); Las Campanas 2.5m | — | 1984Sci...226.1421S |
| beta Pic | beta-pic_kalas1995 | Kalas & Jewitt 1995, AJ 110, 794 (R-band coronagraphy, large-scale disk); UH 2.2m | — | 1995AJ....110..794K |
| TW Hya | tw-hya_wfpc2-2000 | Krist+2000, ApJ 538, 793 (WFPC2 face-on disk) | — (none found) | 2000ApJ...538..793K |
| AU Mic | au-mic_kalas2004 | Kalas+2004, Science 303, 1990 (disk discovery); UH 2.2m | astro-ph/0403132 | 2004Sci...303.1990K |
| AU Mic | au-mic_keck2004 | Liu 2004, Science 305, 1442 (Keck AO substructure) | astro-ph/0408164 | 2004Sci...305.1442L |
| HD 141569 | hd-141569_nicmos1999 | Weinberger+1999, ApJL 525, L53 (NICMOS) | astro-ph/9909097 | 1999ApJ...525L..53W |
| AB Aur | ab-aur_stis1999 | Grady+1999, ApJL 523, L151 — **STIS, not NICMOS** (brief corrected) | — (none found) | 1999ApJ...523L.151G |
| HD 100546 | hd-100546_nicmos2001 | Augereau+2001, A&A 365, 78 (NICMOS2; picked over Pantin+2000) | astro-ph/0009496 | 2001A&A...365...78A |
| GG Tau | gg-tau_cfht1996 | Roddier+1996, ApJ 463, 326 (UH AO circumbinary ring) | — | 1996ApJ...463..326R |
| HR 4796A | hr-4796a_keck1998 | Koerner+1998, ApJL 503, L83 (MIRLIN 20.8 um; type=disk_mm; picked over Jayawardhana+1998) | astro-ph/9806268 | (not set) |
| GM Aur | gm-aur_nicmos2003 | Schneider+2003, AJ 125, 1467 (NICMOS) | — (none found) | 2003AJ....125.1467S |

**HD 163296 Grady+2000 STIS: NOT added** — `hd-163296_stis2000` already exists in
`data/systems/hd-163296.json` (file null, `_verify` on paper). Instead its ADS scan
(2000ApJ...544..895G) was added to fetch_extra.txt so the pending record can be completed.

## fetch_extra.txt additions

- Retry comment for the PMC SEEDS PDF (browser download fallback if curl fails again).
- ADS article-scan lines (URL \t dest) for the pre-arXiv papers:
  1984Sci...226.1421S → smith1984_betapic.pdf (Science scan may be copyright-blocked; skip on 403/404),
  1995AJ....110..794K → kalas1995_betapic.pdf, 2000ApJ...538..793K → krist2000_twhya.pdf,
  1999ApJ...523L.151G → grady1999_abaur.pdf, 1996ApJ...463..326R → roddier1996_ggtau.pdf,
  2003AJ....125.1467S → schneider2003_gmaur.pdf, 2000ApJ...544..895G → grady2000_hd163296.pdf.

## Verification status / caveats

WebSearch usage: stream A 9/12, stream B 9/10 (Kalas 1995 / Smith 1984 ids were supplied by the
brief; 51 Eri JWST resolved for free via the Balmer+2025 search).

Verified via search (arXiv abs page or ADS abstract seen directly): all arXiv ids above; bibcodes
set only where an ADS URL displayed them, except two mechanical constructions (see below).

Remaining soft spots (no `_verify` flags set; all arXiv ids are confirmed):
- Journal page numbers "A&A 642, L2" (Nowak+2020) and "A&A 685, L1" (Christiaens+2024): volume/issue
  confirmed via A&A URLs, letter numbers from memory; bibcodes left null so links go via arXiv.
- "ApJL 503, L83" page for Koerner+1998: volume + arXiv id confirmed; L83 from memory; bibcode null.
- 2003AJ....125.1467S and the Grady/Krist/Roddier bibcodes: journal/volume/page confirmed by search;
  bibcode strings are the standard mechanical construction (needed for the ADS fetch URLs).
- GG Tau Roddier+1996 facility set to CFHT (UH AO system); label says UH AO — crop agent should
  confirm from the scanned paper.
- Smith & Terrile 1984 wavelength set to 0.89 um (broadband optical CCD) from memory.
- kappa-and_scexao2018 / hr-8799_jwst2025 / 51-eri_jwst2025 bibcodes derivable
  (2018AJ....156..291C shown only on IOP, not ADS — left null).

## For the orchestrator

1. Host run: `gen_fetch_script.py` (collects the 14 new arXiv ids incl. 5 astro-ph classics) →
   `fetch_sources.sh` (also processes fetch_extra.txt) → `extract_sources.py`.
2. `make_systems.py` (merge-by-name; all 15 touched systems already exist — no new coords needed).
3. Crop pass: best figure candidates — Lafreniere+2010 Fig. 1 (1rxs-j1609_gemini2010),
   Balmer+2025 NIRCam galleries, Christiaens+2024 Fig. 1, GRAVITY papers (use detection/orbit
   figure), classic ADS scans (page-level rasterize via pdf_page).
