"""Tests of checkers/circulant_check.py (circulant graphs for the degree-diameter problem) with its C helper
circulant_bfs.c, and of degdiam_check.py --bipartite (standard library only; run by test.sh).

C_n(1, 2k+1) with n = 2k^2 + 2k + 1 has degree 4 and diameter k (the optimal circulants of degree 4): it passes with
diameter k and is refused with diameter k - 1, in Python and in C (k = 1000 has 2,002,001 vertices and goes to C by
itself); the Python and C searches agree on 150 random circulant graphs; repeated jumps and too large degrees are
refused. Even cycles pass the bipartite check and odd cycles fail it.

  python3 -I tests/test_circulant.py"""
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "circulant_check.py")
DD = os.path.join(ROOT, "checkers", "degdiam_check.py")
TMP = tempfile.mkdtemp(prefix="circ_test_")
failures = []


def run(delta, diam, n, jumps, *flags):
    path = os.path.join(TMP, "c.txt")
    with open(path, "w") as f:
        f.write(f"{n}\n" + " ".join(map(str, jumps)) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, str(delta), str(diam), path] + list(flags), capture_output=True,
                       text=True)
    return r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


for k in (2, 5, 30):
    n = 2 * k * k + 2 * k + 1
    for flag in ("--python", "--native"):
        expect(f"C_{n}(1,{2 * k + 1}), diameter {k} {flag}", run(4, k, n, [1, 2 * k + 1], flag), (0, f"RESULT {n}"))
        expect(f"red: the same with diameter {k - 1} {flag}", run(4, k - 1, n, [1, 2 * k + 1], flag)[0], 1)
k = 1000
n = 2 * k * k + 2 * k + 1
code, line = run(4, k, n, [1, 2 * k + 1])
expect(f"C_{n}(1,{2 * k + 1}), diameter {k}, in C by default", (code, line), (0, f"RESULT {n}"))
expect(f"red: the same with diameter {k - 1}", run(4, k - 1, n, [1, 2 * k + 1])[0], 1)
expect("red: a jump repeated as its negative", run(6, 3, 50, [1, 49, 7])[0], 1)
expect("red: degree 6 > 4", run(4, 10, 50, [1, 7, 11])[0], 1)
expect("C_21(1,2,8): degree 6, diameter 2", run(6, 2, 21, [1, 2, 8])[0], 0)
expect("red: C_22(1,2,8), diameter 2", run(6, 2, 22, [1, 2, 8])[0], 1)
expect("red: C_20(2,4,6), disconnected", run(6, 10, 20, [2, 4, 6])[0], 1)
rng = random.Random(20261115)
same = 0
for t in range(150):
    n = rng.randint(5, 3000)
    jumps = rng.sample(range(1, n), rng.randint(1, 5))
    d = rng.randint(1, 12)
    a, b = run(20, d, n, jumps, "--python"), run(20, d, n, jumps, "--native")
    same += a[0] == b[0] and a[1].replace(" (searched in C)", "") == b[1].replace(" (searched in C)", "")
expect("150 random circulant graphs: Python and C agree", same, 150)


def cycle(n):
    path = os.path.join(TMP, "g.txt")
    with open(path, "w") as f:
        f.write("\n".join(f"{i} {(i + 1) % n}" for i in range(n)) + "\n")
    return path


for n, want in ((10, 0), (16, 0), (9, 1), (15, 1)):
    r = subprocess.run([sys.executable, "-I", DD, "2", str(n // 2), cycle(n), "--bipartite"], capture_output=True)
    expect(f"cycle C_{n} with --bipartite ({'even' if n % 2 == 0 else 'odd: red'})", r.returncode, want)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
