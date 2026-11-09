"""Identifying codes and induced forests in a graph by simulated annealing (our own code, Quantavane Originals).

  python3 -I graph_sets.py idcode EDGES SECONDS SEED OUT.txt     smallest identifying code found
  python3 -I graph_sets.py forest EDGES SECONDS SEED OUT.txt     largest induced forest found (its complement is a
                                                                  decycling set)
EDGES: first line "n m", then m lines "u v". The answer is written as the list of chosen vertices (one per line)."""
import math
import random
import sys
import time


def load(path):
    f = open(path)
    n, m = map(int, f.readline().split())
    adj = [set() for _ in range(n)]
    for line in f:
        a, b = map(int, line.split())
        adj[a].add(b)
        adj[b].add(a)
    return n, adj


def id_violations(n, closed, C):
    sig = {}
    bad = 0
    for v in range(n):
        s = frozenset(closed[v] & C)
        if not s:
            bad += 1
        sig[s] = sig.get(s, 0) + 1
    bad += sum(c - 1 for s, c in sig.items() if c > 1)
    return bad


def is_forest(n, adj, S):
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


def main():
    mode, path, secs, seed, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    n, adj = load(path)
    rng = random.Random(seed)
    t0 = time.time()
    if mode == "idcode":
        closed = [adj[v] | {v} for v in range(n)]
        best = set(range(n))
        size = n
        while time.time() - t0 < secs:
            # try to find a valid code of size `size - 1` by annealing on violations
            k = size - 1
            C = set(rng.sample(range(n), k))
            viol = id_violations(n, closed, C)
            T = 2.0
            steps = 0
            while viol > 0 and time.time() - t0 < secs and steps < 200000:
                steps += 1
                a = rng.choice(list(C))
                b = rng.choice([v for v in range(n) if v not in C])
                C2 = (C - {a}) | {b}
                v2 = id_violations(n, closed, C2)
                if v2 <= viol or rng.random() < math.exp(-(v2 - viol) / T):
                    C, viol = C2, v2
                T = max(0.05, T * 0.9995)
            if viol == 0:
                best, size = set(C), k
        res = sorted(best)
    else:
        S = set()
        best = set()
        order = list(range(n))
        while time.time() - t0 < secs:
            rng.shuffle(order)
            S = set()
            for v in order:
                if is_forest(n, adj, S | {v}):
                    S.add(v)
            # local improvement: remove one, add two
            improved = True
            while improved and time.time() - t0 < secs:
                improved = False
                outside = [v for v in range(n) if v not in S]
                rng.shuffle(outside)
                for v in list(S):
                    S2 = S - {v}
                    added = [u for u in outside if is_forest(n, adj, S2 | {u})]
                    for i, a in enumerate(added):
                        for b in added[i + 1:]:
                            if is_forest(n, adj, S2 | {a, b}):
                                S = S2 | {a, b}
                                improved = True
                                break
                        if improved:
                            break
                    if improved:
                        break
            if len(S) > len(best):
                best = set(S)
        res = sorted(best)
    with open(out, "w") as f:
        f.write(f"# {mode}: {len(res)} vertices\n" + "".join(f"{v}\n" for v in res))
    print(mode, len(res))


if __name__ == "__main__":
    main()
