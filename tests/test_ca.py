"""Tests of checkers/ca_check.py with its C helpers ca_trie.c and ca_scan.c (standard library only; run by test.sh):
the two C helpers and the Python check give the same verdict on random arrays (every lane width of ca_trie.c, v up to
64, t = 1 to 5), and every gap a helper reports is a tuple its columns really never show; greedy covering arrays pass
all ways; the strength-2 orthogonal array of a prime field (rows (a, b, a + b x)) passes, and with one row dropped or
one symbol changed it is refused all ways; a large random array goes to C by itself.

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
    agree += run(t, k, v, rows, "--python") == run(t, k, v, rows, "--native") == run(t, k, v, rows, "--mark")
expect(f"{total} random arrays: Python, ca_trie.c and ca_scan.c agree", agree, total)

# the helpers themselves: same verdict, and every reported gap is real (its columns never show its tuple)
sys.path.insert(0, os.path.join(ROOT, "checkers"))
import ca_check  # noqa: E402
same = real = cases = covered = 0
for trial in range(300):
    t = rng.randint(1, 5)
    v = rng.choice([2, 3, 4, 5, 7, 8]) if t >= 3 else rng.choice([2, 3, 5, 8, 9, 16, 17, 32, 33, 64])
    if v ** t > 1500:
        continue
    k = rng.randint(t, 9)
    rows = [[rng.randrange(v) for _ in range(k)] for _ in range(rng.randint(v ** t, 3 * v ** t))]
    if rng.random() < 0.5:                       # repair into a covering array: add a row for every missing tuple
        for cs in itertools.combinations(range(k), t):
            have = {tuple(r[c] for c in cs) for r in rows}
            for tup in itertools.product(range(v), repeat=t):
                if tup not in have:
                    row = [rng.randrange(v) for _ in range(k)]
                    for c, x in zip(cs, tup):
                        row[c] = x
                    rows.append(row)
                    have.add(tuple(row[c] for c in cs))
    cases += 1
    g1, g2 = ca_check.first_gap_native(rows, t, k, v, "ca_trie"), ca_check.first_gap_native(rows, t, k, v, "ca_scan")
    g0 = ca_check.first_gap(rows, t, k, v)
    same += (g1 is None) == (g2 is None) == (g0 is None)
    covered += g1 is None
    if g1 is None:
        real += 1
    else:
        cs, tup = g1
        real += len(cs) == len(tup) and all(tuple(r[c] for c in cs) != tuple(tup) for r in rows)
expect(f"{cases} random arrays ({covered} covering): ca_trie.c, ca_scan.c and Python give the same verdict", same, cases)
expect(f"{cases} random arrays: every gap ca_trie.c reports is a tuple its columns never show", real, cases)

# the orthogonal array OA(p^2; 2, p + 1, p): rows (a, b, a + b, a + 2b, ..., a + (p-1) b) with b, plus the column b
for p in (3, 5, 7):
    rows = [[b] + [(a + b * x) % p for x in range(p)] for a in range(p) for b in range(p)]
    for flag in ("--python", "--native", "--mark"):
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
# 20 symbols (32-bit lanes): OA(400; 2, 3, 20) from Z_20 (rows (a, b, a + b)) passes in C by default when the
# check is large enough; a strength-2 array with 21 columns over GF(23) (rows (a, b, a + b x), x = 0..20 and the
# column b): C(22, 2) x 529 visits in C with --native, and with a row dropped refused
p = 23
oa = [[b] + [(a + b * x) % p for x in range(21)] for a in range(p) for b in range(p)]
expect("OA(529; 2, 22, 23) --native", run(2, 22, p, oa, "--native"), 0)
expect("red: OA(529; 2, 22, 23) with a row dropped --native", run(2, 22, p, oa[:-1], "--native"), 1)
# a covering array of strength 3 through ca_trie.c by default: 150 columns over 2 symbols, 120 random rows repaired
# until every 3-set shows all 8 tuples (C(150,3) x rows > 5 x 10^7 visits); a column turned into a copy is refused
rows3 = [[rng.randrange(2) for _ in range(150)] for _ in range(120)]
for cs in itertools.combinations(range(150), 3):
    have = {tuple(r[c] for c in cs) for r in rows3}
    for tup in itertools.product(range(2), repeat=3):
        if tup not in have:
            row = [rng.randrange(2) for _ in range(150)]
            for c, x in zip(cs, tup):
                row[c] = x
            rows3.append(row)
            have.add(tuple(row[c] for c in cs))
expect(f"repaired CA({len(rows3)}; 3, 150, 2) (C by default)", run(3, 150, 2, rows3), 0)
expect(f"same, --mark", run(3, 150, 2, rows3, "--mark"), 0)
copy = [r[:149] + [r[7]] for r in rows3]
expect("red: the same with the last column a copy of column 8", run(3, 150, 2, copy), 1)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
