"""Exact check of a packing of subspaces in a real Grassmannian (standard library only).

  python3 -I grass_check.py M N COUNT FILE

FILE holds COUNT subspaces of dimension N in R^M, each given by N spanning vectors of M coordinates: COUNT x N x M
numbers in all, separated by white space (or commas), subspace after subspace and vector after vector, as in N. J. A.
Sloane's files (neilsloane.com/grass/, for instance grassc.4.2.8.txt). A number is an integer, a decimal (optionally
with an exponent, as in .19124869568340759E+01) or a fraction p/q; each is read exactly. Lines starting with '#' are
ignored. The vectors need not be orthonormal: only the subspace they span counts.

The squared chordal distance between two N-spaces is the sum of the squares of the sines of their N principal angles
(Conway, Hardin and Sloane, 1996): with the projections P_A and P_B, D(A, B) = N - tr(P_A P_B). Every vector is scaled
to integers (a scaling does not change the subspace); with the integer N x M matrices A and B,
P_A = A^T G_A^(-1) A for the Gram matrix G_A = A A^T, so D(A, B) = N - tr(adj(G_A) X adj(G_B) X^T) / (det G_A det G_B)
with X = A B^T: an exact rational number from integers only. Each subspace must have dimension N (det G_A > 0).

Prints the least squared chordal distance over all pairs, as a decimal and, as its last line, "RESULT p/q" (exact),
and exits 0 for a valid packing; exits 1 otherwise. The value is to be maximized."""
import math
import re
import sys
from fractions import Fraction

NUM = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eEdD][+-]?\d+)?$")


def number(tok):
    if "/" in tok:
        p, _, q = tok.partition("/")
        if not (re.fullmatch(r"[+-]?\d+", p) and re.fullmatch(r"\d+", q)) or int(q) == 0:
            raise ValueError(tok)
        return Fraction(int(p), int(q))
    if not NUM.match(tok):
        raise ValueError(tok)
    return Fraction(tok.replace("D", "E").replace("d", "e"))


def det_adj(G):
    """(det G, adj G) of a small integer matrix, by cofactors (N <= 3) or fraction-free elimination."""
    n = len(G)
    if n == 1:
        return G[0][0], [[1]]
    if n == 2:
        (a, b), (c, d) = G
        return a * d - b * c, [[d, -b], [-c, a]]
    if n == 3:
        (a, b, c), (d, e, f), (g, h, i) = G
        A = [[e * i - f * h, c * h - b * i, b * f - c * e],
             [f * g - d * i, a * i - c * g, c * d - a * f],
             [d * h - e * g, b * g - a * h, a * e - b * d]]
        return a * A[0][0] + b * A[1][0] + c * A[2][0], A
    # general N: det and inverse by Fractions, adj = det * inverse
    M = [[Fraction(x) for x in row] + [Fraction(int(r == c)) for c in range(n)] for r, row in enumerate(G)]
    det = Fraction(1)
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col]), None)
        if piv is None:
            return 0, None
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            det = -det
        pv = M[col][col]
        det *= pv
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    d = int(det)
    return d, [[int(x * det) for x in row[n:]] for row in M]


def read_packing(path, m, n, count):
    toks = []
    for line in open(path):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        toks.extend(s.replace(",", " ").split())
    if len(toks) != count * n * m:
        raise ValueError(f"{len(toks)} numbers, expected COUNT x N x M = {count * n * m}")
    vals = [number(t) for t in toks]
    subs = []
    for s in range(count):
        vecs = []
        for j in range(n):
            v = vals[(s * n + j) * m:(s * n + j + 1) * m]
            den = 1
            for x in v:
                den = den * x.denominator // math.gcd(den, x.denominator)
            vecs.append([int(x * den) for x in v])
        subs.append(vecs)
    return subs


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 4:
        print(__doc__)
        return 1
    try:
        m, n, count = (int(x) for x in argv[:3])
        if not (1 <= n < m and count >= 2):
            raise ValueError("need 1 <= N < M and COUNT >= 2")
        subs = read_packing(argv[3], m, n, count)
    except (ValueError, OSError, ZeroDivisionError) as err:
        print(f"malformed: {err}")
        return 1
    pre = []
    for s, A in enumerate(subs):
        G = [[sum(x * y for x, y in zip(a, b)) for b in A] for a in A]
        det, adj = det_adj(G)
        if det <= 0:
            print(f"subspace {s + 1}: its {n} vectors are dependent (they span less than dimension {n})")
            return 1
        pre.append((A, det, adj))
    best_num, best_den, best_pair = None, None, None
    for i in range(count):
        A, dA, adjA = pre[i]
        for j in range(i + 1, count):
            B, dB, adjB = pre[j]
            X = [[sum(x * y for x, y in zip(a, b)) for b in B] for a in A]
            if n == 1:
                num, den = dA * dB - X[0][0] * X[0][0], dA * dB      # 1 - (a.b)^2 / (|a|^2 |b|^2)
            else:
                Y = [[sum(adjA[r][t] * X[t][c] for t in range(n)) for c in range(n)] for r in range(n)]
                Z = [[sum(Y[r][t] * adjB[t][c] for t in range(n)) for c in range(n)] for r in range(n)]
                tr = sum(Z[r][c] * X[r][c] for r in range(n) for c in range(n))
                num, den = n * dA * dB - tr, dA * dB
            if best_num is None or num * best_den < best_num * den:
                best_num, best_den, best_pair = num, den, (i, j)
    value = Fraction(best_num, best_den)
    if value < 0:
        print("internal error: a negative squared distance")
        return 1
    i, j = best_pair
    dec = value.numerator * 10 ** 18 // value.denominator
    print(f"{count} subspaces of dimension {n} in R^{m}; the closest pair is {i + 1} and {j + 1}")
    print(f"least squared chordal distance {dec // 10 ** 18}.{dec % 10 ** 18:018d} (rounded down)")
    print(f"RESULT {value.numerator}/{value.denominator}" if value.denominator != 1 else f"RESULT {value.numerator}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
