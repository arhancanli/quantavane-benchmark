"""Tests of checkers/ds_check.py, difference sets in abelian groups, and its C helper ds_scan.c (standard library only;
run by test.sh): known difference sets pass both ways and with one element changed or repeated are refused; the C
count (with its fast methods, and digit by digit) and the Python count agree on random subsets; known signed
difference sets pass with --signed and fail with a sign flipped or an element moved; a Paley set with 6.2 million ordered pairs goes to C by itself.

Known sets: Paley sets (the squares modulo a prime p = 3 mod 4), Singer's (13,4,1) set {0,1,3,9}, and from D. Gordon's
La Jolla Difference Set Repository (CC BY 4.0) sets with parameters (16,6,2), (40,13,4), (45,12,3), (36,15,6) and
(64,28,12) in the groups named below, written in their primary decomposition.

  python3 -I tests/test_ds.py"""
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "ds_check.py")
TMP = tempfile.mkdtemp(prefix="ds_test_")
failures = []


def run(orders, k, lam, elems, *flags):
    path = os.path.join(TMP, "d.txt")
    with open(path, "w") as f:
        f.write("\n".join(" ".join(map(str, e if isinstance(e, (list, tuple)) else [e])) for e in elems) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, ",".join(map(str, orders)), str(k), str(lam), path] + list(flags),
                       capture_output=True, text=True)
    lines = r.stdout.strip().splitlines()
    return r.returncode, lines[1] if len(lines) > 1 else (lines[0] if lines else "")


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def paley(p):
    return sorted({x * x % p for x in range(1, p)})


KNOWN = [
    ("Paley (11,5,2)", [11], 5, 2, paley(11)),
    ("Paley (43,21,10)", [43], 21, 10, paley(43)),
    ("Singer (13,4,1)", [13], 4, 1, [0, 1, 3, 9]),
    ("(16,6,2) in Z_4 x Z_4", [4, 4], 6, 2, [[0, 0], [1, 0], [0, 1], [2, 1], [1, 2], [2, 2]]),
    ("(16,6,2) in Z_2 x Z_8", [2, 8], 6, 2, [[0, 0], [0, 1], [0, 2], [0, 5], [1, 0], [1, 6]]),
    ("(40,13,4) in Z_40", [40], 13, 4, [0, 1, 2, 4, 5, 8, 13, 14, 17, 19, 24, 26, 34]),
    ("(45,12,3) in Z_3 x Z_15", [3, 3, 5], 12, 3,
     [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 2, 1], [0, 0, 3], [0, 1, 1], [1, 0, 0], [1, 1, 2], [1, 2, 3], [2, 0, 0],
      [2, 1, 3], [2, 2, 2]]),
    ("(36,15,6) in Z_6 x Z_6", [2, 2, 3, 3], 15, 6,
     [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 2, 0], [1, 0, 0, 2], [1, 1, 2, 2], [1, 1, 0, 2], [0, 1, 1, 1],
      [1, 0, 0, 0], [1, 1, 2, 0], [1, 1, 1, 0], [0, 1, 2, 2], [1, 0, 0, 1], [1, 1, 0, 1], [1, 1, 1, 1]]),
    ("(64,28,12) in Z_8 x Z_8", [8, 8], 28, 12,
     [[0, 0], [1, 0], [0, 1], [2, 0], [0, 2], [3, 0], [1, 2], [1, 4], [0, 3], [4, 1], [2, 2], [4, 4], [3, 1], [3, 4],
      [1, 6], [2, 3], [2, 5], [4, 3], [6, 4], [4, 6], [7, 1], [3, 5], [7, 2], [6, 3], [6, 5], [6, 6], [7, 5], [7, 6]]),
    ("(16,6,2) in Z_2^4", [2, 2, 2, 2], 6, 2,
     [[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 1, 1, 1]]),
]
for name, orders, k, lam, elems in KNOWN:
    v = 1
    for n in orders:
        v *= n
    for flag in ("--python", "--native", "--plain"):
        expect(f"{name} {flag}", run(orders, k, lam, elems, flag)[0], 0)
        # one element moved to an element outside the set
        flat = [tuple(e) if isinstance(e, list) else (e,) for e in elems]
        allel = [()]
        for n in orders:
            allel = [a + (x,) for a in allel for x in range(n)]
        new = next(a for a in allel if a not in flat)
        moved = flat[1:] + [new]
        expect(f"red: {name} with an element moved {flag}", run(orders, k, lam, moved, flag)[0], 1)
        expect(f"red: {name} with an element repeated {flag}", run(orders, k, lam, flat[:-1] + flat[:1], flag)[0], 1)

# C against Python on random subsets of sizes k with lambda (v - 1) = k (k - 1): the same verdict and the same first
# element that fails
rng = random.Random(20261115)
same = 0
CASES = [([7], 3), ([13], 4), ([16], 6), ([2, 2, 2, 2], 6), ([4, 4], 10), ([3, 9], 13), ([5, 5], 9), ([31], 6),
         ([31], 15), ([2, 3, 5], 29), ([2, 2, 3, 3], 15), ([2, 2, 4, 3, 3], 66), ([2, 2, 2, 2, 2, 2], 28), ([3, 3, 5], 12)]
for trial in range(40):
    orders, k = CASES[trial % len(CASES)]
    v = 1
    for n in orders:
        v *= n
    allel = [()]
    for n in orders:
        allel = [a + (x,) for a in allel for x in range(n)]
    elems = rng.sample(allel, k)
    lam = k * (k - 1) // (v - 1)
    a, b, c = (run(orders, k, lam, elems, f) for f in ("--python", "--native", "--plain"))
    same += a[0] == b[0] == c[0] and a[1] == b[1].replace(" (counted in C)", "") == c[1].replace(" (counted in C)", "")
expect("40 random subsets: Python, C and C digit by digit give the same verdict and first element", same, 40)
cnt = 0
for p in (7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83):
    q = paley(p)
    q2 = q[:-1] + [next(x for x in range(p) if x not in q)]
    a, b = run([p], len(q), (p - 3) // 4, q2, "--python"), run([p], len(q), (p - 3) // 4, q2, "--native")
    cnt += a[0] == b[0] == 1 and a[1].replace(" (counted in C)", "") == b[1].replace(" (counted in C)", "")
expect("12 broken Paley sets: Python and C refuse with the same first element", cnt, 12)
# a Paley set of 2,499 elements of Z_4999: 6.2 million ordered pairs, counted in C by default
q = paley(4999)
code, line = run([4999], len(q), 1249, q)
expect("Paley (4999,2499,1249), C by default", (code, line.endswith("(counted in C)")), (0, True))
code, line = run([4999], len(q), 1249, q[:-1] + [0])
expect("red: the same with its last element replaced by 0", code, 1)
# signed difference sets (--signed): each line a sign, then the coordinates. Known sets from Gordon's La Jolla Signed
# Difference Set Repository (CC BY 4.0): SDS(5,4,-1) in Z_5 (Paley), SDS(11,6,1) in Z_11 (Paley and zero), SDS(9,8,-1)
# in Z_3 x Z_3 (He, Chen and Ge); with one sign flipped or one element moved they must be refused
SIGNED = [
    ("SDS(5,4,-1) in Z_5", [5], 4, -1, [("+", (1,)), ("+", (4,)), ("-", (2,)), ("-", (3,))]),
    ("SDS(11,6,1) in Z_11", [11], 6, 1, [("+", (x,)) for x in (1, 3, 4, 5, 9)] + [("-", (0,))]),
    ("SDS(9,8,-1) in Z_3 x Z_3", [3, 3], 8, -1, [("+", e) for e in ((1, 1), (2, 0), (2, 2), (1, 0))]
     + [("-", e) for e in ((0, 1), (0, 2), (1, 2), (2, 1))]),
]


def run_signed(orders, k, lam, items):
    path = os.path.join(TMP, "s.txt")
    with open(path, "w") as f:
        f.write("\n".join(sg + " " + " ".join(map(str, e)) for sg, e in items) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, ",".join(map(str, orders)), str(k), str(lam), path, "--signed"],
                       capture_output=True, text=True)
    return r.returncode


for name, orders, k, lam, items in SIGNED:
    expect(f"signed {name}", run_signed(orders, k, lam, items), 0)
    flipped = [("-" if items[0][0] == "+" else "+", items[0][1])] + items[1:]
    expect(f"red: signed {name} with one sign flipped", run_signed(orders, k, lam, flipped), 1)
    allel = [()]
    for n in orders:
        allel = [a + (x,) for a in allel for x in range(n)]
    new = next(a for a in allel if a not in [e for _, e in items])
    expect(f"red: signed {name} with an element moved", run_signed(orders, k, lam, items[:-1] + [(items[-1][0], new)]),
           1)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
