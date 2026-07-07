"""Scattered-light (high-contrast) disk imaging: GPI, SPHERE, HST, JWST, Subaru.

Survey membership marked AGENT TODO must be completed from the papers
(figure panel labels are ground truth for what was actually DETECTED).
"""
from .util import survey, system, img, paper, planet

P_GPIES = paper("Esposito", 2020,
                "Debris Disk Results from the Gemini Planet Imager Exoplanet Survey's Polarimetric Imaging Campaign",
                "AJ 160, 24", arxiv="2004.13722", bibcode="2020AJ....160...24E")
P_LIGHTS = paper("Rich", 2022,
                 "Gemini-LIGHTS: Herbig Ae/Be and Massive T Tauri Protoplanetary Disks Imaged with Gemini Planet Imager",
                 "AJ 164, 109", arxiv="2206.05815")
P_DARTTS = paper("Avenhaus", 2018,
                 "Disks around T Tauri Stars with SPHERE (DARTTS-S). I. SPHERE/IRDIS Polarimetric Imaging of Eight Prominent T Tauri Disks",
                 "ApJ 863, 44", arxiv="1803.10882", bibcode="2018ApJ...863...44A")
P_GARUFI_TAU = paper("Garufi", 2024,
                     "The SPHERE view of the Taurus star-forming region: The full census of planet-forming disks with GTO and DESTINYS programs",
                     "A&A 685, A53", arxiv="2403.02158")
P_GINSKI_CHA = paper("Ginski", 2024,
                     "The SPHERE view of the Chamaeleon I star-forming region: The full census of planet-forming disks with GTO and DESTINYS programs",
                     "A&A 685, A52", arxiv="2403.02149", bibcode="2024A&A...685A..52G")
P_VALEGARD_ORI = paper("Valegard", 2024,
                       "Disk Evolution Study Through Imaging of Nearby Young Stars (DESTINYS): The SPHERE view of the Orion star-forming region",
                       "A&A 685 (2024)", arxiv="2403.02156")
P_SCHNEIDER14 = paper("Schneider", 2014,
                      "Probing for Exoplanets Hiding in Dusty Debris Disks: Disk Imaging, Characterization, and Exploration with HST/STIS Multi-Roll Coronagraphy",
                      "AJ 148, 59", arxiv="1406.7303", bibcode="2014AJ....148...59S")
P_REN_STIS = paper("Ren", 2023,
                   "Debris Disk Color with the Hubble Space Telescope",
                   "A&A 672, A114", arxiv="2302.04273", bibcode="2023A&A...672A.114R")
# ^ exact title verified from arXiv source ms.tex (\title{Debris Disk Color with
#   the \textit{Hubble Space Telescope}}); uniform STIS+NICMOS study of 23 systems.
P_REN_KS = paper("Ren", 2023,
                 "Protoplanetary disks in Ks-band total intensity and polarized light",
                 "A&A 680, A114", arxiv="2310.08589", bibcode="2023A&A...680A.114R")
# ^ verified from arXiv source ms.tex (author Bin Ren; title exact); star-hopping RDI survey.
P_DISCS = paper("Hom", 2025,
                "The Disks In Scorpius-Centaurus Survey (DISCS) I: Four Newly-Resolved Debris Disks in Polarized Intensity Light",
                "AJ (2025)", arxiv="2505.02976")
P_SPHERE_DEBRIS25 = paper("Engler", 2025,
                          "Characterization of debris disks observed with SPHERE",
                          "A&A 704, A21", arxiv="2512.03128")

PDI_H = {"type": "disk_scattered", "facility": "Gemini-GPI", "instrument": "IFS pol",
         "wavelength_um": 1.65, "wavelength_label": "H band 1.6 um (pol. intensity)",
         "technique": "PDI"}
SPH_PDI = {"type": "disk_scattered", "facility": "VLT-SPHERE", "instrument": "IRDIS DPI",
           "wavelength_um": 1.65, "wavelength_label": "H band 1.6 um (pol. intensity)",
           "technique": "PDI"}
STIS = {"type": "disk_scattered", "facility": "HST", "instrument": "STIS",
        "wavelength_um": 0.58, "wavelength_label": "0.2-1.0 um broadband (optical)",
        "technique": "coronagraphy"}

BLOCKS = [
    # Membership completed from Esposito+2020 Figs. 5+6 panel labels (26 debris disks):
    # 24 in the Qphi gallery (Fig. 5) + HD 15115 and NZ Lup detected in total intensity only (Fig. 6).
    survey("GPIES-debris", P_GPIES, PDI_H,
           [
               ("HR 4796A", {"simbad": "HR 4796"}),
               "HD 15115", "HD 30447", "HD 32297", "HD 35841", "HD 61005",
               "HD 106906", "HD 110058", "HD 111161", "HD 111520", "HD 114082",
               "HD 115600", "HD 117214", "HD 129590", "HD 131835", "HD 143675",
               "HD 145560", "HD 146897", "HD 156623", "HD 157587", "HD 191089",
               ("AU Mic", {}), ("beta Pic", {}),
               ("TWA 7", {"simbad": "TWA 7", "notes": "panel label 'CE Ant' = TWA 7"}),
               ("HR 7012", {"alt_names": ("HD 172555",)}),
               "NZ Lup",
           ],
           categories=("debris",),
           notes="membership complete (26 debris; HD 15115 + NZ Lup total-intensity-only detections)"),

    # The 3 protoplanetary/transitional disks detected by GPIES (Esposito+2020 Fig. 9).
    survey("GPIES", P_GPIES, PDI_H,
           ["AK Sco", "HD 100546", "HD 141569"],
           categories=("protoplanetary",),
           notes="GPIES protoplanetary/transition disk detections (Qphi row of Fig. 9)"),

    # RESOLVED detections only (22/44), from Rich+2022 category galleries
    # (spirals / rings / continuous / irregulars figures; panel labels = ground truth).
    # NOT in the Rich+2022 sample (wrongly seeded before): HD 135344B, MWC 758 —
    # their stale *_gemini-lights records in data/systems need deletion by the orchestrator.
    # HD 150193 IS in the sample (as MWC 863) but only in the "undetermined" (unresolved)
    # category, so it is dropped from members too (stale record likewise).
    # 9 non-detections and 13 unresolved/undetermined targets are excluded.
    survey("Gemini-LIGHTS", P_LIGHTS, PDI_H,
           [
               "HD 100453", "HD 139614", "HD 34700", "HD 142527",          # spirals
               "HD 169142", "HD 141569",                                    # rings
               ("HD 163296", {}),   # panel label "MWC 275"
               ("HD 97048", {}),    # panel label "CU Cha"
               "PDS 66",                                                    # rings
               ("AK Sco", {}), "HD 45677", "HD 50138", "HD 100546",         # continuous
               "HD 142666", "HD 145718", ("HT Lup", {}), ("MWC 297", {}),
               ("MWC 614", {}),
               ("MWC 789", {}), ("FU Ori", {}), ("GW Ori", {}),             # irregulars
               ("Hen 3-365", {}),
           ],
           categories=("protoplanetary",),
           notes="resolved detections only (22/44); J or H band per epoch (see image records)"),

    # DARTTS-S I: 8 disks, membership completed from Avenhaus+2018 Fig. 1 panel labels.
    survey("DARTTS-S", P_DARTTS, SPH_PDI,
           ["IM Lup", "RU Lup", "MY Lup", "PDS 66", "V4046 Sgr",
            ("RX J1615.3-3255", {"simbad": "RX J1615.3-3255",
                                 "notes": "panel label 'RXJ 1615'"}),
            "DoAr 44", "AS 209"],
           categories=("protoplanetary",),
           notes="membership complete (8/8; Fig. 1 labels: IM Lup, RXJ 1615, RU Lup, MY Lup, PDS 66, V4046 Sgr, DoAr 44, AS 209)"),

    # DETECTED disks only (32/43), from Garufi+2024 Fig. 2 (Imagery) + Table C.1 (disk
    # geometry = targets with measurable signal). Excluded (ambient-dominated or formal
    # non-detections): T Tau, XZ Tau, UY Aur, RY Tau, HP Tau, HN Tau, DS Tau, GK Tau,
    # DK Tau, V807 Tau, V1025 Tau.
    survey("SPHERE-Taurus", P_GARUFI_TAU, SPH_PDI,
           [
               "GM Aur", ("GG Tau", {"notes": "PI image (close binary)"}), "AB Aur",
               "RW Aur", "DG Tau", "UX Tau", "V409 Tau",
               ("MWC 758", {"wavelength_um": 2.18,
                            "wavelength_label": "K band 2.2 um (pol. intensity)"}),
               ("LkCa 15", {"wavelength_um": 1.25,
                            "wavelength_label": "J band 1.25 um (pol. intensity)"}),
               ("CQ Tau", {"wavelength_um": 1.25,
                           "wavelength_label": "J band 1.25 um (pol. intensity)"}),
               "IQ Tau", "DL Tau", "MWC 480", "DR Tau", "SU Aur", "V710 Tau",
               "DO Tau", "DM Tau",
               ("UZ Tau E", {"simbad": "UZ Tau", "notes": "panel label 'UZ Tau'; disk around UZ Tau E"}),
               "DQ Tau",
               ("CY Tau", {"wavelength_um": 2.18,
                           "wavelength_label": "K band 2.2 um (pol. intensity)"}),
               "BP Tau", "DH Tau", "CX Tau", "GI Tau", "HQ Tau", "DE Tau",
               "CW Tau", "CI Tau", "IP Tau", "V836 Tau", "DN Tau",
           ],
           region="Taurus", categories=("protoplanetary",),
           notes="detections only (32/43 observed); H band except CQ Tau+LkCa 15 (J) and MWC 758+CY Tau (K)"),
    survey("SPHERE-ChamI", P_GINSKI_CHA, SPH_PDI, [],
           region="Chamaeleon I", categories=("protoplanetary",),
           notes="stub — add detections from Ginski+2024"),
    survey("DESTINYS-Orion", P_VALEGARD_ORI, SPH_PDI, [],
           region="Orion", categories=("protoplanetary",),
           notes="stub — add detections from Valegard+2024"),

    # Membership completed from Schneider+2014 Table 1 (GO 12228): 10 debris disks
    # + 1 protoplanetary (MP Mus = PDS 66, imaged via staging; kept out of this debris block).
    # NOTE: HD 191089 was WRONGLY seeded here (not a Schneider+2014 target) — removed;
    # the stale hd-191089_stis-schneider14 record in data/systems needs deletion by the orchestrator.
    survey("STIS-Schneider14", P_SCHNEIDER14, STIS,
           ["HD 15115", "HD 15745", "HD 32297", "HD 53143", "HD 61005",
            "HD 92945", "HD 107146", "HD 139664", "HD 181327", "AU Mic"],
           categories=("debris",),
           notes="membership complete (10 debris + MP Mus/PDS 66 protoplanetary as 11th target)"),

    # Ren+2023 (2302.04273): uniform HST reprocessing of 23 debris disks,
    # STIS 0.58 um (MRDI) + NICMOS 1.12/1.60 um (NMF). Two records per target.
    # Membership completed from Fig. 2 (STIS) panel labels = Table 1 sample (23/23
    # shown): (a) 49 Ceti ... (w) TWA 25. Panel label "HD 141569" = HD 141569A.
    # NOTE: the 6 systems previously seeded here (GSC 07396-00759, HD 114082,
    # HD 117214, HD 129590, HD 146897, HD 106906) are NOT in this paper — they
    # belong to a different program (Ren AAS240 abstract 2022, "The Large-Scale
    # Structure of Debris Disks Newly Imaged with HST/STIS", unpublished); their
    # stale <sysid>_stis-ren pending records in data/systems need orchestrator
    # deletion or re-pointing to that paper once it appears.
    survey("STIS-Ren", P_REN_STIS, STIS,
           [
               ("49 Cet", {"notes": "panel label '49 Ceti'"}),
               ("AU Mic", {}), ("beta Pic", {}),
               "HD 377", "HD 15115", "HD 15745", "HD 30447", "HD 32297",
               "HD 35650", "HD 35841", "HD 61005", "HD 104860", "HD 110058",
               "HD 131835", "HD 141569", "HD 141943", "HD 181327", "HD 191089",
               "HD 192758", "HD 202917",
               ("HR 4796A", {"simbad": "HR 4796"}),
               ("TWA 7", {}), ("TWA 25", {}),
           ],
           categories=("debris",),
           notes="membership complete (23/23, Ren+2023 Fig. 2 = Table 1 sample)"),
    # NICMOS counterparts: Fig. 3 (F110W, 20 targets; blank cells = HD 35650,
    # TWA 7, TWA 25) + Fig. 4 (F160W, 13 targets). One record per system:
    # F110W crop where available, F160W crop for the 3 F110W-less targets.
    survey("NICMOS-Ren2023", P_REN_STIS,
           {"type": "disk_scattered", "facility": "HST", "instrument": "NICMOS",
            "wavelength_um": 1.12, "wavelength_label": "F110W 1.12 um (NMF reprocessing)",
            "technique": "RDI"},
           [
               ("49 Cet", {}), ("AU Mic", {}), ("beta Pic", {}),
               "HD 377", "HD 15115", "HD 15745", "HD 30447", "HD 32297",
               ("HD 35650", {"wavelength_um": 1.6,
                             "wavelength_label": "F160W 1.60 um (NMF reprocessing)"}),
               "HD 35841", "HD 61005", "HD 104860", "HD 110058",
               "HD 131835", "HD 141569", "HD 141943", "HD 181327", "HD 191089",
               "HD 192758", "HD 202917",
               ("HR 4796A", {"simbad": "HR 4796"}),
               ("TWA 7", {"wavelength_um": 1.6,
                          "wavelength_label": "F160W 1.60 um (NMF reprocessing)"}),
               ("TWA 25", {"wavelength_um": 1.6,
                           "wavelength_label": "F160W 1.60 um (NMF reprocessing)"}),
           ],
           categories=("debris",),
           notes="membership complete (23/23; F110W crops except HD 35650, TWA 7, TWA 25 = F160W-only, Fig. 4)"),

    # Ren+2023 SPHERE Ks star-hopping RDI: 15 disks with good total-intensity detections
    # (fig-K_Total-good gallery panel labels; SAO 206462 = HD 135344B).
    survey("SPHERE-Ks-RDI", P_REN_KS,
           {"type": "disk_scattered", "facility": "VLT-SPHERE", "instrument": "IRDIS Ks",
            "wavelength_um": 2.18, "wavelength_label": "Ks 2.2 um (total intensity, RDI)",
            "technique": "RDI"},
           ["CQ Tau", "HD 34282", "HD 97048", "HD 100453", "HD 100546", "HD 143006",
            "HD 169142", "LkCa 15", ("LkHa 330", {}), "MWC 758", "PDS 66",
            ("PDS 201", {}), ("HD 135344B", {}), ("SZ Cha", {}), "V1247 Ori"],
           categories=("protoplanetary",),
           notes="good-quality Ks RDI detections (15 targets, 18 epochs); panel label SAO 206462 -> HD 135344B"),

    survey("DISCS", P_DISCS, PDI_H, [],
           region="Sco-Cen", categories=("debris",),
           notes="stub — 4 newly resolved debris disks (2025)"),

    survey("SPHERE-debris-2025", P_SPHERE_DEBRIS25, SPH_PDI, [],
           categories=("debris",),
           notes="stub - Engler+2025: 51 resolved debris disks incl. new HD 36968, BD-20 951, HR 8799 & HD 36546 inner belts; AGENT: crop gallery, add members"),

    # ALICE: archival HST/NICMOS reprocessing (~400 targets). Disk images via the
    # science papers; HLSP at https://archive.stsci.edu/prepds/alice/ (host-fetch only).
    # Title verified from arXiv source ms.tex (1512.02220; emulateapj [apjl]);
    # crops = Fig. 2 leftmost column (NICMOS images): TWA 7/TWA 25/HD 35650 F160W,
    # HD 377 F110W.
    survey("ALICE", paper("Choquet", 2016,
                          "First images of debris disks around TWA 7, TWA 25, HD 35650, and HD 377",
                          "ApJL 817, L2", arxiv="1512.02220", bibcode="2016ApJ...817L...2C"),
           {"type": "disk_scattered", "facility": "HST", "instrument": "NICMOS",
            "wavelength_um": 1.1, "wavelength_label": "F110W 1.1 um (ALICE reprocessing)",
            "technique": "RDI"},
           [("TWA 25", {"wavelength_um": 1.6,
                        "wavelength_label": "F160W 1.6 um (ALICE reprocessing)"}),
            ("HD 35650", {"wavelength_um": 1.6,
                          "wavelength_label": "F160W 1.6 um (ALICE reprocessing)"}),
            ("HD 377", {}),
            ("TWA 7", {"wavelength_um": 1.6,
                       "wavelength_label": "F160W 1.6 um (ALICE reprocessing)"})],
           categories=("debris",),
           notes="4/4 first-image disks cropped (Choquet+2016 Fig. 2 NICMOS column). "
                 "Hagan+2018 'ALICE Data Release' (1802.07754) checked via ar5iv: technical "
                 "release paper, NO disk gallery figure — nothing to crop; the '12 disks "
                 "newly revealed by ALICE' (11 first-ever in scattered light) are Soummer+2014 "
                 "x5 (HD 30447, HD 35841, HD 141943, HD 191089, HD 202917), this paper x4, "
                 "Choquet+2017 49 Cet, Choquet+2018 x2 — ALL now covered by nicmos-ren2023 + "
                 "alice records. Choquet+2018 HD 104860/HD 192758 = arXiv 1801.05424 "
                 "(ApJ 854, 53; 2018ApJ...854...53C)."),

    # NACO/PIPPIN: uniform PDI reprocessing of the full NACO archive (57 YSOs).
    survey("NACO-PIPPIN", paper("de Regt", 2024,
                                "Polarimetric differential imaging with VLT/NACO. A comprehensive PDI pipeline for NACO data (PIPPIN)",
                                "A&A 684, A73", arxiv="2404.02222",
                                bibcode="2024A&A...684A..73D"),
           {"type": "disk_scattered", "facility": "VLT-NACO", "instrument": "NACO pol",
            "wavelength_um": 2.18, "wavelength_label": "Ks band (PIPPIN PDI reprocessing)",
            "technique": "PDI"},
           ["HD 135344B",
            ("HD 169142", {"wavelength_um": 1.65,
                           "wavelength_label": "H band (PIPPIN PDI reprocessing)"}),
            "HD 163296", "HD 97048",
            ("HR 4796A", {"simbad": "HR 4796", "categories": ["debris"]}),
            "TW Hya", "HD 100546", "HD 142527",
            ("Sz 91", {"region": "Lupus"}),
            "CR Cha",
            ("PDS 66", {"wavelength_um": 2.06, "alt_names": ["MP Mus"],
                        "wavelength_label": "IB_2.06 2.06 um (PIPPIN PDI reprocessing)"}),
            "AK Sco",
            ("Elias 25", {"simbad": "Elia 2-25", "region": "Ophiuchus"}),
            "SU Aur"],
           categories=("protoplanetary",),
           notes="14/22 Fig. 6 detections cropped (batch I) = all clean disks; the other 8 "
                 "panels (R CrA, Z CMa, Elia 2-29, Parsamian 21, R Mon, YLW 16A, Elia 2-21, "
                 "Mon R2 IRS 3) are envelopes/outflow nebulae, skipped. Bands per caption: "
                 "Ks except HD 169142 (H) and PDS 66 (IB_2.06; panel label 'MP Mus')."),

    # SEEDS summary gallery (Tamura 2016 review, Fig. 3: 20 panels / 19 systems,
    # AB Aur appears twice: wide + close-up, both Hashimoto+2011). Journal ref
    # verified from the Europe-PMC full text (PJAB 92(2), 45-55; PMC4906811;
    # doi 10.2183/pjab.92.45). Per-panel ORIGINAL citations (from the Fig. 3
    # caption) live in data/staging/seeds.json; panels credited "in prep." there
    # (LkHa 330 Bonnefoy, HD 142527 Fukagawa, GM Aur Oh) cite this review itself.
    survey("SEEDS", paper("Tamura", 2016,
                          "SEEDS - Strategic Explorations of Exoplanets and Disks with the Subaru Telescope",
                          "Proc. Japan Acad. Ser. B 92, 45", arxiv=None,
                          bibcode="2016PJAB...92...45T"),
           {"type": "disk_scattered", "facility": "Subaru-HiCIAO", "instrument": "HiCIAO",
            "wavelength_um": 1.65, "wavelength_label": "H band (PDI/ADI)",
            "technique": "PDI"},
           [("AB Aur", {"image_id": "ab-aur_seeds2011"}),          # crop exists
            ("HD 135344B", {"image_id": "hd-135344b_seeds2012"}),  # SAO 206462 panel; crop exists
            "MWC 758", "LkHa 330", "TW Hya", "PDS 70",
            ("Sz 91", {"region": "Lupus", "wavelength_um": 2.15,
                       "wavelength_label": "Ks band (PDI)"}),
            ("Oph IRS 48", {"alt_names": ["WLY 2-48"]}),           # caption name WLY 2-48
            "LkCa 15",
            ("HR 4796A", {"simbad": "HR 4796", "categories": ["debris"],
                          "wavelength_label": "H band (ADI)"}),
            "HD 142527", "HD 169142",
            ("RX J1604.3-2130", {"image_id": "rx-j1604-3-2130_seeds2012"}),  # filled batch I
            "GM Aur", "RY Tau",
            ("SR 21", {"region": "Ophiuchus"}),
            "MWC 480",
            "UX Tau",                                              # panel label UX Tau A
            ("HD 146897", {"alt_names": ["HIP 79977"], "categories": ["debris"],
                           "region": "Upper Sco",
                           "wavelength_label": "H band (ADI)"})],
           # NB 2026-07-06: HIP 79977 == HD 146897; the former duplicate system
           # was merged into hd-146897 (images hd-146897_seeds / _spherez2017).
           categories=("protoplanetary",),
           notes="COMPLETE 2026-07-06: all 20 Tamura 2016 Fig. 3 panels are in the atlas "
                 "(19 original-paper crops + ab-aur_seeds2011-closeup from Fig. 3 itself). "
                 "Good PDF: images/_sources/extra/tamura2016-seeds.pdf (Europe PMC render "
                 "of PMC4906811)."),
]

# --- individual classics -----------------------------------------------------
SYSTEMS = [
    system("HR 4796A", simbad="HR 4796", categories=("debris",), region="TW Hya assoc.",
           images=[
               img("gpi2015", "disk_scattered", "Gemini-GPI", "IFS pol", 2.05,
                   "K1 band 2.05 um pol. (GPI first light)", "PDI",
                   # ^ K1 (not H): all HR 4796A pol data in Perrin+2015 are K1 band
                   #   (Dec 2013 + Mar 2014 epochs); crop = Dec 2013 K1 pol. intensity.
                   paper("Perrin", 2015,
                         "Polarimetry with the Gemini Planet Imager: Methods, Performance at First Light, and the Circumstellar Ring around HR 4796A",
                         "ApJ 799, 182", arxiv="1407.2495", bibcode="2015ApJ...799..182P")),
               img("nicmos1999", "disk_scattered", "HST", "NICMOS", 1.1,
                   "1.1 um (discovery of scattered-light ring)", "coronagraphy",
                   paper("Schneider", 1999,
                         "NICMOS Imaging of the HR 4796A Circumstellar Disk",
                         "ApJL 513, L127", arxiv="astro-ph/9901218",
                         bibcode="1999ApJ...513L.127S")),
               # ^ title verified from arXiv source; crop = Fig. 1b (F110W 1.1 um;
               #   Fig. 1a is the 1.6 um F160W first-epoch image)
               img("stis2018", "disk_scattered", "HST", "STIS", 0.58,
                   "optical; exo-ring halo", "coronagraphy",
                   paper("Schneider", 2018,
                         "The HR 4796A Debris System: Discovery of Extensive Exo-Ring Dust Material",
                         "AJ 155, 77", arxiv="1712.08599", bibcode="2018AJ....155...77S")),
           ]),

    system("TW Hya", categories=("protoplanetary",),
           images=[
               img("sphere2017", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.62,
                   "H band 1.6 um (Qphi pol. intensity)", "PDI",
                   paper("van Boekel", 2017,
                         "Three radial gaps in the disk of TW Hydrae imaged with SPHERE",
                         "ApJ 837, 132", arxiv="1610.08939", bibcode=None)),
               # ^ title verified from arXiv source; crop = H-band Qphi panel of Fig. 2
               img("stis2013", "disk_scattered", "HST", "STIS", 0.58,
                   "optical coronagraphy (gap at 80 au)", "coronagraphy",
                   paper("Debes", 2013,
                         "The 0.5-2.22 um Scattered Light Spectrum of the Disk Around TW Hya: Detection of a Partially Filled Disk Gap at 80 AU",
                         "ApJ 771, 45", arxiv="1306.2969",
                         bibcode="2013ApJ...771...45D")),
               # ^ full title verified from arXiv source (not cropped yet)
           ]),

    system("PDS 70", categories=("protoplanetary",),
           images=[img("sphere2018", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.65,
                       "H band; gap + planet b", "ADI",
                       paper("Keppler", 2018,
                             "Discovery of a planetary-mass companion within the gap of the transition disk around PDS 70",
                             "A&A 617, A44", arxiv="1806.11568", bibcode="2018A&A...617A..44K"))]),

    system("Fomalhaut", categories=("debris",),
           images=[img("acs2005", "disk_scattered", "HST", "ACS", 0.7,
                       "optical (F606W+F814W); eccentric ring", "coronagraphy",
                       # ^ Methods: primary data F814W (833 nm) + F606W follow-up,
                       #   combined for the belt image (Fig. 1a = crop)
                       paper("Kalas", 2005,
                             "A planetary system as the origin of structure in Fomalhaut's dust belt",
                             "Nature 435, 1067", arxiv="astro-ph/0506574",
                             bibcode="2005Natur.435.1067K"))]),

    system("AU Mic", categories=("debris",),
           images=[
               img("acs2005", "disk_scattered", "HST", "ACS", 0.6,
                   "optical edge-on disk", "coronagraphy",
                   paper("Krist", 2005,
                         "HST/ACS Images of the AU Microscopii Debris Disk",
                         "AJ 129, 1008", arxiv=None, bibcode="2005AJ....129.1008K", verify=True)),
               img("sphere2015", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.65,
                   "H band; fast-moving features", "PDI",
                   paper("Boccaletti", 2015,
                         "Fast-moving features in the debris disk around AU Microscopii",
                         "Nature 526, 230", arxiv=None, bibcode="2015Natur.526..230B", verify=True)),
           ]),

    system("beta Pic", categories=("debris",),
           images=[img("gpi2015", "disk_scattered", "Gemini-GPI", "IFS pol", 1.65,
                       "H band pol.; edge-on inner disk", "PDI",
                       paper("Millar-Blanchaer", 2015,
                             "Beta Pictoris' Inner Disk in Polarized Light and New Orbital Parameters for beta Pictoris b",
                             "ApJ 811, 18", arxiv="1508.04787",
                             bibcode="2015ApJ...811...18M"))],
           # ^ title verified from arXiv source betapic_pol.tex (GPI H-band pol.;
           #   crop = Fig. 1 left, Q_r)
           notes="Original 1984 discovery image (Smith & Terrile, Las Campanas coronagraph) predates arXiv; add if desired."),

    system("HD 141569", categories=("protoplanetary", "debris"),
           images=[img("acs2003", "disk_scattered", "HST", "ACS", 0.6,
                       "optical; spiral ring system", "coronagraphy",
                       paper("Clampin", 2003,
                             "Hubble Space Telescope ACS Coronagraphic Imaging of the Circumstellar Disk around HD 141569A",
                             "AJ 126, 385", arxiv=None, bibcode="2003AJ....126..385C", verify=True))],
           notes="Hybrid disk (gas-rich debris / late transition)."),

    system("HD 34700", simbad="HD 34700", categories=("protoplanetary",),
           images=[img("gpi2019", "disk_scattered", "Gemini-GPI", "IFS pol", 1.65,
                       "H band pol.; spiral arms", "PDI",
                       paper("Monnier", 2019,
                             "Multiple spiral arms in the disk around intermediate-mass binary HD 34700A",
                             "ApJ 872, 122", arxiv="1901.02467", bibcode=None))]),
           # ^ title verified from arXiv source monnier.tex

    system("AB Aur", categories=("protoplanetary",),
           images=[
               img("seeds2011", "disk_scattered", "Subaru-HiCIAO", "HiCIAO", 1.65,
                   "H band PDI; double ring + spirals (SEEDS)", "PDI",
                   paper("Hashimoto", 2011,
                         "Direct Imaging of Fine Structures in Giant Planet Forming Regions of the Protoplanetary Disk around AB Aurigae",
                         "ApJL 729, L17", arxiv="1102.4408", bibcode=None)),
               img("sphere2020", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.65,
                   "H band; inner spiral 'twist'", "PDI",
                   paper("Boccaletti", 2020,
                         "Possible evidence of ongoing planet formation in AB Aurigae",
                         "A&A 637, L5", arxiv="2005.09064", bibcode=None)),
               # ^ both titles verified from arXiv sources (ms.tex / 38008corr.tex)
           ]),

    system("HD 135344B", alt_names=("SAO 206462",), categories=("protoplanetary",),
           images=[img("seeds2012", "disk_scattered", "Subaru-HiCIAO", "HiCIAO", 1.65,
                       "H band; discovery of spiral arms (SEEDS)", "PDI",
                       paper("Muto", 2012,
                             "Discovery of Small-Scale Spiral Structures in the Disk of SAO 206462 (HD 135344B): Implications for the Physical State of the Disk from Spiral Density Wave Theory",
                             "ApJL 748, L22", arxiv="1202.6139", bibcode=None))]),
           # ^ full title verified from arXiv source ms.tex

    system("MWC 758", categories=("protoplanetary",),
           images=[img("sphere2015", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.04,
                       "Y band; two-armed spiral", "PDI",
                       paper("Benisty", 2015,
                             "Asymmetric features in the protoplanetary disk MWC 758",
                             "A&A 578, L6", arxiv="1505.05325", bibcode=None))]),
           # ^ title verified from arXiv source letter-mwc758_vfinal.tex

    system("LkCa 15", categories=("protoplanetary",),
           planets=[planet("b", "disputed",
                           "Kraus & Ireland 2012 candidate; later work favors scattered light from inner disk")],
           images=[img("seeds2014", "disk_scattered", "Gemini-NIRI", "NIRI", 2.15,
                       "Ks band; gapped disk (PCA ref.-star subtraction)", "RDI",
                       paper("Thalmann", 2014,
                             "The architecture of the LkCa 15 transitional disk revealed by high-contrast imaging",
                             "A&A 566, A51", arxiv="1402.1766",
                             bibcode="2014A&A...566A..51T"))]),
    # ^ title verified from arXiv source ms.tex. NOTE: this paper's imaging is
    #   Gemini NIRI Ks (epochs K1-K4; crop = Fig. 2a PCA RefSub); the HiCIAO H
    #   data it re-uses are from Thalmann+2010. image_id kept as 'seeds2014'.

    system("RX J1604.3-2130", simbad="2MASS J16042165-2130284",
           categories=("protoplanetary",),
           images=[img("seeds2012", "disk_scattered", "Subaru-HiCIAO", "HiCIAO", 1.65,
                       "H band PDI; cavity + dips (SEEDS)", "PDI",
                       paper("Mayama", 2012,
                             "Subaru Imaging of Asymmetric Features in a Transitional Disk in Upper Scorpius",
                             "ApJL 760, L26", arxiv="1211.3284",
                             bibcode="2012ApJ...760L..26M"))]),
    # ^ title verified from arXiv source .TEX (not cropped yet)

    system("SU Aur", region="Taurus", categories=("protoplanetary",),
           images=[img("sphere2021", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.65,
                       "H band; infalling tails", "PDI",
                       paper("Ginski", 2021,
                             "Disk Evolution Study Through Imaging of Nearby Young Stars (DESTINYS): Late Infall Causing Disk Misalignment and Dynamic Structures in SU Aur",
                             "ApJL 908, L25", arxiv="2102.08781", bibcode=None))]),
           # ^ title verified from arXiv source sample63.tex

    system("HD 100453", categories=("protoplanetary",),
           images=[img("sphere2017", "disk_scattered", "VLT-SPHERE", "IRDIS DPI", 1.25,
                       "J band 1.25 um Qphi; two spirals driven by M-dwarf companion", "PDI",
                       paper("Benisty", 2017,
                             "Shadows and spirals in the protoplanetary disk HD 100453",
                             "A&A 597, A42", arxiv="1610.10089",
                             bibcode="2017A&A...597A..42B"))]),
    # ^ title verified from arXiv source; NIR pol. data are IRDIS J band (plus
    #   ZIMPOL R'/I'), not H — crop = Fig. 1 bottom-left (J Qphi)

    system("HD 97048", categories=("protoplanetary",),
           images=[img("sphere2016", "disk_scattered", "VLT-SPHERE", "IRDIS DPI", 1.25,
                       "J band 1.25 um Qphi (r2-scaled); multiple rings", "PDI",
                       paper("Ginski", 2016,
                             "Direct detection of scattered light gaps in the transitional disk around HD 97048 with VLT/SPHERE",
                             "A&A 595, A112", arxiv="1609.04027",
                             bibcode="2016A&A...595A.112G"))]),
    # ^ title verified from arXiv source; DPI data are J band (ADI was H2H3) —
    #   crop = Fig. 2 row 1 col 3 (Qphi r^2-scaled)

    system("HD 61005", alt_names=("The Moth",), categories=("debris",),
           images=[img("sphere2016", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.65,
                       "H band (ADI); swept-back wings", "ADI",
                       paper("Olofsson", 2016,
                             "Azimuthal asymmetries in the debris disk around HD 61005",
                             "A&A 591, A108", arxiv="1601.07861",
                             bibcode="2016A&A...591A.108O"))]),
    # ^ title verified from arXiv source The_Moth.tex (subtitle "A massive
    #   collision of planetesimals?"); crop = Fig. 1 IRDIS ADI H panel

    system("HD 106906", categories=("debris",),
           planets=[planet("b", "confirmed", "11 MJup companion at ~730 au, outside the disk")],
           images=[img("gpi2015", "disk_scattered", "Gemini-GPI", "IFS", 1.65,
                       "H band; asymmetric edge-on disk", "ADI",
                       paper("Kalas", 2015,
                             "Direct imaging of an asymmetric debris disk in the HD 106906 planetary system",
                             "ApJ 814, 32", arxiv="1510.02747",
                             bibcode="2015ApJ...814...32K"))]),
    # ^ title verified from arXiv source (not cropped yet)

    system("TWA 7", categories=("debris",),
           planets=[planet("b", "candidate", "JWST/MIRI point source in disk gap (Lagrange+2025)")],
           images=[img("stis2021", "disk_scattered", "HST", "STIS", 0.58,
                       "optical; face-on layered ring system", "coronagraphy",
                       paper("Ren", 2021,
                             "A Layered Debris Disk around M Star TWA 7 in Scattered Light",
                             "ApJ 914, 95", arxiv=None, bibcode=None, verify=True))]),
           # ^ WRONG arXiv id removed: 2104.10620 resolves to a graphene/STM condensed-matter
           #   paper (checked downloaded source). Find correct id for Ren+2021 (WebSearch).

    system("HD 110058", categories=("debris",),
           images=[img("sphere2023", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.65,
                       "H band; warped edge-on disk", "ADI",
                       paper("Stasevic", 2023,
                             "An inner warp discovered in the disk around HD 110058 using VLT/SPHERE and HST/STIS",
                             "A&A 678, A8", arxiv=None, bibcode=None, verify=True))]),
           # ^ WRONG arXiv id removed: 2309.01035 resolves to an AAAI-24 machine-learning
           #   paper (checked downloaded source). Find correct id for Stasevic+2023.

    system("HD 32297", categories=("debris",),
           images=[img("stis2005", "disk_scattered", "HST", "STIS", 0.58,
                       "optical; edge-on needle", "coronagraphy",
                       paper("Schneider", 2005,
                             "Discovery of a Nearly Edge-on Disk around HD 32297",
                             "ApJL 629, L117", arxiv=None, bibcode="2005ApJ...629L.117S", verify=True))]),

    system("HD 15115", categories=("debris",),
           images=[img("hst2007", "disk_scattered", "HST", "ACS", 0.6,
                       "optical (F606W); 'blue needle' asymmetric disk", "coronagraphy",
                       paper("Kalas", 2007,
                             "Discovery of Extreme Asymmetry in the Debris Disk Surrounding HD 15115",
                             "ApJL 661, L85", arxiv="0704.0645",
                             bibcode="2007ApJ...661L..85K"))]),
    # ^ title verified from arXiv source ms.tex; crop = Fig. 1 left (ACS/HRC F606W)

    system("HD 181327", categories=("debris",),
           images=[img("nicmos2006", "disk_scattered", "HST", "NICMOS", 1.1,
                       "1.1 um; bright ring", "coronagraphy",
                       paper("Schneider", 2006,
                             "Discovery of an 86 AU Radius Debris Ring around HD 181327",
                             "ApJ 650, 414", arxiv="astro-ph/0606213",
                             bibcode="2006ApJ...650..414S"))]),
    # ^ title verified from arXiv source; crop = Fig. 2a (NICMOS 1.1 um combined image)

    system("HD 202628", categories=("debris",),
           images=[img("stis2012", "disk_scattered", "HST", "STIS", 0.58,
                       "optical; eccentric ring", "coronagraphy",
                       paper("Krist", 2012,
                             "Hubble Space Telescope Observations of the HD 202628 Debris Disk",
                             "AJ 144, 45", arxiv="1206.2078", bibcode=None))]),
           # ^ title verified from arXiv source hd202628_final.tex

    system("HD 53143", categories=("debris",),
           images=[img("acs2006", "disk_scattered", "HST", "ACS", 0.6,
                       "optical ring", "coronagraphy",
                       paper("Kalas", 2006,
                             "First Scattered Light Images of Debris Disks around HD 53143 and HD 139664",
                             "ApJL 637, L57", arxiv="astro-ph/0601488",
                             bibcode="2006ApJ...637L..57K"))]),
    # ^ title verified from arXiv source ms.tex; crop = Fig. 1a (ACS/HRC F606W)

    system("HD 139664", categories=("debris",),
           images=[img("acs2006", "disk_scattered", "HST", "ACS", 0.6,
                       "optical edge-on disk", "coronagraphy",
                       paper("Kalas", 2006,
                             "First Scattered Light Images of Debris Disks around HD 53143 and HD 139664",
                             "ApJL 637, L57", arxiv="astro-ph/0601488",
                             bibcode="2006ApJ...637L..57K"))]),
    # ^ same paper as HD 53143; crop = Fig. 1b

    system("GG Tau", region="Taurus", categories=("protoplanetary",),
           images=[img("sphere2020", "disk_scattered", "VLT-SPHERE", "IRDIS", 1.65,
                       "H band pol.; circumbinary ring + streamers", "PDI",
                       paper("Keppler", 2020,
                             "Gap, shadows, spirals, and streamers: SPHERE observations of binary-disk interactions in GG Tau A",
                             "A&A 639, A62", arxiv="2005.09037", bibcode=None))]),
    # ^ title verified from arXiv source GGTau.tex ("...spirals, and streamers ... GG Tau A")

    system("HD 163296", categories=("protoplanetary",),
           images=[img("stis2000", "disk_scattered", "HST", "STIS", 0.58,
                       "optical; disk + HH knots", "coronagraphy",
                       paper("Grady", 2000,
                             "STIS Coronagraphic Imaging of the Herbig Ae Star: HD 163296",
                             "ApJ 544, 895", arxiv=None, bibcode="2000ApJ...544..895G", verify=True))]),

    system("HD 100546", categories=("protoplanetary",),
           images=[img("acs2007", "disk_scattered", "HST", "ACS", 0.6,
                       "optical; disk with dark lane", "coronagraphy",
                       paper("Ardila", 2007,
                             "A Resolved Debris Disk around the G2V star HD 107146 (VERIFY - intended: Ardila+2007 HD 100546 ACS paper)",
                             "ApJ", arxiv=None, bibcode=None, verify=True))]),
]
