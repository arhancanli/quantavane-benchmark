"""Exact check of a job shop schedule, and of a flexible job shop schedule (standard library only).

  python3 -I jsp_check.py INSTANCE FILE              (job shop)
  python3 -I jsp_check.py --flexible INSTANCE FILE   (flexible job shop)

Job shop INSTANCE (the standard text format of JSPLib and of Taillard's and Demirkol's instances): a line "n m", then
n lines, one per job, each a sequence of (machine, duration) pairs, machines numbered from 0, in the order the job must
follow. Flexible job shop INSTANCE (Brandimarte's format): a line "n m [average]", then n lines, one per job: the number
of operations, then for each operation the number k of machines that can do it followed by k pairs (machine,
duration), machines numbered from 1.

FILE, one line per job in the instance's order: for the job shop, the start time of each operation of the job, in
order; for the flexible job shop, for each operation of the job, the machine chosen and the start time (two integers).
Blank lines and lines starting with '#' are ignored. Times are non-negative integers.

The schedule is valid when every operation starts no earlier than the previous operation of its job ends, every
flexible operation runs on one of its machines for that machine's duration, and no two operations on one machine
overlap (touching is allowed). The value is the makespan, the latest end. Everything is integer arithmetic.

Prints "makespan C" and, as its last line, "RESULT C", and exits 0 for a valid schedule; exits 1 otherwise."""
import sys


def ints(line):
    return [int(x) for x in line.replace(",", " ").split()]


def read_instance(path, flexible):
    lines = [l for l in open(path) if l.strip()]
    head = lines[0].split()
    n, m = int(head[0]), int(float(head[1]))
    jobs = []
    for j in range(n):
        v = ints(lines[1 + j])
        ops = []
        if flexible:
            k, pos = v[0], 1
            for _ in range(k):
                c = v[pos]
                alts = {}
                for o in range(c):
                    mach, dur = v[pos + 1 + 2 * o], v[pos + 2 + 2 * o]
                    alts[mach] = min(dur, alts.get(mach, dur))
                ops.append(alts)
                pos += 1 + 2 * c
            if pos != len(v):
                raise ValueError(f"instance job {j + 1}: {len(v) - pos} numbers left over")
        else:
            if len(v) % 2:
                raise ValueError(f"instance job {j + 1}: an odd number of numbers")
            ops = [{v[2 * o]: v[2 * o + 1]} for o in range(len(v) // 2)]
        jobs.append(ops)
    return n, m, jobs


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    flexible = "--flexible" in argv
    if flexible:
        argv.remove("--flexible")
    if len(argv) != 2:
        print(__doc__)
        return 1
    try:
        n, m, jobs = read_instance(argv[0], flexible)
        rows = [l for l in open(argv[1]) if l.strip() and not l.strip().startswith("#")]
        if len(rows) != n:
            raise ValueError(f"{len(rows)} lines, expected one per job ({n})")
        sched = []                                         # (machine, start, end, job, op)
        for j, (row, ops) in enumerate(zip(rows, jobs)):
            v = ints(row)
            per = 2 if flexible else 1
            if len(v) != per * len(ops):
                raise ValueError(f"job {j + 1}: {len(v)} numbers, expected {per * len(ops)}")
            prev_end = 0
            for o, alts in enumerate(ops):
                if flexible:
                    mach, start = v[2 * o], v[2 * o + 1]
                    if mach not in alts:
                        print(f"job {j + 1}, operation {o + 1}: machine {mach} cannot do it")
                        return 1
                else:
                    (mach,) = alts.keys()
                    start = v[o]
                if start < 0:
                    raise ValueError(f"job {j + 1}, operation {o + 1}: a negative start time")
                if start < prev_end:
                    print(f"job {j + 1}, operation {o + 1} starts at {start}, before the previous one ends at {prev_end}")
                    return 1
                end = start + alts[mach]
                sched.append((mach, start, end, j + 1, o + 1))
                prev_end = end
    except (ValueError, IndexError, OSError) as e:
        print("malformed:", e)
        return 1
    sched.sort()
    for a, b in zip(sched, sched[1:]):
        if a[0] == b[0] and b[1] < a[2]:
            print(f"machine {a[0]}: job {a[3]} operation {a[4]} (until {a[2]}) overlaps job {b[3]} operation {b[4]} "
                  f"(from {b[1]})")
            return 1
    C = max(e for _, _, e, _, _ in sched) if sched else 0
    print(f"{len(sched)} operations of {n} jobs on {m} machines, every precedence and machine respected")
    print(f"makespan {C}")
    print(f"RESULT {C}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
