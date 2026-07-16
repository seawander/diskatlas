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

Herschel PACS coverage push (maintainer: "PACS is a very good instrument and we
didn't cover its images that well"). Baseline was 19 PACS records / 108 debris
disks, almost all single-band. Added **16 PACS records across 9 systems** (1554→
1570), VIEW-verifying every band is genuinely resolved and excluding unresolved
SPIRE/SCUBA blobs + PSF-reference panels: HD 10647 70/100/160 (Liseau10, user-
directed); multi-band fills eta Crv 100/160, AU Mic 160, HR 8799 100/160,
HD 207129 100/160, Vega 160; new-target β Pic 70/100/160 (Vandenbussche10),
HD 181327 70 (Lebreton12), HD 105 70 (Donaldson12, marginal). ~30 lesser no-PACS
debris disks remain (each in a scattered dedicated paper — no efficient multi-
target image source: Pawellek14 is modeling-only, DEBRIS/Tuc-Hor survey papers
yield ~1 resolved target each). "etc observatories" (Spitzer MIPS, SCUBA-2, …)
is a still-broader follow-on. Verify every arXiv id via ADS first (Liseau =
1005.3137 confirmed, not memory).

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


2026-07-11 CAPTION-COMPLETENESS + LANDMARK-SYSTEM SESSION: 1717->1764 records / 474->475 systems / 0 errors, 9 pushes. Executed the maintainer's TOP rule (read EVERY figure caption of EVERY cited paper; one record per instrument/band/epoch; chase new instruments; VIEW-verify panel<->label to avoid hallucination) via fan-out general-purpose crop agents (wget source NOT curl, read all captions, VIEW-verify, panel-only crops <=480px FASTOCTREE, reject models/residuals/S-N maps/non-detections/re-displays; cross-paper redundancy kept = same dataset reduced by a DIFFERENT team/paper is recorded, only same-paper true dups rejected). Agent yields:
- N (+7): HD 100453 MagAO/Clio-2 L' + SPHERE H23 (Wagner 2018); HR 4796A SPHERE IRDIS H-cADI/H2H3-cADI/IFS-YJ (Milli 2017); HD 172555 ZIMPOL VBB 2015 (Engler 2018); Elias 24 ALMA Band 6 ODISEA (Cieza 2017, distinct team from existing DSHARP/Andrews).
- P (+7): HD 121617 ARKS VIII Band 7 (Marino 2026); 4 ODISEA Oph Band 6 disks iso-oph-37/54/127/165 (Cieza 2019, earlier epoch than existing); Oph IRS 48 ALMA Band 7 + VLA Ka (Ohashi 2020).
- Q (+12): HD 142527 NACO H/Ks PDI (Avenhaus 2014); HD 100546 NACO H/Ks/L' PDI multi-epoch incl. first-ever L'-band disk PDI + Gemini/NICI Ks spiral (Boccaletti 2013); HD 32297 NACO H/Ks LOCI (Boccaletti 2012); beta Pic NACO Lyot-H + FQPM-Ks (Boccaletti 2009).
- R (+6): HD 163296 + HD 135344B NACO H/Ks PDI (Garufi 2014/2013); beta Pic b NACO M' 4.78um first-5um image (Currie 2011); HR 8799 bcd Keck/NIRC2 2005 H-epoch A-LOCI (Currie 2012).
- S (+2, within-atlas fix): split MWC 758's under-split generic JWST/NIRCam record into per-filter F187N + F200W, corrected technique coronagraphy->ADI (paper uses direct imaging + ADI-KLIP, no coronagraph); AU Mic JCMT/SCUBA-2 850um marginally-resolved (Matthews 2015).
- T (+7): HD 142527 ALMA Band 7 continuum + mm-polarized-intensity + CO(3-2) gas map (Ohashi 2018 = new mm-pol & gas modalities for the disk); HR 4796A NaCo Ks PDI 2013 + NICMOS F222M first-published + NaCo L' epoch 2010-04-06 (archival Lagrange 2012 = arXiv:1207.1987, obs date source-verified); beta Pic NaCo L' scattered-light DISK (Milli 2014) + GPI J-band planet b 2018-11-18 post-conjunction (Nielsen 2020). Marino 2015 rejected entirely (schematic + re-display + RT models).
- U (+5, NEW SYSTEM): V883 Ori (v883-ori) — landmark FU Ori-type water-snow-line disk, Orion L1641; dist adopted ~414pc since Gaia DR3 parallax unreliable during outburst (matches sibling FUor HBC 494); 5 resolved ALMA bands: Band 6 1.3mm snow-line 0.03"/12au (Cieza 2016 Nature) + Band 6 combined-config (Cieza 2018) + Band 7 0.88mm / Band 4 2.0mm / Band 3 3.1mm (Houge 2024).
SATURATION CONFIRMED this session: panel_audit 'multiband' flags are mostly FALSE POSITIVES (extra panels are U_phi/SNR/model/re-display; atlas already holds the real bands e.g. AF Lep F444W, HD 163296 JWST F410M/F200W + SPHERE H/J, HD 106906 MIRI both filters). Under-split-generic-record class exhausted to its last real case (MWC 758, fixed; MWC 297 already properly split into IRDIS 2018 + IFS 2015 + IFS 2018). Final 3-paper discovery sweep (Xie 2024 2410.00136 = JWST MIRI/MRS spectroscopy of T Cha outburst, NOT imaging; Villenave 2025 2503.05872 + Zhang 2023 2305.03862 = visibility-reanalysis re-displays of already-held DSHARP/Taurus-survey/ODISEA data) returned ZERO new images/systems. LOGGED for future directed adds (data/paper_finder/new_system_candidates.txt): Orion 218-354 silhouette disk (Follette 2013 MagAO/VisAO Halpha SDI, first ground-based AO silhouette disk). Consistent with maintenance-mode: retrospective discovery is saturated; prefer weekly fresh_papers + directed asks over bulk crawls.

2026-07-11 (consistency audit). Full audit pass over the post-Orion-batch
database: validate.py 0/0, dup_check 0 byte-identical crops, crop_qa 0
MULTIPANEL / 0 missing files (246 GUTTER_EDGE advisories, borderline-pixel
class, left as-is), audit_bibcodes --fix --fill verified all 624 papers clean
and derived 8 missing journal strings. Epoch sweep caught 12 records ingested
in the last two days without observation dates (rule-4 misses) and recovered
all of them from sources: Looney et al. 2000 BIMA 2.7 mm survey (6 records,
survey window 1996 May-1998 Mar -> 1996-1998), CY Tau VLA 7.1 mm (Perez 2015
observing log, Q-band tracks 2010-2012), PDS 66 GPI K1 (Wolff 2016 Table 1,
2014-05-15) and STIS (MAST GO-12228 visits 2011-03-31 + 2011-06-04 -> 2011),
V960 Mon ERIS/NIX (Dasgupta 2025, 2024-01-01), NGC 1068 VLA A-array 6 cm
(Gallimore 1996 Table 1 read from the ADS scan, 1994-05-09), HD 100453 NACO
(Chen 2006, archival ESO data, 2003-06-02). Epoch coverage 93.6% -> 94.3%
(104 dateless records remain, all pre-audited hopeless class).

2026-07-11 (annotation audit, user-reported). User caught the HIP 39017 NIRC2
L' credit citing "Franson et al. 2024" for a Tobin et al. 2024 figure, and a
missing third panel in the Tobin detection figure. Fixed both: the missing
CHARIS Dec 2022 panel was re-cropped from source (hip-39017_charis-dec2022,
epoch 2022-12-31 from the observing log), the Feb CHARIS epoch corrected from
"2022-2023" to 2022-02-21, and all three credits now carry panel-precise
Tobin references. A global credit-vs-paper scan (surname + year against the
paper block) then swept all records: 7 more mis-attributed or placeholder
credits fixed after VIEW/source verification (AR Pup ZIMPOL Kluska->Ertel
Fig. 5; Orion Src I Chen 2021->Wright 2022 Fig. 1; BD+45 598 Farkas->Vincent
Fig. 3; HH 212 Lin->Lee Fig. 1a; HD 92945 + TWA 20 JWST placeholder credits
-> Lazzoni/Palatnick Fig. 1 panels; WISPIT 1 placeholders -> Fig. A.2/A.3;
WISPIT 2 placeholders -> Lawlor Fig. 8 per-epoch panels). Also synced 35
paper-year fields to their ADS bibcode years (arXiv-year drift, e.g. "Bohn et
al. 2019" -> 2020) with 28 credit strings updated in step, and normalized 4
first_author formats ("M. Benisty" -> "Benisty"). validate.py now enforces
all of this permanently: credit-vs-paper author/year consistency and
paper-year-vs-bibcode-year are ERRORS (ALICE/archive credits exempt).

2026-07-11 (notes citations, user-reported). User flagged that HIP 39017's
free-text notes asserted the star's age, gamma Dor variability, and HGCA
acceleration with no references, so they read like unsourced/hallucinated
claims. Fixed HIP 39017 (each claim now cites Handler 1999 / Henry 2011 /
Brandt 2021 / Tobin 2024, added as companion-b extra_papers) then swept the
whole atlas: 64 systems had claim-bearing notes with zero citations. Rewrote
57 of them to weave inline author+year citations (7 pure "coverage:" editorial
notes left as-is); 66 of 67 mentions now linkify to real SciX abstracts, the
lone search-link being 61 Vir's RV-planet ref (Vogt 2010, not a recorded
paper). Also hardened frontend linkifyCitations: a shared citeSurname() helper
deaccents+lowercases the last name token and the name character class now
includes accented letters, so "Huélamo+2026" and "El Morsy+2025" resolve to
their abstracts (verified in-browser via the local Chromium). Most of the
batch-3 data edits + the app.js change were swept into the concurrent
ingestion session's commit e33f558 by its git add -A (shared-checkout race);
content is correct and on master.

2026-07-11 (single-image imaged-planet reaudit, user-directed). User rule: a
confirmed directly-imaged planet is almost never confirmed by ONE image - it
needs multi-wavelength/multi-epoch, preferably multi-instrument coverage, "or
the field treats it as a candidate, not a planet." Two-step reaudit of every
lone-image planet host: STEP 1 = split the cited discovery figure into all its
panels; STEP 2 (mandatory if still single) = find a second detection in ANOTHER
published paper via ADS/arXiv. Ingested 44 records this pass (2102->2146), on top
of the earlier +12 already in 721b934 (beta Pic d, GJ 504 5 filters, HR 8799
2004, HD 33632 A, HIP 21152). Step-1 splits (+28): HIP 75056 Bb full Y/J/H/K1/K2
x 2 epochs (Wagner 2020), GJ 758 B two 2009 CPM epochs (Thalmann 2009), HIP 64892
B (Cheetham 2018), HD 984 B NACO+SINFONI (Meshkat 2015), CD-35 2722 B NICI
JHK+NIFS (Wahhaj 2011), XEST 13-010 KOINTREAU-2b Pan-STARRS grizy (Walker 2026),
LSPM J1446 2nd L' epoch (Uyama 2025), GU Psc b Keck H+K (Naud 2014), 2M0219 F2 J
(Artigau 2015). Step-2 second-paper detections (+16): HD 19467 B gained 6 JWST/NIRCam bands (Greenbaum 2023) + 4
SPHERE/IRDIS bands (Maire 2020); HIP 78530 B gained LBT/LMIRCam L' (Bailey 2013);
DH Tau b gained SPHERE-IRDIS H (van Holstein 2021) + HST/WFC3 F656N (Zhou 2014);
SR 12 c - which held ONLY its ALMA CPD map - gained its missing optical+mid-IR
detection: HST/WFC3 F656N (Finley 2026, 2606.12862) + Spitzer/IRAC 3.6um
(Martinez 2022); CVSO 30 c gained a Keck/NIRC2 H panel (Schmidt 2016 step-1).
Honest negatives (searched, no companion detection image published): CT Cha b
(Bonnefoy 2014 spectra-only; Ginski 2024 unresolved pol. light) stays single;
Lachapelle 2015 (HIP 78530) spectroscopy-only. Also surfaced: YSES 2b is now a
refuted background star (Kenworthy 2025) and FW Tau b is disputed (edge-on disk /
low-mass star, Caceres 2015 / Wu 2017) - left annotated, not forced. Final scan:
of 26 remaining lone-planet-image hosts, ALL fall in justified buckets (13 disk-
embedded candidate protoplanets w/ rich disk coverage, 7 SPHERE disk-survey
stellar companions, 3 brand-new 2026 KOINTREAU candidates, 2 wide-CPM confirmed
by CPM+spectroscopy, 2 refuted/disputed); zero unexplained singles. 520 systems,
2146 image records, 0 errors / 0 warnings.

2026-07-11 (CT Cha b, user-directed - corrects the "stays single" call above). The
prior step-2 agent declared CT Cha b single after checking only Bonnefoy 2014 +
Ginski 2024. The maintainer pointed to the fuller literature: +5 detection panels
added. Wu 2015 (arXiv 1501.01396 = 2015ApJ...801....4W) Fig 1 BOTTOM row = Magellan
MagAO/VisAO halo-subtracted optical detections of CT Cha B in r' (0.62, faint/
smoothed), i' (0.77), z' (0.91), Y_S (0.98 um), obs 2013-04-06. Cugno 2025 (arXiv
2509.15209 = 2025ApJ...991L..46C, ApJL) = JWST/MIRI MRS spectral-cross-correlation
starlight-removed detection of CT Cha b's carbon-rich circumplanetary disk (13.3-
15.6 um image, PID 1958, obs 2022-08-15). CT Cha b now has 6 planet images spanning
NACO NIR (Schmidt 2008) + MagAO optical (Wu 2015) + JWST mid-IR (Cugno 2025).
LESSON: a "no follow-up image" negative from a narrow 2-3 paper agent check is
unreliable - run the full ADS abs:+imaging sweep before concluding single. 520
systems, 2151 image records, 0 errors / 0 warnings.

2026-07-11 (FU Ori binary companion, user-directed). FU Ori held only disk images;
added the infrared companion FU Ori S (~0.5"/~230 au S of FU Ori N, a reddened
A_V~8-12 ~late-G/K young star, possibly the more massive component). +4 detection
panels: Pueyo et al. 2012 (arXiv 1211.6741 = 2012ApJ...757...57P) Fig 1 bottom row =
Palomar/P1640 damped-LOCI coronagraphic REDUCED J (1.24) + H (1.65 um) images
(FU Ori N behind the mask, S arrowed), obs 2009-03-17; and Subaru/IRCS AO K' 2.12 um
of the 2003-12-15 epoch in two reductions kept per cross-paper policy - Reipurth &
Aspin 2004 (2004ApJ...608L..65R, non-arXiv, pulled via ADS PUB_PDF gateway) Fig 1
discovery image (FU Ori 180deg-rotation self-subtracted, S 0.5" S) + Pueyo 2012
Fig 6 right self-calibrated-PSF reprocessing of the same IRCS data. Added FU Ori S
to planets[] (validate requires a planets entry when planet-typed images exist);
planet_hosts 87->88. 520 systems, 2155 image records, 0 errors / 0 warnings.

2026-07-11 (CT Cha discovery-crop fix, user-reported). The held Schmidt & al. 2008
(0809.2812) Fig 1 NACO Ks crop (ct-cha_naco2008) had been zoomed onto the saturated
CT Cha A blob only, cutting OFF the companion candidate (CT Cha B) 2.67" NW. Re-
cropped the full published panel from the source EPS - now shows CT Cha A, the
labelled "companion candidate" (B), the cc2 background object, N/E compass and 1"
scale bar. Also corrected the record epoch 2006-02-17 -> 2007-03-02 (the caption
states Fig 1 is the 2007 March 2 image) and set Ks 2.18 um. No count change.

2026-07-11 (jets in ppds - new coverage axis, user-directed). Started documenting
protoplanetary-disk JETS/HH flows (typed disk_scattered, matching how the atlas's
8 existing optical-jet images are already typed - no schema change). ESO Halpha 574
(edge-on Cha I CTTS, previously only an ALMA Band 7 edge-on disk): added its HST/
WFPC2 bipolar-jet image (knots A1-A3) cropped from Whelan et al. 2014 (arXiv
1403.3232 = 2014A&A...565A..80W) Fig 1 left, which re-displays the Robberto 2012
HST data (early 2009); also rewrote the placeholder notes. Dispatched a subagent to
harvest the broader Robberto et al. 2012 (arXiv 1205.2727 = 2012AJ....144...83R,
"HST Imaging Survey of Low-mass Stars in Chamaeleon I", WFPC2 F547M/F631N[OI]/
F656N[Ha]/F673N[SII], GO 11983) jet+disk atlas, Figs 2-11 (SX Cha, CT Cha, HH 48,
WW Cha, Ass Cha T 2-16, CED 112 IRS 4, ...) - results pending. 520 systems, 2156
image records, 0 errors / 0 warnings.

2026-07-11 (T Cha NACO/SAM, user-directed). +6 VLT-NACO Sparse Aperture Masking
maximum-entropy image reconstructions of T Cha (Cheetham et al. 2015, arXiv
1502.05084 = 2015MNRAS.450L...1C, "Near-IR imaging of T Cha: evidence for
scattered-light disc structures at Solar system scales", Fig 2, 2x3 panels): L'
3.8um at 2010-03-14 / 2011-03-14 / 2012-03-08 / 2013-03-25, and Ks 2.18um at
2011-03-15 / 2013-03-26 (obs dates from the log table; H-band 2013-03-27 not in
Fig 2). Typed disk_scattered and labelled explicitly as DISC scattered-light
structure (the paper shows the NW+E "two point source" SAM signals are forward-
scattering from the highly-inclined disc, NOT the previously-claimed companion;
user flagged this). t-cha 3->9 images. 520 systems, 2162 image records, 0 errors.

2026-07-11 (Robberto 2012 Cha I HST jet+disk atlas - subagent harvest). Subagent
processed Figs 2-11 of Robberto et al. 2012 (arXiv 1205.2727 = 2012AJ....144...83R,
HST/WFPC2 GO 11983, F547M/F631N[OI]/F656N[Ha]/F673N[SII], obs 2009); read every
caption, VIEW-verified every crop, distinguished real features from CTE trails.
+9 panels (all disk_scattered): CT Cha [OI]+[SII] extended circumstellar emission
(Fig 4; "C2" label softened - the known background source, not a companion);
HH 48 F547M edge-on-disk scattered light (B) + [SII] HH flow (A) (Fig 6, existing
hh-48-ne); WW Cha [SII] extended shock / HH 915 (Fig 9). 3 NEW Cha I systems with
SIMBAD coords/mags: SX Cha (M1.5+M3 binary, [SII] jet protuberance, Fig 2), Sz 4
(=Ass Cha T 2-5, M4, resolved 0.15" close binary, Fig 3), CED 112 IRS 4 (=FM Cha,
HH 914 Ha+[OI] eastward knot, Fig 8). Skipped Fig 5 (NACO archival non-HST + dup),
Fig 7 Ass Cha T 2-16 (marginal FWHM), Fig 10 ESO-Ha 569 (below detection limit),
Fig 11 ESO-Ha 574 (done separately from Whelan 2014), Fig 1 (field map). 523
systems, 2171 image records, 0 errors / 0 warnings.

2026-07-11 (J11095340=FM Cha merge + Kurtovic-gallery coordinate audit, user-
directed). User flagged that gallery system J11095340 = 2MASS J11095340-7634255
(Kurtovic 2605.30023 Table 2), which SIMBAD resolves to FM Cha - the SAME object as
ced112-irs4 (= CED 112 IRS 4), just created for the jets task. MERGED j11095340
(ALMA disk) + ced112-irs4 (Robberto HST HH 914 jet) into a single system fm-cha
"FM Cha" (3 images; image files git mv'd to images/fm-cha/, old two systems removed).
Then audited coordinate completeness: 0 systems have null coords, but the 12
bare-J-number gallery systems revealed a systematic bug - 9 had ra/dec mis-parsed
from their 2MASS designation (HHMMSSss read as HH MM SSSS -> positions off by
degrees; a SIMBAD cone-search at the stored coords hit empty sky). Recomputed all 9
correctly from the 2MASS names and SIMBAD-verified each to <0.2": j04343128,
j04360131, j05080709, j160421-7, j16070854, j16090141, j16092697, j16102955,
j16140792. Renamed j16140792 -> V1098 Sco (its real name). Set valid resolvable
simbad ids on the 3 that had bare-J placeholders (j16000236 -> UCAC3 96-205752;
j16100501 -> 2MASS J16100501-2132318; j17110392 -> 2MASS J17110392-2722551; their
coords were already correct). 522 systems, 2171 image records, 0 errors / 0 warnings.

2026-07-11 (coordinate sweep + name cleanup, user-directed follow-up). SWEEP: parsed
every system whose name/simbad/alt encodes a position (85 systems) with a correct
2MASS/WISE parser and compared to stored coords; only 3 exceeded 5" and all 3 have
CORRECT stored coords (1RXS J1609 = RX J1609.5-2105 hit 0.16"; two HSCS quasars hit
0.16") - the flags were just coarse catalog-name precision (ROSAT/HSC). Conclusion:
the HHMMSSss mis-parse was fully contained to the 9 gallery systems already fixed;
no other coordinate errors. NAMES: renamed 31 raw-designation systems (long "2MASS
J..." / bare truncated J-numbers / a Gaia DR2 number) to shorter names - a common
name where one exists (j160421-7 -> RX J1604.3-2130 A, the famous shadowed disk),
else a literature-style JHHMM+/-DDMM moniker TRUNCATED from the 2MASS designation
(e.g. 2MASS J04124068+2438157 -> J0412+2438, matching the "J0412" the papers use;
first pass mistakenly ROUNDED giving J0413/J1609, corrected to truncation). Full
designations preserved in alt_names; simbad fields left SIMBAD-resolvable. No name
collisions. 522 systems, 2172 image records, 0 errors / 0 warnings.

2026-07-11 (short-name collision fix + J1612 recrop, user follow-up). User clarified
the short-moniker policy: keep number-based JHHMM monikers, BUT where two+ systems
share the same JHHMM RA prefix the short form is ambiguous, so don't use it for them.
Reverted 10 such systems to their full 2MASS names (moniker kept in alt_names):
J1608 (x3: 2MASS J16082324-1930009, J16083070-3828268, J16085324-3914401), J1609
(x3: J16090075-1908526, J16090141-3925119, J16092697-3836269), J1610 (x2: J16100501
-2132318, J16102955-3922144), J1612 (x2: J16120668-3010270, J16124373-3815031).
Short monikers retained only where the JHHMM prefix is unique. Also recropped the
2.2um K-band Q_phi panel of 2MASS J16120668-3010270 (sphere-k-qphi record) from
Ginski et al. 2025 (2506.05892) Fig 2 panel 2: the old crop had bled in panel 1's
right edge + the bottom ax label; the new crop is the clean single panel. 522
systems, 2172 image records, 0 errors / 0 warnings.

2026-07-11 (moniker convention clarified - restored). Maintainer clarified the
JHHMM+/-DDMM convention: J + first-4-digits-of-RA + sign + first-4-digits-of-Dec
(e.g. J1612-3010, J1612-3815), where the Dec half distinguishes objects sharing an
RA prefix. So the prior "revert colliding groups to full 2MASS" was an over-
correction; RESTORED the monikers on all 10: J1608-1930/-3828/-3914,
J1609-1908/-3925/-3836, J1610-2132/-3922, J1612-3010/-3815. All monikers are unique
full strings; full 2MASS designations remain in alt_names. 522 systems, 2172 image
records, 0 errors / 0 warnings.

2026-07-11 (naming-convention audit, user-directed). Swept all 522 system names for
format inconsistencies. Normalized 16 to the dominant conventions: catalog-prefix
SPACE (Sz113/Sz69/Sz73/Sz74 B -> Sz 113 etc. [24 Sz were already spaced]; MHO2/MHO6
-> MHO 2/6; SVS13A -> SVS 13A); IRS SPACE (BHR71 IRS1/2, GSS30 IRS3, Ced 110 IRS4,
Oph IRS43, R CrA IRS5N/7B -> "... IRS N", matching the spaced L1551 IRS 5 / Oph IRS
44 / Oph IRS 48); and 3-letter constellation abbreviations for Bayer names (gamma
Ophiuchi -> gamma Oph, pi1 Gruis -> pi1 Gru, matching beta Pic / eta Crv / kappa
And / alpha Cen A) with the full genitive kept in alt_names. Left intentionally:
ESO Halpha 569/574 keep the Halpha symbol (standard for the emission-line survey
name, not a Bayer letter). Post-audit no prefix space splits or double/trailing
spaces remain. 522 systems, 2172 image records, 0 errors / 0 warnings.

2026-07-11 (duplicate-system merge sweep + health_check.py). Built backend-data/
health_check.py - permanent cross-system integrity tool encoding every invariant
this session's bugs taught: (1) duplicate systems via identical simbad ids AND
coordinate-pair proximity (<8", allowlist for true close pairs hk-tau/hk-tau-b,
mho-1/mho2, sz-65/sz-66); (2) coord-vs-designation consistency (the 2MASS
HHMMSSss centisecond parser, 60" allowance for coarse 1RXS/HSCS/RX-J names);
(3) naming conventions (prefix/IRS spacing, Bayer 3-letter abbrevs, bare-J names,
moniker completeness, name collisions, whitespace); (4) placeholder-notes backlog
as a non-fatal warning. First run found SEVEN duplicate systems beyond the earlier
FM Cha case - the same star ingested twice with coverage split across entries.
All merged (survivor <- dupe, images git mv'd + ids reprefixed, alt_names unioned):
gamma-oph <- hd-161868 ("gamma Oph"; also dropped a same-paper duplicate - Han 2026
MIRI F2550W was held on BOTH entries; fixed bogus HR 6630 alt -> HR 6629);
gw-lup <- sz-71 ("GW Lup" = Sz 71, AGE-PRO record consolidated); pds-66 <- mp-mus
("MP Mus", 16 images now together); tyc-9340-437-1 <- cp-72-2713 ("CPD-72 2713");
v606-ori <- so-1274 ("V606 Ori" = SO 1274); j16070854 <- lup-160708 ("J1607-3914",
Martinien 2026 edge-on record consolidated); rx-j1604-3-2130 <- j160421-7
("RX J1604.3-2130 A", 9 images - the famous shadowed disk had been split 7+2).
health_check.py added to HANDOFF quick-start (run after every batch that adds/
renames systems). Surfaced backlog: 123 systems still carry AUTO-CREATED
placeholder notes. Frontend search confirmed to index alt_names (renames stay
findable). 515 systems, 2171 image records, 0 errors / 0 warnings.

2026-07-12 (9k-frontier ladder triage + freeze lift, apply batch 1). User challenged
the papers_explored 964/9,943 ratio; ran the full title->abstract->conclusion
iff-ladder over ALL 8,986 unexplored frontier papers (6 title/abstract agents +
13 conclusion agents, ADS-OA-first fetching after arXiv rate limits, ar5iv third
route). Funnel: 7,117 FAIL_TITLE (79%), 593 FAIL_ABSTRACT, 84 fail-conclusion/
no-abstract, 165 deferred non-OA classics, 1,027 PASS (confirmed imaging papers;
488 all-held targets, 539 with new targets; ~95 SIMBAD-confirmed genuinely-new
names in the coarse pass). All dispositions folded into paper_finder_state
(485->9,471) -> papers_explored 9,945/9,945 = COMPLETE triage of the harvested
universe. Stage-4 figure harvest running in waves (4+2 agents so far; manifests
parked in scratchpad triage9k/parked/). WRITER CONFIRMED the release regeneration
-> freeze lifted; applied batch 1: fx manifest (14: AGE-PRO USco Band 7 1.05mm
x10, GM Aur SMA CO 3-2/2-1 Hughes 2009, HD 163296 VLA 7mm + PdBI 12CO Isella
2007) + s4b (51) + s4d (64). +21 NEW systems: quasar hosts J0148+0600 (z=5.977),
ULAS J1120+0641 (z=7.085, most distant atlas object), J159-02 (z=6.381) from
EIGER V (Yue 2024) + 4 Zakamska 2019 HST ERQ/type-2 hosts; embedded protostars
NGC 1333 IRAS 2A/4A/4B, VLA 1623, TMC-1 (Persson 2016, van 't Hoff 2020);
rho-Oph YSOs GY 263 (eDisk cavity disk), Oph IRS 54, Elias 29, GSS 30 IRS 1
(Beckford 2008 UKIRT polarimetry); naked-eye mid-IR debris zeta Lep, HD 71155,
beta UMa, alpha CrB, alpha Sgr (Moerchen 2010). Cross-paper depth: HR 8799 +13
epochs/bands (SPHERE commissioning 2014 set, Currie 2011/2014 multi-telescope
L'/Ks/J, Skemer 2012 LBT first-light H + 3.3um; first 3.3 + 4.05 um records),
IM Lup 4-epoch spiral-winding series (Yoshida 2025 NatAs), HD 142527 4-band ALMA
full-Stokes polarimetry (Ohashi 2025 NatAs), HD 163296 CHARA/MIRC-X 4-epoch
inner-disk reconstructions (Setterholm 2025), PDS 70 12 molecular maps
(Rampinelli 2024) + 7-epoch SPHERE Qphi series (Ma 2024) + JWST/NIRISS AMI b&c
(Blakely 2025), Flying Saucer EODS tomography suite (Dutrey/Guilloteau 2025),
eDisk IRAS 04166+2706 7-panel set. Fixes: oph-irs-44 coords 4.8"->SIMBAD; 7
slash-epochs normalized; gy-263/oph-irs43 allowlisted (true 6.9" pair). 20/21
new systems SIMBAD-enriched. 542 systems, 2421 records, 0 errors / 0 warnings;
papers_in_atlas 683. Batch 2 (s4a 118 + s4c 60 crops) lands before the new pin.

2026-07-12 (refuted companion + batch 3). Added HD 131399 as a refuted-companion
system (the maintainer's directed ask now that refuted companions are in scope):
HD 131399 Ab, claimed by Wagner et al. 2016 (Science, VLT/SPHERE) as the first
planet imaged within a hierarchical triple, was shown to be a slow-moving
background star by Nielsen et al. 2017 (Gemini/GPI common-proper-motion + SPHERE/
Keck reanalysis). Two image records: Wagner Fig 1E discovery composite (planet b +
A/B/C) and Nielsen Fig 1 GPI 4-epoch cADI refutation; planets[] status refuted,
Nielsen as extra_papers (hollow-marker system like yses-2/cvso-30). Correction from
VIEWing the sources: the 2017 A&A letters (Pecaut - Am-star nature; Lagrange -
HARPS stellar companion) are STAR characterization, NOT imaging refutations of Ab;
there is no separate Wagner follow-up. Batch 3: the s4c cross-paper crop images had
been lost when the prior session's scratchpad (5c2a9753) expired before they were
applied; regenerated all 69 panels via a re-crop agent using the recovered manifest
as an exact recipe (ADS-PUB_PDF empty for the 2025-26 preprints -> export.arxiv.org
mirror; every crop VIEW-verified). Systems touched: PDS 70 (873um full-pol + B3/4/6
continuum, Liu 2026), PDS 66 (SiS isotopologues, Yoshida 2026), MWC 480 (ALMA B7/6/
3 + VLA Ka/X, Shi 2026), HD 163296 (Law CS J=2-1..10-9 + C34S/H2CS/H2C34S 11-line
ladder incl. an SMA record + Izquierdo HCN/C2H CPD candidate), T Tau (Beck
periastron 4 continuum epochs + 350 GHz extended), HD 131835 (ARKS SPHERE+ALMA
overlay), IRAS 04166/04169 (Sato B213 pol; Han eDisk XVII mm/cm/line suite),
Fomalhaut (Kalas STIS cs1/cs2 + Chittidi ALMA ansae/full mosaics), HD 100453 (Booth
8 COMs incl. first 13CH3OH in a Class II disk), V960 Mon (Weber environment), HD
100546 (Rampinelli first resolved water vapor). Lesson banked: apply/commit crop
waves the SAME session; never park unapplied crops across a session boundary. 600
systems, 2610 image records, 0 errors / 0 warnings; health_check OK; papers_in_atlas
712. Re-pinned the release for the manuscript.

2026-07-11 (exploration round: 4 parallel agents, STILL-OPEN queue cleared).
Forward axis first: fresh_papers --days 4 -> 53 submissions, 0 hits (quiet).
Retrospective round on the queued veins, +121 records +6 systems (2171->2292,
515->521):
(1) Hom et al. 2024 GPI Paper II (2402.00214 = 2024MNRAS.528.6959H): +10 GPI
total-intensity pyKLIP records (8 H + 2 K1), per-target epochs 2015-2018 -
fills the total-intensity axis beside the held Esposito 2020 polarized GPI.
(2) MAPS line-emission maps (Law 2021 MAPS III, 2109.06210 = 2021ApJS..257....3L):
+35 = 5 disks x 7 tracers (12CO/13CO/C18O 2-1, C2H, HCN 3-2, HCO+ 1-0, CS 2-1)
moment-0 maps, survey=MAPS - the atlas's first molecular-tracer axis.
(3) AGE-PRO Oph+USco (Ruiz-Rodriguez 2025 2506.10731 + Agurto-Gangas 2025
2506.10735 - agent corrected the brief's Trapman guess): +37 (12CO/13CO mom-0
galleries + 3 missing continuum), 4 NEW systems (ISO-Oph 161, J1605-2023,
J1611-1918, BV Sco); continuum for the other 17 already held from AGE-PRO I,
correctly skipped as same-dataset; 1 cloud-mush 13CO dropped after VIEW.
AGE-PRO now COMPLETE 30/30. Follow-up available: Agurto-Gangas Fig 8 Band 7.
(4) Pre-ALMA mm classics: +39, 2 NEW systems (WL 18, DoAr 24 E). SMA 880um Oph
galleries (Andrews 2009 x9 + 2010 x8, 2005-2009, pre-ALMA cavities of SR 21/
SR 24S/DoAr 44), CARMA 1.3mm (Isella 2009 x11, per-track dates), PdBI landmarks:
LkCa 15 FIRST cavity image + MWC 480 (Pietu 2006), AB Aur ring + sub-arcsec 13CO
(Pietu 2005), GG Tau 'ring world' (Guilloteau 1999, obs 1997) and THE FIRST
GG Tau ring image (Dutrey 1994, obs 1992-93; scanned A&A pages via ADS - the
atlas's earliest mm epoch). Alias cross-matches coordinate-verified (GSS 39=
elias-27, VSSG 1=elias-20, WSB 60=iso-oph-196); zero duplicate systems created
(health_check clean after every batch). Isella Fig 2 GM Aur/TW Hya/HD 163296
panels skipped (re-published SMA/PdBI data; ingest from originals later).
521 systems, 2292 image records, 0 errors / 0 warnings.

2026-07-11 (internal review round-2: data reconciliation + release pinning).
Ingestion HALTED; two in-flight agent manifests parked in scratchpad (14 fx_
crops: AGE-PRO USco Band 7 x10, GM Aur SMA CO x2, HD 163296 VLA 7mm + PdBI CO).
TASK 2 (epoch regression, blocking): coverage had fallen 2068/2171 (95.2%) ->
1939/2292 (84.6%). Root cause: the Kurtovic 2026 (151 rec) and Vioque 2026 (97)
gallery batches were ingested WITHOUT epochs (epoch-at-ingestion rule violated);
git history proves the fields were never present - the facet-normalization pass
stripped nothing. Backfilled 227 records via epoch_archives.py alma (paper-tex
ALMA project codes -> TAP ivoa.obscore; 215 code-tier + 12 cone-tier; all with
provenance entries) -> 2166/2292 = 94.5%. ESO mode found 0 (recent SPHERE data
not yet public in obscore). 126 residue documented (21 uncovered gallery, 11
REASONS multi-config combos, ~90 pre-existing hard tail). Plus 5 SOURCE-VERIFIED
epoch corrections on existing records: v2149-ori '2001 Dec'->2020-02-16 (old
value was the Koehler 2006 astrometric epoch, not the SPHERE obs; Valegard
Table 1), hd-294260 2020-03-04->2020-02-18 (Table 1), hd-163296 PdBI 1.3+2.8mm
'2001-2003'->'2003-2004' (Isella 2007: '2003/2004 winter season'; old value was
the VLA range), gm-aur_sma2009 '2005-2006'->'2005-11' (Hughes 2009: Nov 5+26).
TASK 3 (granularity): per-LINE records STAND - molecular lines are physically
distinct tracers (chemistry/layers/radii), consolidating would cram 7 tracers
into one crop. Added content=continuum|line to ALL 2292 records (2145/147; regex
classifier incl. narrow-band Halpha/[SII]/Paalpha and jet emission-line images),
REQUIRED on disk_mm in validate.py, rule documented in data/README.md. Scope
statement: one record per continuum band per instrument per epoch; one record
per spectral line for line data products.
TASK 4 (spot-checks): (a) 114-426 NOT over-split - 12 distinct NIRCam filters
(water-ice science is per-band) + RGB composite + 4 NICMOS 1997 + NICMOS 1998
re-display; every record a distinct filter x epoch x instrument. (b) beta Pic
mm = 9 records; Dent 2014 held; Matra 2017/2019 + Wilner 2011 SMA held only via
the REASONS re-reduction - originals QUEUED post-release in known_missing.
(c) facility 37->36 fold = raw 'PdBI' facet merged into IRAM:Interferometer
(same physical facility, AAS keyword form) - correct; set-diff across builds
shows no facility lost; canonical count 37.
ALSO: 52 cited notes applied from the pre-halt agent (placeholder backlog
123->71; every claim carries an inline citation grounded in the record's own
paper; agent's paper-target sanity check also surfaced 2 of the epoch errors
above). RELEASE STATS BLOCK: 521 systems / 2292 image records / epochs 2166
(94.5%) / categories prot 318 + deb 106 + evo 19 + qso 20 / content 2145
continuum + 147 line / companion hosts 91 (non-refuted 88; 107 companions) /
papers_in_atlas 657 builder (664 distinct refs) / papers_explored 964 / papers_
known 9943 / 37 AAS facility keys / 71 instrument families. This commit = THE
paper release snapshot; no ingestion until the writer confirms regeneration.

2026-07-11 (HD 34282, user-directed). Added ONLY panel (a) of Fig 1 of Quiroz et al.
2022 (arXiv 2111.12708 = 2022ApJ...924L...4Q, "Improving Planet Detection with Disk
Modeling: Keck/NIRC2 Imaging of the HD 34282 Single-armed Protoplanetary Disk"): the
Keck/NIRC2 vortex L' 3.8um KLIP/ADI reduction (6 KL components) of the single-armed
disk (ring + blob + spiral), obs UT 2017-02-07 (program C328, PI Ruane). This is the
ORIGINAL-paper reduction of the same NIRC2 data the atlas already holds re-reduced by
Wallack et al. 2024 (Fig 4) - both kept per cross-paper method-diversity policy.
Panels (b)-(f) (SPHERE Qphi, contours, best-fit models, residuals) skipped per user
instruction. hd-34282 12->13 images. 522 systems, 2172 image records, 0 errors.

2026-07-11 (infra: UX + deploy improvements, Fable 5 session). Three
user-facing improvements to the viewer, verified in a live preview: (1) deep
links now carry the image index — #s=<id>&i=<n>, written by showImg() as you
navigate (arrows/swipe/keyboard) and restored at boot, so the exact panel on
screen is always shareable (hash ownership moved from openDetail to showImg);
(2) detail images carry a meaningful alt ("name — wavelength label") instead
of alt=""; (3) an image 404 (stale cached data.js after an id rename, missing
offline file) now swaps in a translated notice (new d_imgerr key, all 12
languages) instead of a broken-image icon. Deploy hardening: pages.yml stamps
every frontend asset URL with the commit SHA at artifact-build time
(cache-busting; repo copy stays clean for offline file:// use), so a Pages
visitor can never mix a cached app.js with a fresh data.js inside the 10-min
HTTP cache window. frontend/README rows added for all of the above.

## 2026-07-11 — bibcode verification fix (v1788-ori)

export_bibtex.py flagged a first-author mismatch on 2007IAUS..240..250T
(record said "Tokovinin", ADS says "Thomas"). ADS check: that bibcode is
Thomas et al. 2007, "Multiplicity of Herbig Ae/Be Stars" (IAU Symp. 240,
p. 250) — the right paper for the HD 37411 (Herbig Ae/Be) triple, and the
one Valegard et al. 2024 (2024A&A...685A..54V) cites for the companions.
Tokovinin's only IAUS 240 contribution is p. 306 (tidal dissipation),
unrelated. Fixed first_author -> "Thomas" on planets B and C in
data/systems/v1788-ori.json; bibcode kept. validate/build clean;
export_bibtex.py re-run: 0 verification problems.

2026-07-11 (epoch audit, user-reported TWA 7). User caught TWA 7's second
STIS record showing the same 2019 dataset as the first but dated "2011-2021"
— the harvest had folded the 2011 STIS *spectroscopy* visits (prop 11616)
and the re-reduction survey's span into the epoch. MAST-verified every
record citing the Ren 2023 "Debris Disk Color" survey (23 targets, queried
by proposal id: GO-13381/15218/12228/13786 + the beta Pic and HD 141569A
multi-program combos) plus the Schneider 2014 / Stark 2023 STIS relatives:
12 corrections, dominated by the publication-year leak ("...-2023" spans on
2010-2015 data). Rule added to HANDOFF: re-reductions of the same dataset
carry the same epoch. Second pass: normalized all 319 prose-form epochs
("2019 Feb 3", "2010 Apr", "2015-01 to 2015-02") to ISO policy forms
(YYYY-MM-DD / new YYYY-MM tier / YYYY), spot-checked, validate 0/0;
epoch coverage 94.5%.

2026-07-11 (all-systems epoch sweep, follow-up to the TWA 7 catch). Hard
sanity scan of all 2292 record epochs (year ranges, span order, epoch vs
publication year, conservative instrument commissioning windows) found ONE
impossible date: HR 4796A NICMOS F222M "2009-08-12" (NICMOS ended science
in 2008; the harvest had grabbed the paper's NACO date) -> 2005-05-09 per
MAST prop 10167. Soft scan (same instrument + wavelength, different papers,
disagreeing epochs) flagged 42 groups; 37 are genuinely multi-epoch or
different programs (correct), 4 were wrong and fixed after MAST/tex
verification: AU Mic Schneider14 STIS "1998-2013" -> 2010-2011, HD 61005
Schneider14 STIS -> 2011, CY Tau CARMA 1.3mm "2009" -> 2007-2011 (Perez 15
log spans 2007-2011), PDS 66 Schneider14 6-roll "2012" -> 2011 (no 2012
visit exists). AGE-PRO per-target spans left as-is (deliberate archival+LP
combinations). validate.py now enforces epoch sanity permanently: ISO forms
only, years within 1980-2027, ordered spans, and epoch must not postdate
the paper (all four negative-tested).

## 2026-07-11 — facility facet keys aligned with AAS keywords

facility_map.py brought in line with the paper's \facilities audit (Overleaf
ms.tex 1c8ee62 + f007bcc, against the official AAS facility-keyword list):
WHT -> ING:Herschel (ING 4.2m William Herschel Telescope, not the space
observatory) and CMO-2.5m -> SAI-2.5m via new FAC_TABLE entries. Bug fix:
'Gemini-GMOS/CFHT' (GU Psc b discovery, Naud et al. 2014) resolved its Gemini
half to Gemini:Gillett; the paper's survey used GMOS-S on Gemini SOUTH
(verified from the arXiv abstract), so the Gemini-South heuristic now also
keys on 'gmos-s'. Deliberate display-level departures from the paper are now
documented in the module docstring: the facet keeps one grouped 'VLT' chip
(paper counts per unit telescope, VLT:Antu/Melipal/Yepun) and 'OVRO' stays
short (no AAS keyword for the mm array; paper spells it out). Full-dataset
diff: exactly 3 records changed fac_keys; chips 37 -> 37; validate 0/0;
build census audits green.

## 2026-07-14 — Moment-map completeness harvest (batch 1)

Protoplanetary/embedded-disk systems that carried ALMA *continuum* records but no
*spectral-line* (moment-map) records were systematically back-filled. Rationale
(maintainer): a resolved disk with published ALMA continuum almost always has
published CO/isotopologue moment maps somewhere in the literature. ~186 candidate
systems were split across 6 parallel agents; each PDF-triaged the already-cited
papers first (fast path), and only when the cited paper was continuum-only or
model-only did it run a single bounded ADS search for the dedicated kinematics
paper, then cropped the published moment-0 (integrated intensity) and/or moment-1
(velocity field) panels from the authors' source figures.

Result: **+85 VIEW-verified `disk_mm`/`content:line` records across 51 systems**,
from **20 new source papers** (ADS-verified titles + bibcodes) plus 14 already-held
papers reused. Notable fallbacks: the eDisk *overview* (Ohashi 2023, 2306.15406)
only shows moment maps for its demo source R CrA IRS7B, so the per-target eDisk
papers were used instead — eDisk V (Sai, Ced110 IRS4), VI (Aso, IRAS 16253-2429),
IX (Sharma, R CrA IRS5N), XI (Gavino, BHR71 IRS2), XVI (Santamaría-Miranda,
GSS30 IRS3). AGE-PRO Lupus/Ophiuchus (Deng/Zhang 2025) and DESTINYS (Huang 2022)
supplied several more. Three agent-reported author attributions were corrected
against ADS at ingestion (Oph IRS 48 → Bruderer 2014 not van der Marel; R CrA
IRS5N → Sharma not Sai; BHR71 IRS2 → Gavino not Kido).

**24 systems flagged `needs_paper`** — the cited paper is continuum/scattered-light
only and the bounded search found no clean resolved-disk moment map, or the CO is a
formal non-detection (e.g. Elias 2-32 = Oph 4, CIDA 9), or only jet/outflow-scale
contour maps / PV diagrams exist (HH 212). These, plus a deferred **batch 2 of ~111
systems** that need per-target kinematics-paper searches, are the remaining line-map
gap. Atlas after batch 1: **606 systems / 2793 image records / 737 papers**,
0 validate errors, 0 health-check findings.

## 2026-07-14 — SONS survey completion + moment-map batch 2

**SONS (JCMT/SCUBA-2 850 um debris discs, Holland et al. 2017).** The atlas held
only ~34 SONS targets. Fetched the arXiv e-print (1706.01218) figure set and cropped
the 850 um S/N image panel from the survey appendix montages (Figs A1-A14) for every
detected target not yet covered: **+21 records** — 16 new debris systems seeded with
SIMBAD coordinates (HD 6798, HD 8907, tau Cet, 38 Ari, beta Per, HD 22179, HD 25457,
GJ 322, sigma Boo, HD 141378, 44 Ser, 37 Her, 39 Her, HD 212695, 39 Peg, plus lambda
Boo) + SONS records appended to 5 existing systems (HD 13161, HD 15745, HD 35841,
TWA 7, HD 92945). Two integrity catches during VIEW-verification: the paper's Fig A4b
caption reads "HD 19536" but the panel itself is labelled **HD 19356 (beta Per)** — the
panel is ground truth, so the target/coords were set to HD 19356; and the auto-generated
sid `hd-125162` collided with the pre-existing lambda Boo system (which lacked its HD
number in any name field, so the matcher missed it) — the original was restored from git
and the SONS record appended alongside its Herschel/PACS record, with "HD 125162" added
to its alt_names to prevent a recurrence.

**Moment-map batch 2 (the continuum-survey-only tail).** The 111 protoplanetary/embedded
disks with ALMA continuum but no line record whose cited papers were pure continuum
surveys (DSHARP, Long, Vioque TD, Kurtovic, Cieza) were worked by 6 parallel agents,
each PDF-triaging the cited papers then running a bounded ADS search for a dedicated
kinematics paper. Yield: **+40 VIEW-verified line records across 20 systems** from 12 new
source papers (RW Aur multiple-flyby CO, Rodriguez 2018; Oph IRS 67 circumbinary C17O /
H13CO+, Artur de la Villarmois 2018; EX Lup, Hales 2018; edge-on ZZ Tau IRS, Hashimoto
2021; V883 Ori ASSAY C17O, Lee 2024; VLA 1623W FAUST C18O, Mercimek 2023; CI Tau 13CO,
Rosotti 2021; SR 24S, Pinilla 2017; V892 Tau, Long 2021; HD 97048 HCO+/12CO, Booth 2019
/ van der Plas 2017; HD 142666, Stapper 2023; ONC 216-0939, Diaz-Berrios 2024; HP Cha /
Sz Cha, Woelfer 2023; and Lupus survey II resolved 12CO galleries, Ansdell 2018). The
remaining ~91 batch-2 systems are `needs_paper`: their disks are unresolved or gas-faint
in the survey data, the CO is a formal non-detection, or only outflow/envelope-scale or
channel-map/PV products exist (no clean resolved-disk moment map). Combined with batch 1,
the moment-map completeness pass added 125 line records across 71 systems. Atlas after:
**621 systems / 2854 image records / 749 papers**, 0 validate errors, 0 health findings.

## 2026-07-16 — Classic resolved submm/mm debris-disk discovery images (paper-audit gap fill)

A paper audit flagged that the first-generation resolved submm/mm images of nearby
debris disks were missing from the atlas. Each candidate was ADS-verified against its
source (bibcode, authorship, and — decisively — whether an authors' e-print exists),
never from memory:

- **eps Eri** — Greaves et al. 1998 (ApJL 506, L133; astro-ph/9808224): the discovery
  JCMT/SCUBA 850 um image of the epsilon Eridani dust ring. Author e-print carries
  `fig1.eps`; cropped and rotated upright. Obs Aug 1997-Feb 1998 -> epoch 1997-1998.
- **Vega** — Koerner et al. 2001 (ApJL 560, L181; astro-ph/0109424): first mm-wave
  aperture-synthesis image (OVRO Millimeter Array, 3", ring arc at ~95 au). Cropped the
  "1.3 mm Continuum" panel of `f1.eps`. Obs fall 1999-spring 2001 -> epoch 1999-2001.
- **Vega** — Wilner et al. 2002 (ApJL 569, L115; astro-ph/0203264): IRAM PdBI 1.3 mm
  image resolving two dust concentrations. Cropped the 3-panel observed strip `f1.eps`
  (the `f2/f3` model images were excluded). Obs 2001 Feb 14/18, Mar 18/27 -> epoch 2001-02-14.

**Deferred** (recorded in `data/paper_finder_state.json`): Holland et al. 1998 (Nature 392,
788 — the SCUBA 850 um discovery images of Fomalhaut / beta Pic / Vega) and Zhao et al. 2024
(RAA 24, 065010 — MWC 480 gas-kinematics planet-signature maps). Neither has an arXiv/open
author e-print, so the atlas crop-source rule (authors' e-print figures, never journal
typesetting) cannot be met; they join the deferred non-OA classics bucket. Fomalhaut/beta Pic
already carry modern ALMA + SCUBA-2 SONS imaging, Vega's mm structure is now represented via
Koerner 2001 + Wilner 2002, and MWC 480 already carries seven MAPS moment-map line records.
Atlas after: 621 systems / 2857 image records / 752 papers, 0 errors / 0 warnings.

## 2026-07-16 — Zhao 2024 MWC 480 kinematic-signature maps

Ingested Zhao et al. 2024 (RAA 24, 065010): **+6 line records** into `mwc-480` —
Fig. 2 moment-0 and Fig. 4 fitted line-of-sight velocity maps for 12CO/13CO/C18O (2-1),
the observational basis of the paper's rotational/radial/vertical flow decomposition
probing kinematic planet-formation signatures. The data are a re-analysis of archival
MAPS observations (2018.1.01055.L), so epoch 2018, matching the atlas's existing MAPS
records (cross-paper re-reductions are in scope by policy). One adjudication: Fig. 2
panel (b)'s printed sublabel reads "12CO", but the caption, the colorbar scale, and the
correctly-labelled (b) panels of Figs. 3-4 identify the column as 13CO — recorded as
13CO with the figure typo noted on the record. Atlas after: 621 systems / 2863 image
records, 0 errors / 0 warnings.
