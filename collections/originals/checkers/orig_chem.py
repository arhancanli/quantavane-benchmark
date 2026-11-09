"""Exact checkers for the chemistry problems of the Quantavane Originals (standard library only).

  python3 -I orig_chem.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved, an integer or p/q); it
exits 0 only for a valid certificate and 1 otherwise. Problems:

  benzenoid-kemeny H FILE   FILE: H hexagons "q r" (axial coordinates of the hexagonal tiling: the neighbours of
                            (q, r) are (q+-1, r), (q, r+-1), (q+1, r-1), (q-1, r+1)), one per line. Valid when the
                            hexagons are distinct, connected through shared edges and enclose no hole (a benzenoid
                            system). Value: Kemeny's constant of the molecular graph (vertices: the hexagons' corners;
                            edges: their sides), K = (1/(2m)) * sum over vertex pairs {i, j} of d_i d_j R_ij, with R the
                            resistance distance, d the degrees and m the number of edges, in exact rational arithmetic.
                            (Equivalently K = sum over the eigenvalues lambda != 1 of the transition matrix of
                            1/(1 - lambda).)
  cata-kemeny H FILE        the same for catacondensed benzenoids: valid only if the molecular graph has no internal
                            vertex (every carbon atom on the perimeter; equivalently 4H + 2 vertices and no three
                            hexagons sharing a vertex). Value: Kemeny's constant, exactly.
  lj-fcc N FILE             FILE: N lines "x y z", distinct integer points with x + y + z even (sites of the
                            face-centred cubic lattice, nearest neighbours at squared distance 2). Value: the
                            Lennard-Jones energy with the nearest-neighbour distance at the minimum of the pair
                            potential, cut off at 2.5 sigma: the sum over the pairs at squared distance q <= 8 (the
                            first four shells) of 64/q^6 - 16/q^3 (each nearest-neighbour pair counts -1), in exact
                            rational arithmetic.
  diamond-bonds N FILE      FILE: N lines "x y z", distinct sites of the diamond lattice: either all three coordinates
                            even with x + y + z = 0 (mod 4) (sublattice A) or all three odd with x + y + z = 3 (mod 4)
                            (sublattice B = A + (1, 1, 1)); two sites are bonded when their squared distance is 3 (each
                            site has four bonds in the crystal). Valid when the N atoms are connected through bonds (one
                            molecule). Value: the number of dangling bonds, 4N - 2B with B the bonds between the atoms:
                            the number of hydrogen atoms of the hydrocarbon C_N H_(4N-2B) cut from diamond.
  diamond-knot FILE         FILE: lines "x y z", the atoms of a ring in order: distinct sites of the diamond lattice,
                            each bonded (squared distance 3) to the next and the last to the first (a closed
                            self-avoiding polygon of the lattice). Valid when the ring is knotted, as certified by its
                            knot determinant |Delta(-1)| (computed from a regular projection: the Fox colouring matrix
                            of the diagram with one row and one column removed) being larger than 1 (1 for the unknot,
                            3 for the trefoil, 5 for the figure-eight knot). Value: the number of atoms.
  diamond-link FILE         FILE: two rings of the diamond lattice, each as lines "x y z" in order (distinct sites,
                            each bonded to the next and the last to the first), separated by a line holding only "-".
                            Valid when the rings share no site and are linked: their linking number, half the sum of
                            the signs of the crossings between them in a regular projection, is not zero (a [2]catenane).
                            Value: the total number of atoms."""
import sys
from fractions import Fraction

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]


def cells(path):
    out = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if line:
            q, r = (int(t) for t in line.replace(",", " ").split())
            out.append((q, r))
    return out


def connected(cs):
    s = set(cs)
    seen = {cs[0]}
    stack = [cs[0]]
    while stack:
        q, r = stack.pop()
        for dq, dr in DIRS:
            n = (q + dq, r + dr)
            if n in s and n not in seen:
                seen.add(n)
                stack.append(n)
    return len(seen) == len(s)


def has_hole(cs):
    s = set(cs)
    lo_q, hi_q = min(q for q, r in s) - 2, max(q for q, r in s) + 2
    lo_r, hi_r = min(r for q, r in s) - 2, max(r for q, r in s) + 2
    seen = {(lo_q, lo_r)}
    stack = [(lo_q, lo_r)]
    while stack:
        q, r = stack.pop()
        for dq, dr in DIRS:
            n = (q + dq, r + dr)
            if lo_q <= n[0] <= hi_q and lo_r <= n[1] <= hi_r and n not in s and n not in seen:
                seen.add(n)
                stack.append(n)
    return len(seen) != (hi_q - lo_q + 1) * (hi_r - lo_r + 1) - len(s)


def molecular_graph(cs):
    idx, edges = {}, set()
    for q, r in cs:
        cx, cy = 2 * q + r, r - q
        cor = [(cx + a, cy + b) for a, b in ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))]
        for v in cor:
            idx.setdefault(v, len(idx))
        for i in range(6):
            a, b = idx[cor[i]], idx[cor[(i + 1) % 6]]
            edges.add((min(a, b), max(a, b)))
    return len(idx), sorted(edges)


def kemeny(n, edges):
    deg = [0] * n
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    # M = L + J/n is invertible; its inverse G gives R_ij = G_ii + G_jj - 2 G_ij
    A = [[Fraction(1, n)] * n + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for i in range(n):
        A[i][i] += deg[i]
    for a, b in edges:
        A[a][b] -= 1
        A[b][a] -= 1
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    G = [row[n:] for row in A]
    s = Fraction(0)
    for i in range(n):
        for j in range(i + 1, n):
            s += deg[i] * deg[j] * (G[i][i] + G[j][j] - 2 * G[i][j])
    return s / (2 * len(edges))


def benzenoid_kemeny(args, path):
    h = int(args[0])
    cs = cells(path)
    if len(cs) != h or len(set(cs)) != h:
        print(f"{len(cs)} hexagons ({len(set(cs))} distinct), expected {h} distinct hexagons")
        return 1
    if not connected(cs):
        print("the hexagons are not connected through shared edges")
        return 1
    if has_hole(cs):
        print("the hexagons enclose a hole (not a benzenoid system)")
        return 1
    n, edges = molecular_graph(cs)
    k = kemeny(n, edges)
    print(f"benzenoid with {h} hexagons: {n} vertices, {len(edges)} edges; Kemeny's constant {k} = {float(k):.12f}")
    print(f"RESULT {k.numerator}/{k.denominator}" if k.denominator != 1 else f"RESULT {k.numerator}")
    return 0


def cata_kemeny(args, path):
    h = int(args[0])
    cs = cells(path)
    if len(cs) == h and len(set(cs)) == h:
        n, edges = molecular_graph(cs)
        if n != 4 * h + 2:
            print(f"not catacondensed: {n} vertices instead of {4 * h + 2} (some carbon atom is internal)")
            return 1
    return benzenoid_kemeny(args, path)


def lj_fcc(args, path):
    n = int(args[0])
    pts = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if line:
            x, y, z = (int(t) for t in line.split())
            pts.append((x, y, z))
    if len(pts) != n or len(set(pts)) != n:
        print(f"expected {n} distinct points")
        return 1
    if any((x + y + z) % 2 for x, y, z in pts):
        print("a point with an odd coordinate sum is not a site of the face-centred cubic lattice")
        return 1
    terms = {}
    for i in range(n):
        for j in range(i + 1, n):
            q = sum((a - b) ** 2 for a, b in zip(pts[i], pts[j]))
            if q <= 8:
                terms[q] = terms.get(q, 0) + 1
    energy = sum(Fraction(64 * c, q ** 6) - Fraction(16 * c, q ** 3) for q, c in terms.items())
    print(f"{n} atoms, {terms.get(2, 0)} nearest-neighbour pairs; energy {float(energy):.9f}")
    print(f"RESULT {energy.numerator}/{energy.denominator}" if energy.denominator != 1 else f"RESULT {energy.numerator}")
    return 0


def diamond_site(x, y, z):
    if x % 2 == 0 and y % 2 == 0 and z % 2 == 0:
        return (x + y + z) % 4 == 0
    if x % 2 == 1 and y % 2 == 1 and z % 2 == 1:
        return (x + y + z) % 4 == 3
    return False


def diamond_bonds(args, path):
    n = int(args[0])
    pts = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if line:
            x, y, z = (int(t) for t in line.split())
            pts.append((x, y, z))
    if len(pts) != n or len(set(pts)) != n:
        print(f"expected {n} distinct sites, found {len(pts)} ({len(set(pts))} distinct)")
        return 1
    bad = [p for p in pts if not diamond_site(*p)]
    if bad:
        print(f"{bad[0]} is not a site of the diamond lattice")
        return 1
    where = set(pts)
    steps = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
    nbrs = {p: [q for q in ((p[0] + a, p[1] + b, p[2] + c) for a, b, c in steps) if q in where] for p in pts}
    bonds = sum(len(v) for v in nbrs.values()) // 2
    seen, stack = {pts[0]}, [pts[0]]
    while stack:
        for q in nbrs[stack.pop()]:
            if q not in seen:
                seen.add(q)
                stack.append(q)
    if len(seen) != n:
        print(f"the atoms are not connected: {len(seen)} of {n} reachable from the first one")
        return 1
    print(f"{n} atoms of the diamond lattice, connected, {bonds} bonds; dangling bonds (hydrogens) 4N - 2B = {4 * n - 2 * bonds}: C{n}H{4 * n - 2 * bonds}")
    print(f"RESULT {4 * n - 2 * bonds}")
    return 0


KNOT_DIRS = [(1, 3, 7), (2, 5, 11), (3, 7, 13), (5, 2, 9), (7, 11, 4), (4, 9, 17), (11, 6, 5), (13, 17, 3)]


def _cross3(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def _on_seg(a, b, c):
    return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])


def knot_diagram(pts, d):
    """The crossings of the projection of the closed polygon pts along the direction d, as (point, segment i,
    parameter s, segment j, parameter t, True when segment i passes over), or None when the projection is not
    regular (two vertices on one point, a vertex on another segment, adjacent segments collinear, two crossings at
    one point)."""
    e = (1, 0, 0) if d[0] == 0 else (0, 1, 0)
    u = _cross3(d, e)
    v = _cross3(d, u)
    P = [(_dot3(u, p), _dot3(v, p)) for p in pts]
    H = [_dot3(d, p) for p in pts]
    n = len(pts)
    if len(set(P)) != n:
        return None
    out = []
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        for j in range(i + 1, n):
            c, dd = P[j], P[(j + 1) % n]
            if j == i + 1 or (i == 0 and j == n - 1):
                if _orient(a, b, dd if j == i + 1 else c) == 0:
                    return None
                continue
            o1, o2, o3, o4 = _orient(a, b, c), _orient(a, b, dd), _orient(c, dd, a), _orient(c, dd, b)
            if 0 in (o1, o2, o3, o4):
                if (o1 == 0 and _on_seg(a, b, c)) or (o2 == 0 and _on_seg(a, b, dd)) or \
                        (o3 == 0 and _on_seg(c, dd, a)) or (o4 == 0 and _on_seg(c, dd, b)):
                    return None
                continue
            if (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0):
                s_, t_ = Fraction(o3, o3 - o4), Fraction(o1, o1 - o2)
                hi = H[i] + s_ * (H[(i + 1) % n] - H[i])
                hj = H[j] + t_ * (H[(j + 1) % n] - H[j])
                if hi == hj:
                    return None
                out.append(((a[0] + s_ * (b[0] - a[0]), a[1] + s_ * (b[1] - a[1])), i, s_, j, t_, hi > hj))
    if len({c[0] for c in out}) != len(out):
        return None
    return out


def knot_determinant(pts):
    """|Delta(-1)| of a closed polygon given by integer points, from the first regular projection in KNOT_DIRS."""
    for d in KNOT_DIRS:
        cr = knot_diagram(pts, d)
        if cr is not None:
            break
    else:
        raise ValueError("no regular projection found among the built-in directions")
    if not cr:
        return 1
    unders = [((j, t), (i, s_), k) if i_over else ((i, s_), (j, t), k) for k, (pt, i, s_, j, t, i_over) in enumerate(cr)]
    cuts = sorted(u for u, o, k in unders)
    m = len(cuts)
    rows = []
    for under, over, k in unders:
        r_out = cuts.index(under)
        r_over = (sum(1 for c in cuts if c < over) - 1) % m
        row = [0] * m
        row[r_over] += 2
        row[(r_out - 1) % m] -= 1
        row[r_out] -= 1
        rows.append(row)
    A = [[Fraction(x) for x in row[1:]] for row in rows[1:]]
    det = Fraction(1)
    for c in range(len(A)):
        piv = next((r for r in range(c, len(A)) if A[r][c] != 0), None)
        if piv is None:
            return 0
        if piv != c:
            A[c], A[piv] = A[piv], A[c]
            det = -det
        det *= A[c][c]
        for r in range(c + 1, len(A)):
            if A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return abs(int(det))


def diamond_knot(args, path):
    pts = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if line:
            x, y, z = (int(t) for t in line.split())
            pts.append((x, y, z))
    n = len(pts)
    if n < 6 or len(set(pts)) != n:
        print(f"expected at least 6 distinct sites, found {n} ({len(set(pts))} distinct)")
        return 1
    bad = [p for p in pts if not diamond_site(*p)]
    if bad:
        print(f"{bad[0]} is not a site of the diamond lattice")
        return 1
    for i in range(n):
        if sum((a - b) ** 2 for a, b in zip(pts[i], pts[(i + 1) % n])) != 3:
            print(f"atoms {i} and {(i + 1) % n} are not bonded (squared distance 3)")
            return 1
    det = knot_determinant(pts)
    if det == 1:
        print(f"a ring of {n} atoms whose knot determinant is 1: not certified knotted")
        return 1
    print(f"a ring of {n} atoms of the diamond lattice, knotted: knot determinant |Delta(-1)| = {det}")
    print(f"RESULT {n}")
    return 0


def linking_number(A, B):
    """The linking number of two disjoint closed polygons (integer points), from the first projection direction in
    KNOT_DIRS that is regular for the pair: the signed crossings where A passes over B (the crossings where B passes
    over A give the same number, which is checked)."""
    for d in KNOT_DIRS:
        e = (1, 0, 0) if d[0] == 0 else (0, 1, 0)
        u = _cross3(d, e)
        v = _cross3(d, u)
        PA = [(_dot3(u, p), _dot3(v, p)) for p in A]
        PB = [(_dot3(u, p), _dot3(v, p)) for p in B]
        HA = [_dot3(d, p) for p in A]
        HB = [_dot3(d, p) for p in B]
        if len(set(PA) | set(PB)) != len(A) + len(B):
            continue
        over, under, points, regular = 0, 0, set(), True
        for i in range(len(A)):
            a, b = PA[i], PA[(i + 1) % len(A)]
            for j in range(len(B)):
                c, dd = PB[j], PB[(j + 1) % len(B)]
                o1, o2, o3, o4 = _orient(a, b, c), _orient(a, b, dd), _orient(c, dd, a), _orient(c, dd, b)
                if 0 in (o1, o2, o3, o4):
                    if (o1 == 0 and _on_seg(a, b, c)) or (o2 == 0 and _on_seg(a, b, dd)) or \
                            (o3 == 0 and _on_seg(c, dd, a)) or (o4 == 0 and _on_seg(c, dd, b)):
                        regular = False
                    continue
                if (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0):
                    s_, t_ = Fraction(o3, o3 - o4), Fraction(o1, o1 - o2)
                    ha = HA[i] + s_ * (HA[(i + 1) % len(A)] - HA[i])
                    hb = HB[j] + t_ * (HB[(j + 1) % len(B)] - HB[j])
                    pt = (a[0] + s_ * (b[0] - a[0]), a[1] + s_ * (b[1] - a[1]))
                    if ha == hb or pt in points:
                        regular = False
                    points.add(pt)
                    cr = (b[0] - a[0]) * (dd[1] - c[1]) - (b[1] - a[1]) * (dd[0] - c[0])
                    sign = 1 if cr > 0 else -1
                    if ha > hb:           # A over B: sign of (over direction x under direction)
                        over += sign
                    else:                 # B over A: the same product taken the other way round
                        under -= sign
            if not regular:
                break
        if regular:
            if over != under:
                raise ValueError("inconsistent crossing signs")
            return over
    raise ValueError("no regular projection found among the built-in directions")


def diamond_link(args, path):
    rings, cur = [], []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if line == "-":
            rings.append(cur)
            cur = []
        elif line:
            x, y, z = (int(t) for t in line.split())
            cur.append((x, y, z))
    rings.append(cur)
    if len(rings) != 2:
        print(f"expected two rings separated by a line '-', found {len(rings)}")
        return 1
    for k, ring in enumerate(rings):
        n = len(ring)
        if n < 6 or len(set(ring)) != n:
            print(f"ring {k + 1}: expected at least 6 distinct sites, found {n}")
            return 1
        bad = [p for p in ring if not diamond_site(*p)]
        if bad:
            print(f"ring {k + 1}: {bad[0]} is not a site of the diamond lattice")
            return 1
        for i in range(n):
            if sum((a - b) ** 2 for a, b in zip(ring[i], ring[(i + 1) % n])) != 3:
                print(f"ring {k + 1}: atoms {i} and {(i + 1) % n} are not bonded (squared distance 3)")
                return 1
    if set(rings[0]) & set(rings[1]):
        print("the two rings share a site")
        return 1
    lk = linking_number(rings[0], rings[1])
    if lk == 0:
        print("linking number 0: the rings are not certified linked")
        return 1
    total = len(rings[0]) + len(rings[1])
    print(f"two rings of {len(rings[0])} and {len(rings[1])} atoms of the diamond lattice, linking number {lk}")
    print(f"RESULT {total}")
    return 0


PROBLEMS = {"benzenoid-kemeny": (1, benzenoid_kemeny), "cata-kemeny": (1, cata_kemeny), "lj-fcc": (1, lj_fcc),
            "diamond-bonds": (1, diamond_bonds),
            "diamond-knot": (0, diamond_knot),
            "diamond-link": (0, diamond_link)}


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
