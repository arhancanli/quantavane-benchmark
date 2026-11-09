"""HP lattice proteins on the triangular lattice for the Fibonacci words (our own code, Quantavane Originals).

  python3 -I hp_tri.py exact N              exhaustive search over self-avoiding conformations (N <= 14)
  python3 -I hp_tri.py anneal N SECONDS SEED OUT.txt    simulated annealing with pivot and local moves

The sequence of length N = F_k is the Fibonacci word: S_1 = P, S_2 = H, S_k = S_(k-1) S_(k-2) (H hydrophobic,
P polar). A conformation puts monomer i on a site (a_i, b_i) of the triangular lattice (the point a + b e^(i pi/3)),
consecutive monomers on neighbouring sites (differences (1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)), all sites
distinct. The energy is minus the number of pairs of H monomers that are lattice neighbours but not consecutive."""
import math
import random
import sys
import time

DIRS = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]


def fib_word(n):
    a, b = "P", "H"
    while len(b) < n:
        a, b = b, b + a
    if len(b) != n:
        raise ValueError(f"{n} is not a Fibonacci number >= 1")
    return b


def energy(seq, pos):
    where = {p: i for i, p in enumerate(pos)}
    e = 0
    for i, p in enumerate(pos):
        if seq[i] != "H":
            continue
        for dx, dy in DIRS:
            j = where.get((p[0] + dx, p[1] + dy))
            if j is not None and j > i + 1 and seq[j] == "H":
                e -= 1
    return e


def exact(n):
    seq = fib_word(n)
    best = [1, None]
    pos = [(0, 0), (1, 0)]
    occ = {(0, 0): 0, (1, 0): 1}

    def contacts(i, p):
        c = 0
        if seq[i] == "H":
            for dx, dy in DIRS:
                j = occ.get((p[0] + dx, p[1] + dy))
                if j is not None and j < i - 1 and seq[j] == "H":
                    c += 1
        return c
    hs_left = [sum(1 for c in seq[i:] if c == "H") for i in range(n + 1)]

    def rec(e, turned):
        i = len(pos)
        if i == n:
            if e < best[0]:
                best[0], best[1] = e, list(pos)
            return
        # bound: each remaining H gains at most 4 new contacts (6 neighbours minus 2 chain neighbours)
        if e - 4 * hs_left[i] >= best[0]:
            return
        x, y = pos[-1]
        for k, (dx, dy) in enumerate(DIRS):
            p = (x + dx, y + dy)
            if p in occ:
                continue
            if not turned and k not in (0, 1, 2, 3):   # mirror symmetry: the first turn goes left (or straight)
                pass
            occ[p] = i
            pos.append(p)
            rec(e - contacts(i, p), turned or k != 0)
            pos.pop()
            del occ[p]
    rec(0, False)
    return seq, best[0], best[1]


def anneal(n, secs, seed):
    seq = fib_word(n)
    rng = random.Random(seed)
    pos = [(i, 0) for i in range(n)]
    e = energy(seq, pos)
    best = (e, list(pos))
    t0 = time.time()
    T = 2.0
    rot = [lambda x, y: (x, y), lambda x, y: (-y, x + y), lambda x, y: (-x - y, x), lambda x, y: (-x, -y),
           lambda x, y: (y, -x - y), lambda x, y: (x + y, -x)]          # rotations by 0, 60, ..., 300 degrees
    while time.time() - t0 < secs:
        k = rng.randrange(1, n - 1)
        r = rng.choice(rot[1:])
        cx, cy = pos[k]
        if rng.random() < 0.5:
            new = pos[:k + 1] + [(cx + r(x - cx, y - cy)[0], cy + r(x - cx, y - cy)[1]) for x, y in pos[k + 1:]]
        else:
            new = [(cx + r(x - cx, y - cy)[0], cy + r(x - cx, y - cy)[1]) for x, y in pos[:k]] + pos[k:]
        if len(set(new)) != n:
            continue
        e2 = energy(seq, new)
        if e2 <= e or rng.random() < math.exp(-(e2 - e) / T):
            pos, e = new, e2
            if e < best[0]:
                best = (e, list(pos))
        T = max(0.15, T * 0.99995)
    return seq, best[0], best[1]


def main():
    if sys.argv[1] == "exact":
        seq, e, pos = exact(int(sys.argv[2]))
        print(len(seq), seq, e)
        return
    n, secs, seed, out = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    seq, e, pos = anneal(n, secs, seed)
    with open(out, "w") as f:
        f.write(f"# Fibonacci HP chain of length {n} ({seq}) on the triangular lattice: energy {e}\n")
        f.write("".join(f"{a} {b}\n" for a, b in pos))
    print(n, e)


if __name__ == "__main__":
    main()
