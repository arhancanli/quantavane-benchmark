"""Tests of checkers/golomb_check.py and its C helper golomb_scan.c (standard library only; run by test.sh): the
Erdos-Turan rulers 2pk + (k^2 mod p), k < p, for primes p on both sides of the 3,000-mark threshold, pass with their
lengths; with the last mark moved to repeat a difference, or with a mark repeated, they fail; the optimal ruler with
5 marks (0 2 7 8 11) passes with length 11.

  python3 -I tests/test_golomb.py"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "golomb_check.py")
TMP = tempfile.mkdtemp(prefix="golomb_test_")
failures = []


def run(m, marks):
    path = os.path.join(TMP, "g.txt")
    open(path, "w").write(" ".join(map(str, marks)) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, str(m), path], capture_output=True, text=True)
    return r.returncode, (r.stdout.strip().splitlines() or [""])[-1]


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


expect("optimal ruler with 5 marks", run(5, [0, 2, 7, 8, 11]), (0, "RESULT 11"))
expect("red: 0 1 2 (difference 1 twice)", run(3, [0, 1, 2])[0], 1)
for p in (101, 2999, 3001, 7919):
    marks = [2 * p * k + (k * k) % p for k in range(p)]
    expect(f"Erdos-Turan ruler, p = {p}", run(p, marks), (0, f"RESULT {marks[-1]}"))
    bad = marks[:-1] + [marks[-2] + marks[1] - marks[0]]
    expect(f"red: p = {p}, last mark repeats a difference", run(p, bad)[0], 1)
    expect(f"red: p = {p}, a mark repeated", run(p, marks[:-1] + [marks[0]])[0], 1)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
