#!/usr/bin/env python3
"""Compile backend-data/seeds/ + data/coords_cache.json -> data/systems/*.json.

Non-destructive: existing system files are MERGED (hand edits win for scalar
fields; image records are matched by image_id — seed versions do not overwrite
an existing record unless --force-seed).

Usage:
  python3 make_systems.py                  # build/merge all
  python3 make_systems.py --missing-coords # report systems lacking RA/Dec (+ SIMBAD script)
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from seeds import ALL_BLOCKS, ALL_SYSTEMS            # noqa: E402
from seeds.util import slugify                        # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SYS_DIR = ROOT / "data" / "systems"
COORDS = ROOT / "data" / "coords_cache.json"
TODAY = datetime.date.today().isoformat()


def load_coords():
    if COORDS.exists():
        return json.loads(COORDS.read_text())
    return {}


def survey_slug(s):
    return slugify(s)


def base_system(name, simbad=None):
    return {"id": slugify(name), "name": name, "alt_names": [],
            "simbad": simbad or name, "ra_deg": None, "dec_deg": None,
            "dist_pc": None, "plx_mas": None, "mags": None, "sptype": None,
            "region": None, "categories": [], "planets": [], "images": [],
            "notes": None, "last_updated": TODAY}


def expand_seeds():
    """Return dict id -> system built purely from seeds."""
    out = {}

    def get(name, simbad=None):
        sid = slugify(name)
        if sid not in out:
            out[sid] = base_system(name, simbad)
        return out[sid]

    for blk in ALL_BLOCKS:
        for m in blk["members"]:
            name, ov = (m, {}) if isinstance(m, str) else m
            sys_ = get(name, ov.get("simbad"))
            if ov.get("simbad"):
                sys_["simbad"] = ov["simbad"]
            for an in ov.get("alt_names", []):
                if an not in sys_["alt_names"]:
                    sys_["alt_names"].append(an)
            region = ov.get("region") or blk.get("region")
            if region and not sys_["region"]:
                sys_["region"] = region
            for c in ov.get("categories", blk["categories"]):
                if c not in sys_["categories"]:
                    sys_["categories"].append(c)
            for p in ov.get("planets", []):
                if p["name"] not in [q["name"] for q in sys_["planets"]]:
                    sys_["planets"].append(dict(p))
            rec = dict(blk["image_defaults"])
            rec.update({k: v for k, v in ov.items()
                        if k in ("wavelength_um", "wavelength_label", "instrument")})
            iid = ov.get("image_id") or f'{sys_["id"]}_{survey_slug(blk["survey"])}'
            rec.update({"image_id": iid, "survey": blk["survey"], "file": None,
                        "credit": None, "paper": dict(blk["paper"])})
            sys_["images"].append(rec)

    for s in ALL_SYSTEMS:
        sys_ = get(s["name"], s.get("simbad"))
        if s.get("simbad"):
            sys_["simbad"] = s["simbad"]
        for an in s.get("alt_names", []):
            if an not in sys_["alt_names"]:
                sys_["alt_names"].append(an)
        if s.get("region") and not sys_["region"]:
            sys_["region"] = s["region"]
        for c in s.get("categories", []):
            if c not in sys_["categories"]:
                sys_["categories"].append(c)
        for p in s.get("planets", []):
            if p["name"] not in [q["name"] for q in sys_["planets"]]:
                sys_["planets"].append(dict(p))
        if s.get("notes"):
            sys_["notes"] = (sys_["notes"] + " | " if sys_["notes"] else "") + s["notes"]
        for im in s.get("images", []):
            rec = {k: v for k, v in im.items()
                   if k not in ("image_id_suffix", "file_status")}
            rec["image_id"] = f'{sys_["id"]}_{im["image_id_suffix"]}'
            rec["file"] = None
            rec.setdefault("survey", None)
            sys_["images"].append(rec)
    return out


def apply_coords(systems, coords):
    n = 0
    for s in systems.values():
        for key in (s["simbad"], s["name"], *s["alt_names"]):
            c = coords.get(key)
            if c:
                if s["ra_deg"] is None:
                    s["ra_deg"], s["dec_deg"] = c.get("ra"), c.get("dec")
                if c.get("plx_mas"):
                    s.setdefault("plx_mas", None)
                    if s["plx_mas"] is None:
                        s["plx_mas"] = c["plx_mas"]
                    if s["dist_pc"] is None:
                        s["dist_pc"] = round(1000.0 / c["plx_mas"], 1)
                if s["sptype"] is None and c.get("sptype"):
                    s["sptype"] = c["sptype"]
                if c.get("mags") and not s.get("mags"):
                    s["mags"] = c["mags"]
                n += 1
                break
    return n


def merge_into_existing(seeded, force_seed=False):
    SYS_DIR.mkdir(parents=True, exist_ok=True)
    created = updated = 0
    for sid, s in sorted(seeded.items()):
        f = SYS_DIR / f"{sid}.json"
        if not f.exists():
            f.write_text(json.dumps(s, indent=1, ensure_ascii=False))
            created += 1
            continue
        cur = json.loads(f.read_text())
        changed = False
        for k in ("ra_deg", "dec_deg", "dist_pc", "plx_mas", "mags", "sptype",
                  "region", "notes"):
            if cur.get(k) in (None, "") and s.get(k) not in (None, ""):
                cur[k] = s[k]
                changed = True
        for lst, key in (("alt_names", None), ("categories", None)):
            for v in s[lst]:
                if v not in cur.get(lst, []):
                    cur.setdefault(lst, []).append(v)
                    changed = True
        have_pl = {p["name"] for p in cur.get("planets", [])}
        for p in s["planets"]:
            if p["name"] not in have_pl:
                cur.setdefault("planets", []).append(p)
                changed = True
        have_im = {i["image_id"]: idx for idx, i in enumerate(cur.get("images", []))}
        for im in s["images"]:
            if im["image_id"] not in have_im:
                cur.setdefault("images", []).append(im)
                changed = True
            elif force_seed:
                keep_file = cur["images"][have_im[im["image_id"]]].get("file")
                im2 = dict(im)
                if keep_file:
                    im2["file"] = keep_file
                cur["images"][have_im[im["image_id"]]] = im2
                changed = True
        if changed:
            cur["last_updated"] = TODAY
            f.write_text(json.dumps(cur, indent=1, ensure_ascii=False))
            updated += 1
    return created, updated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--missing-coords", action="store_true")
    ap.add_argument("--force-seed", action="store_true")
    a = ap.parse_args()

    seeded = expand_seeds()
    coords = load_coords()
    hit = apply_coords(seeded, coords)

    if a.missing_coords:
        missing = []
        for f in sorted(SYS_DIR.glob("*.json")):
            s = json.loads(f.read_text())
            if s.get("ra_deg") is None:
                missing.append(s["simbad"])
        for sid, s in sorted(seeded.items()):
            if s["ra_deg"] is None and s["simbad"] not in missing \
               and not (SYS_DIR / f"{sid}.json").exists():
                missing.append(s["simbad"])
        print(f"# {len(missing)} systems lack coordinates. SIMBAD sim-script:")
        print('format object form1 "%IDLIST(1)|%COO(d;A D)|%PLX(V)|%SP(S)"')
        for m in missing:
            print(f"query id {m}")
        return

    created, updated = merge_into_existing(seeded, a.force_seed)
    print(f"seeds: {len(seeded)} systems ({hit} with coords) -> "
          f"created {created}, updated {updated}, dir={SYS_DIR}")


if __name__ == "__main__":
    main()
