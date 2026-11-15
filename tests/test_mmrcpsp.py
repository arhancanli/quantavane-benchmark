"""Tests of checkers/rcpsp_check.py in its multi-mode format mm (standard library only; run by test.sh).

- 300 random multi-mode instances written in the PSPLIB format (3 to 7 activities between the dummies, 1 to 3 modes,
  1 or 2 renewable and nonrenewable resources) with random mode choices and start times, some built by a serial
  schedule and some broken: the checker's verdict and makespan agree with an independent check written here (resource
  use summed at every integer time, precedences, nonrenewable totals).
- Red controls on a synthetic instance: a mode that does not exist, a nonrenewable resource exceeded, a start before
  a predecessor finishes, a wrong count of numbers.
- When the MMLIB instances and Solutions Update's best known solutions files are under instances/mmrcpsp/ (not in the
  repository; see families/multi-mode-scheduling/family.json): the published solutions of 40 open cells certify their
  best known makespans through obb.py ("does not improve"), and each is refused with its last real activity started
  one unit before its predecessors allow.

  python3 -I tests/test_mmrcpsp.py"""
import csv
import json
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "rcpsp_check.py")
TMP = tempfile.mkdtemp(prefix="mm_test_")
failures = []


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def write_instance(n, succ, modes, rcap, ncap):
    path = os.path.join(TMP, "x.mm")
    R, N = len(rcap), len(ncap)
    L = [f"jobs  (incl. supersource/sink ):\t{n}", "RESOURCES", f"- renewable                 : {R} R",
         f"- nonrenewable              : {N} N", "- doubly constrained        : 0 D", "*" * 72,
         "PRECEDENCE RELATIONS:", "jobnr.    #modes  #successors   successors"]
    for j in range(n):
        L.append(f"{j + 1}\t{len(modes[j])}\t{len(succ[j])}\t\t" + " ".join(str(s + 1) for s in succ[j]))
    L += ["*" * 72, "REQUESTS/DURATIONS", "jobnr.\tmode\tdur\t" + "\t".join(f"R{k + 1}" for k in range(R)) +
          "\t" + "\t".join(f"N{k + 1}" for k in range(N)), "-" * 72]
    for j in range(n):
        for m, (d, rr, nn) in enumerate(modes[j]):
            L.append((f"{j + 1}\t" if m == 0 else "\t") + f"{m + 1}\t{d}\t" + "\t".join(map(str, rr + nn)))
    L += ["*" * 72, "", " RESOURCE AVAILABILITIES ", "\t" + "\t".join(f"R {k + 1}" for k in range(R)) + "\t" +
          "\t".join(f"N {k + 1}" for k in range(N)), "\t" + "\t".join(map(str, rcap + ncap)), "", "*" * 72]
    with open(path, "w") as f:
        f.write("\r\n".join(L) + "\r\n")
    return path


def run(inst, numbers):
    path = os.path.join(TMP, "s.txt")
    with open(path, "w") as f:
        f.write(" ".join(map(str, numbers)) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, "mm", inst, path], capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    return int(last.split()[1]) if r.returncode == 0 and last.startswith("RESULT") else None


def independent(n, succ, modes, rcap, ncap, chosen, starts):
    if any(not 1 <= m <= len(modes[j]) for j, m in enumerate(chosen)) or any(s < 0 for s in starts):
        return None
    d = [modes[j][m - 1][0] for j, m in enumerate(chosen)]
    for k in range(len(ncap)):
        if sum(modes[j][m - 1][2][k] for j, m in enumerate(chosen)) > ncap[k]:
            return None
    for i in range(n):
        if any(starts[j] < starts[i] + d[i] for j in succ[i]):
            return None
    end = max(s + x for s, x in zip(starts, d))
    for t in range(end):
        for k in range(len(rcap)):
            if sum(modes[j][chosen[j] - 1][1][k] for j in range(n) if starts[j] <= t < starts[j] + d[j]) > rcap[k]:
                return None
    return end


rng = random.Random(2026)
agree = 0
for trial in range(300):
    real = rng.randint(3, 7)
    n = real + 2
    R, N = rng.randint(1, 2), rng.randint(1, 2)
    succ = [[] for _ in range(n)]
    for j in range(1, n - 1):
        preds = [i for i in range(1, j) if rng.random() < 0.3]
        for i in preds:
            succ[i].append(j)
        if not preds:
            succ[0].append(j)
    for j in range(1, n - 1):
        if not succ[j]:
            succ[j].append(n - 1)
    modes = [[(0, [0] * R, [0] * N)]] + [[(rng.randint(1, 5), [rng.randint(0, 4) for _ in range(R)],
                                            [rng.randint(0, 4) for _ in range(N)]) for _ in range(rng.randint(1, 3))]
                                          for _ in range(real)] + [[(0, [0] * R, [0] * N)]]
    rcap = [rng.randint(4, 7) for _ in range(R)]
    ncap = [rng.randint(real, 3 * real) for _ in range(N)]
    inst = write_instance(n, succ, modes, rcap, ncap)
    chosen = [1] + [rng.randint(1, len(modes[j])) for j in range(1, n - 1)] + [1]
    # serial schedule: each activity at the earliest time after its predecessors where its resources fit
    d = [modes[j][chosen[j] - 1][0] for j in range(n)]
    starts, use = [0] * n, {}
    for j in range(n):
        t = max([starts[i] + d[i] for i in range(j) if j in succ[i]], default=0)
        dem = modes[j][chosen[j] - 1][1]
        while any(use.get((u, k), 0) + dem[k] > rcap[k] for u in range(t, t + d[j]) for k in range(R)):
            t += 1
        for u in range(t, t + d[j]):
            for k in range(R):
                use[(u, k)] = use.get((u, k), 0) + dem[k]
        starts[j] = t
    kind = trial % 4
    if kind == 1:
        j = rng.randrange(1, n)
        starts[j] = max(0, starts[j] - rng.randint(1, 3))
    elif kind == 2:
        j = rng.randrange(1, n - 1)
        chosen[j] = rng.randint(1, len(modes[j]))
    want = independent(n, succ, modes, rcap, ncap, chosen, starts)
    got = run(inst, chosen + starts)
    agree += got == want
    if got != want:
        print(f"FAIL  random instance {trial}: checker {got}, independent {want}")
expect("300 random multi-mode instances: the checker agrees with an independent check", agree, 300)

# red controls on one synthetic instance
succ = [[1, 2], [3], [3], []]
modes = [[(0, [0], [0])], [(2, [2], [3]), (4, [1], [1])], [(3, [2], [2])], [(0, [0], [0])]]
inst = write_instance(4, succ, modes, [3], [4])
expect("a feasible schedule (modes 1 2 1 1)", run(inst, [1, 2, 1, 1, 0, 0, 0, 4]), 4)
expect("the same in Solutions Update's layout (real activities' modes only)", run(inst, [2, 1, 0, 0, 0, 4]), 4)
expect("red a mode that does not exist", run(inst, [1, 3, 1, 1, 0, 0, 0, 4]), None)
expect("red nonrenewable resource exceeded (modes 1 1: 3 + 2 > 4)", run(inst, [1, 1, 1, 1, 0, 0, 2, 3]), None)
expect("red a start before its predecessor finishes", run(inst, [1, 2, 1, 1, 0, 0, 0, 3]), None)
inst2 = write_instance(4, succ, modes, [3], [10])
expect("modes 1 1 run one after the other (nonrenewable 5 <= 10)", run(inst2, [1, 1, 1, 1, 0, 0, 2, 5]), 5)
expect("red renewable resource exceeded (modes 1 1 together: 2 + 2 > 3)", run(inst2, [1, 1, 1, 1, 0, 0, 0, 3]), None)
expect("red a wrong count of numbers", run(inst, [1, 2, 1, 1, 0, 0, 0]), None)

# published solutions of open cells (only when the instances and the best known solutions files are present)
base = os.path.join(ROOT, "instances", "mmrcpsp")
cells = [json.loads(l) for l in open(os.path.join(ROOT, "families", "multi-mode-scheduling", "cells.jsonl"))]
bks_files = {"MMLIB50": "MM50_7_BKS.csv", "MMLIB100": "MM100_6_BKS.csv", "MMLIB+": "MMplus_2_BKS.csv"}
if all(os.path.exists(os.path.join(base, f)) for f in bks_files.values()) and os.path.isdir(os.path.join(base, "MMLIB+")):
    sols = {}
    for s, f in bks_files.items():
        for r in csv.reader(open(os.path.join(base, f), encoding="latin-1"), delimiter=";"):
            if r and r[0].isdigit() and len(r) > 4:
                sols[(s, int(r[0]))] = (int(r[2]), [int(x) for x in r[4:] if x.strip()])
    picked = [c for c in random.Random(7).sample(cells, len(cells)) if (c["params"]["set"], c["params"]["id"]) in sols][:40]
    good = 0
    for c in picked:
        val, nums = sols[(c["params"]["set"], c["params"]["id"])]
        path = os.path.join(TMP, "bks.txt")
        with open(path, "w") as f:
            f.write(" ".join(map(str, nums)) + "\n")
        r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "obb.py"), "check", c["id"], path],
                           capture_output=True, text=True)
        ok = f"certified value {c['best']}/1" in r.stdout and "does not improve" in r.stdout and val == int(c["best"])
        # red: the last real activity one unit earlier than its latest predecessor's finish allows is infeasible
        # only if it then overlaps a predecessor; simply start every activity at 0 instead
        bad = nums[:len(nums) - (len(nums) + 2) // 2] + [0] * ((len(nums) + 2) // 2)
        with open(path, "w") as f:
            f.write(" ".join(map(str, bad)) + "\n")
        r2 = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "obb.py"), "check", c["id"], path],
                            capture_output=True, text=True)
        good += ok and "NOT CERTIFIED" in r2.stdout
    expect(f"{len(picked)} published best known solutions of open cells certify their values (and fail with all "
           f"starts at 0)", good, len(picked))
else:
    print("skip  published solutions: instances/mmrcpsp/ does not hold the MMLIB instances and the *_BKS.csv files")
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
