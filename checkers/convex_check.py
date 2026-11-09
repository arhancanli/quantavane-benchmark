"""Exact check of a counterexample to the Erdos-Szekeres conjecture (Erdos problem #107; standard library only).

  python3 -I convex_check.py FILE

The Erdos-Szekeres ("happy ending") conjecture says that among any 2^(n-2) + 1 points in the plane in general position
some n of them are the vertices of a convex polygon; it is proved for n <= 6 (f(6) = 17, Szekeres and Peters 2006).
FILE holds points, one "x y" per line with integer coordinates. The checker refuses repeated points and any three
points on a line (the condition "general position"), then computes c, the largest number of the points in convex
position, exactly: for every point p taken as the lowest vertex, the other points above it are sorted by angle around
p and a dynamic programme over pairs of consecutive vertices finds the longest chain with only left turns that closes
at p. The set is a counterexample when it has at least 2^(c-1) + 1 points, since then it has no convex (c+1)-gon.
Prints the number of points and c; for a counterexample prints "RESULT 1" and exits 0, otherwise exits 1."""
import functools
import sys
from math import gcd


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def general_position(pts):
    """None if no two points coincide and no three are collinear, else a message."""
    n = len(pts)
    if len(set(pts)) != n:
        return "two points coincide"
    for i in range(n):
        seen = {}
        xi, yi = pts[i]
        for j in range(n):
            if j == i:
                continue
            dx, dy = pts[j][0] - xi, pts[j][1] - yi
            g = gcd(dx, dy)
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            if (dx, dy) in seen:
                return f"points {i}, {seen[(dx, dy)]} and {j} are collinear"
            seen[(dx, dy)] = j
    return None


def largest_convex(pts):
    """The largest number of the points in convex position (all of them vertices of their convex hull)."""
    n = len(pts)
    best = min(n, 2)
    if n >= 3:
        best = 3                            # any three points in general position
    for p in pts:
        above = [q for q in pts if (q[1], q[0]) > (p[1], p[0])]
        if len(above) + 1 <= best:
            continue
        # angular order around p, counterclockwise from the direction (1, 0); all angles lie in [0, pi)
        above.sort(key=functools.cmp_to_key(lambda a, b: -1 if cross(p, a, b) > 0 else 1))
        m = len(above)
        # f[i][j]: most vertices of a chain p -> ... -> above[i] -> above[j] (i < j) with left turns only
        f = [[0] * m for _ in range(m)]
        for j in range(m):
            for i in range(j):
                f[i][j] = 3                  # p -> above[i] -> above[j] is always a left turn here
        for i in range(m):
            # chains ending with the edge h -> i, best first, extended by i -> j where (h, i, j) turns left
            incoming = sorted(((f[h][i], h) for h in range(i)), reverse=True)
            a = above[i]
            for j in range(i + 1, m):
                b = above[j]
                for val, h in incoming:
                    if val + 1 <= f[i][j]:
                        break
                    if cross(above[h], a, b) > 0:
                        f[i][j] = val + 1
                        break
        for i in range(m):
            for j in range(i + 1, m):
                if f[i][j] > best and cross(above[i], above[j], p) > 0:
                    best = f[i][j]
    return best


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    pts = []
    for line in open(sys.argv[1], encoding="ascii", errors="replace"):
        s = line.split("#")[0].replace(",", " ").split()
        if not s:
            continue
        if len(s) != 2:
            print(f"not a point: {line.strip()[:60]!r}")
            return 1
        try:
            pts.append((int(s[0]), int(s[1])))
        except ValueError:
            print(f"coordinates must be integers: {line.strip()[:60]!r}")
            return 1
    msg = general_position(pts)
    if msg:
        print(f"not in general position: {msg}")
        return 1
    n = len(pts)
    c = largest_convex(pts)
    print(f"{n} points in general position; the largest subset in convex position has {c} points")
    if n >= 2 ** (c - 1) + 1:
        print(f"{n} >= 2^{c - 1} + 1 points with no convex {c + 1}-gon: a counterexample to the conjecture")
        print("RESULT 1")
        return 0
    print(f"not a counterexample: a counterexample with no convex {c + 1}-gon needs at least {2 ** (c - 1) + 1} points")
    return 1


if __name__ == "__main__":
    sys.exit(main())
