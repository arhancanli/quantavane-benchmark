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
                            rational arithmetic."""
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


PROBLEMS = {"benzenoid-kemeny": (1, benzenoid_kemeny), "cata-kemeny": (1, cata_kemeny), "lj-fcc": (1, lj_fcc)}


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
