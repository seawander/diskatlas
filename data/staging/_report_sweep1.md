# Sweep-1 report — famous debris disks, dedicated ALMA papers (metadata-only)

Date: 2026-07-06. Budget: 14 WebSearches, 14 used. No crops, no merge/build, no seed edits.
Scope of edits: ONLY `data/systems/<id>.json` of the 12 assigned targets (images[] append +
last_updated bump) and this report.

All 12 targets already carry REASONS/ARKS survey mm crops; what was missing was each system's
landmark single-target ALMA paper. Added one pending record (`file: null`, `survey: null`,
`credit: null`) per system. Every arXiv id below was verified against arxiv.org/ADS links in
search results (title match confirmed from snippets).

## Added records (12)

| system | image_id | paper | arXiv | band / wavelength | bibcode |
|---|---|---|---|---|---|
| hd-32297 | hd-32297_alma2018 | MacGregor+2018, ApJ 869, 75 (mm halos, HD 32297 & 61005) | 1812.05610 | Band 6, 1.3 mm | 2018ApJ...869...75M |
| hd-61005 | hd-61005_alma2018 | MacGregor+2018, ApJ 869, 75 (same paper as above) | 1812.05610 | Band 6, 1.3 mm | 2018ApJ...869...75M |
| hd-15115 | hd-15115_alma2019 | MacGregor+2019, "Multiple Rings of Millimeter Dust Emission..." | 1905.08258 | Band 6, 1.3 mm | (null; journal "ApJL" `_verify`) |
| hd-92945 | hd-92945_alma2019 | Marino+2019, MNRAS 484, 1257 (gap in broad disc) | 1901.01406 | Band 7, 0.86 mm | 2019MNRAS.484.1257M |
| hd-206893 | hd-206893_alma2020 | Marino+2020, MNRAS 498, 1319 (disc + gap at 74 au) | 2010.12582 | Band 6, 1.3 mm (`_verify` band) | 2020MNRAS.498.1319M |
| hd-181327 | hd-181327_alma2016 | Marino+2016, MNRAS 460, 2933 (exocometary gas + ring) | 1605.05331 | Band 6, 1.3 mm + CO 2-1 | 2016MNRAS.460.2933M |
| hr-4796a | hr-4796a_alma2018 | Kennedy+2018, MNRAS 475, 4924 (narrow ring) | 1801.05429 | Band 7, 880 um | (null, not shown) |
| hd-10647 | hd-10647_alma2021 | Lovell+2021, MNRAS 506, 1978 (q1 Eri, asymmetric disc) | 2106.05975 | Band 6/7, 1.3 mm | 2021MNRAS.506.1978L |
| hd-131835 | hd-131835_alma2019 | Kral+2019, MNRAS 489, 3670 (imaging [CI]; shielded secondary disc) | 1811.08439 | Band 8, [CI] 492 GHz (609 um) (`_verify` author/band) | (null) |
| hd-129590 | hd-129590_alma2020 | Kral+2020, MNRAS 497, 2811 (belt survey; CO detected) | 2005.05841 | Band 6, 1.3 mm + CO 2-1 | 2020MNRAS.497.2811K |
| hd-105 | hd-105_alma2018 | Marshall+2018, "Comprehensive analysis of HD 105..." | 1811.06440 | Band 6, 1.3 mm archival (`_verify` journal/year) | (null) |
| 49-cet | 49-cet_alma2017 | Hughes+2017, ApJ 839, 86 (CO 3-2 + continuum profiles) | 1704.01972 | Band 7, ~0.85 mm + CO 3-2 | 2017ApJ...839...86H |

## "No resolved ALMA image" notes added

None — every target has a published resolved (or at least detected+modelled) ALMA observation;
no `coverage:` notes were written.

## Caveats / follow-ups for the orchestrator

- `_verify: true` set on 4 records (hd-15115 journal; hd-206893 band/wavelength; hd-131835
  first-author "Kral" + Band 8 inferred from [CI] 492 GHz, confirm vs. tarball; hd-105
  journal/publication year — arXiv posted 2018-11, may be published 2019).
- hd-32297 and hd-61005 share one tarball (1812.05610) — one fetch serves two crops.
- hd-129590 (Kral+2020) is a detection-survey image (compact belt, Band 6); crop value is modest
  but it is the only dedicated non-survey ALMA paper found for it (other hits: ARKS 2605.03009,
  scattered-light 1706.04624, modelling 2304.06074).
- 49-cet: memory said 1704.01973; the verified id from the arxiv.org link is **1704.01972** — use that.
- hd-105.json still carries the `AUTO-CREATED from staging - fill metadata & coords` note
  (untouched; coords/mags appear present, sptype/dist fields worth an eventual pass).
- Did NOT spend remaining budget on coverage_todo big names (GW Ori, HD 98800, GG Tau...) —
  the last 2 searches were needed to disambiguate hd-105 (results conflate with HD 105211)
  and hd-129590.

## Search log (14)

1. HD 32297 ALMA -> 1812.05610 (also covers HD 61005)
2. HD 61005 ALMA -> same, 1812.05610 confirmed independently
3. HD 15115 ALMA MacGregor -> 1905.08258 (2019, rings+gap); older SMA 1501.05962 skipped
4. HD 92945 ALMA Marino -> 1901.01406
5. HD 206893 ALMA Marino -> 2010.12582 (also saw Nederlander+2021 2101.08849, not added)
6. HD 181327 Marino 2016 -> 1605.05331
7. HR 4796A Kennedy 2018 -> 1801.05429
8. q1 Eri Lovell 2021 -> 2106.05975
9. HD 131835 Hales/Kral -> 1811.08439 (Kral [CI] imaging; no separate Hales imaging paper surfaced)
10. HD 129590 resolved ALMA -> inconclusive (survey papers only)
11. HD 105 Marino -> conflated with HD 105211, no id
12. 49 Ceti Hughes 2017 -> 1704.01972
13. HD 105 Marshall archival ALMA -> 1811.06440
14. HD 129590 CO Kral -> 2005.05841
