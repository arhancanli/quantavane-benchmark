"""Exact checkers for the physics problems of the Quantavane Originals (standard library only).

  python3 -I orig_phys.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact energy of the submitted configuration,
an integer or p/q); it exits 0 only for a well-formed configuration and 1 otherwise. Problems:

  paley-ising P FILE     FILE: P spins, written as + and - (or 1 and -1), spin i for i = 0, ..., P-1; P a prime
                         with P = 1 mod 4. Value: E(s) = sum over i < j of chi(j - i) s_i s_j, where chi is the
                         Legendre symbol modulo P (couplings +1 on the edges of the Paley graph, -1 elsewhere).
  polytope-ising KIND FILE
                         FILE: one spin per vertex of the graph of a 4-dimensional polytope or of the E8 root polytope
                         (KIND 600: the 600-cell, 120 vertices; KIND snub: the snub 24-cell, 96 vertices; KIND ga: the
                         grand antiprism, 100 vertices; KIND 120: the 120-cell, 600 vertices; KIND e8: the 4_21 polytope, 240 vertices;
                         KIND 5, 8, 16, 24: the 5-cell, tesseract, 16-cell and 24-cell; KIND gosset: the Gosset
                         polytope 3_21, 56 vertices; see polytope_graph for each vertex order), as + and - in the vertex order of this checker (see
                         polytope_graph). Value: the antiferromagnetic Ising energy E(s) = sum over edges uv of s_u s_v
                         (each satisfied edge gives -1, each frustrated edge +1).
  polytope-potts KIND Q FILE
                         FILE: one colour 0..Q-1 per vertex of the polytope graph (KIND as above), separated by spaces
                         or newlines, in the checker's vertex order. Value: the energy of the Q-state Potts
                         antiferromagnet, the number of edges whose two ends have the same colour.
  mclaughlin-ising FILE  FILE: 275 spins, written as + and - (or 1 and -1), in the vertex order of mclaughlin_graph: the
                         McLaughlin graph, the unique strongly regular graph with parameters (275, 112, 30, 56), built
                         from the Steiner system S(4,7,23) (the octads of the extended binary Golay code through the
                         point 0, with 0 removed: 253 heptads on the points 1..23); vertices: the 22 points 2..23, then
                         the 77 heptads through the point 1, then the 176 heptads avoiding it (heptads sorted); a point
                         is adjacent to the heptads through 1 that miss it and to the heptads avoiding 1 that contain
                         it, two heptads of the same kind are adjacent when they meet in one point, a heptad through 1
                         and one avoiding it when they meet in three points (A. E. Brouwer's 22 + 77 + 176
                         construction). Value: the antiferromagnetic Ising energy E(s) = sum over edges uv of s_u s_v.
  mclaughlin-sub KIND FILE
                         the same on a subgraph of the McLaughlin graph: KIND local, the 112 neighbours of vertex 0
                         (srg(112, 30, 2, 10)); KIND second, the 162 vertices not adjacent to vertex 0 (srg(162, 56, 10,
                         24)); spins in the McLaughlin graph's vertex order."""
import itertools
from fractions import Fraction as F
import sys


def spins(path, n):
    text = open(path, encoding="ascii", errors="replace").read()
    text = "\n".join(line.split("#")[0] for line in text.splitlines())
    toks = text.replace(",", " ").split()
    if len(toks) == 1 or all(set(t) <= set("+-") for t in toks):
        s = [1 if c == "+" else -1 for c in "".join(toks)]
        if not all(c in "+-" for c in "".join(toks)):
            raise ValueError("spins must be + or -")
    else:
        s = [int(t) for t in toks]
        if any(v not in (1, -1) for v in s):
            raise ValueError("spins must be 1 or -1")
    if len(s) != n:
        raise ValueError(f"{len(s)} spins, expected {n}")
    return s


def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def paley_ising(args, path):
    p = int(args[0])
    if not isprime(p) or p % 4 != 1:
        print("P must be a prime with P = 1 mod 4")
        return 1
    s = spins(path, p)
    chi = [0] + [1 if pow(a, (p - 1) // 2, p) == 1 else -1 for a in range(1, p)]
    e = sum(chi[(j - i) % p] * s[i] * s[j] for i in range(p) for j in range(i + 1, p))
    print(f"Paley Ising model on {p} spins: energy {e} (magnetization {sum(s)})")
    print(f"RESULT {e}")
    return 0


def _q5mul(x, y):      # a + b sqrt5 as pairs of Fractions
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def _cell600_points():
    h, z = (F(1, 2), F(0)), (F(0), F(0))
    phi_h = _q5mul((F(1, 2), F(1, 2)), h)
    iphi_h = _q5mul((F(-1, 2), F(1, 2)), h)
    neg = lambda x: (-x[0], -x[1])
    pts = set()
    for i in range(4):
        for s in ((F(1), F(0)), (F(-1), F(0))):
            v = [z] * 4
            v[i] = s
            pts.add(tuple(v))
    for signs in itertools.product((h, neg(h)), repeat=4):
        pts.add(tuple(signs))
    base = [phi_h, h, iphi_h, z]
    for perm in itertools.permutations(range(4)):
        if sum(1 for a in range(4) for b in range(a + 1, 4) if perm[a] > perm[b]) % 2:
            continue
        for signs in itertools.product((1, -1), repeat=3):
            sg = iter(signs)
            pts.add(tuple(v if v == z else (v if next(sg) == 1 else neg(v)) for v in (base[perm[k]] for k in range(4))))
    return sorted(pts)


def _cell600():
    h, z = (F(1, 2), F(0)), (F(0), F(0))
    phi_h = _q5mul((F(1, 2), F(1, 2)), h)           # phi/2
    iphi_h = _q5mul((F(-1, 2), F(1, 2)), h)         # 1/(2 phi)
    neg = lambda x: (-x[0], -x[1])
    pts = set()
    for i in range(4):
        for s in ((F(1), F(0)), (F(-1), F(0))):
            v = [z] * 4
            v[i] = s
            pts.add(tuple(v))
    for signs in itertools.product((h, neg(h)), repeat=4):
        pts.add(tuple(signs))
    base = [phi_h, h, iphi_h, z]
    for perm in itertools.permutations(range(4)):
        if sum(1 for a in range(4) for b in range(a + 1, 4) if perm[a] > perm[b]) % 2:
            continue
        for signs in itertools.product((1, -1), repeat=3):
            sg = iter(signs)
            pts.add(tuple(v if v == z else (v if next(sg) == 1 else neg(v)) for v in (base[perm[k]] for k in range(4))))
    pts = sorted(pts)
    def ip(a, b):
        t = (F(0), F(0))
        for k in range(4):
            m = _q5mul(a[k], b[k])
            t = (t[0] + m[0], t[1] + m[1])
        return t
    edges = [(a, b) for a in range(120) for b in range(a + 1, 120) if ip(pts[a], pts[b]) == phi_h]
    return 120, edges


def polytope_graph(kind):
    """The vertex order is part of the certificate format: 600-cell vertices sorted as tuples of coordinates
    (a + b sqrt5 written (a, b)); 120-cell vertices are the 4-cliques (cells) of the 600-cell graph sorted as tuples
    of 600-cell vertex numbers; E8 roots doubled to integer vectors and sorted."""
    if kind == "600":
        n, e = _cell600()
        assert len(e) == 720
        return n, e
    if kind == "snub":
        # the snub 24-cell: the 600-cell without its 24 vertices with rational coordinates (an inscribed 24-cell,
        # pairwise non-adjacent); its edges are the 600-cell edges among the other 96 vertices (432 of them)
        pts = _cell600_points()
        n6, e6 = _cell600()
        keep = [i for i, p in enumerate(pts) if any(c[1] != 0 for c in p)]
        idx = {v: j for j, v in enumerate(keep)}
        edges = [(idx[a], idx[b]) for a, b in e6 if a in idx and b in idx]
        assert len(keep) == 96 and len(edges) == 432
        return 96, edges
    if kind == "ga":
        # the grand antiprism: the 600-cell without two great decagons in orthogonal planes. The first decagon starts
        # at vertex 0 and its least-numbered neighbour and follows v_(k+1) = phi v_k - v_(k-1); the second is the first
        # decagon (in vertex order) among the 10 vertices orthogonal to the first. 100 vertices, 500 edges remain.
        pts = _cell600_points()
        n6, e6 = _cell600()
        idx = {q: i for i, q in enumerate(pts)}
        adj6 = [set() for _ in range(120)]
        for a, b in e6:
            adj6[a].add(b)
            adj6[b].add(a)
        phi = (F(1, 2), F(1, 2))
        zero = (F(0), F(0))

        def ip(a, b):
            t = zero
            for k in range(4):
                m = _q5mul(a[k], b[k])
                t = (t[0] + m[0], t[1] + m[1])
            return t

        def ring(u, v):
            r = [u, v]
            for _ in range(8):
                w = tuple((_q5mul(phi, pts[r[-1]][k])[0] - pts[r[-2]][k][0], _q5mul(phi, pts[r[-1]][k])[1] - pts[r[-2]][k][1]) for k in range(4))
                if w not in idx:
                    return None
                r.append(idx[w])
            return r
        r1 = ring(0, min(adj6[0]))
        orth = [w for w in range(120) if all(ip(pts[w], pts[x]) == zero for x in r1)]
        r2 = next(r for w in orth for x in sorted(adj6[w]) if x in orth for r in [ring(w, x)] if r)
        removed = set(r1) | set(r2)
        keep = [i for i in range(120) if i not in removed]
        k2 = {v: j for j, v in enumerate(keep)}
        edges = [(k2[a], k2[b]) for a, b in e6 if a in k2 and b in k2]
        assert len(keep) == 100 and len(edges) == 500
        return 100, edges
    if kind == "120":
        n6, e6 = _cell600()
        adj = [set() for _ in range(n6)]
        for a, b in e6:
            adj[a].add(b)
            adj[b].add(a)
        cells = sorted({tuple(sorted((a, b, c, d))) for a, b in e6 for c in adj[a] & adj[b]
                        for d in adj[a] & adj[b] & adj[c] if len({a, b, c, d}) == 4})
        by_tri = {}
        for i, c in enumerate(cells):
            for t in itertools.combinations(c, 3):
                by_tri.setdefault(t, []).append(i)
        edges = sorted(tuple(sorted(v)) for v in by_tri.values())
        assert len(cells) == 600 and len(edges) == 1200
        return 600, edges
    if kind == "e8":
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
        edges = [(a, b) for a in range(240) for b in range(a + 1, 240)
                 if sum(x * y for x, y in zip(roots[a], roots[b])) == 4]
        assert len(edges) == 6720
        return 240, edges
    if kind == "5":                 # the 5-cell: K5
        return 5, [(a, b) for a in range(5) for b in range(a + 1, 5)]
    if kind == "8":                 # the 8-cell (tesseract): vertex a in 0..15 as a bit vector, edges at Hamming distance 1
        return 16, [(a, b) for a in range(16) for b in range(a + 1, 16) if bin(a ^ b).count("1") == 1]
    if kind == "16":                # the 16-cell: vertices +e_0, -e_0, +e_1, ...; every pair except opposite vertices
        return 8, [(a, b) for a in range(8) for b in range(a + 1, 8) if a // 2 != b // 2]
    if kind == "24":                # the 24-cell: the 24 vertices of the 600-cell with rational coordinates, in the
        pts = _cell600_points()     # 600-cell's vertex order, adjacent at inner product 1/2
        keep = [p for p in pts if all(c[1] == 0 for c in p)]
        edges = [(a, b) for a in range(24) for b in range(a + 1, 24)
                 if sum(x[0] * y[0] for x, y in zip(keep[a], keep[b])) == F(1, 2)]
        assert len(keep) == 24 and len(edges) == 96
        return 24, edges
    if kind == "gosset":            # the Gosset polytope 3_21: the 56 roots of E8 (doubled, as for KIND e8) with inner
        n8, e8 = polytope_graph("e8")   # product 1 with the first root, adjacent at inner product 1 (27 neighbours)
        nb = sorted(b for a, b in e8 if a == 0) + sorted(a for a, b in e8 if b == 0)
        nb = sorted(nb)
        idx = {v: i for i, v in enumerate(nb)}
        es = set(e8)
        edges = [(idx[a], idx[b]) for a in nb for b in nb if a < b and (a, b) in es]
        assert len(nb) == 56 and len(edges) == 756
        return 56, edges
    raise ValueError("KIND must be 600, snub, ga, 120, e8, 5, 8, 16, 24 or gosset")


def polytope_ising(args, path):
    n, edges = polytope_graph(args[0])
    s = spins(path, n)
    e = sum(s[a] * s[b] for a, b in edges)
    frustrated = sum(1 for a, b in edges if s[a] == s[b])
    print(f"polytope {args[0]}: {n} spins, {len(edges)} edges, {frustrated} frustrated edges, energy {e}")
    print(f"RESULT {e}")
    return 0


def polytope_potts(args, path):
    n, edges = polytope_graph(args[0])
    q = int(args[1])
    toks = " ".join(line.split("#")[0] for line in open(path, encoding="ascii", errors="replace")).split()
    c = [int(t) for t in toks]
    if len(c) != n or any(not 0 <= x < q for x in c):
        print(f"expected {n} colours between 0 and {q - 1}")
        return 1
    mono = sum(1 for a, b in edges if c[a] == c[b])
    print(f"{q}-state Potts antiferromagnet on polytope {args[0]}: {mono} of {len(edges)} edges monochromatic")
    print(f"RESULT {mono}")
    return 0


GOLAY_B = ["110111000101", "101110001011", "011100010111", "111000101101", "110001011011", "100010110111",
           "000101101111", "001011011101", "010110111001", "101101110001", "011011100011", "111111111110"]


def golay_octads():
    """The 759 octads of the extended binary Golay code from its generator matrix [I | B], as sets of 0..23."""
    rows = [(1 << (23 - i)) | int(GOLAY_B[i], 2) for i in range(12)]
    words = set()
    for mask in range(1 << 12):
        w = 0
        for i in range(12):
            if mask >> i & 1:
                w ^= rows[i]
        if bin(w).count("1") == 8:
            words.add(w)
    return [frozenset(23 - j for j in range(24) if w >> j & 1) for w in words]


def mclaughlin_graph():
    hept = sorted(tuple(sorted(o - {0})) for o in golay_octads() if 0 in o)
    through = [set(h) for h in hept if 1 in h]
    avoid = [set(h) for h in hept if 1 not in h]
    verts = [("p", q) for q in range(2, 24)] + [("B", b) for b in through] + [("C", c) for c in avoid]
    edges = []
    for i in range(len(verts)):
        ti, a = verts[i]
        for j in range(i + 1, len(verts)):
            tj, b = verts[j]
            if ti == "p" and tj == "p":
                continue
            if ti == "p":
                ok = (a not in b) if tj == "B" else (a in b)
            else:
                k = len(a & b)
                ok = (k == 1) if ti == tj else (k == 3)
            if ok:
                edges.append((i, j))
    return len(verts), edges


def mclaughlin_ising(args, path):
    n, edges = mclaughlin_graph()
    s = spins(path, n)
    deg = [0] * n
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    if n != 275 or len(edges) != 15400 or set(deg) != {112}:
        print("internal error: the McLaughlin graph was not built correctly")
        return 1
    e = sum(s[a] * s[b] for a, b in edges)
    cut = sum(1 for a, b in edges if s[a] != s[b])
    print(f"McLaughlin graph: 275 vertices, 15400 edges; {cut} edges joining opposite spins; E = {e}")
    print(f"RESULT {e}")
    return 0


def mclaughlin_sub(args, path):
    """KIND local: the subgraph induced on the 112 neighbours of vertex 0 (srg(112, 30, 2, 10), the collinearity graph of
    GQ(3, 9)); KIND second: on the 162 vertices other than 0 not adjacent to it (srg(162, 56, 10, 24)); vertices in
    the McLaughlin graph's order."""
    n, edges = mclaughlin_graph()
    nb = {b for a, b in edges if a == 0} | {a for a, b in edges if b == 0}
    keep = sorted(nb) if args[0] == "local" else sorted(set(range(1, n)) - nb) if args[0] == "second" else None
    if keep is None:
        print("KIND must be local or second")
        return 1
    idx = {v: i for i, v in enumerate(keep)}
    sub = [(idx[a], idx[b]) for a, b in edges if a in idx and b in idx]
    if (len(keep), len(sub)) not in ((112, 1680), (162, 4536)):
        print("internal error: the subgraph was not built correctly")
        return 1
    s = spins(path, len(keep))
    e = sum(s[a] * s[b] for a, b in sub)
    print(f"McLaughlin subgraph {args[0]}: {len(keep)} vertices, {len(sub)} edges; E = {e}")
    print(f"RESULT {e}")
    return 0


PROBLEMS = {"paley-ising": (1, paley_ising), "polytope-ising": (1, polytope_ising), "mclaughlin-sub": (1, mclaughlin_sub),
            "polytope-potts": (2, polytope_potts),
            "mclaughlin-ising": (0, mclaughlin_ising)}


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in PROBLEMS:
        print(__doc__)
        return 2
    nargs, fn = PROBLEMS[sys.argv[1]]
    if len(sys.argv) != 3 + nargs:
        print(__doc__)
        return 2
    try:
        return fn(sys.argv[2:-1], sys.argv[-1])
    except (ValueError, OSError) as e:
        print(f"unreadable certificate: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
