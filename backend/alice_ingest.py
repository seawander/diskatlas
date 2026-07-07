#!/usr/bin/env python3
"""Ingest ALICE HLSP combined-coadd previews for atlas systems.

ALICE (Archival Legacy Investigations of Circumstellar Environments) re-processed
~400 HST/NICMOS coronagraphic targets; STScI hosts per-target combined-coadd PNGs:
  https://archive.stsci.edu/missions/hlsp/alice/<prog>/<target>/<filt>/preview/
      hlsp_alice_hst_nicmos_<prog>-<target>_<filt>_v1_combined.png

This script (idempotent):
 1. appends download lines for the cross-matched targets to backend/fetch_extra.txt
    (host fetch -> images/_sources/alice/<sysid>_<filt>.png);
 2. adds a pending image record per (system, filter) to data/systems/<id>.json;
 3. after the host run, `--attach` downsizes the PNGs into images/<sysid>/ and
    fills the records' file fields.

Cross-match table below: (program, alice-target, filter, system_id).
Curated 2026-07-06 from the full target_pages listing vs. the 273-system atlas.
"""
import json
import sys
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / "data" / "systems"
EXTRA = Path(__file__).parent / "fetch_extra.txt"
TODAY = datetime.date.today().isoformat()

WL = {"f110w": (1.1, "F110W 1.1 um"), "f160w": (1.6, "F160W 1.6 um"),
      "f165m": (1.65, "F165M 1.65 um"), "f171m": (1.71, "F171M 1.71 um"),
      "f180m": (1.8, "F180M 1.80 um"), "f204m": (2.04, "F204M 2.04 um"),
      "f212n": (2.12, "F212N 2.12 um"), "f222m": (2.22, "F222M 2.22 um")}

# (program, target-slug-in-archive, filter, atlas system_id)
M = [
    (10177, "aa-tau", "f160w", "aa-tau"),
    (7233, "49-cet", "f110w", "49-cet"),
    (7248, "beta-pic-disk", "f160w", "beta-pic"),
    (10177, "bp-tau", "f110w", "bp-tau"),
    (10177, "ci-tau", "f110w", "ci-tau"),
    (10177, "cq-tau", "f110w", "cq-tau"),
    (10177, "cy-tau", "f110w", "cy-tau"),
    (10177, "dl-tau", "f160w", "dl-tau"),
    (10177, "dm-tau", "f160w", "dm-tau"),
    (7418, "do-tau", "f160w", "do-tau"),
    (10177, "doar-25", "f160w", "doar-25"),
    (10177, "dq-tau", "f110w", "dq-tau"),
    (7829, "dr-tau", "f212n", "dr-tau"),
    (10228, "gj803", "f160w", "au-mic"),
    (10852, "gm-aur", "f110w", "gm-aur"),
    (10177, "go-tau", "f160w", "go-tau"),
    (7226, "hd105", "f160w", "hd-105"),
    # (10527, "hd-104860", "f110w", "hd-104860"),  # no preview in archive
    (10177, "hd107146", "f110w", "hd-107146"),
    (10177, "hd135344", "f110w", "hd-135344b"),
    (7226, "hd141569", "f110w", "hd-141569"),
    (11155, "hd142527", "f110w", "hd-142527"),
    (10177, "hd142666", "f110w", "hd-142666"),
    (10849, "hd-143006", "f110w", "hd-143006"),
    (10540, "hd15115", "f110w", "hd-15115"),
    (10177, "hd15745", "f110w", "hd-15745"),
    (10177, "hd163296", "f110w", "hd-163296"),
    (10177, "hd164249", "f110w", "hd-164249"),
    (10177, "hd169142", "f110w", "hd-169142"),
    (10540, "hd170773", "f110w", "hd-170773"),
    (10177, "hd181327", "f110w", "hd-181327"),
    (10527, "hd-191089", "f110w", "hd-191089"),
    (10849, "hd-202917", "f110w", "hd-202917"),
    (10177, "hd30447", "f110w", "hd-30447"),
    (10177, "hd32297", "f110w", "hd-32297"),
    (10177, "hd35841", "f110w", "hd-35841"),
    (10177, "hd36112", "f110w", "mwc-758"),
    (10527, "hd-377", "f110w", "hd-377"),
    (10599, "hd-53143", "f110w", "hd-53143"),
    (10599, "hd-139664", "f110w", "hd-139664"),
    (10527, "hd-61005", "f110w", "hd-61005"),
    (10177, "hd92945", "f110w", "hd-92945"),
    (11155, "hd97048", "f110w", "hd-97048"),
    (11155, "hd100546", "f110w", "hd-100546"),
    (10244, "hd109085", "f160w", "eta-crv"),
    (10527, "hd-141943", "f110w", "hd-141943"),
    (11155, "hd31293", "f110w", "ab-aur"),
    (10167, "hr4796a", "f171m", "hr-4796a"),
    (7226, "hr8799", "f160w", "hr-8799"),
    (10177, "lkca-15", "f110w", "lkca-15"),
    (10527, "pds-66", "f110w", "pds-66"),
    (10177, "ry-tau", "f110w", "ry-tau"),
    (10849, "rx-j1842.9-3532", "f110w", "rx-j1842-9-3532"),
    (10849, "rx-j1852.3-3700", "f110w", "rx-j1852-3-3700"),
    (10177, "sz-82", "f160w", "im-lup"),
    (7226, "tw-hydrae", "f110w", "tw-hya"),
    (7226, "twa7", "f165m", "twa-7"),
    (10176, "twa25", "f160w", "twa-25"),
    (10177, "uz-tau-e", "f110w", "uz-tau-e"),
    (10177, "v1121-oph", "f110w", "as-205"),
    (7226, "hd35850", "f160w", "af-lep"),
    (10176, "tyc9340-0437", "f160w", "tyc-9340-437-1"),
]

PAPER = {"first_author": "Hagan", "year": 2018,
         "title": "ALICE Data Release: A revaluation of HST-NICMOS coronagraphic images",
         "journal": "AJ 155, 179", "arxiv": "1802.07754", "bibcode": None}


def url(prog, tgt, filt):
    return (f"https://archive.stsci.edu/missions/hlsp/alice/{prog}/{tgt}/{filt}/"
            f"preview/hlsp_alice_hst_nicmos_{prog}-{tgt}_{filt}_v1_combined.png")


def dest(sid, filt):
    return f"images/_sources/alice/{sid}_{filt}.png"


def main():
    attach = "--attach" in sys.argv
    lines = EXTRA.read_text().splitlines()
    have = set(lines)
    added_fetch = added_rec = attached = 0

    if not attach:
        out = ["", "# --- ALICE HLSP combined coadds (auto: backend/alice_ingest.py) ---"]
        for prog, tgt, filt, sid in M:
            line = f"{url(prog, tgt, filt)}\t{dest(sid, filt)}"
            if line not in have:
                out.append(line)
                added_fetch += 1
        if added_fetch:
            EXTRA.write_text("\n".join(lines + out) + "\n")

    for prog, tgt, filt, sid in M:
        f = SYS / f"{sid}.json"
        if not f.exists():
            print("MISS system", sid)
            continue
        s = json.loads(f.read_text())
        iid = f"{sid}_alice-{filt}"
        rec = next((im for im in s["images"] if im["image_id"] == iid), None)
        wl, wlab = WL[filt]
        if rec is None and not attach:
            s["images"].append({
                "image_id": iid, "type": "disk_scattered", "facility": "HST",
                "instrument": "NICMOS", "wavelength_um": wl,
                "wavelength_label": f"{wlab} (ALICE archival reprocessing, combined coadd)",
                "technique": "RDI", "survey": "ALICE", "file": None,
                "credit": f"ALICE HLSP v1 combined coadd (HST program {prog}, STScI)",
                "paper": dict(PAPER)})
            added_rec += 1
            s["last_updated"] = TODAY
            f.write_text(json.dumps(s, indent=1, ensure_ascii=False))
        elif rec is not None and attach and not rec.get("file"):
            src = ROOT / dest(sid, filt)
            if not src.exists() or src.stat().st_size < 5000:
                continue
            from PIL import Image
            im = Image.open(src).convert("RGB")
            if max(im.size) > 560:
                sc = 560 / max(im.size)
                im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
            outp = ROOT / "images" / sid / f"{iid}.png"
            outp.parent.mkdir(parents=True, exist_ok=True)
            im.save(outp, optimize=True)
            rec["file"] = f"images/{sid}/{iid}.png"
            attached += 1
            s["last_updated"] = TODAY
            f.write_text(json.dumps(s, indent=1, ensure_ascii=False))

    print(f"fetch-lines added: {added_fetch}, records added: {added_rec}, attached: {attached}")


if __name__ == "__main__":
    main()
