#!/usr/bin/env python3
"""Writes cells/unknotting.jsonl, the open cells of the unknotting table, from the pinned KnotInfo file (standard
library only).

  python3 -I tools/knotinfo_cells.py [KNOTINFO_CSV]      (default: instances/knotinfo/knotinfo_data_complete.csv,
                                                          fetched by fetch.sh)
  python3 -I tools/knotinfo_cells.py --check [KNOTINFO_CSV]   (check the cells file against the pinned source)

A cell is a prime knot of at most 11 crossings whose unknotting number KnotInfo gives as an interval [a, b], unless a
later paper settles it (CLOSED below, with the source). The cell's best known value is b (KnotInfo's upper bound), its
bound a (the lower bound). The knot is given by KnotInfo's braid word; the checker starts from that word. Only values
are stored (the knot's name, its braid word, the two bounds, its Alexander polynomial and signature for the tests); no
KnotInfo file is copied. A certificate in refs/cells/unknotting/KNOT.txt, if present, is replayed by the checker and its
value recorded in the cell."""
import csv
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # collections/open-tables
ROOT = os.path.dirname(os.path.dirname(HERE))
SOURCE = {
    "file": "instances/knotinfo/knotinfo_data_complete.csv",
    "url": "https://raw.githubusercontent.com/soehms/database_knotinfo/219c2d982b89fb92b6ab0c556f28cdd766a18734/"
           "database_knotinfo/csv_data/knotinfo_data_complete.csv",
    "sha256": "ed4447ff81dc50e2561764760d631356186c34e2dd35f89cc84e0a4d8fedd3d0",
    "release": "database_knotinfo 2026.11.2 (commit 219c2d9, 2 Nov 2026), the KnotInfo spreadsheet of that date",
    "read": "2026-11-12",
}
# Settled after the KnotInfo file of 2 Nov 2026: u = c4 = |sigma|/2 + 1 (D. McCoy, J. Park, Special alternating links
# of minimal unlinking number, arXiv:2603.10732v2, 24 Mar 2026, Table 1 and the list after (4.2)).
CLOSED = {k: ("4", "D. McCoy and J. Park, arXiv:2603.10732v2 (24 Mar 2026), Table 1: u = 4")
          for k in ("11a_291", "11a_298", "11a_319", "11a_336", "11a_340", "11a_353", "11a_356", "11a_357")}
MAX_CROSSINGS = 11


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_knotinfo(path):
    if sha256(path) != SOURCE["sha256"]:
        sys.exit(f"{path}: SHA-256 is not the pinned {SOURCE['sha256']} (run fetch.sh)")
    csv.field_size_limit(1 << 30)
    with open(path, newline="") as f:
        r = csv.reader(f, delimiter="|")
        header = next(r)
        next(r)                                                     # the row of column titles
        idx = {h: j for j, h in enumerate(header)}
        for row in r:
            yield {k: row[idx[k]] for k in ("name", "crossing_number", "unknotting_number", "braid_notation",
                                             "alexander_polynomial_vector", "signature")}


def cell_id(knot):
    return "unknotting-" + knot.replace("_", "-")


def certificate(knot, braid):
    rel = f"collections/open-tables/refs/cells/unknotting/{knot}.txt"
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return None, None
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "checkers", "unknot_check.py"), braid, path],
                       capture_output=True, text=True)
    m = re.findall(r"^RESULT (\d+)$", r.stdout, re.M)
    if r.returncode != 0 or not m:
        sys.exit(f"{rel}: the checker refuses it:\n{r.stdout[-500:]}")
    return rel, m[-1]


def build(path):
    cells, closed = [], []
    for k in read_knotinfo(path):
        if not k["crossing_number"].isdigit() or not 0 < int(k["crossing_number"]) <= MAX_CROSSINGS:
            continue
        m = re.fullmatch(r"\[(\d+),(\d+)\]", k["unknotting_number"].replace(" ", ""))
        if not m:
            continue
        lo, hi = m.groups()
        if k["name"] in CLOSED:
            closed.append({"knot": k["name"], "knotinfo": k["unknotting_number"], "value": CLOSED[k["name"]][0],
                           "source": CLOSED[k["name"]][1]})
            continue
        braid = k["braid_notation"].strip("[]").replace(" ", "")
        cert, val = certificate(k["name"], braid)
        cells.append({
            "id": cell_id(k["name"]), "family": "unknotting",
            "params": {"knot": k["name"], "braid": braid},
            "best": hi, "bound": lo, "status": "open", "first_entry": False,
            "published": {"value": hi, "holder": "KnotInfo (C. Livingston, A. H. Moore)",
                          "source": f"KnotInfo, unknotting number {k['unknotting_number']} (upper bound {hi}, lower "
                                    f"bound {lo}); {SOURCE['release']}, read {SOURCE['read']}"},
            "crossings": int(k["crossing_number"]),
            "alexander_vector": k["alexander_polynomial_vector"], "signature": k["signature"],
            "certificate": cert, "certificate_value": val, "date": SOURCE["read"],
        })
    return cells, closed


def main():
    args = sys.argv[1:]
    check = bool(args) and args[0] == "--check"
    if check:
        args = args[1:]
    path = args[0] if args else os.path.join(ROOT, SOURCE["file"])
    cells, closed = build(path)
    out = os.path.join(HERE, "cells", "unknotting.jsonl")
    text = "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cells)
    if check:
        same = open(out).read() == text
        print(f"{'ok' if same else 'DIFFERS'}: {len(cells)} cells from the pinned KnotInfo file; {len(closed)} closed")
        return 0 if same else 1
    with open(out, "w") as f:
        f.write(text)
    with open(os.path.join(HERE, "cells", "unknotting.closed.json"), "w") as f:
        json.dump(closed, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{len(cells)} open cells, {sum(1 for c in cells if c['certificate'])} with a certificate; {len(closed)} "
          f"settled since the KnotInfo file (cells/unknotting.closed.json)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
