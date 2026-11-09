"""Short reset words for the automaton Q_p (x -> x + 1, x -> x^2 mod p) by the greedy pair-merging algorithm.

  python3 -I sync_greedy.py P OUT.txt [TRIES]

For every pair of states the length of a shortest word merging them is computed once (breadth-first search backwards
from the diagonal in the pair automaton). Starting from all states, the algorithm repeatedly picks a pair of current
states with the shortest merging word (ties broken at random over TRIES runs), applies that word to every current
state, and stops at one state (Eppstein's greedy method). Our own code; it gives upper bounds only."""
import random
import sys
from collections import deque


def main():
    p, out = int(sys.argv[1]), sys.argv[2]
    tries = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    f = [lambda x: (x + 1) % p, lambda x: x * x % p]
    pre = [[[] for _ in range(p)] for _ in range(2)]        # preimages
    for l in range(2):
        for x in range(p):
            pre[l][f[l](x)].append(x)
    INF = 10 ** 9
    dist = [[INF] * p for _ in range(p)]
    nxt = [[None] * p for _ in range(p)]
    dq = deque()
    for x in range(p):
        dist[x][x] = 0
        dq.append((x, x))
    while dq:
        u, v = dq.popleft()
        for l in range(2):
            for a in pre[l][u]:
                for b in pre[l][v]:
                    if dist[a][b] == INF:
                        dist[a][b] = dist[u][v] + 1
                        nxt[a][b] = l
                        dq.append((a, b))
    if any(dist[a][b] == INF for a in range(p) for b in range(p)):
        print(p, "not synchronizing")
        return
    best = None
    rng = random.Random(1)
    for t in range(tries):
        S = set(range(p))
        word = []
        while len(S) > 1:
            Sl = list(S)
            m = min(dist[a][b] for i, a in enumerate(Sl) for b in Sl[i + 1:])
            cands = [(a, b) for i, a in enumerate(Sl) for b in Sl[i + 1:] if dist[a][b] == m]
            a, b = rng.choice(cands)
            w = []
            while a != b:
                l = nxt[a][b]
                w.append(l)
                a, b = f[l](a), f[l](b)
            for l in w:
                S = {f[l](x) for x in S}
            word += w
        if best is None or len(word) < len(best):
            best = word
    s = "".join("ab"[l] for l in best)
    with open(out, "w") as fh:
        fh.write(f"# reset word of length {len(s)} for Q_{p} (greedy pair merging)\n{s}\n")
    print(p, len(s))


if __name__ == "__main__":
    main()
