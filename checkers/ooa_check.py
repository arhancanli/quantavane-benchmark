"""Exact strength check of a linear ordered orthogonal array over GF(B): orthogonal arrays (depth 1), ordered
orthogonal arrays of depth 2 to 8, and digital nets (standard library only).

  python3 -I ooa_check.py B T M K FILE [--way E|D|both] [--max-work N]

B is one of 2, 3, 4, 5, 7, 8, 9, 16, 25, 27, 32, 49, 64, 81, 128, 256. T is the depth: an integer, or the word net.
The object is the set of the B^M vectors x G, x in GF(B)^M, where G has M rows and S * D columns: S factors, each
with D columns in order of depth, D = T for an integer T and D = K for T = net (a digital (M - K, M, S)-net is the
same thing as such an array: column j of factor i is row j of the i-th generator matrix). It has strength K when,
for every way of taking the first d_i columns of each factor with d_1 + ... + d_S = K, those K columns of G are
linearly independent. Columns deeper than K never matter.

FILE holds G: M rows of S * D field elements, written as integers 0..B-1 separated by spaces or commas (for B up to 9
a row may also be one string of digits). Blank lines and lines starting with '#' are ignored. For a prime B an
element is a residue. Otherwise the integer a = a_0 + a_1 p + a_2 p^2 + ... stands for a_0 + a_1 x + a_2 x^2 + ...
modulo the polynomial listed in FIELDS (the Conway polynomial of the field); the program checks that x is primitive,
which also proves the polynomial irreducible.

Two separate exact methods:
  D  walks every choice of depths with a running echelon basis and stops at the first dependent column
     (about N * K steps, N = the number of depth vectors of weight K);
  E  lists the row space once per line through the origin, records for each word how many leading zeros each factor
     has, and computes from that the number of dual words of each weight 1..K in the Niederreiter-Rosenbloom-Tsfasman
     metric (a MacWilliams identity in exact integers): strength K means all those numbers are zero
     (about B^M * S * D / (B - 1) steps).
By default the cheaper one runs; --way both runs the two and requires the same verdict.

Prints "RESULT S" as its last line and exits 0 when the strength is at least K; prints the reason and exits 1 when it
is not or the input is malformed; exits 2 when both methods would need more than --max-work steps (default 2^33)."""
import sys

# (characteristic p, degree e, modulus coefficients from x^0 up to x^e)
FIELDS = {2: (2, 1, None), 3: (3, 1, None), 5: (5, 1, None), 7: (7, 1, None),
          4: (2, 2, (1, 1, 1)), 8: (2, 3, (1, 1, 0, 1)), 9: (3, 2, (2, 2, 1)), 16: (2, 4, (1, 1, 0, 0, 1)),
          25: (5, 2, (2, 4, 1)), 27: (3, 3, (1, 2, 0, 1)), 32: (2, 5, (1, 0, 1, 0, 0, 1)), 49: (7, 2, (3, 6, 1)),
          64: (2, 6, (1, 1, 0, 1, 1, 0, 1)), 81: (3, 4, (2, 0, 0, 2, 1)), 128: (2, 7, (1, 1, 0, 0, 0, 0, 0, 1)),
          256: (2, 8, (1, 0, 1, 1, 1, 0, 0, 0, 1))}


class Field:
    def __init__(self, q):
        self.q = q
        p, e, mod = FIELDS[q]
        self.p, self.e = p, e
        dig = [[(a // p ** i) % p for i in range(e)] for a in range(q)]

        def number(ds):
            return sum(d * p ** i for i, d in enumerate(ds))

        self.add = [[number([(x + y) % p for x, y in zip(dig[a], dig[b])]) for b in range(q)] for a in range(q)]
        self.neg = [number([(-x) % p for x in dig[a]]) for a in range(q)]

        def mul(a, b):
            if e == 1:
                return a * b % p
            prod = [0] * (2 * e - 1)
            for i, x in enumerate(dig[a]):
                if x:
                    for j, y in enumerate(dig[b]):
                        prod[i + j] = (prod[i + j] + x * y) % p
            for i in range(2 * e - 2, e - 1, -1):     # x^e = -(mod_0 + ... + mod_(e-1) x^(e-1))
                c = prod[i]
                if c:
                    prod[i] = 0
                    for j in range(e):
                        prod[i - e + j] = (prod[i - e + j] - c * mod[j]) % p
            return number(prod[:e])

        self.mul = [[mul(a, b) for b in range(q)] for a in range(q)]
        self.inv = [0] * q
        for a in range(1, q):
            self.inv[a] = next(b for b in range(1, q) if self.mul[a][b] == 1)      # fails if a has no inverse
        if e > 1:
            powers, y = set(), 1
            for _ in range(q - 1):
                y = self.mul[y][p]
                powers.add(y)
            assert len(powers) == q - 1, "x is not primitive"


def depth_vectors(s, t, k, cap):
    """Number of d in [0, t]^s with sum k (may stop early once it exceeds cap)."""
    row = [1] + [0] * k
    for _ in range(s):
        new, run = [0] * (k + 1), 0
        for j in range(k + 1):
            run += row[j]
            if j - t - 1 >= 0:
                run -= row[j - t - 1]
            new[j] = run
        row = new
        if row[k] > cap:
            break
    return row[k]


# ---------------------------------------------------------------- method D: depth vectors with a running basis
def way_d(F, cols, s, t, k):
    """cols[i][j] = column j of factor i (a tuple of M field elements). Returns (ok, message, leaves)."""
    q, mul, add, neg, inv = F.q, F.mul, F.add, F.neg, F.inv
    binary = q == 2
    if binary:
        cols = [[sum(v << r for r, v in enumerate(c)) for c in fac] for fac in cols]
    leaves = 0

    def reduce(v, basis):
        if binary:
            for pbit, bv in basis:
                if v & pbit:
                    v ^= bv
            return v
        v = list(v)
        for piv, bv in basis:
            c = v[piv]
            if c:
                f = neg[c]
                v = [add[x][mul[f][y]] for x, y in zip(v, bv)]
        return v

    def pivoted(v):
        if binary:
            return (v & -v, v)
        piv = next(i for i, x in enumerate(v) if x)
        f = inv[v[piv]]
        return (piv, [mul[f][x] for x in v])

    def rec(start, r, basis, chosen):
        nonlocal leaves
        for i in range(start, s):
            if (s - i) * t < r:                       # not enough factors left to reach weight K
                return None
            b2 = basis
            for d in range(1, min(t, r) + 1):
                v = reduce(cols[i][d - 1], b2)
                if (v == 0) if binary else (not any(v)):
                    return chosen + [(i + 1, d)]
                b2 = b2 + [pivoted(v)]
                if r - d == 0:
                    leaves += 1
                else:
                    bad = rec(i + 1, r - d, b2, chosen + [(i + 1, d)])
                    if bad:
                        return bad
        return None

    bad = rec(0, k, [], [])
    if bad:
        return False, "dependent columns: (factor, depth) = " + ", ".join(f"({i},{d})" for i, d in bad), leaves
    return True, f"{leaves} depth vectors of weight {k}, all independent", leaves


# ---------------------------------------------------------------- method E: row space and dual weights
def way_e(F, cols, m, s, t, k):
    """Returns (ok, message). cols as in way_d; only the first t columns of each factor are used."""
    q, mul, add, neg = F.q, F.mul, F.add, F.neg
    L = s * t
    rows = [[cols[i][j][r] for i in range(s) for j in range(t)] for r in range(m)]
    tally = {}

    def profile_of(word):
        prof = [0] * (t + 1)
        for i in range(s):
            base = i * t
            lz = 0
            while lz < t and word[base + lz] == 0:
                lz += 1
            prof[lz] += 1
        return tuple(prof)

    if q == 2:
        ints = [sum(v << c for c, v in enumerate(row)) for row in rows]
        if t == 1:
            hist = [0] * (s + 1)
            w = 0
            for g in range(1, 1 << m):
                w ^= ints[(g & -g).bit_length() - 1]
                hist[bin(w).count("1")] += 1
            for wt, c in enumerate(hist):
                if c:
                    tally[(wt, s - wt)] = c
        else:
            mask = (1 << t) - 1
            lzt = [next((j for j in range(t) if (v >> j) & 1), t) for v in range(1 << t)]
            shifts = [i * t for i in range(s)]
            w = 0
            for g in range(1, 1 << m):
                w ^= ints[(g & -g).bit_length() - 1]
                prof = [0] * (t + 1)
                for sh in shifts:
                    prof[lzt[(w >> sh) & mask]] += 1
                key = tuple(prof)
                tally[key] = tally.get(key, 0) + 1
    else:
        mult = [[[mul[c][x] for x in row] for c in range(q)] for row in rows]          # mult[r][c] = c * row r
        for lead in range(m):                          # words whose first nonzero coefficient is 1, at row `lead`
            free = list(range(lead + 1, m))
            cur = rows[lead][:]
            digits = [0] * len(free)
            while True:
                key = profile_of(cur)
                tally[key] = tally.get(key, 0) + (q - 1)
                pos = 0                                # odometer: next coefficient vector
                while pos < len(free):
                    r, old = free[pos], digits[pos]
                    new = (old + 1) % q
                    digits[pos] = new
                    delta = mult[r][add[new][neg[old]]]
                    cur = [add[x][y] for x, y in zip(cur, delta)]
                    if new:
                        break
                    pos += 1
                else:
                    break
    zero = [0] * (t + 1)
    zero[t] = s
    tally[tuple(zero)] = tally.get(tuple(zero), 0) + 1                                  # the zero word
    assert sum(tally.values()) == q ** m

    def polymul(a, b):
        out = [0] * (k + 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if i + j > k:
                        break
                    out[i + j] += x * y
        return out

    P = []                                             # P[l](z) for a factor with l leading zeros
    for l in range(t + 1):
        p = [0] * (k + 1)
        p[0] = 1
        for j in range(1, l + 1):
            if j <= k:
                p[j] = q ** j - q ** (j - 1)
        if l < t and l + 1 <= k:
            p[l + 1] = -(q ** l)
        P.append(p)
    powers = [{0: [1] + [0] * k} for _ in range(t + 1)]

    def power(l, n):
        cache = powers[l]
        if n not in cache:
            half = power(l, n // 2)
            sq = polymul(half, half)
            cache[n] = polymul(sq, P[l]) if n % 2 else sq
        return cache[n]

    total = [0] * (k + 1)
    for prof, cnt in tally.items():
        poly = [1] + [0] * k
        for l, n in enumerate(prof):
            if n:
                poly = polymul(poly, power(l, n))
        for j in range(k + 1):
            total[j] += cnt * poly[j]
    size = q ** m
    assert total[0] == size and all(x % size == 0 and x >= 0 for x in total), "the dual weight counts are not integers"
    dual = [x // size for x in total]
    first = next((j for j in range(1, k + 1) if dual[j]), None)
    if first is not None:
        return False, f"{dual[first]} nonzero dual words of weight {first} (strength {first - 1})"
    return True, f"no nonzero dual word of weight 1..{k} ({len(tally)} leading-zero profiles over {size} words)"


def read_matrix(path, q, m):
    rows = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        toks = line.replace(",", " ").split()
        if len(toks) == 1 and q <= 9 and len(toks[0]) > 1 and toks[0].isdigit():
            toks = list(toks[0])
        if not all(x.isdigit() for x in toks):
            raise ValueError("an entry is not a non-negative integer")
        row = [int(x) for x in toks]
        if any(x >= q for x in row):
            raise ValueError(f"an entry is not below {q}")
        rows.append(row)
    if len(rows) != m:
        raise ValueError(f"{len(rows)} rows, expected {m}")
    if len({len(r) for r in rows}) != 1 or not rows[0]:
        raise ValueError("the rows do not all have the same positive length")
    return rows


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    way, max_work = None, 2 ** 33
    if "--way" in argv:
        i = argv.index("--way"); way = argv[i + 1]; del argv[i:i + 2]
    if "--max-work" in argv:
        i = argv.index("--max-work"); max_work = int(float(argv[i + 1])); del argv[i:i + 2]
    if len(argv) != 5 or way not in (None, "E", "D", "both"):
        print(__doc__)
        return 1
    try:
        q, m, k = int(argv[0]), int(argv[2]), int(argv[3])
        depth = None if argv[1] == "net" else int(argv[1])
        if q not in FIELDS or m < 1 or not 1 <= k <= m or (depth is not None and depth < 1):
            raise ValueError("need B in the list, M >= 1, 1 <= K <= M, T >= 1 or net")
        G = read_matrix(argv[4], q, m)
    except (ValueError, OSError) as err:
        print(f"malformed: {err}")
        return 1
    D = k if depth is None else depth
    if len(G[0]) % D:
        print(f"malformed: {len(G[0])} columns is not a multiple of the depth {D}")
        return 1
    s = len(G[0]) // D
    t = min(D, k)
    if s * t < k:
        print(f"malformed: {s} factors of depth {t} cannot carry strength {k}")
        return 1
    F = Field(q)
    cols = [[tuple(G[r][i * D + j] for r in range(m)) for j in range(t)] for i in range(s)]
    n = depth_vectors(s, t, k, max_work)
    work_d = n * k
    work_e = q ** m * s * t // max(1, q - 1)
    name = "net" if depth is None else f"depth {depth}"
    print(f"linear ordered orthogonal array over GF({q}), {name}: {q}^{m} runs, {s} factors, strength to check {k}")
    print(f"work: method D about {work_d:.3g} steps{' or more' if n > max_work else ''}, method E about {work_e:.3g} steps")
    if way is None:
        way = "D" if work_d <= work_e else "E"
    if (way in ("D", "both") and work_d > max_work) or (way in ("E", "both") and work_e > max_work):
        if way != "both" and min(work_d, work_e) <= max_work:
            way = "D" if work_d <= work_e else "E"
        else:
            print(f"too large to check here (more than {max_work:.3g} steps)")
            return 2
    verdicts = []
    if way in ("D", "both"):
        ok, msg, _ = way_d(F, cols, s, t, k)
        print(f"method D: {'strength at least ' + str(k) if ok else 'NOT strength ' + str(k)}: {msg}")
        verdicts.append(ok)
    if way in ("E", "both"):
        ok, msg = way_e(F, cols, m, s, t, k)
        print(f"method E: {'strength at least ' + str(k) if ok else 'NOT strength ' + str(k)}: {msg}")
        verdicts.append(ok)
    if len(set(verdicts)) != 1:
        print("the two methods disagree: no verdict")
        return 1
    if not verdicts[0]:
        return 1
    print(f"RESULT {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
