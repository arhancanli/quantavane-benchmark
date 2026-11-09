"""Benzenoids with small Kemeny constant for larger h, by a beam over h (our own code, Quantavane Originals).

  python3 -I benzenoid_beam.py HSTART HEND BEAM START.json OUT.json

Starts from the exact lists for HSTART (benzenoids.py output, its three smallest) or from all benzenoids of HSTART if
the file holds them, extends every kept benzenoid by one hexagon in every possible way (no holes), computes Kemeny's
constant in floating point, keeps the BEAM smallest distinct shapes, and repeats up to HEND. The best shape of each h
is recomputed exactly. A heuristic: values for h above the exhaustive range are upper bounds only."""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import benzenoids as B


def main():
    h0, h1, beam, start, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    if start.startswith("all:"):
        lv = B.polyhexes(h0)
        cur = [p for p in lv[h0] if not B.has_hole(p)]
    else:
        d = json.load(open(start))
        cur = [tuple(tuple(c) for c in x["cells"]) for x in d[str(h0)]["min"]]
    res = {}
    for h in range(h0 + 1, h1 + 1):
        nxt = set()
        for p in cur:
            cs = set(p)
            for q, r in p:
                for dq, dr in B.DIRS:
                    nb = (q + dq, r + dr)
                    if nb not in cs:
                        c = B.canon(cs | {nb})
                        if c not in nxt and not B.has_hole(c):
                            nxt.add(c)
        scored = []
        for p in nxt:
            n, e = B.graph(p)
            scored.append((B.kemeny_float(n, e), p))
        scored.sort()
        cur = [p for _, p in scored[:beam]]
        n, e = B.graph(cur[0])
        k = B.kemeny_exact(n, e)
        res[h] = {"cells": cur[0], "kemeny": f"{k.numerator}/{k.denominator}", "float": float(k), "n": n, "m": len(e),
                  "candidates": len(nxt)}
        print(h, len(nxt), "best %.6f" % float(k), n, len(e), flush=True)
        json.dump(res, open(out, "w"), indent=0)


if __name__ == "__main__":
    main()
