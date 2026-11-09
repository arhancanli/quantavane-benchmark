"""Exact checkers for the coding theory problems of the Quantavane Originals (standard library only).

  python3 -I orig_codes.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved); it exits 0 only for a
valid certificate and 1 otherwise. Problems:

  cell600-idcode FILE  FILE: vertex numbers 0..119 of the 600-cell's graph (vertex order as in cell600_graph). Valid
                       when the set C is an identifying code: for every vertex v the set N[v] & C (N[v]: v and its
                       12 neighbours) is nonempty, and these sets are different for different v. Value: |C|.
  e8-idcode FILE       the same for the graph of the E8 root polytope 4_21: the 240 roots of E8 (doubled to integer
                       vectors: two entries +-2, or eight entries +-1 with an even number of minus signs), sorted,
                       adjacent when their inner product is 4 (1 in the usual scaling; 56 neighbours each). FILE:
                       vertex numbers 0..239 in that order. Value: |C|."""
import sys






def _q5mul(x, y):      # a + b sqrt5 as pairs of Fractions
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def cell600_graph():
    """The 600-cell's graph: 120 unit quaternions with coordinates in Q(sqrt 5), sorted; adjacent at inner product
    phi/2. The vertex order is the sorted order of the coordinate tuples (a + b sqrt5 written (a, b))."""
    from fractions import Fraction as F
    import itertools
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
    pts = sorted(pts)

    def ip(a, b):
        t = (F(0), F(0))
        for k in range(4):
            m = _q5mul(a[k], b[k])
            t = (t[0] + m[0], t[1] + m[1])
        return t
    adj = [set() for _ in range(120)]
    for a in range(120):
        for b in range(a + 1, 120):
            if ip(pts[a], pts[b]) == phi_h:
                adj[a].add(b)
                adj[b].add(a)
    assert sum(map(len, adj)) == 1440
    return adj


def vertex_list(path, n):
    vs = [int(t) for t in " ".join(line.split("#")[0] for line in open(path, encoding="ascii", errors="replace")).split()]
    if any(v < 0 or v >= n for v in vs) or len(set(vs)) != len(vs):
        raise ValueError(f"vertices must be distinct numbers 0..{n - 1}")
    return vs


def e8_graph():
    import itertools
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
    adj = [set() for _ in range(240)]
    for a in range(240):
        for b in range(a + 1, 240):
            if sum(x * y for x, y in zip(roots[a], roots[b])) == 4:
                adj[a].add(b)
                adj[b].add(a)
    assert sum(map(len, adj)) == 2 * 6720
    return adj


def identifying(adj, C, name):
    n = len(adj)
    seen = {}
    for v in range(n):
        sig = frozenset((adj[v] | {v}) & C)
        if not sig:
            print(f"vertex {v} is not dominated by the code")
            return 1
        if sig in seen:
            print(f"vertices {seen[sig]} and {v} have the same code neighbourhood")
            return 1
        seen[sig] = v
    print(f"identifying code of the {name} with {len(C)} vertices: all {n} closed neighbourhoods meet it in "
          f"different nonempty sets")
    print(f"RESULT {len(C)}")
    return 0


def e8_idcode(args, path):
    return identifying(e8_graph(), set(vertex_list(path, 240)), "E8 root polytope")


def cell600_idcode(args, path):
    adj = cell600_graph()
    C = set(vertex_list(path, 120))
    seen = {}
    for v in range(120):
        sig = frozenset((adj[v] | {v}) & C)
        if not sig:
            print(f"vertex {v} is not dominated by the code")
            return 1
        if sig in seen:
            print(f"vertices {seen[sig]} and {v} have the same code neighbourhood")
            return 1
        seen[sig] = v
    print(f"identifying code of the 600-cell with {len(C)} vertices: all 120 closed neighbourhoods meet it in "
          f"different nonempty sets")
    print(f"RESULT {len(C)}")
    return 0


PROBLEMS = {"cell600-idcode": (0, cell600_idcode), "e8-idcode": (0, e8_idcode)}


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
