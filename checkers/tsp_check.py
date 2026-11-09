"""Exact length of a travelling salesman tour for a TSPLIB instance with EUC_2D distances (standard library only).

  python3 -I tsp_check.py INSTANCE TOUR

INSTANCE is a TSPLIB file with EDGE_WEIGHT_TYPE EUC_2D and a NODE_COORD_SECTION ("id x y" per line), such as the
Mona Lisa instance mona-lisa100K.tsp of R. Bosch. TOUR lists the DIMENSION cities in the order visited, either as a
TSPLIB tour file (a TOUR_SECTION ending with -1) or one city id per line; the tour returns to its first city. The
distance between two cities is the TSPLIB EUC_2D distance, the Euclidean distance rounded to the nearest integer
(halves rounded up). It is computed exactly from the coordinates as rational numbers: with q = dx^2 + dy^2, the
distance is the integer r with (r - 1/2)^2 <= q < (r + 1/2)^2. Prints the number of cities and "RESULT L", the tour
length; exits 0 for a tour that visits every city exactly once, 1 otherwise. L is the score (smaller is better)."""
import math
import sys
from fractions import Fraction


def read_instance(path):
    dim, kind, coords, in_coords = None, None, {}, False
    for line in open(path, encoding="ascii", errors="replace"):
        s = line.strip()
        if not s:
            continue
        if in_coords:
            if s == "EOF":
                break
            parts = s.split()
            if len(parts) != 3:
                raise ValueError(f"bad coordinate line {s[:60]!r}")
            coords[int(parts[0])] = (Fraction(parts[1]), Fraction(parts[2]))
            continue
        key = s.split(":")[0].strip().upper()
        if key == "DIMENSION":
            dim = int(s.split(":")[1])
        elif key == "EDGE_WEIGHT_TYPE":
            kind = s.split(":")[1].strip()
        elif key == "NODE_COORD_SECTION":
            in_coords = True
    if kind != "EUC_2D":
        raise ValueError(f"EDGE_WEIGHT_TYPE {kind}; only EUC_2D is supported")
    if dim is None or sorted(coords) != list(range(1, dim + 1)):
        raise ValueError("the coordinates do not cover cities 1..DIMENSION")
    return dim, coords


def read_tour(path):
    ids, in_section, plain = [], False, True
    for line in open(path, encoding="ascii", errors="replace"):
        s = line.strip()
        if not s:
            continue
        if s.upper().startswith("TOUR_SECTION"):
            in_section, plain = True, False
            continue
        if plain and not in_section and not s.lstrip("-").isdigit():
            continue                      # a header line of a TSPLIB tour file
        for tok in s.split():
            if tok == "-1" or tok == "EOF":
                return ids
            ids.append(int(tok))
    return ids


def euc2d(a, b):
    """nint of the Euclidean distance, exactly: the integer r with (r - 1/2)^2 <= q < (r + 1/2)^2."""
    dx, dy = a[0] - b[0], a[1] - b[1]
    q = dx * dx + dy * dy
    if q.denominator == 1:
        qi = q.numerator
        r = math.isqrt(qi)
        return r + 1 if 4 * qi >= (2 * r + 1) ** 2 else r
    num, den = q.numerator, q.denominator
    r = math.isqrt(num // den)
    while Fraction(2 * r + 1, 2) ** 2 <= q:
        r += 1
    while r > 0 and Fraction(2 * r - 1, 2) ** 2 > q:
        r -= 1
    return r


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    try:
        dim, coords = read_instance(sys.argv[1])
        tour = read_tour(sys.argv[2])
    except (ValueError, OSError) as e:
        print(f"cannot read the files: {e}")
        return 1
    if len(tour) != dim or set(tour) != set(range(1, dim + 1)):
        missing = dim - len(set(tour) & set(range(1, dim + 1)))
        print(f"the tour has {len(tour)} entries and misses {missing} of the {dim} cities")
        return 1
    if all(x.denominator == 1 and y.denominator == 1 for x, y in coords.values()):
        pts = {c: (int(x), int(y)) for c, (x, y) in coords.items()}
        total = 0
        for i in range(dim):
            ax, ay = pts[tour[i]]
            bx, by = pts[tour[i - 1]]
            qi = (ax - bx) ** 2 + (ay - by) ** 2
            r = math.isqrt(qi)
            total += r + 1 if 4 * qi >= (2 * r + 1) ** 2 else r
    else:
        total = sum(euc2d(coords[tour[i]], coords[tour[i - 1]]) for i in range(dim))
    print(f"{dim} cities, each visited once; EUC_2D tour length {total}")
    print(f"RESULT {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
