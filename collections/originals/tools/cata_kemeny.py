"""Catacondensed benzenoids with small Kemeny constant (our own code, Quantavane Originals; problem cata-kemeny).

  python3 -I cata_kemeny.py exact HMAX OUT.json            every catacondensed benzenoid up to HMAX hexagons
  python3 -I cata_kemeny.py beam HSTART HEND BEAM OUT.json   beam search above the exhaustive range

A benzenoid (no holes) with h hexagons is catacondensed when its molecular graph has 4h + 2 vertices (no internal
vertex). 'exact' enumerates all of them with benzenoids.py (the counts 1, 2, 5, 12, 36, 118, 411, 1489, 5572 of
OEIS A038142 for h = 2..10), and records for each h the count, the minimum of Kemeny's constant (recomputed in exact
arithmetic), whether the minimiser is branched (some hexagon has three neighbouring hexagons) and the minimum over
unbranched systems (planar hexagonal chains). 'beam' starts from all catacondensed systems with HSTART hexagons,
keeps the BEAM with the smallest constant, extends each by one hexagon in every way that stays catacondensed and
repeats up to HEND; the best of each h is recomputed exactly. The beam values are upper bounds only. (The published
h = 19 value came from 'beam 10 19 80'.)"""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import benzenoids as B


def is_cata(p, h):
    n, e = B.graph(p)
    return n == 4 * h + 2


def branched(p):
    s = set(p)
    return any(sum((q + dq, r + dr) in s for dq, dr in B.DIRS) > 2 for q, r in p)


def exact(hmax, out):
    lv = B.polyhexes(hmax)
    res = {}
    for h in range(2, hmax + 1):
        cata = sorted((B.kemeny_float(*B.graph(p)), p) for p in lv[h] if not B.has_hole(p) and is_cata(p, h))
        best = cata[0][1]
        k = B.kemeny_exact(*B.graph(best))
        bu = min((x for x in cata if not branched(x[1])), default=None)
        res[h] = {"count": len(cata), "min": f"{k.numerator}/{k.denominator}", "float": float(k), "cells": best,
                  "branched": branched(best), "min_unbranched": bu[0] if bu else None}
        print(h, len(cata), "min %.6f" % float(k), "branched" if branched(best) else "unbranched",
              "chains %.6f" % bu[0] if bu else "", flush=True)
    json.dump(res, open(out, "w"))


def beam(h0, h1, width, out):
    lv = B.polyhexes(h0)
    cur = sorted((B.kemeny_float(*B.graph(p)), p) for p in lv[h0] if not B.has_hole(p) and is_cata(p, h0))
    cur = [p for _, p in cur[:width]]
    res = {}
    for h in range(h0 + 1, h1 + 1):
        nxt = set()
        for p in cur:
            cs = set(p)
            for q, r in p:
                for dq, dr in B.DIRS:
                    nb = (q + dq, r + dr)
                    if nb in cs:
                        continue
                    c = B.canon(cs | {nb})
                    if c not in nxt and not B.has_hole(c) and is_cata(c, h):
                        nxt.add(c)
        sc = sorted((B.kemeny_float(*B.graph(p)), p) for p in nxt)
        cur = [p for _, p in sc[:width]]
        k = B.kemeny_exact(*B.graph(cur[0]))
        res[h] = {"cells": cur[0], "kemeny": f"{k.numerator}/{k.denominator}", "float": float(k)}
        print(h, len(nxt), "%.6f" % float(k), flush=True)
        json.dump(res, open(out, "w"))


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "exact":
        exact(int(sys.argv[2]), sys.argv[3])
    elif len(sys.argv) == 6 and sys.argv[1] == "beam":
        beam(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
