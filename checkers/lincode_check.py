"""Exact minimum distance of a linear code over GF(Q), Q in {2, 3, 4, 5, 7, 8, 9} (standard library only).

  python3 -I lincode_check.py Q N K FILE

FILE is a generator matrix: K rows of N field elements, written as integers 0..Q-1 separated by spaces or commas, or
as N digits with no separators. Blank lines and lines starting with '#' are ignored. For prime Q an element is a
residue mod Q. For Q = 4, 8 and 9 the integer a = a_0 + a_1 p + a_2 p^2 (p = 2, 2, 3) stands for the polynomial
a_0 + a_1 x + a_2 x^2 modulo x^2 + x + 1 (Q = 4), x^3 + x + 1 (Q = 8) or x^2 + 2x + 2 (Q = 9), the Conway
polynomials, so that x is a primitive element.

The rows must be linearly independent (rank K, found by Gaussian elimination). The minimum distance is then computed
exactly from the weight distribution:
- when K <= N - K, by listing every codeword once per line through the origin (the codewords whose first nonzero
  coefficient is 1, each multiple having the same weight), stepping through them with a Gray code so that each step
  adds one vector;
- otherwise by listing the codewords of the dual code (dimension N - K, a generator built from the reduced echelon
  form and checked orthogonal to every given row) in the same way and applying the MacWilliams identities, in exact
  integer arithmetic, to the weights 1, 2, ... of the code itself until one is held by a codeword (each count is
  checked to be a non-negative integer).
The work is about Q^min(K, N-K) / (Q - 1) vector additions.

Prints the number of codewords of each weight (up to D when the dual code was listed), "distance D" and, as its last line, "RESULT D", and exits 0 for a valid generator
matrix; exits 1 otherwise."""
import math
import sys

try:
    popcount = int.bit_count        # Python 3.10+
except AttributeError:              # Python 3.9
    def popcount(x):
        return bin(x).count("1")

# (characteristic p, degree e, modulus coefficients from x^0 up to x^e)
FIELDS = {2: (2, 1, None), 3: (3, 1, None), 5: (5, 1, None), 7: (7, 1, None),
          4: (2, 2, (1, 1, 1)), 8: (2, 3, (1, 1, 0, 1)), 9: (3, 2, (2, 2, 1))}


class Field:
    def __init__(self, q):
        self.q = q
        self.p, self.e, mod = FIELDS[q]
        p, e = self.p, self.e

        def digits(a):
            return [(a // p ** i) % p for i in range(e)]

        def number(ds):
            return sum(d * p ** i for i, d in enumerate(ds))

        self.digits = [digits(a) for a in range(q)]
        self.add = [[number([(x + y) % p for x, y in zip(digits(a), digits(b))]) for b in range(q)] for a in range(q)]
        self.neg = [number([(-x) % p for x in digits(a)]) for a in range(q)]

        def mul(a, b):
            if e == 1:
                return a * b % p
            prod = [0] * (2 * e - 1)
            for i, x in enumerate(digits(a)):
                for j, y in enumerate(digits(b)):
                    prod[i + j] = (prod[i + j] + x * y) % p
            for i in range(2 * e - 2, e - 1, -1):     # reduce with x^e = -(mod_0 + ... + mod_(e-1) x^(e-1))
                c = prod[i]
                if c:
                    prod[i] = 0
                    for j in range(e):
                        prod[i - e + j] = (prod[i - e + j] - c * mod[j]) % p
            return number(prod[:e])

        self.mul = [[mul(a, b) for b in range(q)] for a in range(q)]
        self.inv = [0] * q
        for a in range(1, q):
            self.inv[a] = next(b for b in range(1, q) if self.mul[a][b] == 1)
        if e > 1:   # x must be primitive (the moduli above are Conway polynomials)
            powers, y = set(), 1
            for _ in range(q - 1):
                y = self.mul[y][p]
                powers.add(y)
            assert len(powers) == q - 1, "x is not primitive"


def rref(F, rows, n):
    """Reduced row echelon form; returns (rows, pivot columns). Row operations only."""
    rows = [r[:] for r in rows]
    pivots, r = [], 0
    for c in range(n):
        if r == len(rows):
            break
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = F.inv[rows[r][c]]
        rows[r] = [F.mul[inv][x] for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = F.neg[rows[i][c]]
                rows[i] = [F.add[x][F.mul[f][y]] for x, y in zip(rows[i], rows[r])]
        pivots.append(c)
        r += 1
    return rows[:r], pivots


def dual_basis(F, echelon, pivots, n):
    """A basis of the dual code: for each non-pivot column f, the vector with 1 at f and -G[i][f] at pivot i."""
    free = [c for c in range(n) if c not in set(pivots)]
    out = []
    for f in free:
        h = [0] * n
        h[f] = 1
        for i, pc in enumerate(pivots):
            h[pc] = F.neg[echelon[i][f]]
        out.append(h)
    return out


class Packed:
    """Vectors over GF(q) as e 'planes', one per base-p digit of the coordinates. p = 2: a plane is a bit mask. p odd:
    a plane holds one 5-bit field per coordinate (value 0..p-1), added with a carry-free mod-p reduction."""

    def __init__(self, F, n):
        self.F, self.n, self.p, self.e = F, n, F.p, F.e
        if self.p > 2:
            self.ones = sum(1 << (5 * i) for i in range(n))
            self.c = (16 - self.p) * self.ones

    def pack(self, vec):
        planes = []
        for d in range(self.e):
            x = 0
            for i, a in enumerate(vec):
                dig = self.F.digits[a][d]
                if dig:
                    x |= dig << (i if self.p == 2 else 5 * i)
            planes.append(x)
        return planes


def projective_histogram(F, basis, n):
    """Weights of the nonzero codewords of the span of basis, one codeword per line through the origin."""
    P = Packed(F, n)
    p, e, q = F.p, F.e, F.q
    hist = [0] * (n + 1)
    x_power = [1]
    for _ in range(e - 1):
        x_power.append(F.mul[x_power[-1]][p])
    for i in range(len(basis)):
        start = P.pack(basis[i])
        gens = [P.pack([F.mul[a][y] for y in basis[j]]) for j in range(i + 1, len(basis)) for a in x_power]
        if p == 2:
            _walk_binary(start, gens, hist)
        else:
            _walk_odd(P, start, gens, hist)
    return hist


def _walk_binary(start, gens, hist):
    e = len(start)
    count = 1 << len(gens)
    if e == 1:
        c = start[0]
        g = [x[0] for x in gens]
        hist[popcount(c)] += 1
        for s in range(1, count):
            c ^= g[(s & -s).bit_length() - 1]
            hist[popcount(c)] += 1
    else:
        cur = list(start)
        hist[popcount(_or(cur))] += 1
        for s in range(1, count):
            g = gens[(s & -s).bit_length() - 1]
            for d in range(e):
                cur[d] ^= g[d]
            hist[popcount(_or(cur))] += 1


def _or(planes):
    x = 0
    for y in planes:
        x |= y
    return x


def _walk_odd(P, start, gens, hist):
    p, e, ones, c = P.p, P.e, P.ones, P.c
    cur = list(start)
    nz = _or(cur)
    hist[popcount((nz | nz >> 1 | nz >> 2) & ones)] += 1
    G = len(gens)
    digit = [0] * G
    for _ in range(p ** G - 1):
        j = 0                                   # modular Gray code: the first counter digit below p - 1 steps up
        while digit[j] == p - 1:
            digit[j] = 0
            j += 1
        digit[j] += 1
        g = gens[j]
        for d in range(e):
            s = cur[d] + g[d]
            cur[d] = s - (((s + c) >> 4) & ones) * p
        nz = _or(cur)
        hist[popcount((nz | nz >> 1 | nz >> 2) & ones)] += 1


def krawtchouk(n, q, i, j):
    return sum((-1) ** s * (q - 1) ** (i - s) * math.comb(j, s) * math.comb(n - j, i - s) for s in range(i + 1))


def weight_distribution(F, rows, n, k):
    """(weights, how): the number of codewords of weight 0, 1, ..., d, where d is the minimum distance (the full
    distribution when every codeword is listed)."""
    echelon, pivots = rref(F, rows, n)
    if len(pivots) < k:
        raise ValueError(f"the rows have rank {len(pivots)}, not {k}: not a generator matrix of a [{n},{k}] code")
    q = F.q
    if k <= n - k:
        h = projective_histogram(F, echelon, n)
        A = [x * (q - 1) for x in h]
        A[0] = 1
        return A, "listed every codeword"
    dual = dual_basis(F, echelon, pivots, n)
    for g in rows:                                  # the dual basis is orthogonal to every row given
        for hv in dual:
            s = 0
            for a, b in zip(g, hv):
                if a and b:
                    s = F.add[s][F.mul[a][b]]
            if s:
                raise AssertionError("dual basis not orthogonal")
    h = projective_histogram(F, dual, n) if dual else [0] * (n + 1)
    B = [x * (q - 1) for x in h]
    B[0] = 1
    size = q ** (n - k)
    A = [1]
    for i in range(1, n - k + 2):                   # the Singleton bound: d <= n - k + 1
        num = sum(B[j] * krawtchouk(n, q, i, j) for j in range(n + 1) if B[j])
        if num % size or num < 0:
            raise AssertionError("MacWilliams transform not a non-negative integer")
        A.append(num // size)
        if A[-1]:
            break
    return A, f"listed every codeword of the dual code (dimension {n - k}) and applied the MacWilliams identities"


def read_matrix(path, q, n):
    rows = []
    for no, line in enumerate(open(path), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.replace(",", " ").split()
        if len(parts) == 1 and len(s) == n and s.isdigit():
            parts = list(s)
        try:
            row = [int(x) for x in parts]
        except ValueError:
            raise SystemExit(f"line {no}: not a row of integers")
        if len(row) != n:
            raise SystemExit(f"line {no}: {len(row)} entries, not {n}")
        if not all(0 <= x < q for x in row):
            raise SystemExit(f"line {no}: an entry outside 0..{q - 1}")
        rows.append(row)
    return rows


def main():
    q, n, k = (int(x) for x in sys.argv[1:4])
    if q not in FIELDS or not 1 <= k <= n:
        print(f"need Q in {sorted(FIELDS)} and 1 <= K <= N, got Q={q} N={n} K={k}")
        return 1
    rows = read_matrix(sys.argv[4], q, n)
    if len(rows) != k:
        print(f"{len(rows)} rows, not {k}")
        return 1
    F = Field(q)
    try:
        A, how = weight_distribution(F, rows, n, k)
    except ValueError as err:
        print(err)
        return 1
    d = next(i for i in range(1, n + 1) if A[i])
    print(f"[{n},{k}] code over GF({q}): {how}")
    print("codewords by weight" + (" (up to the minimum distance)" if len(A) <= n else "") + ": "
          + " ".join(f"{i}:{a}" for i, a in enumerate(A) if a))
    print(f"distance {d}")
    print(f"RESULT {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
