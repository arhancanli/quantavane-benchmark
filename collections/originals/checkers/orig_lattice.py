"""Exact checkers for the lattice point-set problems of the Quantavane Originals (standard library only).

  python3 -I orig_lattice.py PROBLEM N FILE

PROBLEM is LATTICE-PROPERTY. FILE lists distinct points of the region of side N of the lattice, one point per line as
integers (lines starting with # are skipped). Every computation is exact integer arithmetic. The check prints what it
verified and ends with "RESULT v", v the number of points; it exits 0 only for a valid certificate, 1 otherwise.

Lattices and their regions of side N:

  tri      the triangular grid T_N: points "a b" with a, b >= 0 and a + b <= N - 1, the point a + b w of the plane,
           w = e^(i pi/3); squared distance da^2 + da db + db^2 (unit nearest-neighbour distance).
  hex      the honeycomb grid of side N: the points (a, b) of T_N with a - b not divisible by 3. The triangular lattice
           without its index-3 sublattice of hexagon centres is the honeycomb (graphene) lattice with unit bonds;
           the metric is that of T_N.
  kagome   the kagome grid of side N: the points (a, b) of T_N with a and b not both even (the triangular lattice
           without the index-4 sublattice 2Z[w], the kagome lattice with unit bonds); the metric is that of T_N.
  cube     the cubic grid {0, ..., N-1}^3: points "x y z", squared distance dx^2 + dy^2 + dz^2.
  tetra    the tetrahedral grid of side N (a piece of the face-centred cubic lattice): points "a b c" with a, b, c >= 0
           and a + b + c <= N - 1, the point a e1 + b e2 + c e3 with unit vectors at 60 degrees to each other;
           squared distance da^2 + db^2 + dc^2 + da db + db dc + dc da (as in tetra-distinct, checkers/orig_geom.py).
  bcc      the body-centred cubic crystal of side N: points "x y z" with 0 <= x, y, z <= 2N - 2 and x, y, z all even
           (the N^3 cube corners) or all odd (the (N-1)^3 cube centres); coordinates in units of half the cube edge,
           squared distance dx^2 + dy^2 + dz^2 (nearest neighbours at 3).

Properties (each a condition on every pair, triple or quadruple of the chosen points):

  distinct   all pairwise distances are different.
  isosceles  no point is equidistant from two others: no three points p, q, r with |pq| = |pr| (this includes the
             degenerate case of p the midpoint of q and r), so every point sees all the others at different distances.
  right      no three points p, q, r with a right angle at p: (q - p).(r - p) = 0.
  collinear  no three points on a line."""
import itertools
import sys

LATTICES = ("tri", "hex", "kagome", "cube", "tetra", "bcc")
PROPS = ("distinct", "isosceles", "right", "collinear")


def member(lat, n, p):
    if lat in ("tri", "hex", "kagome"):
        if len(p) != 2:
            return False
        a, b = p
        if a < 0 or b < 0 or a + b > n - 1:
            return False
        if lat == "hex":
            return (a - b) % 3 != 0
        if lat == "kagome":
            return not (a % 2 == 0 and b % 2 == 0)
        return True
    if len(p) != 3:
        return False
    if lat == "cube":
        return all(0 <= c <= n - 1 for c in p)
    if lat == "tetra":
        return min(p) >= 0 and sum(p) <= n - 1
    if lat == "bcc":
        return all(0 <= c <= 2 * n - 2 for c in p) and p[0] % 2 == p[1] % 2 == p[2] % 2
    raise ValueError(lat)


def dot2(lat, u, v):
    """Twice the inner product (an integer for every lattice here)."""
    if lat in ("tri", "hex", "kagome"):
        return 2 * u[0] * v[0] + u[0] * v[1] + u[1] * v[0] + 2 * u[1] * v[1]
    if lat == "tetra":
        return (2 * (u[0] * v[0] + u[1] * v[1] + u[2] * v[2]) + u[0] * v[1] + u[1] * v[0] + u[1] * v[2] + u[2] * v[1]
                + u[0] * v[2] + u[2] * v[0])
    return 2 * (u[0] * v[0] + u[1] * v[1] + u[2] * v[2])


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def d2(lat, p, q):
    u = sub(p, q)
    return dot2(lat, u, u) // 2


def collinear(u, v):
    if len(u) == 2:
        return u[0] * v[1] - u[1] * v[0] == 0
    return u[1] * v[2] - u[2] * v[1] == 0 and u[2] * v[0] - u[0] * v[2] == 0 and u[0] * v[1] - u[1] * v[0] == 0


def read_points(lat, n, path):
    pts = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        p = tuple(int(t) for t in line.replace(",", " ").split())
        if not member(lat, n, p):
            raise ValueError(f"{p} is not a point of the {lat} region of side {n}")
        pts.append(p)
    if len(set(pts)) != len(pts):
        raise ValueError("a point is repeated")
    return pts


def check(lat, prop, n, pts):
    """None if the points have the property, else a description of a violation."""
    if prop == "distinct":
        seen = {}
        for p, q in itertools.combinations(pts, 2):
            d = d2(lat, p, q)
            if d in seen:
                return f"the squared distance {d} occurs twice: {seen[d]} and {(p, q)}"
            seen[d] = (p, q)
        return None
    if prop == "isosceles":
        for p in pts:
            seen = {}
            for q in pts:
                if q != p:
                    d = d2(lat, p, q)
                    if d in seen:
                        return f"{p} is at squared distance {d} from both {seen[d]} and {q}"
                    seen[d] = q
        return None
    if prop == "right":
        for p in pts:
            others = [sub(q, p) for q in pts if q != p]
            for u, v in itertools.combinations(others, 2):
                if dot2(lat, u, v) == 0:
                    return f"a right angle at {p}"
        return None
    if prop == "collinear":
        for p, q, r in itertools.combinations(pts, 3):
            if collinear(sub(q, p), sub(r, p)):
                return f"{p}, {q} and {r} are collinear"
        return None
    raise ValueError(prop)


def main():
    if len(sys.argv) != 4 or "-" not in sys.argv[1]:
        print(__doc__)
        return 2
    lat, prop = sys.argv[1].split("-", 1)
    if lat not in LATTICES or prop not in PROPS:
        print(__doc__)
        return 2
    try:
        n = int(sys.argv[2])
        pts = read_points(lat, n, sys.argv[3])
    except (ValueError, OSError) as e:
        print(f"unreadable certificate: {e}")
        return 1
    bad = check(lat, prop, n, pts)
    if bad:
        print(f"not valid: {bad}")
        return 1
    what = {"distinct": "all pairwise distances different", "isosceles": "no point equidistant from two others",
            "right": "no right angle", "collinear": "no three on a line"}[prop]
    print(f"{len(pts)} points of the {lat} region of side {n}: {what}")
    print(f"RESULT {len(pts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
