# Batch P1 report — edge-on disk ingest (2026-07-06)

Scope: 2008.06518 (Villenave+2020 survey Fig. 1), 2204.00640, 2309.07040,
2302.01949, 2002.05723 (COCONUTS-1 Fig. 1), 2107.02805 (COCONUTS-2 image fix).
29 crops, 13 new systems, 12 coords added, 4 stubs in `backend/seeds/scattered3.py` fixed.
No merge/build run (per concurrency protocol).

## Paper identities (all verified from source .tex; journals from .bbl of citing papers in _sources)

| arXiv | Paper | Journal | bibcode |
|---|---|---|---|
| 2008.06518 | Villenave+2020 "Observations of edge-on protoplanetary disks with ALMA. I. Results from continuum data" | A&A 642, A164 | 2020A&A...642A.164V |
| 2204.00640 | Villenave+2022 "A highly settled disk around Oph 163131" | ApJ 930, 11 | 2022ApJ...930...11V |
| 2309.07040 | Duchêne+2024 "JWST imaging of edge-on protoplanetary disks. I. Fully vertically mixed 10 μm grains in the outer regions of a 1000 au disk" (target = Tau 042021) | AJ 167, 77 (*from memory, high conf. — not found in corpus bbls*) | 2024AJ....167...77D |
| 2302.01949 | Villenave+2023 "Modest dust settling in the IRAS04302+2247 Class I protoplanetary disk" | ApJ 946, 70 | 2023ApJ...946...70V |
| 2002.05723 | Zhang+2020 "COol Companions ON Ultrawide orbiTS (COCONUTS). I. A High-Gravity T4 Benchmark around an Old White Dwarf..." | ApJ 891, 171 | 2020ApJ...891..171Z |
| 2107.02805 | Zhang+2021 "The Second Discovery from the COCONUTS Program: ..." | ApJL 916, L11 | 2021ApJ...916L..11Z |

## ⚠ Deviation: 2204.00640 "Figs 11 AND 14"

The brief asked for Figs 11 & 14. In the source (and published) numbering these are
**Fig. 11 = pebble-accretion growth-timescale contour plot** (`dtgplotv14_100AU_R0.05.png`)
and **Fig. 14 = the SED** — *not images of the disk* (verified by eye; views kept as
`images/_sources/_views/p1_oph_fig11dtg.png` / `p1_oph_fig14sed-1.png`). Figure numbers were
presumably garbled upstream. I instead cropped the paper's signature imagery, **Fig. 1**
(super-resolution 1.3 mm continuum, left panel + labeled ring/gap zoom, right panel) →
`oph-163131_alma2022`, `oph-163131_alma2022-zoom`. If the user really wants the two plots,
they are one-manifest jobs away.

## Job 1 — EdgeOn-ALMA-2020 (Villenave+2020 Fig. 1 = Figures/Images_vertical.pdf)

All 22 disk panels cropped (12 sources; panel-label ↔ file match verified on contact
sheets `_views/p1_check_primaries.png` / `p1_check_extras.png`):

- Primary `<sid>_edgeon-alma2020` = Band 7 (0.89 mm) panel; **Oph 163131's single panel
  is Band 6 (1.3 mm)** — its seed/staging metadata say Band 6.
- Extras via staging only: `-b4` (2.06 mm; 8 sources) and `-b6` (1.3 mm; Tau 042021, HH 30).
- **HK Tau B panel → existing system `hk-tau`** (disk around the B component; wavelength_label
  says so). NOT a new system. Its record label is set in `p1-edgeon-alma2020-b7hk.json`.
- Figure label "HH 48" = paper's adopted name **HH 48 NE** (Table 1) → system `hh-48-ne`.

## New systems (13) — regions/categories for merge shells (also encoded in seeds + coords_todo_batchP1.txt)

| id | name | simbad (coords_cache key) | region | categories |
|---|---|---|---|---|
| tau-042021 | Tau 042021 | 2MASS J04202144+2813491 | Taurus | protoplanetary |
| hh-30 | HH 30 | HH 30 | Taurus | protoplanetary |
| iras-04302-2247 | IRAS 04302+2247 (alt "Butterfly Star") | IRAS 04302+2247 | Taurus | protoplanetary |
| hv-tau-c | HV Tau C | HV Tau C | Taurus | protoplanetary |
| iras-04200-2759 | IRAS 04200+2759 | IRAS 04200+2759 | Taurus | protoplanetary |
| haro-6-5b | Haro 6-5B (alt "FS Tau B") | Haro 6-5B | Taurus | protoplanetary |
| iras-04158-2805 | IRAS 04158+2805 | IRAS 04158+2805 | Taurus | protoplanetary |
| oph-163131 | Oph 163131 (alt "2MASS J16313124-2426281") | SSTc2d J163131.2-242627 | Ophiuchus | protoplanetary |
| eso-halpha-569 | ESO-Hα 569 | ESO-HA 569 | Chamaeleon I | protoplanetary |
| eso-halpha-574 | ESO-Hα 574 | ESO-HA 574 | Chamaeleon I | protoplanetary |
| hh-48-ne | HH 48 NE | 2MASS J11042275-7718080 | Chamaeleon I | protoplanetary |
| coconuts-1 | COCONUTS-1 | PSO J058.9855+45.4184 | (field, 31.5 pc → region null) | [] ; planets: B |

Coords: RA/Dec (+SpT) for all 12 keys above inserted into `data/coords_cache.json`
directly from **Villenave+2020 Table 1 (J2000)** / the PSO name position, each with a
`"source"` field. `make_systems.py` will therefore give every new system sky-map coords
immediately; the host SIMBAD pass (names in `data/coords_todo_batchP1.txt`) is only for
plx/mags enrichment. (`hk-tau` already had coords — untouched.)

## Jobs 2–5 crops (singles; checked on `_views/p1_check_singles.png`)

| image_id | content | notes |
|---|---|---|
| oph-163131_alma2022 | ALMA B6 1.3 mm, 0.02" (Fig. 1 L) | disk_mm |
| oph-163131_alma2022-zoom | labeled ring/gap zoom (Fig. 1 R) | disk_mm |
| tau-042021_jwst2024 | HST+JWST 0.8/2.0/7.7 µm composite (Fig. 1) | disk_scattered, wavelength_um 2.0 |
| tau-042021_jwst2024-f770w | MIRI 7.7 µm X-wings (Fig. 2 crop) | disk_scattered (scattered-light-dominated at 7.7 µm for this edge-on) |
| iras-04302-2247_vla2023 | VLA Ka 9.2 mm free-free-corrected (Fig. 2 crop) | new wavelength for atlas; 0.9/2.1 mm already covered by the 2020 survey crops |
| coconuts-1_discovery2020 | PS1 y-band finder, A+B labeled (Fig. 1) | type planet, 0.96 µm |
| coconuts-2_discovery2021 | AllWISE W1+W2 bi-color, A+b labeled (Fig. 1 UL panel crop) | fixes the file:null record; staging updates facility WISE / instrument AllWISE W1+W2 / λ 4.6 µm / paper w/ bibcode |

## Files written (all within batch-P1 ownership)

- `backend/manifests/batch-p1/*.json` — 11 manifests
- `images/<sysid>/*.png` — 29 crops (trimmed; all ≤ 560 px, ≤ 400 KB; largest
  tau-042021_jwst2024.png 344 KB at 500 px kept RGB — 256-color quantization caused banding)
- `data/staging/p1-*.json` — 11 staging files, 29 records
- `backend/seeds/scattered3.py` — 5 stubs replaced: EdgeOn-ALMA-2020 survey block
  (12 members, verified paper) + `EDGEON_SYSTEMS` (Oph 163131 / Tau 042021 /
  IRAS 04302+2247 / COCONUTS-1 as `system()` entries so their records get
  `survey: null` per data/README link rules); all `_verify` flags removed
- `data/coords_cache.json` — +12 keys (add-only, existing keys untouched)
- `data/coords_todo_batchP1.txt`
- `images/_sources/_views/p1_*` — rasterized sources + verification contact sheets

## Handoff notes for the orchestrator

1. Run order `make_systems.py` → `merge_staging.py` works best (systems born with
   coords/region/categories from seeds+cache; then staging attaches files and appends
   the -b4/-b6 extras, which exist in staging only). merge-before-make also converges.
2. `data/systems/coconuts-2.json` (not editable by me): `planets[0].paper` still has
   `"_verify": true` and no bibcode → set bibcode `2021ApJ...916L..11Z`, drop `_verify`;
   the note "~6 MJup, 7000 au separation" → paper says 6.3 MJup, 6471 au (594").
   My staging fixes the *image* record only.
3. Existing `hk-tau.json` has display name "hk tau" — could be prettified to "HK Tau".
4. ingestion_status.json (not editable by me): suggest entries
   `EdgeOn-ALMA-2020 / Villenave2022-Oph163131 / Duchene2024-JWST / Villenave2023-VLA /
   COCONUTS: entries done, coords done (paper values; SIMBAD enrichment pending), images done`.
5. Duchêne+2024 journal "AJ 167, 77" + bibcode are from memory (identity itself verified
   from tex) — 30-second ADS check recommended.
6. Pre-existing (NOT from this batch) duplicate seed image_ids noticed across seed
   modules: `ab-aur_seeds2011`, `hd-135344b_seeds2012`, `rx-j1604-3-2130_seeds2012`
   (SEEDS survey block vs. individual SYSTEMS entries elsewhere).
7. iras-04158-2805_edgeon-alma2020-b4 is a faithful crop of a near-non-detection
   (0.7 mJy/beam peak); drop it if it looks too empty in the UI.
