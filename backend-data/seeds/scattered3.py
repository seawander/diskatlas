"""Expansion seeds added by the comprehensiveness curator agent (Batch H).
Same structures as planets.py/scattered.py.

Workstream B: classic disk images, pre-2010 back to 1984 (the historical layer
of the atlas). All records file=null; pre-arXiv papers have their ADS article
scans listed in backend-data/fetch_extra.txt for the host fetch pass.
NOTE: HD 163296 Grady+2000 STIS is NOT re-seeded here — data/systems already
holds hd-163296_stis2000 (its ADS scan was added to fetch_extra.txt instead).
Paper ids verified via web search 2026-07-06 (see data/staging/_report_batchH.md).
"""
from .util import survey, system, img, paper, planet

BLOCKS = []


def dimg(suffix, facility, instrument, wl, wl_label, technique, p, type_="disk_scattered"):
    return img(suffix, type_, facility, instrument, wl, wl_label, technique, p)


SYSTEMS = [
    # ---- beta Pic: the two foundational epochs ------------------------------
    system("beta Pic", images=[
        dimg("smith1984", "Las Campanas 2.5m", "CCD coronagraph", 0.89,
             "optical coronagraphy; first image of any circumstellar disk (1984)",
             "coronagraphy",
             paper("Smith", 1984,
                   "A circumstellar disk around beta Pictoris",
                   "Science 226, 1421", arxiv=None, bibcode="1984Sci...226.1421S")),
        dimg("kalas1995", "UH 2.2m", "coronagraph camera", 0.65,
             "R band coronagraphy (classic large-scale disk)", "coronagraphy",
             paper("Kalas", 1995,
                   "Asymmetries in the beta Pictoris dust disk",
                   "AJ 110, 794", arxiv=None, bibcode="1995AJ....110..794K")),
    ]),

    # ---- TW Hya: first scattered-light image of the face-on disk ------------
    system("TW Hya", images=[
        dimg("wfpc2-2000", "HST", "WFPC2", 0.6,
             "R/I PSF-subtracted imaging; face-on disk halo to ~200 au", "other",
             paper("Krist", 2000,
                   "WFPC2 Images of a Face-on Disk Surrounding TW Hydrae",
                   "ApJ 538, 793", arxiv=None, bibcode="2000ApJ...538..793K")),
    ]),

    # ---- AU Mic: 2004 discovery + Keck AO substructure ----------------------
    system("AU Mic", images=[
        dimg("kalas2004", "UH 2.2m", "coronagraph camera", 0.65,
             "R band coronagraphy; edge-on disk discovery (50-210 au)", "coronagraphy",
             paper("Kalas", 2004,
                   "Discovery of a Large Dust Disk around the Nearby Star AU Microscopii",
                   "Science 303, 1990", arxiv="astro-ph/0403132",
                   bibcode="2004Sci...303.1990K")),
        dimg("keck2004", "Keck", "AO NIR imager", 1.63,
             "H band AO; inner-disk substructure at 15-80 au", "other",
             paper("Liu", 2004,
                   "Substructure in the Circumstellar Disk around the Young Star AU Microscopii",
                   "Science 305, 1442", arxiv="astro-ph/0408164",
                   bibcode="2004Sci...305.1442L")),
    ]),

    # ---- HD 141569: NICMOS discovery of the ringed disk ----------------------
    system("HD 141569", images=[
        dimg("nicmos1999", "HST", "NICMOS", 1.1,
             "1.1 um coronagraphy; ~400 au disk with gap at 250 au", "coronagraphy",
             paper("Weinberger", 1999,
                   "The Circumstellar Disk of HD 141569 Imaged with NICMOS",
                   "ApJL 525, L53", arxiv="astro-ph/9909097",
                   bibcode="1999ApJ...525L..53W")),
    ]),

    # ---- AB Aur: first HST coronagraphic image (STIS, not NICMOS) -----------
    system("AB Aur", images=[
        dimg("stis1999", "HST", "STIS", 0.58,
             "optical coronagraphy; nebulosity/disk to ~1300 au", "coronagraphy",
             paper("Grady", 1999,
                   "Hubble Space Telescope Space Telescope Imaging Spectrograph Coronagraphic Imaging of the Herbig Ae Star AB Aurigae",
                   "ApJL 523, L151", arxiv=None, bibcode="1999ApJ...523L.151G")),
    ]),

    # ---- HD 100546: NICMOS2 coronagraphy ------------------------------------
    system("HD 100546", images=[
        dimg("nicmos2001", "HST", "NICMOS2", 1.6,
             "1.6 um coronagraphy; disk from ~50 to ~380 au", "coronagraphy",
             paper("Augereau", 2001,
                   "HST/NICMOS2 coronagraphic observations of the circumstellar environment of three old PMS stars: HD 100546, SAO 206462 and MWC 480",
                   "A&A 365, 78", arxiv="astro-ph/0009496",
                   bibcode="2001A&A...365...78A")),
    ]),

    # ---- GG Tau: first optical/NIR image of the circumbinary ring -----------
    # Facility VERIFIED from the ADS scan (batch I): "The instrument was mounted
    # at the Cassegrain f/36 focus of the Canada-France-Hawaii Telescope (CFHT)",
    # night of 1994 Dec 23 (UH IfA AO system + Hodapp HgCdTe camera) -> facility
    # CFHT is correct. Crop = Fig. 1b, J band, matched-PSF deconvolution.
    system("GG Tau", images=[
        dimg("cfht1996", "CFHT", "UH adaptive optics", 1.25,
             "I/J/H/K AO imaging; circumbinary ring detection", "other",
             paper("Roddier", 1996,
                   "Adaptive Optics Imaging of GG Tauri: Optical Detection of the Circumbinary Ring",
                   "ApJ 463, 326", arxiv=None, bibcode="1996ApJ...463..326R")),
    ]),

    # ---- HR 4796A: 1998 thermal-IR discovery of the ring --------------------
    system("HR 4796A", images=[
        dimg("keck1998", "Keck", "MIRLIN", 20.8,
             "20.8 um thermal imaging; disk resolved (companion paper: Jayawardhana+1998)",
             "other",
             paper("Koerner", 1998,
                   "Mid-Infrared Imaging of a Circumstellar Disk around HR 4796: Mapping the Debris of Planetary Formation",
                   "ApJL 503, L83", arxiv="astro-ph/9806268", bibcode=None),
             type_="disk_mm"),
    ]),

    # ---- GM Aur: NICMOS coronagraphy -----------------------------------------
    system("GM Aur", images=[
        dimg("nicmos2003", "HST", "NICMOS", 1.1,
             "1.1/1.6 um coronagraphy; ~300 au flared disk + envelope", "coronagraphy",
             paper("Schneider", 2003,
                   "NICMOS Coronagraphic Observations of the GM Aurigae Circumstellar Disk",
                   "AJ 125, 1467", arxiv=None, bibcode="2003AJ....125.1467S")),
    ]),
]

# --- edge-on protoplanetary disk papers + COCONUTS-1 (batch P1) ------------------
# Stubs completed 2026-07-06: paper identities/titles verified from the arXiv
# source .tex files; journal/volume verified from .bbl files of citing papers in
# images/_sources/extracted/ (Duchene 2024 = AJ 167, 77 from memory, high conf.).
# Coordinates from the papers themselves -> data/coords_cache.json (keys = simbad
# names below, "source" fields mark them) + data/coords_todo_batchP1.txt.

PAPER_VILLENAVE20 = paper("Villenave", 2020,
    "Observations of edge-on protoplanetary disks with ALMA. I. Results from continuum data",
    "A&A 642, A164", arxiv="2008.06518", bibcode="2020A&A...642A.164V")
PAPER_VILLENAVE22 = paper("Villenave", 2022,
    "A highly settled disk around Oph 163131",
    "ApJ 930, 11", arxiv="2204.00640", bibcode="2022ApJ...930...11V")
PAPER_DUCHENE24 = paper("Duchêne", 2024,
    "JWST imaging of edge-on protoplanetary disks. I. Fully vertically mixed 10 μm grains in the outer regions of a 1000 au disk",
    "AJ 167, 77", arxiv="2309.07040", bibcode="2024AJ....167...77D")
PAPER_VILLENAVE23 = paper("Villenave", 2023,
    "Modest dust settling in the IRAS04302+2247 Class I protoplanetary disk",
    "ApJ 946, 70", arxiv="2302.01949", bibcode="2023ApJ...946...70V")
PAPER_ZHANG20 = paper("Zhang", 2020,
    "COol Companions ON Ultrawide orbiTS (COCONUTS). I. A High-Gravity T4 Benchmark around an Old White Dwarf and A Re-Examination of the Surface-Gravity Dependence of the L/T Transition",
    "ApJ 891, 171", arxiv="2002.05723", bibcode="2020ApJ...891..171Z")

# Villenave+2020 Fig. 1 gallery: 12 edge-on disks, panel labels verified by eye.
# Primary crop per system = <sid>_edgeon-alma2020 (band 7; Oph 163131 has band 6
# only). Extra band 4/6 panels (<sid>_edgeon-alma2020-b4/-b6) enter via staging.
EDGEON_ALMA_2020 = survey("EdgeOn-ALMA-2020", PAPER_VILLENAVE20,
    {"type": "disk_mm", "facility": "ALMA", "instrument": "Band 7",
     "wavelength_um": 890, "wavelength_label": "0.89 mm continuum (edge-on)",
     "technique": "interferometry"},
    [
     ("IRAS 04302+2247", {"image_id": "iras-04302-2247_edgeon-alma2020",
                          "region": "Taurus", "alt_names": ["Butterfly Star"]}),
     # NB 2026-07-07: the edge-on disk belongs to the SECONDARY -> its own system
     ("HK Tau B", {"image_id": "hk-tau-b_edgeon-alma2020", "region": "Taurus",
                   "simbad": "V* HK Tau B",
                   "wavelength_label": "0.89 mm continuum (edge-on disk of the secondary)"}),
     ("HV Tau C", {"image_id": "hv-tau-c_edgeon-alma2020", "region": "Taurus"}),
     ("IRAS 04200+2759", {"image_id": "iras-04200-2759_edgeon-alma2020",
                          "region": "Taurus"}),
     ("Haro 6-5B", {"image_id": "haro-6-5b_edgeon-alma2020", "region": "Taurus",
                    "alt_names": ["FS Tau B"]}),
     ("IRAS 04158+2805", {"image_id": "iras-04158-2805_edgeon-alma2020",
                          "region": "Taurus"}),
     ("Tau 042021", {"simbad": "2MASS J04202144+2813491",
                     "image_id": "tau-042021_edgeon-alma2020", "region": "Taurus"}),
     ("HH 30", {"image_id": "hh-30_edgeon-alma2020", "region": "Taurus"}),
     ("Oph 163131", {"simbad": "SSTc2d J163131.2-242627",
                     "image_id": "oph-163131_edgeon-alma2020", "region": "Ophiuchus",
                     "instrument": "Band 6", "wavelength_um": 1300,
                     "wavelength_label": "1.3 mm continuum (edge-on)"}),
     ("ESO-Hα 569", {"simbad": "ESO-HA 569", "region": "Chamaeleon I",
                     "image_id": "eso-halpha-569_edgeon-alma2020"}),
     ("ESO-Hα 574", {"simbad": "ESO-HA 574", "region": "Chamaeleon I",
                     "image_id": "eso-halpha-574_edgeon-alma2020"}),
     ("HH 48 NE", {"simbad": "2MASS J11042275-7718080", "region": "Chamaeleon I",
                   "image_id": "hh-48-ne_edgeon-alma2020"}),
    ], categories=("protoplanetary",))

BLOCKS += [EDGEON_ALMA_2020]

# Single-target papers (former EdgeOn-2204 / EdgeOn-2309 / EdgeOn-2302 / COCONUTS
# stubs) as individual systems -> image records get survey=None per data/README.
# NOTE 2204.00640: the requested "Figs 11 and 14" are a pebble-accretion contour
# plot and the SED (not disk imagery; verified by eye) -- cropped the signature
# Fig. 1 continuum image + labeled zoom instead. See _report_batchP1.md.
EDGEON_SYSTEMS = [
    system("Oph 163131", simbad="SSTc2d J163131.2-242627", region="Ophiuchus",
           categories=("protoplanetary",),
           alt_names=["2MASS J16313124-2426281"],
           images=[
               img("alma2022", "disk_mm", "ALMA", "Band 6", 1300,
                   "1.3 mm continuum at 0.02\" (3 au) resolution", "interferometry",
                   PAPER_VILLENAVE22),
               img("alma2022-zoom", "disk_mm", "ALMA", "Band 6", 1300,
                   "1.3 mm continuum, zoomed (rings and gap labeled)",
                   "interferometry", PAPER_VILLENAVE22),
           ]),
    system("Tau 042021", simbad="2MASS J04202144+2813491", region="Taurus",
           categories=("protoplanetary",), images=[
               img("jwst2024", "disk_scattered", "JWST", "NIRCam/MIRI (+HST ACS)",
                   2.0, "0.8/2.0/7.7 µm color composite (HST+JWST)", "other",
                   PAPER_DUCHENE24),
               img("jwst2024-f770w", "disk_scattered", "JWST", "MIRI F770W", 7.7,
                   "7.7 µm imaging (X-shaped mid-IR wings)", "other",
                   PAPER_DUCHENE24),
           ]),
    system("IRAS 04302+2247", region="Taurus", categories=("protoplanetary",),
           images=[
               img("vla2023", "disk_mm", "VLA", "Ka band", 9200,
                   "9.2 mm continuum (free-free corrected)", "interferometry",
                   PAPER_VILLENAVE23),
           ]),
    system("COCONUTS-1", simbad="PSO J058.9855+45.4184", categories=(),
           planets=[{**planet("B", "confirmed",
                              "T4 brown-dwarf benchmark companion, 40.6\" = 1280 au"
                              " from the DA white dwarf primary"),
                     "paper": {"first_author": "Zhang", "year": 2020,
                               "arxiv": "2002.05723",
                               "bibcode": "2020ApJ...891..171Z"}}],
           images=[
               img("discovery2020", "planet", "Pan-STARRS1", "GPC1, y band", 0.96,
                   "PS1 y-band image: T4 companion 40.6\" (1280 au) from the white dwarf",
                   "other", PAPER_ZHANG20),
           ],
           notes="COCONUTS-1A = DA white dwarf (31.5 pc, age 7.3 Gyr); "
                 "COCONUTS-1B = wide T4 companion (Zhang et al. 2020, COCONUTS I)."),
]
SYSTEMS += EDGEON_SYSTEMS

# Keck/NIRC2 vortex L-prime survey of 43 mm-substructured disks (2408.04048).
# Batch S 2026-07-06: paper identity verified from main.tex (title/first author)
# + web search (AJ 168, 78; DOI 10.3847/1538-3881/ad390c). Fig. 4 maps 8 disks
# in scattered light; membership below = Fig. 4 panel labels verified by eye:
# 2MJ1604 / LkHa 330 / LkCa15 / MWC758 // PDS 70 / RY Tau / HD 34282 / CQ Tau.
# All 8 systems pre-exist in data/systems/. Every panel is an RDI reduction
# except CQ Tau (ADI) -> technique fixed per-record in the batch-S staging.
BLOCKS += [
    survey("Keck-vortex-2024", paper("Wallack", 2024,
           "A Survey of Protoplanetary Disks Using the Keck/NIRC2 Vortex Coronagraph",
           "AJ 168, 78", arxiv="2408.04048", bibcode="2024AJ....168...78W"),
           {"type": "disk_scattered", "facility": "Keck", "instrument": "NIRC2 vortex",
            "wavelength_um": 3.8,
            "wavelength_label": "L' 3.8 um scattered light (ALMA contours overlaid)",
            "technique": "RDI"},
           [
            ("RX J1604.3-2130", {"simbad": "2MASS J16042165-2130284"}),
            "LkHa 330",
            "LkCa 15",
            "MWC 758",
            "PDS 70",
            "RY Tau",
            "HD 34282",
            "CQ Tau",  # ADI (only non-RDI panel of Fig. 4)
           ], categories=("protoplanetary",)),
]

# Bahcall HST/WFPC2 quasar-host classics (user-requested).
# Batch T 2026-07-06: titles/authors/targets/redshifts verified BY EYE from the
# arXiv sources (both are dvips PostScript; rendered via ps2pdf+pdftoppm).
# Paper I (astro-ph/9409028, "quasarpaper", 13 pp): Bahcall, Kirhakos & Schneider,
#   "HST Images of Nearby Luminous Quasars" — journal ApJ 435, L11 verified from
#   Paper II's reference list. Fig. 1 (four F606W PSF-subtracted panels) IS in the
#   source and was cropped (manifests/batch-t/t-bahcall-quasars-1994.json).
#   Members (Table 1): PG 0953+414 z=0.239 / PG 1116+215 z=0.177 /
#   PG 1202+281 (GQ Com) z=0.165 / PG 1307+085 z=0.155. Hosts NOT detected
#   (the classic "naked quasar" upper limits); camera = WFC2 half of WFPC2.
# Paper II (astro-ph/9501018, "qpaper2", 43 pp): "HST Images of Nearby Luminous
#   Quasars II: Results for Eight Quasars and Tests of the Detection Sensitivity";
#   journal ApJ 450, 486 + bibcode from agent knowledge (confirm at ADS fetch).
#   NO figures in the source (captions only) -> records stay file=null; the four
#   quasars new in Paper II are seeded below (candidate hosts: PG 1116+215,
#   3C 273, PG 1444+407; the Paper-I four are not re-seeded to avoid duplicate
#   near-identical F606W records). Published-PDF fetch lines: backend-data/fetch_extra.txt.
BLOCKS += [
    survey("Bahcall-quasars-1994", paper("Bahcall", 1994,
           "HST Images of Nearby Luminous Quasars",
           "ApJL 435, L11", arxiv="astro-ph/9409028",
           bibcode="1994ApJ...435L..11B"),
           {"type": "quasar", "facility": "HST", "instrument": "WFPC2 (WFC)",
            "wavelength_um": 0.6,
            "wavelength_label": "F606W; PSF-subtracted quasar image "
                                "(host-galaxy upper limit, the 'naked quasar' result)",
            "technique": "other"},
           [
            ("PG 0953+414", {"image_id": "pg-0953-414_bahcall1994"}),
            ("PG 1116+215", {"image_id": "pg-1116-215_bahcall1994"}),
            ("PG 1202+281", {"image_id": "pg-1202-281_bahcall1994",
                             "alt_names": ["GQ Com"]}),
            ("PG 1307+085", {"image_id": "pg-1307-085_bahcall1994"}),
           ], region="extragalactic", categories=("quasar",),
           notes="four radio-quiet PG quasars, z=0.155-0.239; cropped by batch T"),
    survey("Bahcall-quasars-1995", paper("Bahcall", 1995,
           "HST Images of Nearby Luminous Quasars II: Results for Eight Quasars"
           " and Tests of the Detection Sensitivity",
           "ApJ 450, 486", arxiv="astro-ph/9501018",
           bibcode="1995ApJ...450..486B"),
           {"type": "quasar", "facility": "HST", "instrument": "WFPC2 (WFC)",
            "wavelength_um": 0.6,
            "wavelength_label": "F606W; quasar host imaging",
            "technique": "other"},
           [
            ("3C 273", {"image_id": "3c-273_bahcall1995",
                        "wavelength_label": "F606W; candidate host galaxy"
                                            " (radio-loud, jet visible)"}),
            ("PKS 1302-102", {"image_id": "pks-1302-102_bahcall1995",
                              "wavelength_label": "F606W; radio-loud quasar with close"
                                                  " companion galaxies (host inconclusive)"}),
            ("PG 1444+407", {"image_id": "pg-1444-407_bahcall1995",
                             "wavelength_label": "F606W; candidate host galaxy"
                                                 " after PSF subtraction"}),
            ("3C 323.1", {"image_id": "3c-323-1_bahcall1995",
                          "wavelength_label": "F606W; radio-loud quasar"
                                              " (host-galaxy upper limit)"}),
           ], region="extragalactic", categories=("quasar",),
           notes="the four quasars new in Paper II (full sample = 8, z=0.155-0.286);"
                 " no source figures - crop from published PDF when fetched"),
]
