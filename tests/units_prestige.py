"""Unit tests of the checkers added in v2.1 for the Prestige 100 collection (standard library only; run by test.sh).

1. Known objects built here, each with its exact value: a Welch Costas array of order 10, the Petersen graph
   srg(10,3,0,1), the Paley graph srg(13,6,2,3), the Hoffman-Singleton graph srg(50,7,0,1) (Robertson's pentagons and
   pentagrams), the projective planes PG(2,2) and PG(2,3), four MOLS of order 5, Strassen's algorithm <2,2,2;7> over Q,
   Q(i) and GF(2), the schoolbook <2,2,2;8>, a six-city EUC_2D tour.
2. Red controls, each refused (exit status 1): a Costas array with two columns swapped, Petersen minus an edge, Paley 13
   with lambda and mu exchanged, PG(2,3) with one point moved, two equal Latin squares, Strassen with one sign flipped,
   Strassen over GF(2) where characteristic 0 is required, a tour missing a city, three collinear points, a regular
   nonagon (not a counterexample), a path (unimodal) and a triangle (not a forest).
3. Cross-checks against brute force on random small cases: the largest subset in convex position (convex_check.py)
   against all subsets, and independence polynomials of forests (tree_unimodal_check.py) against all vertex subsets.

  python3 -I tests/units_prestige.py [CROSS_CHECK_CASES]"""
import importlib.util
import itertools
import json
import math
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "certs", "units_prestige")
failures = []


def checker(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "checkers", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write(name, text):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(text)
    return path


def expect(prog, args, status, result=None):
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "checkers", prog)] + [str(a) for a in args],
                       capture_output=True, text=True)
    last = [x for x in r.stdout.splitlines() if x.startswith("RESULT ")]
    ok = r.returncode == status and (result is None or (last and last[-1] == f"RESULT {result}"))
    label = f"{prog} {' '.join(os.path.basename(str(a)) for a in args)}"
    print(f"{'ok  ' if ok else 'FAIL'}  {label}: exit {r.returncode}{' ' + last[-1] if last else ''}")
    if not ok:
        failures.append(label)


def edges_text(edges):
    return "".join(f"{a} {b}\n" for a, b in edges)


def main():
    cases = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    os.makedirs(OUT, exist_ok=True)
    # Costas: Welch construction p = 11, primitive root 2 (order 10)
    perm = [pow(2, i, 11) for i in range(10)]
    expect("costas_check.py", [10, write("costas_welch10.txt", " ".join(map(str, perm)) + "\n")], 0, 1)
    bad = perm[:]
    bad[0], bad[1] = bad[1], bad[0]
    expect("costas_check.py", [10, write("control_costas_swap.txt", " ".join(map(str, bad)) + "\n")], 1)
    # strongly regular graphs
    pet = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (1, 6), (2, 7), (3, 8), (4, 9), (5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]
    expect("srg_check.py", [10, 3, 0, 1, write("petersen.txt", edges_text(pet))], 0, 1)
    expect("srg_check.py", [10, 3, 0, 1, write("control_petersen_minus_edge.txt", edges_text(pet[:-1]))], 1)
    sq = {x * x % 13 for x in range(1, 13)}
    paley = [(a, b) for a in range(13) for b in range(a + 1, 13) if (b - a) % 13 in sq]
    path = write("paley13.txt", edges_text(paley))
    expect("srg_check.py", [13, 6, 2, 3, path], 0, 1)
    expect("srg_check.py", [13, 6, 3, 2, path], 1)
    mat = [[1 if (i != j and (j - i) % 13 in sq) else 0 for j in range(13)] for i in range(13)]
    expect("srg_check.py", [13, 6, 2, 3, write("paley13_matrix.txt", "".join("".join(map(str, r)) + "\n" for r in mat))], 0, 1)
    hs = set()
    for h in range(5):
        for j in range(5):
            hs.add(tuple(sorted((5 * h + j, 5 * h + (j + 1) % 5))))
            hs.add(tuple(sorted((25 + 5 * h + j, 25 + 5 * h + (j + 2) % 5))))
            for i in range(5):
                hs.add(tuple(sorted((5 * h + j, 25 + 5 * i + (h * i + j) % 5))))
    expect("srg_check.py", [50, 7, 0, 1, write("hoffman_singleton.txt", edges_text(sorted(hs)))], 0, 1)
    # projective planes PG(2,q), q prime: points and lines are the normalised nonzero vectors of GF(q)^3
    for q in (2, 3):
        vecs = []
        for v in itertools.product(range(q), repeat=3):
            if any(v):
                inv = pow(next(x for x in v if x), -1, q)
                w = tuple(x * inv % q for x in v)
                if w not in vecs:
                    vecs.append(w)
        lines = [[i for i, x in enumerate(vecs) if sum(a * b for a, b in zip(x, L)) % q == 0] for L in vecs]
        expect("projplane_check.py", [q, write(f"pg2_{q}.txt", "".join(" ".join(map(str, l)) + "\n" for l in lines))], 0, 1)
    lines[0] = lines[0][:-1] + [next(x for x in range(13) if x not in lines[0])]
    expect("projplane_check.py", [3, write("control_pg2_3_moved.txt", "".join(" ".join(map(str, l)) + "\n" for l in lines))], 1)
    # MOLS of order 5
    sqs = [[[(k * i + j) % 5 for j in range(5)] for i in range(5)] for k in range(1, 5)]
    block = lambda s: "\n".join(" ".join(map(str, r)) for r in s)
    expect("mols_check.py", [5, write("mols5_4.txt", "\n\n".join(block(s) for s in sqs) + "\n")], 0, 4)
    expect("mols_check.py", [5, write("control_mols5_equal.txt", "\n\n".join(block(s) for s in (sqs[0], sqs[0])) + "\n")], 1)
    # matrix multiplication: Strassen and the schoolbook method for 2 x 2
    def E(*ent):
        m = [[0, 0], [0, 0]]
        for i, j, v in ent:
            m[i][j] = v
        return m
    strassen = [[E((0, 0, 1), (1, 1, 1)), E((0, 0, 1), (1, 1, 1)), E((0, 0, 1), (1, 1, 1))],
                [E((1, 0, 1), (1, 1, 1)), E((0, 0, 1)), E((1, 0, 1), (1, 1, -1))],
                [E((0, 0, 1)), E((0, 1, 1), (1, 1, -1)), E((0, 1, 1), (1, 1, 1))],
                [E((1, 1, 1)), E((1, 0, 1), (0, 0, -1)), E((0, 0, 1), (1, 0, 1))],
                [E((0, 0, 1), (0, 1, 1)), E((1, 1, 1)), E((0, 0, -1), (0, 1, 1))],
                [E((1, 0, 1), (0, 0, -1)), E((0, 0, 1), (0, 1, 1)), E((1, 1, 1))],
                [E((0, 1, 1), (1, 1, -1)), E((1, 0, 1), (1, 1, 1)), E((0, 0, 1))]]
    expect("matmul_check.py", [2, 2, 2, "char0", write("strassen_q.json", json.dumps({"field": "Q", "terms": strassen}))], 0, 7)
    qi = [[[[[x, 0] for x in row] for row in M] for M in t] for t in strassen]
    expect("matmul_check.py", [2, 2, 2, "char0", write("strassen_qi.json", json.dumps({"field": "Q(i)", "terms": qi}))], 0, 7)
    gf2 = write("strassen_gf2.json", json.dumps({"field": "GF(2)", "terms": strassen}))
    expect("matmul_check.py", [2, 2, 2, "any", gf2], 0, 7)
    expect("matmul_check.py", [2, 2, 2, "char0", gf2], 1)
    flipped = json.loads(json.dumps(strassen))
    flipped[6][2][0][0] = -1
    expect("matmul_check.py", [2, 2, 2, "any", write("control_strassen_sign.json", json.dumps({"field": "Q", "terms": flipped}))], 1)
    naive = [[E((i, j, 1)), E((j, k, 1)), E((i, k, 1))] for i in range(2) for j in range(2) for k in range(2)]
    expect("matmul_check.py", [2, 2, 2, "any", write("schoolbook222.json", json.dumps({"field": "Q", "terms": naive}))], 0, 8)
    # a six-city EUC_2D tour; length by the TSPLIB formula (int)(sqrt(d) + 0.5)
    pts = [(0, 0), (3, 4), (7, 1), (6, 8), (2, 9), (10, 5)]
    inst = write("tiny.tsp", "NAME : tiny\nTYPE : TSP\nDIMENSION : 6\nEDGE_WEIGHT_TYPE : EUC_2D\nNODE_COORD_SECTION\n"
                 + "".join(f"{i + 1} {x} {y}\n" for i, (x, y) in enumerate(pts)) + "EOF\n")
    tour = [1, 2, 4, 5, 6, 3]
    length = sum(int(math.sqrt((pts[tour[i] - 1][0] - pts[tour[i - 1] - 1][0]) ** 2 + (pts[tour[i] - 1][1] - pts[tour[i - 1] - 1][1]) ** 2) + 0.5) for i in range(6))
    expect("tsp_check.py", [inst, write("tiny.tour", "TOUR_SECTION\n" + "\n".join(map(str, tour)) + "\n-1\nEOF\n")], 0, length)
    expect("tsp_check.py", [inst, write("control_tiny_missing.tour", "\n".join(map(str, tour[:-1])) + "\n")], 1)
    # Erdos-Szekeres and Erdos #993: controls (no counterexample is known, so no positive object exists)
    expect("convex_check.py", [write("control_collinear.txt", "0 0\n1 1\n2 2\n5 0\n")], 1)
    nonagon = [(round(1000 * math.cos(2 * math.pi * k / 9)), round(1000 * math.sin(2 * math.pi * k / 9))) for k in range(9)]
    expect("convex_check.py", [write("control_nonagon.txt", "".join(f"{x} {y}\n" for x, y in nonagon))], 1)
    expect("tree_unimodal_check.py", [write("control_path.txt", "0 1\n1 2\n2 3\n3 4\n")], 1)
    expect("tree_unimodal_check.py", [write("control_triangle.txt", "0 1\n1 2\n2 0\n")], 1)
    # cross-checks against brute force
    cc, tu = checker("convex_check"), checker("tree_unimodal_check")

    def hull_size(ps):
        ps = sorted(ps)

        def half(seq):
            h = []
            for p in seq:
                while len(h) >= 2 and cc.cross(h[-2], h[-1], p) <= 0:
                    h.pop()
                h.append(p)
            return h
        return len(half(ps)) + len(half(ps[::-1])) - 2
    rng = random.Random(2026)
    bad = 0
    for _ in range(cases):
        n = rng.randint(3, 10)
        while True:
            pts = [(rng.randint(-15, 15), rng.randint(-15, 15)) for _ in range(n)]
            if cc.general_position(pts) is None:
                break
        brute = max([3] + [k for k in range(4, n + 1) if any(hull_size(list(s)) == k for s in itertools.combinations(pts, k))])
        bad += cc.largest_convex(pts) != brute
    print(f"{'ok  ' if not bad else 'FAIL'}  convex_check largest convex subset = brute force on {cases} random point sets")
    if bad:
        failures.append("convex cross-check")
    bad = 0
    for _ in range(cases):
        n = rng.randint(1, 13)
        edges = [(rng.randrange(i), i) for i in range(1, n) if rng.random() < 0.85]
        adj = [[] for _ in range(n)]
        nb = [0] * n
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
            nb[u] |= 1 << v
            nb[v] |= 1 << u
        count = [0] * (n + 1)
        for mask in range(1 << n):
            if all(not (nb[i] & mask) for i in range(n) if mask >> i & 1):
                count[bin(mask).count("1")] += 1
        while len(count) > 1 and count[-1] == 0:
            count.pop()
        bad += tu.independence_polynomial(n, adj) != count
    print(f"{'ok  ' if not bad else 'FAIL'}  tree_unimodal_check independence polynomial = brute force on {cases} random forests")
    if bad:
        failures.append("forest cross-check")
    if tu.first_rise_after_fall([1, 3, 3, 2, 2, 1]) is not None or tu.first_rise_after_fall([1, 3, 2, 4]) != 3:
        failures.append("unimodality test")
    print(f"{len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
