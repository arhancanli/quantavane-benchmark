"""Exact checkers for the colouring problems of the Quantavane Originals (standard library only).

  python3 -I orig_colour.py PROBLEM K FILE

FILE: the colours of 1, 2, ..., n as digits 0..K-1, in order (line breaks, spaces and lines starting with # are
ignored). The check lists every solution of the equation with all its numbers at most n and verifies that none is
monochromatic; it prints what it verified and ends with "RESULT n" (n, the length of the colouring); it exits 0 only
for a valid colouring. Problems:

  quad-pyth    Pythagorean quadruples x^2 + y^2 + z^2 = w^2 with 1 <= x <= y <= z < w <= n (x, y, z may repeat:
               1 + 4 + 4 = 9). For each w and each z < w the checker looks up every way to write w^2 - z^2 as x^2 + y^2
               with x <= y <= z in a table of the sums of two squares up to n^2 built by direct enumeration.
  squares-ap   three squares in arithmetic progression, x^2 + y^2 = 2 z^2 with 1 <= x < z < y <= n. Since x and y have
               the same parity, u = (y + x)/2 and v = (y - x)/2 satisfy u^2 + v^2 = z^2, and conversely; the checker
               lists the Pythagorean triples (u, v, z) with u + v <= n by Euclid's formula k (m^2 - l^2, 2ml, m^2 + l^2)
               over all coprime m > l of opposite parity and all k, which gives every triple exactly once."""
import math
import sys


def colouring(path, k):
    s = "".join(l.split("#")[0] for l in open(path, encoding="ascii", errors="replace"))
    s = "".join(s.split())
    if not s or any(c not in "0123456789"[:k] for c in s):
        raise ValueError(f"expected a string of digits 0..{k - 1}")
    return [None] + [int(c) for c in s]


def quad_pyth(n):
    two = {}
    for y in range(1, n + 1):
        for x in range(1, y + 1):
            two.setdefault(x * x + y * y, []).append((x, y))
    for w in range(2, n + 1):
        for z in range(1, w):
            for x, y in two.get(w * w - z * z, ()):
                if y <= z:
                    yield (x, y, z, w)


def squares_ap(n):
    m = 2
    while m * m + 2 * m - 1 <= n:      # u + v = m^2 + 2ml - l^2 grows with l, smallest at l = 1
        for l in range(1, m):
            if m * m + 2 * m * l - l * l > n:
                break
            if (m - l) % 2 == 1 and math.gcd(m, l) == 1:
                a, b, c = m * m - l * l, 2 * m * l, m * m + l * l
                u, v = max(a, b), min(a, b)
                kk = 1
                while kk * (u + v) <= n:
                    yield (kk * (u - v), kk * c, kk * (u + v))        # x < z < y
                    kk += 1
        m += 1


EQUATIONS = {"quad-pyth": quad_pyth, "squares-ap": squares_ap}


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in EQUATIONS:
        print(__doc__)
        return 2
    try:
        k = int(sys.argv[2])
        if not 2 <= k <= 10:
            raise ValueError("K must be between 2 and 10")
        col = colouring(sys.argv[3], k)
    except (ValueError, OSError) as e:
        print(f"unreadable certificate: {e}")
        return 1
    n = len(col) - 1
    count = 0
    for sol in EQUATIONS[sys.argv[1]](n):
        count += 1
        if len({col[v] for v in sol}) == 1:
            print(f"not valid: the solution {sol} is monochromatic (colour {col[sol[0]]})")
            return 1
    print(f"a colouring of 1..{n} with {k} colours: none of the {count} solutions is monochromatic")
    print(f"RESULT {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
