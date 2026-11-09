"""Exact checkers for the discrete geometry problems of the Quantavane Originals (standard library only).

  python3 -I orig_geom.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved); it exits 0 only for a
valid certificate and 1 otherwise. Points of the triangular grid T_n are written "a b" (one per line), meaning the
point a + b*e^(i*pi/3) with a, b >= 0 and a + b <= n - 1; the squared distance between two points is
da^2 + da*db + db^2, and three points are collinear when da1*db2 - da2*db1 = 0 (|da1*db2 - da2*db1| is the area of
their triangle in units of sqrt(3)/4, the area of a unit triangle). Problems:

  tri-distinct N FILE      points of T_N with all pairwise distances distinct. Value: the number of points.
  tri-areas N FILE         points of T_N such that every three of them form a triangle of nonzero area and all
                           these areas are different. Value: the number of points."""
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


PROBLEMS = {"tri-distinct": (1, tri_distinct), "tri-areas": (1, tri_areas)}


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
