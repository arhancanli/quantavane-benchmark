"""Exact check of a no-three-in-line set in the N x N grid (standard library only).

  python3 -I no3line_check.py N FILE

FILE holds the points separated by whitespace, each written x,y with integers 0 <= x, y < N (the format of Leaps in
Bounds). No three of them may lie on a line. For each point the checker reduces the direction to every other point to
lowest terms with a fixed sign; a direction seen twice means three points on a line. Prints the number of points and
"RESULT size"; exits 0 for a valid set, 1 otherwise."""
import math
import sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    n = int(sys.argv[1])
    pts = []
    for tok in "\n".join(line.split("#")[0] for line in open(sys.argv[2], encoding="ascii", errors="replace")).split():
        try:
            x, y = (int(v) for v in tok.split(","))
        except ValueError:
            print(f"{tok[:40]!r} is not a point x,y")
            return 1
        if not (0 <= x < n and 0 <= y < n):
            print(f"point {x},{y} is outside the {n} x {n} grid")
            return 1
        pts.append((x, y))
    if len(set(pts)) != len(pts):
        print("a point is repeated")
        return 1
    for i, (x, y) in enumerate(pts):
        dirs = {}
        for j, (u, v) in enumerate(pts):
            if j == i:
                continue
            dx, dy = u - x, v - y
            g = math.gcd(dx, dy)
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            if (dx, dy) in dirs:
                print(f"{pts[dirs[(dx, dy)]]}, {(x, y)} and {(u, v)} lie on a line")
                return 1
            dirs[(dx, dy)] = j
    print(f"{len(pts)} points in the {n} x {n} grid, no three on a line")
    print(f"RESULT {len(pts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
