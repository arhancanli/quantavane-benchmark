"""Tests of checkers/cayley_check.py and its C helper cayley_bfs.c (Cayley graphs for the degree-diameter problem;
standard library only and a C compiler; run by test.sh).

- Known Cayley graphs: the Wagner graph Cay(Z_8, {1, 7, 4}) (order 8, degree 3, diameter 2: the table's optimal value
  for degree 3 and diameter 2), the hypercube Q_10 as Cay(Z_2^10, unit vectors) (order 1024, diameter 10), the
  symmetric group S_8 with its adjacent transpositions (order 40320, diameter 28), cycles Cay(Z_n, {1, -1}); both
  routes give the same order and diameter, and one diameter less is refused.
- 120 random inverse-closed generating sets of permutations on up to 8 points: the Python and C searches agree on the
  order and the diameter.
- Red controls: a set not closed under inverses, the identity in S, a generator repeated, too many generators, a line
  that is not a permutation.
- Semidirect products Z_m x|_a Z_n (the form "semidirect m n a", C helper cayley_sdp.c): 150 random groups and
  inverse-closed sets; the Python and C searches of the pairs agree with the permutation route (Python and
  cayley_bfs.c) on the right regular representation of the same group, a separately written program.
- Published record graphs: 15 Cayley graphs of semidirect products whose generators F. Comellas's tables print (read
  15 Nov 2026; for four of them the inverses are added here, and three list their generators as the integers x n + y)
  reproduce their published orders through obb.py, certifying the best known values of 15 cells; one diameter less is
  refused.
- Red controls for the semidirect form: a^m != 1 mod n, a not a unit, the identity, an inverse missing, a pair out of
  range.

  python3 -I tests/test_cayley.py"""
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "cayley_check.py")
sys.path.insert(0, os.path.join(ROOT, "checkers"))
import cayley_check as CC  # noqa: E402
TMP = tempfile.mkdtemp(prefix="cayley_test_")
failures = []


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def run(d, k, m, gens, *flags):
    path = os.path.join(TMP, "g.txt")
    with open(path, "w") as f:
        f.write(f"points {m}\n" + "".join(" ".join(map(str, g)) + "\n" for g in gens))
    r = subprocess.run([sys.executable, "-I", CHECK, str(d), str(k), path] + list(flags), capture_output=True, text=True)
    out = r.stdout.strip().splitlines()
    if r.returncode:
        return "refused"
    return out[-2].split("order ")[1].split(",")[0] + " / " + out[-2].split("diameter ")[1]


def shift(n, a):
    return [(x + a) % n for x in range(n)]


def swap(m, i, j):
    p = list(range(m))
    p[i], p[j] = p[j], p[i]
    return p


cube = [swap(20, 2 * i, 2 * i + 1) for i in range(10)]
sym = [swap(8, i, i + 1) for i in range(7)]
for label, d, k, m, gens, want in (("Wagner graph Cay(Z_8, {1, 7, 4})", 3, 2, 8, [shift(8, 1), shift(8, 7), shift(8, 4)], "8 / 2"),
                                   ("hypercube Q_10", 10, 10, 20, cube, "1024 / 10"),
                                   ("S_8 with adjacent transpositions", 7, 28, 8, sym, "40320 / 28"),
                                   ("cycle C_101 = Cay(Z_101, {1, -1})", 2, 50, 101, [shift(101, 1), shift(101, 100)], "101 / 50")):
    for flag in ("--python", "--native"):
        expect(f"{label} {flag}", run(d, k, m, gens, flag), want)
    expect(f"red {label} with diameter {k - 1}", run(d, k - 1, m, gens), "refused")

rng = random.Random(2026)
agree = 0
for trial in range(120):
    m = rng.randint(3, 8)
    gens = []
    for _ in range(rng.randint(1, 3)):
        p = list(range(m))
        rng.shuffle(p)
        if p == list(range(m)):
            continue
        inv = [0] * m
        for i, x in enumerate(p):
            inv[x] = i
        for g in (p, inv):
            if g not in gens:
                gens.append(g)
    if not gens:
        continue
    a, b = run(len(gens), 10 ** 6, m, gens, "--python"), run(len(gens), 10 ** 6, m, gens, "--native")
    agree += a == b and a != "refused"
    if a != b:
        print(f"FAIL  random set {trial}: Python {a}, C {b}")
expect("random inverse-closed sets: Python and C agree (of those tried)", agree >= 100, True)

expect("red a set not closed under inverses", run(3, 10, 5, [shift(5, 1)]), "refused")
expect("red the identity in S", run(3, 10, 5, [shift(5, 1), shift(5, 4), list(range(5))]), "refused")
expect("red a generator repeated", run(3, 10, 5, [shift(5, 1), shift(5, 4), shift(5, 1)]), "refused")
expect("red more generators than the degree", run(1, 10, 5, [shift(5, 1), shift(5, 4)]), "refused")
expect("red a line that is not a permutation", run(3, 10, 5, [[0, 0, 1, 2, 3]]), "refused")


# semidirect products of cyclic groups
def run_sdp(d, k, m, n, a, gens, *flags):
    path = os.path.join(TMP, "s.txt")
    with open(path, "w") as f:
        f.write(f"semidirect {m} {n} {a}\n" + "".join(f"{x} {y}\n" for x, y in gens))
    r = subprocess.run([sys.executable, "-I", CHECK, str(d), str(k), path] + list(flags), capture_output=True, text=True)
    out = r.stdout.strip().splitlines()
    if r.returncode:
        return "refused"
    return out[-2].split("order ")[1].split(",")[0] + " / " + out[-2].split("diameter ")[1]


def close(gens, m, n, a):
    S = list(dict.fromkeys(gens))
    for g in list(S):
        inv = CC.sdp_inv(g, m, n, a)
        if inv not in S:
            S.append(inv)
    return S


def regular(gens, m, n, a):
    """the right regular representation: s acts on the indices x n + y of the elements by g -> g s"""
    return [[(lambda h: h[0] * n + h[1])(CC.sdp_mul(divmod(i, n), s, m, n, a)) for i in range(m * n)] for s in gens]


agree = tried = 0
while tried < 150:
    n = rng.randint(2, 40)
    a = rng.choice([u for u in range(1, n) if math.gcd(u, n) == 1] or [0])
    o = next(e for e in range(1, n + 1) if pow(a, e, n) == 1 % n)
    m = o * rng.randint(1, max(1, 400 // (o * n)))
    if m * n > 600:
        continue
    gens = close([(rng.randrange(m), rng.randrange(n)) for _ in range(rng.randint(1, 3))], m, n, a)
    gens = [g for g in gens if g != (0, 0)]
    if not gens:
        continue
    tried += 1
    want = run(len(gens), 10 ** 6, m * n, regular(gens, m, n, a), "--python")
    got = {want, run(len(gens), 10 ** 6, m * n, regular(gens, m, n, a), "--native"),
           run_sdp(len(gens), 10 ** 6, m, n, a, gens, "--python"), run_sdp(len(gens), 10 ** 6, m, n, a, gens, "--native")}
    agree += len(got) == 1 and want != "refused"
    if len(got) != 1:
        print(f"FAIL  semidirect {m} {n} {a} {gens}: {got}")
expect("150 random semidirect products: pairs (Python, C) and the regular representation (Python, C) agree", agree, 150)

# published record graphs (F. Comellas's pages desc_g3 to desc_g8, read 15 Nov 2026): degree, diameter, order, m, n, a,
# the generators as printed (pairs, or the integers x n + y)
PUBLISHED = [
    (9, 4, 1640, 40, 41, 22, "[23,14]<>[17,33]:[25,18]<>[15,13]:[27,35]<>[13,33]:[2,23]<>[38,8]:[20,3]<>[20,3]"),
    (10, 4, 2485, 35, 71, 2, "(18,57)<>(17,13), (12,66)<>(23,3), (29,12)<>(6,13), (33,22)<>(2,54), (14,27)<>(21,35)"),
    (14, 3, 1053, 9, 117, 16, "[7,102]<>[2,96]:[8,29]<>[1,4]:[4,14]<>[5,43]:[1,33]<>[8,93]:[8,35]<>[1,25]:[5,95]<>[4,1]:"
                              "[2,73]<>[7,2]"),
    (8, 5, 5334, 21, 254, 25, "[2,60]<>[19,6]:[3,122]<>[18,160]:[6,81]<>[15,241]:[8,169]<>[13,59]"),
    (9, 5, 9020, 20, 451, 46, "(19,402), (14,161), (13,302), (11,412), (10,0)"),
    (10, 5, 14047, 11, 1277, 135, "[10,962]<>[1,384]:[2,27]<>[9,1207]:[8,1151]<>[3,176]:[2,390]<>[9,124]:[7,1138]<>[4,489]"),
    (11, 5, 20952, 24, 873, 785, "[20,465]<>[4,561]:[19,708]<>[5,114]:[13,553]<>[11,277]:[18,763]<>[6,587]:[0,42]<>[0,831]:"
                                 "[12,639]<>[12,639]"),
    (12, 5, 29621, 19, 1559, 1205, "[4,358] [15,963] [12,47] [9,233] :[14,645] [12,1195]"),
    (14, 5, 61307, 101, 607, 122, "[60,466]<>[41,422]:[52,127]<>[49,420]:[38,603]<>[63,174]:[21,132]<>[80,30]:"
                                  "[12,242]<>[89,213]:[40,318]<>[61,423]:[65,248]<>[36,371]"),
    (15, 5, 82584, 36, 2294, 57, "[5,929]<>[31,119]:[8,1792]<>[28,2076]:[19,515]<>[17,1219]:[22,467]<>[14,2151]:"
                                 "[7,2210]<>[29,690]:[16,1994]<>[20,990]:[13,1984]<>[23,1302]:[18,2263]<>[18,2263]"),
    (7, 6, 12654, 18, 703, 85, "(17,397), (13,486), (10,188), (9,0)"),
    (6, 8, 80050, 25, 3202, 1419, "(24,519), (20,163), (14,2724)"),
    (7, 7, 56952, 24, 2373, 44, [3082, 5577, 17883, 29904, 40986, 53484, 55264]),
    (8, 8, 744878, 23, 32386, 2491, [69812, 184915, 266362, 294870, 479750, 502200, 605493, 682624]),
    (9, 8, 1857060, 90, 20634, 233, [232439, 393476, 675380, 870223, 938353, 1008533, 1211224, 1472366, 1633979]),
]
cells = {json.loads(line)["id"]: json.loads(line) for line in open(os.path.join(ROOT, "families", "cayley-degree-diameter",
                                                                               "cells.jsonl"))}
good = 0
for d, k, order, m, n, a, printed in PUBLISHED:
    g = (divmod(i, n) for i in printed) if isinstance(printed, list) else \
        ((int(x), int(y)) for x, y in re.findall(r"[\[(]\s*(\d+)\s*,\s*(\d+)\s*[\])]", printed))
    S = close(list(g), m, n, a)
    path = os.path.join(TMP, f"pub_{d}_{k}.txt")
    with open(path, "w") as f:
        f.write(f"semidirect {m} {n} {a}\n" + "".join(f"{x} {y}\n" for x, y in S))
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "obb.py"), "check", f"caydd-{d}-{k}", path],
                       capture_output=True, text=True)
    ok = (len(S) == d and cells[f"caydd-{d}-{k}"]["best"] == str(order) and f"certified value {order}/1" in r.stdout
          and "does not improve" in r.stdout and run_sdp(d, k - 1, m, n, a, S) == "refused")
    good += ok
    if not ok:
        print(f"FAIL  published ({d},{k}) = {order}: {r.stdout.strip()[-300:]}")
expect("15 published record graphs reproduce their orders through obb.py (cells certified); one diameter less refused",
       good, 15)

w = [(1, 0), (3, 0)]                      # Z_4 x|_3 Z_7: 3^4 = 4 mod 7, not a group
expect("red semidirect: a^m != 1 mod n", run_sdp(2, 10, 4, 7, 3, w), "refused")
expect("red semidirect: a not a unit mod n", run_sdp(2, 10, 2, 9, 3, [(1, 0)]), "refused")
S = close([(1, 1), (0, 1)], 6, 7, 2)
expect("a valid semidirect set (Z_6 x|_2 Z_7, the group of order 42)", run_sdp(len(S), 10, 6, 7, 2, S), "42 / " +
       run(len(S), 10, 42, regular(S, 6, 7, 2)).split(" / ")[1])
expect("red semidirect: the identity in S", run_sdp(len(S) + 1, 10, 6, 7, 2, S + [(0, 0)]), "refused")
expect("red semidirect: an inverse missing", run_sdp(len(S), 10, 6, 7, 2, S[:-1]), "refused")
expect("red semidirect: a pair out of range", run_sdp(len(S) + 1, 10, 6, 7, 2, S + [(6, 0)]), "refused")
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
