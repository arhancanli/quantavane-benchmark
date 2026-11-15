"""ccd_cells.py: the Lennard-Jones clusters of the Cambridge Cluster Database (N <= 150) as the benchmark family
lj-cluster, checked by checkers/cluster_check.py.

  python3 -I ccd_cells.py TABLES150.html READ REVISION     (writes families/lj-cluster/)

TABLES150.html is the page jon/structures/LJ/tables.150.html of the database (Wales and Doye's table of putative global
minima for N = 3..150, with its references). Its second table (the lowest icosahedral minima, which are not global
minima) is not read. Cells: N = 14..150; N <= 13 are left out (the smallest clusters, whose minima are the most
studied and, for the smallest, settled). Larger N (the database's tables for 310..1000) are left out: values
published after those tables (for example Yu et al. 2019 for N near 1000) are not in them."""
import hashlib
import html
import json
import os
import re
import sys


def cells(row):
    raw = [re.split(r"(?i)</td>", c)[0] for c in re.split(r"(?i)<td[^>]*>", row)[1:]]
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c))).strip() for c in raw]


def main():
    page, read, revision = sys.argv[1:4]
    raw = open(page, "rb").read()
    t = re.sub(r"(?s)<!--.*?-->", "", raw.decode("latin-1"))
    t = t[:t.find("Lowest energy icosahedral minima")]
    rows = {}
    for row in re.findall(r"(?is)<tr>(.*?)</tr>", t):
        c = cells(row)
        for k in range(0, len(c) - 3, 5):                   # N, point group, energy, reference, (blank)
            n, pg, e, ref = c[k], c[k + 1], c[k + 2], c[k + 3]
            if n.isdigit() and re.fullmatch(r"-\d+\.\d+", e):
                rows[int(n)] = (e, re.sub(r"[^A-Za-z0-9 .,'/-]", "", ref)[:60], re.sub(r"[^A-Za-z0-9 ]", "", pg)[:10])
    assert len(rows) >= 140, len(rows)
    out = []
    for n in sorted(rows):
        if n < 14:
            continue
        e, ref, pg = rows[n]
        cell = {"id": f"lj-n{n}", "params": {"n": n}, "best": e}
        if ref:
            cell["holder"] = f"reference {ref} of the database's table" + (f" (point group {pg})" if pg else "")
        out.append(cell)
    fam = {
        "family": "lj-cluster", "title": "Lennard-Jones clusters with the lowest energy",
        "added": "2.2", "objective": "minimize", "id_prefixes": ["lj-"],
        "keeper": "D. J. Wales and others, the Cambridge Cluster Database (www-wales.ch.cam.ac.uk/CCD.html)",
        "page": "https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/LJ/tables.150.html",
        "read": read, "revision": revision, "exact_values": False,
        "template": {"title": "Lennard-Jones cluster of {n} atoms",
                     "statement": "Place {n} atoms in space so that the Lennard-Jones energy, the sum over pairs of 4 (r^-12 - r^-6) in reduced units, is as low as possible.",
                     "submission": "Text file: {n} lines, the coordinates x y z of each atom (decimal numbers); see checkers/cluster_check.py.",
                     "args": ["lj", "{n}"]},
        "checker": {"program": "cluster_check.py", "value": "result"},
        "score": "the energy, rounded up in the 12th decimal: a proven upper bound (lower is better)",
        "best_text": "The putative global minimum in the database is {best} ({holder}); a cluster with a lower energy improves it.",
        "holder_unknown": "not named in the table",
        "holder_sources": "the reference column of the table (Wales and Doye, J. Phys. Chem. A 101 (1997) 5111, and the works it cites)",
        "open_rule": "every N from 14 to 150 of the table of putative global minima (none is proven optimal)",
        "left_out": "N <= 13; the database's tables for N = 310 to 1000 (later published values are not in them); the table of icosahedral minima",
        "frames": "the database's own coordinate files for N = 3..150 (read 1 Nov 2026) give, by checkers/cluster_check.py, the listed energies to the printed six decimals (checked for N = 13, 38, 77, 98, 150)",
        "page_sha256": hashlib.sha256(raw).hexdigest(),
        "cells": "cells.jsonl", "count": len(out), "quantavane_records": 0, "single_problems_left_out": 0,
    }
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = os.path.join(root, "families", "lj-cluster")
    os.makedirs(d, exist_ok=True)
    json.dump(fam, open(os.path.join(d, "family.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(d, "cells.jsonl"), "w") as f:
        for c in out:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print("family written:", len(out))


if __name__ == "__main__":
    main()
