"""Edge 2-colourings with few monochromatic triangles, by simulated annealing (our own code, Quantavane Originals).

  python3 -I mono_triangles.py EDGES SWEEPS SEED OUT.txt

EDGES: first line "n m", then the m edges "u v" (their order numbers the edges 0..m-1). A move flips the colour of
one edge; its effect is read from the triangles through that edge. Writes the colouring as a string of 0 and 1 (one
per edge, in order) and prints the number of monochromatic triangles."""
import math
import random
import sys


def main():
    path, sweeps, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    f = open(path)
    n, m = map(int, f.readline().split())
    E = [tuple(map(int, line.split())) for line in f]
    eid = {}
    adj = [set() for _ in range(n)]
    for i, (a, b) in enumerate(E):
        eid[(a, b)] = eid[(b, a)] = i
        adj[a].add(b)
        adj[b].add(a)
    tri_of = [[] for _ in range(m)]       # for each edge, the pairs of other edges closing a triangle
    for i, (a, b) in enumerate(E):
        for c in adj[a] & adj[b]:
            tri_of[i].append((eid[(a, c)], eid[(b, c)]))
    rng = random.Random(seed)
    col = [rng.randrange(2) for _ in range(m)]
    mono = sum(1 for i in range(m) for x, y in tri_of[i] if col[x] == col[y] == col[i]) // 3
    best, bestc = mono, col[:]
    for s in range(sweeps):
        T = 3.0 * (0.05 / 3.0) ** (s / max(1, sweeps - 1))
        for _ in range(m):
            i = rng.randrange(m)
            c = col[i]
            d = 0
            for x, y in tri_of[i]:
                if col[x] == col[y]:
                    d += -1 if col[x] == c else 1
            if d <= 0 or rng.random() < math.exp(-d / T):
                col[i] = 1 - c
                mono += d
                if mono < best:
                    best, bestc = mono, col[:]
    assert best == sum(1 for i in range(m) for x, y in tri_of[i] if bestc[x] == bestc[y] == bestc[i]) // 3
    with open(out, "w") as fh:
        fh.write(f"# red-blue colouring of the {m} edges with {best} monochromatic triangles\n" + "".join(map(str, bestc)) + "\n")
    print(best)


if __name__ == "__main__":
    main()
