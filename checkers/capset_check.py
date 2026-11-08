"""Exact check of a cap set in F_3^N (standard library only).

  python3 -I capset_check.py N FILE

FILE holds the points separated by whitespace, each written as its N coordinates, digits 0 to 2 with nothing between
them (the format of Leaps in Bounds). A cap set has no three distinct points on a line; three distinct points x, y, z
are on a line exactly when x + y + z = 0 coordinatewise mod 3. For every pair x, y the checker looks up the third
point -(x + y) of their line. Prints the size and "RESULT size"; exits 0 for a valid cap set, 1 otherwise."""
import sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    n = int(sys.argv[1])
    pts = "\n".join(line.split("#")[0] for line in open(sys.argv[2], encoding="ascii", errors="replace")).split()
    for p in pts:
        if len(p) != n or any(c not in "012" for c in p):
            print(f"point {p[:40]!r} is not {n} digits from 0 to 2")
            return 1
    if len(set(pts)) != len(pts):
        print("a point is repeated")
        return 1
    have = set(pts)
    vec = [[int(c) for c in p] for p in pts]
    for i in range(len(vec)):
        a = vec[i]
        for j in range(i + 1, len(vec)):
            b = vec[j]
            z = "".join("012"[(-(x + y)) % 3] for x, y in zip(a, b))
            if z in have:
                print(f"{pts[i]}, {pts[j]} and {z} lie on a line")
                return 1
    print(f"cap set in F_3^{n}: {len(pts)} points, no three on a line")
    print(f"RESULT {len(pts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
