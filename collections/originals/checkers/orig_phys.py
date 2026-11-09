"""Exact checkers for the physics problems of the Quantavane Originals (standard library only).

  python3 -I orig_phys.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact energy of the submitted configuration,
an integer or p/q); it exits 0 only for a well-formed configuration and 1 otherwise. Problems:

  paley-ising P FILE     FILE: P spins, written as + and - (or 1 and -1), spin i for i = 0, ..., P-1; P a prime
                         with P = 1 mod 4. Value: E(s) = sum over i < j of chi(j - i) s_i s_j, where chi is the
                         Legendre symbol modulo P (couplings +1 on the edges of the Paley graph, -1 elsewhere).
  polytope-ising KIND FILE
                         FILE: one spin per vertex of the graph of a 4-dimensional regular polytope or of the E8 root
                         polytope (KIND 600: the 600-cell, 120 vertices; KIND 120: the 120-cell, 600 vertices; KIND e8:
                         the 4_21 polytope, 240 vertices), as + and - in the vertex order of this checker (see
                         polytope_graph). Value: the antiferromagnetic Ising energy E(s) = sum over edges uv of s_u s_v
                         (each satisfied edge gives -1, each frustrated edge +1).
  polytope-potts KIND Q FILE
                         FILE: one colour 0..Q-1 per vertex of the polytope graph (KIND as above), separated by spaces
                         or newlines, in the checker's vertex order. Value: the energy of the Q-state Potts
                         antiferromagnet, the number of edges whose two ends have the same colour."""
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
    raise ValueError("KIND must be 600, 120 or e8")


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


PROBLEMS = {"paley-ising": (1, paley_ising), "polytope-ising": (1, polytope_ising),
            "polytope-potts": (2, polytope_potts)}


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
