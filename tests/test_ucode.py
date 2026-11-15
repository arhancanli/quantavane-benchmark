"""Tests of checkers/ucode_check.py and its C helper ucode_scan.c (standard library only; run by test.sh): the binary
Hamming code [7,4,3] and the ternary tetracode [4,2,3] pass both ways and fail at a larger distance; a repeated word,
a symbol outside its coordinate's alphabet and a short word are refused; on random mixed binary/ternary codes this
program and the C helper give the same verdict; a code of 4,096 words (the [12,12,1] binary space, which has distance
1) goes to C by itself and fails at distance 2.

  python3 -I tests/test_ucode.py"""
import itertools
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "ucode_check.py")
TMP = tempfile.mkdtemp(prefix="ucode_test_")
failures = []


def run(spec, D, words, *flags):
    path = os.path.join(TMP, "w.txt")
    with open(path, "w") as f:
        f.write("\n".join(" ".join(map(str, w)) for w in words) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, spec, str(D), path] + list(flags), capture_output=True, text=True)
    return r.returncode, (r.stdout.strip().splitlines() or [""])[-1]


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


G = [[1, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 1, 0, 1], [0, 0, 1, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1]]
ham = [[sum(c * g[j] for c, g in zip(x, G)) % 2 for j in range(7)] for x in itertools.product(range(2), repeat=4)]
tetra = [[a, b, (a + b) % 3, (a + 2 * b) % 3] for a in range(3) for b in range(3)]
for flag in ("--python", "--native"):
    expect(f"Hamming [7,4,3] {flag}", run("2^7", 3, ham, flag), (0, "RESULT 16"))
    expect(f"red: Hamming at distance 4 {flag}", run("2^7", 4, ham, flag)[0], 1)
    expect(f"tetracode [4,2,3] {flag}", run("3^4", 3, tetra, flag), (0, "RESULT 9"))
    expect(f"red: tetracode with a word repeated {flag}", run("3^4", 3, tetra + [tetra[3]], flag)[0], 1)
expect("red: symbol 2 in a binary coordinate", run("2^1.3^2", 1, [[2, 0, 0]])[0], 1)
expect("red: a short word", run("3^4", 1, [[0, 1, 2]])[0], 1)
expect("malformed: alphabet 9", run("9^2", 1, [[0, 1]])[0], 1)
expect("mixed: (0,0,0), (1,1,1), (0,2,2)? distance 2 in 2^1.3^2", run("2^1.3^2", 2, [[0, 0, 0], [1, 1, 1], [0, 2, 2]]), (0, "RESULT 3"))
rng = random.Random(20261115)
agree = 0
for trial in range(60):
    m, n = rng.randint(0, 4), rng.randint(1, 5)
    spec = ".".join(x for x in (f"2^{m}" if m else "", f"3^{n}") if x)
    sizes = [2] * m + [3] * n
    words = [[rng.randrange(q) for q in sizes] for _ in range(rng.randint(2, 40))]
    D = rng.randint(1, len(sizes))
    agree += run(spec, D, words, "--python")[0] == run(spec, D, words, "--native")[0]
expect("60 random mixed codes: Python and C agree", agree, 60)
space = [list(map(int, f"{i:012b}")) for i in range(4096)]
expect("the binary space of length 12 at distance 1 (C by default)", run("2^12", 1, space), (0, "RESULT 4096"))
expect("red: the same at distance 2", run("2^12", 2, space)[0], 1)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
