"""Exact check of a packing of circles or balls in a container (the Packomania sections with rational geometry).
Standard library only.

  python3 -I pack_check.py SECTION N FILE

FILE: the first line that is not blank and does not start with '#' holds one decimal number V; then N lines, each
the centre of one circle or ball, its coordinates as decimal numbers separated by spaces or commas. All numbers are
read exactly (as fractions with a power-of-ten denominator) and every test below is done in integer arithmetic, so
the verdict has no rounding at all.

Sections (containers in our frame; Packomania's containers have the same size, so its values compare directly):
  equal radius r = V, larger is better:
    csq   circles in the unit square [0,1]^2
    cci   circles in the circle of radius 1 centred at 0
    csc   circles in the half disc {y >= 0, x^2 + y^2 <= 1}
    ccq   circles in the quarter disc {x >= 0, y >= 0, x^2 + y^2 <= 1}
    crt   circles in the isosceles right triangle {x >= 0, y >= 0, x + y <= 1}
    scu   balls in the unit cube [0,1]^3
    ssp   balls in the ball of radius 1 centred at 0 in R^3
    hsp4, hsp5, hsp6   balls in the ball of radius 1 centred at 0 in R^4, R^5, R^6
  circle i has radius i (i = 1..N, in the order of the lines), container size V, smaller is better:
    ccin  the circle of radius V centred at 0
    csqn  the square [0,V]^2
A packing is valid when every circle (ball) lies in the container and no two overlap (touching is allowed):
|c_i - c_j|^2 >= (r_i + r_j)^2 for i < j. Pairs are tested through a grid of cells of side 2 max r_i, which is exact:
two centres in cells that are not neighbours differ by at least the cell side in some coordinate.

Prints the reason and exits 1 for an invalid packing or malformed input; otherwise prints the checks made and, as
its last line, "RESULT p/q" (V as an exact reduced fraction; the line before it gives V as written), and exits 0."""
import sys
from math import gcd


EQUAL = {"csq": 2, "cci": 2, "csc": 2, "ccq": 2, "crt": 2, "scu": 3, "ssp": 3, "hsp4": 4, "hsp5": 5, "hsp6": 6}
GROWING = {"ccin": 2, "csqn": 2}


def parse_dec(s):
    s = s.strip()
    if not s:
        raise ValueError("empty number")
    neg = s.startswith("-")
    if s[0] in "+-":
        s = s[1:]
    if "e" in s.lower():
        raise ValueError("exponents are not accepted: " + s)
    if s.count(".") > 1 or not s.replace(".", "").isdigit():
        raise ValueError("not a decimal number: " + s)
    whole, _, frac = s.partition(".")
    num = int((whole or "0") + frac)
    return (-num if neg else num), len(frac)


def read(path, dim, n):
    lines = [l.strip() for l in open(path) if l.strip() and not l.strip().startswith("#")]
    if len(lines) != n + 1:
        raise ValueError(f"expected 1 + {n} lines, found {len(lines)}")
    raw = [parse_dec(lines[0])]
    pts = []
    for i, l in enumerate(lines[1:]):
        parts = [p for p in l.replace(",", " ").split() if p]
        if len(parts) != dim:
            raise ValueError(f"line {i + 2}: expected {dim} coordinates, found {len(parts)}")
        pts.append([parse_dec(p) for p in parts])
    scale = max([raw[0][1]] + [d for p in pts for _, d in p])
    S = 10 ** scale

    def to_int(v):
        num, d = v
        return num * 10 ** (scale - d)
    return to_int(raw[0]), [[to_int(v) for v in p] for p in pts], S


def check(section, n, path):
    if section in EQUAL:
        dim = EQUAL[section]
    elif section in GROWING:
        dim = GROWING[section]
    else:
        raise ValueError("unknown section " + section)
    V, P, S = read(path, dim, n)          # every number is (integer) / S
    if V <= 0:
        raise ValueError("the value must be positive")
    radii = [V] * n if section in EQUAL else [i * S for i in range(1, n + 1)]
    # container: each test is an exact inequality between integers (numbers scaled by S, squares by S^2)
    for i, (c, r) in enumerate(zip(P, radii)):
        bad = None
        if section in ("csq", "scu"):
            if any(x < r or x > S - r for x in c):
                bad = "outside the unit square/cube"
        elif section in ("cci", "ssp", "hsp4", "hsp5", "hsp6"):
            if r > S or sum(x * x for x in c) > (S - r) ** 2:
                bad = "outside the unit ball"
        elif section == "csc":
            x, y = c
            if r > S or y < r or x * x + y * y > (S - r) ** 2:
                bad = "outside the half disc"
        elif section == "ccq":
            x, y = c
            if r > S or x < r or y < r or x * x + y * y > (S - r) ** 2:
                bad = "outside the quarter disc"
        elif section == "crt":
            x, y = c
            g = S - x - y                  # sqrt(2) times the distance to the hypotenuse, scaled by S
            if x < r or y < r or g < 0 or g * g < 2 * r * r:
                bad = "outside the triangle"
        elif section == "ccin":
            if V < r or sum(x * x for x in c) > (V - r) ** 2:
                bad = f"circle of radius {i + 1} outside the circle of radius V"
        elif section == "csqn":
            if any(x < r or x > V - r for x in c):
                bad = f"circle of radius {i + 1} outside the square of side V"
        if bad:
            return False, f"circle {i + 1}: {bad}"
    side = 2 * max(radii)
    grid = {}
    for i, c in enumerate(P):
        grid.setdefault(tuple(x // side for x in c), []).append(i)
    pairs = 0
    from itertools import product
    offsets = [o for o in product((-1, 0, 1), repeat=dim)]
    for key, members in grid.items():
        for o in offsets:
            other = grid.get(tuple(k + d for k, d in zip(key, o)))
            if not other:
                continue
            for i in members:
                ci, ri = P[i], radii[i]
                for j in other:
                    if j <= i:
                        continue
                    pairs += 1
                    s = ri + radii[j]
                    if sum((a - b) * (a - b) for a, b in zip(ci, P[j])) < s * s:
                        return False, f"circles {i + 1} and {j + 1} overlap"
    return True, f"{n} centres inside the container; {pairs} nearby pairs tested exactly, none overlapping"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3:
        print(__doc__)
        return 1
    section, n, path = argv[0], int(argv[1]), argv[2]
    try:
        ok, msg = check(section, n, path)
    except (ValueError, OSError) as e:
        print("malformed:", e)
        return 1
    print(msg)
    if not ok:
        return 1
    value = [l.strip() for l in open(path) if l.strip() and not l.strip().startswith("#")][0]
    num, d = parse_dec(value)
    g = gcd(num, 10 ** d)
    p, q = num // g, 10 ** d // g
    print("value", value)
    print("RESULT", p if q == 1 else f"{p}/{q}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
