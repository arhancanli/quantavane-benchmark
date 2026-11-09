"""Exact check of a bilinear algorithm for matrix multiplication (standard library only).

  python3 -I matmul_check.py N M P FIELDS FILE

An algorithm of rank R for the product C = A B of an N x M matrix A by an M x P matrix B is a list of R terms
(U_r, V_r, W_r): U_r is N x M, V_r is M x P and W_r is N x P, and

    m_r = (sum_ij U_r[i][j] A[i][j]) * (sum_jk V_r[j][k] B[j][k]),     C[i][k] = sum_r W_r[i][k] m_r

for all matrices A and B over a field, with A and B not assumed to commute. Equivalently, for all indices,
sum_r U_r[i][j] V_r[j'][k] W_r[i'][k'] = 1 when i = i', j = j' and k = k', and 0 otherwise: the R terms decompose the
matrix multiplication tensor <N,M,P>. The checker computes these sums exactly over the field of the file.

FILE is JSON: {"field": F, "terms": [[U, V, W], ...]} with F one of "Q" (rational numbers), "Q(i)" (Gaussian
rationals) or "GF(p)" for a prime p. Matrices are lists of rows. An entry is an integer or a string "a/b"; over Q(i)
it may also be a pair [re, im] of such numbers; over GF(p) a fraction a/b means a times the inverse of b modulo p.
FIELDS is "any" (every field above is accepted) or "char0" (only Q and Q(i): a rank found over GF(2) alone, like
the rank-47 algorithm for 4 x 4 matrices of Fawzi et al. 2022, does not count there). Terms with a zero factor are
not counted. Prints the format, the field and "RESULT R", the number of terms; exits 0 for a correct algorithm, 1
otherwise. R is the score (smaller is better)."""
import json
import sys
from fractions import Fraction


def is_prime(p):
    if p < 2:
        return False
    d = 2
    while d * d <= p:
        if p % d == 0:
            return False
        d += 1
    return True


def rational(x):
    if isinstance(x, bool):
        raise ValueError("booleans are not numbers")
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str) and x.strip():
        return Fraction(x.strip())
    raise ValueError(f"not a rational number: {x!r}")


def make_field(name):
    """(parse, add, mul, zero, one, is_zero) for the field named in the file."""
    if name == "Q":
        return (rational, lambda a, b: a + b, lambda a, b: a * b, Fraction(0), Fraction(1), lambda a: a == 0)
    if name == "Q(i)":
        def parse(x):
            if isinstance(x, list):
                if len(x) != 2:
                    raise ValueError("a Gaussian rational is a pair [re, im]")
                return (rational(x[0]), rational(x[1]))
            return (rational(x), Fraction(0))
        return (parse, lambda a, b: (a[0] + b[0], a[1] + b[1]),
                lambda a, b: (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]),
                (Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)), lambda a: a[0] == 0 and a[1] == 0)
    if name.startswith("GF(") and name.endswith(")"):
        p = int(name[3:-1])
        if not is_prime(p):
            raise ValueError(f"{p} is not a prime")

        def parse(x):
            q = rational(x)
            if q.denominator % p == 0:
                raise ValueError(f"{x!r} has a denominator divisible by {p}")
            return q.numerator * pow(q.denominator, -1, p) % p
        return (parse, lambda a, b: (a + b) % p, lambda a, b: a * b % p, 0, 1, lambda a: a == 0)
    raise ValueError(f"unknown field {name!r}: use Q, Q(i) or GF(p)")


def main():
    if len(sys.argv) != 6:
        print(__doc__)
        return 2
    n, m, p = (int(x) for x in sys.argv[1:4])
    fields = sys.argv[4]
    if fields not in ("any", "char0"):
        print("FIELDS must be any or char0")
        return 2
    try:
        data = json.load(open(sys.argv[5], encoding="utf-8"))
        name = data["field"]
        parse, add, mul, zero, one, is_zero = make_field(name)
        if fields == "char0" and name not in ("Q", "Q(i)"):
            print(f"this problem asks for an algorithm over a field of characteristic 0 (Q or Q(i)), not {name}")
            return 1
        terms = []
        for t, term in enumerate(data["terms"]):
            if len(term) != 3:
                raise ValueError(f"term {t + 1} is not [U, V, W]")
            shapes = ((n, m), (m, p), (n, p))
            mats = []
            for mat, (r, c) in zip(term, shapes):
                if len(mat) != r or any(len(row) != c for row in mat):
                    raise ValueError(f"term {t + 1}: a factor is not {r} x {c}")
                mats.append([[parse(x) for x in row] for row in mat])
            terms.append(mats)
    except (ValueError, KeyError, TypeError, ZeroDivisionError, json.JSONDecodeError) as e:
        print(f"cannot read the algorithm: {e}")
        return 1
    total = {}
    rank = 0
    for U, V, W in terms:
        us = [((i, j), U[i][j]) for i in range(n) for j in range(m) if not is_zero(U[i][j])]
        vs = [((j, k), V[j][k]) for j in range(m) for k in range(p) if not is_zero(V[j][k])]
        ws = [((i, k), W[i][k]) for i in range(n) for k in range(p) if not is_zero(W[i][k])]
        if not (us and vs and ws):
            continue
        rank += 1
        for a, x in us:
            for b, y in vs:
                xy = mul(x, y)
                for c, z in ws:
                    key = (a, b, c)
                    total[key] = add(total.get(key, zero), mul(xy, z))
    for i in range(n):
        for j in range(m):
            for k in range(p):
                key = ((i, j), (j, k), (i, k))
                if total.pop(key, zero) != one:
                    print(f"the coefficient of A[{i}][{j}] B[{j}][{k}] in C[{i}][{k}] is not 1")
                    return 1
    for key, val in total.items():
        if not is_zero(val):
            (i, j), (j2, k), (i2, k2) = key
            print(f"A[{i}][{j}] B[{j2}][{k}] appears in C[{i2}][{k2}] with a nonzero coefficient")
            return 1
    print(f"<{n}x{m}x{p}> over {name}: a correct bilinear algorithm with {rank} multiplications")
    print(f"RESULT {rank}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
