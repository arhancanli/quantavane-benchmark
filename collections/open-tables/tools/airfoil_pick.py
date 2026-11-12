#!/usr/bin/env python3
"""Picks the entry of each airfoil cell from a folder of candidate designs (standard library only).

  python3 -I tools/airfoil_pick.py CANDIDATE_DIR

For each cell of refs/cells/airfoil-grid.jsonl, every candidate certificate in CANDIDATE_DIR whose cell has the same
family and Reynolds number is scored by checkers/airfoil_check.py with this cell's arguments (a design found for a
stricter cell is a valid design for a looser one). The best one is written to refs/cells/FAMILY/ID.txt when it beats
the cell's NACA baseline (or when the cell has none), with a first line naming the search that found it."""
import json
import os
import re
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKER = os.path.join(HERE, "checkers", "airfoil_check.py")


def score(args, path):
    r = subprocess.run([sys.executable, "-I", CHECKER] + args + [path], capture_output=True, text=True)
    m = re.findall(r"^RESULT (\d+)(?:/(\d+))?$", r.stdout, re.M)
    return Fraction(int(m[-1][0]), int(m[-1][1] or 1)) if r.returncode == 0 and m else None


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    cand_dir = sys.argv[1]
    grid = [json.loads(l) for l in open(os.path.join(HERE, "refs", "cells", "airfoil-grid.jsonl")) if l.strip()]
    by_id = {g["id"]: g for g in grid}
    cands = [f for f in sorted(os.listdir(cand_dir)) if f.endswith(".txt") and f[:-4] in by_id]
    for g in grid:
        mode = g["params"]["mode"]
        best = None
        for f in cands:
            src = by_id[f[:-4]]
            if src["family"] != g["family"] or src["params"]["re"] != g["params"]["re"]:
                continue
            v = score(g["checker_args"], os.path.join(cand_dir, f))
            if v is not None and (best is None or (v > best[0] if mode == "ld" else v < best[0])):
                best = (v, f)
        base = Fraction(g["baseline"]["value"]) if g["baseline"] else None
        if best and (base is None or (best[0] > base if mode == "ld" else best[0] < base)):
            text = open(os.path.join(cand_dir, best[1])).read().splitlines()
            how = text[0].lstrip("# ").split(": ", 1)[-1]
            note = f"# {g['id']}: {how}; found for {best[1][:-4]}" if best[1][:-4] != g["id"] else f"# {g['id']}: {how}"
            out = os.path.join(HERE, "refs", "cells", g["family"], g["id"] + ".txt")
            with open(out, "w") as fh:
                fh.write("\n".join([note] + text[1:]) + "\n")
            v2 = score(g["checker_args"], out)
            print(f"{g['id']}: {float(best[0]):.6g} from {best[1]} (baseline {float(base) if base else '-'}); "
                  f"rechecked {float(v2):.6g}")
        else:
            print(f"{g['id']}: no candidate beats the baseline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
