"""Exact check of a schedule for the multi-skilled resource-constrained project scheduling problem, basic version
(MSRCPSP; the MSLIB format of J. Snauwaert and M. Vanhoucke; standard library only).

  python3 -I msrcpsp_check.py INSTANCE.msrcp SCHEDULE

INSTANCE (.msrcp, an extension of the Patterson format): the Project Module (the number of activities including the
dummy first and last ones, of multi-skilled resources, of skill types and of skill levels; two informative lines; then
per activity its duration, its number of successors and the successors, numbered from 1), the Workforce Module (per
resource, 1 for every skill type it masters, 0 otherwise) and the Skill Requirements Module (per activity, the number
of resources it needs for each skill type). The other modules (skill levels, costs, usage, rework) belong to other
versions of the problem and are not read.

SCHEDULE: one line per activity, in the instance's order (the dummies included): its start time, then one pair
"resource:skill" (both numbered from 1) for every resource it uses and the skill that resource provides; '#' starts a
comment. Checked exactly: every start is a non-negative integer; every activity starts no earlier than each of its
predecessors finishes; every resource named masters the skill it provides and appears at most once in the activity;
for every skill type the activity has exactly as many resources as it requires; and no resource works on two
activities at once (an activity of duration d started at s holds its resources during [s, s + d)). The makespan is
the latest finish. Prints "makespan M" and, as its last line, "RESULT M", and exits 0 for a feasible schedule; exits 1
otherwise."""
import re
import sys


def read_instance(path):
    lines = open(path, encoding="latin-1").read().splitlines()
    mods, cur = {}, None
    for line in lines:
        s = line.strip()
        if s.startswith("\\*"):
            cur = s.strip("\\* ").strip()
            mods[cur] = []
        elif cur is not None and re.match(r"-?\d", s):
            mods[cur].append(s.split())

    def ints(module):
        return [[int(x) for x in row] for row in mods[module]]
    proj = ints("Project Module")
    n, nres, nskills = proj[0][0], proj[0][1], proj[0][2]
    acts = proj[3:3 + n]
    if len(acts) != n:
        raise ValueError(f"{len(acts)} activity lines for {n} activities")
    dur = [a[0] for a in acts]
    succ = [[x - 1 for x in a[2:2 + a[1]]] for a in acts]
    work = ints("Workforce Module")[:nres]
    req = ints("Skill Requirements Module")[:n]
    if len(work) != nres or any(len(w) != nskills for w in work):
        raise ValueError("the Workforce Module does not match the number of resources and skills")
    if len(req) != n or any(len(r) != nskills for r in req):
        raise ValueError("the Skill Requirements Module does not match the number of activities and skills")
    return n, nres, nskills, dur, succ, work, req


def check(n, nres, nskills, dur, succ, work, req, sched):
    if len(sched) != n:
        return None, f"{len(sched)} schedule lines for {n} activities"
    starts = [s for s, _ in sched]
    if any(s < 0 for s in starts):
        return None, "a negative start time"
    for i in range(n):
        for j in succ[i]:
            if not 0 <= j < n:
                return None, f"activity {i + 1}: successor {j + 1} out of range"
            if starts[j] < starts[i] + dur[i]:
                return None, (f"activity {j + 1} starts at {starts[j]}, before its predecessor {i + 1} finishes at "
                              f"{starts[i] + dur[i]}")
    busy = [[] for _ in range(nres)]
    for i, (s, pairs) in enumerate(sched):
        count = [0] * nskills
        used = set()
        for r, k in pairs:
            if not (0 <= r < nres and 0 <= k < nskills):
                return None, f"activity {i + 1}: resource {r + 1} or skill {k + 1} out of range"
            if r in used:
                return None, f"activity {i + 1}: resource {r + 1} named twice"
            if not work[r][k]:
                return None, f"activity {i + 1}: resource {r + 1} does not master skill {k + 1}"
            used.add(r)
            count[k] += 1
        if count != req[i]:
            return None, f"activity {i + 1}: resources per skill {count}, required {req[i]}"
        if dur[i] > 0:
            for r in used:
                busy[r].append((s, s + dur[i], i))
    for r in range(nres):
        iv = sorted(busy[r])
        for (a, b, i), (c, d, j) in zip(iv, iv[1:]):
            if c < b:
                return None, f"resource {r + 1} works on activities {i + 1} and {j + 1} at once (time {c})"
    return max(s + d for s, d in zip(starts, dur)), "precedences, skills and resource use hold"


def read_schedule(path):
    out = []
    for line in open(path, encoding="ascii", errors="replace"):
        tok = line.split("#")[0].replace(",", " ").split()
        if not tok:
            continue
        s = int(tok[0])
        pairs = []
        for t in tok[1:]:
            m = re.fullmatch(r"(\d+):(\d+)", t)
            if not m:
                raise ValueError(f"not a resource:skill pair: {t!r}")
            pairs.append((int(m.group(1)) - 1, int(m.group(2)) - 1))
        out.append((s, pairs))
    return out


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    try:
        inst = read_instance(sys.argv[1])
    except (ValueError, KeyError, IndexError, OSError) as err:
        print(f"cannot read the instance: {err}")
        return 1
    try:
        sched = read_schedule(sys.argv[2])
    except (ValueError, OSError) as err:
        print(f"cannot read the schedule: {err}")
        return 1
    makespan, why = check(*inst, sched)
    print(why)
    if makespan is None:
        return 1
    print(f"makespan {makespan}")
    print(f"RESULT {makespan}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
