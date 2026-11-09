"""Step-function upper bounds for the three-part minimum overlap constant (our own code, Quantavane Originals).

  python3 -I overlap3.py M ITERS SEED DEN OUT.txt

Three step functions f_1, f_2, f_3 on [0,3] with M cells of width 3/M (M divisible by 3), values in [0,1],
f_1 + f_2 + f_3 = 1 on every cell and each of integral 1 (column sums M/3). The overlap of parts a != b at shift x is
the integral of f_a(t) f_b(t - x) dt; on a common grid it is linear between grid shifts, so its maximum is
(3/M) max_k sum_i f_a[i] f_b[i-k]. The program lowers the largest overlap by multiplicative gradient steps on a
log-sum-exp smoothing, rebalancing rows and columns after each step (Sinkhorn), then rounds to multiples of 1/DEN
with exact row and column sums (the certificate: M lines of three integers)."""
import math
import random
import sys


def overlaps(f, m):
    out = []
    for a in range(3):
        for b in range(3):
            if a == b:
                continue
            for k in range(-(m - 1), m):
                s = 0.0
                for i in range(max(0, k), min(m, m + k)):
                    s += f[i][a] * f[i - k][b]
                out.append((s, a, b, k))
    return out


def sinkhorn(f, m, rounds=60):
    for _ in range(rounds):
        f = [[v / sum(r) for v in r] for r in f]
        cols = [sum(f[i][a] for i in range(m)) for a in range(3)]
        f = [[f[i][a] * (m / 3) / cols[a] for a in range(3)] for i in range(m)]
    return [[v / sum(r) for v in r] for r in f]


def main():
    m, iters, seed, den, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = random.Random(seed)
    f = sinkhorn([[0.5 + rng.random() for _ in range(3)] for _ in range(m)], m)
    best = None
    for it in range(iters):
        ov = overlaps(f, m)
        mx = max(o[0] for o in ov)
        val = 3.0 / m * mx
        if best is None or val < best[0]:
            best = (val, [r[:] for r in f])
        beta = 30.0 * (1 + 40.0 * it / iters)
        w = [(math.exp(beta * (o[0] / mx - 1.0)), o) for o in ov]
        z = sum(x for x, _ in w)
        g = [[0.0] * 3 for _ in range(m)]
        for wt, (s, a, b, k) in w:
            if wt < 1e-12:
                continue
            for i in range(max(0, k), min(m, m + k)):
                g[i][a] += wt * f[i - k][b] / z
                g[i - k][b] += wt * f[i][a] / z
        gm = max(max(r) for r in g) or 1.0
        eta = 0.3 / (1 + 3.0 * it / iters)
        f = sinkhorn([[f[i][a] * math.exp(-eta * g[i][a] / gm) for a in range(3)] for i in range(m)], m)
        if it % 200 == 0:
            print(it, round(val, 6), round(best[0], 6), flush=True)
    f = best[1]
    # round: integers in [0, den] with row sums den and column sums den*m/3 (greedy repair)
    q = [[int(round(v * den)) for v in r] for r in f]
    for i in range(m):
        d = den - sum(q[i])
        while d != 0:
            a = max(range(3), key=lambda t: (f[i][t] * den - q[i][t]) * (1 if d > 0 else -1))
            step = 1 if d > 0 else -1
            if 0 <= q[i][a] + step <= den:
                q[i][a] += step
                d -= step
            else:
                break
    target = den * m // 3
    for _ in range(10 * m * den):
        cols = [sum(q[i][a] for i in range(m)) for a in range(3)]
        if cols == [target] * 3:
            break
        hi = max(range(3), key=lambda a: cols[a])
        lo = min(range(3), key=lambda a: cols[a])
        i = max((i for i in range(m) if q[i][hi] > 0 and q[i][lo] < den), key=lambda i: f[i][lo] - f[i][hi])
        q[i][hi] -= 1
        q[i][lo] += 1
    with open(out, "w") as fh:
        fh.write(f"# three-part step function on [0,3], {m} cells, values = entries / {den}; float overlap {best[0]:.9f}\n")
        for r in q:
            fh.write(" ".join(map(str, r)) + "\n")
    print("best", best[0])


if __name__ == "__main__":
    main()
