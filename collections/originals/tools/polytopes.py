"""Graphs of the 600-cell, the 120-cell and the E8 root polytope 4_21 (our own code, exact arithmetic).

  python3 -I polytopes.py 600|120|e8 OUT.edges [OUT.J]

600-cell: the 120 unit quaternions of the binary icosahedral group, written with coordinates in Q(sqrt 5) as pairs
(a, b) meaning a + b*sqrt(5); two vertices are adjacent when their inner product is phi/2 = (1 + sqrt 5)/4 (the
nearest neighbours: 12 each, 720 edges). 120-cell: its dual; vertices are the 600 tetrahedral cells of the 600-cell
(the 4-cliques of its graph), adjacent when they share a triangle (4 each, 1200 edges). 4_21: the 240 roots of E8
(the 112 vectors with two entries +-1 and the 128 vectors with all entries +-1/2 and an even number of minus signs,
doubled to integers), adjacent when their inner product is 1 (in the usual scaling; 56 each, 6720 edges).
Writes the edge list "u v" (0-based) and optionally the coupling matrix for tools/src/ising.c (J = +1 on edges)."""
import itertools
import sys
from fractions import Fraction as F

HALF = F(1, 2)


def mul(x, y):          # numbers a + b sqrt5 as pairs of Fractions
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def cell600():
    phi = (HALF, HALF)                 # (1 + sqrt5)/2
    iphi = (F(-1, 2), HALF)            # 1/phi = (sqrt5 - 1)/2
    z, one, h = (F(0), F(0)), (F(1), F(0)), (HALF, F(0))
    pts = set()
    for i in range(4):                 # 8 vertices (+-1, 0, 0, 0)
        for s in (one, neg(one)):
            v = [z] * 4
            v[i] = s
            pts.add(tuple(v))
    for signs in itertools.product((h, neg(h)), repeat=4):   # 16 vertices (+-1/2, ...)
        pts.add(tuple(signs))
    base = [mul(phi, h), h, mul(iphi, h), z]                # even permutations of (phi, 1, 1/phi, 0)/2
    for perm in itertools.permutations(range(4)):
        inv = sum(1 for a in range(4) for b in range(a + 1, 4) if perm[a] > perm[b])
        if inv % 2:
            continue
        for signs in itertools.product((1, -1), repeat=3):
            vals = [base[perm[k]] for k in range(4)]
            sgn = iter(signs)
            vals = [v if v == z else (v if next(sgn) == 1 else neg(v)) for v in vals]
            pts.add(tuple(vals))
    pts = sorted(pts)
    assert len(pts) == 120
    target = mul(phi, h)               # inner product phi/2
    edges = []
    for a in range(120):
        for b in range(a + 1, 120):
            ip = (F(0), F(0))
            for k in range(4):
                ip = add(ip, mul(pts[a][k], pts[b][k]))
            if ip == target:
                edges.append((a, b))
    assert len(edges) == 720
    return 120, edges


def cell120():
    n, e6 = cell600()
    adj = [set() for _ in range(n)]
    for a, b in e6:
        adj[a].add(b)
        adj[b].add(a)
    cells = sorted({tuple(sorted(q)) for a, b in e6 for c in adj[a] & adj[b] for d in adj[a] & adj[b] & adj[c]
                    for q in [(a, b, c, d)] if len(set(q)) == 4})
    assert len(cells) == 600
    index = {c: i for i, c in enumerate(cells)}
    by_tri = {}
    for i, c in enumerate(cells):
        for t in itertools.combinations(c, 3):
            by_tri.setdefault(t, []).append(i)
    edges = sorted(tuple(sorted(v)) for v in by_tri.values() if len(v) == 2)
    assert len(edges) == 1200 and all(len(v) == 2 for v in by_tri.values())
    return 600, edges


def e8():
    roots = set()
    for i, j in itertools.combinations(range(8), 2):
        for si, sj in itertools.product((2, -2), repeat=2):
            v = [0] * 8
            v[i], v[j] = si, sj
            roots.add(tuple(v))
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            roots.add(signs)
    roots = sorted(roots)
    assert len(roots) == 240
    edges = [(a, b) for a in range(240) for b in range(a + 1, 240)
             if sum(x * y for x, y in zip(roots[a], roots[b])) == 4]       # doubled coordinates: 4 means 1
    assert len(edges) == 6720
    return 240, edges


def main():
    kind, out = sys.argv[1], sys.argv[2]
    n, edges = {"600": cell600, "120": cell120, "e8": e8}[kind]()
    with open(out, "w") as f:
        f.write(f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges))
    if len(sys.argv) > 3:
        J = [[0] * n for _ in range(n)]
        for a, b in edges:
            J[a][b] = J[b][a] = 1
        with open(sys.argv[3], "w") as f:
            f.write(f"{n}\n" + "".join(" ".join(map(str, r)) + "\n" for r in J))
    print(kind, n, "vertices", len(edges), "edges")


if __name__ == "__main__":
    main()
