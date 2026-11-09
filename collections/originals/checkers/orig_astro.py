"""Exact checkers for the astronomy problems of the Quantavane Originals (standard library only).

  python3 -I orig_astro.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved); it exits 0 only for a
valid certificate and 1 otherwise. Problems:

  nrm-segments S FILE   FILE: lines "a b", the segments of a mirror of S rings that carry a hole. Segment centres are
                        the points a + b*w of the triangular lattice (w = e^(i pi/3)) with hexagonal norm
                        max(|a|, |b|, |a + b|) from 1 to S (the centre segment is missing). Valid when the holes are
                        distinct segments and no baseline repeats: the vectors p - q between two holes are all
                        different, a vector and its negative counting as the same baseline. Value: number of holes.
  y-array N FILE        FILE: three lines, the distances (positive integers) of the antennas on the three arms of a
                        Y whose arms meet at 120 degrees (a line "-" for an empty arm). Two antennas on one arm at a
                        and a' have squared distance (a - a')^2, on two arms a^2 + ab + b^2. Valid when there are N
                        antennas, no place is used twice and all N(N - 1)/2 squared baseline lengths are different.
                        Value: the arm length, the largest distance used."""
import sys


def points(path):
    out = []
    for line in open(path):
        line = line.split("#")[0].strip()
        if line:
            a, b = line.split()
            out.append((int(a), int(b)))
    return out


def hexnorm(a, b):
    return max(abs(a), abs(b), abs(a + b))


def nrm_segments(args, path):
    s = int(args[0])
    P = points(path)
    if len(set(P)) != len(P):
        print("a segment is listed twice")
        return 1
    for a, b in P:
        if not 1 <= hexnorm(a, b) <= s:
            print(f"({a}, {b}) is not a segment of the {s}-ring mirror (hexagonal norm {hexnorm(a, b)})")
            return 1
    seen = {}
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            da, db = P[i][0] - P[j][0], P[i][1] - P[j][1]
            if da < 0 or (da == 0 and db < 0):
                da, db = -da, -db
            if (da, db) in seen:
                k, l = seen[(da, db)]
                print(f"baseline ({da}, {db}) repeats: holes {P[i]}, {P[j]} and {P[k]}, {P[l]}")
                return 1
            seen[(da, db)] = (i, j)
    print(f"{len(P)} holes on the {s}-ring mirror ({3 * s * (s + 1)} segments), {len(seen)} baselines, all different")
    print(f"RESULT {len(P)}")
    return 0


def y_array(args, path):
    n = int(args[0])
    rows = [l.split("#")[0].strip() for l in open(path) if l.split("#")[0].strip()]
    if len(rows) != 3:
        print("expected three lines, one per arm ('-' for an empty arm)")
        return 1
    arms = [[] if r == "-" else [int(t) for t in r.replace(",", " ").split()] for r in rows]
    if any(a < 1 for arm in arms for a in arm) or any(len(set(arm)) != len(arm) for arm in arms):
        print("distances must be positive and different on each arm")
        return 1
    ants = [(k, a) for k, arm in enumerate(arms) for a in arm]
    if len(ants) != n:
        print(f"expected {n} antennas, found {len(ants)}")
        return 1
    seen = {}
    for i in range(n):
        for j in range(i + 1, n):
            (k1, a), (k2, b) = ants[i], ants[j]
            q = (a - b) ** 2 if k1 == k2 else a * a + a * b + b * b
            if q in seen:
                print(f"squared length {q} occurs twice: {ants[i]}, {ants[j]} and {seen[q]}")
                return 1
            seen[q] = (ants[i], ants[j])
    L = max(a for _, a in ants)
    print(f"{n} antennas on arms of {', '.join(str(len(arm)) for arm in arms)}; all {len(seen)} baseline lengths different; arm length {L}")
    print(f"RESULT {L}")
    return 0


PROBLEMS = {"nrm-segments": (1, nrm_segments), "y-array": (1, y_array)}


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in PROBLEMS:
        print(__doc__)
        return 2
    nargs, fn = PROBLEMS[sys.argv[1]]
    if len(sys.argv) != 3 + nargs:
        print(__doc__)
        return 2
    try:
        return fn(sys.argv[2:-1], sys.argv[-1])
    except (ValueError, IndexError, OSError) as e:
        print(f"invalid certificate: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
