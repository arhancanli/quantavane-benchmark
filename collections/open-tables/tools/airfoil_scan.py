#!/usr/bin/env python3
"""Scores published NACA sections in the QV-Foil 1 model, for the baselines of the airfoil tables (standard library
only; the same code as checkers/airfoil_check.py, imported, so every value is the checker's own).

  python3 -I tools/airfoil_scan.py OUT.jsonl [RE ...]

For every NACA 4-digit section (camber 0-7 %, camber position 0.2-0.7, thickness 6-24 %) and every 5-digit section of
the 230 type (design lift 0.15-0.6, camber position 0.05-0.25, thickness 6-24 %), and every Reynolds number given
(default: those of the tables), the angle of attack runs from -2 to 12 degrees in steps of 0.25. One line of JSON per
section and Reynolds number: the largest thickness and, per angle, Cl, Cd and Cm (or the reason the model refused)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "checkers"))
import airfoil_check as A  # noqa: E402

RES = (500000, 1000000, 3000000, 6000000, 9000000)
ALPHAS = [k / 4.0 for k in range(-8, 49)]


def designations():
    for m in range(0, 8):
        for p in ([0] if m == 0 else range(2, 8)):
            for t in range(6, 25):
                yield f"{m}{p}{t:02d}"
    for L in range(1, 5):
        for P in range(1, 6):
            for t in range(6, 25):
                yield f"{L}{P}0{t:02d}"


def scan(code, res):
    nodes, th, _, _ = A.geometry(code, None, None)
    ps = A.panel_solution(nodes)
    out = {re: [] for re in res}
    for a in ALPHAS:
        flow = A.panel_flow(ps, a)
        for re in res:
            try:
                v = A.viscous(flow, float(re))
                out[re].append([a, flow["cl"], v["cd"], flow["cm"]])
            except A.Refused as e:
                out[re].append([a, flow["cl"], None, str(e)[:40]])
    return th, out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    res = [int(x) for x in sys.argv[2:]] or list(RES)
    with open(sys.argv[1], "w") as f:
        for code in designations():
            try:
                th, out = scan(code, res)
            except A.Refused as e:
                f.write(json.dumps({"naca": code, "refused": str(e)}) + "\n")
                continue
            for re in res:
                f.write(json.dumps({"naca": code, "re": re, "thickness": th, "polar": out[re]}) + "\n")
            f.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
