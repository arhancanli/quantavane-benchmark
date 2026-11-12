#!/usr/bin/env python3
"""First searches for the QV-Topo 1 tables (numpy; run as python3 tools/topopt_search.py ..., not with -I if numpy is in
the user site). Our own code, written from the published equations; no program of anyone else is run:
- SIMP cells: optimality criteria (OC) with the density filter (Andreassen et al. 2011, section 2 and 3), run to a tight
  stop, from the uniform design and from designs first converged with other filter radii, with penalty continuation
  and perturbed restarts; the method of moving asymptotes (Svanberg 1987) with the volume constraint kept exact.
- 0/1 cells, minimum feature size 2: SIMP with a density filter and a tanh projection (continuation in beta), then a
  plain, a k x k box or a dilated threshold, a morphological repair that keeps and joins the load and support pieces,
  a trim to the volume and a local search of strip and single-element moves; size 3: our size-2 designs of the same load
  case grown into 3 x 3 squares, repaired, trimmed and searched the same way.
- Periodic cells: SIMP on the cell (designs symmetric under the square's symmetries, a periodic filter, projection),
  threshold, repair and symmetric moves for the bulk and shear cells; rotating squares drawn on the grid and a local
  search for the Poisson cells.
Every design is written as a certificate and scored by checkers/topopt_check.py (standard library only); only the
checker's value counts.

  python3 tools/topopt_search.py grid                    write refs/cells/topopt-grid.jsonl (every cell)
  python3 tools/topopt_search.py run CELL_ID [SEED]      search one cell, write refs/cells/FAMILY/CELL_ID.txt
  python3 tools/topopt_search.py replay88 CELL_ID        the 88-line paper's OC loop (move 0.2, stop when the largest
                                                         change is below 0.01) on a SIMP cell: prints the compliance
                                                         of each iteration, to compare with the value the paper prints
  python3 tools/topopt_search.py base CELL_ID            write the cell's baseline certificate (SIMP: that replay,
                                                         scaled to the volume limit; periodic cells: a plain lattice)
"""
import json
import math
import os
import re
import subprocess
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import topopt_fe as F  # noqa: E402

warnings.filterwarnings("ignore", category=RuntimeWarning)   # numpy 2.0 + Accelerate: spurious matmul warnings
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(HERE))
CHECKER = os.path.join(HERE, "checkers", "topopt_check.py")
GRID = os.path.join(HERE, "refs", "cells", "topopt-grid.jsonl")


# ------------------------------------------------------------------ the cells


def grid_cells():
    cells = []

    def comp(fam, case, nx, ny, vf, form, param):
        tag = f"r{param}" if form == "simp" else f"k{param}"
        cid = f"{fam}-{case}-{nx}x{ny}-v{vf}-{tag}"
        cells.append({"id": cid, "family": fam, "params": {"case": case, "nelx": str(nx), "nely": str(ny),
                                                           "volfrac": vf, "form": form, "param": str(param)},
                      "checker_args": ["compliance", case, str(nx), str(ny), vf, form, str(param)]})
    comp("topopt-simp", "mbb", 60, 20, "0.5", "simp", "2.4")
    comp("topopt-simp", "mbb", 150, 50, "0.5", "simp", "6")
    for vf in ("0.3", "0.4"):
        comp("topopt-simp", "mbb", 60, 20, vf, "simp", "2.4")
    for vf in ("0.3", "0.4", "0.5"):
        comp("topopt-simp", "cantilever", 80, 50, vf, "simp", "3")
    for vf in ("0.3", "0.4", "0.5"):
        comp("topopt-simp", "lbracket", 50, 50, vf, "simp", "2")
    for case, nx, ny in (("mbb", 60, 20), ("cantilever", 80, 50), ("lbracket", 50, 50)):
        for k, vfs in ((2, ("0.3", "0.4", "0.5")), (3, ("0.5",))):
            for vf in vfs:
                comp("topopt-binary", case, nx, ny, vf, "binary", k)
    for target, vfs, floor in (("bulk", ("0.3", "0.4", "0.5", "0.6"), "0"), ("shear", ("0.3", "0.4", "0.5", "0.6"), "0"),
                               ("poisson", ("0.4", "0.5", "0.6"), "0.01")):
        for vf in vfs:
            cid = f"metacell-{target}-n40-v{vf}-k2" + (f"-f{floor}" if target == "poisson" else "")
            cells.append({"id": cid, "family": f"metacell-{target}",
                          "params": {"target": target, "n": "40", "volfrac": vf, "k": "2", "floor": floor},
                          "checker_args": ["cell", target, "40", vf, "2", floor]})
    return cells


def find_cell(cid):
    for c in grid_cells():
        if c["id"] == cid:
            return c
    raise SystemExit(f"unknown cell {cid}")


def check(args, path):
    r = subprocess.run([sys.executable, "-I", CHECKER] + args + [path], capture_output=True, text=True)
    m = re.findall(r"^RESULT (-?\d+)(?:/(\d+))?$", r.stdout, re.M)
    if r.returncode != 0 or not m:
        return None, r.stdout
    from fractions import Fraction
    return Fraction(int(m[-1][0]), int(m[-1][1] or 1)), r.stdout


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ------------------------------------------------------------------ SIMP with the density filter (OC)


def oc_update(x, dc, dv, filt, design, vtarget, move, tol=1e-12):
    l1, l2 = 0.0, 1e9
    xd = x[design]
    g = np.sqrt(np.maximum(-dc[design], 0.0) / dv[design])
    lo, hi = np.maximum(0.0, xd - move), np.minimum(1.0, xd + move)
    while (l2 - l1) / (l1 + l2) > tol:
        lmid = 0.5 * (l2 + l1)
        xn = np.clip(xd * g / math.sqrt(lmid), lo, hi)
        xnew = np.zeros_like(x)
        xnew[design] = xn
        if filt.apply(xnew).sum() > vtarget:
            l1 = lmid
        else:
            l2 = lmid
    return xnew


def simp_run(st, vf, rmin, penal_of, maxit, tol, move, x0=None, bisect_tol=1e-9, stop_p=3.0, verbose=False):
    filt = F.DensityFilter(rmin, st.design)
    design = st.design
    x = np.where(design, vf, 0.0) if x0 is None else x0.copy()
    vtarget = vf * st.n_design
    dv = filt.transpose(design.astype(float))
    hist = []
    for it in range(maxit):
        p = penal_of(it)
        xp = filt.apply(x)
        E = np.where(design, F.EMIN + xp ** p * (1 - F.EMIN), F.EMIN)
        c, ce = st.analyse(E)
        hist.append(c)
        dc = filt.transpose(-p * (1 - F.EMIN) * xp ** (p - 1) * ce * design)
        xnew = oc_update(x, dc, dv, filt, design, vtarget, move, bisect_tol)
        change = float(np.abs(xnew - x).max())
        x = xnew
        if verbose and (it < 5 or it % 50 == 0):
            log(f"it {it} p {p} c {c:.6f} change {change:.5f}")
        if p >= stop_p and change < tol:
            break
    return x, hist


def simp_compliance(st, x, rmin, vf):
    filt = F.DensityFilter(rmin, st.design)
    xp = filt.apply(x)
    c, _ = st.analyse(np.where(st.design, F.EMIN + xp ** 3 * (1 - F.EMIN), F.EMIN))
    return c, xp


def finalize_simp(st, x, rmin, vf):
    """Scale to the exact volume and round down to 6 decimals (the filter is linear and positive)."""
    filt = F.DensityFilter(rmin, st.design)
    vol = filt.apply(x).sum()
    lim = vf * st.n_design
    if vol > lim:
        x = x * (lim / vol) * (1 - 1e-9)
    return np.floor(x * 1e6) / 1e6 * st.design


def mma_run(st, vf, rmin, maxit, tol, x0=None, move=0.3, asyinit=0.5, asyincr=1.2, asydecr=0.7):
    """The method of moving asymptotes (K. Svanberg, Int. J. Numer. Meth. Eng. 24 (1987) 359-373; our code) for the
    SIMP problem with the density filter: the compliance by its MMA approximation, the volume constraint (linear in x
    after the filter) kept exact; the separable subproblem by bisection on the volume multiplier, each element's
    stationary point by bisection on its convex one-dimensional problem."""
    filt = F.DensityFilter(rmin, st.design)
    design = st.design
    x = np.where(design, vf, 0.0) if x0 is None else x0.copy()
    V = vf * st.n_design
    dv = filt.transpose(design.astype(float))
    xo1, xo2, low, upp = x.copy(), x.copy(), None, None
    f0 = None
    hist = []
    for it in range(maxit):
        xp = filt.apply(x)
        c, ce = st.analyse(np.where(design, F.EMIN + xp ** 3 * (1 - F.EMIN), F.EMIN))
        hist.append(c)
        g = filt.transpose(-3 * (1 - F.EMIN) * xp ** 2 * ce * design)
        if f0 is None:
            f0 = c
        g = g / f0
        if it < 2:
            low, upp = x - asyinit, x + asyinit
        else:
            zz = (x - xo1) * (xo1 - xo2)
            gam = np.where(zz > 0, asyincr, np.where(zz < 0, asydecr, 1.0))
            low, upp = x - gam * (xo1 - low), x + gam * (upp - xo1)
            low = np.clip(low, x - 10.0, x - 0.01)
            upp = np.clip(upp, x + 0.01, x + 10.0)
        alpha = np.maximum.reduce([np.zeros_like(x), low + 0.1 * (x - low), x - move])
        beta = np.minimum.reduce([np.ones_like(x), upp - 0.1 * (upp - x), x + move])
        reg = 1e-5 / (upp - low)
        P = (upp - x) ** 2 * (np.maximum(g, 0) + 0.001 * np.abs(g) + reg)
        Q = (x - low) ** 2 * (np.maximum(-g, 0) + 0.001 * np.abs(g) + reg)

        def x_of(lam):
            a, b = alpha.copy(), beta.copy()
            for _ in range(50):
                mid = 0.5 * (a + b)
                h = P / (upp - mid) ** 2 - Q / (mid - low) ** 2 + lam * dv
                a = np.where(h < 0, mid, a)
                b = np.where(h < 0, b, mid)
            return np.where(design, 0.5 * (a + b), 0.0)
        l1, l2 = 0.0, 1.0
        while (x_of(l2) * dv).sum() > V:
            l2 *= 2.0
        for _ in range(60):
            lm = 0.5 * (l1 + l2)
            if (x_of(lm) * dv).sum() > V:
                l1 = lm
            else:
                l2 = lm
        xn = x_of(l2)
        xo2, xo1 = xo1, x
        change = float(np.abs(xn - x).max())
        x = xn
        if change < tol:
            break
    return x, hist


def search_simp(cell, seed):
    p = cell["params"]
    st = F.Structure(p["case"], int(p["nelx"]), int(p["nely"]))
    vf, rmin = float(p["volfrac"]), float(p["param"])
    runs = []
    full = cell["id"] in ("topopt-simp-mbb-60x20-v0.5-r2.4", "topopt-simp-mbb-150x50-v0.5-r6")   # published values
    it_max = 3000 if full else 1500
    # (a) the 88-line paper's loop (move 0.2, from the uniform design) run on to a tight stop
    x, h = simp_run(st, vf, rmin, lambda it: 3.0, it_max, 1e-5, 0.2)
    runs.append(("OC, uniform start, move 0.2, stopped when the largest change < 1e-5", x))
    if full:
        # (b) continuation of the penalty 1 -> 3 (steps of 0.25 every 30 iterations), then to a tight stop
        x, h = simp_run(st, vf, rmin, lambda it: min(3.0, 1.0 + 0.25 * (it // 30)), it_max, 1e-5, 0.2)
        runs.append(("OC, penalty continuation 1 -> 3 in steps of 0.25, move 0.2, stopped at a change < 1e-5", x))
        # (c) a smaller move limit from (a)
        x, h = simp_run(st, vf, rmin, lambda it: 3.0, it_max, 1e-6, 0.05, x0=runs[0][1])
        runs.append(("OC from (a) with move 0.05, stopped at a change < 1e-6", x))
    # (d) other topologies: start from the converged design of another filter radius (a search device only; the
    # design is then converged and scored with the cell's radius)
    for r2 in ((0.6 * rmin, 1.5 * rmin, 2.0 * rmin, 2.5 * rmin) if full else (0.6 * rmin, 1.5 * rmin)):
        x2, _ = simp_run(st, vf, max(1.1, r2), lambda it: 3.0, 400, 1e-3, 0.2)
        x, h = simp_run(st, vf, rmin, lambda it: 3.0, it_max, 1e-5, 0.2, x0=x2)
        runs.append((f"OC from the design converged with a filter radius {max(1.1, r2):.2f}, then with the cell's "
                     f"radius to a change < 1e-5", x))
        if full:
            xm, _ = mma_run(st, vf, rmin, 600, 1e-7, x0=x, move=0.1)
            runs.append((f"OC from the design converged with a filter radius {max(1.1, r2):.2f}, then with the cell's "
                         f"radius to a change < 1e-5, then MMA (move 0.1) to a change < 1e-7", xm))
    # (f) the method of moving asymptotes from the uniform design
    x, h = mma_run(st, vf, rmin, 600, 1e-6)
    runs.append(("MMA (our code) from the uniform design, to a change < 1e-6", x))
    if full:
        x, h = simp_run(st, vf, rmin, lambda it: 3.0, it_max, 1e-6, 0.05, x0=x)
        runs.append(("MMA from the uniform design, then OC with move 0.05 to a change < 1e-6", x))
        x, h = mma_run(st, vf, rmin, 600, 1e-6, x0=runs[2][1], move=0.1)
        runs.append(("MMA (move 0.1) from (c), to a change < 1e-6", x))
        # (e) perturbed restarts of (c)
        rng = np.random.default_rng(seed)
        for t in range(2):
            x0 = np.clip(runs[2][1] + 0.15 * rng.standard_normal(runs[2][1].shape), 0, 1) * st.design
            x, h = simp_run(st, vf, rmin, lambda it: 3.0, it_max, 1e-5, 0.2, x0=x0)
            runs.append((f"OC from (c) perturbed by noise 0.15 (seed {seed}.{t}), to a change < 1e-5", x))
    best = None
    for how, x in runs:
        xf = finalize_simp(st, x, rmin, vf)
        c, _ = simp_compliance(st, xf, rmin, vf)
        log(f"{cell['id']}: {how}: {c:.6f}")
        if best is None or c < best[0]:
            best = (c, how, xf)
    return best


def replay88(cell, write=False):
    """The 88-line paper's loop (its section 3 and appendix, our code): uniform start, OC with move 0.2 and a
    bisection to a relative 1e-3, stop when the largest change is below 0.01. The compliance printed at an iteration
    is that of the design at its start, so the design kept is the one before the last update."""
    p = cell["params"]
    st = F.Structure(p["case"], int(p["nelx"]), int(p["nely"]))
    vf, rmin = float(p["volfrac"]), float(p["param"])
    filt = F.DensityFilter(rmin, st.design)
    design = st.design
    x = np.where(design, vf, 0.0)
    dv = filt.transpose(design.astype(float))
    hist = []
    for it in range(2000):
        xp = filt.apply(x)
        c, ce = st.analyse(np.where(design, F.EMIN + xp ** 3 * (1 - F.EMIN), F.EMIN))
        hist.append(c)
        dc = filt.transpose(-3 * (1 - F.EMIN) * xp ** 2 * ce * design)
        xnew = oc_update(x, dc, dv, filt, design, vf * st.n_design, 0.2, 1e-3)
        change = float(np.abs(xnew - x).max())
        if change < 0.01:
            break
        x = xnew
    for i, c in enumerate(hist):
        if i < 3 or i >= len(hist) - 3:
            print(f"It.: {i + 1:4d} Obj.: {c:11.4f}")
    print(f"{len(hist)} iterations; last printed compliance {hist[-1]:.4f}")
    if write:
        xf = finalize_simp(st, x, rmin, vf)
        c, _ = simp_compliance(st, xf, rmin, vf)
        how = (f"baseline: our replay of the 88-line paper's optimality-criteria loop (uniform start, move 0.2, stop "
               f"when the largest change is below 0.01; {len(hist)} iterations, last printed compliance "
               f"{hist[-1]:.4f}), the design of the last printed iteration scaled to the volume limit")
        rel = f"collections/open-tables/refs/cells/{cell['family']}/{cell['id']}.base.txt"
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        F.write_simp(path, xf, [f"{cell['id']}: {how}", "QV-Topo 1 (a numerical model); checker args: " +
                                " ".join(cell["checker_args"])])
        got, out = check(cell["checker_args"], path)
        log(f"{cell['id']}: baseline {c:.6f}; checker {got} ({None if got is None else float(got)})")
    return hist


def lattice_base(cell):
    """Plain lattices for the periodic cells: bars along the cell edges (bulk) or along the diagonals (shear), as
    thick as the volume allows."""
    p = cell["params"]
    n, vf, k = int(p["n"]), float(p["volfrac"]), int(p["k"])
    from fractions import Fraction
    m = int(Fraction(p["volfrac"]) * n * n)
    rules = Rules(np.ones((n, n), bool), k, True, symmetric=True)
    best = None
    for t in range(1, n // 2):
        r, c = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        if p["target"] == "bulk":
            S = (np.minimum(r, n - 1 - r) < t) | (np.minimum(c, n - 1 - c) < t)
            name = f"square grid of bars {2 * t} elements wide along the cell edges"
        elif p["target"] == "shear":
            S = (np.abs(r - c) < t) | (np.abs(r + c - (n - 1)) < t)
            name = f"diagonal grid of bars (|r - c| < {t} and |r + c - {n - 1}| < {t})"
        else:
            return None
        if S.sum() > m:
            break
        if rules.ok(S):
            best = (S, name)
    if best is None:
        return None
    S, name = best
    rel = f"collections/open-tables/refs/cells/{cell['family']}/{cell['id']}.base.txt"
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    F.write_binary(path, S, [f"{cell['id']}: baseline: a plain {name}", "QV-Topo 1 (a numerical model); checker "
                                                                        "args: " + " ".join(cell["checker_args"])])
    got, out = check(cell["checker_args"], path)
    log(f"{cell['id']}: baseline {name}: checker {got} ({None if got is None else float(got)})")
    return got


# ------------------------------------------------------------------ 0/1 designs: threshold, repair, local search


class Rules:
    def __init__(self, design, k, periodic, load_elems=(), supports=(), symmetric=False):
        self.design, self.k, self.periodic = design, k, periodic
        self.load_elems, self.supports, self.symmetric = load_elems, supports, symmetric

    def ok(self, S):
        good, _, _ = F.feature_ok(S, self.k, self.design, self.periodic)
        if not good:
            return False
        lab, nc = F.components(S, self.periodic)
        if nc != 1:
            return False
        if not self.periodic:
            if not any(S[iy, ix] for ix, iy in self.load_elems):
                return False
            for sup in self.supports:
                if not any(S[iy, ix] for ix, iy in sup):
                    return False
        elif not wraps(S):
            return False
        return True


def wraps(S):
    n = S.shape[0]
    cells = {(c, r) for r, c in zip(*np.nonzero(S))}
    if not cells:
        return False
    start = min(cells)
    lift = {start: start}
    stack, periods = [start], set()
    while stack:
        u = stack.pop()
        X, Y = lift[u]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = ((u[0] + dx) % n, (u[1] + dy) % n)
            if v not in cells:
                continue
            P = (X + dx, Y + dy)
            if v not in lift:
                lift[v] = P
                stack.append(v)
            else:
                d = (P[0] - lift[v][0], P[1] - lift[v][1])
                if d != (0, 0):
                    periods.add((d[0] // n, d[1] // n))
    ps = sorted(periods)
    return any(a[0] * b[1] - a[1] * b[0] for i, a in enumerate(ps) for b in ps[i + 1:])


def symmetrize(S):
    return S | S[:, ::-1] | S[::-1, :] | S.T | S[::-1, ::-1] | S.T[:, ::-1] | S.T[::-1, :] | S.T[::-1, ::-1]


def orbit_mask(n, cells):
    M = np.zeros((n, n), bool)
    for r, c in cells:
        M[r, c] = True
    return symmetrize(M)


def repair(S, rules, rounds=20, req=(), xp=None):
    """Opening, closing and filling of point contacts until stable; then the piece that holds the required elements
    (load and supports), joined to the other required pieces along the cheapest path through dense elements, grown
    into k x k squares; without required elements, the largest piece."""
    k, design, per = rules.k, rules.design, rules.periodic
    for attempt in range(4):
        for _ in range(rounds):
            prev = S.copy()
            S = F.opening(S, k, design, per)
            S = F.closing(S, k, design, per)
            _, _, pc = F.feature_ok(S, k, design, per)
            if pc.any():
                ys, xs = np.nonzero(pc)
                for y, x in zip(ys, xs):
                    for dy in (0, 1):
                        for dx in (0, 1):
                            yy, xx = y + dy, x + dx
                            if per:
                                yy %= S.shape[0]
                                xx %= S.shape[1]
                            if design[yy, xx]:
                                S[yy, xx] = True
            if rules.symmetric:
                S = symmetrize(S)
            if np.array_equal(S, prev):
                break
        lab, nc = F.components(S, per)
        if not req:
            if nc > 1:
                sizes = np.bincount(lab[lab >= 0])
                S = lab == int(np.argmax(sizes))
            return S
        for y, x in req:                                   # required elements stay solid
            sy, sx = inside_square(y, x, k, S.shape)
            S[sy, sx] |= design[sy, sx]
        lab, nc = F.components(S, per)
        comps = sorted({int(lab[y, x]) for y, x in req if lab[y, x] >= 0})
        if len(comps) <= 1:
            return lab == comps[0] if comps else S
        main = lab == comps[0]
        for cid in comps[1:]:
            path = cheapest_path(main, lab == cid, xp if xp is not None else S.astype(float), design)
            for y, x in path:
                sy, sx = inside_square(y, x, k, S.shape)
                S[sy, sx] |= design[sy, sx]
            main = main | (lab == cid)
            for y, x in path:
                main[y, x] = True
    lab, nc = F.components(S, per)
    comps = sorted({int(lab[y, x]) for y, x in req if lab[y, x] >= 0})
    return lab == comps[0] if comps else S


def cheapest_path(A, B, xp, design):
    """Cells of a cheapest 4-connected path from set A to set B, each step costing 1.05 - density (0 inside A)."""
    import heapq
    ny, nx = A.shape
    dist = np.full((ny, nx), np.inf)
    prev = {}
    heap = []
    for y, x in zip(*np.nonzero(A)):
        dist[y, x] = 0.0
        heap.append((0.0, int(y), int(x)))
    heapq.heapify(heap)
    while heap:
        d, y, x = heapq.heappop(heap)
        if d > dist[y, x]:
            continue
        if B[y, x]:
            out = []
            while (y, x) in prev:
                out.append((y, x))
                y, x = prev[(y, x)]
            return out
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < ny and 0 <= xx < nx and design[yy, xx]:
                nd = d + (0.0 if A[yy, xx] else 1.05 - min(1.0, float(xp[yy, xx])))
                if nd < dist[yy, xx]:
                    dist[yy, xx] = nd
                    prev[(yy, xx)] = (y, x)
                    heapq.heappush(heap, (nd, yy, xx))
    return []


def strips(shape, k, periodic):
    """All single elements and all k-long horizontal and vertical strips (lists of (iy, ix))."""
    ny, nx = shape
    out = [[(iy, ix)] for iy in range(ny) for ix in range(nx)]
    for iy in range(ny):
        for ix in range(nx):
            for dx, dy in ((1, 0), (0, 1)):
                cells = []
                for t in range(k):
                    y, x = iy + dy * t, ix + dx * t
                    if periodic:
                        y, x = y % ny, x % nx
                    elif not (y < ny and x < nx):
                        cells = None
                        break
                    cells.append((y, x))
                if cells:
                    out.append(cells)
    return out


class Objective:
    """f(S) -> (value to minimise, sensitivity of adding / removing per element, raw report)."""

    def __init__(self, kind, obj):
        self.kind, self.obj = kind, obj
        self.cache = {}

    def __call__(self, S):
        key = S.tobytes()
        if key in self.cache:
            return self.cache[key]
        if self.kind == "compliance":
            st = self.obj
            c, ce = st.analyse(np.where(S, 1.0, F.EMIN))
            out = (c, ce, c)                       # ce: d(-c)/dE for adding (void) or removing (solid)
        else:
            cell, target, floor = self.obj
            C, e = cell.homogenise(np.where(S, 1.0, F.EMIN))
            n2 = S.shape[0] ** 2
            if target == "bulk":
                v = (C[0, 0] + C[1, 1] + 2 * C[0, 1]) / 4
                g = (e[0, 0] + e[1, 1] + 2 * e[0, 1]) / 4 / n2
                out = (-v, g, v)
            elif target == "shear":
                out = (-C[2, 2], e[2, 2] / n2, C[2, 2])
            else:
                Sm = np.linalg.inv(C)
                nus = (-Sm[0, 1] / Sm[0, 0], -Sm[0, 1] / Sm[1, 1])
                Es = (1 / Sm[0, 0], 1 / Sm[1, 1])
                j = 0 if nus[0] >= nus[1] else 1
                dS = -np.einsum("ik,kle,lj->ije", Sm, e.reshape(3, 3, -1) / n2, Sm)      # dS / dmodulus_e
                dnu = -(dS[0, 1] * Sm[j, j] - Sm[0, 1] * dS[j, j]) / Sm[j, j] ** 2
                Emin_ = min(Es)
                jj = 0 if Es[0] <= Es[1] else 1
                dE = -dS[jj, jj] / Sm[jj, jj] ** 2
                pen = 0.0 if Emin_ >= floor else 50.0 * (floor - Emin_) / floor + 1.0
                gpen = 0.0 if Emin_ >= floor else 50.0 * dE / floor
                out = (nus[j] + pen, (-dnu + gpen).reshape(S.shape), (nus[j], Emin_))
        if len(self.cache) > 20000:
            self.cache.clear()
        self.cache[key] = out
        return out


def local_search(S, rules, objective, budget, rng, m, label, tries=40, window=30):
    """Swap moves (remove one k-long strip, add another) and additions while under the volume limit, with the
    symmetric images of each strip for cells; candidates ranked by the first-order gain, the first valid move that
    improves the exact objective is taken. The window of ranked candidates widens after a round without gain."""
    k, per = rules.k, rules.periodic
    shape = S.shape
    lib = strips(shape, k, per)
    f, g, _ = objective(S)
    evals, stall, win = 0, 0, window
    while evals < budget and stall < 4:
        improved = False
        f, g, _ = objective(S)
        rem, add = [], []
        for cells in lib:
            vals = [S[y, x] for y, x in cells]
            if all(vals):
                rem.append((sum(g[y, x] for y, x in cells), cells))
            elif not any(vals) and all(rules.design[y, x] for y, x in cells):
                if any(S[(y + dy) % shape[0] if per else min(max(y + dy, 0), shape[0] - 1),
                         (x + dx) % shape[1] if per else min(max(x + dx, 0), shape[1] - 1)]
                       for y, x in cells for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    add.append((sum(g[y, x] for y, x in cells), cells))
        rem.sort(key=lambda t: t[0])
        add.sort(key=lambda t: -t[0])
        count = int(S.sum())
        moves = []
        if count < m:
            moves += [(-a[0] * 2.0, [], a[1]) for a in add[:win]]
        moves += [(r[0] - a[0], r[1], a[1]) for r in rem[:win] for a in add[:win]]
        moves.sort(key=lambda t: t[0])
        head, tail = moves[:4 * tries], moves[4 * tries:]
        rng.shuffle(tail)
        tried = 0
        for _, rc, ac in head + tail:
            if tried >= tries or evals >= budget:
                break
            if rules.symmetric:
                T = sym_apply(S, rc, ac)
            else:
                T = S.copy()
                for y, x in rc:
                    T[y, x] = False
                for y, x in ac:
                    T[y, x] = True
            if T.sum() > m or np.array_equal(T, S) or not rules.ok(T):
                continue
            tried += 1
            evals += 1
            fT, _, _ = objective(T)
            if fT < f - 1e-12:
                S, f = T, fT
                improved = True
                break
        if improved:
            stall, win = 0, window
        else:
            stall += 1
            win = min(4 * window, 2 * win)
    log(f"{label}: local search {evals} evaluations, objective {f:.9f}")
    return S


def sym_apply(S, rem, add):
    n = S.shape[0]
    T = S.copy()
    if rem:
        T &= ~orbit_mask(n, rem)
    if add:
        T |= orbit_mask(n, add)
    return T


def fit_volume(S, rules, objective, m, rng, exact=8):
    """Remove strips until at most m elements remain: among the valid strips of least first-order value, the one
    whose removal raises the exact objective least (several strips per round while far from m)."""
    k, per = rules.k, rules.periodic
    lib = strips(S.shape, k, per)
    guard = 0
    while S.sum() > m and guard < 3000:
        guard += 1
        f, g, _ = objective(S)
        cands = [(sum(g[y, x] for y, x in cells), cells) for cells in lib if all(S[y, x] for y, x in cells)]
        cands.sort(key=lambda t: t[0])
        valid = []
        for _, cells in cands[:300]:
            T = sym_apply(S, cells, []) if rules.symmetric else S.copy()
            if not rules.symmetric:
                for y, x in cells:
                    T[y, x] = False
            if rules.ok(T):
                valid.append((cells, T))
                if len(valid) >= exact:
                    break
        if not valid:
            return None
        scored = sorted(((objective(T)[0], i) for i, (cells, T) in enumerate(valid)))
        S = valid[scored[0][1]][1]
    return S if S.sum() <= m else None


def threshold(xp, design, m, symmetric=False):
    vals = np.where(design, xp, -1.0).ravel()
    order = np.argsort(-vals, kind="stable")
    S = np.zeros(vals.size, bool)
    S[order[:m]] = True
    S = S.reshape(xp.shape)
    return symmetrize(S) if symmetric else S


def box_threshold(xp, design, k, count, periodic, symmetric=False):
    """The union of the k x k squares whose mean density is at least t, with t chosen (by bisection) so that about
    `count` elements are solid: every solid element then lies in a solid k x k square by construction."""
    ny, nx = xp.shape
    X = np.where(design, xp, 0.0)
    if periodic:
        box = sum(np.roll(np.roll(X, -qy, 0), -qx, 1) for qy in range(k) for qx in range(k)) / (k * k)
        inside = np.ones_like(box, bool)
    else:
        box = np.zeros((ny - k + 1, nx - k + 1))
        dbox = np.zeros_like(box)
        for qy in range(k):
            for qx in range(k):
                box += X[qy:qy + ny - k + 1, qx:qx + nx - k + 1]
                dbox += design[qy:qy + ny - k + 1, qx:qx + nx - k + 1]
        box /= k * k
        inside = dbox == k * k

    def make(t):
        E = (box >= t) & inside
        S = np.zeros((ny, nx), bool)
        for qy in range(k):
            for qx in range(k):
                if periodic:
                    S |= np.roll(np.roll(E, qy, 0), qx, 1)
                else:
                    S[qy:qy + ny - k + 1, qx:qx + nx - k + 1] |= E
        S &= design
        return symmetrize(S) if symmetric else S
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if make(mid).sum() > count:
            lo = mid
        else:
            hi = mid
    return make(hi)


def inside_square(y, x, k, shape):
    """The k x k square inside the grid that contains (y, x), as slices (centred where possible)."""
    ny, nx = shape
    ty = min(max(y - (k - 1) // 2, 0), ny - k)
    tx = min(max(x - (k - 1) // 2, 0), nx - k)
    return slice(ty, ty + k), slice(tx, tx + k)


def dilate_threshold(xp, design, k, count, periodic, symmetric=False):
    """The top elements, each grown into a k x k square (inside the grid where it is not periodic), so thin members
    become k wide and every solid element lies in a solid k x k square; the number of top elements is chosen by
    bisection so that at most `count` elements are solid."""
    ny, nx = xp.shape
    vals = np.where(design, xp, -1.0).ravel()
    order = np.argsort(-vals, kind="stable")

    def make(c):
        S = np.zeros((ny, nx), bool)
        for e in order[:c]:
            y, x = divmod(int(e), nx)
            if periodic:
                for qy in range(k):
                    for qx in range(k):
                        S[(y + qy) % ny, (x + qx) % nx] = True
            else:
                sy, sx = inside_square(y, x, k, (ny, nx))
                S[sy, sx] = True
        S &= design
        return symmetrize(S) if symmetric else S
    lo, hi = 1, int(design.sum())
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if make(mid).sum() <= count:
            lo = mid
        else:
            hi = mid
    return make(lo)


def valid_threshold(xp, design, rules, objective, m, rng, symmetric=False, steps=(0, 8, 16, 32, 64, 96, 128, 192,
                                                                                    256)):
    """Every threshold count m + extra, by the plain threshold and by the k x k box threshold, whose repaired design
    satisfies every rule, trimmed to at most m elements; the best of them by the exact objective."""
    best = (None, None, None)
    req = []                                    # the load element and the densest element of each support
    if not rules.periodic:
        groups = [rules.load_elems] + list(rules.supports)
        for g in groups:
            ix, iy = max(g, key=lambda e: xp[e[1], e[0]])
            req.append((iy, ix))
        xp = xp.copy()
        for y, x in req:
            xp[y, x] = 2.0
    for extra in steps:
        for kind in ("plain", "box", "dilated"):
            if kind == "plain":
                S = threshold(xp, design, m + extra, symmetric)
            elif kind == "box":
                S = box_threshold(xp, design, rules.k, m + extra, rules.periodic, symmetric)
            else:
                S = dilate_threshold(xp, design, rules.k, m + extra, rules.periodic, symmetric)
            S = repair(S, rules, req=req, xp=xp)
            if not rules.ok(S):
                continue
            if S.sum() > m:
                S = fit_volume(S, rules, objective, m, rng)
                if S is None or not rules.ok(S):
                    continue
            f = objective(S)[0]
            if best[0] is None or f < best[0]:
                best = (f, S, f"{extra} ({kind})")
    return best[1], best[2]


def heaviside(xt, beta, eta=0.5):
    a, b = math.tanh(beta * eta), math.tanh(beta * (1 - eta))
    return (a + np.tanh(beta * (xt - eta))) / (a + b), beta * (1 - np.tanh(beta * (xt - eta)) ** 2) / (a + b)


def projected_simp(st, vf, R, iters_per_beta=60, betas=(1, 2, 4, 8, 16, 32), move=0.1):
    """SIMP with a density filter of radius R and a tanh projection (continuation in beta); returns xPhys."""
    filt = F.DensityFilter(R, st.design)
    design = st.design
    x = np.where(design, vf, 0.0)
    vtarget = vf * st.n_design
    for beta in betas:
        for it in range(iters_per_beta):
            xt = filt.apply(x)
            xp, dxp = heaviside(xt, beta)
            xp = xp * design
            E = np.where(design, F.EMIN + xp ** 3 * (1 - F.EMIN), F.EMIN)
            c, ce = st.analyse(E)
            dc = filt.transpose(-3 * (1 - F.EMIN) * xp ** 2 * ce * dxp * design)
            dv = filt.transpose(dxp * design)
            l1, l2 = 0.0, 1e9
            xd = x[design]
            gg = np.sqrt(np.maximum(-dc[design], 0) / np.maximum(dv[design], 1e-12))
            lo, hi = np.maximum(0, xd - move), np.minimum(1, xd + move)
            while (l2 - l1) / (l1 + l2) > 1e-6:
                lmid = 0.5 * (l1 + l2)
                xn = np.zeros_like(x)
                xn[design] = np.clip(xd * gg / math.sqrt(lmid), lo, hi)
                if (heaviside(filt.apply(xn), beta)[0] * design).sum() > vtarget:
                    l1 = lmid
                else:
                    l2 = lmid
            change = np.abs(xn - x).max()
            x = xn
            if change < 1e-3:
                break
    xt = filt.apply(x)
    return heaviside(xt, betas[-1])[0] * design


def grow_k2(cell, st, k, m, rules, obj, rng):
    """For k > 2: each of our designs for minimum feature size 2 of the same load case, every element grown into the
    k x k square around it (inside the grid), repaired, trimmed to the volume and improved by the local search."""
    p = cell["params"]
    req = [(g[0][1], g[0][0]) for g in [rules.load_elems] + list(rules.supports)]
    best = None
    for v2 in ("0.3", "0.4", "0.5"):
        f2 = os.path.join(HERE, "refs", "cells", "topopt-binary",
                          f"topopt-binary-{p['case']}-{p['nelx']}x{p['nely']}-v{v2}-k2.txt")
        if not os.path.exists(f2):
            continue
        rows = [l.strip() for l in open(f2) if l[:1] in "01"]
        S2 = np.array([[ch == "1" for ch in r] for r in rows])
        G = np.zeros_like(S2)
        for y, x in zip(*np.nonzero(S2)):
            sy, sx = inside_square(int(y), int(x), k, S2.shape)
            G[sy, sx] = True
        G &= st.design
        S = repair(G, rules, req=req, xp=S2.astype(float))
        if not rules.ok(S):
            continue
        if S.sum() > m:
            S = fit_volume(S, rules, obj, m, rng)
            if S is None or not rules.ok(S):
                log(f"{cell['id']}: our k = 2 design at volume {v2}, grown: trimming failed")
                continue
        c0 = obj(S)[0]
        S = local_search(S, rules, obj, 800, rng, m, f"{cell['id']} (grown from volume {v2})")
        c = obj(S)[0]
        log(f"{cell['id']}: our design for minimum feature size 2 at volume {v2} grown: {c0:.4f} -> {c:.4f}")
        if best is None or c < best[0]:
            best = (c, f"our design for minimum feature size 2 at volume {v2} with every element grown into the {k} x "
                       f"{k} square around it, repaired, trimmed to the volume by strip removals, local search of "
                       f"strip and single-element moves", S)
    return best


def search_binary(cell, seed):
    p = cell["params"]
    st = F.Structure(p["case"], int(p["nelx"]), int(p["nely"]))
    vf, k = float(p["volfrac"]), int(p["param"])
    from fractions import Fraction
    m = int(Fraction(p["volfrac"]) * st.n_design)
    rules = Rules(st.design, k, False, st.load_elems, st.supports)
    obj = Objective("compliance", st)
    rng = np.random.default_rng(seed)
    if k > 2:
        return grow_k2(cell, st, k, m, rules, obj, rng)
    best = None
    starts = []
    for R in (1.5 * k, 2.0 * k):
        xp = projected_simp(st, vf, R)
        starts.append((f"SIMP with a density filter of radius {R} and a projection (beta to 32)", xp))
    for frac in (0.6, 0.75):                       # thinner members, then dilated by the k x k square to the volume
        xp = projected_simp(st, vf * frac, float(k))
        starts.append((f"SIMP at volume {vf * frac:.3f} with a density filter of radius {k} and a projection (beta to "
                       f"32), dilated", xp))
    xs, _ = simp_run(st, vf, max(2.0, 1.2 * k), lambda it: 3.0, 400, 1e-3, 0.2)
    starts.append((f"SIMP with a density filter of radius {max(2.0, 1.2 * k)}", F.DensityFilter(max(2.0, 1.2 * k),
                                                                                                  st.design).apply(xs)))
    for how, xp in starts:
        S, extra = valid_threshold(xp, st.design, rules, obj, m, rng)
        if S is None:
            log(f"{cell['id']}: {how}: no valid threshold")
            continue
        c0 = obj(S)[0]
        S = local_search(S, rules, obj, 1500, rng, m, f"{cell['id']} ({how}, +{extra})")
        c = obj(S)[0]
        log(f"{cell['id']}: {how}, threshold +{extra}: {c0:.4f} -> {c:.4f}")
        if best is None or c < best[0]:
            best = (c, f"{how}; threshold, morphological repair, local search of {k}-element strip moves", S)
    return best


# ------------------------------------------------------------------ periodic cells


def cell_simp(cell_fe, target, vf, R, floor, seed, iters=360, betas=(1, 2, 4, 8, 16, 32)):
    """SIMP on the periodic cell with D4-symmetric designs (the design and the sensitivities averaged over the
    symmetry group), a periodic density filter and projection; a generic update (OC for stiffness targets, a
    sign-aware OC for the Poisson target)."""
    n = cell_fe.n
    rng = np.random.default_rng(seed)
    filt = F.DensityFilter(R, np.ones((n, n), bool), periodic=True)
    yy, xx = np.meshgrid(np.arange(n) + 0.5 - n / 2, np.arange(n) + 0.5 - n / 2, indexing="ij")
    rr = np.sqrt(xx ** 2 + yy ** 2)
    if target == "poisson":
        x = np.clip(vf + 0.25 * rng.standard_normal((n, n)), 0, 1)
    else:
        x = np.clip(np.where(rr < n * (0.25 + 0.1 * rng.random()), vf - 0.2, vf + 0.1) +
                    0.05 * rng.standard_normal((n, n)), 0, 1)
    x = symavg(x)
    move = 0.1
    vtarget = vf * n * n
    for beta in betas:
        for it in range(iters // len(betas)):
            xt = filt.apply(x)
            xp, dxp = heaviside(xt, beta)
            E = F.EMIN + xp ** 3 * (1 - F.EMIN)
            C, e = cell_fe.homogenise(E)
            dE = 3 * (1 - F.EMIN) * xp ** 2 * dxp
            n2 = n * n
            if target == "bulk":
                dobj = -((e[0, 0] + e[1, 1] + 2 * e[0, 1]) / 4 / n2) * dE
            elif target == "shear":
                dobj = -(e[2, 2] / n2) * dE
            else:
                c11 = (C[0, 0] + C[1, 1]) / 2
                dc11 = (e[0, 0] + e[1, 1]) / 2 / n2
                dnu = (e[0, 1] / n2 * c11 - C[0, 1] * dc11) / c11 ** 2
                w = 0.0 if c11 > 1.5 * floor else 20.0 / floor
                dobj = (dnu - w * dc11) * dE
            dobj = symavg(filt.transpose(dobj))
            dv = symavg(filt.transpose(dxp))
            # sign-aware OC: elements whose objective falls with more material grow, the others shrink
            l1, l2 = 1e-12, 1e9
            lo, hi = np.maximum(0, x - move), np.minimum(1, x + move)
            for _ in range(80):
                lmid = math.sqrt(l1 * l2)
                B = np.maximum(-dobj, 1e-30) / (lmid * dv)
                xn = np.clip(x * np.sqrt(B), lo, hi)
                if heaviside(filt.apply(xn), beta)[0].sum() > vtarget:
                    l1 = lmid
                else:
                    l2 = lmid
            x = symavg(xn)
    return heaviside(filt.apply(x), betas[-1])[0]


def symavg(a):
    return (a + a[:, ::-1] + a[::-1, :] + a.T + a[::-1, ::-1] + a.T[:, ::-1] + a.T[::-1, :] + a.T[::-1, ::-1]) / 8


def rotating_squares(n, theta_deg, shrink, hinge):
    """Squares rotated alternately by +-theta whose corners meet (Grima and Evans' rotating squares), shrunk by
    `shrink` and joined at the corners by discs of radius `hinge`: an auxetic seed for the Poisson cells."""
    yy, xx = np.meshgrid(np.arange(n) + 0.5, np.arange(n) + 0.5, indexing="ij")
    th = math.radians(theta_deg)
    L = n / 2
    side = L / (math.cos(th) + math.sin(th))
    S = np.zeros((n, n), bool)
    for i in range(-1, 3):
        for j in range(-1, 3):
            cx, cy = L / 2 + i * L, L / 2 + j * L
            a = th if (i + j) % 2 == 0 else -th
            dx, dy = xx - cx, yy - cy
            u, v = dx * math.cos(a) + dy * math.sin(a), -dx * math.sin(a) + dy * math.cos(a)
            S |= (np.abs(u) <= (side - shrink) / 2) & (np.abs(v) <= (side - shrink) / 2)
            for q in range(4):
                ang = a + math.pi / 4 + q * math.pi / 2
                px, py = cx + side / math.sqrt(2) * math.cos(ang), cy + side / math.sqrt(2) * math.sin(ang)
                S |= (xx - px) ** 2 + (yy - py) ** 2 <= hinge ** 2
    return S


def poisson_seeds(n, k, m, obj, rules, count=4):
    found = []
    for th in range(4, 40, 2):
        for shrink in (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0):
            for hinge in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
                S = repair(rotating_squares(n, th, shrink, hinge), rules)
                if S.sum() > m or not rules.ok(S):
                    continue
                f, _, raw = obj(S)
                found.append((f, f"rotating squares (angle {th} degrees, shrunk by {shrink}, hinges of radius "
                                 f"{hinge})", S))
    found.sort(key=lambda t: t[0])
    return found[:count]


def search_cell(cell, seed):
    p = cell["params"]
    target, n, vf, k, floor = p["target"], int(p["n"]), float(p["volfrac"]), int(p["k"]), float(p["floor"])
    from fractions import Fraction
    m = int(Fraction(p["volfrac"]) * n * n)
    cfe = F.Cell(n)
    rules = Rules(np.ones((n, n), bool), k, True, symmetric=True)
    obj = Objective("cell", (cfe, target, floor))
    rng = np.random.default_rng(seed)
    best = None
    if target == "poisson":
        rules_p = Rules(np.ones((n, n), bool), k, True, symmetric=False)
        for f0, how, S in poisson_seeds(n, k, m, obj, rules_p):
            S = local_search(S, rules_p, obj, 600, rng, m, f"{cell['id']} {how}")
            f1, _, raw = obj(S)
            log(f"{cell['id']}: {how}: {f0:.6f} -> {f1:.6f} {raw}")
            if raw[1] >= floor and (best is None or f1 < best[0]):
                best = (f1, f"seed: {how}; local search of {k}-element strip moves", S)
        return best
    for trial in range(4):
        R = (2.0, 2.5, 3.0)[trial % 3]
        xp = cell_simp(cfe, target, vf, R, floor, seed * 100 + trial)
        S, extra = valid_threshold(xp, np.ones((n, n), bool), rules, obj, m, rng, symmetric=True)
        if S is None:
            log(f"{cell['id']}: trial {trial} (filter {R}): no valid threshold")
            continue
        f0 = obj(S)[0]
        S = local_search(S, rules, obj, 800, rng, m, f"{cell['id']} trial {trial}")
        f1, _, raw = obj(S)
        log(f"{cell['id']}: trial {trial} (filter {R}, +{extra}): {f0:.6f} -> {f1:.6f} {raw}")
        if best is None or f1 < best[0]:
            best = (f1, f"SIMP on the periodic cell (symmetric designs, density filter {R}, projection), threshold, "
                        f"repair, local search of symmetric strip moves", S)
    return best


# ------------------------------------------------------------------ main


def write_cert(cell, how, design, form):
    fam = cell["family"]
    rel = f"collections/open-tables/refs/cells/{fam}/{cell['id']}.txt"
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    head = [f"{cell['id']}: {how}", "QV-Topo 1 (a numerical model); checker args: " + " ".join(cell["checker_args"])]
    if form == "simp":
        F.write_simp(path, design, head)
    else:
        F.write_binary(path, design, head)
    return rel, path


def main():
    a = sys.argv[1:]
    if a and a[0] == "grid":
        os.makedirs(os.path.dirname(GRID), exist_ok=True)
        with open(GRID, "w") as f:
            for c in grid_cells():
                f.write(json.dumps(c) + "\n")
        print(f"{len(grid_cells())} cells")
        return 0
    if len(a) >= 2 and a[0] == "replay88":
        replay88(find_cell(a[1]))
        return 0
    if len(a) >= 2 and a[0] == "base":
        cell = find_cell(a[1])
        if cell["family"] == "topopt-simp":
            replay88(cell, write=True)
        elif cell["family"].startswith("metacell"):
            lattice_base(cell)
        return 0
    if len(a) >= 2 and a[0] == "run":
        cell = find_cell(a[1])
        seed = int(a[2]) if len(a) > 2 else 1
        t = time.time()
        if cell["family"] == "topopt-simp":
            val, how, design = search_simp(cell, seed)
            form = "simp"
        elif cell["family"] == "topopt-binary":
            r = search_binary(cell, seed)
            if r is None:
                log(f"{cell['id']}: no valid design found")
                return 1
            val, how, design = r
            form = "binary"
        else:
            r = search_cell(cell, seed)
            if r is None:
                log(f"{cell['id']}: no valid design found")
                return 1
            val, how, design = r
            form = "binary"
        rel, path = write_cert(cell, how, design, form)
        got, out = check(cell["checker_args"], path)
        log(f"{cell['id']}: search value {val!r}; checker {got} ({None if got is None else float(got)}); "
            f"{time.time() - t:.0f} s")
        if got is None:
            print(out[-800:])
            return 1
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
