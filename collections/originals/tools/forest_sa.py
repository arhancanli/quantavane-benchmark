"""Large induced forests (small decycling sets) by simulated annealing (our own code, Quantavane Originals).

  python3 -I forest_sa.py EDGES SECONDS SEED OUT.txt

State: a vertex set S inducing a forest. Move: add a random vertex v outside S; if S + v has cycles, remove random
vertices of S adjacent to v (other than one chosen neighbour) until it is a forest again; accept by the Metropolis
rule on |S|. Writes the largest S found, one vertex per line."""
import math
import random
import sys
import time


def main():
    path, secs, seed, out = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    f = open(path)
    n, m = map(int, f.readline().split())
    adj = [set() for _ in range(n)]
    for line in f:
        a, b = map(int, line.split())
        adj[a].add(b)
        adj[b].add(a)
    rng = random.Random(seed)

    def acyclic(S):
        parent = {v: v for v in S}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for v in S:
            for u in adj[v]:
                if u in S and u < v:
                    a, b = find(u), find(v)
                    if a == b:
                        return False
                    parent[a] = b
        return True

    S = set()
    best = set()
    t0 = time.time()
    T = 1.0
    while time.time() - t0 < secs:
        v = rng.randrange(n)
        if v in S:
            continue
        S2 = set(S)
        S2.add(v)
        nb = [u for u in adj[v] if u in S2]
        rng.shuffle(nb)
        while not acyclic(S2) and nb:
            S2.discard(nb.pop())
        if not acyclic(S2):
            continue
        d = len(S2) - len(S)
        if d >= 0 or rng.random() < math.exp(d / T):
            S = S2
            if len(S) > len(best):
                best = set(S)
        T = max(0.05, T * 0.99995)
    with open(out, "w") as fh:
        fh.write(f"# induced forest with {len(best)} vertices\n" + "".join(f"{v}\n" for v in sorted(best)))
    print(len(best))


if __name__ == "__main__":
    main()
