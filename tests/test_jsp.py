"""Tests of checkers/jsp_check.py (standard library only; run by test.sh): small job shop and flexible job shop
instances with hand-made schedules (a valid one with its makespan; red controls: two operations overlapping on a
machine, an operation before its predecessor ends, a machine that cannot do the operation, a negative start, a short
line), and random instances where a greedy schedule passes and the same schedule shifted to overlap fails.

  python3 -I tests/test_jsp.py"""
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "jsp_check.py")
TMP = tempfile.mkdtemp(prefix="jsp_test_")
failures = []


def run(inst, sol, flexible=False):
    ip, sp = os.path.join(TMP, "i.txt"), os.path.join(TMP, "s.txt")
    open(ip, "w").write(inst)
    open(sp, "w").write(sol)
    r = subprocess.run([sys.executable, "-I", CHECK] + (["--flexible"] if flexible else []) + [ip, sp],
                       capture_output=True, text=True)
    return r.returncode, (r.stdout.strip().splitlines() or [""])[-1]


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


J = "2 2\n0 3 1 2\n1 2 0 4\n"
expect("job shop 2 x 2, makespan 7", run(J, "0 3\n0 3\n"), (0, "RESULT 7"))
expect("red: two operations overlap on machine 0", run(J, "0 3\n0 2\n")[0], 1)
expect("red: an operation before its predecessor ends", run(J, "0 2\n0 3\n")[0], 1)
expect("red: a negative start", run(J, "0 3\n-1 3\n")[0], 1)
expect("red: a short line", run(J, "0 3\n0\n")[0], 1)
F = "2 2 1\n2 2 1 3 2 2 1 2 1\n1 1 2 4\n"
expect("flexible 2 jobs, makespan 7", run(F, "2 0 2 2\n2 3\n", True), (0, "RESULT 7"))
expect("flexible: the other machine for operation 1, makespan 8", run(F, "1 0 2 3\n2 4\n", True), (0, "RESULT 8"))
expect("red: flexible overlap on machine 2", run(F, "2 0 2 2\n2 2\n", True)[0], 1)
expect("red: flexible precedence", run(F, "1 0 2 2\n2 3\n", True)[0], 1)
expect("red: a machine that cannot do the operation", run(F, "2 0 1 2\n2 3\n", True)[0], 1)


def greedy(jobs):
    """Jobs as lists of (machine, duration): place operations job by job at the earliest time after the job's previous
    operation and after everything already on the machine."""
    free, out = {}, []
    for ops in jobs:
        t, starts = 0, []
        for mach, dur in ops:
            s = max(t, free.get(mach, 0))
            starts.append(s)
            t = s + dur
            free[mach] = t
        out.append(starts)
    return out


rng = random.Random(20261115)
ok = 0
for trial in range(30):
    n, m = rng.randint(2, 6), rng.randint(2, 5)
    jobs = [[(mach, rng.randint(1, 9)) for mach in rng.sample(range(m), m)] for _ in range(n)]
    inst = f"{n} {m}\n" + "".join(" ".join(f"{a} {b}" for a, b in ops) + "\n" for ops in jobs)
    st = greedy(jobs)
    good = run(inst, "".join(" ".join(map(str, s)) + "\n" for s in st))
    C = max(s[-1] + ops[-1][1] for s, ops in zip(st, jobs))
    # move the first operation of the last job onto the first operation of the job before it on the same machine
    bad_st = [s[:] for s in st]
    mach0 = jobs[-1][0][0]
    other = next(((j, o) for j in range(n - 1) for o, (mm, _) in enumerate(jobs[j]) if mm == mach0), None)
    if other:
        bad_st[-1][0] = st[other[0]][other[1]]
        bad = run(inst, "".join(" ".join(map(str, s)) + "\n" for s in bad_st))
    else:
        bad = (1, "")
    ok += good == (0, f"RESULT {C}") and bad[0] == 1
expect("30 random job shops: greedy schedules pass with their makespan, shifted copies fail", ok, 30)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
