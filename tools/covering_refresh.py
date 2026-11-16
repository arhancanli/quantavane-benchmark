"""covering_refresh.py: refresh the family covering-design from a newer Covering Repository list, keeping every rule of
import_families.py covering-design (bounds, the cells left out, holders).

  python3 -I covering_refresh.py OLD.csv NEW.csv OURS.json UPLOADED_DIR READ REVISION

OLD.csv is the v,k,t,m,b export the cells were built from, NEW.csv the newer one (both in the export format of
export_live.py: header v,k,t,m,b). Entries whose value did not change keep their cell, or stay out, as before. For an
entry whose value fell: a cell takes the new value (and is dropped if the new value reaches its lower bound, or, for m
> t, is at most 3 blocks); its holder is ours when our records (OURS.json, the files in UPLOADED_DIR named
"v,k,t,m-b.txt") hold a covering of that size, else not named (the Covering Repository's lists name no author). An
entry left out before is admitted when the builder's rules now admit it and need no bound beyond the ones computed
here (m > t: the counting and Turan bounds and the one-hour estimate of the check); an entry with m = t would need the
La Jolla Covering Repository's lower bound and is reported, not admitted. Values never rise in these lists; a rise
stops the refresh."""
import csv
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import import_families as F  # noqa: E402

FAM = os.path.join(ROOT, "families", "covering-design")


def load(path):
    out = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            out[tuple(int(r[x]) for x in "vktm")] = int(r["b"])
    return out


def main():
    if len(sys.argv) != 7:
        print(__doc__)
        return 2
    old_path, new_path, ours_path, uploaded, read, revision = sys.argv[1:]
    old, new = load(old_path), load(new_path)
    if set(old) != set(new):
        raise SystemExit(f"the lists differ in their entries: {len(set(new) - set(old))} new, "
                         f"{len(set(old) - set(new))} gone; rebuild with import_families.py instead")
    rose = [k for k in new if new[k] > old[k]]
    if rose:
        raise SystemExit(f"{len(rose)} values rose (first {rose[0]}): check the lists")
    ours = {}
    for r in json.load(open(ours_path)):
        ours.setdefault((r["v"], r["k"], r["t"], r.get("m", r["t"])), set()).add(r["blocks"])
    for name in os.listdir(uploaded):
        m = re.fullmatch(r"(\d+),(\d+),(\d+),(\d+)-(\d+)\.txt", name)
        if m:
            ours.setdefault(tuple(map(int, m.groups()[:4])), set()).add(int(m.group(5)))
    defn = json.load(open(os.path.join(FAM, "family.json")))
    cells = {tuple(c["params"][x] for x in "vktm"): c for c in map(json.loads, open(os.path.join(FAM, "cells.jsonl")))}
    singles = F.single_ids()
    st = {"values changed in the list": 0, "cells with a new value": 0, "cells solved": 0, "cells now at most 3 blocks": 0,
          "our records beaten": 0, "new values that are ours": 0, "admitted": 0, "still too long to check": 0,
          "m = t, would need the La Jolla bound": 0, "changed entries already single problems": 0}
    keep = {}
    for key, c in cells.items():
        nb, ob = new[key], int(c["best"])
        if nb == ob:
            keep[key] = c
            continue
        st["values changed in the list"] += 1
        v, k, t, m = key
        lb = int(c["bound"].split()[0])
        if c.get("quantavane_record"):
            st["our records beaten"] += 1
        if nb <= lb:
            st["cells solved"] += 1
            continue
        if m > t and nb <= 3:
            st["cells now at most 3 blocks"] += 1
            continue
        mine = nb in ours.get(key, ())
        st["new values that are ours"] += mine
        st["cells with a new value"] += 1
        keep[key] = F.make_cell(c["id"], c["params"], nb, c["bound"], F.OURS if mine else None, mine, c.get("variant"))
    lotto_big_new = 0
    for key in new:
        if key in cells or new[key] == old[key]:
            continue
        st["values changed in the list"] += 1
        v, k, t, m = key
        nb = new[key]
        cid = f"covering-{v}-{k}-{t}" if m == t else f"covering-{v}-{k}-{t}-{m}"
        if cid in singles:
            st["changed entries already single problems"] += 1
            continue
        if m == t:
            if nb > F.schoenheim(v, k, t) and nb * math.comb(k, t) <= 10 ** 10:
                st["m = t, would need the La Jolla bound"] += 1
            continue
        lb, how = F.lotto_bound(v, k, t, m)
        if nb <= lb or nb <= 3:
            continue
        if nb > 1000 and (v > 128 or F.lotto_check_hours(v, k, t, m, nb) > 1):
            st["still too long to check"] += 1
            continue
        lotto_big_new += nb > 1000
        mine = nb in ours.get(key, ())
        st["admitted"] += 1
        keep[key] = F.make_cell(cid, {"v": v, "k": k, "t": t, "m": m}, nb, f"{lb} ({how})", F.OURS if mine else None,
                                mine, "lotto")
    rows = [keep[key] for key in new if key in keep]      # the export's order, which is the builder's
    defn["read"] = read
    defn["revision"] = revision
    defn["holder_sources"] = (defn["holder_sources"].split("; values changed since")[0] +
                              "; values changed since 14 Nov 2026 come from the repository's two complete lists, which "
                              "name no author: the holder is ours when our records hold a covering of that size, "
                              "otherwise see the entry on coveringrepository.com")
    heavy_m = st["admitted"]
    defn["left_out"] = re.sub(r"(\d+) entries whose check would be very long",
                              lambda mm: f"{int(mm.group(1)) - heavy_m} entries whose check would be very long",
                              defn["left_out"])
    defn["left_out"] = re.sub(r"(\d+) with m > t, more than 1,000 blocks",
                              lambda mm: f"{int(mm.group(1)) - heavy_m} with m > t, more than 1,000 blocks",
                              defn["left_out"])
    defn["left_out"] = re.sub(r"(\d+) entries equal to their lower bound",
                              lambda mm: f"{int(mm.group(1)) + st['cells solved']} entries equal to their lower bound",
                              defn["left_out"])
    defn["left_out"] = re.sub(r"(\d+) entries with m > t and at most 3",
                              lambda mm: f"{int(mm.group(1)) + st['cells now at most 3 blocks']} entries with m > t "
                                         "and at most 3", defn["left_out"])
    cnt = defn["counts"]
    cnt["t = m"] = sum(1 for r in rows if r["params"]["m"] == r["params"]["t"])
    cnt["m > t"] = len(rows) - cnt["t = m"]
    cnt["m > t with more than 1,000 blocks (searched in C)"] += lotto_big_new
    defn["refresh"] = dict(st)
    defn["permission"] = (
        "Automatic download of the two list files (download_archive.aspx, download_archive_vkt.aspx), up to once a "
        "day, and the listing of these entries with credit to the original authors: written permission of the "
        "Covering Repository's keeper, 16 Nov 2026. The search page and the designs are never read by script.")
    for k in ("cells", "count", "quantavane_records", "single_problems_left_out"):
        defn.pop(k, None)
    F.write_family(defn, rows)
    print(json.dumps(st))
    return 0


if __name__ == "__main__":
    sys.exit(main())
