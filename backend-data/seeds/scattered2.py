"""Seed blocks added by ingest agents (Engler+2025, DESTINYS ChamI/Orion, DISCS, NACO-PIPPIN...).
Same structures as scattered.py. Owned by Batch F agent.

Membership below was read off the actual gallery figures (panel labels = ground truth):
 - Engler+2025 (2512.03128): Fig. 5a/5b (36 Qphi panels, PDF pages 9-10) + Fig. 2a/2b
   (39 total-intensity panels, PDF pages 6-7); union = 50 unique systems. Systems with a
   Qphi panel are seeded in the PDI block; the 14 systems detected in total intensity only
   are seeded in the ADI block. Crops: backend-data/manifests/sphere-f/engler-p[1-4].json.
 - Ginski+2024 ChamI (2403.02149): Fig. 2 (ChaI-gallery.pdf), 13 detection panels.
 - Valegard+2024 Orion (2403.02156): Fig. 2 (detected-disks-orion.pdf), 10 detections.
 - Hom+2025 DISCS (2505.02976): Fig. 1 (Qr_image_all_v3.pdf), 4 resolved of 7 observed.
"""
from .util import survey, paper

# --- papers (verified against the arXiv sources) -----------------------------
P2_ENGLER25 = paper("Engler", 2025,
                    "Characterization of debris disks observed with SPHERE",
                    "A&A 704, A21", arxiv="2512.03128")
# ^ title verified from PDF page 1 (2512.03128.pdf); A&A 704, A21 (2025).
P2_GINSKI_CHA = paper("Ginski", 2024,
                      "The SPHERE view of the Chamaeleon I star-forming region: The full census of planet-forming disks with GTO and DESTINYS programs",
                      "A&A 685, A52", arxiv="2403.02149", bibcode="2024A&A...685A..52G")
P2_VALEGARD_ORI = paper("Valegard", 2024,
                        "Disk Evolution Study Through Imaging of Nearby Young Stars (DESTINYS): The SPHERE view of the Orion star-forming region",
                        "A&A 685, A54", arxiv="2403.02156", bibcode="2024A&A...685A..54V")
P2_DISCS = paper("Hom", 2025,
                 "The Disks In Scorpius-Centaurus Survey (DISCS) I: Four Newly-Resolved Debris Disks in Polarized Intensity Light",
                 "AJ, in press", arxiv="2505.02976")
# ^ first author verified from source (scocenauthors2.txt): Justin Hom (Crotts is 3rd
#   author — the P_DISCS stub in scattered.py has the wrong first author).
#   "\accepted{May 1, 2025, The Astronomical Journal}".

SPH_PDI_H = {"type": "disk_scattered", "facility": "VLT-SPHERE", "instrument": "IRDIS DPI",
             "wavelength_um": 1.65, "wavelength_label": "H band 1.6 um (pol. intensity)",
             "technique": "PDI"}
SPH_TOTI_H = {"type": "disk_scattered", "facility": "VLT-SPHERE", "instrument": "IRDIS/IFS",
              "wavelength_um": 1.65, "wavelength_label": "H band 1.6 um (total intensity)",
              "technique": "ADI"}
GPI_PDI_H = {"type": "disk_scattered", "facility": "Gemini-GPI", "instrument": "IFS pol",
             "wavelength_um": 1.65, "wavelength_label": "H band 1.6 um (Qr pol. intensity)",
             "technique": "PDI"}

BLOCKS = [
    # ------------------------------------------------------------------ Engler+2025
    # Members with a polarized-intensity panel (Fig. 5a+5b; 36 systems).
    # Panel labels are HD numbers; classics mapped to existing ids:
    # HD 9672=49 Cet, HD 39060=beta Pic, HD 109573=HR 4796A, HD 172555=HR 7012,
    # HD 197481=AU Mic, HD 218396=HR 8799.
    survey("SPHERE-debris-2025", P2_ENGLER25, SPH_PDI_H,
           [
               "HD 377",
               ("49 Cet", {"alt_names": ("HD 9672",)}),
               "HD 15115", "HD 30447", "HD 32297", "HD 35841",
               "HD 36968",          # NEW detection (resolved for the first time)
               "HD 38397",
               ("beta Pic", {"alt_names": ("HD 39060",)}),
               "HD 61005",
               ("HD 98800", {"instrument": "ZIMPOL",
                             "wavelength_um": 0.63,
                             "wavelength_label": "ZIMPOL R' 0.63 um (pol. intensity)"}),
               # ^ smallest disk of the sample (R~3 au around the B binary);
               #   Fig. 5 panel is the ZIMPOL R_PRIME Qphi image (scale bar 0.5").
               "HD 106906",
               ("HR 4796A", {"simbad": "HR 4796", "alt_names": ("HD 109573",)}),
               "HD 114082", "HD 115600", "HD 117214", "HD 120326", "HD 121617",
               "HD 129590", "HD 131835", "HD 141569",
               ("HD 145560", {"instrument": "ZIMPOL",
                              "wavelength_um": 0.735,
                              "wavelength_label": "ZIMPOL VBB 0.74 um (pol. intensity)"}),
               "HD 146897", "HD 156623", "HD 157587", "HD 160305",
               ("HR 7012", {"instrument": "ZIMPOL",
                            "wavelength_um": 0.735,
                            "wavelength_label": "ZIMPOL VBB 0.74 um (pol. intensity)",
                            "alt_names": ("HD 172555",)}),
               # ^ warm ~10 au belt detected with ZIMPOL (Engler et al. 2018).
               "HD 181327", "HD 191089", "HD 192758",
               ("AU Mic", {"alt_names": ("HD 197481",)}),
               "HD 202917",
               ("HR 8799", {"alt_names": ("HD 218396",)}),
               ("BD-20 951", {}),   # NEW detection (resolved for the first time)
               "TWA 7",
               ("GSC 07396-00759", {}),
           ],
           categories=("debris",),
           notes=None),
    # Members detected in TOTAL intensity only (Fig. 2a+2b; no Fig. 5 panel; 14 systems).
    survey("SPHERE-debris-2025", P2_ENGLER25, SPH_TOTI_H,
           [
               "HD 105", "HD 16743",
               "HD 36546",          # incl. newly resolved inner belt (~55 au)
               "HD 38206", "HD 92945", "HD 110058", "HD 111520", "HD 112810",
               "HD 131488", "HD 141011", "HD 141943", "HD 146181", "HD 182681",
               "TWA 25",
           ],
           categories=("debris",),
           notes="Engler+2025 total-intensity-only detections (Fig. 2); '51 debris disks' resolved in the 161-star archival SPHERE sample (multi-belt bookkeeping); gallery union = 50 unique systems, all cropped (36 PDI + 14 total-intensity)"),

    # ------------------------------------------------------------- DESTINYS Cham I
    # 13 systems with extended circumstellar dust in Fig. 2 (ChaI-gallery.pdf);
    # 12 are disk detections, CHX 22 shows a companion-shaped tail-like structure
    # (Zhang+2023) and is kept with a caveat note. H band except HD 97048 + SY Cha
    # (K band) and CS Cha + CV Cha (J band).
    survey("SPHERE-ChamI", P2_GINSKI_CHA, SPH_PDI_H,
           [
               ("Sz 45", {}),
               ("CV Cha", {"wavelength_um": 1.25,
                           "wavelength_label": "J band 1.25 um (Qphi pol. intensity)"}),
               "VZ Cha", "CT Cha", "CR Cha",
               ("SY Cha", {"wavelength_um": 2.18,
                           "wavelength_label": "K band 2.2 um (Qphi pol. intensity)"}),
               ("CHX 22", {}),      # tail-like structure around close binary, not a
                                    # regular disk (Zhang et al. 2023)
               "WW Cha",
               ("HD 97048", {"wavelength_um": 2.18,
                             "wavelength_label": "K band 2.2 um (Qphi pol. intensity)"}),
               ("HP Cha", {}),      # circumprimary disk; B/C companions in panel
               ("CS Cha", {"wavelength_um": 1.25,
                           "wavelength_label": "J band 1.25 um (Qphi pol. intensity)"}),
               "TW Cha", "SZ Cha",
           ],
           region="Chamaeleon I", categories=("protoplanetary",),
           notes="detections only (13/20 with extended signal; 12 disks + CHX 22 tail); crops from Fig. 2 mosaic"),

    # -------------------------------------------------------------- DESTINYS Orion
    # All 10 disks detected in SPHERE H-band Qphi (Fig. 2 = detected-disks-orion.pdf):
    # 3 bright (V351 Ori = PDS 201, V599 Ori, V1012 Ori) + 7 faint.
    survey("DESTINYS-Orion", P2_VALEGARD_ORI, SPH_PDI_H,
           [
               "HD 294260", "HD 294268", "PDS 110", "PDS 113", "RV Ori",
               "V1012 Ori", "V1650 Ori",
               ("PDS 201", {"alt_names": ("V351 Ori",)}),  # panel label 'V351Ori'
               "V599 Ori", "V606 Ori",
           ],
           region="Orion", categories=("protoplanetary",),
           notes="detections only (10/23 observed); Fig. 2 gallery panel labels"),

    # ------------------------------------------------------------------------ DISCS
    # GPI (Gemini-South) H-band pol.; 7 new Sco-Cen targets observed, 4 disks resolved:
    # HD 98363, HD 109832, HD 146181 for the first time ever, HD 112810 for the first
    # time in polarized intensity. (HD 108904, HD 119718 non-detections; HD 113556 only
    # a tentative arc hint — excluded.)
    survey("DISCS", P2_DISCS, GPI_PDI_H,
           ["HD 98363", "HD 109832", "HD 112810", "HD 146181"],
           region="Sco-Cen", categories=("debris",),
           notes="4 resolved disks of DISCS I (Fig. 1 Qr gallery); GPI H-band PDI"),
]

SYSTEMS = []
