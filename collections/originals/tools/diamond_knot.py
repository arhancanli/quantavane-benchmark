"""Short knotted rings in the diamond lattice (our own code, Quantavane Originals, problem diamond-knot).

  python3 -I diamond_knot.py SCALE SECONDS SEED OUT

Start from the trefoil curve (sin t + 2 sin 2t, cos t - 2 cos 2t, -sin 3t), scaled by SCALE, routed through sites of
the diamond lattice by shortest lattice paths; then shorten: replace a window of the ring by a shorter lattice path
between its ends through free sites (breadth-first search), keeping the ring knotted (knot determinant > 1, computed by
knot_determinant of checkers/orig_chem.py); between rounds, random moves replace a window by another path of the same
length. The shortest ring found is written to OUT as lines "x y z"."""
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "checkers"))
from orig_chem import knot_determinant

STEPS = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def nbrs(p):
    s = 1 if p[0] % 2 == 0 else -1
    return [(p[0] + s * a, p[1] + s * b, p[2] + s * c) for a, b, c in STEPS]


def nearest_site(x, y, z):
    best = None
    for a in range(int(math.floor(x)) - 2, int(math.floor(x)) + 3):
        for b in range(int(math.floor(y)) - 2, int(math.floor(y)) + 3):
            for c in range(int(math.floor(z)) - 2, int(math.floor(z)) + 3):
                ok = (a % 2 == 0 and b % 2 == 0 and c % 2 == 0 and (a + b + c) % 4 == 0) or (a % 2 and b % 2 and c % 2 and (a + b + c) % 4 == 3)
                if ok:
                    dd = (a - x) ** 2 + (b - y) ** 2 + (c - z) ** 2
                    if best is None or dd < best[0]:
                        best = (dd, (a, b, c))
    return best[1]


def bfs_path(src, dst, blocked, maxlen):
    if src == dst:
        return [src]
    prev = {src: None}
    frontier = [src]
    for depth in range(maxlen):
        nxt = []
        for p in frontier:
            for q in nbrs(p):
                if q in prev or (q in blocked and q != dst):
                    continue
                prev[q] = p
                if q == dst:
                    path = [q]
                    while prev[path[-1]] is not None:
                        path.append(prev[path[-1]])
                    return path[::-1]
                nxt.append(q)
        frontier = nxt
    return None


def initial(scale, rng):
    f = lambda t: (math.sin(t) + 2 * math.sin(2 * t), math.cos(t) - 2 * math.cos(2 * t), -math.sin(3 * t))
    targets = []
    for k in range(60):
        x, y, z = f(2 * math.pi * k / 60)
        s = nearest_site(scale * x, scale * y, scale * z)
        if not targets or s != targets[-1]:
            targets.append(s)
    poly = [targets[0]]
    used = {targets[0]}
    for k in range(1, len(targets) + 1):
        dst = targets[k % len(targets)]
        if dst in used and k < len(targets):
            continue
        path = bfs_path(poly[-1], dst, used - ({dst} if k == len(targets) else set()), 60)
        if path is None:
            return None
        for q in path[1:]:
            if k == len(targets) and q == targets[0]:
                break
            poly.append(q)
            used.add(q)
    if poly[0] not in nbrs(poly[-1]) or len(set(poly)) != len(poly):
        return None
    return poly


def shorten(poly, rng, deadline):
    improved = True
    while improved and time.time() < deadline:
        improved = False
        n = len(poly)
        for L in range(2, min(14, n // 2)):
            starts = list(range(n))
            rng.shuffle(starts)
            for i in starts:
                j = (i + L) % n
                inner = {poly[(i + k) % n] for k in range(1, L)}
                blocked = set(poly) - inner
                path = bfs_path(poly[i], poly[j], blocked, L - 1)
                if path is None or len(path) - 1 >= L:
                    continue
                if j > i:
                    new = poly[:i + 1] + path[1:-1] + poly[j:]
                else:                                  # the window wraps around the start of the list
                    new = poly[j:i + 1] + path[1:-1]
                if len(set(new)) != len(new):
                    continue
                if knot_determinant(new) > 1:
                    poly = new
                    improved = True
                    break
            if improved:
                break
    return poly


def wiggle(poly, rng, tries=200):
    """Replace a random window by a random different path of the same length through free sites."""
    n = len(poly)
    for _ in range(tries):
        L = rng.choice([4, 6, 8])
        i = rng.randrange(n)
        j = (i + L) % n
        inner = {poly[(i + k) % n] for k in range(1, L)}
        blocked = set(poly) - inner
        path = [poly[i]]
        ok = True
        for step in range(L - 1):
            opts = [q for q in nbrs(path[-1]) if q not in blocked and q not in path]
            if not opts:
                ok = False
                break
            path.append(rng.choice(opts))
        if not ok or poly[j] not in nbrs(path[-1]):
            continue
        path.append(poly[j])
        if j > i:
            new = poly[:i + 1] + path[1:-1] + poly[j:]
        else:
            new = poly[j:i + 1] + path[1:-1]
        if len(new) == n and len(set(new)) == n and new != poly and knot_determinant(new) > 1:
            return new
    return poly


def main():
    scale, secs, seed, out = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    poly = None
    while poly is None:
        poly = initial(scale, rng)
        scale *= 1.1
    assert knot_determinant(poly) > 1, "the routed curve is not knotted"
    print("start", len(poly), flush=True)
    deadline = time.time() + secs
    best = list(poly)
    while time.time() < deadline:
        poly = shorten(poly, rng, deadline)
        if len(poly) < len(best):
            best = list(poly)
            print("best", len(best), flush=True)
            with open(out, "w") as f:
                f.write("".join(f"{x} {y} {z}\n" for x, y, z in best))
        for _ in range(rng.randrange(1, 6)):
            poly = wiggle(poly, rng)
        if rng.random() < 0.05:
            poly = list(best)
    print("final", len(best))


if __name__ == "__main__":
    main()
