"""Step-function upper bounds for the square autoconvolution constant (our own code, Quantavane Originals).

  python3 -I autoconv2d.py M ITERS SEED OUT.txt [START.txt]

A nonnegative step function f on the square [-1/4, 1/4]^2, constant on the M x M cells of side h = 1/(2M) with
values a[i][j], has ||f*f||_inf / (int f)^2 = 4 M^2 max_u (a*a)[u] / (sum a)^2, where a*a is the discrete
autoconvolution of the array (f*f is bilinear on each cell of its grid, so its maximum is at a grid point, where it
equals h^2 (a*a)[u]). This program lowers that ratio by exponentiated-gradient steps on a log-sum-exp smoothing of the
maximum, then writes the array scaled to integers (the certificate; the checker recomputes the ratio exactly)."""
import math
import random
import sys


def conv(a, m):
    n = 2 * m - 1
    c = [[0.0] * n for _ in range(n)]
    for i in range(m):
        ai = a[i]
        for j in range(m):
            v = ai[j]
            if v == 0:
                continue
            for k in range(m):
                ak = a[k]
                row = c[i + k]
                for l in range(m):
                    row[j + l] += v * ak[l]
    return c


def ratio(a, m):
    s = sum(map(sum, a))
    c = conv(a, m)
    return 4 * m * m * max(map(max, c)) / (s * s)


def main():
    m, iters, seed, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    if len(sys.argv) > 5:
        a = [[float(x) for x in line.split()] for line in open(sys.argv[5]) if line.strip() and not line.startswith("#")]
        assert len(a) == m
    else:
        a = [[1.0 + 0.3 * rng.random() for _ in range(m)] for _ in range(m)]
    s = sum(map(sum, a))
    a = [[v / s for v in row] for row in a]
    best = (ratio(a, m), [row[:] for row in a])
    n = 2 * m - 1
    for it in range(iters):
        c = conv(a, m)
        mx = max(map(max, c))
        beta = 30.0 * (1.0 + 60.0 * it / max(1, iters - 1))
        w = [[math.exp(beta * (c[u][v] / mx - 1.0)) for v in range(n)] for u in range(n)]
        z = sum(map(sum, w))
        # gradient of LSE(c)/... with respect to a[k][l]: 2 * sum_u w[u] a[u-k] / z
        g = [[0.0] * m for _ in range(m)]
        for k in range(m):
            for l in range(m):
                acc = 0.0
                for i in range(m):
                    wi = w[i + k]
                    ai = a[i]
                    for j in range(m):
                        acc += wi[j + l] * ai[j]
                g[k][l] = 2.0 * acc / z
        gm = max(map(max, g))
        eta = 0.15 / (1.0 + 4.0 * it / max(1, iters - 1))
        a = [[a[k][l] * math.exp(-eta * (g[k][l] / gm - 1.0)) for l in range(m)] for k in range(m)]
        s = sum(map(sum, a))
        a = [[v / s for v in row] for row in a]
        r = ratio(a, m)
        if r < best[0]:
            best = (r, [row[:] for row in a])
        if it % 50 == 0:
            print(it, round(r, 6), round(best[0], 6), flush=True)
    a = best[1]
    scale = 10 ** 6 / max(map(max, a))
    ia = [[int(round(v * scale)) for v in row] for row in a]
    with open(out, "w") as f:
        f.write(f"# {m} x {m} step function on [-1/4,1/4]^2 (rows), float ratio {best[0]:.9f}\n")
        for row in ia:
            f.write(" ".join(map(str, row)) + "\n")
    print("best", best[0])


if __name__ == "__main__":
    main()
