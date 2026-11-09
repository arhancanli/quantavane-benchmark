"""Small catenanes in the diamond lattice (our own code, Quantavane Originals, problem diamond-link).

  python3 -I diamond_link.py SCALE SECONDS SEED OUT

Two linked circles (a Hopf link: one in the plane z = 0 around the origin, one in the plane y = 0 around (SCALE, 0, 0))
are routed through sites of the diamond lattice by shortest lattice paths, the second avoiding the first; then each
ring is shortened in turn by replacing a window with a shorter lattice path through free sites (breadth-first search),
keeping the rings disjoint and linked (linking number of checkers/orig_chem.py not zero), with random same-length moves
between rounds. The smallest pair found is written to OUT (first ring, a line '-', second ring)."""
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "checkers"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orig_chem import linking_number
from diamond_knot import nbrs, nearest_site, bfs_path


def route(f, scale, avoid):
    targets = []
    for k in range(48):
        s = nearest_site(*(scale * c for c in f(2 * math.pi * k / 48)))
        if s not in avoid and (not targets or s != targets[-1]):
            targets.append(s)
    ring, used = [targets[0]], set(avoid) | {targets[0]}
    for k in range(1, len(targets) + 1):
        dst = targets[k % len(targets)]
        if dst in used and k < len(targets):
            continue
        path = bfs_path(ring[-1], dst, used - ({dst} if k == len(targets) else set()), 80)
        if path is None:
            return None
        for q in path[1:]:
            if k == len(targets) and q == targets[0]:
                break
            ring.append(q)
            used.add(q)
    if ring[0] not in nbrs(ring[-1]) or len(set(ring)) != len(ring):
        return None
    return ring


def replace_window(ring, i, L, path):
    n = len(ring)
    j = (i + L) % n
    return ring[:i + 1] + path[1:-1] + ring[j:] if j > i else ring[j:i + 1] + path[1:-1]


def shorten(rings, k, rng, deadline):
    ring, other = rings[k], rings[1 - k]
    improved = True
    while improved and time.time() < deadline:
        improved = False
        n = len(ring)
        for L in range(2, min(14, n // 2)):
            starts = list(range(n))
            rng.shuffle(starts)
            for i in starts:
                inner = {ring[(i + t) % n] for t in range(1, L)}
                blocked = (set(ring) - inner) | set(other)
                path = bfs_path(ring[i], ring[(i + L) % n], blocked, L - 1)
                if path is None or len(path) - 1 >= L:
                    continue
                new = replace_window(ring, i, L, path)
                if len(set(new)) == len(new) and linking_number(new, other) != 0:
                    ring = new
                    improved = True
                    break
            if improved:
                break
    rings[k] = ring
    return rings


def wiggle(rings, k, rng, tries=100):
    ring, other = rings[k], rings[1 - k]
    n = len(ring)
    for _ in range(tries):
        L = rng.choice([4, 6])
        i = rng.randrange(n)
        inner = {ring[(i + t) % n] for t in range(1, L)}
        blocked = (set(ring) - inner) | set(other)
        path = [ring[i]]
        for step in range(L - 1):
            opts = [q for q in nbrs(path[-1]) if q not in blocked and q not in path]
            if not opts:
                break
            path.append(rng.choice(opts))
        if len(path) != L or ring[(i + L) % n] not in nbrs(path[-1]):
            continue
        path.append(ring[(i + L) % n])
        new = replace_window(ring, i, L, path)
        if len(new) == n and len(set(new)) == n and new != ring and linking_number(new, other) != 0:
            rings[k] = new
            return rings
    return rings


def main():
    scale, secs, seed, out = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    rings = None
    while rings is None:
        a = route(lambda t: (math.cos(t), math.sin(t), 0.0), scale, set())
        b = route(lambda t: (1 + math.cos(t), 0.0, math.sin(t)), scale, set(a)) if a else None
        rings = [a, b] if a and b and linking_number(a, b) != 0 else None
        scale *= 1.1
    deadline = time.time() + secs
    best = [list(rings[0]), list(rings[1])]
    print("start", len(best[0]) + len(best[1]), flush=True)
    while time.time() < deadline:
        for k in (0, 1):
            rings = shorten(rings, k, rng, deadline)
        if len(rings[0]) + len(rings[1]) < len(best[0]) + len(best[1]):
            best = [list(rings[0]), list(rings[1])]
            print("best", len(best[0]) + len(best[1]), len(best[0]), len(best[1]), flush=True)
            with open(out, "w") as f:
                f.write("".join(f"{x} {y} {z}\n" for x, y, z in best[0]) + "-\n" + "".join(f"{x} {y} {z}\n" for x, y, z in best[1]))
        for _ in range(rng.randrange(1, 5)):
            rings = wiggle(rings, rng.randrange(2), rng)
        if rng.random() < 0.05:
            rings = [list(best[0]), list(best[1])]
    print("final", len(best[0]) + len(best[1]))


if __name__ == "__main__":
    main()
