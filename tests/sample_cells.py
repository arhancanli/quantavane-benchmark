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
    dims = {"csq": 2, "cci": 2, "csc": 2, "ccq": 2, "crt": 2, "scu": 3, "ssp": 3, "hsp4": 4, "hsp5": 5, "hsp6": 6}
    cells = [c for c in family_cells("circle-packing") if c["params"]["n"] <= 300]
    for c in rng.sample(cells, min(n + 2, len(cells))):
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
    for c in rng.sample(family_cells("growing-circle-packing"), n):
        sec, N = c["params"]["section"], c["params"]["n"]
        L = N * (N + 1)
        xs, x = [], 0
        for i in range(1, N + 1):
            xs.append(x + i)
            x += 2 * i
        if sec == "ccin":
            V = L // 2
            pts = [(xi - V, 0) for xi in xs]
        else:
            V = max(L, 2 * N)
            pts = [(xi, N) for xi in xs]
        lines = [str(V)] + [f"{a} {b}" for a, b in pts]
        good = write(f"{c['id']}.txt", lines)
        expect(f"sample {c['id']} circles in a row", obb(c["id"], good), "does not improve,")
        bad = write(f"{c['id']}_red.txt", [str(V - 1)] + lines[1:])
        expect(f"red   {c['id']} (container shrunk by 1)", obb(c["id"], bad), "NOT CERTIFIED,")


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
                       ("growing-circle-packing", test_growing_circle_packing)):
        if os.path.exists(os.path.join(ROOT, "families", name, "cells.jsonl")):
            test(n, rng)
        else:
            print(f"FAIL  family {name}: no cells")
            failures.append(name)
    print(f"sampled cells: {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
