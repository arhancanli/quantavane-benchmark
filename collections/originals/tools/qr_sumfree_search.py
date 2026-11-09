"""Large sum-free subsets of the quadratic residues modulo p (our own code, Quantavane Originals).

  python3 -I qr_sumfree_search.py P SECONDS SEED OUT.txt

A subset A of the nonzero squares mod P is sum-free when a + b = c (mod P) has no solution with a, b, c in A (a = b
allowed). Randomized greedy construction, then local search: remove one or two elements and re-add greedily in
random order; keep the largest set found. Our own code; lower bounds only."""
import random
import sys
import time


def main():
    p, secs, seed, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    Q = sorted({x * x % p for x in range(1, p)})

    def fits(x, S):
        if (2 * x) % p in S:
            return False
        for a in S:
            if (a + x) % p in S or (x - a) % p in S or (a - x) % p in S or (2 * a) % p == x or (a + x) % p == x:
                return False
        return True

    def extend(S):
        order = Q[:]
        rng.shuffle(order)
        for x in order:
            if x not in S and fits(x, S):
                S.add(x)
        return S
    best = set()
    cur = extend(set())
    t0 = time.time()
    while time.time() - t0 < secs:
        if len(cur) > len(best):
            best = set(cur)
        trial = set(cur)
        for _ in range(rng.choice((1, 1, 2, 3))):
            if trial:
                trial.discard(rng.choice(sorted(trial)))
        trial = extend(trial)
        if len(trial) >= len(cur) or rng.random() < 0.02:
            cur = trial
    if len(cur) > len(best):
        best = cur
    with open(out, "w") as f:
        f.write(f"# sum-free subset of the quadratic residues mod {p}: {len(best)} elements\n" + " ".join(map(str, sorted(best))) + "\n")
    print(p, len(best))


if __name__ == "__main__":
    main()
