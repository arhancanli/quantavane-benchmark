"""q-state Potts antiferromagnet (fewest monochromatic edges in a q-colouring) by simulated annealing (our own code).

  python3 -I potts.py EDGES Q SWEEPS RESTARTS SEED OUT.txt
EDGES: first line "n m", then m lines "u v". Writes the colouring (one colour 0..Q-1 per vertex, in order) and prints
the number of monochromatic edges."""
import math
import random
import sys


def main():
    path, q, sweeps, restarts, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    f = open(path)
    n, m = map(int, f.readline().split())
    adj = [[] for _ in range(n)]
    E = []
    for line in f:
        a, b = map(int, line.split())
        adj[a].append(b)
        adj[b].append(a)
        E.append((a, b))
    rng = random.Random(seed)
    best, bestc = None, None
    for r in range(restarts):
        c = [rng.randrange(q) for _ in range(n)]
        mono = sum(1 for a, b in E if c[a] == c[b])
        cur_best, cur_c = mono, c[:]
        for s in range(sweeps):
            T = 2.0 * (0.02 / 2.0) ** (s / max(1, sweeps - 1))
            for _ in range(n):
                v = rng.randrange(n)
                new = rng.randrange(q - 1)
                if new >= c[v]:
                    new += 1
                d = sum(1 for u in adj[v] if c[u] == new) - sum(1 for u in adj[v] if c[u] == c[v])
                if d <= 0 or rng.random() < math.exp(-d / T):
                    c[v] = new
                    mono += d
                    if mono < cur_best:
                        cur_best, cur_c = mono, c[:]
        if best is None or cur_best < best:
            best, bestc = cur_best, cur_c
    assert best == sum(1 for a, b in E if bestc[a] == bestc[b])
    with open(out, "w") as fh:
        fh.write(f"# {q}-colouring with {best} monochromatic edges\n" + " ".join(map(str, bestc)) + "\n")
    print(q, best)


if __name__ == "__main__":
    main()
