"""Tests of checkers/msrcpsp_check.py (the multi-skilled RCPSP, basic version; standard library only; run by test.sh).

- Random instances (300 drawn) written in the MSLIB format (4 to 9 activities between the dummies, 3 to 8 resources, 2 or 3
  skill types) with schedules from a serial schedule generator (each activity at the earliest time when a matching
  of its skill requirements to free resources exists), some of them broken (a start moved earlier, a resource
  swapped, a skill changed, a pair dropped): the checker's verdict and makespan agree with an independent check
  written here (every integer time, every resource).
- Red controls on a small instance: a resource that lacks the skill, a resource named twice, too few resources for a
  skill, a resource on two activities at once, a start before a predecessor finishes, a line missing.
- With the MSLIB instances under instances/mslib/ (not in the repository; see families/mslib-scheduling/family.json),
  the generator's schedules for 20 open cells are certified through obb.py and do not improve the best known
  makespans (MSLIB publishes values, not schedules), and every start at 0 is refused.

  python3 -I tests/test_msrcpsp.py"""
import json
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "msrcpsp_check.py")
sys.path.insert(0, os.path.join(ROOT, "checkers"))
import msrcpsp_check as MC  # noqa: E402

TMP = tempfile.mkdtemp(prefix="ms_test_")
failures = []


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def write_instance(dur, succ, work, req):
    n, nres, ns = len(dur), len(work), len(work[0])
    L = ["\\* Project Module *\\", f"{n}\t{nres}\t{ns}\t1", "", "0", "", "0", ""]
    for i in range(n):
        L.append(f"{dur[i]}\t{len(succ[i])}\t" + " ".join(str(j + 1) for j in succ[i]))
    L += ["", "\\* Workforce Module *\\"] + ["\t".join(map(str, w)) + "\t" for w in work]
    L += ["", "\\* Skill Requirements Module *\\"] + ["\t".join(map(str, r)) + "\t" for r in req]
    path = os.path.join(TMP, "x.msrcp")
    with open(path, "w") as f:
        f.write("\n".join(L) + "\n")
    return path


def write_schedule(sched):
    path = os.path.join(TMP, "s.txt")
    with open(path, "w") as f:
        for s, pairs in sched:
            f.write(str(s) + "".join(f" {r + 1}:{k + 1}" for r, k in pairs) + "\n")
    return path


def run(inst, sched, obb_id=None):
    path = write_schedule(sched)
    cmd = [sys.executable, "-I", CHECK, inst, path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    return int(last.split()[1]) if r.returncode == 0 and last.startswith("RESULT") else None


def serial_schedule(n, nres, ns, dur, succ, work, req):
    """each activity (in an order that respects precedences) at the earliest time when its skill slots can be
    matched to resources mastering them and free for its whole duration"""
    preds = [[] for _ in range(n)]
    for i in range(n):
        for j in succ[i]:
            preds[j].append(i)
    order, seen = [], set()
    while len(order) < n:
        for i in range(n):
            if i not in seen and all(p in seen for p in preds[i]):
                order.append(i)
                seen.add(i)
    start, assign, busy = [0] * n, [[] for _ in range(n)], [[] for _ in range(nres)]
    for i in order:
        t = max([start[p] + dur[p] for p in preds[i]], default=0)
        slots = [k for k in range(ns) for _ in range(req[i][k])]
        while True:
            free = [r for r in range(nres) if all(b <= t or a >= t + dur[i] for a, b in busy[r]) or dur[i] == 0]
            match = {}

            def augment(slot, visited):
                for r in free:
                    if work[r][slots[slot]] and r not in visited:
                        visited.add(r)
                        if r not in match or augment(match[r], visited):
                            match[r] = slot
                            return True
                return False
            if all(augment(s, set()) for s in range(len(slots))):
                break
            t += 1
            if t > 10 ** 6:
                return None
        start[i] = t
        assign[i] = sorted((r, slots[s]) for r, s in match.items())
        for r, _ in assign[i]:
            if dur[i]:
                busy[r].append((t, t + dur[i]))
    return [(start[i], assign[i]) for i in range(n)]


def independent(n, nres, ns, dur, succ, work, req, sched):
    if len(sched) != n or any(s < 0 for s, _ in sched):
        return None
    for i in range(n):
        if any(sched[j][0] < sched[i][0] + dur[i] for j in succ[i]):
            return None
        pairs = sched[i][1]
        if len({r for r, _ in pairs}) != len(pairs) or any(not (0 <= r < nres and 0 <= k < ns) or not work[r][k] for r, k in pairs):
            return None
        if [sum(1 for _, k in pairs if k == kk) for kk in range(ns)] != req[i]:
            return None
    end = max(s + d for (s, _), d in zip(sched, dur))
    for t in range(end):
        for r in range(nres):
            if sum(1 for i in range(n) if sched[i][0] <= t < sched[i][0] + dur[i] and any(x == r for x, _ in sched[i][1])) > 1:
                return None
    return end


rng = random.Random(2026)
agree = tried = 0
for trial in range(300):
    real = rng.randint(4, 9)
    n = real + 2
    ns = rng.randint(2, 3)
    nres = rng.randint(3, 8)
    work = [[int(rng.random() < 0.5) for _ in range(ns)] for _ in range(nres)]
    for k in range(ns):
        if not any(w[k] for w in work):
            work[rng.randrange(nres)][k] = 1
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
    dur = [0] + [rng.randint(1, 5) for _ in range(real)] + [0]
    req = [[0] * ns]
    for _ in range(real):
        r = [0] * ns
        for k in rng.sample(range(ns), rng.randint(1, ns)):
            r[k] = rng.randint(1, max(1, sum(w[k] for w in work) // 2))
        req.append(r)
    req.append([0] * ns)
    inst = write_instance(dur, succ, work, req)
    sched = serial_schedule(n, nres, ns, dur, succ, work, req)
    if sched is None:
        continue
    kind = trial % 5
    i = rng.randrange(1, n - 1)
    if kind == 1:
        sched[i] = (max(0, sched[i][0] - rng.randint(1, 3)), sched[i][1])
    elif kind == 2 and sched[i][1]:
        r, k = sched[i][1][0]
        sched[i] = (sched[i][0], [(rng.randrange(nres), k)] + sched[i][1][1:])
    elif kind == 3 and sched[i][1]:
        r, k = sched[i][1][0]
        sched[i] = (sched[i][0], [(r, rng.randrange(ns))] + sched[i][1][1:])
    elif kind == 4 and sched[i][1]:
        sched[i] = (sched[i][0], sched[i][1][1:])
    want = independent(n, nres, ns, dur, succ, work, req, sched)
    got = run(inst, sched)
    tried += 1
    agree += got == want
    if got != want:
        print(f"FAIL  random instance {trial}: checker {got}, independent {want}")
expect(f"{tried} random instances (of 300 drawn; the generator gives up on some): the checker agrees with an "
       "independent check", agree, tried)
expect("enough random instances", tried >= 250, True)

# red controls: activities 2 and 3 need skill 1 once each, resource 1 masters skill 1, resource 2 skills 1 and 2
work = [[1, 0], [1, 1]]
dur = [0, 2, 3, 0]
succ = [[1, 2], [3], [3], []]
req = [[0, 0], [1, 0], [1, 1], [0, 0]]
inst = write_instance(dur, succ, work, req)
good = [(0, []), (0, [(0, 0)]), (0, [(1, 1)])]
expect("red skill 2 needed too: activity 3 has only one resource", run(inst, good + [(3, [])]), None)
good = [(0, []), (0, [(0, 0)]), (2, [(0, 0), (1, 1)]), (5, [])]
expect("a feasible schedule", run(inst, good), 5)
expect("red a resource that lacks the skill (resource 1, skill 2)", run(inst, [(0, []), (0, [(0, 0)]), (2, [(1, 0), (0, 1)]), (5, [])]), None)
expect("red a resource named twice", run(inst, [(0, []), (0, [(0, 0)]), (2, [(1, 0), (1, 1)]), (5, [])]), None)
expect("red a resource on two activities at once", run(inst, [(0, []), (0, [(0, 0)]), (1, [(0, 0), (1, 1)]), (4, [])]), None)
expect("red a start before a predecessor finishes", run(inst, [(0, []), (0, [(0, 0)]), (2, [(0, 0), (1, 1)]), (4, [])]), None)
expect("red a line missing", run(inst, good[:3]), None)

# real instances, when present
base = os.path.join(ROOT, "instances", "mslib")
cells = [json.loads(l) for l in open(os.path.join(ROOT, "families", "mslib-scheduling", "cells.jsonl"))]
if os.path.isdir(base):
    picked = random.Random(5).sample(cells, 20)
    good_n = 0
    for c in picked:
        path = os.path.join(base, c["params"]["set"], c["params"]["file"])
        inst = MC.read_instance(path)
        sched = serial_schedule(*inst)
        p1 = write_schedule(sched)
        r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "obb.py"), "check", c["id"], p1], capture_output=True, text=True)
        val = MC.check(*inst, sched)[0]
        ok = f"certified value {val}/1" in r.stdout and "does not improve" in r.stdout and val >= int(c["best"])
        p2 = write_schedule([(0, a) for _, a in sched])
        r2 = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "obb.py"), "check", c["id"], p2], capture_output=True, text=True)
        good_n += ok and "NOT CERTIFIED" in r2.stdout
    expect("20 open cells: serial schedules certified, not better than the best known; all starts at 0 refused", good_n, 20)
else:
    print("skip  real instances: instances/mslib/ does not hold the MSLIB instances")
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
