"""Colourings of 1..n with no monochromatic solution of a Diophantine equation: the SAT search behind the colouring
problems of the Quantavane Originals (python-sat with CaDiCaL; our own encoding; run with a Python that has pysat).

  python3 colour_sat.py EQUATION K SECONDS OUTDIR

EQUATION is quad-pyth (x^2 + y^2 + z^2 = w^2, x <= y <= z < w) or squares-ap (x^2 + y^2 = 2 z^2, x < z < y). The
numbers are added one at a time (n = 1, 2, ...): each new solution with largest element n adds, for each colour c,
the clause "not all of its elements have colour c"; every number gets at least one colour (a number with several
takes the first), and 1 gets colour 0 (the colours are symmetric). The solver is incremental, so each n costs one
call. Writes OUTDIR/K_n.txt for the largest n found satisfiable (the colouring, one digit per number) and, when the
formula becomes unsatisfiable at n + 1, says so: then n is exact (the answer for K colours). Prints JSON lines."""
import json
import math
import os
import sys
import time

from pysat.solvers import Solver


def quad_pyth_new(w, two_sq):
    """Solutions x <= y <= z < w of x^2 + y^2 + z^2 = w^2 with largest element w."""
    out = []
    for z in range(1, w):
        r = w * w - z * z
        for x, y in two_sq.get(r, ()):
            if y <= z:
                out.append((x, y, z, w))
    return out


def squares_ap_new(y):
    """Solutions x < z < y of x^2 + y^2 = 2 z^2 with largest element y."""
    out = []
    for z in range(1, y):
        r = 2 * z * z - y * y
        if r <= 0:
            continue
        x = math.isqrt(r)
        if x * x == r and x < z:
            out.append((x, z, y))
    return out


def main():
    eq, k, secs, outdir = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    os.makedirs(outdir, exist_ok=True)
    var = lambda i, c: (i - 1) * k + c + 1
    s = Solver(name="cadical195")
    s.add_clause([var(1, 0)])
    two_sq = {}
    t0 = time.time()
    n, last, nsol = 0, 0, 0
    exact = False
    while time.time() - t0 < secs:
        n += 1
        s.add_clause([var(n, c) for c in range(k)])
        if eq == "quad-pyth":
            for x in range(1, n + 1):          # sums x^2 + n^2 for the table of sums of two squares (x <= n)
                two_sq.setdefault(x * x + n * n, []).append((x, n))
            sols = quad_pyth_new(n, two_sq)
        else:
            sols = squares_ap_new(n)
        for S in sols:
            nsol += 1
            for c in range(k):
                s.add_clause([-var(i, c) for i in set(S)])
        if not s.solve():
            exact = True
            break
        model = s.get_model()
        last = n
    if last:
        pos = set(v for v in model if v > 0)
        col = [next(c for c in range(k) if var(i, c) in pos) for i in range(1, last + 1)]
        with open(os.path.join(outdir, f"{k}_{last}.txt"), "w") as f:
            f.write(f"# {eq}, {k} colours: a colouring of 1..{last} with no monochromatic solution"
                    f"{' (the largest: 1..' + str(last + 1) + ' cannot be coloured)' if exact else ''}\n")
            f.write("".join(map(str, col)) + "\n")
    print(json.dumps({"equation": eq, "k": k, "largest_colourable": last, "exact": exact, "solutions": nsol,
                      "seconds": round(time.time() - t0, 1)}), flush=True)


if __name__ == "__main__":
    main()
