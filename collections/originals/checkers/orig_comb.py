"""Exact checkers for the combinatorics and analysis problems of the Quantavane Originals (standard library only).

  python3 -I orig_comb.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved, an integer or p/q); it
exits 0 only for a valid certificate and 1 otherwise. Problems:

  autoconv-square M FILE   FILE: an M x M array of nonnegative integers a[i][j] (M lines of M numbers), not all
                           zero: the step function f on [-1/4, 1/4]^2 equal to a[i][j] on the cell
                           [-1/4 + i h, -1/4 + (i+1) h] x [-1/4 + j h, -1/4 + (j+1) h], h = 1/(2M). Value:
                           ||f*f||_inf / (integral of f)^2 = 4 M^2 max_u (a*a)[u] / (sum of a)^2, exactly. (f*f is
                           bilinear on each cell of side h of its grid, so its maximum is attained at a grid point,
                           where it equals h^2 (a*a)[u]; a*a is the discrete autoconvolution of the array.)
  overlap-square M DEN FILE
                           FILE: an M x M array of integers a[i][j] between 0 and DEN with sum DEN * M^2 / 2: the
                           step function f = a/DEN on the cells of side 2/M of [0,2]^2 (so 0 <= f <= 1 and the
                           integral of f is 2, half the area). With g = 1 - f on the square and 0 outside, the value
                           is the overlap sup over x of integral f(t) g(t - x) dt = (4/M^2) max_k sum_i
                           a_i (DEN - a_(i-k)) / DEN^2 (the cross-correlation of two step functions is bilinear on
                           each grid cell, so the supremum is attained at a grid point), exactly.
  overlap-three M DEN FILE FILE: M lines of three integers between 0 and DEN (M divisible by 3): on the i-th cell of
                           width 3/M of [0,3] the three step functions f_1, f_2, f_3 take the values entry/DEN; every
                           line must sum to DEN (f_1 + f_2 + f_3 = 1) and every column to DEN M/3 (each integral 1).
                           Value: the largest overlap, max over parts a != b and shifts x of integral f_a(t) f_b(t - x)
                           dt = (3/M) max_k sum_i e_a[i] e_b[i-k] / DEN^2 (the overlap is linear between grid shifts),
                           exactly.
  ap-cover P K FILE        FILE: lines "a d", each the progression {a, a+d, ..., a+(K-1)d} modulo the prime P (d not 0
                           mod P, so its K elements are distinct). Valid when every pair of elements of Z_P lies in
                           some progression. Value: the number of progressions.
  e8-goodman FILE          FILE: a string of 6720 digits 0 and 1 (whitespace ignored), the colours of the edges of the
                           E8 root graph (the 240 roots doubled to integer vectors: two entries +-2, or eight entries
                           +-1 with an even number of minus signs; sorted; adjacent when the inner product is 4),
                           listed as the pairs (a, b), a < b, in lexicographic order. Value: the number of
                           monochromatic triangles.
  cell600-forest FILE      FILE: vertex numbers 0..119 of the 600-cell's graph (vertex order as in cell600_graph)
                           whose induced subgraph is a forest (no cycle). Value: the number of vertices; the 120 minus
                           it is the size of a decycling (feedback vertex) set.
  e8-resolving FILE        FILE: vertex numbers 0..239 of the E8 root graph (the 240 roots doubled to integer vectors,
                           sorted, adjacent when the inner product is 4, as for e8-goodman). Valid when the set W
                           resolves the graph: the vectors of graph distances (d(v, w))_(w in W) are different for all
                           240 vertices v. Value: |W|."""
import itertools
import sys
from fractions import Fraction


def matrix(path):
    rows = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if line:
            rows.append([int(t) for t in line.replace(",", " ").split()])
    return rows


def autoconv_square(args, path):
    m = int(args[0])
    a = matrix(path)
    if len(a) != m or any(len(r) != m for r in a):
        print(f"expected {m} rows of {m} integers")
        return 1
    if any(v < 0 for r in a for v in r) or not any(v for r in a for v in r):
        print("the values must be nonnegative and not all zero")
        return 1
    n = 2 * m - 1
    c = [[0] * n for _ in range(n)]
    nz = [(i, j, a[i][j]) for i in range(m) for j in range(m) if a[i][j]]
    for i, j, v in nz:
        for k, l, w in nz:
            c[i + k][j + l] += v * w
    mx = max(map(max, c))
    s = sum(map(sum, a))
    r = Fraction(4 * m * m * mx, s * s)
    print(f"{m} x {m} step function: max of the discrete autoconvolution {mx}, sum {s}; "
          f"||f*f||_inf / (int f)^2 = {r} = {float(r):.12f}")
    print(f"RESULT {r.numerator}/{r.denominator}" if r.denominator != 1 else f"RESULT {r.numerator}")
    return 0


def overlap_square(args, path):
    m, den = int(args[0]), int(args[1])
    a = matrix(path)
    if len(a) != m or any(len(r) != m for r in a):
        print(f"expected {m} rows of {m} integers")
        return 1
    if any(v < 0 or v > den for r in a for v in r):
        print(f"the values must lie between 0 and {den}")
        return 1
    if 2 * sum(map(sum, a)) != den * m * m:
        print(f"the values must sum to {den} * {m}^2 / 2 (integral of f equal to 2)")
        return 1
    best = 0
    for k1 in range(-(m - 1), m):
        for k2 in range(-(m - 1), m):
            s = 0
            for i1 in range(max(0, k1), min(m, m + k1)):
                ai, bi = a[i1], a[i1 - k1]
                for i2 in range(max(0, k2), min(m, m + k2)):
                    s += ai[i2] * (den - bi[i2 - k2])
            best = max(best, s)
    r = Fraction(4 * best, m * m * den * den)
    print(f"{m} x {m} step function with values in [0,1], integral 2: overlap {r} = {float(r):.12f}")
    print(f"RESULT {r.numerator}/{r.denominator}" if r.denominator != 1 else f"RESULT {r.numerator}")
    return 0


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


def ap_cover(args, path):
    p, k = int(args[0]), int(args[1])
    if p < 3 or any(p % d == 0 for d in range(2, int(p ** 0.5) + 1)) or not 2 <= k <= p:
        print("P must be an odd prime and 2 <= K <= P")
        return 1
    rows = matrix(path)
    covered = set()
    for r in rows:
        if len(r) != 2 or r[1] % p == 0:
            print(f"bad progression line {r}: expected 'a d' with d not 0 mod {p}")
            return 1
        a, d = r
        b = sorted((a + i * d) % p for i in range(k))
        for i in range(k):
            for j in range(i + 1, k):
                covered.add((b[i], b[j]))
    missing = p * (p - 1) // 2 - len(covered)
    if missing:
        x, y = next((x, y) for x in range(p) for y in range(x + 1, p) if (x, y) not in covered)
        print(f"{missing} pairs not covered, for instance {{{x}, {y}}}")
        return 1
    print(f"{len(rows)} progressions of length {k} cover all {p * (p - 1) // 2} pairs of Z_{p}")
    print(f"RESULT {len(rows)}")
    return 0


def e8_edges():
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
    return [(a, b) for a in range(240) for b in range(a + 1, 240) if sum(x * y for x, y in zip(roots[a], roots[b])) == 4]


def e8_goodman(args, path):
    edges = e8_edges()
    text = "".join("".join(line.split("#")[0].split()) for line in open(path, encoding="ascii", errors="replace"))
    if len(text) != len(edges) or set(text) - set("01"):
        print(f"expected {len(edges)} colours 0 or 1")
        return 1
    col = {e: text[i] for i, e in enumerate(edges)}
    adj = [set() for _ in range(240)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    mono = total = 0
    for a, b in edges:
        for c in adj[a] & adj[b]:
            if c > b:
                total += 1
                if col[(a, b)] == col[(a, c)] == col[(b, c)]:
                    mono += 1
    print(f"E8 root graph: {total} triangles, {mono} monochromatic under the colouring")
    print(f"RESULT {mono}")
    return 0


def cell600_forest(args, path):
    adj = cell600_graph()
    S = vertex_list(path, 120)
    parent = {v: v for v in S}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    Sset = set(S)
    for v in S:
        for u in adj[v]:
            if u in Sset and u < v:
                a, b = find(u), find(v)
                if a == b:
                    print(f"the induced subgraph has a cycle (through the edge {u}-{v})")
                    return 1
                parent[a] = b
    print(f"induced forest of the 600-cell on {len(S)} vertices (decycling set of size {120 - len(S)})")
    print(f"RESULT {len(S)}")
    return 0


def overlap_three(args, path):
    m, den = int(args[0]), int(args[1])
    rows = matrix(path)
    if m % 3 or len(rows) != m or any(len(r) != 3 for r in rows):
        print(f"expected {m} lines of three integers (M divisible by 3)")
        return 1
    if any(v < 0 or v > den for r in rows for v in r) or any(sum(r) != den for r in rows):
        print(f"every value must lie in [0, {den}] and every line must sum to {den}")
        return 1
    if any(sum(r[a] for r in rows) * 3 != den * m for a in range(3)):
        print(f"every column must sum to {den} * {m} / 3 (each part of integral 1)")
        return 1
    best, arg = 0, None
    for a in range(3):
        for b in range(3):
            if a == b:
                continue
            for k in range(-(m - 1), m):
                t = sum(rows[i][a] * rows[i - k][b] for i in range(max(0, k), min(m, m + k)))
                if t > best:
                    best, arg = t, (a + 1, b + 1, k)
    r = Fraction(3 * best, m * den * den)
    print(f"three-part step function on [0,3] with {m} cells: largest overlap {r} = {float(r):.12f} "
          f"(parts {arg[0]}, {arg[1]} at shift {arg[2]} cells)")
    print(f"RESULT {r.numerator}/{r.denominator}" if r.denominator != 1 else f"RESULT {r.numerator}")
    return 0


def e8_resolving(args, path):
    W = vertex_list(path, 240)
    if W is None:
        return 1
    adj = [[] for _ in range(240)]
    for a, b in e8_edges():
        adj[a].append(b)
        adj[b].append(a)
    cols = []
    for w in W:
        d = [-1] * 240
        d[w] = 0
        q = [w]
        for u in q:
            for x in adj[u]:
                if d[x] < 0:
                    d[x] = d[u] + 1
                    q.append(x)
        cols.append(d)
    vecs = {}
    for v in range(240):
        key = tuple(c[v] for c in cols)
        if key in vecs:
            print(f"vertices {vecs[key]} and {v} have the same distances {key} to the set")
            return 1
        vecs[key] = v
    print(f"{len(W)} vertices resolve the E8 root graph: all 240 distance vectors are different")
    print(f"RESULT {len(W)}")
    return 0


PROBLEMS = {"autoconv-square": (1, autoconv_square), "e8-resolving": (0, e8_resolving), "overlap-square": (2, overlap_square),
            "overlap-three": (2, overlap_three), "ap-cover": (2, ap_cover), "e8-goodman": (0, e8_goodman),
            "cell600-forest": (0, cell600_forest)}


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
