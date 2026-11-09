"""Step-function upper bounds for the minimum overlap constant of the square (our own code, Quantavane Originals).

  python3 -I overlap2d.py M ITERS SEED DEN OUT.txt [START.txt]

A step function f on [0,2]^2 with values f_i in [0,1] on the M x M cells of side 2/M and integral 2 (sum of f_i equal
to M^2/2) has overlap M(f) = sup_x integral f(t) (1 - f)(t - x) dt = (2/M)^2 max_k sum_i f_i g_(i-k), g = 1 - f on the
square and 0 outside (the cross-correlation of two step functions is bilinear on each grid cell, so its maximum is at
a grid point). This program lowers the maximum by projected gradient steps on a log-sum-exp smoothing, keeping
0 <= f <= 1 and the sum fixed, then rounds f to multiples of 1/DEN with the exact sum (the certificate)."""
import math
import random
import sys


def xcorr(f, m):
    g = [[1.0 - v for v in row] for row in f]
    n = 2 * m - 1
    c = [[0.0] * n for _ in range(n)]       # c[k1+m-1][k2+m-1] = sum_i f[i] g[i-k]
    for i1 in range(m):
        for i2 in range(m):
            v = f[i1][i2]
            if v == 0:
                continue
            for j1 in range(m):
                row = c[i1 - j1 + m - 1]
                gj = g[j1]
                for j2 in range(m):
                    row[i2 - j2 + m - 1] += v * gj[j2]
    return c


def value(f, m):
    return (2.0 / m) ** 2 * max(map(max, xcorr(f, m)))


def project(f, m, total):
    """Project onto {0 <= f <= 1, sum f = total} by bisection on a shift."""
    flat = [v for row in f for v in row]
    lo, hi = -2.0, 2.0
    for _ in range(60):
        mid = (lo + hi) / 2
        s = sum(min(1.0, max(0.0, v - mid)) for v in flat)
        if s > total:
            lo = mid
        else:
            hi = mid
    return [[min(1.0, max(0.0, v - hi)) for v in row] for row in f]


def main():
    m, iters, seed, den, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = random.Random(seed)
    total = m * m / 2
    if len(sys.argv) > 6:
        f = [[float(x) / den for x in line.split()] for line in open(sys.argv[6]) if line.strip() and not line.startswith("#")]
    else:
        f = [[0.5 + 0.3 * (rng.random() - 0.5) for _ in range(m)] for _ in range(m)]
    f = project(f, m, total)
    best = (value(f, m), [r[:] for r in f])
    n = 2 * m - 1
    for it in range(iters):
        c = xcorr(f, m)
        mx = max(map(max, c))
        beta = 20.0 * (1 + 40.0 * it / iters)
        w = [[math.exp(beta * (c[a][b] / mx - 1.0)) for b in range(n)] for a in range(n)]
        z = sum(map(sum, w))
        g = [[1.0 - v for v in row] for row in f]
        grad = [[0.0] * m for _ in range(m)]
        # d/df_i of sum_k w_k sum_j f_j g_(j-k):  sum_k w_k g_(i-k)  -  sum_k w_k f_(i+k)  (g = 1 - f inside the square)
        for i1 in range(m):
            for i2 in range(m):
                acc = 0.0
                for j1 in range(m):
                    wr = w[i1 - j1 + m - 1]
                    for j2 in range(m):
                        acc += wr[i2 - j2 + m - 1] * g[j1][j2]
                    wr2 = w[j1 - i1 + m - 1]
                    fj = f[j1]
                    for j2 in range(m):
                        acc -= wr2[j2 - i2 + m - 1] * fj[j2]
                grad[i1][i2] = acc / z
        gm = max(abs(v) for row in grad for v in row) or 1.0
        eta = 0.08 / (1 + 3.0 * it / iters)
        f = project([[f[a][b] - eta * grad[a][b] / gm for b in range(m)] for a in range(m)], m, total)
        v = value(f, m)
        if v < best[0]:
            best = (v, [r[:] for r in f])
        if it % 100 == 0:
            print(it, round(v, 6), round(best[0], 6), flush=True)
    f = best[1]
    # round to multiples of 1/den keeping the exact sum den * m^2 / 2
    target = den * m * m // 2
    q = [[int(round(v * den)) for v in row] for row in f]
    diff = target - sum(map(sum, q))
    cells = sorted(((f[a][b] * den - q[a][b], a, b) for a in range(m) for b in range(m)), reverse=(diff > 0))
    for r, a, b in cells:
        if diff == 0:
            break
        step = 1 if diff > 0 else -1
        if 0 <= q[a][b] + step <= den:
            q[a][b] += step
            diff -= step
    with open(out, "w") as fh:
        fh.write(f"# {m} x {m} step function on [0,2]^2, values = entries / {den}; float overlap {best[0]:.9f}\n")
        for row in q:
            fh.write(" ".join(map(str, row)) + "\n")
    print("best", best[0])


if __name__ == "__main__":
    main()
