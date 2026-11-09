"""Large subsets of the triangular grid T_n with all distances distinct, or with all triangle areas distinct (our
own code, Quantavane Originals).

  python3 -I tri_distinct_search.py N SECONDS SEED OUT.txt [areas]

Randomized greedy construction followed by local search: repeatedly remove one or two points and re-add points
greedily (in random order) while every pairwise squared distance da^2 + da*db + db^2 stays distinct (with 'areas':
while every triangle has a nonzero area |da1*db2 - da2*db1| different from all others); keep the largest set found. Writes the points "a b", one per line."""
import random
import sys
import time


def main():
    n, secs, seed, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    areas = len(sys.argv) > 5 and sys.argv[5] == "areas"
    rng = random.Random(seed)
    pts = [(a, b) for a in range(n) for b in range(n - a)]
    d2 = lambda p, q: (p[0] - q[0]) ** 2 + (p[0] - q[0]) * (p[1] - q[1]) + (p[1] - q[1]) ** 2

    def keys(p, cur):
        if areas:
            return [abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])) for i, q in enumerate(cur) for r in cur[i + 1:]]
        return [d2(p, q) for q in cur]

    def extend(cur, used):
        order = pts[:]
        rng.shuffle(order)
        cs = set(cur)
        for p in order:
            if p in cs:
                continue
            ds = keys(p, cur)
            if len(set(ds)) == len(ds) and not any(d in used for d in ds) and not (areas and 0 in ds):
                cur.append(p)
                cs.add(p)
                used.update(ds)
        return cur, used

    best = []
    t0 = time.time()
    cur, used = extend([], set())
    while time.time() - t0 < secs:
        if len(cur) > len(best):
            best = cur[:]
        trial = cur[:]
        for _ in range(rng.choice((1, 1, 2, 3))):
            if trial:
                trial.pop(rng.randrange(len(trial)))
        u = set()
        for i in range(len(trial)):
            u.update(keys(trial[i], trial[:i]))
        trial, u = extend(trial, u)
        if len(trial) >= len(cur) or rng.random() < 0.02:
            cur, used = trial, u
    if len(cur) > len(best):
        best = cur
    with open(out, "w") as f:
        f.write(f"# {len(best)} points of T_{n} with distinct {'triangle areas' if areas else 'distances'}\n")
        for a, b in sorted(best):
            f.write(f"{a} {b}\n")
    print(n, len(best))


if __name__ == "__main__":
    main()
