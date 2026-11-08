"""Exact check of a kissing configuration (standard library only).

  python3 -I kissing_check.py D FILE

FILE holds one vector per line, integer coordinates separated by whitespace or commas (the vector format of Leaps in
Bounds, without symmetries). All vectors must have the same squared norm N > 0 and every inner product between two
of them must be at most N/2: normalised, they are unit vectors at angles of at least 60 degrees, so unit spheres
centred at twice them touch the unit sphere at the origin without overlapping. The vectors may have more than D
coordinates when they span a space of dimension at most D, which the checker decides by exact integer elimination.
k such vectors show that the kissing number in dimension D is at least k.

All inner products are computed exactly with big-integer arithmetic: the vectors of a block are packed, reversed,
into one integer in base 2^b (b large enough that no coefficient of the product carries), and one multiplication by
the packed form of a vector x gives the inner products of x with the whole block, read off as base-2^b digits. Prints
the count, the norm and the largest inner product, then "RESULT k"; exits 0 for a valid configuration, 1 otherwise."""
import math
import sys
from array import array

BLOCK = 1024


def rank_at_most(vecs, d):
    """True if the vectors span a space of dimension at most d (exact fraction-free elimination)."""
    basis = []                                   # (pivot column, integer row), each zero at earlier pivots
    for v in vecs:
        w = list(v)
        for c, b in basis:
            if w[c]:
                f, g = b[c], w[c]
                w = [x * f - y * g for x, y in zip(w, b)]
        if any(w):
            g = 0
            for x in w:
                g = math.gcd(g, x)
            w = [x // g for x in w]
            basis.append((next(i for i, x in enumerate(w) if x), w))
            if len(basis) > d:
                return False
    return True


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    d = int(sys.argv[1])
    vecs = []
    for line in open(sys.argv[2], encoding="ascii", errors="replace"):
        s = line.split("#")[0].replace(",", " ").split()
        if s:
            try:
                vecs.append([int(x) for x in s])
            except ValueError:
                print(f"not a vector of integers: {line.strip()[:60]!r}")
                return 1
    if not vecs:
        print("no vectors")
        return 1
    m = len(vecs[0])
    if any(len(v) != m for v in vecs):
        print("the vectors do not all have the same number of coordinates")
        return 1
    norm = sum(x * x for x in vecs[0])
    for i, v in enumerate(vecs):
        if sum(x * x for x in v) != norm:
            print(f"vector {i + 1} has squared norm {sum(x * x for x in v)}, not {norm}")
            return 1
    if norm == 0:
        print("the zero vector is not allowed")
        return 1
    if m > d and not rank_at_most(vecs, d):
        print(f"the vectors span a space of dimension more than {d}")
        return 1
    k = len(vecs)
    top = max(abs(x) for v in vecs for x in v)
    bound = m * top * top                        # no coefficient of a product exceeds this in absolute value
    for b, code in ((16, "H"), (32, "I" if array("I").itemsize == 4 else "L"), (64, "Q")):
        if bound < (1 << (b - 1)):
            break
    else:
        print("coordinates too large for this checker")
        return 1
    base, half, step = 1 << b, 1 << (b - 1), 2 * m - 1
    limit = half + norm // 2                     # a digit above this is an inner product above N/2

    def pack(rows):
        """Sum over t of (row t reversed) * base^(t*step), as an integer."""
        pos, neg = array(code, bytes(array(code).itemsize * len(rows) * step)), None
        neg = array(code, bytes(array(code).itemsize * len(rows) * step))
        for t, row in enumerate(rows):
            at = t * step + m - 1
            for i, x in enumerate(row):
                if x > 0:
                    pos[at - i] = x
                elif x < 0:
                    neg[at - i] = -x
        if sys.byteorder == "big":
            pos.byteswap()
            neg.byteswap()
        return int.from_bytes(pos.tobytes(), "little") - int.from_bytes(neg.tobytes(), "little")

    blocks = [pack(vecs[s:s + BLOCK]) for s in range(0, k, BLOCK)]
    offsets = {}
    worst, worst_pair = None, None
    for i, x in enumerate(vecs):
        xv = 0
        for c in reversed(x):
            xv = xv * base + c
        for bi in range(i // BLOCK, len(blocks)):
            cnt = min(BLOCK, k - bi * BLOCK)
            if cnt not in offsets:
                offsets[cnt] = half * ((base ** (cnt * step) - 1) // (base - 1))
            prod = xv * blocks[bi] + offsets[cnt]
            digits = array(code)
            digits.frombytes(prod.to_bytes(cnt * step * b // 8, "little"))
            if sys.byteorder == "big":
                digits.byteswap()
            ips = digits[m - 1::step]
            first = 0
            if bi == i // BLOCK:                 # the diagonal block: only partners after i
                first = i - bi * BLOCK + 1
                ips = ips[first:]
            if not ips:
                continue
            hi = max(ips)
            if worst is None or hi > worst:
                worst, worst_pair = hi, (i, bi * BLOCK + first + ips.index(hi))
            if hi > limit:
                a, c = worst_pair
                print(f"vectors {a + 1} and {c + 1} have inner product {hi - half} > {norm}/2")
                return 1
    largest = "none (one vector)" if worst is None else f"{worst - half}"
    print(f"vectors {k} coordinates {m} dimension <= {d} squared norm {norm} largest inner product {largest} "
          f"<= {norm}/2")
    print(f"RESULT {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
