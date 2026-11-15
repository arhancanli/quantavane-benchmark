"""Tests of checkers/oa_check.py and its C helper oa_scan.c (standard library only; run by test.sh).

- Linear objects written out run by run: oa_check.py (both ways) gives the verdict of ooa_check.py on the generator
  matrix, on random objects over GF(2) to GF(9), depths 1, 2, 3 and net.
- A Latin square of order 6 is an OA(36; 2, 3, 6) and passes; with one symbol changed, or one run dropped, it fails.
- Red controls: a symbol out of range, a run count that is not B^M.

  python3 -I tests/test_oa.py"""
import itertools
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "checkers"))
import ooa_check as oc  # noqa: E402

CHECK = os.path.join(ROOT, "checkers", "oa_check.py")
TMP = tempfile.mkdtemp(prefix="oa_test_")
failures = []


def run(args, rows, *flags):
    path = os.path.join(TMP, "a.txt")
    with open(path, "w") as f:
        f.write("\n".join(" ".join(map(str, r)) for r in rows) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK] + [str(a) for a in args] + [path] + list(flags),
                       capture_output=True, text=True)
    return r.returncode


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


rng = random.Random(20261115)
agree = total = 0
for trial in range(160):
    q = rng.choice([2, 2, 3, 4, 5, 7, 8, 9])
    F = oc.Field(q)
    m = rng.randint(2, 4 if q <= 3 else 3)
    k = rng.randint(1, m)
    T = rng.choice([1, 2, 3, "net"])
    D = k if T == "net" else T
    t = min(D, k)
    s = rng.randint(-(-k // t), -(-k // t) + 3)
    if q ** m * s * D > 20000:
        continue
    G = [[rng.randrange(q) for _ in range(s * D)] for _ in range(m)]
    if rng.random() < 0.5:
        for r in range(m):
            for c in range(min(m, s * D)):
                G[r][c] = 1 if r == c else 0
    runs = []
    for x in itertools.product(range(q), repeat=m):
        w = [0] * (s * D)
        for c, row in zip(x, G):
            if c:
                w = [F.add[a][F.mul[c][b]] for a, b in zip(w, row)]
        runs.append(w)
    gpath = os.path.join(TMP, "g.txt")
    with open(gpath, "w") as f:
        f.write("\n".join(" ".join(map(str, r)) for r in G) + "\n")
    lin = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "checkers", "ooa_check.py"), str(q), str(T), str(m),
                          str(k), gpath], capture_output=True, text=True).returncode
    a = run([q, T, m, k], runs, "--python")
    b = run([q, T, m, k], runs, "--native")
    total += 1
    agree += a == b == lin
expect(f"{total} linear objects run by run: oa_check.py (Python, C) and ooa_check.py agree", agree, total)
L = [[(i + j) % 6 for j in range(6)] for i in range(6)]
oa = [[i, j, L[i][j]] for i in range(6) for j in range(6)]
for flag in ("--python", "--native"):
    expect(f"Latin square of order 6 as OA(36; 2, 3, 6) {flag}", run([6, 1, 2, 2], oa, flag), 0)
    bad = [r[:] for r in oa]
    bad[7][2] = (bad[7][2] + 1) % 6
    expect(f"red: one symbol changed {flag}", run([6, 1, 2, 2], bad, flag), 1)
expect("red: a run dropped (35 runs, not 6^2)", run([6, 1, 2, 2], oa[1:]), 1)
expect("red: a symbol out of range", run([6, 1, 2, 2], oa[:-1] + [[5, 5, 6]]), 1)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
