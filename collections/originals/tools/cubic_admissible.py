"""Admissible sets for the cubic family n^3 + h (our own code, Quantavane Originals).

  python3 -I cubic_admissible.py exact KMAX
  python3 -I cubic_admissible.py sieve K TRIALS SEED OUT.txt

H (positive integers) is admissible for n^3 + h if for every prime p some n has n^3 + h != 0 (mod p) for all h in H,
i.e. the residues -h miss one of the values of n^3 (mod p), 0 included: all p residues when p = 3 or p = 2 (mod 3), and
(p + 2)/3 of them when p = 1 (mod 3). Only primes p <= 3K - 2 can fail. exact: least m with an admissible K-set in
[1, m] (depth-first search over sets with largest element m, m increasing). sieve: randomized greedy sieve as in
quad_sieve.py (for each prime delete the h whose -h lies in the least used cube class), K smallest survivors."""
import random
import sys


def primes(n):
    return [p for p in range(2, n + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def cubes(p):
    return sorted({x ** 3 % p for x in range(p)})


def admissible(H):
    for p in primes(max(2, 3 * len(H) - 2)):
        if set(cubes(p)) <= {(-h) % p for h in H}:
            return False
    return True


def exact(kmax):
    m = 1
    for k in range(1, kmax + 1):
        ps = primes(max(2, 3 * k - 2))
        cs = {p: cubes(p) for p in ps}
        while True:
            hit = {p: {} for p in ps}

            def add(h, d):
                for p in ps:
                    s = (-h) % p
                    hit[p][s] = hit[p].get(s, 0) + d
                    if hit[p][s] == 0:
                        del hit[p][s]

            def ok():
                return all(any(c not in hit[p] for c in cs[p]) for p in ps)
            found = None
            chosen = [m]
            add(m, 1)

            def rec(start):
                nonlocal found
                if found:
                    return
                if len(chosen) == k:
                    found = sorted(chosen)
                    return
                for h in range(start, 0, -1):
                    if len(chosen) + h < k:
                        return
                    add(h, 1)
                    if ok():
                        chosen.append(h)
                        rec(h - 1)
                        chosen.pop()
                    add(h, -1)
                    if found:
                        return
            if ok():
                rec(m - 1)
            if found:
                print(k, m, " ".join(map(str, found)), flush=True)
                break
            m += 1


def sieve(k, trials, seed, out):
    ps = primes(max(2, 3 * k - 2))
    rng = random.Random(seed)
    best = None
    for t in range(trials):
        lo, hi, got = k, 60 * k + 50, None
        while lo < hi:
            mid = (lo + hi) // 2
            r2 = random.Random(t * 7919 + seed)
            hs = list(range(1, mid + 1))
            okk = True
            for p in ps:
                cl = cubes(p)
                cnt = {c: sum(1 for h in hs if (-h) % p == c) for c in cl}
                low = min(cnt.values())
                c = r2.choice([x for x in cl if cnt[x] == low])
                hs = [h for h in hs if (-h) % p != c]
                if len(hs) < k:
                    okk = False
                    break
            if okk:
                hi, got = mid, hs[:k]
            else:
                lo = mid + 1
        if got and admissible(got) and (best is None or max(got) < max(best)):
            best = got
    with open(out, "w") as f:
        f.write(f"# admissible {k}-set for n^3 + h with largest element {max(best)}\n" + " ".join(map(str, best)) + "\n")
    print(k, max(best))


if __name__ == "__main__":
    if sys.argv[1] == "exact":
        exact(int(sys.argv[2]))
    else:
        sieve(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
