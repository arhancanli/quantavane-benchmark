"""Tests of checkers/ca_check.py with its C helper ca_scan.c (standard library only; run by test.sh): the C scan and
the Python check give the same verdict on random arrays; greedy covering arrays pass both ways; the strength-2
orthogonal array of a prime field (rows (a, b, a + b x)) passes, and with one row dropped or one symbol changed it is
refused both ways; a large random array goes to C by itself.

  python3 -I tests/test_ca.py"""
import itertools
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "ca_check.py")
TMP = tempfile.mkdtemp(prefix="ca_test_")
failures = []


def run(t, k, v, rows, *flags):
    path = os.path.join(TMP, "a.txt")
    with open(path, "w") as f:
        f.write("\n".join(" ".join(map(str, r)) for r in rows) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, str(t), str(k), str(v), path] + list(flags),
                       capture_output=True, text=True)
    return r.returncode


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


rng = random.Random(20261115)
agree = total = 0
for trial in range(80):
    t, v = rng.randint(1, 4), rng.randint(2, 5)
    k = rng.randint(t, 10)
    if v ** t > 300:
        continue
    rows = [[rng.randrange(v) for _ in range(k)] for _ in range(rng.randint(v ** t, 4 * v ** t))]
    total += 1
    agree += run(t, k, v, rows, "--python") == run(t, k, v, rows, "--native")
expect(f"{total} random arrays: Python and C agree", agree, total)

# the orthogonal array OA(p^2; 2, p + 1, p): rows (a, b, a + b, a + 2b, ..., a + (p-1) b) with b, plus the column b
for p in (3, 5, 7):
    rows = [[b] + [(a + b * x) % p for x in range(p)] for a in range(p) for b in range(p)]
    for flag in ("--python", "--native"):
        expect(f"OA({p * p}; 2, {p + 1}, {p}) {flag}", run(2, p + 1, p, rows, flag), 0)
        expect(f"red: OA({p * p}; 2, {p + 1}, {p}) with a row dropped {flag}", run(2, p + 1, p, rows[1:], flag), 1)
        bad = [r[:] for r in rows]
        bad[4][2] = (bad[4][2] + 1) % p
        expect(f"red: OA({p * p}; 2, {p + 1}, {p}) with one symbol changed {flag}", run(2, p + 1, p, bad, flag), 1)

# a random array of 3,000 rows, 60 columns over 3 symbols covers every 4-set (C(60,4) x 3,000 = 1.46 x 10^9 visits:
# C by default); duplicating one column makes the 4-sets holding both copies miss tuples such as (0, 1, ., .)
big = [[rng.randrange(3) for _ in range(60)] for _ in range(3000)]
expect("random CA(3000; 4, 60, 3) (C by default)", run(4, 60, 3, big), 0)
dup = [r[:-1] + [r[0]] for r in big]
expect("red: the same with the last column a copy of the first", run(4, 60, 3, dup), 1)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
