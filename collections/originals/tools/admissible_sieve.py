"""Small-diameter admissible k-sets in Z[i] or Z[w] by a greedy sieve in a disc, then local repair (our own code).

  python3 -I admissible_sieve.py RING K [TRIALS] [SEED]      RING = 4 for Z[i], 3 for Z[w]

For centres c in a fundamental cell and squared radii R, take the lattice points z with norm(z - c) <= R, and for each
prime ideal P of norm <= K (smallest norm first) delete the residue class modulo P that holds the fewest remaining
points (ties broken at random). If at least K points remain, the K points nearest to c give an admissible K-set; its
diameter (largest squared distance) is recorded. Prints the best diameter and the set, one point "x y" per line."""
import random
import sys


def nrm(ring, x, y):
    return x * x + y * y if ring == 4 else x * x - x * y + y * y


def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def ideals(ring, kmax):
    """Prime ideals of norm <= kmax as (norm, kind, p, r): residue of x + y*u is x + y*r mod p (kind 0) or (x, y) mod p
    (kind 1, inert p of norm p^2); u = i for ring 4, u = w for ring 3."""
    out = []
    for p in range(2, kmax + 1):
        if not isprime(p):
            continue
        if ring == 4:
            if p == 2:
                out.append((2, 0, 2, 1))
            elif p % 4 == 1:
                r = next(a for a in range(2, p) if (a * a + 1) % p == 0)
                out += [(p, 0, p, r), (p, 0, p, p - r)]
            elif p * p <= kmax:
                out.append((p * p, 1, p, 0))
        else:
            if p == 3:
                out.append((3, 0, 3, 1))
            elif p % 3 == 1:
                r = next(a for a in range(2, p) if (a * a + a + 1) % p == 0)
                out += [(p, 0, p, r), (p, 0, p, (r * r) % p)]
            elif p * p <= kmax:
                out.append((p * p, 1, p, 0))
    return out


def residue(ideal, x, y):
    n, kind, p, r = ideal
    return (x % p, y % p) if kind == 1 else (x + y * r) % p


def admissible(ring, pts):
    k = len(pts)
    for I in ideals(ring, k):
        if len({residue(I, x, y) for x, y in pts}) == I[0]:
            return False
    return True


def diameter(ring, pts):
    return max((nrm(ring, a[0] - b[0], a[1] - b[1]) for i, a in enumerate(pts) for b in pts[i + 1:]), default=0)


def sieve(ring, k, cx, cy, R, rng, ids):
    """cx, cy: centre in quarter units (the centre is (cx/4, cy/4)); R: squared radius in sixteenths."""
    m = int((R ** 0.5) / 4) + 3
    ox, oy = cx // 4, cy // 4
    pts = []
    for x in range(ox - m - 2, ox + m + 3):
        for y in range(oy - m - 2, oy + m + 3):
            d = nrm(ring, 4 * x - cx, 4 * y - cy)
            if d <= R:
                pts.append((d, x, y))
    if len(pts) < k:
        return None
    for I in ids:
        cnt = {}
        for _, x, y in pts:
            c = residue(I, x, y)
            cnt[c] = cnt.get(c, 0) + 1
        if len(cnt) < I[0]:
            continue                     # a class is already empty
        lo = min(cnt.values())
        drop = rng.choice([c for c, v in cnt.items() if v == lo])
        pts = [t for t in pts if residue(I, t[1], t[2]) != drop]
        if len(pts) < k:
            return None
    pts.sort()
    return [(x, y) for _, x, y in pts[:k]]


def improve(ring, k, pts, ids, rng, rounds=400):
    """Remove a point on the diameter and add any admissible point that lowers the diameter."""
    best = list(pts)
    D = diameter(ring, best)
    for _ in range(rounds):
        far = [(a, b) for i, a in enumerate(best) for b in best[i + 1:] if nrm(ring, a[0] - b[0], a[1] - b[1]) == D]
        a, b = rng.choice(far)
        out = rng.choice([a, b])
        rest = [p for p in best if p != out]
        xs = [p[0] for p in rest]
        ys = [p[1] for p in rest]
        cands = [(x, y) for x in range(min(xs) - 2, max(xs) + 3) for y in range(min(ys) - 2, max(ys) + 3)
                 if (x, y) not in rest and all(nrm(ring, x - p[0], y - p[1]) < D for p in rest)]
        rng.shuffle(cands)
        for c in cands:
            trial = rest + [c]
            if admissible(ring, trial):
                d2 = diameter(ring, trial)
                if d2 < D or (d2 == D and rng.random() < 0.3):
                    best, D = trial, d2
                    break
    return best, D


def main():
    ring, k = int(sys.argv[1]), int(sys.argv[2])
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 0)
    ids = sorted(ideals(ring, k))
    best, bestD = None, None
    for t in range(trials):
        cx, cy = rng.randrange(4), rng.randrange(4)
        lo, hi = 1, 64 * k * 16
        found = None
        while lo < hi:                       # least squared radius with k survivors (for this tie-breaking)
            mid = (lo + hi) // 2
            got = sieve(ring, k, cx, cy, mid, random.Random(t), ids)
            if got:
                hi, found = mid, got
            else:
                lo = mid + 1
        if not found:
            continue
        assert admissible(ring, found)
        pts, D = improve(ring, k, found, ids, rng, rounds=60)
        if bestD is None or D < bestD:
            best, bestD = pts, D
    best, bestD = improve(ring, k, best, ids, rng, rounds=2000)
    assert admissible(ring, best) and len(set(best)) == k
    print(f"# ring {ring} k {k} diameter {bestD}")
    for x, y in sorted(best):
        print(x, y)


if __name__ == "__main__":
    main()
