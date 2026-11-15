"""Tests of checkers/covering_check.py for (v,k,t) coverings with its C helper covering_mark.c (standard library only;
run by test.sh): the C marking and the Python marking give the same verdict and the same count of uncovered t-subsets
on random block sets; greedy coverings pass both ways, and with one block dropped both refuse them; a covering with
more than 2 x 10^7 subsets to mark goes to C by itself, and the same covering with one block dropped is refused.

  python3 -I tests/test_covering.py"""
import itertools
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "covering_check.py")
failures = []
TMP = tempfile.mkdtemp(prefix="covering_test_")


def run(v, k, t, m, blocks, *flags):
    path = os.path.join(TMP, "d.txt")
    with open(path, "w") as f:
        f.write("\n".join(" ".join(map(str, b)) for b in blocks) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, str(v), str(k), str(t), str(m), path] + list(flags),
                       capture_output=True, text=True)
    lines = r.stdout.strip().splitlines()
    return r.returncode, lines[0] if lines else ""


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def greedy(v, k, t):
    covered, blocks = set(), []
    for T in itertools.combinations(range(1, v + 1), t):
        if T in covered:
            continue
        rest = [p for p in range(1, v + 1) if p not in T][:k - t]
        b = sorted(T + tuple(rest))
        blocks.append(b)
        covered.update(itertools.combinations(b, t))
    return blocks


rng = random.Random(20261115)
same = 0
for trial in range(60):
    v = rng.randint(5, 16)
    k = rng.randint(1, min(7, v))
    t = rng.randint(1, k)
    blocks = [sorted(rng.sample(range(1, v + 1), k)) for _ in range(rng.randint(1, 80))]
    a, b = run(v, k, t, t, blocks, "--python"), run(v, k, t, t, blocks, "--native")
    same += a[0] == b[0] and a[1].replace(" (marked in C)", "") == b[1].replace(" (marked in C)", "")
expect("60 random block sets: Python and C agree (verdict and count)", same, 60)
for v, k, t in ((12, 5, 3), (14, 6, 4), (16, 7, 3), (20, 8, 2), (11, 6, 5)):
    bl = greedy(v, k, t)
    for flag in ("--python", "--native"):
        expect(f"greedy C({v},{k},{t}) with {len(bl)} blocks {flag}", run(v, k, t, t, bl, flag)[0], 0)
        expect(f"red: C({v},{k},{t}) with its last block dropped {flag}", run(v, k, t, t, bl[:-1], flag)[0], 1)
# above 2 x 10^7 subsets to mark the C helper is used by default: F = {1..15} plus each 5-subset S of {16..30} gives
# C(15,5) = 3,003 blocks of 20 points, 3,003 x C(20,5) = 46.6 million marks, and covers every 5-subset T of 1..30 (take
# S containing T's points above 15); with one block dropped, its own S is uncovered
F = list(range(1, 16))
blocks = [F + list(S) for S in itertools.combinations(range(16, 31), 5)]
code, line = run(30, 20, 5, 5, blocks)
expect("C(30,20,5) with 3,003 blocks (46.6 million marks, C by default)", (code, "marked in C" in line), (0, True))
code, line = run(30, 20, 5, 5, blocks[1:])
expect("red: the same with one block dropped", (code, line.startswith("1 of 142506")), (1, True))

# m > t: the search in C (covering_lotto.c) against the Python search, which it follows step for step: on random block
# sets, half of them repaired into valid designs (a block through a bad set found by the Python search), both must give
# the same verdict and the same bad set
sys.path.insert(0, os.path.join(ROOT, "checkers"))
import covering_check  # noqa: E402

same = valid = 0
for trial in range(200):
    v = rng.randint(5, 22)
    k = rng.randint(1, min(8, v - 1))
    t = rng.randint(1, k)
    m = rng.randint(t + 1, min(v, t + 6))
    blocks = [sorted(rng.sample(range(1, v + 1), k)) for _ in range(rng.randint(1, 40))]
    if trial % 2 == 0:
        for _ in range(400):
            bad = covering_check.find_bad_set(blocks, v, t, m)
            if bad is None:
                break
            pts = sorted(bad)
            rng.shuffle(pts)
            b = set(pts[:k])
            while len(b) < k:
                b.add(rng.randint(1, v))
            blocks.append(sorted(b))
    a, b = run(v, k, t, m, blocks, "--python"), run(v, k, t, m, blocks, "--native")
    valid += a[0] == 0
    same += a[0] == b[0] and a[1].replace(" (searched in C)", "") == b[1].replace(" (searched in C)", "")
expect(f"200 random (v,k,t,m) block sets ({valid} valid): Python and C agree (verdict and bad set)", same, 200)
for ref in sorted(os.listdir(os.path.join(ROOT, "refs"))):
    parts = ref[len("ours_covering_"):-4].split("-") if ref.startswith("ours_covering_") else []
    if len(parts) != 4:
        continue
    v, k, t, m = map(int, parts)
    bl = [list(map(int, x.split())) for x in open(os.path.join(ROOT, "refs", ref)) if x.strip()]
    for flag in ("--python", "--native"):
        expect(f"our C({v},{k},{t},{m}) with {len(bl)} blocks {flag}", run(v, k, t, m, bl, flag)[0], 0)
# every 5-subset of 1..14 (2,002 blocks) is a (14,5,3,5) covering, searched in C by default; with the blocks that meet
# S = {1,...,5} in 3 or more points removed, S is bad and the search must find a bad set
blocks = [list(b) for b in itertools.combinations(range(1, 15), 5)]
code, line = run(14, 5, 3, 5, blocks)
expect("all 2,002 5-subsets of 1..14 as a C(14,5,3,5) design (C by default)", (code, line), (0, "no bad m-subset exists "
                                                                                           "(searched in C)"))
holes = [b for b in blocks if len(set(b) & {1, 2, 3, 4, 5}) < 3]
code, line = run(14, 5, 3, 5, holes)
expect(f"red: the {len(holes)} blocks meeting {{1..5}} in at most 2 points", (code, line.startswith("the 5-subset")),
       (1, True))
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
