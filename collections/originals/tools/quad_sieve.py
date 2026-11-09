"""Admissible k-sets for n^2 + h with small largest element, by a randomized greedy sieve (our own code).

  python3 -I quad_sieve.py K TRIALS SEED OUT.txt

Start from [1, M]; for each prime p <= 2K - 1 (in increasing order) choose a square class s mod p (s = n^2 mod p,
0 included) and delete every h with -h = s (mod p), choosing s among those that delete fewest (ties at random); keep
the K smallest survivors. The least M that works is found by bisection for each trial; the best set is written."""
import random
import sys


def primes(n):
    return [p for p in range(2, n + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def sieve(k, M, ps, rng):
    hs = list(range(1, M + 1))
    for p in ps:
        sq = sorted({x * x % p for x in range(p)})
        cnt = {s: sum(1 for h in hs if (-h) % p == s) for s in sq}
        lo = min(cnt.values())
        s = rng.choice([t for t in sq if cnt[t] == lo])
        hs = [h for h in hs if (-h) % p != s]
        if len(hs) < k:
            return None
    return hs[:k]


def admissible(H):
    for p in primes(max(2, 2 * len(H) - 1)):
        sq = {x * x % p for x in range(p)}
        if sq <= {(-h) % p for h in H}:
            return False
    return True


def main():
    k, trials, seed, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    ps = primes(max(2, 2 * k - 1))
    rng = random.Random(seed)
    best = None
    for t in range(trials):
        lo, hi, got = k, 40 * k + 50, None
        while lo < hi:
            mid = (lo + hi) // 2
            r = sieve(k, mid, ps, random.Random(t * 7919 + seed))
            if r:
                hi, got = mid, r
            else:
                lo = mid + 1
        if got and admissible(got) and (best is None or max(got) < max(best)):
            best = got
    with open(out, "w") as f:
        f.write(f"# admissible {k}-set for n^2 + h with largest element {max(best)}\n" + " ".join(map(str, best)) + "\n")
    print(k, max(best))


if __name__ == "__main__":
    main()
