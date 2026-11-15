"""Exact minimum distance of an additive (stabilizer) quantum code [[N,K]] over GF(Q), Q in {2, 3, 4, 5, 7, 8}
(standard library only; a C compiler makes large codes faster).

  python3 -I qcode_check.py Q N K FILE [--max-work W] [--python]

FILE is a stabilizer matrix: one generator per line, 2N elements of GF(Q), the N "X" entries then the N "Z" entries
(a '|' between the halves is allowed), as integers 0..Q-1 separated by spaces or commas, or as digits with no
separators (2N digits in all, for instance "0110|1001"). Blank lines and lines starting with '#' are ignored. For Q = 4 and 8 the integer a = a_0 + 2 a_1 + 4 a_2
stands for a_0 + a_1 x + a_2 x^2 modulo x^2 + x + 1 (Q = 4) or x^3 + x + 1 (Q = 8). Q = 2 is the qubit table of
codetables.de (its q = 4), Q = 3 the qutrit table (q = 9), Q = 4, 5, 7, 8 the tables with q = 16, 25, 49, 64.

The stabilizer S is the additive group the lines generate, that is their span over the prime field GF(p) of GF(Q)
(Q = p^m). For a code that is linear over GF(Q), give m generators per GF(Q)-generator g, for instance g and x g. The
checker
- finds the rank r of the lines over GF(p) (Gaussian elimination) and requires r = m (N - K), so that S has
  Q^(N-K) elements and the code has dimension Q^K;
- requires every two lines to be orthogonal in the trace-symplectic form Tr(sum_i a_i b'_i - a'_i b_i) (a = X part,
  b = Z part, Tr from GF(Q) to GF(p)), so that S is commutative;
- lists every element of S once (the C helper qcode_enum.c, or this program for small S), counting A_w, the elements
  of symplectic weight w (the coordinates where X or Z is nonzero);
- obtains B_w, the number of elements of weight w in the trace-symplectic dual S', by the MacWilliams identity
  B_j = (1/|S|) sum_i A_i K_j(i) with the Krawtchouk polynomials of an alphabet of size Q^2, in exact integers (each
  B_j is checked to be a non-negative integer);
- reports the minimum distance D: for K >= 1 the least w >= 1 with B_w > A_w (an element of S' outside S), for K = 0
  the least w >= 1 with A_w > 0 (then S' = S).
The work is about Q^(N-K) steps for Q = 2, 4, 8 and Q^(N-K) / (Q - 1) for Q = 3, 5, 7; above --max-work (default
2^34) the program stops with exit status 2.

Prints "distance D" and, as its last line, "RESULT D", and exits 0 for a valid code; exits 1 otherwise."""
import math
import os
import subprocess
import sys

FIELDS = {2: (2, 1, None), 3: (3, 1, None), 5: (5, 1, None), 7: (7, 1, None),
          4: (2, 2, (1, 1, 1)), 8: (2, 3, (1, 1, 0, 1))}
HERE = os.path.dirname(os.path.abspath(__file__))


class Field:
    def __init__(self, q):
        self.q = q
        p, e, mod = FIELDS[q]
        self.p, self.e = p, e
        dig = [[(a // p ** i) % p for i in range(e)] for a in range(q)]
        self.dig = dig

        def number(ds):
            return sum(d * p ** i for i, d in enumerate(ds))

        def mul(a, b):
            if e == 1:
                return a * b % p
            prod = [0] * (2 * e - 1)
            for i, x in enumerate(dig[a]):
                for j, y in enumerate(dig[b]):
                    prod[i + j] = (prod[i + j] + x * y) % p
            for i in range(2 * e - 2, e - 1, -1):
                c = prod[i]
                if c:
                    prod[i] = 0
                    for j in range(e):
                        prod[i - e + j] = (prod[i - e + j] - c * mod[j]) % p
            return number(prod[:e])

        self.mul = [[mul(a, b) for b in range(q)] for a in range(q)]
        self.add = [[number([(x + y) % p for x, y in zip(dig[a], dig[b])]) for b in range(q)] for a in range(q)]
        self.neg = [number([(-x) % p for x in dig[a]]) for a in range(q)]
        if e > 1:                                   # x must have order q - 1 (so the modulus is irreducible)
            y, seen = 1, set()
            for _ in range(q - 1):
                y = self.mul[y][p]
                seen.add(y)
            assert len(seen) == q - 1, "x is not primitive"

        def trace(a):                               # a + a^p + ... + a^(p^(e-1)), an element of GF(p)
            t, y = 0, a
            for _ in range(e):
                t = self.add[t][y]
                z = 1
                for _ in range(p):
                    z = self.mul[z][y]
                y = z
            assert t < p, "the trace is not in the prime field"
            return t

        self.trace = [trace(a) for a in range(q)]


def read_rows(path, q, n):
    rows = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        toks = line.replace("|", " ").replace(",", " ").split()
        if (len(toks) != 2 * n and all(t.isdigit() for t in toks) and sum(len(t) for t in toks) == 2 * n):
            toks = list("".join(toks))              # digit strings without separators, e.g. "0110|1001"
        if not all(x.isdigit() for x in toks):
            raise ValueError("an entry is not a non-negative integer")
        row = [int(x) for x in toks]
        if len(row) != 2 * n:
            raise ValueError(f"a line has {len(row)} entries, expected 2N = {2 * n}")
        if any(x >= q for x in row):
            raise ValueError(f"an entry is not below {q}")
        rows.append(row)
    if not rows:
        raise ValueError("no generators")
    return rows


def prime_basis(F, rows, n):
    """Rows as vectors over GF(p) (coordinate i: the m digits of X_i, then the m digits of Z_i); a basis of their
    span, in echelon form, by Gaussian elimination."""
    p, m = F.p, F.e
    vecs = []
    for row in rows:
        v = []
        for i in range(n):
            v.extend(F.dig[row[i]])
            v.extend(F.dig[row[n + i]])
        vecs.append(v)
    basis, pivots = [], []
    for v in vecs:
        v = v[:]
        for b, pc in zip(basis, pivots):
            c = v[pc]
            if c:
                v = [(x - c * y) % p for x, y in zip(v, b)]
        piv = next((i for i, x in enumerate(v) if x), None)
        if piv is None:
            continue
        inv = pow(v[piv], p - 2, p)
        v = [x * inv % p for x in v]
        for idx, b in enumerate(basis):            # keep the basis reduced
            c = b[piv]
            if c:
                basis[idx] = [(x - c * y) % p for x, y in zip(b, v)]
        basis.append(v)
        pivots.append(piv)
    return basis


def weights_python(p, n, D, basis):
    """A_w for the span of the basis (GF(p) vectors of n groups of D digits), by listing every element."""
    r = len(basis)
    A = [0] * (n + 1)
    A[0] = 1
    if p == 2:
        ints = [[sum(1 << i for i in range(n) if b[i * D + d]) for d in range(D)] for b in basis]
        cur = [0] * D
        for s in range(1, 1 << r):
            j = (s & -s).bit_length() - 1
            cur = [c ^ g for c, g in zip(cur, ints[j])]
            o = 0
            for c in cur:
                o |= c
            A[bin(o).count("1")] += 1
        return A
    for lead in range(r):                            # lines through the origin: first nonzero coefficient 1
        cur = basis[lead][:]
        dig = [0] * r
        while True:
            w = sum(1 for i in range(n) if any(cur[i * D:(i + 1) * D]))
            A[w] += p - 1
            j = lead + 1
            while j < r:
                cur = [(x + y) % p for x, y in zip(cur, basis[j])]
                dig[j] += 1
                if dig[j] < p:
                    break
                dig[j] = 0
                j += 1
            if j == r:
                break
    return A


def weights_native(p, n, D, basis):
    exe = os.path.join(HERE, "bin", "qcode_enum")
    src = os.path.join(HERE, "qcode_enum.c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    text = f"{p} {n} {D} {len(basis)}\n" + "".join(" ".join(map(str, b)) + "\n" for b in basis)
    out = subprocess.run([exe], input=text, capture_output=True, text=True, check=True).stdout
    A = [0] * (n + 1)
    for line in out.splitlines():
        if line.startswith("A "):
            _, w, c = line.split()
            A[int(w)] = int(c)
    return A


def krawtchouk(j, i, n, a):
    """K_j(i) for an alphabet of size a: sum_s (-1)^s (a-1)^(j-s) C(i,s) C(n-i,j-s)."""
    return sum((-1) ** s * (a - 1) ** (j - s) * math.comb(i, s) * math.comb(n - i, j - s) for s in range(0, j + 1))


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    max_work, force_python = 2 ** 34, False
    if "--max-work" in argv:
        i = argv.index("--max-work"); max_work = int(float(argv[i + 1])); del argv[i:i + 2]
    if "--python" in argv:
        argv.remove("--python"); force_python = True
    if len(argv) != 4:
        print(__doc__)
        return 1
    try:
        q, n, k = int(argv[0]), int(argv[1]), int(argv[2])
        if q not in FIELDS or n < 1 or not 0 <= k <= n:
            raise ValueError("need Q in 2, 3, 4, 5, 7, 8, N >= 1 and 0 <= K <= N")
        rows = read_rows(argv[3], q, n)
    except (ValueError, OSError) as err:
        print(f"malformed: {err}")
        return 1
    F = Field(q)
    p, m = F.p, F.e
    # commutativity: every two generators orthogonal in the trace-symplectic form
    for a in range(len(rows)):
        for b in range(a + 1, len(rows)):
            s = 0
            ra, rb = rows[a], rows[b]
            for i in range(n):
                s = F.add[s][F.mul[ra[i]][rb[n + i]]]
                s = F.add[s][F.neg[F.mul[rb[i]][ra[n + i]]]]
            if F.trace[s]:
                print(f"not a stabilizer: generators {a + 1} and {b + 1} do not commute (trace-symplectic product {F.trace[s]})")
                return 1
    basis = prime_basis(F, rows, n)
    r = len(basis)
    if r != m * (n - k):
        print(f"wrong size: the generators span a group of {p}^{r} elements; [[{n},{k}]] over GF({q}) needs "
              f"{p}^{m * (n - k)} (rank {m * (n - k)} over GF({p}))")
        return 1
    work = (p ** r) if p == 2 else (p ** r - 1) // (p - 1)
    print(f"stabilizer code [[{n},{k}]] over GF({q}): {r} independent generators over GF({p}), all commuting; "
          f"{work} elements of S to list")
    if work > max_work:
        print(f"too large to check here (more than {max_work:.3g} steps)")
        return 2
    D = 2 * m
    if force_python or work <= 2 ** 16:
        A = weights_python(p, n, D, basis)
    else:
        A = weights_native(p, n, D, basis)
    size = p ** r
    if sum(A) != size:
        print("internal error: the weight counts do not add up to |S|")
        return 1
    alph = q * q
    if k == 0:
        d = next((w for w in range(1, n + 1) if A[w]), None)
        if d is None:
            print("internal error: no nonzero element")
            return 1
        print("weights of S (nonzero, up to D): " + ", ".join(f"{w}:{A[w]}" for w in range(1, d + 1) if A[w]))
    else:
        d = None
        B_seen = []
        for j in range(0, n + 1):
            tot = sum(A[i] * krawtchouk(j, i, n, alph) for i in range(n + 1) if A[i])
            if tot % size or tot < 0:
                print(f"internal error: B_{j} = {tot}/{size} is not a non-negative integer")
                return 1
            B = tot // size
            if j == 0 and B != 1:
                print("internal error: B_0 is not 1")
                return 1
            if j >= 1 and B < A[j]:
                print(f"internal error: B_{j} = {B} < A_{j} = {A[j]}")
                return 1
            B_seen.append(B)
            if j >= 1 and B > A[j]:
                d = j
                break
        if d is None:
            print("internal error: S' has no element outside S")
            return 1
        print("weights up to D, (A_w in S, B_w in S'): " +
              ", ".join(f"{w}:({A[w]},{B_seen[w]})" for w in range(1, d + 1) if A[w] or B_seen[w]))
    print(f"distance {d}")
    print(f"RESULT {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
