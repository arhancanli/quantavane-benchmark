"""Largest point sets with a pair or triple property in lattice regions: the search behind the lattice problems of
the Quantavane Originals (OR-Tools CP-SAT; our own models; run with a Python that has ortools).

  python3 lattice_sets.py LATTICE-PROPERTY NMIN NMAX SECONDS OUTDIR [WORKERS] [STOP]

For each side N from NMIN to NMAX: builds the 0/1 model of the property on the region of side N (the definitions are
imported from checkers/orig_lattice.py, so the search and the checker agree), solves it with CP-SAT for at most
SECONDS of CP-SAT's deterministic time (a measure of work, about a second each), and writes the best set found to OUTDIR/N.txt with a header line giving the status. The solution for side
N - 1 is the hint for side N (the regions are nested). Prints one JSON line per side: the value, whether CP-SAT proved
it optimal (an exhaustive search: the 'exact' cells) and the best bound it proved. With STOP, the run ends after
STOP sides in a row without a proof of optimality.

Models, x_p = 1 when the point p is chosen:
  distinct   y_pq >= x_p + x_q - 1 for every pair; at most one chosen pair per squared distance.
  isosceles  for every point p and every distance class around p: at most one chosen point in the class if x_p = 1.
  right      not all three of p, q, r for every right angle q-p-r.
  collinear  at most two chosen points on every line with three or more points of the region."""
import importlib.util
import itertools
import json
import os
import sys
import time

from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("orig_lattice", os.path.join(HERE, "checkers", "orig_lattice.py"))
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)


def region(lat, n):
    if lat in ("tri", "hex", "kagome"):
        cand = [(a, b) for a in range(n) for b in range(n - a)]
    elif lat in ("cube", "tetra"):
        cand = list(itertools.product(range(n), repeat=3))
    elif lat == "bcc":
        cand = list(itertools.product(range(2 * n - 1), repeat=3))
    else:
        raise ValueError(lat)
    return [p for p in cand if L.member(lat, n, p)]


def lines(lat, pts):
    """Every line through at least three points of pts, as a list of index lists."""
    idx = {p: i for i, p in enumerate(pts)}
    seen = set()
    out = []
    for i, j in itertools.combinations(range(len(pts)), 2):
        if (i, j) in seen:
            continue
        p, q = pts[i], pts[j]
        u = L.sub(q, p)
        on = [k for k, r in enumerate(pts) if L.collinear(u, L.sub(r, p))]
        for a, b in itertools.combinations(on, 2):
            seen.add((a, b))
        if len(on) >= 3:
            out.append(on)
    return out


def model(lat, prop, pts):
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f"x{i}") for i in range(len(pts))]
    n = len(pts)
    if prop == "distinct":
        cls = {}
        for i, j in itertools.combinations(range(n), 2):
            cls.setdefault(L.d2(lat, pts[i], pts[j]), []).append((i, j))
        for pairs in cls.values():
            if len(pairs) < 2:
                continue
            ys = []
            for i, j in pairs:
                y = m.NewBoolVar("")
                m.AddBoolOr([x[i].Not(), x[j].Not(), y])
                ys.append(y)
            m.AddAtMostOne(ys)
    elif prop == "isosceles":
        for i in range(n):
            cls = {}
            for j in range(n):
                if j != i:
                    cls.setdefault(L.d2(lat, pts[i], pts[j]), []).append(j)
            for js in cls.values():
                if len(js) >= 2:
                    m.AddAtMostOne([x[j] for j in js]).OnlyEnforceIf(x[i])
    elif prop == "right":
        for i in range(n):
            vs = [(j, L.sub(pts[j], pts[i])) for j in range(n) if j != i]
            for (j, u), (k, v) in itertools.combinations(vs, 2):
                if L.dot2(lat, u, v) == 0:
                    m.AddBoolOr([x[i].Not(), x[j].Not(), x[k].Not()])
    elif prop == "collinear":
        for on in lines(lat, pts):
            m.Add(sum(x[k] for k in on) <= 2)
    else:
        raise ValueError(prop)
    m.Maximize(sum(x))
    return m, x


def main():
    pid, nmin, nmax, secs, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    stop = int(sys.argv[7]) if len(sys.argv) > 7 else 10 ** 9
    misses = 0
    lat, prop = pid.split("-", 1)
    os.makedirs(outdir, exist_ok=True)
    prev = None
    for n in range(nmin, nmax + 1):
        pts = region(lat, n)
        t = time.time()
        m, x = model(lat, prop, pts)
        if prev is None and os.path.exists(os.path.join(outdir, f"{n - 1}.txt")):
            prev = {tuple(int(c) for c in l.split()) for l in open(os.path.join(outdir, f"{n - 1}.txt"))
                    if l.strip() and not l.startswith("#")}
        if prev:
            for i, p in enumerate(pts):
                m.AddHint(x[i], p in prev)
        s = cp_model.CpSolver()
        s.parameters.max_deterministic_time = secs        # work-based, so pauses of the process do not cut it
        s.parameters.num_workers = workers
        st = s.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(json.dumps({"id": pid, "n": n, "status": s.StatusName(st)}), flush=True)
            break
        chosen = [pts[i] for i in range(len(pts)) if s.Value(x[i])]
        bad = L.check(lat, prop, n, chosen)
        assert bad is None, bad
        exact = st == cp_model.OPTIMAL
        path = os.path.join(outdir, f"{n}.txt")
        if os.path.exists(path):         # never replace a larger set, or an equal one already proved optimal
            old = open(path).read()
            oldn = sum(1 for l in old.splitlines() if l.strip() and not l.startswith("#"))
            if oldn > len(chosen) or (oldn == len(chosen) and ("optimal" in old.splitlines()[0] or not exact)):
                chosen = [tuple(int(c) for c in l.split()) for l in old.splitlines() if l.strip() and not l.startswith("#")]
                exact = exact or "optimal" in old.splitlines()[0]
        with open(path, "w") as f:
            f.write(f"# {pid}, side {n}: {len(chosen)} points ({'optimal: CP-SAT proved it' if exact else 'best found'})\n")
            for p in sorted(chosen):
                f.write(" ".join(map(str, p)) + "\n")
        prev = set(chosen)
        misses = 0 if exact else misses + 1
        print(json.dumps({"id": pid, "n": n, "points": len(pts), "value": len(chosen), "exact": exact,
                          "bound": int(s.BestObjectiveBound()), "seconds": round(time.time() - t, 1)}), flush=True)
        if misses >= stop:
            break


if __name__ == "__main__":
    main()
