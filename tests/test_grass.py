"""Tests of checkers/grass_check.py (standard library only; run by test.sh): exact values of known packings (the four
diagonals of the cube, 8/9 = Rankin's simplex bound; orthogonal coordinate planes and planes at 45 degrees), the
same value for another basis or a scaling of each subspace, the exact rational result against a floating-point
computation of the principal angles on random packings (n = 1 to 4, which takes the general elimination path),
Sloane's number formats, and red controls: a repeated subspace (distance 0), dependent vectors, a number too few or
too many, a malformed number.

  python3 -I tests/test_grass.py"""
import math
import os
import random
import subprocess
import sys
import tempfile
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "grass_check.py")
TMP = tempfile.mkdtemp(prefix="grass_test_")
failures = []


def run(m, n, count, subs, raw=None):
    path = os.path.join(TMP, "p.txt")
    with open(path, "w") as f:
        if raw is not None:
            f.write(raw)
        else:
            for s in subs:
                for v in s:
                    f.write(" ".join(str(x) for x in v) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, str(m), str(n), str(count), path], capture_output=True, text=True)
    val = None
    for line in r.stdout.splitlines():
        if line.startswith("RESULT "):
            val = Fraction(line.split()[1])
    return r.returncode, val


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def float_D(A, B):
    """n - tr(P_A P_B) in floating point, from orthonormalized bases (Gram-Schmidt)."""
    def ortho(V):
        out = []
        for v in V:
            w = [float(x) for x in v]
            for u in out:
                d = sum(a * b for a, b in zip(w, u))
                w = [a - d * b for a, b in zip(w, u)]
            nrm = math.sqrt(sum(a * a for a in w))
            out.append([a / nrm for a in w])
        return out
    QA, QB = ortho(A), ortho(B)
    return len(A) - sum(sum(a * b for a, b in zip(u, w)) ** 2 for u in QA for w in QB)


# the four diagonals of the cube: |cos| = 1/3, D = 8/9 (Rankin's simplex bound for 4 lines in R^3)
cube = [[[1, 1, 1]], [[1, -1, -1]], [[-1, 1, -1]], [[-1, -1, 1]]]
expect("4 cube diagonals in R^3: 8/9", run(3, 1, 4, cube), (0, Fraction(8, 9)))
expect("same, each vector scaled (3, -1/2, 0.25, 7)", run(3, 1, 4, [[[3, 3, 3]], [["-1/2", "1/2", "1/2"]],
                                                                    [["-0.25", "0.25", "-0.25"]], [[-7, -7, 7]]]),
       (0, Fraction(8, 9)))
# planes in R^4: span(e1,e2), span(e3,e4) at distance 2; span(e1+e3, e2+e4) at 45 degrees to both: distance 1
planes = [[[1, 0, 0, 0], [0, 1, 0, 0]], [[0, 0, 1, 0], [0, 0, 0, 1]], [[1, 0, 1, 0], [0, 1, 0, 1]]]
expect("three planes in R^4: 1", run(4, 2, 3, planes), (0, Fraction(1)))
expect("same planes, other bases (sums and multiples of the vectors)",
       run(4, 2, 3, [[[1, 1, 0, 0], [2, -1, 0, 0]], [[0, 0, 5, 0], [0, 0, 1, 1]], [[1, 1, 1, 1], [1, -1, 1, -1]]]),
       (0, Fraction(1)))
expect("only the first two planes: 2", run(4, 2, 2, planes[:2]), (0, Fraction(2)))
# Sloane's formats: Fortran exponents, leading points, commas, comments
raw = "# comment\n.10000000000000000E+01, 0\n0 .2E1\n1.0 1.0\n"
expect("formats: E exponents, leading point, commas, comment (three lines in R^2: 1/2)", run(2, 1, 3, None, raw),
       (0, Fraction(1, 2)))
# random rational packings against floating point (n = 4 takes the general elimination path)
rng = random.Random(20261116)
agree = total = 0
for trial in range(60):
    n = rng.randint(1, 4)
    m = rng.randint(n + 1, n + 5)
    count = rng.randint(2, 7)
    subs = [[[Fraction(rng.randint(-99, 99), rng.randint(1, 9)) for _ in range(m)] for _ in range(n)]
            for _ in range(count)]
    code, val = run(m, n, count, subs)
    want = min(float_D(subs[i], subs[j]) for i in range(count) for j in range(i + 1, count))
    total += 1
    agree += code == 0 and abs(float(val) - want) < 1e-9
expect(f"{total} random rational packings (n = 1 to 4): exact result = floating-point principal angles", agree, total)
# red controls
expect("red: a subspace repeated (distance 0)", run(3, 1, 5, cube + [cube[0]]), (0, Fraction(0)))
expect("red: a plane given by two dependent vectors", run(4, 2, 2, [planes[0], [[1, 2, 0, 0], [2, 4, 0, 0]]])[0], 1)
expect("red: a number too few", run(3, 1, 4, None, "1 1 1\n1 -1 -1\n-1 1 -1\n-1 -1\n")[0], 1)
expect("red: a number too many", run(3, 1, 4, None, "1 1 1\n1 -1 -1\n-1 1 -1\n-1 -1 1 1\n")[0], 1)
expect("red: a malformed number", run(3, 1, 4, None, "1 1 1\n1 -1 -1\n-1 1 -1\n-1 -1 1x\n")[0], 1)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
