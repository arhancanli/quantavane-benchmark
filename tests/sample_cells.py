"""Sampled-cell tests for the problem families (standard library only; run by test.sh).

For each family a few cells are drawn at random (seeded, among cells small enough to build an object for quickly).
For each drawn cell our own code builds a simple valid object (a greedy covering design or covering array, random
points on the sphere, a random linear code in systematic form, a greedy constant weight code, an ordered orthogonal
array made of unit vectors, a grid of equal circles, circles of radii 1..N in a row); obb.py must certify it
and must find that it does not improve the best known value. Then a red control (the same object broken: a block,
row or word removed or repeated, a dependent row, a point too few) must be refused. The project-scheduling family
needs the instance files of its sets (not copied here): its cells are tested when instances/rcpsp/ holds them, and its
checker is tested on instances generated here in all three formats.

  python3 -I tests/sample_cells.py [CELLS_PER_FAMILY] [SEED]"""
import itertools
import math
import json
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "certs", "samples")
CHECKERS = os.path.join(ROOT, "checkers")
failures = []


def family_cells(name):
    with open(os.path.join(ROOT, "families", name, "cells.jsonl")) as f:
        return [json.loads(line) for line in f if line.strip()]


def obb(pid, path):
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "obb.py"), "check", pid, path],
                       capture_output=True, text=True)
    words = [w for w in ("IMPROVES", "does not improve", "NOT CERTIFIED") if w in r.stdout]
    return ",".join(sorted(words, key=r.stdout.find)) + ","


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def write(name, lines):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


# ------------------------------------------------------------------------------------------------ objects

def greedy_covering(v, k, t):
    """Blocks covering every t-subset of 1..v: each still uncovered t-subset, in order, gets a block made of it and
    the first other points."""
    covered, blocks = set(), []
    for T in itertools.combinations(range(1, v + 1), t):
        if T in covered:
            continue
        rest = [p for p in range(1, v + 1) if p not in T][:k - t]
        b = sorted(T + tuple(rest))
        blocks.append(b)
        covered.update(itertools.combinations(b, t))
    return blocks


def greedy_array(t, k, v, rng):
    """Random rows (v^t of them), then one new row for each tuple still missing: a covering array, not a small one."""
    rows = [[rng.randrange(v) for _ in range(k)] for _ in range(v ** t)]
    for cols in itertools.combinations(range(k), t):
        seen = {tuple(r[c] for c in cols) for r in rows}
        for tup in itertools.product(range(v), repeat=t):
            if tup not in seen:
                r = [rng.randrange(v) for _ in range(k)]
                for c, s in zip(cols, tup):
                    r[c] = s
                rows.append(r)
                seen.add(tup)
    return rows


def greedy_cw(n, d, w):
    """The lexicographic code: every w-subset of 1..n in order, kept when it differs from all kept ones in >= d."""
    share = w - (d + 1) // 2 + 1        # two words of weight w are too close when they share this many positions
    words, seen = [], set()
    for x in itertools.combinations(range(1, n + 1), w):
        subs = list(itertools.combinations(x, share)) if share > 0 else []
        if share > 0 and any(s in seen for s in subs):
            continue
        words.append(x)
        seen.update(subs)
    return words


# ------------------------------------------------------------------------------------------------ families

def test_covering_design(n, rng):
    import math
    small = [c for c in family_cells("covering-design")
             if c["params"]["v"] <= 13 and math.comb(c["params"]["v"], c["params"]["t"]) <= 1500]
    for c in rng.sample(small, min(n, len(small))):
        p = c["params"]
        blocks = greedy_covering(p["v"], p["k"], p["t"])
        lines = [" ".join(map(str, b)) for b in blocks]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} greedy covering ({len(blocks)} blocks)", obb(c["id"], good), "does not improve,")
        if p["m"] == p["t"]:     # the last block holds a t-subset no earlier block holds
            bad = write(f"{c['id']}_red.txt", lines[:-1])
            what = "last block removed"
        else:
            bad = write(f"{c['id']}_red.txt", lines[1:] + [" ".join(map(str, blocks[0][:-1] + [p["v"] + 1]))])
            what = "a point outside 1..v"
        expect(f"red   {c['id']} ({what})", obb(c["id"], bad), "NOT CERTIFIED,")
    # the cells with m > t and more than 1,000 blocks (searched in C since 15 Nov 2026): a greedy t-covering is a
    # valid (v,k,t,m) design; with the blocks that meet one m-subset in t or more points removed, that m-subset is bad
    big = [c for c in family_cells("covering-design") if c["params"]["m"] > c["params"]["t"] and int(c["best"]) > 1000
           and math.comb(c["params"]["v"], c["params"]["t"]) <= 20000]
    for c in rng.sample(big, min(n, len(big))):
        p = c["params"]
        blocks = greedy_covering(p["v"], p["k"], p["t"])
        good = write(f"{c['id']}.txt", [" ".join(map(str, b)) for b in blocks])
        expect(f"sample {c['id']} greedy covering ({len(blocks)} blocks, searched in C)", obb(c["id"], good),
               "does not improve," if len(blocks) >= int(c["best"]) else "IMPROVES,")
        S = set(rng.sample(range(1, p["v"] + 1), p["m"]))
        holes = [" ".join(map(str, b)) for b in blocks if len(S & set(b)) < p["t"]]
        bad = write(f"{c['id']}_red.txt", holes)
        expect(f"red   {c['id']} (the blocks meeting one {p['m']}-subset in {p['t']} or more points removed)",
               obb(c["id"], bad), "NOT CERTIFIED,")


def test_covering_array(n, rng):
    import math
    small = [c for c in family_cells("covering-array")
             if math.comb(c["params"]["k"], c["params"]["t"]) * c["params"]["v"] ** c["params"]["t"] <= 200000]
    for c in rng.sample(small, min(n, len(small))):
        p = c["params"]
        rows = greedy_array(p["t"], p["k"], p["v"], rng)
        lines = [" ".join(map(str, r)) for r in rows]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} greedy array ({len(rows)} rows)", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines[:-1])        # the last row was added for a missing tuple
        expect(f"red   {c['id']} (last row removed)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_spherical_code(n, rng):
    small = [c for c in family_cells("spherical-code") if c["params"]["n"] <= 60 and c["params"]["d"] <= 6]
    for c in rng.sample(small, min(n, len(small))):
        d, m = c["params"]["d"], c["params"]["n"]
        pts = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(m)]
        lines = [",".join(f"{x:.15f}" for x in pt) for pt in pts]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} random points", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines[:-1])
        expect(f"red   {c['id']} (a point too few)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_linear_code(n, rng):
    small = [c for c in family_cells("linear-code")
             if c["params"]["q"] ** min(c["params"]["k"], c["params"]["n"] - c["params"]["k"]) <= 4096]
    for c in rng.sample(small, min(n, len(small))):
        q, length, k = c["params"]["q"], c["params"]["n"], c["params"]["k"]
        rows = [[1 if j == i else 0 for j in range(k)] + [rng.randrange(q) for _ in range(length - k)]
                for i in range(k)]
        lines = [" ".join(map(str, r)) for r in rows]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} random systematic code", obb(c["id"], good), "does not improve,")
        if k >= 2:
            bad = write(f"{c['id']}_red.txt", lines[:-1] + [lines[0]])
            what = "a row repeated"
        else:
            bad = write(f"{c['id']}_red.txt", [" ".join(["0"] * length)])
            what = "the zero row"
        expect(f"red   {c['id']} ({what})", obb(c["id"], bad), "NOT CERTIFIED,")


def test_quantum_code(n, rng):
    """Single-qudit Z stabilizers Z_1, ..., Z_(n-k) (with x Z_i, x^2 Z_i over GF(4) and GF(8), so that they generate
    the group over GF(2)) make a valid code of distance 1; with one generator dropped the size is wrong."""
    small = [c for c in family_cells("quantum-code") if c["params"]["n"] - c["params"]["k"] <= 12]
    for c in rng.sample(small, min(n, len(small))):
        q, length, k = c["params"]["q"], c["params"]["n"], c["params"]["k"]
        m = {2: 1, 3: 1, 5: 1, 7: 1, 4: 2, 8: 3}[q]
        lines = []
        for i in range(length - k):
            for j in range(m):
                lines.append(" ".join(["0"] * length) + " | " + " ".join(str(2 ** j if t == i else 0) for t in range(length)))
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} single-qudit Z stabilizers", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines[:-1])
        expect(f"red   {c['id']} (a generator dropped)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_quantum_code_search(n, rng):
    """Qubit cells checked by the low-weight search (their stabilizer is too large to list): single-qubit Z
    stabilizers Z_1, ..., Z_(n-k) leave X on a free qubit as a logical operator of weight 1, which the search finds
    at weight 1; with a generator dropped the size is wrong."""
    big = [c for c in family_cells("quantum-code") if c["params"]["q"] == 2 and c["params"]["n"] - c["params"]["k"] > 37]
    for c in rng.sample(big, min(n, len(big))):
        length, k = c["params"]["n"], c["params"]["k"]
        lines = [" ".join(["0"] * length) + " | " + " ".join("1" if t == i else "0" for t in range(length))
                 for i in range(length - k)]
        expect(f"sample {c['id']} single-qubit Z stabilizers (low-weight search)",
               obb(c["id"], write(f"{c['id']}.txt", lines)), "does not improve,")
        expect(f"red   {c['id']} (a generator dropped)", obb(c["id"], write(f"{c['id']}_red.txt", lines[:-1])),
               "NOT CERTIFIED,")


def test_ea_quantum_code(n, rng):
    """Z_1, ..., Z_(n-k) and X_1, ..., X_c: c pairs that do not commute and n-k-c isotropic generators, a valid
    entanglement-assisted code [[n,k;c]] of distance 1 (or n + 1 when it has no nonzero logical element); with one
    generator dropped the size is wrong."""
    small = [c for c in family_cells("ea-quantum-code") if c["params"]["n"] - c["params"]["k"] + c["params"]["c"] <= 14]
    for c in rng.sample(small, min(n, len(small))):
        q, length, k, e = (c["params"][x] for x in ("q", "n", "k", "c"))
        zero = ["0"] * length
        lines = []
        for i in range(length - k):
            lines.append(" ".join(zero) + " | " + " ".join("1" if t == i else "0" for t in range(length)))
        for i in range(e):
            lines.append(" ".join("1" if t == i else "0" for t in range(length)) + " | " + " ".join(zero))
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} single-qudit Z and X generators", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines[:-1])
        expect(f"red   {c['id']} (a generator dropped)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_unrestricted_code(n, rng):
    """The constant words (s, s, ..., s), one per symbol of the smallest alphabet: every two differ everywhere, a valid
    code below the table; a word repeated must be refused."""
    for c in rng.sample(family_cells("unrestricted-code"), n):
        P = c["params"]
        length = P["n"] + P.get("m", 0)
        smallest = 2 if "m" in P else P["q"]
        lines = [" ".join([str(s)] * length) for s in range(smallest)]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} constant words", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines + [lines[0]])
        expect(f"red   {c['id']} (a word repeated)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_ordered_orthogonal_array(n, rng):
    """An object made of distinct unit vectors has the strength asked for with the fewest factors that can carry it; a
    column repeated at depth 1 of another factor (or at depth 2 of the same one) breaks it."""
    def depth(c):
        return c["params"]["k"] if c["params"]["T"] == "net" else c["params"]["T"]
    small = []
    for c in family_cells("ordered-orthogonal-array"):
        m, k, d = c["params"]["m"], c["params"]["k"], depth(c)
        s0 = -(-k // min(d, k))
        if s0 * d <= m and s0 < int(c["best"]) and c["params"]["b"] ** m <= 4096:
            small.append(c)
    for c in rng.sample(small, min(n, len(small))):
        m, k, d = c["params"]["m"], c["params"]["k"], depth(c)
        s0 = -(-k // min(d, k))
        rows = [[1 if col == r else 0 for col in range(s0 * d)] for r in range(m)]
        good = write(f"{c['id']}.txt", [" ".join(map(str, r)) for r in rows])
        expect(f"sample {c['id']} unit vectors, {s0} factor(s)", obb(c["id"], good), "does not improve,")
        src, dst = (0, d) if s0 >= 2 else (0, 1)
        bad_rows = [r[:] for r in rows]
        for r in bad_rows:
            r[dst] = r[src]
        bad = write(f"{c['id']}_red.txt", [" ".join(map(str, r)) for r in bad_rows])
        expect(f"red   {c['id']} (a column repeated)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_orthogonal_array(n, rng):
    """The unit-vector object of test_ordered_orthogonal_array written out run by run (all x G over the field): valid
    with few factors, below the table; with one run changed it must be refused."""
    sys.path.insert(0, CHECKERS)
    import ooa_check as oc

    def depth(c):
        return c["params"]["k"] if c["params"]["T"] == "net" else c["params"]["T"]
    small = []
    for c in family_cells("orthogonal-array"):
        m, k, d = c["params"]["m"], c["params"]["k"], depth(c)
        s0 = -(-k // min(d, k))
        if s0 * d <= m and s0 < int(c["best"]) and c["params"]["b"] ** m <= 4096 and c["params"]["b"] in oc.FIELDS:
            small.append(c)
    for c in rng.sample(small, min(n, len(small))):
        b, m, k, d = c["params"]["b"], c["params"]["m"], c["params"]["k"], depth(c)
        F = oc.Field(b)
        s0 = -(-k // min(d, k))
        G = [[1 if col == r else 0 for col in range(s0 * d)] for r in range(m)]
        runs = []
        for x in itertools.product(range(b), repeat=m):
            w = [0] * (s0 * d)
            for coef, row in zip(x, G):
                if coef:
                    w = [F.add[a][F.mul[coef][g]] for a, g in zip(w, row)]
            runs.append(w)
        lines = [" ".join(map(str, r)) for r in runs]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} unit vectors written out, {s0} factor(s)", obb(c["id"], good), "does not improve,")
        bad_runs = [r[:] for r in runs]
        bad_runs[1][0] = (bad_runs[1][0] + 1) % b
        bad = write(f"{c['id']}_red.txt", [" ".join(map(str, r)) for r in bad_runs])
        expect(f"red   {c['id']} (one run changed)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_lj_cluster(n, rng):
    """Atoms on a cubic grid of step 1.1: a valid cluster far above the table's energy; two atoms at the same place
    must be refused."""
    for c in rng.sample(family_cells("lj-cluster"), n):
        N = c["params"]["n"]
        k = 1
        while k ** 3 < N:
            k += 1
        pts = [(1.1 * i, 1.1 * j, 1.1 * l) for i in range(k) for j in range(k) for l in range(k)][:N]
        lines = [f"{x:.1f} {y:.1f} {z:.1f}" for x, y, z in pts]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} cubic grid", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines[:-1] + [lines[0]])
        expect(f"red   {c['id']} (two atoms at the same place)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_degree_diameter(n, rng):
    """The cycle on 2D + 1 vertices has degree 2 and diameter D: valid and below the table; the cycle on 2D + 3 vertices
    has diameter D + 1 and must be refused."""
    for c in rng.sample(family_cells("degree-diameter"), n):
        d = c["params"]["d"]
        m = 2 * d + 1
        good = write(f"{c['id']}.txt", [f"{i} {(i + 1) % m}" for i in range(m)])
        expect(f"sample {c['id']} cycle of {m} vertices", obb(c["id"], good), "does not improve,")
        m2 = 2 * d + 3
        bad = write(f"{c['id']}_red.txt", [f"{i} {(i + 1) % m2}" for i in range(m2)])
        expect(f"red   {c['id']} (cycle of {m2} vertices, diameter {d + 1})", obb(c["id"], bad), "NOT CERTIFIED,")


def test_job_shop(n, rng, family="job-shop", flexible=False):
    """A greedy schedule (operations placed job by job, each at the earliest time after its job's previous operation
    and after everything already on its machine; for the flexible shop the first machine listed): valid and longer
    than the best known; with one start time moved one unit earlier it must be refused. Cells whose instance file is
    not under instances/ (fetch.sh) are skipped."""
    cells = [c for c in family_cells(family) if os.path.exists(os.path.join(ROOT, c["params"]["file"]))]
    if not cells:
        print(f"skip  {family}: no instance files under instances/ (run fetch.sh)")
        return
    for c in rng.sample(cells, min(n, len(cells))):
        lines = [l for l in open(os.path.join(ROOT, c["params"]["file"])) if l.strip()]
        nj = int(lines[0].split()[0])
        free, out = {}, []
        for j in range(nj):
            v = [int(x) for x in lines[1 + j].split()]
            ops = []
            if flexible:
                pos = 1
                for _ in range(v[0]):
                    k = v[pos]
                    ops.append((v[pos + 1], v[pos + 2]))
                    pos += 1 + 2 * k
            else:
                ops = [(v[2 * o], v[2 * o + 1]) for o in range(len(v) // 2)]
            t, row = 0, []
            for mach, dur in ops:
                st = max(t, free.get(mach, 0))
                row += [mach, st] if flexible else [st]
                t = st + dur
                free[mach] = t
            out.append(row)
        good = write(f"{c['id']}.txt", [" ".join(map(str, r)) for r in out])
        expect(f"sample {c['id']} greedy schedule", obb(c["id"], good), "does not improve,")
        bad_rows = [r[:] for r in out]
        last = len(bad_rows[-1]) - 1                     # the last operation of the last job, one unit earlier
        bad_rows[-1][last] -= 1
        bad = write(f"{c['id']}_red.txt", [" ".join(map(str, r)) for r in bad_rows])
        expect(f"red   {c['id']} (one start time a unit earlier)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_flexible_job_shop(n, rng):
    test_job_shop(n, rng, "flexible-job-shop", True)


def test_golomb_ruler(n, rng):
    """The first n marks of the Erdos-Turan ruler 2pk + (k^2 mod p) for the least prime p >= n: valid and longer than
    the table; with its last mark moved to repeat a difference it must be refused."""
    small = [c for c in family_cells("golomb-ruler") if c["params"]["n"] <= 5000]     # keeps the bit array small
    for c in rng.sample(small, n):
        m = c["params"]["n"]
        p = m
        while any(p % d == 0 for d in range(2, int(p ** 0.5) + 1)):
            p += 1
        marks = [2 * p * k + (k * k) % p for k in range(m)]
        good = write(f"{c['id']}.txt", [" ".join(map(str, marks))])
        expect(f"sample {c['id']} Erdos-Turan ruler", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", [" ".join(map(str, marks[:-1] + [marks[-2] + marks[1] - marks[0]]))])
        expect(f"red   {c['id']} (a difference repeated)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_strongly_regular_graph(n, rng):
    """No graph is known for any cell, so the green control is the checker on known graphs: the Paley graph P(q) and
    the triangular graph T(s) with their parameters, and the same graphs with one edge moved refused. For each drawn
    cell, a k-regular circulant graph on v vertices (k-regular, but not strongly regular) must be refused."""
    chk = os.path.join(CHECKERS, "srg_check.py")

    def run(v, k, l, m, edges, name):
        path = write(name, [f"{a} {b}" for a, b in edges])
        r = subprocess.run([sys.executable, "-I", chk, str(v), str(k), str(l), str(m), path], capture_output=True,
                           text=True)
        return r.returncode

    for q in (13, 29, 37):
        sq = {x * x % q for x in range(1, q)}
        edges = [(a, b) for a in range(q) for b in range(a + 1, q) if (b - a) % q in sq]
        expect(f"checker: Paley graph P({q})", run(q, (q - 1) // 2, (q - 5) // 4, (q - 1) // 4, edges, f"paley{q}.txt"), 0)
        a, b = edges[0]
        c = next(x for x in range(q) if x not in (a, b) and (a, x) not in edges and (x, a) not in edges)
        moved = edges[1:] + [tuple(sorted((a, c)))]
        expect(f"checker: P({q}) with one edge moved (red)", run(q, (q - 1) // 2, (q - 5) // 4, (q - 1) // 4, moved,
                                                                f"paley{q}_red.txt"), 1)
    for s in (6, 9):
        pairs = list(itertools.combinations(range(s), 2))
        edges = [(i, j) for i, j in itertools.combinations(range(len(pairs)), 2) if set(pairs[i]) & set(pairs[j])]
        v = len(pairs)
        expect(f"checker: triangular graph T({s})", run(v, 2 * (s - 2), s - 2, 4, edges, f"tri{s}.txt"), 0)
    small = [c for c in family_cells("strongly-regular-graph") if c["params"]["v"] <= 400]
    for c in rng.sample(small, min(n, len(small))):
        v, k = c["params"]["v"], c["params"]["k"]
        offs = list(range(1, k // 2 + 1))
        edges = sorted({tuple(sorted((x, (x + o) % v))) for x in range(v) for o in offs})
        if k % 2:                                  # v is even when k is odd: add the antipodal matching
            edges += [(x, x + v // 2) for x in range(v // 2)]
        bad = write(f"{c['id']}_red.txt", [f"{a} {b}" for a, b in edges])
        expect(f"red   {c['id']} (a {k}-regular circulant on {v} vertices)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_difference_set(n, rng):
    """No set is known for any cell (tests/test_ds.py passes known sets through the checker); for each drawn cell a
    random set of k elements of the group, written in the cell's coordinates, must be refused, and so must the same
    set with one element repeated."""
    small = [c for c in family_cells("difference-set") if c["params"]["v"] <= 5000]
    for c in rng.sample(small, min(n, len(small))):
        p = c["params"]
        orders = [int(x) for x in p["orders"].split(",")]
        elems = set()
        while len(elems) < p["k"]:
            elems.add(tuple(rng.randrange(m) for m in orders))
        lines = [" ".join(map(str, e)) for e in sorted(elems)]
        bad = write(f"{c['id']}_red.txt", lines)
        expect(f"red   {c['id']} (a random {p['k']}-subset of {p['group']})", obb(c["id"], bad), "NOT CERTIFIED,")
        bad = write(f"{c['id']}_red2.txt", lines[:-1] + lines[:1])
        expect(f"red   {c['id']} (an element repeated)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_signed_difference_set(n, rng):
    """No set is known for any cell (tests/test_ds.py passes known signed sets); for each drawn cell k random elements
    with as many signs + as the parameters require must be refused."""
    cells = family_cells("signed-difference-set")
    for c in rng.sample(cells, min(n, len(cells))):
        p = c["params"]
        orders = [int(x) for x in p["orders"].split(",")]
        v, k, lam = p["v"], p["k"], p["l"]
        d = round(((k - lam) + lam * v) ** 0.5)
        plus = (k + d) // 2
        elems = set()
        while len(elems) < k:
            elems.add(tuple(rng.randrange(m) for m in orders))
        lines = [("+ " if i < plus else "- ") + " ".join(map(str, e)) for i, e in enumerate(sorted(elems))]
        bad = write(f"{c['id']}_red.txt", lines)
        expect(f"red   {c['id']} (a random signed {k}-subset of {p['group']})", obb(c["id"], bad), "NOT CERTIFIED,")


def test_circulant_degree_diameter(n, rng):
    """C_N(1, ..., m) with m = floor(d/2) and N = 2mk + 1 has degree 2m <= d and diameter k: valid and smaller than
    the table; with N = 2mk + 2m + 1 its diameter is k + 1 and it must be refused."""
    cells = family_cells("circulant-degree-diameter")
    for c in rng.sample(cells, min(n, len(cells))):
        d, k = c["params"]["d"], c["params"]["k"]
        m = d // 2
        good = write(f"{c['id']}.txt", [str(2 * m * k + 1), " ".join(map(str, range(1, m + 1)))])
        expect(f"sample {c['id']} C_{2 * m * k + 1}(1..{m})", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", [str(2 * m * k + 2 * m + 1), " ".join(map(str, range(1, m + 1)))])
        expect(f"red   {c['id']} (diameter {k + 1})", obb(c["id"], bad), "NOT CERTIFIED,")


def test_bipartite_degree_diameter(n, rng):
    """The even cycle C_2k is bipartite with degree 2 and diameter k: valid and smaller than the table; the odd cycle
    C_(2k+1) has diameter k but is not bipartite and must be refused."""
    cells = family_cells("bipartite-degree-diameter")
    for c in rng.sample(cells, min(n, len(cells))):
        k = c["params"]["k"]
        good = write(f"{c['id']}.txt", [f"{i} {(i + 1) % (2 * k)}" for i in range(2 * k)])
        expect(f"sample {c['id']} the cycle C_{2 * k}", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", [f"{i} {(i + 1) % (2 * k + 1)}" for i in range(2 * k + 1)])
        expect(f"red   {c['id']} (the odd cycle C_{2 * k + 1})", obb(c["id"], bad), "NOT CERTIFIED,")


def test_circulant_weighing_matrix(n, rng):
    """No proper matrix is known for any cell; test.sh passes the circulant Hadamard matrix of order 4 through the
    checker and refuses an improper CW(8,4). For each drawn cell a random first row with s(s+1)/2 entries +1 and
    s(s-1)/2 entries -1 must be refused, and so must the all-zero row."""
    cells = family_cells("circulant-weighing-matrix")
    for c in rng.sample(cells, min(n, len(cells))):
        p = c["params"]
        s, size = p["s"], p["n"]
        pos = rng.sample(range(size), s * s)
        row = [0] * size
        for i, x in enumerate(pos):
            row[x] = 1 if i < s * (s + 1) // 2 else -1
        bad = write(f"{c['id']}_red.txt", [" ".join(map(str, row))])
        expect(f"red   {c['id']} (a random row of weight {s * s})", obb(c["id"], bad), "NOT CERTIFIED,")
        bad = write(f"{c['id']}_red0.txt", [" ".join(["0"] * size)])
        expect(f"red   {c['id']} (the zero row)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_constant_weight_code(n, rng):
    import math
    small = [c for c in family_cells("constant-weight-code")
             if math.comb(c["params"]["n"], c["params"]["w"]) <= 20000]
    for c in rng.sample(small, min(n, len(small))):
        p = c["params"]
        words = greedy_cw(p["n"], p["d"], p["w"])
        lines = [" ".join(map(str, x)) for x in words]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} lexicographic code ({len(words)} words)", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines + [lines[0]])
        expect(f"red   {c['id']} (a word repeated)", obb(c["id"], bad), "NOT CERTIFIED,")


def serial_schedule(n, caps, dur, dem, succ):
    """Serial schedule generation in topological order: each activity at the earliest time that fits."""
    pred = [[] for _ in range(n)]
    for i in range(n):
        for j in succ[i]:
            pred[j].append(i)
    order, indeg = [], [len(p) for p in pred]
    ready = [i for i in range(n) if indeg[i] == 0]
    while ready:
        i = ready.pop(0)
        order.append(i)
        for j in succ[i]:
            indeg[j] -= 1
            if indeg[j] == 0:
                ready.append(j)
    horizon = sum(dur) + 1
    use = [[0] * len(caps) for _ in range(horizon + max(dur) + 1)]
    start = [0] * n
    for i in order:
        s = max([start[p] + dur[p] for p in pred[i]] + [0])
        while any(use[x][r] + dem[i][r] > caps[r] for x in range(s, s + dur[i]) for r in range(len(caps))):
            s += 1
        start[i] = s
        for x in range(s, s + dur[i]):
            for r in range(len(caps)):
                use[x][r] += dem[i][r]
    return start


def run_rcpsp(args):
    r = subprocess.run([sys.executable, "-I", os.path.join(CHECKERS, "rcpsp_check.py")] + args,
                       capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    return r.returncode, last


def test_project_scheduling(n, rng):
    # the checker on generated instances, in the three formats it reads
    for trial in range(3):
        real, r = rng.randint(6, 12), 2
        N = real + 2
        dur = [0] + [rng.randint(1, 6) for _ in range(real)] + [0]
        caps = [rng.randint(4, 8) for _ in range(r)]
        dem = [[0] * r] + [[rng.randint(0, c) for c in caps] for _ in range(real)] + [[0] * r]
        succ = [[] for _ in range(N)]
        for i in range(1, real + 1):
            later = list(range(i + 1, real + 1))
            succ[i] = sorted(set(rng.sample(later, min(len(later), rng.randint(0, 2)))))
        has_pred = {j for i in range(1, real + 1) for j in succ[i]}
        succ[0] = [i for i in range(1, real + 1) if i not in has_pred]
        for i in range(1, real + 1):
            if not succ[i]:
                succ[i] = [N - 1]
        start = serial_schedule(N, caps, dur, dem, succ)
        mk = max(s + d for s, d in zip(start, dur))
        rcp = [f"{N} {r}", " ".join(map(str, caps))] + [
            " ".join(map(str, [dur[i]] + dem[i] + [len(succ[i])] + [j + 1 for j in succ[i]])) for i in range(N)]
        sm = ["jobs (incl. supersource/sink ):  %d" % N, "  - renewable                 :  %d   R" % r, "*" * 20,
              "PRECEDENCE RELATIONS:", "jobnr.    #modes  #successors   successors"] + [
            f"  {i + 1}  1  {len(succ[i])}  " + " ".join(str(j + 1) for j in succ[i]) for i in range(N)] + [
            "*" * 20, "REQUESTS/DURATIONS:", "jobnr. mode duration  " + "  ".join(f"R {x + 1}" for x in range(r)),
            "-" * 20] + [f"  {i + 1}  1  {dur[i]}  " + "  ".join(map(str, dem[i])) for i in range(N)] + [
            "*" * 20, "RESOURCEAVAILABILITIES:", "  ".join(f"R {x + 1}" for x in range(r)),
            "  ".join(map(str, caps)), "*" * 20]
        net = [f"{N} {r}", " ".join(["10"] * r)] + [
            " ".join(map(str, [dur[i]] + [10] * r + [len(succ[i])] + [j + 1 for j in succ[i]])) for i in range(N)]
        res = ["generated for the test", "File number 1", "Resource availability:", "\t".join(map(str, caps)),
               "Resource demand (1 line per activity):"] + ["\t".join(map(str, dem[i])) for i in range(1, N - 1)]
        files = {x: write(f"rcpsp_gen{trial}.{x}", lines) for x, lines in
                 (("rcp", rcp), ("sm", sm), ("net", net), ("res", res))}
        good = write(f"rcpsp_gen{trial}_schedule.txt", [";".join(map(str, start))])
        for fmt, args in (("rcp", [files["rcp"]]), ("sm", [files["sm"]]),
                          ("rcp+res", [files["net"], files["res"], "1"])):
            expect(f"unit  rcpsp_check {fmt} generated instance {trial} (serial schedule)",
                   run_rcpsp([fmt] + args + [good]), (0, f"RESULT {mk}"))
        # red controls: an activity moved before its predecessor finishes; a resource over its capacity
        pairs = [(i, j) for i in range(1, N - 1) for j in succ[i] if j < N - 1 and dur[i] > 0]
        if pairs:
            i, j = pairs[0]
            early = list(start)
            early[j] = start[i]
            bad = write(f"rcpsp_gen{trial}_red_precedence.txt", [" ".join(map(str, early))])
            expect(f"red   rcpsp_check generated instance {trial} (activity {j + 1} before its predecessor ends)",
                   run_rcpsp(["rcp", files["rcp"], bad])[0], 1)
    caps, dur, dem = [3], [0, 2, 2, 0], [[0], [2], [2], [0]]
    succ = [[1, 2], [3], [3], []]
    rcp = write("rcpsp_unit.rcp", ["4 1", "3"] + [" ".join(map(str, [dur[i]] + dem[i] + [len(succ[i])] +
                                                                     [j + 1 for j in succ[i]])) for i in range(4)])
    expect("unit  rcpsp_check two activities in turn", run_rcpsp(["rcp", rcp, write("u1.txt", ["0 0 2 4"])]),
           (0, "RESULT 4"))
    expect("red   rcpsp_check two activities at once (demand 4 > capacity 3)",
           run_rcpsp(["rcp", rcp, write("u2.txt", ["0 0 0 2"])])[0], 1)
    expect("red   rcpsp_check the last activity before its predecessor ends",
           run_rcpsp(["rcp", rcp, write("u3.txt", ["0 0 2 3"])])[0], 1)
    # cells of the family, when their instance files are present
    inst = os.path.join(ROOT, "instances", "rcpsp")

    def files(c):
        p = c["params"]
        if c.get("variant") == "netres":
            return [os.path.join(inst, "NetRes", "MT30", p["file"]), os.path.join(inst, "NetRes", "ResSet", p["resources"])]
        return [os.path.join(inst, p["set"], p["file"])]

    have = [c for c in family_cells("project-scheduling") if all(os.path.exists(f) for f in files(c))]
    if not have:
        print("skip  project-scheduling cells: no instance files under instances/rcpsp/ (see the family's 'instances')")
        return
    sys.path.insert(0, CHECKERS)
    import rcpsp_check
    for c in rng.sample(have, min(n, len(have))):
        paths = files(c)
        if c.get("variant") == "netres":
            N, _, dur, _, succ = rcpsp_check.read_rcp(paths[0])
            caps, real = rcpsp_check.read_profile(paths[1], c["params"]["profile"])
            dem = [[0] * len(caps)] + real + [[0] * len(caps)]
        elif c.get("variant") == "sm":
            N, caps, dur, dem, succ = rcpsp_check.read_sm(paths[0])
        else:
            N, caps, dur, dem, succ = rcpsp_check.read_rcp(paths[0])
        start = serial_schedule(N, caps, dur, dem, succ)
        good = write(f"{c['id']}.txt", [" ".join(map(str, start))])
        expect(f"sample {c['id']} serial schedule", obb(c["id"], good), "does not improve,")


def test_circle_packing(n, rng):
    """Equal circles (balls) on a grid inside a box that lies in the container, radius half the grid step: valid and
    below the table; the same packing with one centre repeated must be refused."""
    import math
    from fractions import Fraction as Fr
    boxes = {"csq": (0, 1), "scu": (0, 1), "cci": (Fr(-1, 4), Fr(1, 4)), "ssp": (Fr(-1, 4), Fr(1, 4)),
             "hsp4": (Fr(-1, 4), Fr(1, 4)), "hsp5": (Fr(-1, 4), Fr(1, 4)), "hsp6": (Fr(-1, 4), Fr(1, 4)),
             "ccq": (Fr(1, 4), Fr(1, 2)), "crt": (Fr(1, 8), Fr(3, 8))}
    boxes.update({f"crc{h}00": (0, Fr(h, 10)) for h in range(1, 9)})     # a square of side h in the 1 x h rectangle
    dims = {"csq": 2, "cci": 2, "csc": 2, "ccq": 2, "crt": 2, "scu": 3, "ssp": 3, "hsp4": 4, "hsp5": 5, "hsp6": 6}
    dims.update({f"crc{h}00": 2 for h in range(1, 9)})
    cells = [c for c in family_cells("circle-packing") if c["params"]["n"] <= 300]
    rect = [c for c in cells if c["params"]["section"].startswith("crc")]
    for c in rng.sample(cells, min(n + 2, len(cells))) + rng.sample(rect, min(2, len(rect))):
        sec, N = c["params"]["section"], c["params"]["n"]
        d = dims[sec]
        k = 1
        while k ** d < N:
            k += 1
        if sec == "csc":
            lo = [Fr(-1, 4), Fr(1, 4)]; side = Fr(1, 4)
        else:
            a, b = boxes[sec]; lo = [Fr(a)] * d; side = Fr(b) - Fr(a)
        r = side / (2 * k)
        pts = []
        for idx in itertools.product(range(k), repeat=d):
            if len(pts) == N:
                break
            pts.append([lo[j] + (2 * idx[j] + 1) * r for j in range(d)])
        def num(x):
            return f"{x.numerator / x.denominator:.30f}" if x.denominator & (x.denominator - 1) else str(x.numerator / x.denominator)
        def dec(x):
            q, rem = divmod(abs(x.numerator) * 10 ** 40, x.denominator)
            s = str(q).zfill(41)
            return ("-" if x < 0 else "") + s[:-40] + "." + s[-40:]
        rr = Fr(int(r * 10 ** 40), 10 ** 40)          # rounded down: still a valid radius
        lines = [dec(rr)] + [" ".join(dec(x) for x in p) for p in pts]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} grid of {N}", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines[:-1] + [lines[1]])
        expect(f"red   {c['id']} (a centre repeated)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_growing_circle_packing(n, rng):
    """Circles of radii 1..N in a row along a diameter (or along the middle of the square): valid and far above the
    table; the container shrunk by one must be refused."""
    grow = family_cells("growing-circle-packing")
    for c in rng.sample(grow, n) + rng.sample([c for c in grow if c["params"]["section"] == "sspn"], 1):
        sec, N = c["params"]["section"], c["params"]["n"]
        L = N * (N + 1)
        xs, x = [], 0
        for i in range(1, N + 1):
            xs.append(x + i)
            x += 2 * i
        if sec in ("ccin", "sspn"):
            V = L // 2
            pts = [(xi - V, 0) + ((0,) if sec == "sspn" else ()) for xi in xs]
        else:
            V = max(L, 2 * N)
            pts = [(xi, N) for xi in xs]
        lines = [str(V)] + [" ".join(map(str, p)) for p in pts]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} circles in a row", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", [str(V - 1)] + lines[1:])
        expect(f"red   {c['id']} (container shrunk by 1)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_circle_packing_sum(n, rng):
    """N equal circles on a grid in the unit square (radius half the step): valid, and its sum of radii is below the
    table; a radius enlarged so that two circles overlap must be refused."""
    for c in rng.sample(family_cells("circle-packing-sum"), n):
        N = c["params"]["n"]
        k = 1
        while k * k < N:
            k += 1
        r = 1 / (2 * k)
        pts = [((2 * i + 1) * r, (2 * j + 1) * r) for i in range(k) for j in range(k)][:N]
        lines = [f"{x:.12f} {y:.12f} {r * 0.999999:.12f}" for x, y in pts]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} grid of {N} equal circles", obb(c["id"], good), "does not improve,")
        x, y = pts[0]
        bad = write(f"{c['id']}_red.txt", [f"{x:.12f} {y:.12f} {r * 1.000001:.12f}"] + lines[1:])
        expect(f"red   {c['id']} (one radius too large)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_polygon_circle_packing(n, rng):
    """Equal circles on a k x k grid in the square [-a/2, a/2]^2 (a = the apothem, so the square lies in the incircle):
    valid and below the table; a centre repeated must be refused."""
    from fractions import Fraction as Fr
    for c in rng.sample(family_cells("polygon-circle-packing"), n):
        sec, N = c["params"]["section"], c["params"]["n"]
        sides = {"cpt": 5, "chx": 6, "chp": 7, "coc": 8, "cno": 9, "cdc": 10, "chd": 11, "cdd": 12, "ctd": 13,
                 "crd": 14, "cpd": 15, "cxd": 16, "ced": 17}[sec]
        a = Fr(int(math.cos(math.pi / sides) * 10 ** 9) - 10, 10 ** 9)          # below the apothem
        k = 1
        while k * k < N:
            k += 1
        h = a / 2
        r = h / k
        pts = [(-h + (2 * i + 1) * r, -h + (2 * j + 1) * r) for i in range(k) for j in range(k)][:N]

        def dec(x):
            q = x.numerator * 10 ** 30 // x.denominator if x >= 0 else -((-x.numerator) * 10 ** 30 // x.denominator)
            sgn = "-" if q < 0 else ""
            st = str(abs(q)).rjust(31, "0")
            return sgn + st[:-30] + "." + st[-30:]
        rr = Fr(int(r * 10 ** 30), 10 ** 30)
        lines = [dec(rr)] + [f"{dec(x)} {dec(y)}" for x, y in pts]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} grid of {N} in the regular {sides}-gon", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines[:-1] + [lines[1]])
        expect(f"red   {c['id']} (a centre repeated)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_unequal_circle_packing(n, rng):
    """Circles i = 1..N in a row, spaced by upper bounds of their radii, in a container with room to spare: valid and
    far above the table; the container shrunk to a third must be refused."""
    for c in rng.sample(family_cells("unequal-circle-packing"), n):
        sec, N = c["params"]["section"], c["params"]["n"]
        expo = {"ccir": 0.5, "ccis": -0.5, "ccic": -2 / 3, "ccib": -0.2, "csqr": 0.5, "csqs": 0.5}[sec]
        rad = [((N / i) if sec == "csqs" else i) ** expo for i in range(1, N + 1)]
        ub = [math.ceil(x * 10 ** 6 + 1) / 10 ** 6 for x in rad]
        L = sum(2 * u for u in ub)
        xs, x = [], 0.0
        for u in ub:
            xs.append(x + u)
            x += 2 * u
        if sec.startswith("cci"):
            V = math.ceil(L / 2) + 1
            pts = [(xi - L / 2, 0.0) for xi in xs]
        else:
            V = math.ceil(max(L, 2 * max(ub))) + 1
            pts = [(xi, max(ub)) for xi in xs]
        lines = [str(V)] + [f"{px:.7f} {py:.7f}" for px, py in pts]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} circles in a row", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", [f"{V / 3:.6f}"] + lines[1:])
        expect(f"red   {c['id']} (container shrunk to a third)", obb(c["id"], bad), "NOT CERTIFIED,")


def test_grassmannian_packing(n, rng):
    small = [c for c in family_cells("grassmannian-packing") if c["params"]["N"] <= 60]
    for c in rng.sample(small, min(n, len(small))):
        m, k, cnt = c["params"]["m"], c["params"]["n"], c["params"]["N"]
        lines = [" ".join(f"{rng.gauss(0, 1):.12f}" for _ in range(m)) for _ in range(cnt * k)]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} random subspaces", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", lines[:-1])
        expect(f"red   {c['id']} (a vector too few)", obb(c["id"], bad), "NOT CERTIFIED,")
    # nine lines in R^4 (the rows of a Hadamard matrix of order 4, the coordinate axes, a row repeated): a valid
    # packing whose closest pair is at distance 0, certified and not an improvement
    c = next((c for c in family_cells("grassmannian-packing") if c["params"] == {"m": 4, "n": 1, "N": 9}), None)
    if c:
        cube4 = ["1 1 1 1", "1 1 -1 -1", "1 -1 1 -1", "1 -1 -1 1", "1 0 0 0", "0 1 0 0", "0 0 1 0", "0 0 0 1",
                 "1 1 1 1"]
        expect("red   grass-4-1-9: a line repeated (distance 0)", obb(c["id"], write("grass-4-1-9_rep.txt", cube4)),
               "does not improve,")


def test_complete_arc(n, rng):
    """A conic (q odd) or a conic with its nucleus (q even) is a complete arc of q + 1 or q + 2 points: certified, far
    above the table; with a point removed it is not complete and must be refused. Fields GF(p^h) are given by the
    first irreducible polynomial found."""
    sys.path.insert(0, CHECKERS)
    import arc_check
    cells = family_cells("complete-arc")
    picks = rng.sample([c for c in cells if c["params"]["h"] == 1 and c["params"]["q"] <= 700], n)
    picks += rng.sample([c for c in cells if c["params"]["h"] > 1 and c["params"]["q"] <= 1000], 1)
    for c in picks:
        q, p, h = c["params"]["q"], c["params"]["p"], c["params"]["h"]
        head, poly = [], None
        if h > 1:
            poly = next(f for f in ([k % p ** (i + 1) // p ** i for i in range(h)] + [1] for k in range(1, p ** h))
                        if f[0] and arc_check.irreducible(f, p))
            head = ["poly " + " ".join(map(str, poly))]
        F = arc_check.Field(q, p, h, poly)
        pts = [(1, t, F.mul(t, t)) for t in range(q)] + [(0, 0, 1)] + ([(0, 1, 0)] if p == 2 else [])
        lines = head + [f"{x} {y} {z}" for x, y, z in pts]
        expect(f"sample {c['id']} {'conic' if p > 2 else 'hyperoval'} of {len(pts)} points",
               obb(c["id"], write(f"{c['id']}.txt", lines)), "does not improve,")
        expect(f"red   {c['id']} (a point removed)", obb(c["id"], write(f"{c['id']}_red.txt", head + lines[len(head) + 1:])),
               "NOT CERTIFIED,")


def test_mols(n, rng):
    """For odd n the squares i + j and 2i + j mod n are orthogonal: certified (2 squares, below every cell's value);
    with the second square a copy of the first they are refused."""
    for c in rng.sample([c for c in family_cells("mols") if c["params"]["n"] % 2 and c["params"]["n"] <= 801], n):
        m = c["params"]["n"]
        sq = [[" ".join(str((a * i + j) % m) for j in range(m)) for i in range(m)] for a in (1, 2)]
        expect(f"sample {c['id']} the squares i + j and 2i + j", obb(c["id"], write(f"{c['id']}.txt", sq[0] + sq[1])),
               "does not improve,")
        expect(f"red   {c['id']} (a square repeated)", obb(c["id"], write(f"{c['id']}_red.txt", sq[0] + sq[0])),
               "NOT CERTIFIED,")
    # large orders: a product difference matrix over the prime-power factors (rows i < the smallest prime, entries
    # i c mod n_l in each factor), certified with (smallest prime - 2) squares; a row repeated is refused
    for c in rng.sample([c for c in family_cells("mols") if c["params"]["n"] % 2 and c["params"]["n"] > 3200], n):
        m, orders, primes, r = c["params"]["n"], [], [], c["params"]["n"]
        d = 2
        while r > 1:
            if r % d == 0:
                o = 1
                while r % d == 0:
                    r //= d
                    o *= d
                orders.append(o)
                primes.append(d)
            d += 1
        rows = []
        for i in range(min(primes)):
            row = []
            for col in range(m):
                x, w, cc = 0, 1, col
                for o in orders:
                    x += (i * (cc % o) % o) * w
                    cc //= o
                    w *= o
                row.append(str(x))
            rows.append(" ".join(row))
        head = "group " + " ".join(map(str, orders))
        expect(f"sample {c['id']} a product difference matrix over {orders}",
               obb(c["id"], write(f"{c['id']}_dm.txt", [head] + rows)), "does not improve,")
        expect(f"red   {c['id']} (a row of the matrix repeated)",
               obb(c["id"], write(f"{c['id']}_dm_red.txt", [head] + rows + [rows[1]])), "NOT CERTIFIED,")


def test_cayley_degree_diameter(n, rng):
    """The cycle Cay(Z_(2k+1), {1, -1}) (degree 2, diameter k) for the cell's diameter k: certified and far below the
    table; with the inverse of 1 left out the set is refused."""
    for c in rng.sample(family_cells("cayley-degree-diameter"), n):
        k = c["params"]["k"]
        m = 2 * k + 1
        gens = [[(x + 1) % m for x in range(m)], [(x - 1) % m for x in range(m)]]
        lines = [f"points {m}"] + [" ".join(map(str, g)) for g in gens]
        expect(f"sample {c['id']} the cycle Cay(Z_{m}, {{1, -1}})", obb(c["id"], write(f"{c['id']}.txt", lines)),
               "does not improve,")
        expect(f"red   {c['id']} (the inverse of 1 left out)", obb(c["id"], write(f"{c['id']}_red.txt", lines[:2])),
               "NOT CERTIFIED,")


def test_multi_mode_scheduling(n, rng):
    """With the MMLIB instances under instances/mmrcpsp/ (not in the repository): every activity in its mode of least
    nonrenewable demand, the activities one after the other: feasible when those modes fit the nonrenewable
    capacities (an independent sum here predicts the verdict), far above the best known makespan; every start at 0 is
    refused."""
    base = os.path.join(ROOT, "instances", "mmrcpsp")
    if not os.path.isdir(base):
        print("skip  multi-mode-scheduling: no instances under instances/mmrcpsp/")
        return
    sys.path.insert(0, CHECKERS)
    import rcpsp_check
    for c in rng.sample(family_cells("multi-mode-scheduling"), n):
        inst = os.path.join(base, c["params"]["set"], c["params"]["file"])
        if not os.path.exists(inst):
            print(f"skip  {c['id']}: {inst} missing")
            continue
        nn, rcap, ncap, succ, modes = rcpsp_check.read_mm(inst)
        pick = [min(range(len(modes[j])), key=lambda m: sum(modes[j][m][2])) + 1 for j in range(nn)]
        starts, t = [], 0
        for j in range(nn):
            starts.append(t)
            t += modes[j][pick[j] - 1][0]
        fits = all(sum(modes[j][pick[j] - 1][2][k] for j in range(nn)) <= ncap[k] for k in range(len(ncap))) and all(
            all(x <= cap for x, cap in zip(modes[j][pick[j] - 1][1], rcap)) for j in range(nn))
        want = "does not improve," if fits else "NOT CERTIFIED,"
        expect(f"sample {c['id']} a chain in least-nonrenewable modes", obb(c["id"], write(f"{c['id']}.txt", [" ".join(
            map(str, pick + starts))])), want)
        expect(f"red   {c['id']} (every start at 0)", obb(c["id"], write(f"{c['id']}_red.txt", [" ".join(
            map(str, pick + [0] * nn))])), "NOT CERTIFIED,")


def test_mslib_scheduling(n, rng):
    """With the MSLIB instances under instances/mslib/ (not in the repository): the activities one after the other, each
    with its skill requirements matched to resources mastering them (augmenting paths), is feasible and far above the
    best known makespan; with every start at 0 it is refused."""
    base = os.path.join(ROOT, "instances", "mslib")
    if not os.path.isdir(base):
        print("skip  mslib-scheduling: no instances under instances/mslib/")
        return
    sys.path.insert(0, CHECKERS)
    import msrcpsp_check
    for c in rng.sample(family_cells("mslib-scheduling"), n):
        nact, nres, ns, dur, succ, work, req = msrcpsp_check.read_instance(
            os.path.join(base, c["params"]["set"], c["params"]["file"]))
        lines, t = [], 0
        for i in range(nact):
            slots = [k for k in range(ns) for _ in range(req[i][k])]
            match = {}

            def augment(slot, seen):
                for r in range(nres):
                    if work[r][slots[slot]] and r not in seen:
                        seen.add(r)
                        if r not in match or augment(match[r], seen):
                            match[r] = slot
                            return True
                return False
            assert all(augment(x, set()) for x in range(len(slots)))
            lines.append(f"{t} " + " ".join(f"{r + 1}:{slots[x] + 1}" for r, x in match.items()))
            t += dur[i]
        expect(f"sample {c['id']} activities one after the other", obb(c["id"], write(f"{c['id']}.txt", lines)),
               "does not improve,")
        zero = ["0 " + l.split(" ", 1)[1] if " " in l else "0" for l in lines]
        expect(f"red   {c['id']} (every start at 0)", obb(c["id"], write(f"{c['id']}_red.txt", zero)), "NOT CERTIFIED,")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    os.makedirs(OUT, exist_ok=True)
    rng = random.Random(seed)
    for name, test in (("covering-design", test_covering_design), ("covering-array", test_covering_array),
                       ("spherical-code", test_spherical_code), ("linear-code", test_linear_code),
                       ("constant-weight-code", test_constant_weight_code),
                       ("project-scheduling", test_project_scheduling),
                       ("ordered-orthogonal-array", test_ordered_orthogonal_array),
                       ("circle-packing", test_circle_packing),
                       ("growing-circle-packing", test_growing_circle_packing),
                       ("quantum-code", test_quantum_code),
                       ("quantum-code", test_quantum_code_search),
                       ("circle-packing-sum", test_circle_packing_sum),
                       ("polygon-circle-packing", test_polygon_circle_packing),
                       ("ea-quantum-code", test_ea_quantum_code),
                       ("unrestricted-code", test_unrestricted_code),
                       ("orthogonal-array", test_orthogonal_array),
                       ("lj-cluster", test_lj_cluster),
                       ("degree-diameter", test_degree_diameter),
                       ("job-shop", test_job_shop),
                       ("golomb-ruler", test_golomb_ruler),
                       ("strongly-regular-graph", test_strongly_regular_graph),
                       ("difference-set", test_difference_set),
                       ("circulant-weighing-matrix", test_circulant_weighing_matrix),
                       ("signed-difference-set", test_signed_difference_set),
                       ("circulant-degree-diameter", test_circulant_degree_diameter),
                       ("bipartite-degree-diameter", test_bipartite_degree_diameter),
                       ("flexible-job-shop", test_flexible_job_shop),
                       ("unequal-circle-packing", test_unequal_circle_packing),
                       ("grassmannian-packing", test_grassmannian_packing),
                       ("complete-arc", test_complete_arc),
                       ("mols", test_mols),
                       ("multi-mode-scheduling", test_multi_mode_scheduling),
                       ("cayley-degree-diameter", test_cayley_degree_diameter),
                       ("mslib-scheduling", test_mslib_scheduling)):
        if os.path.exists(os.path.join(ROOT, "families", name, "cells.jsonl")):
            test(n, rng)
        else:
            print(f"FAIL  family {name}: no cells")
            failures.append(name)
    print(f"sampled cells: {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
