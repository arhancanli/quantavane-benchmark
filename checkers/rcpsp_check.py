"""Exact check of a schedule for the resource-constrained project scheduling problem (standard library only).

  python3 -I rcpsp_check.py rcp INSTANCE.rcp SCHEDULE
  python3 -I rcpsp_check.py sm INSTANCE.sm SCHEDULE
  python3 -I rcpsp_check.py rcp+res NETWORK.rcp RESOURCES.txt PROFILE SCHEDULE

Instance formats, as served by the keepers of the instance sets:
- rcp (Patterson format): the number of activities and of renewable resources, the capacities, then for each activity
  its duration, its demand for each resource, its number of successors and their numbers (from 1);
- sm (PSPLIB, single mode): the sections PRECEDENCE RELATIONS, REQUESTS/DURATIONS and RESOURCEAVAILABILITIES;
- rcp+res (NetRes, Vanhoucke and Coelho): durations and successors from a Patterson network whose resource columns are
  placeholders, with capacities and demands from block PROFILE ("File number PROFILE") of a resource file: its line
  after "Resource availability" and one line per activity after "Resource demand" (the dummy first and last activities
  demand nothing).

SCHEDULE: the start time of every activity, in the instance's order (the dummy first and last activities included),
as integers separated by spaces, commas, semicolons or new lines. Checked exactly: every start is a non-negative
integer; every activity starts no earlier than each predecessor finishes; at every moment the activities in progress
(an activity of duration d started at s is in progress during [s, s + d)) demand no more of any resource than its
capacity. The makespan is the latest finish. Prints "makespan M" and, as its last line, "RESULT M", and exits 0 for a
feasible schedule; exits 1 otherwise."""
import re
import sys


def ints(text):
    return [int(x) for x in re.findall(r"-?\d+", text)]


def read_rcp(path, with_resources=True):
    nums = ints(open(path, encoding="latin-1").read())
    n, r = nums[0], nums[1]
    caps = nums[2:2 + r]
    pos = 2 + r
    dur, dem, succ = [], [], []
    for _ in range(n):
        dur.append(nums[pos])
        dem.append(nums[pos + 1:pos + 1 + r])
        k = nums[pos + 1 + r]
        succ.append([s - 1 for s in nums[pos + 2 + r:pos + 2 + r + k]])
        pos += 2 + r + k
    if pos != len(nums):
        raise ValueError(f"{len(nums) - pos} numbers left after {n} activities")
    return n, caps, dur, dem, succ


def read_sm(path):
    lines = open(path, encoding="latin-1").read().splitlines()
    n = next(int(re.search(r":\s*(\d+)", s).group(1)) for s in lines if s.lower().startswith("jobs (incl."))
    r = next(int(re.search(r":\s*(\d+)", s).group(1)) for s in lines if "- renewable" in s)

    def section(title):
        i = next(j for j, s in enumerate(lines) if s.strip().upper().startswith(title))
        out = []
        for s in lines[i + 1:]:
            if s.startswith("***"):
                break
            if re.match(r"\s*\d", s):
                out.append(ints(s))
        return out

    prec = section("PRECEDENCE RELATIONS")
    req = section("REQUESTS/DURATIONS")
    caps = section("RESOURCEAVAILABILITIES")[0][:r]
    if len(prec) != n or len(req) != n:
        raise ValueError(f"expected {n} activities in both sections, found {len(prec)} and {len(req)}")
    dur, dem, succ = [0] * n, [None] * n, [None] * n
    for row in prec:
        j, _modes, k = row[0], row[1], row[2]
        succ[j - 1] = [s - 1 for s in row[3:3 + k]]
    for row in req:
        j = row[0]
        dur[j - 1] = row[2]
        dem[j - 1] = row[3:3 + r]   # renewable resources come first
    return n, caps, dur, dem, succ


def read_profile(path, profile):
    caps, dem, mode, inside = None, [], None, False
    for line in open(path, encoding="latin-1"):
        s = line.strip()
        m = re.match(r"File number (\d+)", s)
        if m:
            if inside:
                break
            inside = int(m.group(1)) == profile
            continue
        if not inside:
            continue
        if s.startswith("Resource availability"):
            mode = "cap"
            continue
        if s.startswith("Resource demand"):
            mode = "dem"
            continue
        nums = s.split()
        if nums and all(x.isdigit() for x in nums):
            if mode == "cap" and caps is None:
                caps = [int(x) for x in nums]
            elif mode == "dem":
                dem.append([int(x) for x in nums])
    if caps is None:
        raise ValueError(f"no profile {profile} in {path}")
    return caps, dem


def check(n, caps, dur, dem, succ, starts):
    if len(starts) != n:
        return None, f"{len(starts)} start times for {n} activities"
    if any(s < 0 for s in starts):
        return None, "a negative start time"
    for i in range(n):
        if dur[i] < 0 or any(x < 0 for x in dem[i]):
            return None, f"activity {i + 1}: negative duration or demand in the instance"
        for j in succ[i]:
            if not 0 <= j < n:
                return None, f"activity {i + 1}: successor {j + 1} out of range"
            if starts[j] < starts[i] + dur[i]:
                return None, (f"activity {j + 1} starts at {starts[j]}, before its predecessor {i + 1} finishes at "
                              f"{starts[i] + dur[i]}")
    # sweep: at each time an activity starts, the activities in progress then must fit
    events = []
    for i in range(n):
        if dur[i] > 0:
            events.append((starts[i], 1, i))
            events.append((starts[i] + dur[i], 0, i))       # ends are processed before starts at the same time
    events.sort()
    use = [0] * len(caps)
    for time, kind, i in events:
        for r, x in enumerate(dem[i]):
            use[r] += x if kind else -x
        if kind:
            for r, c in enumerate(caps):
                if use[r] > c:
                    return None, f"resource {r + 1} over capacity at time {time}: {use[r]} > {c}"
    return max(s + d for s, d in zip(starts, dur)), "precedences and resource capacities hold"


def main():
    fmt = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        if fmt == "rcp" and len(sys.argv) == 4:
            n, caps, dur, dem, succ = read_rcp(sys.argv[2])
            sched = sys.argv[3]
        elif fmt == "sm" and len(sys.argv) == 4:
            n, caps, dur, dem, succ = read_sm(sys.argv[2])
            sched = sys.argv[3]
        elif fmt == "rcp+res" and len(sys.argv) == 6:
            n, _, dur, _, succ = read_rcp(sys.argv[2])
            caps, real = read_profile(sys.argv[3], int(sys.argv[4]))
            if len(real) != n - 2 or any(len(x) != len(caps) for x in real):
                raise ValueError(f"profile {sys.argv[4]}: {len(real)} demand lines for {n - 2} activities")
            zero = [0] * len(caps)
            dem = [zero] + real + [zero]
            sched = sys.argv[5]
        else:
            print(__doc__)
            return 2
    except (ValueError, IndexError, StopIteration, OSError) as err:
        print(f"cannot read the instance: {err}")
        return 1
    try:
        starts = ints(open(sched).read())
    except OSError as err:
        print(f"cannot read the schedule: {err}")
        return 1
    makespan, why = check(n, caps, dur, dem, succ, starts)
    print(why)
    if makespan is None:
        return 1
    print(f"makespan {makespan}")
    print(f"RESULT {makespan}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
