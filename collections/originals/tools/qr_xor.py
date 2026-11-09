"""XOR circuits for the quadratic-residue circulant over GF(2) by Paar's greedy method (our own code).

  python3 -I qr_xor.py P TRIES SEED OUT.txt

The matrix Q_P has Q[i][j] = 1 when j - i is a nonzero square modulo P. Every output row is a set of inputs; the
method repeatedly takes the pair of available signals that occurs together in the most rows (ties at random), adds
the gate s = a XOR b, and replaces the pair by s in those rows, until every row is one signal. The best of TRIES runs
is written as: P, the number of gates G, G lines "a b" (signal numbers; inputs are 0..P-1, gate k is P+k-1... in
order), and a last line with the signal number of each output row."""
import random
import sys
from itertools import combinations


def qr_rows(p):
    qr = {x * x % p for x in range(1, p)}
    return [{(i + d) % p for d in qr} for i in range(p)]


def paar(p, rng):
    rows = [set(r) for r in qr_rows(p)]
    gates = []
    nxt = p
    while any(len(r) > 1 for r in rows):
        cnt = {}
        for r in rows:
            if len(r) > 1:
                for a, b in combinations(sorted(r), 2):
                    cnt[(a, b)] = cnt.get((a, b), 0) + 1
        mx = max(cnt.values())
        a, b = rng.choice([k for k, v in cnt.items() if v == mx])
        gates.append((a, b))
        for r in rows:
            if a in r and b in r:
                r.discard(a)
                r.discard(b)
                r.add(nxt)
        nxt += 1
    return gates, [next(iter(r)) for r in rows]


def main():
    p, tries, seed, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    best = None
    for _ in range(tries):
        g, o = paar(p, rng)
        if best is None or len(g) < len(best[0]):
            best = (g, o)
    g, o = best
    with open(out, "w") as f:
        f.write(f"# XOR circuit for the quadratic-residue circulant Q_{p}: {len(g)} gates (Paar's greedy method)\n")
        f.write(f"{p} {len(g)}\n" + "".join(f"{a} {b}\n" for a, b in g) + " ".join(map(str, o)) + "\n")
    print(p, len(g))


if __name__ == "__main__":
    main()
