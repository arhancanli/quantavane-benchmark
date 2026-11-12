#!/usr/bin/env python3
"""Writes cells/topopt-simp.jsonl, cells/topopt-binary.jsonl and cells/metacell-{bulk,shear,poisson}.jsonl from the
certificates in refs/cells/FAMILY/ (standard library only).

  python3 -I tools/topopt_cells.py

Every value is the checker's (checkers/topopt_check.py) on a certificate file: ID.txt is our best design, ID.base.txt
a baseline (for SIMP cells: our replay of the 88-line paper's optimality-criteria loop with its stopping rule; for the
periodic cells: a plain lattice). A cell's best value is a published one when a paper prints the compliance of the
same problem under identical settings (two MBB cells, PUBLISHED below) and nothing better is certified here;
otherwise our best certified value, a first entry. A certified value counts against a published one only when it is
below the published value moved one unit in its last printed decimal (as obb.py compares)."""
import json
import os
import re
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(HERE))
CHECKER = os.path.join(HERE, "checkers", "topopt_check.py")
GRID = os.path.join(HERE, "refs", "cells", "topopt-grid.jsonl")
DATE = "2026-11-13"
FAMILIES = ("topopt-simp", "topopt-binary", "metacell-bulk", "metacell-shear", "metacell-poisson")
OURS = "Quantavane (Arhan Canli)"
PRE88 = ("E. Andreassen, A. Clausen, M. Schevenels, B. S. Lazarov, O. Sigmund, Efficient topology optimization in "
         "MATLAB using 88 lines of code, preprint of 27 Oct 2010 (Lirias, KU Leuven, lirias.kuleuven.be/retrieve/225946), "
         "Fig. 3, bottom row (density filter), read 2026-11-13; the journal version (Struct. Multidisc. Optim. 43 (2011) "
         "1-16) shows the same designs without the values. Section 3.4: MBB beam, volume fraction 0.5, penalty 3, filter "
         "radius 0.04 times the width (2.4 and 6). A number cited with attribution; no text or code copied")
PINN = ("PINNeAPPle-Labs/PINNeAPPle on GitHub (Apache-2.0), examples/topology_optimization/results/mbb_summary.json at "
        "commit a3a93b7c (12 Oct 2026): 'MBB, MMA, filter', compliance 233.4878134 after 58 iterations of MMA (its "
        "script 01_mbb_beam.py: MBB 60 x 20, volume 0.5, density filter r_min = 2.4, the setup of the 88-line paper), "
        "read 2026-11-13")
OTHERS60 = ("Other published values for the same setup: 233.71 (" + PRE88 + "); 233.6004 (UdvardiPeter/topokit on GitHub, "
            "MIT, benchmarks/tests/data/mbb_60x20_mma.npz, MMA capped at 100 iterations, commit 4f867d2c of 9 Aug 2026); "
            "233.7146 (reproductions of the 88-line loop: qBraid/open-simulation-examples, Apache-2.0, 6 Oct 2026; "
            "lambdaclass/stabileo; tysunseven/topopt-hw)")
PUBLISHED = {
    "topopt-simp-mbb-60x20-v0.5-r2.4": {"value": "233.4878", "holder": "PINNeAPPle-Labs (MMA with the density filter)",
                                        "source": PINN + ". " + OTHERS60},
    "topopt-simp-mbb-150x50-v0.5-r6": {"value": "235.73", "holder": "Andreassen, Clausen, Schevenels, Lazarov, Sigmund "
                                       "(the 88-line code)",
                                       "source": PRE88 + " (150 x 50: c = 235.73). The same 235.7337 in SOPTX (L. He, H. Wei, T. Tian, "
                                                 "arXiv:2505.02438, the density-filter MBB figure) and in qBraid's "
                                                 "reproduction; no lower value found"},
}


def check(args, path):
    r = subprocess.run([sys.executable, "-I", CHECKER] + args + [path], capture_output=True, text=True)
    m = re.findall(r"^RESULT (-?\d+)(?:/(\d+))?$", r.stdout, re.M)
    if r.returncode != 0 or not m:
        return None, r.stdout
    return Fraction(int(m[-1][0]), int(m[-1][1] or 1)), r.stdout


def text(fr):
    return str(fr.numerator) if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"


def decimal(fr, fam):
    return f"{float(fr):.3f}" if fam.startswith("topopt") else f"{float(fr):.6f}"


def better(fam, a, b):
    return (a > b) if fam in ("metacell-bulk", "metacell-shear") else (a < b)


def threshold(fam, value_text):
    unit = Fraction(1, 10 ** len(value_text.split(".")[1])) if "." in value_text else Fraction(1)
    v = Fraction(value_text)
    return v + unit if fam in ("metacell-bulk", "metacell-shear") else v - unit


def first_line(path, cid):
    line = open(path).readline().strip("# \n")
    return line[len(cid) + 2:] if line.startswith(cid + ": ") else line


def bound(c):
    p = c["params"]
    if c["family"] != "metacell-bulk":
        return None
    f = Fraction(p["volfrac"])
    k1, m1 = Fraction(1) / (2 * (1 - Fraction(3, 10))), Fraction(1) / (2 * (1 + Fraction(3, 10)))
    hs = f * k1 * m1 / ((1 - f) * k1 + m1)
    return f"{float(hs):.6f}"


def main():
    grid = [json.loads(l) for l in open(GRID) if l.strip()]
    out = {f: [] for f in FAMILIES}
    for c in grid:
        fam = c["family"]
        rel = f"collections/open-tables/refs/cells/{fam}/{c['id']}.txt"
        brel = f"collections/open-tables/refs/cells/{fam}/{c['id']}.base.txt"
        entry = base = None
        if os.path.exists(os.path.join(ROOT, rel)):
            v, o = check(c["checker_args"], os.path.join(ROOT, rel))
            if v is None:
                sys.exit(f"{rel}: refused by the checker\n{o[-600:]}")
            entry = {"value": text(v), "decimal": decimal(v, fam), "certificate": rel,
                     "how": first_line(os.path.join(ROOT, rel), c["id"])}
        if os.path.exists(os.path.join(ROOT, brel)):
            v, o = check(c["checker_args"], os.path.join(ROOT, brel))
            if v is None:
                sys.exit(f"{brel}: refused by the checker\n{o[-600:]}")
            base = {"value": text(v), "decimal": decimal(v, fam), "certificate": brel,
                    "how": first_line(os.path.join(ROOT, brel), c["id"])}
        if entry is None and base is None:
            print(f"{c['id']}: no certificate yet: left out")
            continue
        ours = [x for x in (entry, base) if x]
        mine = ours[0]
        for x in ours[1:]:
            if better(fam, Fraction(x["value"]), Fraction(mine["value"])):
                mine = x
        pub = PUBLISHED.get(c["id"])
        rec = dict(c)
        rec.update(entry=entry, baseline=base, date=DATE)
        if pub:
            beats = better(fam, Fraction(mine["value"]), threshold(fam, pub["value"]))
            rec["published"] = dict(pub, rounded=True)
            if beats:
                rec.update(best=mine["value"], best_decimal=mine["decimal"], first_entry=False, holder=OURS,
                           how=mine["how"], quantavane=True, certificate=mine["certificate"],
                           certificate_value=mine["value"], status="beats the published value",
                           record=True)
            else:
                rec.update(best=pub["value"], best_decimal=pub["value"], first_entry=False, holder=pub["holder"],
                           how="published value", quantavane=False, certificate=mine["certificate"],
                           certificate_value=mine["value"], status="published value", record=False)
        else:
            rec.update(best=mine["value"], best_decimal=mine["decimal"], first_entry=True, published=None,
                       holder=OURS, how=mine["how"], quantavane=True, certificate=mine["certificate"],
                       certificate_value=mine["value"], status="first entry", record=False)
        b = bound(c)
        if b:
            rec["bound"] = b
        out[fam].append(rec)
    for fam, cs in out.items():
        with open(os.path.join(HERE, "cells", fam + ".jsonl"), "w") as f:
            for c in cs:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"{fam}: {len(cs)} cells; {sum(1 for c in cs if c.get('record'))} beat a published value; "
              f"{sum(1 for c in cs if c.get('first_entry'))} first entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
