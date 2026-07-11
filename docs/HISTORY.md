# HISTORY — append-only session archive (diskatlas)

**Do NOT load this file into context.** It exists so details are never lost;
`grep` it for a specific date, system, or tool name when (and only when) a
question actually points here. Newest first.

---

## 2026-07-10 (latest) — caption-based missing-panel audit (panel_audit.py)

Built `backend/panel_audit.py` (user request: "whenever you crop an image it
should come from the captions of the Figures ... go through the entire archive
and see if you've missed many panels"). It reads each record's `Fig. N` credit,
pulls that figure's caption from the local arXiv `.tex`, estimates panel count,
and flags figures where atlas-held records < caption panels. Added confidence
tags: `multiband` (≥2 distinct wavelength tokens), `variant` (Uphi/r²/model/
weighting = display-only), `review` (untokenized band names). Run: 45 multiband,
82 review, 92 variant (`data/paper_finder/panel_audit_2026-07-10.txt`).

Burned down the multiband tier + spot-checked review, VIEW-verifying each.
**Recovered 9 genuine panels** (1540→1549 records): GM Aur ALMA Band 4 (Huang20)
+ ACS/SBC F165LP + ACS/HRC F330W + WFPC2 F555W (Hornbeck16, fixed F140LP epoch
2003-2008→2008-08-13); RY Tau CARMA 2.8 mm (Isella10); gamma Oph MIRI F1500W
(Han26); HD 16743 NICMOS F160W (Marshall23); Z CMa ALMA Band 6 1.3 mm streamer
(Dong22); HD 61005 IRDIS ADI K-band (Olofsson16 split-fix). **Rejected ~10 false
positives** — re-imaged archival data already held from the original (PDS 70 B7
= Benisty21; AS 205 1.3mm = DSHARP; HL Tau ALMA = Partnership), display variants
(J1608 coro/nocoro + Qphi/Uphi; 14 Her F444W subtraction stages; 3C273 pre-
subtraction c/e/g = held d/f/h), marginal/noise detections (HD 206893 0.88mm;
HD 15115 2006 Keck), and unresolved continuum insets (HD 97048 SIV/NeII).
Fetch lesson: single `curl` silently caps arXiv e-prints at 2 MiB — use `wget`.

Follow-up ("redo and gp") — maintainer set the redundancy policy: **record the
same target/band from any DIFFERENT paper**, including literal re-displays of
another team's product (documents reduction diversity; never skip on "already
have a better one"; only same-paper true duplicates + non-images + non-detections
+ unresolved points are rejected). Reversed the redundancy/quality skips and
added: HD 15115 Keck-II AO H (Kalas07), HD 206893 0.88mm (Marino20), AS 205
1.3mm (Phuong26 = DSHARP product), PDS 70 Band 7 (Doi24 = Benisty21 smoothed),
HL Tau 1.3mm (Carrasco-González16 = Partnership data). 1549→1554 records.
See auto-memory `cross-paper-redundancy-ok`.

## 2026-07-10 (later) — census adjudication of category-less systems

Ten systems with empty categories+planets but disk-typed records were adjudicated
against their source papers (Valegard 2024 A&A 685 A54 for DESTINYS-Orion; Garufi
2024 A&A 685 A53 for Taurus; Osorio 2016; Akeson 2019; + audit-2 extras):
(b) companion-only, records retyped disk_scattered->planet, companions added:
brun-252 B (new M0 0.22"), kiso-a-0904-60 B (known equal-mass 1.96", Tokovinin
2020), ry-ori B (possible substellar 0.076 Msun 0.39"), tx-ori B (new M5 0.11"),
v1787-ori B (Arun 2020, 6.6") + C (new M3 0.22"), v1788-ori B+C (known triple,
Tokovinin 2007), v2149-ori B (known F8 binary, Koehler 2006), v807-tau Bab
(0.17", Garufi 2024; its ALMA record removed: Akeson components unresolved/
Gaussian, Bab undetected at 1.3mm).
(a) resolved disk: xz-tau -> protoplanetary (Osorio 2016 dwarf transitional disk
around XZ Tau B, r~3.4 au); af-lep -> debris (ALICE F160W record).
(c) removed: v1025-tau (whole system; Garufi 2024: "No QU pattern ... treated as
a non-detection", Class III), vega_nircam2024 (F444W sources S1/S2 extended,
extragalactic background; disk undetected at F444W). Exclusions logged in
paper_finder_state (1901.05029, 2410.16551).
Audit-2 extras reconciled (planet-typed records, empty planets): 2MASS
J16120668 b (Halpha candidate, Li 2025), DM Tau b (NRM candidate, Willson 2016),
HD 100453 B (Chen 2006 + Follette 2023), HD 142527 B (Biller 2012 ApJL 753 L38),
HD 163296 b (F410M candidate, Uyama 2025), MWC 297 B (Ubeira-Gabellini 2020),
WW Cha B (GRAVITY 2021, interferometry).
NEW build-time audits (validate.py errors + build.py hard-fail, negative-tested):
disk-typed records with empty categories; planet-typed records with empty
planets. Final: 467 systems / 1497 records / 83 planet hosts / 0 errors.

## Session state 2026-07-10 (live log — update on every hand-off)

CURRENT: 468 systems / 1500 image records / 0 errors / 0 warnings /
**epoch coverage 92.1%** (1382 records carry an observation date).

07-10 ITEMS:
- **AGE-PRO Lupus complete 10/10** (Sz 66/77/95 new systems + Sz 72 record;
  Deng+2025 Fig. 5; compact disks flagged marginally-resolved in notes).
- **HD 143811 AB b**: both discovery figures in full — Jones+2025 (ApJL 995,
  L41) Fig. 1 all 3 panels AND Squicciarini+2025 (A&A 702, L10, COBREX) Fig. 1
  all 3 PACO S/N panels; 6 records, per-panel obs epochs; both papers credited
  on the planet (extra_papers).
- **THE EPOCH HARVEST** — see the dedicated section below. `epoch` = OBSERVATION
  date, never publication date; 13% → 92.1% in one pass, per-record provenance.

## Observation epochs (`epoch` field) — method & maintenance

The paper's core claim is *instrument- and epoch-level* coverage, so every image
record should carry the date the data were **taken**. The 2026-07-10 harvest
recovered 1382/1500 (92.1%); the method, in priority order (the paper writer
should describe it this way, numbers in `paper_Overleaf/notes_epoch_methods.md`):

1. **The record's own paper** (~700 records). `backend/epoch_harvest.py tex`
   parses the local arXiv sources (`images/_sources/extracted/<id>/`, fetched by
   `backend/fetch_sources.py`): TeX comments stripped (commented-out table rows
   poison naive regex extraction), observing-log **table rows matched by target
   alias AND the record's instrument keyword** (multi-target surveys observe
   different targets on different nights; multi-instrument papers different
   cameras), context windows naming a *different* instrument rejected
   ("foreign"), windows naming none may only vote year precision. Survey-specific
   extractors handle odd log formats (Ren Ks star-hopping log; GPIES / Crotts /
   Hom compact-YYMMDD; LIGHTS YYYYMMDD; DISCS bare-HIP rows; eDisk grouped
   rows). ~290 multi-date papers and pre-arXiv classics were hand-adjudicated by
   reading the extraction windows. Every manually REJECTED candidate is pinned
   in the script's BLOCKLIST so re-runs stay clean.
2. **Observatory archives** (~470 records), only where the paper states no
   dates, always bounded by the paper date (`backend/epoch_archives.py`):
   MAST for HST+JWST by position+instrument+filter; ESO TAP for SPHERE by
   position; ALMA TAP by **project codes greped from the paper tex** (exact
   per-target execution dates) falling back to position+band cones; Herschel
   HSA TAP.
3. **Precision is honest, never inflated**: `YYYY-MM-DD` only when all matched
   executions cluster within ~45 d; `YYYY` when they span one calendar year;
   `YYYY-YYYY` when the published image combines executions across years (the
   viewer chip shows the first year; tooltip says "observations span … (combined
   data)").

Every recovered epoch has its origin + evidence snippet in
`data/paper_finder/epoch_provenance.json` (tex:row/instr/adjudicated…,
mast:…, eso:…, alma:code/cone, hsa). `backend/epoch_audit.py` reports coverage.
The remaining 118 records (7.9%) are papers that state no dates AND archives are
silent: SMA-only REASONS targets, pre-TAP BIMA/VLA/SMA classics, VLTI/PIONIER
post-AGB, VHS tiles, a few SEEDS/CIAO images — recoverable only by per-paper
archaeology.

**Maintenance rule: every NEW record ingested from now on must carry `epoch` at
ingestion time** (read it from the paper's observing log while you have the
source open — it costs seconds then, hours later). Cross-checks that caught real
errors: instrument-impossible years (a "Herschel 2015" after the 2013 cryostat
death, an ACS date after the 2007 HRC failure), RV/calibration/reference-star
context leaks, and one corrupt legacy value (`lkha-233` had literal "Marin
2025", an author-year — true FOC epoch 1995-06-17 from MAST).

## Session state 2026-07-09 (previous log)

464 systems / 1490 image records / 0 errors / 0 warnings.

FINAL 07-09 ITEMS (after the burn-down below):
- **Metadata completion** (`audit_bibcodes.py --fill`, new mode): filled ALL 691
  `bibcode:null` blocks from arXiv→ADS resolution + derived 149 journal strings;
  Perrin GO-11155 poster → `2009AAS...21340903P`. First-ever 0-errors/0-WARNINGS
  validate. `export_bibtex.py` full pass: 598 entries, no author mismatches.
- **crop_qa full sweep**: session's 46 new crops all clean; 3 genuine MULTIPANEL
  fixes — β Pic d 6-panel gallery (Sutlieff & Bonse 2026) → 5 per-instrument
  records; Todorov 2010 WFPC2+NIRI 2×2 → 2 records; HR 8799 NICMOS 1998 two-roll
  crop → panel (c) alone.
- **`fresh_papers.py` first digest triaged** (8/8 reviewed, all excluded — CD-35
  2722 "exosatellite" = RV periodograms; CI Tau "hidden rings" = UNRESOLVED, the
  B3/B7 "maps" are polar R-φ plots not sky images; rest theory/transits/spectra).
  BUG FIX: state-ledger dedupe was a silent no-op (ledger keys are Semantic
  Scholar hashes); the sweeper now recognizes arXiv-id-keyed entries, which
  digest reviews write. Digest for the current window returns empty.
- **LATE 07-09 — 3 data bugs (user-reported overlapping markers + mislabel):**
  (a) GY 91 == ISO-Oph 54 and (b) GY 21 == ISO-Oph 37 were duplicate systems at
  identical coords (SIMBAD: both pairs are one [GY92] object) — merged the
  iso-oph-* dupes into the GY entries and deleted them; also fixed gy-91's WRONG
  alias "ISO-Oph 63" (that is [GY92] 109). Then (user follow-up) renamed both
  FULLY to their ISO-Oph designations — display name, slug/id, image dirs, and
  image_ids all `iso-oph-54` / `iso-oph-37` (the names the 4 covering papers use);
  GY 91/21 and [GY92] 91/21 kept as searchable aliases. NOTE: `git mv a b/c.png`
  does NOT create dir `b/` (unlike `mv`) — `mkdir -p` the destination first.
  (c) UX Tau's `alma2020` crop was
  actually the SPHERE J-band Qphi image (Menard 2020 Fig. 1) — relabeled it
  VLT-SPHERE/IRDIS J and added the REAL ALMA record from the same paper's
  Fig. B.1. Net: 466→464 systems, 1489→1490 records.
- **Agent-doc + paper number sync (user asked, other agents offline):** the paper
  `paper_Overleaf/ms.tex` was lagging at 466/1475 — updated abstract, census
  table (tab:census), SIMBAD count (464 sys / 462 resolvable — G023.01-00.41
  resolved to MSX5C G023.0126-00.4177 on 2026-07-09, leaving only the 2 HSC
  z>6 quasars as genuine exceptions), conclusion, and
  the dedup narrative (now names the two Oph merges); regenerated tab-coverage /
  tab-tonight / fig-skymap / fig-census and recompiled `ms.pdf` with tectonic
  (12 pp). All prose stats in README/HANDOFF also refreshed to 464/1490.
  CANONICAL CENSUS (recompute with build.py + the counting snippet if editing
  the paper): 464 systems = 262 protoplanetary + 106 debris + 19 evolved + 58
  companion-only + 20 quasar (58 = 464 − 406 categorized; 1 system is
  multi-category); 1490 records; 81 non-refuted companions across 68 hosts;
  599 distinct cited papers; 38 facilities; 67 instrument families; 9921/867
  candidates harvested/triaged.

WHAT THE 07-09 CONTINUATION DID (all committed + pushed to master):
- **Directed multi-figure adds (user-requested, high yield):** Weber+2023 SPHERE/IRDIS
  H for AS 205 / SR 24S / FU Ori; Dasgupta+2025 ERIS L' for V960 Mon; Ren+2019 Fig. 1
  STIS/NICMOS/GPI for HD 191089; Faramaz+2021 ALMA B7 for HR 8799; Stark+2023 STIS for
  HD 53143; Wagner+2015 IRDIS K1/K2 + IFS Y/J/H for HD 100453. FIXED DoAr 44 Casassus
  mislabel (crop was Fig 1b = ALMA 336 GHz, labeled SPHERE → split into correct a+b).
- **NEW TOOL `backend/system_audit.py` — target-side completeness audit** (see the
  `target-side-completeness-audit` memory). ADS `abs:"<name>"` per system (anonymous
  tier has NO `object:`), gate = imaging-phrase + named-facility + DISK_CTX
  (disk/companion context; kills the abs:"DO Tau"→Planck collisions), rank by
  citations × instrument-novelty. Headline output = NEW-INSTR gaps. Cache + report
  under `data/paper_finder/` (gitignored). Verified finds ingested: PDS 70 MagAO Hα
  (Wagner+2018 — the ORIGINAL accreting-planet detection), HD 100546 MagAO Hα
  (Follette+2017), HR 4796A MagAO Clio-2 L' + VisAO Ys (Rodigas+2015), HD 100453 NACO
  Ks companion-B discovery (Chen+2006, non-arXiv; ADS `link_gateway/<bib>/PUB_PDF`).
  False positives correctly skipped by VIEW-verify: Fomalhaut "Subaru" (J-band
  non-detection), HD 100546 "ZIMPOL" (sample mention; figures are HD 142527).
- **Miles Lucas feedback:** instrument taxonomy now `SCExAO/CHARIS` (23 records,
  was flat CHARIS) + `SCExAO/VAMPIRES` + `SCExAO/MEC`, matching the SPHERE/<sub>
  convention (frontend parent-prefix filtering handles it generically). His papers:
  HD 169142 (Lucas+2025 AJ) Fig. 3 2×4 gallery → 7 per-instrument records incl. the
  atlas' first VAMPIRES record; VAMPIRES instrument paper (Lucas+2024 PASP) → NEW
  SYSTEM R Aqr (evolved; Hα jet+nebula); AB Aur Dykes+2024 Fig. 2 → J/H/K split
  (replaced JHK composite; paper has TWO caption typos: band order and "January"
  epoch — trust panel labels: 2020-10-04); HD 34700 Chen+2024 Fig. 3 middle column
  → Qphi J/H/K. Mullin+2026 & HD 1160 stamps reviewed (already in / not atlas-grade).
- Worklist CLOSED OUT 2026-07-09 (all four items resolved):
  (1) "T Tau Keck (Bally+2000)" = COLLISION — ADS stems abs:"T Tau" to match
  "T Tauri", so EVERY t-tau audit flag was about other Taurus objects; Bally 2000
  is Orion proplyds. Lesson recorded in the target-side-completeness-audit memory.
  (2) Vega NICMOS/Keck flags = "Vega-like" phrase collisions — coverage verified
  complete. (3) DISCS SMA (Öberg+2011): ingested 267 GHz continuum for IM Lup +
  HD 142527 (MY Lup flag = false positive, not in the sample). BONUS from the same
  worklist row: Looney+2000 BIMA 2.7 mm panel-(d) maps ingested for DG Tau,
  DG Tau B, L1551 IRS5, HL Tau, GG Tau, GM Aur (new BIMA facility for all six).
  (4) Morales+2013: title lists the full sample (HD 70313/71722/159492/104860) —
  all four already in the atlas; nothing left. (Fukagawa+2010: user-checked,
  dropped. Padgett+1999: done, 5 panels + 3 new systems.)
- **NEW TOOL `backend/fresh_papers.py` (2026-07-09)** — the forward-looking weekly
  sweep (last N days of astro-ph.EP/SR via anonymous ADS `arxiv_class:`+`entdate:`;
  the arXiv export API 429s this host). Flags atlas-target mentions (literal
  word-boundary names, no stemming trap) + candidate new imaging papers; dedupes
  against both ledgers. RUN WEEKLY: `python3 backend/fresh_papers.py` → review the
  digest, VIEW figures, ingest. Also: `audit_bibcodes.py --fix --fill` after every
  big batch (2026-07-09 pass filled ALL 691 null bibcodes + 149 journals → validate
  is now 0 errors / 0 WARNINGS; keep it that way).
- FINAL burn-down of the remaining top-of-list flags (2026-07-09, list now clean):
  GQ Lup NACO discovery + AU Mic Keck (Liu 2004) = already in atlas (flags were
  im-lup/beta-pic name collisions). NGC 1068 VLA = REAL gap → ingested Gallimore
  1996 Fig. 2 VLA-A 6 cm jet map (ADS scan, no arXiv; skipped the 18 cm Fig. 1 —
  inset-collage too tangled to crop cleanly). Verified non-imaging and skipped:
  DG Tau STIS (jet spectroscopy), Keck-Interferometer/PTI visibilities (dg-tau,
  mwc-297), NIR spectral library (ct-cha/dh-tau/et-cha), [Ne II] spectroscopy
  (cs-cha/hd-34700), PDS 70 GRAVITY astrometry (no image figure), Natta 2004 VLA
  Herbig 'search' (photometry), as-218/et-cha ALMA sample-statistics flags.

## Session state 2026-07-08 (previous log)

WHAT THIS SESSION DID (all committed + pushed to master):
- **Snowball deepening then saturation.** Added the BACKWARD reference axis to
  `find_papers.py` (`--direction both`, `cache_refs/`, `--min-year 1995`) so non-arXiv
  classics (Grady 2005, Perrin 2009, Schneider/Augereau…) surface, not just forward
  citations. Ran many PF/discovery batches → grew from ~405 to 462 systems (post-AGB
  "evolved" disks, AGB/RSG, massive-YSO, edge-on protostellar, quasar-host, plus classic
  HST/NICMOS/STIS/ACS coronagraphy). Hit genuine SATURATION: last keyword sweep was
  ~2 hits / 700 candidates. **The user's directed "add paper X, crop figure Y" requests
  are far higher-yield than the autonomous dragnet** — treat the snowball as a *targeted*
  tool now, not a background crawl.
- **Multi-panel figure splitting (big theme; see the `split-multipanel-figures` memory).**
  Source figures that show one target at several wavelengths were often ingested as ONE
  crop → mis-sorted (a Ks+L' strip hidden at 3.8 µm). Split ~26 records → ~74 per-band
  records across fleets + individual asks (3C 273 Komugi 3 ALMA bands, PDS 201 Wagner LBTI
  Ks/L'/vAPP, HD 135344B Stolker R/I/Y/J, HL Tau Mullin NIRCam 2×2, CY Tau Perez mm strip,
  ESO Hα 569 Wolff F606W, HD 15115 CHARIS J/H/K, HIP 65426 JWST 6-band, etc.). RULE:
  re-crop each band FROM SOURCE (don't slice the low-res combined image); one record per
  band; DON'T split RGB composites / wavelength ranges / same-band roll angles / multi-epoch
  galleries / "B/C"=companion-letter panels. Splitting also caught facility mislabels
  (CY Tau "VLA" was really CARMA at 1.3/2.8 mm).
- **New local QA tooling (runs on the DGX, token-free — use these before eyeballing):**
  `backend/crop_qa.py` (edge-uniformity / colorbar-bleed / gutter / MULTIPANEL / `--ocr`
  axis-text; report → `data/paper_finder/crop_qa.json`), `backend/dup_check.py` (md5
  exact-dup reliable; `--near` GPU pHash is noisy for faint crops), `backend/audit_bibcodes.py`
  (arxiv→ADS bibcode audit, `--fix`). GPU note: at ~1.4k small crops there is NO useful
  GPU speedup (I/O-bound); the real bottleneck is token-judgement + source-PDF fetches.
- **Bibcode/metadata audit** (`audit_bibcodes.py`): fixed 14 hallucinated/wrong bibcodes
  + 4 mislabeled first-authors (AR Pup Kluska→Ertel, Orion Src I Chen→Wright, HH 212
  Lin→Lee, BD+45 598 Farkas→Vincent), re-derived 29 journal strings. Anonymous ADS via
  `ui.adsabs.harvard.edu/v1/accounts/bootstrap` (no token). Keep bibcodes ADS-correct;
  resolve `bibcode:null` records opportunistically.
- **`evolved` category added** (backend `validate.py` CATS + frontend chip/legend/hexagon
  marker; 21 systems: post-AGB + AGB). **SPHERE instrument facet split** into
  `SPHERE/IRDIS` · `SPHERE/ZIMPOL` · `SPHERE/IFS` (`facility_map.instr_key`); the frontend
  INSTRUMENT facet does parent⊇children (clicking "SPHERE" matches all three).

NEXT / OPEN: snowball is at diminishing returns — prefer user-directed adds. `crop_qa.py`
GUTTER_EDGE (167) is mostly benign (edge-on disks have dark-sky edges) — screening only;
its MULTIPANEL flags are the actionable ones. Morales 2013 has 3 more Herschel belts if
wanted (HD 70313/71722/159492 already added; sample was 4). A local ML QA-classifier (fine-tune
on the GB10 to replace token-costly crop eyeballing) was proposed but not built.


---

## Ledger prose archive (moved out of data/ingestion_status.json 2026-07-10)

2026-07-10 EPOCH HARVEST: observation-date backfill 13%->92.1% (1382/1500; remaining 118 = SMA-only REASONS targets, pre-TAP BIMA/VLA/SMA classics, VLTI PIONIER post-AGB, VHS tiles, a few SEEDS/CIAO). epoch = OBSERVATION date at honest precision (day / YYYY / YYYY-YYYY range for multi-year combines). Pipeline: backend/epoch_harvest.py (multi-target tex extraction: comment-stripped, alias+instrument row/window matching, foreign-instrument window rejection, BLOCKLIST of manually rejected poisons) + backend/epoch_archives.py (MAST HST+JWST by position+instrument+filter, ESO TAP for SPHERE, ALMA TAP by tex-greped project codes then cones, Herschel HSA TAP) + backend/fetch_sources.py (~310 arXiv source packages fetched incl old astro-ph/ ids) + survey-log extractors (Ren Ks star-hopping, GPIES/Crotts/Hom YYMMDD, LIGHTS YYYYMMDD, DISCS bare-HIP, eDisk/MAPS/sigma-Ori rows) + ~200 hand-adjudicated picks from reading source windows. Per-record provenance in data/paper_finder/epoch_provenance.json. Viewer: obs epoch = bare bold year chip (tooltip full date/range); pub year only as italic (YYYY) fallback. Remaining ~10% = papers that state no dates + archives silent (old BIMA/VLA/SMA, VLTI PIONIER post-AGB, VHS tiles, some SEEDS/CIAO classics). 2026-07-10: 468 systems / 1495 records / 0 errors. Internal-review batch. AGE-PRO Lupus sample now COMPLETE 10/10 (Deng+2025, 2506.10734): added the 3 absent targets Sz 66 (Lupus 8), Sz 77 (Lupus 5), Sz 95 (Lupus 9) as new systems, each ALMA Band 6 1.3mm continuum from Fig.5; SIMBAD-resolved coords/mags; compact disks flagged marginally-resolved (~0.35"/~54 au beam) in record+system notes. Lupus-number<->source mapping from Fig.3 SED labels: L1 Sz65, L2 Sz71, L3 J16124373-3815031, L4 Sz72, L5 Sz77, L6 J16085324-3914401, L7 Sz131, L8 Sz66, L9 Sz95, L10 V1094 Sco. EPOCH = observation date (was mislabelled pub date): frontend chip shows obs epoch as a bare year (full date in tooltip), pub year only as italic (YYYY) when obs epoch unknown; backend/epoch_picks.py holds 135 curated source-verified obs dates matched per-record to each record's instrument (coverage 3.9->13.1%). Survey-recall gaps worked: tagged sz-71 + v1094-sco AGE-PRO continuum records (survey field was null though labels said AGE-PRO); NEW Sz 72 (=HM Lup, Lupus 4) ALMA Band 6 1.3mm continuum from Deng+2025 AGE-PRO-III Fig.5 (2506.10734). DEFERRED recall gaps (low value / risky crop): gamma Oph REASONS mm belt (already have JWST/MIRI thermal; Fig.1 is a dense 74-panel in-raster-labelled gallery, panel-index crop error-prone), IRAS 04302 eDisk Band 6 (already has Villenave Band 4+7 + 8 other records). exoALMA 'HD135344' and MAPS 'HD 162396' recall hits = false positives (disk is hd-135344b which already has exoALMA; MAPS parse artifact). 2026-07-08 (post-crash recovery): 405 systems / 1249 records / 0 errors. Recovered 42 orphan crops (crash killed 7 agents; re-verified every arXiv id from source, rebuilt records) + GJ 581. Ledger 484/721/5477. 403 systems / 1200 records / 0 errors. Snowball run 2 with --rank triage (target-matched papers first); exoALMA I CO gallery; MWC 758 Ren epochs; PF4+PF5 agent batches in flight (see HANDOFF.md 'Session state 2026-07-08'). 2026-07-07 FINAL for this session: 401 systems / 1181 image records (all local) / 65 imaged-companion hosts / 0 errors / SIMBAD 399/399 resolvable idents coordinate-verified (2 explicit-null quasars use coordinate links). 400+ systems / 1160+ records / 0 errors. Done: SEEDS Tamura Fig.3 completed (+AB Aur close-up); instrument-level sweep v2 over ALL systems (44 agents, ~140 verified new-instrument crops incl. far-IR scope extension); Hom+2024 GPI totI; Ren+2023 Ks Qphi completion; Xie+2022 RDI gallery; MAPS CO maps; pre-ALMA mm classics; user-batch figures (beta Pic d, WISPIT 2, HD 142527 B, AB Aur moment-1, 49 Cet, TWA 7, HR 8799 archival, MUSE maps, ACS gaps); survey batches eDisk(17)/AGE-PRO(16)/SPHERE-NIR-census(25)/sigma Ori(pending)/eruptive stars(4+Z CMa); paper-finder Skill run 1 (25+ new companion hosts & disks: PZ Tel B, VHS J1256 b, HD 33632 Ab, HIP 21152 B, RY Lup, SR 12 c, Wray 15-788, CVSO 30, HD 143811...); catalog cross-checks (Wikipedia 20 missing verified; circumstellardisks.org 323 mined, proplyd+Herschel-debris waves launched). Data fixes: hip-79977 merged into hd-146897 (duplicate); 5 HSC quasar name signs; YSES 2b refuted; wrong ids fixed (HD 169142 planet 2303.03652->2302.11302; beta Pic c; YSES-1 b/c swap; FW Tau 1303.4525->1311.7664). Frontend: Instrument facet; Facility facet = AAS keywords (facility_map.py, VLT>=VLTI rule); light/dark theme; airmass.org chart links; SciX citation linkifier + extra_papers; SIMBAD audit (25 idents repaired, coord-verified) + coordinate-link fallback; panel-only crop trim (450 files). Still in flight at time of writing: sweep chunks 01/08/11, Kurtovic ALMA-summary batch, proplyds x3, Herschel-debris x2, PF2. See _ledgers for bookkeeping split. 2026-07-08 keyword-discovery sweep B: 430 systems / 1322 records / 0 errors. +10 genuinely new resolved systems via open-ended arXiv keyword search (not citation-crawl): BD+45 598 (SCExAO/CHARIS debris disk), AR Puppis (SPHERE ZIMPOL/IRDIS circumbinary disk), L1551 IRS 5 (ALMA circumbinary ring), HH 80-81 (VLA/SMA massive-protostar disk), HR 5999 (VLTI/AMBER reconstructed sub-AU image), ET Cha (SPHERE DESTINYS companion detection), 99 Herculis (Herschel polar circumbinary debris disk), Orion Source I (ALMA/JVLA edge-on disk), HH 212 (ALMA 878um polarization edge-on disk), 2MASS J16083070-3828268 (SPHERE PDI transition-disk cavity). Dropped as non-qualifying during triage: FN Tauri (SMA shows point source only, no resolved structure), Kleinmann-Wright Object (MIDI visibility/SED fit only, no reconstructed image), HD 106893 (name likely confused with HD 106906, no arXiv hits), J1407/V1400 Cen (ring system only eclipse-photometric, ALMA non-detection), WD 1054-226 (photometric transiting debris, no image). Queued for future ingest: CB 26 (ALMA edge-on dust continuum), L2 Puppis (ALMA resolved disk + candidate planet), WL 17 (ALMA substructure, Ophiuchus), HD 113337 (Herschel disk image embedded in modeling paper, needs cleaner figure), Cep A HW2 (LBA high-mass disk-outflow).
