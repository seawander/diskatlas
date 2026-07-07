"""ALMA (and mm-interferometry) protoplanetary-disk surveys and classics.

Membership sources:
- DSHARP: Andrews et al. 2018 Table 1 (20 disks) — COMPLETE.
- Taurus/Long+2018: the 12 substructured disks of Fig. 1 — COMPLETE.
- Taurus/Long+2019: full 32-disk sample — the 20 compact/smooth disks (Fig. 3 panel
  labels) are listed here; the 12 substructured ones live in the Long+2018 block. COMPLETE.
- exoALMA: 15 disks (exoALMA I Table 1) — COMPLETE; continuum images from exoALMA IV.
- ODISEA long-baseline (Cieza+2021 ODISEA III, Table 1 + Fig. 3): 10 disks — COMPLETE.
"""
from .util import survey, system, img, paper, planet

P_DSHARP = paper("Andrews", 2018,
                 "The Disk Substructures at High Angular Resolution Project (DSHARP). I. Motivation, Sample, Calibration, and Overview",
                 "ApJL 869, L41", arxiv="1812.04040", bibcode="2018ApJ...869L..41A")
P_LONG18 = paper("Long", 2018,
                 "Gaps and Rings in an ALMA Survey of Disks in the Taurus Star-forming Region",
                 "ApJ 869, 17", arxiv="1810.06044", bibcode="2018ApJ...869...17L")
P_LONG19 = paper("Long", 2019,
                 "Compact Disks in a High-resolution ALMA Survey of Dust Structures in the Taurus Molecular Cloud",
                 "ApJ 882, 49", arxiv="1906.10809", bibcode="2019ApJ...882...49L")
P_EXOALMA1 = paper("Teague", 2025,
                   "exoALMA I. Science Goals, Project Design and Data Products",
                   "ApJL 984, L6", arxiv="2504.18688", verify=True)
P_EXOALMA4 = paper("Curone", 2025,
                   "exoALMA IV: Substructures, Asymmetries, and the Faint Outer Disk in Continuum Emission",
                   "ApJL (exoALMA special issue)", arxiv="2504.18725")
# Title/arXiv id verified against the source tarball (ms.tex \title); journal from ADS convention.
P_ODISEA = paper("Cieza", 2021,
                 "The Ophiuchus DIsc Survey Employing ALMA (ODISEA) - III: the evolution of substructures in massive discs at 3-5 au resolution",
                 "MNRAS 501, 2934", arxiv="2012.00189", bibcode="2021MNRAS.501.2934C")

MM = {"type": "disk_mm", "facility": "ALMA", "technique": "interferometry"}

BLOCKS = [
    survey("DSHARP", P_DSHARP,
           {**MM, "instrument": "Band 6", "wavelength_um": 1250,
            "wavelength_label": "1.25 mm continuum"},
           [
               ("HT Lup", {"region": "Lupus"}),
               ("GW Lup", {"region": "Lupus"}),
               ("IM Lup", {"region": "Lupus"}),
               ("RU Lup", {"region": "Lupus"}),
               ("Sz 114", {"region": "Lupus"}),
               ("Sz 129", {"region": "Lupus"}),
               ("MY Lup", {"region": "Lupus"}),
               ("HD 142666", {"region": "Upper Sco / Sco-Cen"}),
               ("HD 143006", {"region": "Upper Sco / Sco-Cen"}),
               ("AS 205", {"region": "Ophiuchus"}),
               ("SR 4", {"simbad": "EM* SR 4", "region": "Ophiuchus"}),
               ("Elias 20", {"simbad": "Elia 2-20", "region": "Ophiuchus"}),
               ("DoAr 25", {"region": "Ophiuchus"}),
               ("Elias 24", {"simbad": "Elia 2-24", "region": "Ophiuchus"}),
               ("Elias 27", {"simbad": "Elia 2-27", "region": "Ophiuchus"}),
               ("DoAr 33", {"region": "Ophiuchus"}),
               ("WSB 52", {"region": "Ophiuchus"}),
               ("WaOph 6", {"simbad": "V2508 Oph", "region": "Ophiuchus"}),
               ("AS 209", {"region": "Ophiuchus"}),
               ("HD 163296", {"region": "isolated Herbig Ae"}),
           ],
           categories=("protoplanetary",)),

    survey("Taurus-Long2018", P_LONG18,
           {**MM, "instrument": "Band 6", "wavelength_um": 1330,
            "wavelength_label": "1.33 mm continuum"},
           [
               "CI Tau", "CIDA 9", "DL Tau", "DN Tau", "DS Tau", "FT Tau",
               "GO Tau", "IP Tau", "IQ Tau", "MWC 480", "RY Tau",
               ("UZ Tau E", {"simbad": "UZ Tau"}),
           ],
           region="Taurus", categories=("protoplanetary",)),

    # Long+2019: the remaining (compact/smooth) members of the 32-disk sample,
    # from the Fig. 3 mosaic panel labels (panels 13-32; 12 smooth singles + 8 binaries).
    survey("Taurus-Long2019", P_LONG19,
           {**MM, "instrument": "Band 6", "wavelength_um": 1330,
            "wavelength_label": "1.33 mm continuum"},
           [
               "BP Tau", "V409 Tau", "DR Tau", "HO Tau",
               ("Haro 6-13", {"alt_names": ["V806 Tau"]}),
               "DO Tau", "DQ Tau", "GI Tau", "V836 Tau", "HQ Tau",
               "HP Tau", "GK Tau",
               # smooth disks in binaries (last mosaic row):
               "V710 Tau", "HK Tau", "DH Tau", "T Tau", "HN Tau",
               "RW Aur", "DK Tau", "UY Aur",
           ],
           region="Taurus", categories=("protoplanetary",),
           notes=None),

    survey("exoALMA", P_EXOALMA4,
           {**MM, "instrument": "Band 7", "wavelength_um": 900,
            "wavelength_label": "0.9 mm continuum"},
           [
               ("AA Tau", {"region": "Taurus"}),
               ("CQ Tau", {"region": "Taurus-Auriga"}),
               ("DM Tau", {"region": "Taurus"}),
               ("HD 34282", {"region": "Orion outskirts"}),
               ("HD 135344B", {"alt_names": ["SAO 206462"], "region": "Sco-Cen"}),
               ("HD 143006", {"region": "Upper Sco / Sco-Cen"}),
               ("RX J1604.3-2130", {"simbad": "2MASS J16042165-2130284",
                                    "alt_names": ["J1604"], "region": "Upper Sco"}),
               ("RX J1615.3-3255", {"alt_names": ["J1615"], "region": "Lupus"}),
               ("RX J1842.9-3532", {"alt_names": ["J1842"], "region": "CrA"}),
               ("RX J1852.3-3700", {"alt_names": ["J1852"], "region": "CrA"}),
               ("LkCa 15", {"region": "Taurus"}),
               ("MWC 758", {"alt_names": ["HD 36112"], "region": "Taurus-Auriga"}),
               ("PDS 66", {"alt_names": ["MP Mus"], "region": "Lower Cen-Crux"}),
               ("SY Cha", {"region": "Chamaeleon I"}),
               ("V4046 Sgr", {"region": "beta Pic moving group"}),
           ],
           categories=("protoplanetary",)),

    # ODISEA long-baseline sample (Cieza+2021 ODISEA III, Table 1 / Fig. 3 labels).
    # The 5 DSHARP Ophiuchus members of the same flux-limited sample (SR 4,
    # Elias 2-20/2-24/2-27, DoAr 25) are already in the DSHARP block.
    survey("ODISEA", P_ODISEA,
           {**MM, "instrument": "Band 6", "wavelength_um": 1300,
            "wavelength_label": "1.3 mm continuum"},
           [
               ("ISO-Oph 54", {"notes": "Class I (SSTc2d J162640.5-242714)"}),
               ("WLY 2-63", {"alt_names": ["IRS 63"],
                             "notes": "flat-spectrum source (SSTc2d J163135.6-240129)"}),
               ("ISO-Oph 37", {"notes": "flat-spectrum source (SSTc2d J162623.6-242439)"}),
               ("ISO-Oph 17", {"notes": "SSTc2d J162610.3-242054"}),
               "DoAr 44",
               "WSB 82",
               ("ISO-Oph 2", {"notes": "binary; 2.2 au cavity in primary, companion disk ISO-Oph 2B"}),
               "ISO-Oph 196",
               ("SR 24S", {"simbad": "EM* SR 24S"}),
               ("RX J1633.9-2442", {"simbad": "RX J1633.9-2442"}),
           ],
           region="Ophiuchus", categories=("protoplanetary",)),
]

SYSTEMS = [
    system("HL Tau", region="Taurus", categories=("protoplanetary",),
           images=[img("alma2015", "disk_mm", "ALMA", "Bands 6+7", 1000,
                       "1.0 mm continuum (B6+B7 combined, iconic ring image)", "interferometry",
                       paper("ALMA Partnership", 2015,
                             "First Results from High Angular Resolution ALMA Observations Toward the HL Tau Region",
                             "ApJL 808, L3", arxiv="1503.02649",
                             bibcode="2015ApJ...808L...3A"))],
           notes="The first iconic ALMA ring system."),

    system("TW Hya", region="TW Hya association", categories=("protoplanetary",),
           images=[img("alma2016", "disk_mm", "ALMA", "Band 7", 870,
                       "870 um continuum", "interferometry",
                       paper("Andrews", 2016,
                             "Ringed Substructure and a Gap at 1 au in the Nearest Protoplanetary Disk",
                             "ApJL 820, L40", arxiv="1603.09352",
                             bibcode="2016ApJ...820L..40A"))]),

    system("PDS 70", region="Upper Cen-Lup", categories=("protoplanetary",),
           planets=[planet("b"), planet("c")],
           images=[img("alma2021", "disk_mm", "ALMA", "Band 7", 855,
                       "855 um continuum (ring + CPD around c)", "interferometry",
                       paper("Benisty", 2021,
                             "A Circumplanetary Disk around PDS 70 c",
                             "ApJL 916, L2", arxiv="2108.07123",
                             bibcode="2021ApJ...916L...2B"))],
           notes="Only system with two confirmed planets caught in formation inside the disk cavity."),

    system("GM Aur", region="Taurus", categories=("protoplanetary",),
           images=[img("alma2020", "disk_mm", "ALMA", "Band 6", 1100,
                       "1.1 mm continuum", "interferometry",
                       paper("Huang", 2020,
                             "A Multifrequency ALMA Characterization of Substructures in the GM Aur Protoplanetary Disk",
                             "ApJ 891, 48", arxiv="2001.11040",
                             bibcode="2020ApJ...891...48H"))]),

    system("AB Aur", alt_names=("HD 31293",), region="Taurus-Auriga",
           categories=("protoplanetary",),
           planets=[planet("b", "candidate",
                           "Currie+2022 NIR/UV point source; disputed (scattered light?)")],
           images=[img("alma2017", "disk_mm", "ALMA", "Band 6", 1300,
                       "1.3 mm continuum + CO spirals", "interferometry",
                       paper("Tang", 2017,
                             "Planet Formation in AB Aurigae: Imaging of the Inner Gaseous Spirals Observed inside the Dust Cavity",
                             "ApJ 840, 32", arxiv="1704.02699", bibcode=None))]),

    system("HD 142527", region="Sco-Cen", categories=("protoplanetary",),
           images=[img("alma2013", "disk_mm", "ALMA", "Band 7", 870,
                       "870 um continuum (horseshoe)", "interferometry",
                       paper("Casassus", 2013,
                             "Flows of gas through a protoplanetary gap",
                             "Nature 493, 191", arxiv="1305.6062",
                             bibcode="2013Natur.493..191C"))],
           notes="Extreme azimuthal dust asymmetry; M-dwarf companion inside cavity."),

    system("Oph IRS 48", simbad="WLY 2-48", region="Ophiuchus",
           categories=("protoplanetary",),
           images=[img("alma2013", "disk_mm", "ALMA", "Band 9", 440,
                       "0.44 mm continuum (dust trap)", "interferometry",
                       paper("van der Marel", 2013,
                             "A major asymmetric dust trap in a transition disk",
                             "Science 340, 1199", arxiv="1306.1768",
                             bibcode="2013Sci...340.1199V"))],
           notes="Prototype azimuthal dust trap. IRS 48 = WLY 2-48 (confirmed in van der Marel+2013 M&M)."),

    system("HD 169142", region="isolated Herbig", categories=("protoplanetary",),
           planets=[planet("b", "candidate", "Hammond+2023 recovery of Gratton+2019 candidate in gap")],
           images=[img("alma2017", "disk_mm", "ALMA", "Band 6", 1300,
                       "1.3 mm continuum rings", "interferometry",
                       paper("Fedele", 2017,
                             "ALMA unveils rings and gaps in the protoplanetary system HD 169142: signatures of two giant protoplanets",
                             "A&A 600, A72", arxiv="1702.02844", bibcode=None))]),

    system("HD 100546", region="Sco-Cen outskirts", categories=("protoplanetary",),
           planets=[planet("b", "disputed", "Quanz+2013 candidate; nature debated"),
                    planet("c", "disputed", "inner candidate; unconfirmed")],
           # NOTE: arXiv id 1403.0121 was WRONG (that tarball = Agundez hot-Jupiter
           # chemistry paper). Bibcode confirmed from a .bbl (2014ApJ...791L...6W);
           # correct arXiv id still to be found + source fetched (title unverified).
           images=[img("alma2014", "disk_mm", "ALMA", "Band 7", 870,
                       "870 um continuum", "interferometry",
                       paper("Walsh", 2014,
                             "ALMA Reveals the Anatomy of the mm-sized Dust and Molecular Gas in the HD 100546 Disk",
                             "ApJL 791, L6", arxiv=None,
                             bibcode="2014ApJ...791L...6W", verify=True))]),

    system("MWC 758", alt_names=("HD 36112",), region="Taurus-Auriga",
           categories=("protoplanetary",),
           planets=[planet("c", "candidate", "Wagner+2023 JWST/LBT candidate at ~100 au")],
           images=[img("alma2018", "disk_mm", "ALMA", "Band 7", 870,
                       "870 um continuum (clumps + cavity)", "interferometry",
                       paper("Dong", 2018,
                             "The Eccentric Cavity, Triple Rings, Two-Armed Spirals, and Double Clumps of the MWC 758 Disk",
                             "ApJ 860, 124", arxiv="1805.12141", bibcode=None))]),

    # NOTE: arXiv id was 1709.02068 (WRONG: that tarball = a particle-physics paper).
    # Correct id 1710.05028 recovered from a bibliography Eprint entry (exact title +
    # ApJ 848 match); source tarball still needs a host fetch for the crop.
    system("V1247 Ori", region="Orion", categories=("protoplanetary",),
           images=[img("alma2017", "disk_mm", "ALMA", "Band 7", 870,
                       "870 um continuum (crescent)", "interferometry",
                       paper("Kraus", 2017,
                             "Dust-trapping Vortices and a Potentially Planet-triggered Spiral Wake in the Pre-transitional Disk of V1247 Orionis",
                             "ApJL 848, L11", arxiv="1710.05028", bibcode=None))]),

    system("Elias 27", simbad="Elia 2-27", alt_names=("Elias 2-27",),
           region="Ophiuchus", categories=("protoplanetary",),
           images=[img("alma2016", "disk_mm", "ALMA", "Band 6", 1300,
                       "1.3 mm continuum (grand-design spirals)", "interferometry",
                       paper("Perez", 2016,
                             "Spiral density waves in a young protoplanetary disk",
                             "Science 353, 1519", arxiv="1610.05139",
                             bibcode="2016Sci...353.1519P"))],
           notes="Same star as DSHARP 'Elias 27' — records merge under one system id."),

    system("AS 209", region="Ophiuchus", categories=("protoplanetary",),
           planets=[planet("b", "candidate", "Bae+2022: 13CO-detected CPD candidate in gas gap at ~200 au")],
           images=[]),
]
