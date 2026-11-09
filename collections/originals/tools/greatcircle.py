"""Sets of vertices of the 600-cell and the 120-cell with no three on a great circle (our own code, Quantavane
Originals, problem cell120-great).

  python3 -I greatcircle.py lines 600|120              the great circles through at least three vertex pairs
  python3 -I greatcircle.py partition 600|120          the Hopf partition into great decagons (the upper bound)
  python3 -I greatcircle.py exact600                   exhaustive search for the 600-cell (its 60 antipodal pairs)
  python3 -I greatcircle.py search120 SECONDS SEED OUT local search for the 120-cell (its 300 antipodal pairs)

Exact arithmetic in Q(sqrt 5): numbers a + b sqrt5 as pairs of Fractions. The 600-cell's 120 vertices are the unit
quaternions of the binary icosahedral group, numbered as in checkers/orig_codes.py (cell600_graph); the 120-cell's 600
vertices are the centres (vertex sums) of the 600 tetrahedral cells of the 600-cell. Three vertices lie on a great
circle exactly when they span at most a plane through the centre, so a valid set takes at most one vertex of each
antipodal pair; a plane through two vertices is identified by its normalised Plucker coordinates."""
import itertools
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, __file__.rsplit("/tools/", 1)[0] + "/checkers")
import orig_geom  # noqa: E402  (the checker's exact construction)


def partition(lines, n, size):
    """A partition of the n points into lines of the given size (exact cover search), or None."""
    L = [frozenset(l) for l in lines if len(l) == size]
    by = {}
    for l in L:
        for p in l:
            by.setdefault(p, []).append(l)
    sol = []

    def dfs(cov):
        if len(cov) == n:
            return True
        p = next(q for q in range(n) if q not in cov)
        for l in by.get(p, []):
            if not l & cov:
                sol.append(l)
                if dfs(cov | l):
                    return True
                sol.pop()
        return False
    return sol if dfs(frozenset()) else None


def qmul(p, q):
    """Quaternion product in Q(sqrt 5)^4, (w, x, y, z)."""
    m = orig_geom._q5mul
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    add = lambda *t: (sum(x[0] for x in t), sum(x[1] for x in t))
    neg = lambda x: (-x[0], -x[1])
    return (add(m(a1, a2), neg(m(b1, b2)), neg(m(c1, c2)), neg(m(d1, d2))),
            add(m(a1, b2), m(b1, a2), m(c1, d2), neg(m(d1, c2))),
            add(m(a1, c2), neg(m(b1, d2)), m(c1, a2), m(d1, b2)),
            add(m(a1, d2), m(b1, c2), neg(m(c1, b2)), m(d1, a2)))


def hopf_partition(kind):
    """The great decagons cut out by left multiplication with g = (phi/2, 1/2, 1/(2 phi), 0), an element of order 10
    of the binary icosahedral group: its orbits on the vertices of the 600-cell (kind '600') or on the cells, i.e. the
    vertices of the 120-cell (kind '120'), each of 10 vertices on one great circle. Returned as sets of indices into
    great_points(kind), with the check that each orbit spans a single plane."""
    pts600, _ = orig_geom.cell600_points()
    index = {v: i for i, v in enumerate(pts600)}
    g = next(v for v in pts600 if v[0] == ((F(1, 4), F(1, 4))) and v[1] == (F(1, 2), F(0)) and v[3] == (F(0), F(0)))
    perm = [index[qmul(g, v)] for v in pts600]
    gp, labels = orig_geom.great_points(kind)
    if kind == "600":
        key = {lab: i for i, lab in enumerate(labels)}
        items = list(range(120))
        rep = lambda v: v
        vec = lambda v: pts600[v]
    else:
        cells, _, _ = orig_geom.cell600_cells()
        key = {lab: i for i, lab in enumerate(labels)}
        items = cells
        vec = lambda c: orig_geom._vsum([pts600[i] for i in c])
    neg = lambda v: tuple((-x[0], -x[1]) for x in v)
    point_of = {}
    for i, p in enumerate(gp):
        point_of[p] = i
        point_of[neg(p)] = i
    seen, parts = set(), []
    for it in items:
        if it in seen:
            continue
        orbit, cur = [], it
        while cur not in seen:
            seen.add(cur)
            orbit.append(cur)
            cur = perm[cur] if kind == "600" else tuple(sorted(perm[i] for i in cur))
        vs = [vec(o) for o in orbit]
        planes = {orig_geom.plane_key(vs[0], v) for v in vs[1:] if orig_geom.plane_key(vs[0], v) is not None}
        assert len(orbit) == 10 and len(planes) == 1, (len(orbit), len(planes))
        parts.append(frozenset(point_of[v] for v in vs))
    assert all(len(p) == 5 for p in parts) and len(set().union(*parts)) == len(gp)
    return parts


def main():
    mode = sys.argv[1]
    if mode == "lines":
        pts, labels = orig_geom.great_points(sys.argv[2])
        lines = orig_geom.great_lines(pts)
        big = [l for l in lines if len(l) >= 3]
        sizes = {}
        for l in big:
            sizes[len(l)] = sizes.get(len(l), 0) + 1
        print(f"{len(pts)} antipodal pairs; great circles through >= 3 of them: {len(big)}, by size {sorted(sizes.items())}")
        return 0
    if mode == "partition":
        parts = hopf_partition(sys.argv[2])
        print(f"{sys.argv[2]}: {len(parts)} disjoint great decagons cover all {5 * len(parts)} antipodal pairs, so a set with "
              f"no three on a great circle has at most {2 * len(parts)} vertices")
        return 0
    if mode == "exact600":
        pts, labels = orig_geom.great_points("600")
        lines = [l for l in orig_geom.great_lines(pts) if len(l) >= 3]
        n = len(pts)
        on = [[] for _ in range(n)]
        for li, l in enumerate(lines):
            for p in l:
                on[p].append(li)
        part = hopf_partition("600")           # 12 disjoint great decagons cover the 60 pairs
        cnt = [0] * len(lines)
        best = [0, []]
        chosen = []

        def bound(i):
            rest = 0
            for L in part:
                have = sum(1 for q in L if q in chosen_set)
                left = sum(1 for q in L if q >= i)
                rest += min(2 - have, left)
            return len(chosen) + rest

        chosen_set = set()

        def dfs(i):
            if bound(i) <= best[0]:
                return
            if i == n:
                best[0], best[1] = len(chosen), list(chosen)
                print(f"  {best[0]}", flush=True)
                return
            if all(cnt[li] < 2 for li in on[i]):
                for li in on[i]:
                    cnt[li] += 1
                chosen.append(i)
                chosen_set.add(i)
                dfs(i + 1)
                chosen.pop()
                chosen_set.discard(i)
                for li in on[i]:
                    cnt[li] -= 1
            dfs(i + 1)
        dfs(0)
        print(f"600-cell: largest set with no three vertices on a great circle: {best[0]} (bound 24 from 12 decagons): {[labels[p] for p in best[1]]}")
        return 0
    if mode == "search120":
        secs, seed, out = float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        rng = random.Random(seed)
        pts, labels = orig_geom.great_points("120")
        lines = [l for l in orig_geom.great_lines(pts) if len(l) >= 3]
        n = len(pts)
        on = [[] for _ in range(n)]
        for li, l in enumerate(lines):
            for p in l:
                on[p].append(li)
        best = []
        t0 = time.time()
        while time.time() - t0 < secs:
            cnt = [0] * len(lines)
            S = set()
            order = list(range(n))
            rng.shuffle(order)
            for p in order:                       # random greedy
                if all(cnt[li] < 2 for li in on[p]):
                    S.add(p)
                    for li in on[p]:
                        cnt[li] += 1
            improved = True
            while improved and time.time() - t0 < secs:   # 1-for-2 and swap moves
                improved = False
                outside = [p for p in range(n) if p not in S]
                rng.shuffle(outside)
                for p in outside:
                    blocking = {q for li in on[p] if cnt[li] >= 2 for q in lines[li] if q in S}
                    if len(blocking) == 1:
                        q = blocking.pop()
                        for li in on[q]:
                            cnt[li] -= 1
                        S.discard(q)
                        S.add(p)
                        for li in on[p]:
                            cnt[li] += 1
                        free = [r for r in range(n) if r not in S and all(cnt[li] < 2 for li in on[r])]
                        for r in free:
                            if all(cnt[li] < 2 for li in on[r]):
                                S.add(r)
                                for li in on[r]:
                                    cnt[li] += 1
                                improved = True
            if len(S) > len(best):
                best = sorted(S)
                print(f"  {len(best)}", flush=True)
        with open(out, "w") as f:
            for p in best:
                f.write(" ".join(map(str, labels[p])) + "\n")
        print(f"120-cell: {len(best)} vertices, no three on a great circle")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
