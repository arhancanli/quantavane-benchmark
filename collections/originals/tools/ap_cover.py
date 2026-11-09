"""Pair coverings of Z_v by arithmetic progressions (our own code, Quantavane Originals).

  python3 -I ap_cover.py exact V K [NODECAP]        least number of k-term progressions covering all pairs (search)
  python3 -I ap_cover.py search V K SECONDS SEED OUT.txt

A block is a k-term progression {a, a+d, ..., a+(k-1)d} in Z_v with k distinct elements. exact: depth-first search
over blocks containing the least uncovered pair, with the bound uncovered / C(k,2), iterative deepening on the number
of blocks. search: greedy (the block covering most uncovered pairs, ties at random) followed by a local search that
removes a block and repairs greedily. Writes the blocks as 'a d' lines."""
import itertools
import random
import sys
import time


def blocks(v, k):
    out = set()
    for d in range(1, v):
        for a in range(v):
            b = tuple(sorted((a + i * d) % v for i in range(k)))
            if len(set(b)) == k:
                out.add((b, (a, d)))
    seen = {}
    for b, ad in out:
        seen.setdefault(b, ad)
    return [(b, seen[b]) for b in sorted(seen)]


def pairs_of(b):
    return [(x, y) for x, y in itertools.combinations(b, 2)]


def exact(v, k, cap):
    B = blocks(v, k)
    pidx = {p: i for i, p in enumerate(itertools.combinations(range(v), 2))}
    bp = [frozenset(pidx[p] for p in pairs_of(b)) for b, _ in B]
    by_pair = {}
    for i, s in enumerate(bp):
        for p in s:
            by_pair.setdefault(p, []).append(i)
    allp = frozenset(range(len(pidx)))
    per = k * (k - 1) // 2
    nodes = [0]

    def rec(unc, left, chosen):
        nodes[0] += 1
        if nodes[0] > cap:
            return None
        if not unc:
            return chosen
        if left == 0 or len(unc) > left * per:
            return None
        p = min(unc)
        for i in by_pair[p]:
            r = rec(unc - bp[i], left - 1, chosen + [i])
            if r:
                return r
        return None
    lb = -(-len(pidx) // per)
    for m in range(lb, len(pidx) + 1):
        r = rec(allp, m, [])
        if nodes[0] > cap:
            return None, m, nodes[0]
        if r:
            return [B[i][1] for i in r], m, nodes[0]


def search(v, k, secs, seed):
    rng = random.Random(seed)
    B = blocks(v, k)
    pidx = {p: i for i, p in enumerate(itertools.combinations(range(v), 2))}
    bp = [[pidx[p] for p in pairs_of(b)] for b, _ in B]
    npairs = len(pidx)

    def greedy(cover, chosen):
        cnt = cover[:]
        unc = sum(1 for c in cnt if c == 0)
        while unc:
            best, arg = -1, []
            for i, s in enumerate(bp):
                g = sum(1 for p in s if cnt[p] == 0)
                if g > best:
                    best, arg = g, [i]
                elif g == best:
                    arg.append(i)
            i = rng.choice(arg)
            chosen.append(i)
            for p in bp[i]:
                if cnt[p] == 0:
                    unc -= 1
                cnt[p] += 1
        return chosen, cnt
    chosen, cnt = greedy([0] * npairs, [])
    best = list(chosen)
    t0 = time.time()
    while time.time() - t0 < secs:
        trial = list(best)
        for _ in range(rng.choice((1, 2, 2, 3))):
            trial.pop(rng.randrange(len(trial)))
        c = [0] * npairs
        for i in trial:
            for p in bp[i]:
                c[p] += 1
        trial, c = greedy(c, trial)
        # drop redundant blocks
        for i in list(trial):
            if all(c[p] > 1 for p in bp[i]):
                trial.remove(i)
                for p in bp[i]:
                    c[p] -= 1
        if len(trial) <= len(best):
            best = trial
    return [B[i][1] for i in best]


def main():
    if sys.argv[1] == "exact":
        v, k = int(sys.argv[2]), int(sys.argv[3])
        cap = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 7
        r, m, nodes = exact(v, k, cap)
        print(v, k, m if r else f">= {m} (node cap)", nodes, r if r else "")
        return
    v, k, secs, seed, out = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    r = search(v, k, secs, seed)
    with open(out, "w") as f:
        f.write(f"# {len(r)} {k}-term progressions covering every pair of Z_{v} (lines: start a, difference d)\n")
        f.write("".join(f"{a} {d}\n" for a, d in r))
    print(v, k, len(r))


if __name__ == "__main__":
    main()
