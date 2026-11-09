"""Exact checkers for the astronomy problems of the Quantavane Originals (standard library only).

  python3 -I orig_astro.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved); it exits 0 only for a
valid certificate and 1 otherwise. Problems:

  nrm-segments S FILE   FILE: lines "a b", the segments of a mirror of S rings that carry a hole. Segment centres are
                        the points a + b*w of the triangular lattice (w = e^(i pi/3)) with hexagonal norm
                        max(|a|, |b|, |a + b|) from 1 to S (the centre segment is missing). Valid when the holes are
                        distinct segments and no baseline repeats: the vectors p - q between two holes are all
                        different, a vector and its negative counting as the same baseline. Value: number of holes.
  nrm-tilting S FILE    FILE: one line per group, the segments of the group as "a,b" pairs separated by spaces. Valid
                        when every segment of the S-ring mirror is in exactly one group and no baseline repeats within
                        a group. Value: number of groups.
  slew-tour SKY FILE    SKY: collections/originals/instances/bsc-sky.txt; FILE: the HR numbers of all its stars in the
                        order of a closed tour, each once. A step costs max(dRA, dDec) in half arcseconds (both axes
                        of an equatorial mount turning at the same rate; dRA the shorter way round). Value: the
                        length of the tour.
  star-tracker INST K FILE  INST: collections/originals/instances/star-tracker.txt (integer unit vectors of the stars
                        and of the boresights, threshold T); FILE: HR numbers of chosen stars. Valid when every
                        boresight has at least K chosen stars in its field of view (dot product >= T). Value: the
                        number of chosen stars."""
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


def nrm_tilting(args, path):
    s = int(args[0])
    groups = []
    for line in open(path):
        line = line.split("#")[0].strip()
        if line:
            groups.append([tuple(int(t) for t in tok.split(",")) for tok in line.split()])
    allseg = {(a, b) for a in range(-s, s + 1) for b in range(-s, s + 1) if 1 <= hexnorm(a, b) <= s}
    listed = [p for g in groups for p in g]
    if len(listed) != len(set(listed)) or set(listed) != allseg:
        print(f"the groups must contain every one of the {len(allseg)} segments exactly once")
        return 1
    for gi, g in enumerate(groups):
        seen = set()
        for i in range(len(g)):
            for j in range(i + 1, len(g)):
                da, db = g[i][0] - g[j][0], g[i][1] - g[j][1]
                if da < 0 or (da == 0 and db < 0):
                    da, db = -da, -db
                if (da, db) in seen:
                    print(f"group {gi + 1}: baseline ({da}, {db}) repeats")
                    return 1
                seen.add((da, db))
    print(f"{len(groups)} groups cover the {len(allseg)} segments of the {s}-ring mirror; no baseline repeats within a group")
    print(f"RESULT {len(groups)}")
    return 0


def slew_tour(args, path):
    sky = {}
    for line in open(args[0]):
        if line.startswith("#") or not line.strip():
            continue
        hr, ra, dec, v = (int(t) for t in line.split())
        sky[hr] = (3 * ra, 2 * dec)
    tour = [int(t) for line in open(path) for t in line.split("#")[0].split()]
    if len(tour) != len(sky) or set(tour) != set(sky):
        print(f"the tour must list each of the {len(sky)} stars exactly once")
        return 1
    full, total = 2592000, 0
    for i in range(len(tour)):
        (r1, d1), (r2, d2) = sky[tour[i]], sky[tour[(i + 1) % len(tour)]]
        dr = abs(r1 - r2)
        total += max(min(dr, full - dr), abs(d1 - d2))
    print(f"closed tour of the {len(tour)} stars: {total} half arcseconds of slewing ({total / 7200:.2f} degrees)")
    print(f"RESULT {total}")
    return 0


def star_tracker(args, path):
    lines = [l for l in open(args[0]) if not l.startswith("#") and l.strip()]
    T = int(lines[0])
    S, B = (int(t) for t in lines[1].split())
    stars = {}
    for l in lines[2:2 + S]:
        hr, x, y, z = (int(t) for t in l.split())
        stars[hr] = (x, y, z)
    bores = [tuple(int(t) for t in l.split()) for l in lines[2 + S:2 + S + B]]
    k = int(args[1])
    chosen = [int(t) for line in open(path) for t in line.split("#")[0].split()]
    if len(chosen) != len(set(chosen)) or not set(chosen) <= set(stars):
        print("the chosen stars must be distinct stars of the instance")
        return 1
    vec = [stars[h] for h in chosen]
    worst = None
    for i, (bx, by, bz) in enumerate(bores):
        c = sum(1 for x, y, z in vec if x * bx + y * by + z * bz >= T)
        if c < k:
            print(f"boresight {i + 1} sees only {c} chosen stars (needs {k})")
            return 1
        worst = c if worst is None else min(worst, c)
    print(f"{len(chosen)} stars; every one of the {B} boresights sees at least {worst} of them (needs {k})")
    print(f"RESULT {len(chosen)}")
    return 0


PROBLEMS = {"nrm-segments": (1, nrm_segments), "nrm-tilting": (1, nrm_tilting), "slew-tour": (1, slew_tour),
            "star-tracker": (2, star_tracker)}


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
