# Batch I report — NACO/PIPPIN gallery, SEEDS Fig. 3, beta Pic & GG Tau classics, HD 135344 Ab GRAVITY

Date: 2026-07-06. All work within batch-I lanes: `backend/manifests/batch-i/*`,
`backend/seeds/scattered.py` (NACO-PIPPIN + SEEDS blocks only), `backend/seeds/scattered3.py`
(GG Tau comment only), `images/<sysid>/*`, `images/_sources/_views/*`, `data/staging/*`,
`data/coords_todo_batchI.txt`. No merge/build run.

## 1. NACO/PIPPIN (de Regt+2024, A&A 684, A73; 2404.02222) — DONE (14 crops)

Source `plots/figure_gallery.pdf` (= published Fig. 6; \label{fig:gallery}), rasterized at
200 dpi, panel boxes auto-detected. 22 detections in the figure; cropped the **14 clean disk
panels** (rows 1-3): HD 135344B, HD 169142, HD 163296, HD 97048, HR 4796, TW Hya,
HD 100546, HD 142527, Sz 91, CR Cha, MP Mus, AK Sco, Elia 2-25, SU Aur.
**Skipped 8 panels** that are envelopes/outflow nebulae, not disks (paper text concurs):
R CrA, Z CMa, Elia 2-29, Parsamian 21, R Mon (NGC 2261), YLW 16A, Elia 2-21, Mon R2 IRS 3.

- image_id `<sysid>_naco-pippin`, survey "NACO-PIPPIN"; staging `data/staging/naco-pippin.json`.
- Bands per the Fig. 6 caption: Ks (2.18 um) default; **HD 169142 = H (1.65)**;
  **MP Mus = IB_2.06 (2.06 um)** — both fixed in staging + member overrides.
- Panel label mapping: "HR 4796" -> hr-4796a (categories override debris);
  **"MP Mus" -> existing system pds-66** (alt name already present);
  "Elia 2-25" -> NEW system `elias-25` (display "Elias 25", SIMBAD "Elia 2-25" —
  naming consistent with existing elias-20/24/27; distinct from DSHARP Elias 24).
- NEW systems: sz-91, elias-25 (-> coords_todo_batchI.txt). Regions: Sz 91 = Lupus III,
  Elia 2-25 = Ophiuchus; both protoplanetary/YSO.
- Member list + notes filled in the scattered.py NACO-PIPPIN block (defaults switched
  H/Ks 1.65 -> Ks 2.18 to match the majority of panels).

## 2. SEEDS gallery (Tamura 2016 Fig. 3) — metadata DONE, pixels PENDING (source file corrupt)

**`images/_sources/extra/seeds_tamura2016.pdf` is NOT a PDF** — it is a 1.8 KB NCBI/PMC
"Preparing to download" HTML interstitial (proof-of-work challenge), i.e. the host fetch
failed. The sandbox cannot fetch binaries (arxiv/jstage/PMC all blocked; only github/pypi
open; no Chrome browser connected this session). **Host re-fetch needed**:
`https://www.jstage.jst.go.jp/article/pjab/92/2/92_45/_pdf` (J-STAGE, open access) or
PMC4906811. Fig. 3 is a 4x5 grid -> trivial grid manifest once the file is real.

What WAS completed:
- Retrieved the **full text + complete Fig. 3 caption** via the Europe-PMC REST full-text
  route (r.jina.ai wrapper). Journal ref verified: Proc. Japan Acad. Ser. B 92(2), 45-55
  (2016), doi 10.2183/pjab.92.45, bibcode 2016PJAB...92...45T -> `verify=True` dropped
  from the paper block in scattered.py.
- Panel roster (rows, L->R) with ORIGINAL papers from the caption:
  r1: AB Aur (Hashimoto+2011), SAO 206462 (Muto+2012), MWC 758 (Grady+2013),
      LkHa 330 (Bonnefoy in prep.), TW Hya (Akiyama+2015)
  r2: PDS 70 (Hashimoto+2012), Sz 91 (Tsukagoshi+2014), WLY 2-48 = Oph IRS 48
      (Follette+2015), LkCa 15 (Thalmann+2010), HR 4796A (Thalmann+2011)
  r3: AB Aur close-up (Hashimoto+2011), HD 142527 (Fukagawa in prep.),
      HD 169142 (Momose+2015), RX J1604.3-2130A (Mayama+2012), GM Aur (Oh in prep.)
  r4: RY Tau (Takami+2013), SR 21 (Follette+2013), MWC 480 (Kusakabe+2012),
      UX Tau A (Tanii+2012), HIP 79977 (Thalmann+2013)
- **SEEDS block member list filled** (19 systems / 20 panels; AB Aur twice). Members with
  existing crops map via image_id overrides: ab-aur_seeds2011, hd-135344b_seeds2012,
  rx-j1604-3-2130_seeds2012 (no duplicate records will be created; make_systems skips
  existing image_ids).
- **`data/staging/seeds.json`**: 16 pending records (file=null -> "image pending"
  placeholder) with per-panel ORIGINAL citations and credit
  "Tamura 2016 Fig. 3 (crop); original: <Author Year>". arXiv ids found via WebSearch
  (6/6 budget used) + arxiv abs verification:
  Grady13 1212.1466, Akiyama15 1503.01856, Hashimoto12 1208.2075, Tsukagoshi14 1402.1538,
  Follette15 1411.0671, Thalmann10 1005.5162, Thalmann11 1110.2488, Takami13 1306.1887,
  Follette13 1302.5705, Kusakabe12 1205.3159, Thalmann13 1301.0625 — all confirmed.
  `_verify:true` set on: Momose15 (1505.04937) and Tanii12 (1206.1215) — ids from memory,
  unconfirmed. "in prep." panels (LkHa 330, HD 142527, GM Aur) cite the review itself.
- **RX J1604.3-2130 panel FILLED from the original source** (local 1211.3284):
  Mayama+2012 Fig. 1a H-band PI ring cropped -> fills the pre-existing pending record
  `rx-j1604-3-2130_seeds2012` (staging `i-rxj1604-seeds2012.json`; title verified from
  the TEX, bibcode 2012ApJ...760L..26M added, `_verify` cleared).
- `data/staging/i-seeds-retag.json`: minimal records adding survey:"SEEDS" to the three
  already-cropped SEEDS-era disk images (ab-aur_seeds2011, hd-135344b_seeds2012,
  lkca-15_seeds2014) so the collection groups in the frontend. Drop this file if unwanted.
  (kappa-and_seeds2013 / gj-504_seeds2013 planet images left untouched — orchestrator call.)
- NEW systems: sz-91 (shared with NACO), sr-21, hip-79977 (debris, Upper Sco)
  -> coords_todo_batchI.txt.
- NOTE for the orchestrator: run `make_systems.py` BEFORE `merge_staging.py` so the new
  systems get proper names/regions instead of auto-created shells.

## 3. beta Pic classic (Kalas & Jewitt 1995, AJ 110, 794) — DONE

`kalas1995_betapic.pdf` = ADS scan (12 pages). The wide-field R-band coronagraphic disk
image is **Fig. 1 = PLATE 33** (last page, false color, 6.5" occulting spot, north up);
rasterized at 300 dpi and cropped -> fills the seeded pending `beta-pic_kalas1995`
(448x560 px). Facility check: paper states UH 2.24 m on Mauna Kea, R filter -> the seeded
"UH 2.2m / coronagraph camera / 0.65 um" metadata is correct as-is.
Staging: `i-betapic-kalas1995.json`.

## 4. GG Tau classic (Roddier+1996, ApJ 463, 326) — DONE, facility CONFIRMED = CFHT

ADS scan, 13 pages; ring images are Plates 22-24 (Fig. 1 J, Fig. 2 H, Fig. 3 K; each
a=sharp-PSF / b=matched-PSF deconvolution). Cropped **Fig. 1b (J band, matched PSF)** —
the cleanest complete ring — filling pending `gg-tau_cfht1996` (560x403 px).
**Facility verified verbatim from p. 326**: "The instrument was mounted at the Cassegrain
f/36 focus of the Canada-France-Hawaii Telescope (CFHT)" (UH IfA AO system, 1994 Dec 23).
scattered3.py already said CFHT/UH adaptive optics -> no data fix needed; verification
comment added to the GG Tau block. Staging label updated to "J band 1.25 um (AO;
matched-PSF deconvolution)". Staging: `i-ggtau-cfht1996.json`.

## 5. HD 135344 Ab GRAVITY (Stolker+2025, 2507.06206) — DONE (new record)

`fig_gravity.pdf` (= paper Fig. 2) has three VLTI/GRAVITY dual-field Delta-chi^2 detection
maps. Cropped the **2023 Jul 1 epoch** (highest S/N = 5.0; planet position encircled at
~(-130, +38) mas) as NEW record `hd-135344-a_gravity2025`: type planet, VLTI-GRAVITY,
K band 2.2 um, technique interferometry, same Stolker+2025 paper as the existing
sphere2025 record. Staging: `i-hd135344a-gravity2025.json`.

## Deliverables

- 18 new/filled PNGs (all viewed, label<->file verified on a contact sheet; all trimmed,
  <=560 px, <=230 KB): 14x `_naco-pippin`, rx-j1604-3-2130_seeds2012, gg-tau_cfht1996,
  beta-pic_kalas1995, hd-135344-a_gravity2025.
- Staging: naco-pippin.json (14), seeds.json (16 pending), i-rxj1604-seeds2012.json,
  i-ggtau-cfht1996.json, i-betapic-kalas1995.json, i-hd135344a-gravity2025.json,
  i-seeds-retag.json (3 survey tags).
- Manifests: backend/manifests/batch-i/ (5 files).
- Seeds: scattered.py NACO-PIPPIN + SEEDS blocks filled; scattered3.py GG Tau comment.
- data/coords_todo_batchI.txt: Sz 91, SR 21, HIP 79977, Elia 2-25.

## Open items for the orchestrator

1. Host-fetch the real Tamura 2016 PDF (J-STAGE URL above), then crop Fig. 3 with a 4x5
   grid manifest; image_ids/records already staged (16 file=null waiting for pixels;
   keep credits as staged).
2. SIMBAD run for the 4 new systems (coords_todo_batchI.txt).
3. Confirm the two `_verify` arXiv ids: Momose+2015 (1505.04937), Tanii+2012 (1206.1215).
4. ingestion_status.json update (not touched per concurrency protocol): NACO-PIPPIN
   images=done; SEEDS entries/citations=done images=partial (1/20 filled, awaiting PDF);
   singles beta-pic kalas1995 / gg-tau cfht1996 / hd-135344-a gravity2025 = done.
