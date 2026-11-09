"""Lower bounds for nrm-tilting: can G maximum non-redundant sets partition the s-ring mirror? (our own code)

  tools/src/nrm all S K > SETS.txt ; python3 -I nrm_cover.py SETS.txt NSEGMENTS G

When G * K equals the number of segments and K is the largest size of a non-redundant set, a partition into G groups
must use G disjoint sets of exactly K segments. SETS.txt lists every such set as a bit mask; an exhaustive exact-cover
search (always branching on the lowest uncovered segment) decides whether G of them cover all segments."""
import sys


def cover(sets, full, cov, g):
    if cov == full:
        return []
    if g == 0:
        return None
    free = ~cov & full
    low = (free & -free).bit_length() - 1
    for m in sets:
        if m >> low & 1 and not m & cov:
            r = cover(sets, full, cov | m, g - 1)
            if r is not None:
                return [m] + r
    return None


def main():
    sets = [int(l) for l in open(sys.argv[1]) if l.strip()]
    n, g = int(sys.argv[2]), int(sys.argv[3])
    r = cover(sets, (1 << n) - 1, 0, g)
    print(f"{len(sets)} sets; partition of the {n} segments into {g} of them: {'found' if r else 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
