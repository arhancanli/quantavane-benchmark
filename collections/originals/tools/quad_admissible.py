"""Admissible sets for the quadratic family n^2 + h (our own code, Quantavane Originals).

  python3 -I quad_admissible.py KMAX

A set H of positive integers is admissible for n^2 + h if for every prime p some n has n^2 + h != 0 (mod p) for all h
in H, i.e. the residues -h (mod p) miss a square class (one of the (p+1)/2 values of n^2 mod p, 0 included). Only
p <= 2|H| - 1 can fail. For each k this prints the least m such that an admissible k-set of integers in [1, m]
exists, with one such set (exhaustive depth-first search over sets with largest element m, m increasing)."""
import sys


def primes(n):
    return [p for p in range(2, n + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def main():
    kmax = int(sys.argv[1])
    m = 1
    for k in range(1, kmax + 1):
        ps = primes(max(2, 2 * k - 1))
        sqs = {p: sorted({(x * x) % p for x in range(p)}) for p in ps}
        while True:
            # sets with largest element m: choose k-1 others in [1, m-1]; track, for each p, which square classes
            # are hit (a class s is hit by h when s = -h mod p)
            found = None
            hit = {p: {} for p in ps}

            def add(h, d):
                for p in ps:
                    s = (-h) % p
                    if s in hit[p] or True:
                        hit[p][s] = hit[p].get(s, 0) + d
                        if hit[p][s] == 0:
                            del hit[p][s]

            def ok():
                return all(len([s for s in sqs[p] if s in hit[p]]) < len(sqs[p]) for p in ps)

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


if __name__ == "__main__":
    main()
