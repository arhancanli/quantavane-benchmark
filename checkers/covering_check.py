"""Exact check of a covering design (from quantavane-covering-records/verify.py; standard library only).

  python3 -I covering_check.py V K T M FILE

FILE has one block per line, K distinct points from 1..V separated by spaces. With M = T this is a (V,K,T) covering:
every T-subset of {1..V} must lie in some block, and all C(V,T) of them are listed. With M > T it is a (V,K,T,M)
covering: every M-subset must meet some block in at least T points, decided by an exact search for an M-subset that
meets every block in at most T-1 points. Prints "blocks B" and exits 0 when the design is valid, exits 1 otherwise."""
import itertools
import math
import sys


def covers_everything(blocks, v, t):
    seen = set()
    for b in blocks:
        seen.update(itertools.combinations(sorted(b), t))
    missing = math.comb(v, t) - len(seen)
    return missing == 0, (f"{missing} of {math.comb(v, t)} {t}-subsets uncovered" if missing else "every subset covered")


def no_bad_m_subset(blocks, v, t, m):
    """True if every m-subset of 1..v meets some block in at least t points. Points with the same set of blocks are
    interchangeable, so the search picks how many points of each such type a bad m-subset would use, never more than
    t-1 from any block, by depth-first search with a counting bound."""
    member = {p: frozenset(i for i, b in enumerate(blocks) if p in b) for p in range(1, v + 1)}
    count = {}
    for p, ty in member.items():
        count[ty] = count.get(ty, 0) + 1
    free = count.pop(frozenset(), 0)
    types = sorted(count, key=lambda ty: -len(ty))
    cap = [t - 1] * len(blocks)

    def room(ty):
        return min([count[ty]] + [cap[i] for i in ty])

    def search(j, size):
        if size >= m:
            return True
        if size + sum(room(ty) for ty in types[j:]) < m:
            return False
        ty = types[j]
        for x in range(room(ty), -1, -1):
            for i in ty:
                cap[i] -= x
            found = search(j + 1, size + x)
            for i in ty:
                cap[i] += x
            if found:
                return True
        return False

    bad = search(0, free) if types else free >= m
    return (not bad), ("no bad m-subset exists" if not bad else f"some {m}-subset meets every block in fewer than {t} points")


def main():
    v, k, t, m = (int(x) for x in sys.argv[1:5])
    blocks = []
    for line in open(sys.argv[5]):
        line = line.split("#")[0].strip()
        if line:
            blocks.append([int(x) for x in line.split()])
    for b in blocks:
        if len(b) != k or len(set(b)) != k or not all(1 <= p <= v for p in b):
            print(f"invalid block {b}: need {k} distinct points from 1..{v}")
            return 1
    ok, why = covers_everything(blocks, v, t) if m == t else no_bad_m_subset(blocks, v, t, m)
    print(why)
    if not ok:
        return 1
    print(f"blocks {len(blocks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
