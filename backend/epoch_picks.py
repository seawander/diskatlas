#!/usr/bin/env python3
"""Curated, source-verified observation epochs.

Each date below was read out of the record's own source paper (arXiv), matched to
that record's INSTRUMENT (a multi-instrument paper observes different cameras on
different nights, so the pick is per-instrument, not per-paper). Dates are given
at the precision the source states unambiguously; where only the campaign
month/year is clean, the month/year is used. Records whose obs date could not be
tied to the instrument with confidence are left out (epoch_audit tracks them).

Two maps:
  BY_ARXIV  applies to every epoch-less record of that paper (single-instrument
            papers, or same-night/same-year campaigns where all records share a date).
  BY_ID     overrides BY_ARXIV for a specific image_id (mixed-instrument papers).

Usage:  python3 backend/epoch_picks.py [--apply]
"""
import argparse, glob, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BY_ARXIV = {
    # --- single-instrument papers -------------------------------------------
    "0704.0645": "2007 Jan",      # hd-15115  HST/ACS
    "0712.0378": "2006 Jul 17",   # hd-15745  HST/ACS
    "0811.1994": "2004 Oct 25",   # fomalhaut HST/ACS
    "0809.2812": "2006 Feb 17",   # ct-cha    VLT/NACO
    "1005.5162": "2009 Dec 26",   # lkca-15   Subaru/HiCIAO
    "1008.2793": "2006 May 3",    # hd-207129 HST/ACS coronagraph
    "1102.4408": "2009 Oct 31",   # ab-aur    Subaru/HiCIAO (x2)
    "1107.1057": "2005 Jan 24",   # hd-107146 HST/NICMOS
    "1110.2488": "2011 May 24",   # hr-4796a  Subaru/HiCIAO
    "1202.6139": "2011 May 20",   # hd-135344b Subaru/HiCIAO
    "1205.3159": "2010 Jan 24",   # mwc-480   Subaru/HiCIAO
    "1206.1215": "2009 Dec 23",   # ux-tau    Subaru/HiCIAO
    "1206.2078": "2011 May 15",   # hd-202628 HST/STIS
    "1208.2075": "2012 Feb 28",   # pds-70    Subaru/HiCIAO (PDI)
    "1210.5252": "2006 May",      # as-209    SMA 0.88mm
    "1211.3744": "2012 Jan 1",    # kappa-and Subaru/HiCIAO (first detection)
    "1211.5148": "2012 Apr 23",   # au-mic    ALMA Band 6
    "1212.1466": "2012 Mar 11",   # mwc-758   Subaru/HiCIAO
    "1302.5705": "2011 Mar 29",   # sr-21     Subaru/HiCIAO
    "1305.6062": "2012 Jun 2",    # hd-142527 ALMA Band 7
    "1305.7428": "2012 Jan 11",   # hd-95086  VLT/NACO (epoch 1)
    "1306.1887": "2011 Jan 27",   # ry-tau    Subaru/HiCIAO
    "1307.2886": "2011 Mar 26",   # gj-504    Subaru/HiCIAO (H-band discovery)
    "1312.1265": "2013 Apr 7",    # hd-106906 MagAO/Clio2
    "1401.3343": "2012 Nov 4",    # hd-32297  LBTI/LMIRCam
    "1402.1538": "2012 May",      # sz-91     Subaru/HiCIAO
    "1404.1380": "2012 Nov 16",   # beta-pic  ALMA Band 7
    "1405.6542": "2012 Nov 18",   # hd-100546 ALMA Band 7
    "1412.6989": "2013 Oct",      # hr-8799   LBTI/LMIRCam
    "1503.02649": "2014 Oct 14",  # hl-tau    ALMA (all bands, same SV campaign)
    "1505.04937": "2011 May 23",  # hd-169142 Subaru/HiCIAO
    "1601.07861": "2015 May 1",   # hd-61005  SPHERE/IRDIS (dual pol)
    "1603.04853": "2015 Jan",     # hr-8799   ALMA Band 6
    "1605.01453": "2013 Nov 23",  # v1247-ori Subaru/HiCIAO
    "1606.00039": "2015 May 26",  # hd-207129 HST/STIS
    "1606.03118": "2014 Oct 14",  # xz-tau    ALMA
    "1611.01168": "2013 Dec 15",  # eta-crv   ALMA Band 7
    "1702.02844": "2015 Aug 30",  # hd-169142 ALMA Band 6
    "1704.01972": "2013 Nov 4",   # 49-cet    ALMA Band 7
    "1705.05867": "2015 Dec 29",  # fomalhaut ALMA Band 6
    "1709.00417": "2015 Apr 24",  # hd-146897 SPHERE/ZIMPOL
    "1710.05028": "2015 Nov 16",  # v1247-ori ALMA Band 7
    "1805.12141": "2017 Nov 12",  # mwc-758   ALMA Band 7
    "1806.11568": "2016 Mar 25",  # pds-70    SPHERE/IRDIS (J-band)
    "1809.01082": "2016 Jun 30",  # hd-143006 SPHERE/IRDIS DPI
    "1809.10254": "2014 Dec",     # ngc-1068  SPHERE/IRDIS (x2)
    "1810.09457": "2017 Sep 8",   # kappa-and SCExAO/CHARIS
    "1811.08439": "2017 Mar",     # hd-131835 ALMA Band 8
    "1901.01406": "2016 Dec 18",  # hd-92945  ALMA Band 7
    "1901.02467": "2018 Jan 3",   # hd-34700  GPI/IFS pol
    "1903.11903": "2018 Aug 28",  # hr-8799   VLTI/GRAVITY
    "1904.02746": "2016 May 31",  # hd-141943 SPHERE/IRDIS
    "1905.08258": "2016 Jan 1",   # hd-15115  ALMA Band 6
    "1905.09204": "2016 Nov 5",   # cx-tau    ALMA Band 6
    "1906.06305": "2017 Sep",     # hd-100546 ALMA Band 6
    "1911.10853": "2017 Mar 13",  # doar-25   SPHERE/IRDIS
    "1912.01361": "2018 Nov 20",  # ngc-1068  VLTI/GRAVITY
    "2004.03135": "2017 Dec 10",  # gw-ori    ALMA Band 6
    "2004.09597": "2019 Jun 8",   # pds-70    Keck/NIRC2 vortex
    "2005.09037": "2016 Nov 18",  # gg-tau    SPHERE/IRDIS
    "2005.09064": "2019 Dec",     # ab-aur    SPHERE/IRDIS (x2, polarimetry)
    "2007.10991": "2020 Feb 16",  # yses-1    SPHERE/IRDIS
    "2011.00044": "2020 May 31",  # sr-21     Keck/NIRC2 (PWFS)
    "2102.05159": "2019 May 23",  # alpha-cen-a VLT/NEAR-VISIR
    "2102.06339": "2016 Sep",     # ngc-1068  SPHERE/IRDIS DPI
    "2104.08285": "2018 Apr 30",  # yses-2    SPHERE/IRDIS
    "2107.13560": "2018 Jun 21",  # waoph-6   SPHERE/IRDIS DPI
    "2108.07123": "2019 Jul 27",  # pds-70    ALMA Band 7
    "2109.08984": "2019 Jan 12",  # hd-36546  SCExAO/CHARIS
    "2204.00640": "2019 Jun 8",   # oph-163131 ALMA Band 6 (x2)
    "2301.01684": "2019 Apr 4",   # rx-j1604  ALMA Band 6 (epoch 1)
    "2302.05420": "2021 Dec 21",  # af-lep    Keck/NIRC2
    "2302.06332": "2022 Oct 20",  # af-lep    SPHERE/IRDIS
    "2308.05613": "2015 Apr 3",   # hd-110058 SPHERE/IRDIS
    "2401.02830": "2022 Sep 30",  # mwc-758   JWST/NIRCam
    "2410.00156": "2023 Mar 7",   # oph-163131 JWST NIRCam+MIRI (same visits)
    "2410.23636": "2023 Aug 18",  # vega      JWST/MIRI (x2, same run)
    "2503.01599": "2023 Jul 3",   # eps-ind-a JWST/MIRI
    "2505.08863": "2023 Sep 6",   # hd-181327 JWST/NIRSpec IFU
    "2506.09201": "2024 May 18",  # 14-her    JWST/NIRCam
    "2508.18456": "2022 Nov 19",  # wispit-1  SPHERE/IRDIS (epoch 1)
    "2508.19053": "2023 Oct 19",  # wispit-2  SPHERE/IRDIS (epoch 1)
    "2510.20216": "2024 Jun 14",  # twa-20    JWST/NIRCam
    "2512.02159": "2022 Dec 30",  # hip-54515 SCExAO/CHARIS (epoch 1)
    "2603.08780": "2025 May 10",  # eps-ind-a JWST/MIRI (4QPM)
    "2606.23480": "2025 Apr 8",   # hr-4796a  MagAO-X (g' first night)
    # --- multi-instrument, but same year for every record (year-level safe) --
    "2208.14990": "2022",         # hip-65426 JWST ERS (NIRCam+MIRI, 2022)
    "2305.03789": "2022 Oct 22",  # fomalhaut JWST/MIRI (all same visit)
    "2309.07040": "2023 Jan 23",  # tau-042021 JWST NIRCam+MIRI (same visits)
    "2504.13679": "2023 May 16",  # hd-106906 JWST/MIRI (x2)
    "2412.07523": "2023 Jan 23",  # hh-30     JWST NIRCam+MIRI
    "2511.07561": "2024 May 20",  # hd-92945  JWST/NIRCam
    # --- famous single-record picks -----------------------------------------
    "1508.03084": "2014 Dec 18",  # 51-eri    GPI/IFS (first observation)
    "1508.04787": "2013 Dec 12",  # beta-pic  GPI/IFS pol
    "1006.3314": "2009 Oct",      # beta-pic  VLT/NACO (b recovery)
    "1807.00657": "2015 May 6",   # gj-504    SPHERE/IRDIS
    "2204.00633": "2016 Sep 9",   # ab-aur    SCExAO/CHARIS (best epoch)
    "2402.09505": "2022 Jan 8",   # 3c-273    HST/STIS
}

BY_ID = {
    # mixed-instrument papers: per-record obs date
    "beta-pic_jwst-miri": "2022 Dec 13",
    "beta-pic_jwst-nircam-f182m": "2023 Mar 18",
    "beta-pic_jwst-nircam-f210m": "2023 Mar 18",
    "beta-pic_jwst-nircam-f250m": "2023 Mar 18",
    "beta-pic_jwst-nircam-f300m": "2023 Mar 18",
    "beta-pic_jwst-nircam-f335m": "2023 Mar 18",
    "beta-pic_jwst-nircam-f444w": "2023 Mar 18",
    "kappa-and_nirc22014-ks": "2012 Nov 3",
    "kappa-and_nirc22014-lp": "2012 Nov 3",
    "hd-34700_scexao2023": "2019 Oct 27",     # 2310.16873 IRDIS DPI
    "hd-34700_lbti2024": "2022 Feb 14",       # 2310.16873 LBTI/LMIRCam
    "hd-106906_acs2015": "2004 Dec 1",        # 1510.02747 archival ACS
    "ux-tau_sphere-menard2020-j": "2017 Oct 6",  # 2006.02439 IRDIS
    "ux-tau_alma-menard2020": "2016 Aug 10",     # 2006.02439 ALMA
    "doar-44_casassus-sphere": "2016 Mar 15", # 1804.02360 IRDIS
    "doar-44_casassus-alma": "2014 Jul 26",   # 1804.02360 ALMA Band 7
    "lkha-330_sphere-pinilla22": "2017 Oct 5",# 2206.09975 IRDIS DPI
    "pds-70_muse2019": "2018 Jun 20",         # 1906.01486 MUSE NFM
    "hip-53005_scexao-uyama26": "2021 May 9", # 2604.03767 CHARIS
    "hip-53005_nirc2-2024": "2024 Jan 22",    # 2604.03767 Keck/NIRC2
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    w = skipped = 0
    for f in sorted((ROOT / "data" / "systems").glob("*.json")):
        d = json.loads(f.read_text())
        changed = False
        for im in d.get("images", []):
            if im.get("epoch"):
                continue
            iid = im.get("image_id")
            ax = im.get("paper", {}).get("arxiv")
            e = BY_ID.get(iid) or (BY_ARXIV.get(ax) if ax else None)
            if e:
                if a.apply:
                    im["epoch"] = e
                    changed = True
                w += 1
        if changed:
            f.write_text(json.dumps(d, indent=1, ensure_ascii=False))
    print(f"{'applied' if a.apply else 'would apply'} curated obs epoch to {w} records")


if __name__ == "__main__":
    main()
