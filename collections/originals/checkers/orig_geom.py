"""Exact checkers for the discrete geometry problems of the Quantavane Originals (standard library only).

  python3 -I orig_geom.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved); it exits 0 only for a
valid certificate and 1 otherwise. Points of the triangular grid T_n are written "a b" (one per line), meaning the
point a + b*e^(i*pi/3) with a, b >= 0 and a + b <= n - 1; the squared distance between two points is
da^2 + da*db + db^2, and three points are collinear when da1*db2 - da2*db1 = 0 (|da1*db2 - da2*db1| is the area of
their triangle in units of sqrt(3)/4, the area of a unit triangle). Problems:

  tri-distinct N FILE      points of T_N with all pairwise distances distinct. Value: the number of points.
  tri-areas N FILE         points of T_N such that every three of them form a triangle of nonzero area and all
                           these areas are different. Value: the number of points.
  tetra-distinct N FILE    FILE: lines "a b c", points of the tetrahedral grid (a, b, c >= 0, a + b + c <= N - 1), the
                           point a e1 + b e2 + c e3 with unit vectors at 60 degrees to each other (a piece of the
                           face-centred cubic lattice); squared distance da^2 + db^2 + dc^2 + da db + db dc + da dc.
                           Valid when the points are distinct and all pairwise distances are different. Value: the
                           number of points.
  cell120-great FILE       FILE: one line "a b c d" per chosen vertex of the 120-cell, written as the tetrahedral cell
                           of the 600-cell it is the centre of (four vertex numbers 0..119 of the 600-cell, numbered
                           as in checkers/orig_codes.py). Valid when the cells are distinct tetrahedral cells and no
                           three of the chosen vertices lie on a common great circle, i.e. no three of the centre
                           vectors lie in a plane through the origin (exact arithmetic in Q(sqrt 5)). Value: the
                           number of chosen vertices."""
import itertools
import sys
from itertools import combinations


def tri_points(path, n):
    pts = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        a, b = (int(t) for t in line.replace(",", " ").split())
        if a < 0 or b < 0 or a + b > n - 1:
            raise ValueError(f"({a}, {b}) is not a point of T_{n}")
        pts.append((a, b))
    if len(set(pts)) != len(pts):
        raise ValueError("a point is repeated")
    return pts


def area(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]))



def tri_distinct(args, path):
    n = int(args[0])
    pts = tri_points(path, n)
    seen = {}
    for p, q in combinations(pts, 2):
        da, db = p[0] - q[0], p[1] - q[1]
        d = da * da + da * db + db * db
        if d in seen:
            print(f"the squared distance {d} occurs twice: {seen[d]} and {(p, q)}")
            return 1
        seen[d] = (p, q)
    print(f"{len(pts)} points of T_{n}, all {len(seen)} pairwise distances distinct")
    print(f"RESULT {len(pts)}")
    return 0



def tri_areas(args, path):
    n = int(args[0])
    pts = tri_points(path, n)
    seen = {}
    for p, q, r in combinations(pts, 3):
        a = area(p, q, r)
        if a == 0:
            print(f"collinear: {p} {q} {r}")
            return 1
        if a in seen:
            print(f"the area {a} (units of sqrt(3)/4) occurs twice: {seen[a]} and {(p, q, r)}")
            return 1
        seen[a] = (p, q, r)
    print(f"{len(pts)} points of T_{n}: all {len(seen)} triangle areas nonzero and distinct")
    print(f"RESULT {len(pts)}")
    return 0


def tetra_distinct(args, path):
    n = int(args[0])
    pts = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if line:
            pts.append(tuple(int(t) for t in line.split()))
    if any(len(p) != 3 or min(p) < 0 or sum(p) > n - 1 for p in pts) or len(set(pts)) != len(pts):
        print(f"the points must be distinct (a, b, c) with a, b, c >= 0 and a + b + c <= {n - 1}")
        return 1
    seen = {}
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            a, b, c = (pts[i][k] - pts[j][k] for k in range(3))
            q = a * a + b * b + c * c + a * b + b * c + a * c
            if q in seen:
                print(f"squared distance {q} occurs twice: {pts[i]}, {pts[j]} and {seen[q]}")
                return 1
            seen[q] = (pts[i], pts[j])
    print(f"{len(pts)} points of the tetrahedral grid of side {n}, all {len(seen)} distances different")
    print(f"RESULT {len(pts)}")
    return 0


def _q5mul(x, y):      # a + b sqrt5 as pairs of Fractions
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def _q5sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def _q5div(x, y):      # x / y = x (a - b sqrt5) / (a^2 - 5 b^2)
    d = y[0] * y[0] - 5 * y[1] * y[1]
    return _q5mul(x, (y[0] / d, -y[1] / d))


def cell600_points():
    """The 600-cell's 120 vertices (unit quaternions of the binary icosahedral group) with coordinates in Q(sqrt 5),
    sorted: the numbering of cell600_graph in checkers/orig_codes.py."""
    from fractions import Fraction as F
    h, z = (F(1, 2), F(0)), (F(0), F(0))
    phi_h = _q5mul((F(1, 2), F(1, 2)), h)
    iphi_h = _q5mul((F(-1, 2), F(1, 2)), h)
    neg = lambda x: (-x[0], -x[1])
    pts = set()
    for i in range(4):
        for sg in ((F(1), F(0)), (F(-1), F(0))):
            v = [z] * 4
            v[i] = sg
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
    return sorted(pts), phi_h


def cell600_cells():
    """The 600 tetrahedral cells of the 600-cell (4-cliques of its graph) as sorted vertex tuples, and the vertices."""
    pts, phi_h = cell600_points()
    ip = lambda a, b: tuple(sum(x) for x in zip(*[_q5mul(a[k], b[k]) for k in range(4)]))
    adj = [{b for b in range(120) if b != a and ip(pts[a], pts[b]) == phi_h} for a in range(120)]
    cells = sorted({tuple(sorted((a, b, c, d))) for a in range(120) for b in adj[a] for c in adj[a] & adj[b]
                    for d in adj[a] & adj[b] & adj[c]})
    return cells, pts, adj


def _vsum(vs):
    return tuple(tuple(sum(v[k][t] for v in vs) for t in range(2)) for k in range(4))


def plane_key(u, v):
    """Normalised Plucker coordinates of the plane spanned by u and v, or None when u and v are parallel."""
    pl = [_q5sub(_q5mul(u[i], v[j]), _q5mul(u[j], v[i])) for i, j in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))]
    lead = next((x for x in pl if x != (0, 0)), None)
    if lead is None:
        return None
    return tuple(_q5div(x, lead) for x in pl)


def great_points(kind):
    """One vertex of each antipodal pair: of the 600-cell (kind '600', labels = vertex numbers) or of the 120-cell
    (kind '120', vertices = centres of the 600-cell's cells, labels = the cells)."""
    if kind == "600":
        pts, _ = cell600_points()
        items = [(pts[i], i) for i in range(120)]
    else:
        cells, pts, _ = cell600_cells()
        items = [(_vsum([pts[i] for i in c]), c) for c in cells]
    seen, out, labels = set(), [], []
    for v, lab in items:
        neg = tuple((-x[0], -x[1]) for x in v)
        if neg in seen:
            continue
        seen.add(v)
        out.append(v)
        labels.append(lab)
    return out, labels


def great_lines(pts):
    """The planes through the origin spanned by two of the points, each with the set of points it contains."""
    lines = {}
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            k = plane_key(pts[i], pts[j])
            lines.setdefault(k, set()).update((i, j))
    return list(lines.values())


def cell120_great(args, path):
    cells, pts, adj = cell600_cells()
    cellset = set(cells)
    chosen = []
    for line in open(path):
        line = line.split("#")[0].strip()
        if line:
            t = tuple(sorted(int(x) for x in line.split()))
            if t not in cellset:
                print(f"{t} is not a tetrahedral cell of the 600-cell")
                return 1
            chosen.append(t)
    if len(set(chosen)) != len(chosen):
        print("a vertex is listed twice")
        return 1
    vecs = [_vsum([pts[i] for i in c]) for c in chosen]
    planes = {}
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            k = plane_key(vecs[i], vecs[j])
            if k is None:
                print(f"vertices {i + 1} and {j + 1} are opposite: with any third vertex they lie on a great circle")
                if len(vecs) >= 3:
                    return 1
                continue
            planes.setdefault(k, set()).update((i, j))
    worst = max((len(v) for v in planes.values()), default=0)
    if worst >= 3:
        print(f"{worst} of the vertices lie on one great circle")
        return 1
    print(f"{len(vecs)} vertices of the 120-cell, no three on a great circle ({len(planes)} planes, two vertices each)")
    print(f"RESULT {len(vecs)}")
    return 0


PROBLEMS = {"tetra-distinct": (1, tetra_distinct), "cell120-great": (0, cell120_great), "tri-distinct": (1, tri_distinct), "tri-areas": (1, tri_areas)}


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
