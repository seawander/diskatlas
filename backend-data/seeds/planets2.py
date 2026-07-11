"""Expansion seeds added by the comprehensiveness curator agent (Batch H).
Same structures as planets.py/scattered.py.

Workstream A: later-epoch / confirmation images of directly imaged planets
(GRAVITY interferometric detections, JWST imaging, key follow-up epochs).
All records file=null (metadata only); a later host fetch + crop pass fills them.
arXiv ids verified via web search 2026-07-06 (see data/staging/_report_batchH.md).
"""
from .util import survey, system, img, paper, planet

BLOCKS = []


def pimg(suffix, facility, instrument, wl, wl_label, technique, p, credit=None):
    return img(suffix, "planet", facility, instrument, wl, wl_label, technique, p,
               credit=credit)


SYSTEMS = [
    # ---- beta Pic: GRAVITY epochs for b and c -------------------------------
    system("beta Pic", images=[
        pimg("gravity2020", "VLTI-GRAVITY", "GRAVITY (K band)", 2.2,
             "K band interferometry; b spectrum + 10s-of-uas astrometry", "interferometry",
             paper("GRAVITY Collaboration", 2020,
                   "Peering into the formation history of beta Pictoris b with VLTI/GRAVITY long-baseline interferometry",
                   "A&A 633, A110", arxiv="1912.04651", bibcode=None)),
        pimg("gravity2020c", "VLTI-GRAVITY", "GRAVITY (K band)", 2.2,
             "K band interferometry; first direct confirmation of RV planet c", "interferometry",
             paper("Nowak", 2020,
                   "Direct confirmation of the radial-velocity planet beta Pictoris c",
                   "A&A 642, L2", arxiv="2010.04442", bibcode=None)),
    ]),

    # ---- HR 8799: GRAVITY e + JWST NIRCam -----------------------------------
    system("HR 8799", images=[
        pimg("gravity2019", "VLTI-GRAVITY", "GRAVITY (K band)", 2.2,
             "K band; first exoplanet detection by optical interferometry (e)", "interferometry",
             paper("GRAVITY Collaboration", 2019,
                   "First direct detection of an exoplanet by optical interferometry. Astrometry and K-band spectroscopy of HR 8799 e",
                   "A&A 623, L11", arxiv="1903.11903", bibcode="2019A&A...623L..11G")),
        pimg("jwst2025", "JWST", "NIRCam LW bar", 4.1,
             "2.5-4.6 um bar coronagraphy; all four planets, e first seen at 4.6 um", "coronagraphy",
             paper("Balmer", 2025,
                   "JWST-TST High Contrast: Living on the Wedge, or, NIRCam Bar Coronagraphy Reveals CO2 in the HR 8799 and 51 Eri Exoplanets' Atmospheres",
                   "AJ 169, 209", arxiv="2503.13608", bibcode="2025AJ....169..209B")),
    ]),

    # ---- PDS 70: JWST/NIRCam epoch ------------------------------------------
    system("PDS 70", images=[
        pimg("jwst2024", "JWST", "NIRCam", 4.83,
             "1.87 + 4.83 um; b & c re-detected, spiral stream + candidate d", "other",
             paper("Christiaens", 2024,
                   "MINDS: JWST/NIRCam imaging of the protoplanetary disk PDS 70. A spiral accretion stream and a potential third protoplanet",
                   "A&A 685, L1", arxiv="2403.04855", bibcode=None)),
    ]),

    # ---- 51 Eri: JWST NIRCam (same Balmer+2025 paper as HR 8799) ------------
    system("51 Eri", images=[
        pimg("jwst2025", "JWST", "NIRCam LW bar", 4.1,
             "4.1 um bar coronagraphy re-detection of b", "coronagraphy",
             paper("Balmer", 2025,
                   "JWST-TST High Contrast: Living on the Wedge, or, NIRCam Bar Coronagraphy Reveals CO2 in the HR 8799 and 51 Eri Exoplanets' Atmospheres",
                   "AJ 169, 209", arxiv="2503.13608", bibcode="2025AJ....169..209B")),
    ]),

    # ---- GJ 504: SPHERE re-detection epoch ----------------------------------
    system("GJ 504", images=[
        pimg("sphere2018", "VLT-SPHERE", "IRDIS dual-band", 1.6,
             "Y2/Y3/J3/H2/K1 re-detections; system re-analysis", "ADI",
             paper("Bonnefoy", 2018,
                   "The GJ 504 system revisited. Combining interferometric, radial velocity, and high contrast imaging data",
                   "A&A 618, A63", arxiv="1807.00657", bibcode="2018A&A...618A..63B")),
    ]),

    # ---- kappa And: SCExAO/CHARIS epoch --------------------------------------
    system("kappa And", images=[
        pimg("scexao2018", "Subaru-SCExAO", "CHARIS", 1.65,
             "JHK IFS imaging + spectrum of b", "ADI",
             paper("Currie", 2018,
                   "SCExAO/CHARIS Near-infrared Direct Imaging, Spectroscopy, and Forward-Modeling of kappa And b: A Likely Young, Low-gravity Superjovian Companion",
                   "AJ 156, 291", arxiv="1810.09457", bibcode=None)),
    ]),

    # ---- HD 95086: NACO confirmation epoch ----------------------------------
    system("HD 95086", images=[
        pimg("naco2013b", "VLT-NACO", "NACO", 3.8,
             "L' band; common-proper-motion confirmation of b", "ADI",
             paper("Rameau", 2013,
                   "Confirmation of the Planet around HD 95086 by Direct Imaging",
                   "ApJL 779, L26", arxiv="1310.7483", bibcode="2013ApJ...779L..26R")),
    ]),

    # ---- 1RXS J1609: Gemini confirmation (this one HAS a figure) ------------
    system("1RXS J1609", simbad="1RXS J160929.1-210524", images=[
        pimg("gemini2010", "Gemini", "NIRI+ALTAIR", 2.2,
             "K band follow-up epochs; common proper motion confirmed", "ADI",
             paper("Lafreniere", 2010,
                   "The Directly Imaged Planet around the Young Solar Analog 1RXS J160929.1-210524: Confirmation of Common Proper Motion, Temperature, and Mass",
                   "ApJ 719, 497", arxiv="1006.3070", bibcode="2010ApJ...719..497L")),
    ]),

    # NOTE (Batch H): GQ Lup and HIP 99770 later-epoch imaging papers were
    # deliberately skipped — no single canonical confirmation-image paper could
    # be verified within the search budget.
]

# --- late additions (WISPIT systems, YSES-1 JWST, AF Lep archival) -----------
SYSTEMS += [
    system("WISPIT 1", simbad="WISPIT 1", region="Sco-Cen / field (229 pc)", categories=(),
           planets=[planet("b"), planet("c")],
           images=[img("sphere2025", "planet", "VLT-SPHERE", "IRDIS", 1.65,
                       "H band; two co-moving giant planets around a Sun-like binary", "ADI",
                       paper("van Capelleveen", 2025,
                             "WIde Separation Planets In Time (WISPIT): Two directly imaged exoplanets around the Sun-like stellar binary WISPIT 1",
                             "A&A (2025)", arxiv="2508.18456", verify=True))],
           notes="K4+M5.5 binary, ~16 Myr; two wide-orbit planetary-mass companions."),

    system("WISPIT 2", simbad="WISPIT 2", region="~130-240 pc young solar analog",
           categories=("protoplanetary",),
           planets=[planet("b", "confirmed",
                           "~5 MJup H-alpha protoplanet inside the 60-au gap of the multi-ringed disk (2025); PDS 70 analogue"),
                    planet("c", "confirmed",
                           "Inner ~8-12 MJup planet confirmed spectroscopically with VLTI/GRAVITY (2026); orbital motion marginal - follow-up ongoing")],
           images=[
               img("magaox2025", "planet", "Magellan-MagAO-X", "MagAO-X", 0.656,
                   "H-alpha; gap protoplanet b discovery", "other",
                   paper("Close", 2025,
                         "Wide Separation Planets In Time (WISPIT): Discovery of a Gap H-alpha Protoplanet WISPIT 2b with MagAO-X",
                         "ApJL 990, L9", arxiv="2508.19046",
                         bibcode="2025ApJ...990L...9C", verify=True)),
               img("sphere2025", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.65,
                   "H band; multi-ringed disk with b inside the gap", "PDI",
                   paper("van Capelleveen", 2025,
                         "WIde Separation Planets In Time (WISPIT): A gap-clearing planet in a multi-ringed disk around the young solar-type star WISPIT 2",
                         "ApJL (2025)", arxiv="2508.19053", verify=True)),
               img("alma2026", "disk_mm", "ALMA", "Band 6/7", 1300,
                   "2 au resolution continuum of the planet-hosting disk", "interferometry",
                   paper("(TBD)", 2026,
                         "A 2 au resolution view by ALMA of the planet-hosting WISPIT 2 disk",
                         "A&A (2026)", arxiv="2601.15948", verify=True)),
               img("gravity2026", "planet", "VLTI-GRAVITY", "GRAVITY", 2.2,
                   "K band; spectroscopic confirmation of inner planet c", "interferometry",
                   paper("Lawlor", 2026,
                         "Direct spectroscopic confirmation of the young embedded proto-planet WISPIT 2c",
                         "arXiv (2026)", arxiv="2603.22085")),
           ],
           notes="Second known multi-planet system caught in formation inside its natal disk (PDS 70 analogue)."),

    system("YSES-1",
           images=[img("jwst2025", "planet", "JWST", "NIRCam+MIRI", 4.4,
                       "NIRCam image of both planets; silicate clouds in c, CPD around b",
                       "coronagraphy",
                       paper("Hoch", 2025,
                             "Silicate clouds and a circumplanetary disk in the YSES-1 exoplanet system",
                             "Nature (2025)", arxiv="2507.18861", verify=True))]),

    system("AF Lep",
           images=[img("naco2011-4s", "planet", "VLT-NACO", "NACO", 3.8,
                       "L' band; 2011 archival data, planet recovered with 4S ML post-processing (pre-discovery epoch)",
                       "ADI",
                       paper("Bonse", 2024,
                             "Use the 4S (Signal-Safe Speckle Subtraction): Explainable Machine Learning reveals the Giant Exoplanet AF Lep b in High-Contrast Imaging Data from 2011",
                             "AJ (2024)", arxiv="2406.01809", verify=True))]),
]
