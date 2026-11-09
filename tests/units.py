"""Unit tests of the checkers added or changed in v2.0 (standard library only; run by test.sh).

1. Known objects with known values, built here: each checker must print exactly the value as its RESULT line.
   Binary Golay codes [24,12,8] and [23,12,7] (the second through the dual code and the MacWilliams identities), the
   Hamming code [7,4,3], the hexacode [6,3,4] over GF(4), the ternary Golay codes [12,6,6] and [11,6,5], Reed-Solomon
   codes over GF(5), GF(7), GF(8) and GF(9) (minimum distance n - k + 1 only if the field arithmetic is right), the
   Fano plane C(7,3,2) = 7, two triangles as the Turan covering C(6,2,2,3) = 6, the covering arrays CA(4;2,3,2) and
   CA(5;2,4,2).
2. Red controls: each broken object must be refused (exit status 1).
3. Cross-checks against brute force on random small cases (covering designs of both kinds, covering arrays, linear
   codes over every field): the checkers must agree with a direct count every time.

  python3 -I tests/units.py [CROSS_CHECK_CASES]"""
import importlib.util
import itertools
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "certs", "units")
failures = []


def checker(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "checkers", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write(name, lines):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


def run(prog, args):
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "checkers", prog)] + [str(a) for a in args],
                       capture_output=True, text=True)
    res = [line[7:] for line in r.stdout.splitlines() if line.startswith("RESULT ")]
    return r.returncode, (res[-1] if res else None)


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def known_objects():
    golay_b = ["110111000101", "101110001011", "011100010111", "111000101101", "110001011011", "100010110111",
               "000101101111", "001011011101", "010110111001", "101101110001", "011011100011", "111111111110"]
    g24 = [("0" * i + "1" + "0" * (11 - i)) + golay_b[i] for i in range(12)]
    tg = ["011111", "101221", "110122", "121012", "122101", "112210"]
    t12 = ["0" * i + "1" + "0" * (5 - i) + tg[i] for i in range(6)]
    codes = [("golay24", 2, 24, 12, g24, 8), ("golay23", 2, 23, 12, [r[:-1] for r in g24], 7),
             ("hamming7", 2, 7, 4, ["1000110", "0100101", "0010011", "0001111"], 3),
             ("hexacode", 4, 6, 3, ["100122", "010212", "001221"], 4),
             ("tgolay12", 3, 12, 6, t12, 6), ("tgolay11", 3, 11, 6, [r[:-1] for r in t12], 5)]
    lc = checker("lincode_check")
    for q, k in ((5, 2), (7, 3), (8, 3), (8, 5), (9, 4), (9, 6)):       # Reed-Solomon codes [q-1, k, q-k]
        F = lc.Field(q)
        g = next(a for a in range(2, q) if len({_power(F, a, e) for e in range(1, q)}) == q - 1)
        rows = ["".join(str(_power(F, g, (i * j) % (q - 1))) for j in range(q - 1)) for i in range(k)]
        codes.append((f"rs_q{q}_k{k}", q, q - 1, k, rows, q - k))
    for name, q, n, k, rows, d in codes:
        expect(f"unit  lincode_check {name} [{n},{k}] over GF({q}): distance",
               run("lincode_check.py", [q, n, k, write(name + ".txt", rows)]), (0, str(d)))
    expect("red   lincode_check golay24 with a row repeated (rank 11)",
           run("lincode_check.py", [2, 24, 12, write("golay24_red.txt", g24[:-1] + g24[:1])])[0], 1)
    expect("red   lincode_check hexacode with an entry 4 outside GF(4)",
           run("lincode_check.py", [4, 6, 3, write("hexacode_red.txt", ["100124", "010212", "001221"])])[0], 1)

    fano = ["1 2 4", "2 3 5", "3 4 6", "4 5 7", "5 6 1", "6 7 2", "7 1 3"]
    expect("unit  covering_check Fano plane C(7,3,2)", run("covering_check.py", [7, 3, 2, 2, write("fano.txt", fano)]),
           (0, "7"))
    expect("red   covering_check Fano plane without its last block",
           run("covering_check.py", [7, 3, 2, 2, write("fano_red.txt", fano[:-1])])[0], 1)
    turan = ["1 2", "1 3", "2 3", "4 5", "4 6", "5 6"]
    expect("unit  covering_check two triangles C(6,2,2,3) (Turan)",
           run("covering_check.py", [6, 2, 2, 3, write("turan.txt", turan)]), (0, "6"))
    expect("red   covering_check two triangles without the pair 5 6 ({1,5,6} meets no pair)",
           run("covering_check.py", [6, 2, 2, 3, write("turan_red.txt", turan[:-1])])[0], 1)

    ca = ["000", "011", "101", "110"]
    expect("unit  ca_check CA(4;2,3,2)", run("ca_check.py", [2, 3, 2, write("ca232.txt", ca)]), (0, "4"))
    ca5 = ["0000", "0111", "1011", "1101", "1110"]
    expect("unit  ca_check CA(5;2,4,2)", run("ca_check.py", [2, 4, 2, write("ca242.txt", ca5)]), (0, "5"))
    expect("red   ca_check CA(5;2,4,2) with its first row changed to 1111 (columns 1, 2 never show 0 0)",
           run("ca_check.py", [2, 4, 2, write("ca242_red.txt", ["1111"] + ca5[1:])])[0], 1)


def _power(F, a, e):
    y = 1
    for _ in range(e):
        y = F.mul[y][a]
    return y


def cross_checks(cases):
    rng = random.Random(2026)
    cc, ca, lc = checker("covering_check"), checker("ca_check"), checker("lincode_check")
    bad = 0
    for _ in range(cases):                                  # covering designs, both kinds
        v = rng.randint(3, 10)
        k = rng.randint(2, v)
        t = rng.randint(1, k)
        m = rng.randint(t, v)
        blocks = [rng.sample(range(1, v + 1), k) for _ in range(rng.randint(1, 10))]
        want = all(any(len(set(S) & set(b)) >= t for b in blocks) for S in itertools.combinations(range(1, v + 1), m))
        got = cc.covers_everything(blocks, v, k, t)[0] if m == t else cc.find_bad_set(blocks, v, t, m) is None
        bad += got != want
    for _ in range(cases):                                  # covering arrays
        t, v = rng.randint(1, 3), rng.randint(2, 3)
        k = rng.randint(t, 6)
        rows = [[rng.randrange(v) for _ in range(k)] for _ in range(rng.randint(v ** t, v ** t + 10))]
        want = all(any(all(r[c] == s for c, s in zip(cols, tup)) for r in rows)
                   for cols in itertools.combinations(range(k), t) for tup in itertools.product(range(v), repeat=t))
        bad += (ca.first_gap(rows, t, k, v) is None) != want
    for q in (2, 3, 4, 5, 7, 8, 9):                         # linear codes over every field
        F = lc.Field(q)
        for _ in range(max(1, cases // 7)):
            n = rng.randint(1, 8)
            k = rng.randint(1, n)
            while q ** k > 5000:
                k -= 1
            rows = [[rng.randrange(q) for _ in range(n)] for _ in range(k)]
            weights = []
            for coef in itertools.product(range(q), repeat=k):
                if any(coef):
                    vec = [0] * n
                    for a, r in zip(coef, rows):
                        vec = [F.add[x][F.mul[a][y]] for x, y in zip(vec, r)]
                    weights.append(sum(1 for x in vec if x))
            want = 0 if 0 in weights else min(weights)
            try:
                A, _ = lc.weight_distribution(F, rows, n, k)
                got = next(i for i in range(1, len(A)) if A[i])
            except ValueError:
                got = 0
            bad += got != want
    expect(f"cross-check covering_check, ca_check and lincode_check against brute force ({cases} cases each kind)",
           bad, 0)


def main():
    os.makedirs(OUT, exist_ok=True)
    known_objects()
    cross_checks(int(sys.argv[1]) if len(sys.argv) > 1 else 300)
    print(f"unit tests: {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
