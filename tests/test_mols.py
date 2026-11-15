"""Tests of checkers/mols_check.py and its C helper mols_scan.c (mutually orthogonal Latin squares; standard library
only and a C compiler; run by test.sh).

- Complete sets: for a prime p the p - 1 squares L_a(i, j) = a i + j mod p are mutually orthogonal; their Kronecker
  products give MacNeish's sets (min(p, q) - 1 squares of order pq). Both routes certify them.
- 150 random sets (rows, columns and symbols of the squares a i + j mod n permuted at random; sometimes a square
  copied, two cells swapped, a symbol out of range, a row missing or a header that disagrees): the Python route and
  the C helper give the same verdict and the same count.
- Red controls: a square repeated (not orthogonal), two cells of a row swapped (not Latin), the header "N K" with a
  wrong K or N.
- The published sets of C. D. Rosin (arXiv:2611.16299, github.com/Constructive-Codes/MOLS, fetched by fetch.sh into
  certs/mols/) pass by both routes with the published sizes.

  python3 -I tests/test_mols.py"""
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "mols_check.py")
TMP = tempfile.mkdtemp(prefix="mols_test_")
failures = []


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def write(squares, header=None):
    path = os.path.join(TMP, "m.txt")
    with open(path, "w") as f:
        if header:
            f.write(header + "\n")
        for t, sq in enumerate(squares):
            f.write(f"# square {t}\n" + "".join(" ".join(map(str, r)) + "\n" for r in sq))
    return path


def run(n, path, *flags):
    r = subprocess.run([sys.executable, "-I", CHECK, str(n), path] + list(flags), capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    return last if r.returncode == 0 else "refused"


def complete(p):
    return [[[(a * i + j) % p for j in range(p)] for i in range(p)] for a in range(1, p)]


def kron(A, B):
    m, n = len(A[0]), len(B[0])
    return [[[A[t][i // n][j // n] * n + B[t][i % n][j % n] for j in range(m * n)] for i in range(m * n)]
            for t in range(min(len(A), len(B)))]


for p in (3, 5, 7, 11, 13):
    for flag in ("--python", "--native"):
        expect(f"the {p - 1} squares a i + j mod {p} {flag}", run(p, write(complete(p)), flag), f"RESULT {p - 1}")
for p, q in ((3, 5), (5, 7), (7, 11), (3, 13)):
    S = kron(complete(p), complete(q))
    for flag in ("--python", "--native"):
        expect(f"MacNeish: {len(S)} squares of order {p * q} {flag}", run(p * q, write(S), flag), f"RESULT {len(S)}")
S = complete(7)
for flag in ("--python", "--native"):
    expect(f"red a square repeated {flag}", run(7, write(S + [S[0]]), flag), "refused")
    T = [[r[:] for r in sq] for sq in S]
    T[1][2][0], T[1][2][1] = T[1][2][1], T[1][2][0]
    expect(f"red two cells of a row swapped {flag}", run(7, write(T), flag), "refused")
    expect(f"red header with a wrong count {flag}", run(7, write(S, "7 5"), flag), "refused")
    expect(f"red header with a wrong order {flag}", run(7, write(S, "8 6"), flag), "refused")
    expect(f"header '7 6' {flag}", run(7, write(S, "7 6"), flag), "RESULT 6")
    expect(f"symbols 1..7 {flag}", run(7, write([[[x + 1 for x in r] for r in sq] for sq in S]), flag), "RESULT 6")

rng = random.Random(2026)
same = 0
for trial in range(150):
    n = rng.choice([5, 7, 9, 11, 13, 15, 21, 25])
    k = rng.randrange(1, 5)
    rp, cp, sp = (rng.sample(range(n), n) for _ in range(3))
    sq = []
    for _ in range(k):
        a = rng.randrange(1, n)
        sq.append([[sp[(a * rp[i] + cp[j]) % n] for j in range(n)] for i in range(n)])
    kind = rng.randrange(6)
    header = None
    if kind == 1 and k > 1:
        sq[-1] = [r[:] for r in sq[0]]
    elif kind == 2:
        i = rng.randrange(n)
        sq[0][i][0], sq[0][i][1] = sq[0][i][1], sq[0][i][0]
    elif kind == 3:
        sq[0][0][0] = n + 1
    elif kind == 4:
        sq[-1] = sq[-1][:-1]
    elif kind == 5:
        header = f"{n} {k + rng.choice([0, 1])}"
    path = write(sq, header)
    same += run(n, path, "--python") == run(n, path, "--native")
expect("150 random sets: the Python route and the C helper agree", same, 150)

certs = os.path.join(ROOT, "certs", "mols")
for name in sorted(os.listdir(certs)) if os.path.isdir(certs) else []:
    if name.endswith(".txt") and name.startswith("mols_"):
        n, k = int(name[5:8]), int(name[9:11])
        for flag in ("--python", "--native") if n < 100 else ("--native",):
            expect(f"Rosin's {k} MOLS of order {n} {flag}", run(n, os.path.join(certs, name), flag), f"RESULT {k}")
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
