"""Tests of checkers/cluster_check.py (standard library only; run by test.sh): two atoms at distance 1 have energy 0
and at distance 2 exactly 4 (2^-12 - 2^-6) = -63/1024; three atoms on a line at distances 1 and 2 add up; coincident
atoms and malformed lines are refused; the printed value is an upper bound within 10^-12 of the exact energy of a
random cluster (compared with Fraction arithmetic).

  python3 -I tests/test_cluster.py"""
import os
import random
import subprocess
import sys
import tempfile
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "cluster_check.py")
failures = []


def run(n, lines):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("\n".join(lines) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, "lj", str(n), f.name], capture_output=True, text=True)
    os.unlink(f.name)
    return r.returncode, (r.stdout.strip().splitlines() or [""])[-1]


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


expect("two atoms at distance 1", run(2, ["0 0 0", "1 0 0"]), (0, "RESULT 0"))
expect("two atoms at distance 2: -63/1024", run(2, ["0 0 0", "0 2 0"]), (0, "RESULT -63/1024"))
expect("three atoms at 0, 1, 3: 0 + 4(3^-12 - 3^-6) - 63/1024, rounded up at 1e-12", run(3, ["0 0 0", "0 0 1", "0 0 3"])[0], 0)
expect("red: two atoms at the same place", run(2, ["0.5 0.5 0.5", "0.5 0.5 0.5"])[0], 1)
expect("red: a line with two numbers", run(2, ["0 0", "1 0 0"])[0], 1)
expect("red: one line too few", run(3, ["0 0 0", "1 0 0"])[0], 1)
rng = random.Random(20261115)
pts = [[round(rng.uniform(-2, 2), 6) for _ in range(3)] for _ in range(12)]
exact = Fraction(0)
for i in range(12):
    for j in range(i + 1, 12):
        d2 = sum((Fraction(str(a)) - Fraction(str(b))) ** 2 for a, b in zip(pts[i], pts[j]))
        exact += 4 * (1 / d2 ** 6 - 1 / d2 ** 3)
code, last = run(12, [" ".join(f"{x:.6f}" for x in p) for p in pts])
val = Fraction(last.split()[1])
expect("random cluster of 12: the value bounds the exact energy from above, within 1e-12",
       (code, exact <= val < exact + Fraction(1, 10 ** 12)), (0, True))
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
