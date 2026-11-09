"""Benzenoid systems (polyhexes without holes) and their Kemeny constants (our own code, Quantavane Originals).

  python3 -I benzenoids.py HMAX OUT.json

Hexagons are cells (q, r) of the hexagonal tiling in axial coordinates; neighbours (q+1,r), (q-1,r), (q,r+1),
(q,r-1), (q+1,r-1), (q-1,r+1). Free polyhexes are grown cell by cell and kept up to the 12 symmetries of the tiling;
those whose complement has a bounded component (a hole) are dropped. The molecular graph has the hexagons' corners as
vertices. Kemeny's constant K = (1/(2m)) sum over pairs {i,j} of d_i d_j R_ij (R: resistance distance, d: degrees,
m: edges) is computed in floating point for every benzenoid; for each h the smallest values are recomputed exactly
(fractions) and written with their hexagons."""
import json
import sys
from fractions import Fraction

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]


def canon(cells):
    best = None
    pts = list(cells)
    for k in range(12):
        tr = []
        for q, r in pts:
            x, z = q, r
            y = -x - z
            for _ in range(k % 6):          # rotate by 60 degrees: (x, y, z) -> (-z, -x, -y)
                x, y, z = -z, -x, -y
            if k >= 6:                      # reflect: swap y and z
                y, z = z, y
            tr.append((x, z))
        mq = min(a for a, b in tr)
        mr = min(b for a, b in tr)
        t = tuple(sorted((a - mq, b - mr) for a, b in tr))
        if best is None or t < best:
            best = t
    return best


def has_hole(cells):
    cs = set(cells)
    qs = [a for a, b in cs]
    rs = [b for a, b in cs]
    lo_q, hi_q, lo_r, hi_r = min(qs) - 2, max(qs) + 2, min(rs) - 2, max(rs) + 2
    start = (lo_q, lo_r)
    seen = {start}
    stack = [start]
    while stack:
        q, r = stack.pop()
        for dq, dr in DIRS:
            n = (q + dq, r + dr)
            if lo_q <= n[0] <= hi_q and lo_r <= n[1] <= hi_r and n not in cs and n not in seen:
                seen.add(n)
                stack.append(n)
    total = (hi_q - lo_q + 1) * (hi_r - lo_r + 1) - len(cs)
    return len(seen) != total


def polyhexes(hmax):
    levels = {1: {canon([(0, 0)])}}
    for h in range(2, hmax + 1):
        nxt = set()
        for p in levels[h - 1]:
            cs = set(p)
            for q, r in p:
                for dq, dr in DIRS:
                    n = (q + dq, r + dr)
                    if n not in cs:
                        nxt.add(canon(cs | {n}))
        levels[h] = nxt
    return levels


def corners(q, r):
    """The 6 corners of hexagon (q, r), in cyclic order, as points a e1 + b e2 of the unit triangular lattice: hexagon
    centres are the index-3 sublattice {a = b mod 3}, the centre of (q, r) is (2q + r, r - q), and the corners are
    the centre's six nearest lattice points."""
    cx, cy = 2 * q + r, r - q
    offs = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    return [(cx + a, cy + b) for a, b in offs]


def graph(cells):
    idx = {}
    edges = set()
    for q, r in cells:
        cs = corners(q, r)
        for v in cs:
            idx.setdefault(v, len(idx))
        for i in range(6):
            a, b = idx[cs[i]], idx[cs[(i + 1) % 6]]
            edges.add((min(a, b), max(a, b)))
    return len(idx), sorted(edges)


def kemeny_float(n, edges):
    deg = [0] * n
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    M = [[1.0 / n] * n for _ in range(n)]
    for i in range(n):
        M[i][i] += deg[i]
    for a, b in edges:
        M[a][b] -= 1
        M[b][a] -= 1
    inv = invert(M, n, float)
    m = len(edges)
    s = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            s += deg[i] * deg[j] * (inv[i][i] + inv[j][j] - 2 * inv[i][j])
    return s / (2 * m)


def kemeny_exact(n, edges):
    deg = [0] * n
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    M = [[Fraction(1, n)] * n for _ in range(n)]
    for i in range(n):
        M[i][i] += deg[i]
    for a, b in edges:
        M[a][b] -= 1
        M[b][a] -= 1
    inv = invert(M, n, Fraction)
    m = len(edges)
    s = Fraction(0)
    for i in range(n):
        for j in range(i + 1, n):
            s += deg[i] * deg[j] * (inv[i][i] + inv[j][j] - 2 * inv[i][j])
    return s / (2 * m)


def invert(M, n, kind):
    A = [row[:] + [kind(1) if i == j else kind(0) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]


def main():
    hmax, out = int(sys.argv[1]), sys.argv[2]
    levels = polyhexes(hmax)
    res = {}
    for h in range(1, hmax + 1):
        bz = [p for p in levels[h] if not has_hole(p)]
        vals = []
        for p in bz:
            n, e = graph(p)
            vals.append((kemeny_float(n, e), p))
        vals.sort()
        def exact(p):
            n, e = graph(p)
            k = kemeny_exact(n, e)
            return {"cells": p, "kemeny": f"{k.numerator}/{k.denominator}", "float": float(k), "n": n, "m": len(e)}
        res[h] = {"count": len(bz), "min": [exact(p) for kf, p in vals[:3]], "max": exact(vals[-1][1])}
        print(h, len(bz), "min %.6f" % vals[0][0], "max %.6f" % vals[-1][0], flush=True)
    json.dump(res, open(out, "w"), indent=0)


if __name__ == "__main__":
    main()
