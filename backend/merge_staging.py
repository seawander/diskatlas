#!/usr/bin/env python3
"""Fold data/staging/*.json image records into data/systems/*.json.

Each staging record = image record + "system_id". If the system file does not
exist it is created as a minimal shell (id/name/simbad guessed from system_id)
and flagged notes="AUTO-CREATED from staging — fill metadata & coords".
Existing image_ids are updated in place (staging wins for file/credit/paper).
Processed staging files are renamed *.merged.
"""
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / "data" / "systems"
STG = ROOT / "data" / "staging"
TODAY = datetime.date.today().isoformat()


def shell(system_id):
    name = system_id.replace("-", " ").upper() if system_id.startswith("hd-") \
        else system_id.replace("-", " ")
    return {"id": system_id, "name": name, "alt_names": [], "simbad": name,
            "ra_deg": None, "dec_deg": None, "dist_pc": None, "sptype": None,
            "region": None, "categories": [], "planets": [], "images": [],
            "notes": "AUTO-CREATED from staging - fill metadata & coords",
            "last_updated": TODAY}


def main():
    if not STG.exists():
        print("no staging dir")
        return
    n_new = n_upd = n_sys = 0
    for sf in sorted(STG.glob("*.json")):
        recs = json.loads(sf.read_text())
        touched = set()
        for r in recs:
            sid = r.pop("system_id")
            f = SYS / f"{sid}.json"
            if f.exists():
                s = json.loads(f.read_text())
            else:
                s = shell(sid)
                n_sys += 1
            idx = {im["image_id"]: i for i, im in enumerate(s["images"])}
            if r["image_id"] in idx:
                cur = s["images"][idx[r["image_id"]]]
                for k, v in r.items():
                    if v is not None:
                        cur[k] = v
                n_upd += 1
            else:
                s["images"].append(r)
                n_new += 1
            s["last_updated"] = TODAY
            f.write_text(json.dumps(s, indent=1, ensure_ascii=False))
            touched.add(sid)
        sf.rename(sf.with_suffix(".json.merged"))
        print(f"{sf.name}: {len(recs)} records into {len(touched)} systems")
    print(f"new images {n_new}, updated {n_upd}, new systems {n_sys}")


if __name__ == "__main__":
    main()
