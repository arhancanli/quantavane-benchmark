"""Exact check of a packing whose container or radii are irrational: Packomania's regular-polygon sections and its
sections with radii i^(1/2), i^(-1/2), i^(-2/3) and i^(-1/5). Standard library only.

  python3 -I pack_alg_check.py SECTION N FILE

FILE: the first line that is not blank and does not start with '#' holds one decimal number V; then N lines, each the
centre of one circle, two decimal numbers separated by spaces or commas. Every number is read exactly.

Sections (frames are ours; the containers have Packomania's sizes, so values compare directly):
  equal circles of radius r = V in the regular n-gon with circumradius 1 centred at 0, a vertex at (1, 0); larger is
  better: cpt (n = 5), chx (6), chp (7), coc (8), cno (9), cdc (10), chd (11), cdd (12), ctd (13), crd (14),
  cpd (15), cxd (16), ced (17).
  circle i has radius a_i = i^alpha (i = 1..N, in the order of the lines), container size V, smaller is better:
    ccir (alpha = 1/2), ccis (-1/2), ccic (-2/3), ccib (-1/5): the circle of radius V centred at 0;
    csqr (1/2): the square [0,V]^2;
    csqs: the square [0,V]^2 with a_i = (N/i)^(1/2), so that the smallest circle has radius 1 (Packomania's ratio
          for this section is the side over the smallest radius).

A packing is valid when every circle lies in the container and no two overlap (touching is allowed). Every condition
is an inequality between a rational number and an algebraic one, decided exactly:
- the algebraic side is enclosed in an interval with rational ends (cos(j pi / 2n) as an isolated root of the
  Chebyshev polynomial U_(2n-1), found by bisection in exact rational arithmetic; i^alpha from integer roots), and
  the interval is narrowed (128, 256, ... bits) until it lies on one side of the rational one;
- equality is settled by algebra: for a polygon, the difference is written in the 4n-th roots of unity and reduced
  modulo the cyclotomic polynomial (it is zero exactly when the remainder is); for the radii, a difference can only be
  zero when the radicals in it are rational numbers (a sum of square roots, or of cube or fifth roots, equal to a
  rational number or to the square root of one forces this), and then it is computed exactly.
Pairs of circles are tested through a grid of cells of side 2 max a_i (an upper bound), which is exact.

Prints the reason and exits 1 for an invalid packing or malformed input; otherwise prints the checks made and, as its
last line, "RESULT p/q" (V as an exact fraction), and exits 0."""
import math
import sys
from fractions import Fraction

POLYGON = {"cpt": 5, "chx": 6, "chp": 7, "coc": 8, "cno": 9, "cdc": 10, "chd": 11, "cdd": 12, "ctd": 13, "crd": 14,
           "cpd": 15, "cxd": 16, "ced": 17}
RADII = {"ccir": ("circle", Fraction(1, 2)), "ccis": ("circle", Fraction(-1, 2)), "ccic": ("circle", Fraction(-2, 3)),
         "ccib": ("circle", Fraction(-1, 5)), "csqr": ("square", Fraction(1, 2)), "csqs": ("square", Fraction(1, 2))}
SCALED = {"csqs"}                 # a_i = (N / i)^alpha
PRECISIONS = [128 * 2 ** i for i in range(10)]          # up to 65,536 bits


def parse_dec(s):
    s = s.strip()
    if not s:
        raise ValueError("empty number")
    neg = s.startswith("-")
    body = s[1:] if s[0] in "+-" else s
    if "e" in body.lower() or body.count(".") > 1 or not body.replace(".", "").isdigit():
        raise ValueError("not a decimal number: " + s)
    whole, _, frac = body.partition(".")
    v = Fraction(int((whole or "0") + frac), 10 ** len(frac))
    return -v if neg else v


def read(path, n):
    lines = [l.strip() for l in open(path) if l.strip() and not l.strip().startswith("#")]
    if len(lines) != n + 1:
        raise ValueError(f"expected 1 + {n} lines, found {len(lines)}")
    V = parse_dec(lines[0])
    pts = []
    for i, l in enumerate(lines[1:]):
        parts = [p for p in l.replace(",", " ").split() if p]
        if len(parts) != 2:
            raise ValueError(f"line {i + 2}: expected 2 coordinates, found {len(parts)}")
        pts.append((parse_dec(parts[0]), parse_dec(parts[1])))
    return V, pts


# ------------------------------------------------------------------------------------- cos(j pi / 2n), exactly

def chebyshev_u(deg):
    """Coefficients (lowest first) of U_deg: U_0 = 1, U_1 = 2x, U_(k+1) = 2x U_k - U_(k-1)."""
    a, b = [1], [0, 2]
    if deg == 0:
        return a
    for _ in range(deg - 1):
        c = [0] + [2 * x for x in b]
        for i, x in enumerate(a):
            c[i] -= x
        a, b = b, c
    return b


def poly_sign(coeffs, x):
    v = Fraction(0)
    for c in reversed(coeffs):
        v = v * x + c
    return (v > 0) - (v < 0)


class Cosines:
    """Intervals for cos(j pi / (2n)), j = 0..2n, with rational ends, narrowed on demand."""

    def __init__(self, n):
        self.n = n
        self.U = chebyshev_u(2 * n - 1)       # simple roots cos(j pi / 2n), j = 1..2n-1
        self.cache = {}

    def interval(self, j, bits):
        n = self.n
        j = abs(j) % (4 * n)
        if j > 2 * n:
            j = 4 * n - j
        if j == 0:
            return Fraction(1), Fraction(1)
        if j == 2 * n:
            return Fraction(-1), Fraction(-1)
        if j == n:
            return Fraction(0), Fraction(0)
        key = (j, bits)
        if key in self.cache:
            return self.cache[key]
        f = math.cos(j * math.pi / (2 * n))
        delta = Fraction(1, 10 ** 6)          # the roots are more than 10^-3 apart for n <= 17
        lo, hi = Fraction(f) - delta, Fraction(f) + delta
        slo, shi = poly_sign(self.U, lo), poly_sign(self.U, hi)
        if slo == 0 or shi == 0 or slo == shi:
            raise RuntimeError("root isolation failed")       # cannot happen for these n; refuse rather than guess
        width = Fraction(1, 2 ** bits)
        while hi - lo > width:
            mid = (lo + hi) / 2
            sm = poly_sign(self.U, mid)
            if sm == 0:
                lo = hi = mid
                break
            if sm == slo:
                lo = mid
            else:
                hi = mid
        self.cache[key] = (lo, hi)
        return lo, hi


def cyclotomic(N):
    """Integer coefficients (lowest first) of the N-th cyclotomic polynomial."""
    def divide(num, den):
        num = num[:]
        out = [0] * (len(num) - len(den) + 1)
        for i in range(len(out) - 1, -1, -1):
            c = num[i + len(den) - 1] // den[-1]
            out[i] = c
            for j, d in enumerate(den):
                num[i + j] -= c * d
        assert not any(num), "inexact division"
        return out
    p = [-1] + [0] * (N - 1) + [1]
    for d in range(1, N):
        if N % d == 0:
            p = divide(p, cyclotomic(d))
    return p


class Polygon:
    def __init__(self, n):
        self.n = n
        self.cos = Cosines(n)
        self.phi = cyclotomic(4 * n)

    def edge_terms(self, j):
        """The edge with outward normal at angle (2j+1) pi / n: inside means cos(pi/n) - r - x C - y S >= 0, with
        C = cos(m pi / 2n), S = sin(m pi / 2n) = cos((n - m) pi / 2n), m = 4j + 2."""
        m = 4 * j + 2
        return m, self.n - m

    def is_zero(self, const, x, y, m):
        """Is const + cos(pi/n) - x cos(m pi/2n) - y sin(m pi/2n) zero? In xi = exp(i pi / 2n), a primitive 4n-th
        root of unity: cos(a pi/2n) = (xi^a + xi^-a)/2, sin(a pi/2n) = (xi^a - xi^-a) xi^-n / 2. Twice the value is a
        polynomial in xi; reduce it modulo the 4n-th cyclotomic polynomial."""
        N = 4 * self.n
        c = [Fraction(0)] * N

        def add(e, v):
            c[e % N] += v
        add(0, 2 * const)
        add(2, Fraction(1)); add(-2, Fraction(1))
        add(m, -x); add(-m, -x)
        add(m - self.n, -y); add(-m - self.n, y)
        phi = self.phi
        deg = len(phi) - 1
        for i in range(N - 1, deg - 1, -1):      # reduce (phi is monic)
            v = c[i]
            if v:
                c[i] = Fraction(0)
                for k in range(deg):
                    c[i - deg + k] -= v * phi[k]
        return not any(c)

    def inside(self, r, x, y):
        """Exact: the circle of radius r at (x, y) lies in the polygon. Returns (ok, edge)."""
        n = self.n
        for j in range(n):
            m, m2 = self.edge_terms(j)
            const = -r
            for bits in PRECISIONS:
                alo, ahi = self.cos.interval(2, bits)
                clo, chi = self.cos.interval(m, bits)
                slo, shi = self.cos.interval(m2, bits)
                xs = (x * clo, x * chi) if x >= 0 else (x * chi, x * clo)
                ys = (y * slo, y * shi) if y >= 0 else (y * shi, y * slo)
                lo = const + alo - xs[1] - ys[1]
                hi = const + ahi - xs[0] - ys[0]
                if lo >= 0:
                    break
                if hi < 0:
                    return False, j
                if self.is_zero(const, x, y, m):
                    break                        # touching the edge exactly
            else:
                raise RuntimeError("undecided at 65,536 bits")
        return True, None


# ------------------------------------------------------------------------------------- radii i^alpha, exactly

def iroot(a, k):
    """floor(a^(1/k)) for an integer a >= 0."""
    if a < 2:
        return a
    x = 1 << ((a.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + a // x ** (k - 1)) // k
        if y >= x:
            break
        x = y
    while x ** k > a:
        x -= 1
    while (x + 1) ** k <= a:
        x += 1
    return x


class Radius:
    """a = b^alpha for a positive rational b and alpha = p/q: exact when b^|p| is the q-th power of a rational, else
    an interval narrowed on demand."""

    def __init__(self, b, alpha):
        self.i, self.p, self.q = Fraction(b), alpha.numerator, alpha.denominator
        base = self.i ** abs(self.p)
        u, w = base.numerator, base.denominator
        ru, rw = iroot(u, self.q), iroot(w, self.q)
        self.exact = None
        if ru ** self.q == u and rw ** self.q == w:
            self.exact = Fraction(ru, rw) if self.p > 0 else Fraction(rw, ru)
        self.cache = {}

    def interval(self, bits):
        if self.exact is not None:
            return self.exact, self.exact
        if bits not in self.cache:
            base = self.i ** abs(self.p)
            # floor(base 2^(q bits)) <= base 2^(q bits) < floor(...) + 1, so its q-th root lies in [r, r + 1)
            r = iroot((base.numerator << (self.q * bits)) // base.denominator, self.q)
            lo, hi = Fraction(r, 2 ** bits), Fraction(r + 1, 2 ** bits)       # b^(|p|/q) in [lo, hi]
            self.cache[bits] = (lo, hi) if self.p > 0 else (1 / hi, 1 / lo)
        return self.cache[bits]

    def upper_float(self):
        return float(self.interval(64)[1])


def sign_of(f):
    """Exact sign of an expression, given f(bits) -> (lo, hi) enclosures and, when exact, f(None) -> value."""
    exact = f(None)
    if exact is not None:
        return (exact > 0) - (exact < 0)
    for bits in PRECISIONS:
        lo, hi = f(bits)
        if lo > 0:
            return 1
        if hi < 0:
            return -1
    raise RuntimeError("undecided at 65,536 bits")


def square_iv(lo, hi):
    if lo >= 0:
        return lo * lo, hi * hi
    if hi <= 0:
        return hi * hi, lo * lo
    return Fraction(0), max(lo * lo, hi * hi)


def check_radii(section, V, pts):
    shape, alpha = RADII[section]
    n = len(pts)
    rad = [Radius(Fraction(n, i) if section in SCALED else i, alpha) for i in range(1, n + 1)]
    for i, ((x, y), a) in enumerate(zip(pts, rad)):
        if shape == "circle":
            C = x * x + y * y

            def room(bits, a=a):                                     # V - a >= 0
                if bits is None:
                    return None if a.exact is None else V - a.exact
                lo, hi = a.interval(bits)
                return V - hi, V - lo

            def fits(bits, a=a, C=C):                                # (V - a)^2 - C >= 0
                if bits is None:
                    return None if a.exact is None else (V - a.exact) ** 2 - C
                lo, hi = a.interval(bits)
                s0, s1 = square_iv(V - hi, V - lo)
                return s0 - C, s1 - C
            if sign_of(room) < 0 or sign_of(fits) < 0:
                return False, f"circle {i + 1} outside the circle of radius V"
        else:
            for coord in (x, y):
                for gap in (coord, V - coord):
                    def off(bits, a=a, gap=gap):                     # gap - a >= 0
                        if bits is None:
                            return None if a.exact is None else gap - a.exact
                        lo, hi = a.interval(bits)
                        return gap - hi, gap - lo
                    if sign_of(off) < 0:
                        return False, f"circle {i + 1} outside the square of side V"
    side = Fraction(2 * max(r.upper_float() for r in rad) + 1e-9)
    grid = {}
    for i, (x, y) in enumerate(pts):
        grid.setdefault((math.floor(x / side), math.floor(y / side)), []).append(i)
    pairs = 0
    for (gx, gy), members in grid.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in grid.get((gx + dx, gy + dy), []):
                    for i in members:
                        if j <= i:
                            continue
                        pairs += 1
                        (xi, yi), (xj, yj) = pts[i], pts[j]
                        D = (xi - xj) ** 2 + (yi - yj) ** 2
                        a, b = rad[i], rad[j]

                        def apart(bits, a=a, b=b, D=D):              # D - (a + b)^2 >= 0
                            if bits is None:
                                if a.exact is not None and b.exact is not None:
                                    return D - (a.exact + b.exact) ** 2
                                if a.q == 2:                         # (a+b)^2 = a^2 + b^2 + 2ab, ab = (b_i b_j)^(p/2)
                                    ab = Radius(a.i * b.i, Fraction(a.p, 2))
                                    if ab.exact is not None:
                                        return D - (a.i ** a.p + b.i ** b.p + 2 * ab.exact)
                                return None
                            lo1, hi1 = a.interval(bits)
                            lo2, hi2 = b.interval(bits)
                            return D - (hi1 + hi2) ** 2, D - (lo1 + lo2) ** 2
                        if sign_of(apart) < 0:
                            return False, f"circles {i + 1} and {j + 1} overlap"
    return True, f"{n} circles inside the container; {pairs} nearby pairs tested exactly, none overlapping"


def check_polygon(section, r, pts):
    P = Polygon(POLYGON[section])
    if r <= 0:
        raise ValueError("the radius must be positive")
    for i, (x, y) in enumerate(pts):
        ok, edge = P.inside(r, x, y)
        if not ok:
            return False, f"circle {i + 1} crosses edge {edge + 1} of the polygon"
    side = 2 * r
    grid = {}
    for i, (x, y) in enumerate(pts):
        grid.setdefault((math.floor(x / side), math.floor(y / side)), []).append(i)
    pairs = 0
    four = 4 * r * r
    for (gx, gy), members in grid.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in grid.get((gx + dx, gy + dy), []):
                    for i in members:
                        if j <= i:
                            continue
                        pairs += 1
                        (xi, yi), (xj, yj) = pts[i], pts[j]
                        if (xi - xj) ** 2 + (yi - yj) ** 2 < four:
                            return False, f"circles {i + 1} and {j + 1} overlap"
    return True, (f"{len(pts)} circles inside the regular {P.n}-gon (every edge decided exactly); {pairs} nearby pairs "
                  f"tested exactly, none overlapping")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3:
        print(__doc__)
        return 1
    section, n, path = argv[0], int(argv[1]), argv[2]
    try:
        if section not in POLYGON and section not in RADII:
            raise ValueError("unknown section " + section)
        V, pts = read(path, n)
        if V <= 0:
            raise ValueError("the value must be positive")
        ok, msg = check_polygon(section, V, pts) if section in POLYGON else check_radii(section, V, pts)
    except (ValueError, OSError, RuntimeError) as e:
        print("malformed or undecided:", e)
        return 1
    print(msg)
    if not ok:
        return 1
    print("RESULT", V.numerator if V.denominator == 1 else f"{V.numerator}/{V.denominator}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
