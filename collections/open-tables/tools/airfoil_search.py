#!/usr/bin/env python3
"""A first search for the airfoil tables: CMA-ES over class-shape (CST) coefficients and the angle of attack
(Quantavane Open Tables; needs numpy, used only to speed up the panel solution; the score that counts is the one
checkers/airfoil_check.py gives the written certificate).

  python3 -I tools/airfoil_search.py CELLS.jsonl OUTDIR [--cells ID1,ID2] [--evals N] [--seed S] [--order N]

For each cell (mode ld or cd, Reynolds number, smallest largest-thickness, smallest lift), start from the CST fit of
the cell's best NACA baseline (or NACA 4412), minimise a penalised objective with CMA-ES (N. Hansen,
The CMA evolution strategy: a tutorial, arXiv:1604.00772), write the best design as a certificate (coefficients
rounded to 10 significant digits) and run the checker on it. One line of JSON per cell on stdout."""
import json
import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "checkers"))
import airfoil_check as A  # noqa: E402

CHECKER = os.path.join(HERE, "checkers", "airfoil_check.py")
XS = np.array(A.stations())
ALPHA_SCALE = 25.0                       # the search variable is alpha / 25, so that one step size suits all variables
MARGIN_CM, MARGIN_T, MARGIN_CL, MARGIN_TE = 0.0005, 0.0002, 0.0005, 0.05   # stay inside the constraints after rounding
np.seterr(all="ignore")                  # numpy 2.0 with Accelerate raises spurious flags in matmul on macOS


def bernstein(n):
    from math import comb
    return np.array([[comb(n, i) * x ** i * (1 - x) ** (n - i) for i in range(n + 1)] for x in XS])


def cst_y(coef, Bm):
    return np.sqrt(XS) * (1 - XS) * (Bm @ coef)


def fast_solution(nodes):
    """The Hess-Smith system of the checker, assembled with numpy (same formulas; numpy's log and arctan2)."""
    P = np.array(nodes)
    X, Y = P[:, 0], P[:, 1]
    N = len(X) - 1
    dxp, dyp = X[1:] - X[:-1], Y[1:] - Y[:-1]
    L = np.sqrt(dxp * dxp + dyp * dyp)
    sn, cs = dyp / L, dxp / L
    xm, ym = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1])
    dx0 = xm[:, None] - X[None, :-1]
    dy0 = ym[:, None] - Y[None, :-1]
    dx1 = xm[:, None] - X[None, 1:]
    dy1 = ym[:, None] - Y[None, 1:]
    with np.errstate(divide="ignore", invalid="ignore"):
        lnr = 0.5 * np.log((dx1 * dx1 + dy1 * dy1) / (dx0 * dx0 + dy0 * dy0))
    beta = np.arctan2(dy1 * dx0 - dx1 * dy0, dx1 * dx0 + dy1 * dy0)
    idx = np.arange(N)
    lnr[idx, idx] = 0.0
    beta[idx, idx] = math.pi
    sij = sn[:, None] * cs[None, :] - cs[:, None] * sn[None, :]
    cij = cs[:, None] * cs[None, :] + sn[:, None] * sn[None, :]
    k = 1.0 / (2.0 * math.pi)
    An = k * (sij * lnr + cij * beta)
    At = k * (sij * beta - cij * lnr)
    bn = (k * (cij * lnr - sij * beta)).sum(axis=1)
    bt = (k * (sij * lnr + cij * beta)).sum(axis=1)
    Afull = np.zeros((N + 1, N + 1))
    Afull[:N, :N], Afull[:N, N] = An, bn
    Afull[N, :N] = At[0] + At[N - 1]
    Afull[N, N] = bt[0] + bt[N - 1]
    rhs = np.zeros((N + 1, 2))
    rhs[:N, 0], rhs[N, 0] = sn, -(cs[0] + cs[N - 1])
    rhs[:N, 1], rhs[N, 1] = -cs, -(sn[0] + sn[N - 1])
    sol = np.linalg.solve(Afull, rhs)
    Atf = np.zeros((N, N + 1))
    Atf[:, :N], Atf[:, N] = At, bt
    return {"N": N, "Atf": Atf, "sol": sol, "xm": xm, "ym": ym, "len": L, "sn": sn, "cs": cs}


def fast_flow(ps, alpha):
    a = alpha * math.pi / 180.0
    sa, ca = math.sin(a), math.cos(a)
    s = ca * ps["sol"][:, 0] + sa * ps["sol"][:, 1]
    vt = ca * ps["cs"] + sa * ps["sn"] + ps["Atf"] @ s
    cp = 1.0 - vt * vt
    nx, ny = -ps["sn"], ps["cs"]
    dfx, dfy = -cp * ps["len"] * nx, -cp * ps["len"] * ny
    fx, fy = dfx.sum(), dfy.sum()
    mz = ((ps["xm"] - 0.25) * dfy - ps["ym"] * dfx).sum()
    return {"vt": vt.tolist(), "xm": ps["xm"].tolist(), "ym": ps["ym"].tolist(), "cl": fy * ca - fx * sa,
            "cm": -mz}


class Problem:
    def __init__(self, cell, order):
        p = cell["params"]
        self.mode, self.re = p["mode"], float(p["re"])
        self.tmin, self.clmin = float(p["tmin"]), float(p.get("clmin", "0"))
        self.order = order
        self.Bm = bernstein(order)

    def shape(self, z):
        n = self.order + 1
        return z[:n], z[n:2 * n], z[2 * n] * ALPHA_SCALE

    def score(self, z):
        """A value to minimise: -L/D or Cd, plus penalties; None when the model refuses the design. self.last_ok tells
        whether the design meets every constraint with a small margin (only those may become the best)."""
        self.last_ok = False
        up, lo, alpha = self.shape(z)
        if np.max(np.abs(up)) > 1 or np.max(np.abs(lo)) > 1 or not -5 <= alpha <= 15:
            return None
        yu, yl = cst_y(up, self.Bm), cst_y(lo, self.Bm)
        t = yu - yl
        if np.min(t[1:-1]) <= 0:
            return None
        th = float(np.max(t))
        nodes = [(float(x), float(y)) for x, y in zip(XS[::-1], yl[::-1])] + \
                [(float(x), float(y)) for x, y in zip(XS[1:], yu[1:])]
        (x0, y0), (x1, y1), (xn, yn) = nodes[0], nodes[1], nodes[-2]
        ux, uy, vx, vy = x1 - x0, y1 - y0, xn - x0, yn - y0
        if math.degrees(math.atan2(uy * vx - ux * vy, ux * vx + uy * vy)) < A.TE_MIN_DEG + MARGIN_TE:
            return None                          # the checker's trailing-edge wedge rule
        try:
            ps = fast_solution(nodes)
            fl = fast_flow(ps, float(alpha))
            v = A.viscous(fl, self.re)
        except (A.Refused, np.linalg.LinAlgError, ValueError, ZeroDivisionError, OverflowError):
            return None
        cl, cd, cm = fl["cl"], v["cd"], fl["cm"]
        viol = max(0.0, MARGIN_CM + A.CM_MIN - cm) + max(0.0, self.tmin + MARGIN_T - th)
        if self.mode == "cd":
            viol += max(0.0, self.clmin + MARGIN_CL - cl)
        self.last_ok = viol == 0.0
        if self.mode == "ld":
            if cl <= 0:
                return None
            return -cl / cd + 5000.0 * viol
        return cd + 1.0 * viol

    def feasible(self, z):
        up, lo, alpha = self.shape(z)
        t = cst_y(up, self.Bm) - cst_y(lo, self.Bm)
        return float(np.max(t)) >= self.tmin


def cma(f, ok, x0, sigma, evals, rng):
    n = len(x0)
    lam = 4 + int(3 * math.log(n))
    mu = lam // 2
    w = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1))
    w /= w.sum()
    mueff = 1 / np.sum(w ** 2)
    cc, cs = (4 + mueff / n) / (n + 4 + 2 * mueff / n), (mueff + 2) / (n + mueff + 5)
    c1 = 2 / ((n + 1.3) ** 2 + mueff)
    cmu = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff))
    damps = 1 + 2 * max(0, math.sqrt((mueff - 1) / (n + 1)) - 1) + cs
    chin = math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n))
    m, C = np.array(x0, float), np.eye(n)
    pc, ps = np.zeros(n), np.zeros(n)
    best, bestx, used = float("inf"), None, 0
    while used < evals:
        C = (C + C.T) / 2
        vals, Q = np.linalg.eigh(C)
        D = np.sqrt(np.maximum(vals, 1e-20))
        arz = rng.standard_normal((lam, n))
        ys = (arz * D) @ Q.T
        xs = m + sigma * ys
        fs = []
        for x in xs:
            v = f(x)
            used += 1
            fs.append(float("inf") if v is None else v)
            if v is not None and ok() and v < best:
                best, bestx = v, x.copy()
        order = np.argsort(fs)
        if not np.isfinite(fs[order[0]]):
            sigma *= 0.5
            continue
        ysel = ys[order[:mu]]
        yw = w @ ysel
        m = m + sigma * yw
        invsqrt = Q @ np.diag(1 / D) @ Q.T
        ps = (1 - cs) * ps + math.sqrt(cs * (2 - cs) * mueff) * (invsqrt @ yw)
        hs = np.linalg.norm(ps) / math.sqrt(1 - (1 - cs) ** (2 * used / lam)) < (1.4 + 2 / (n + 1)) * chin
        pc = (1 - cc) * pc + hs * math.sqrt(cc * (2 - cc) * mueff) * yw
        C = (1 - c1 - cmu) * C + c1 * (np.outer(pc, pc) + (1 - hs) * cc * (2 - cc) * C) + \
            cmu * (ysel.T * w) @ ysel
        sigma *= math.exp((cs / damps) * (np.linalg.norm(ps) / chin - 1))
        sigma = min(sigma, 0.5)
    return bestx, best


def fit_naca(code, order):
    up, lo = A.naca_surfaces(code, list(XS))
    from math import comb
    out = []
    for pts in (up, lo):
        x = np.array([p[0] for p in pts])
        y = np.array([p[1] for p in pts])
        keep = (x > 0) & (x < 1)
        xk = np.clip(x[keep], 1e-9, 1 - 1e-9)
        Bx = np.array([[comb(order, i) * xx ** i * (1 - xx) ** (order - i) for i in range(order + 1)] for xx in xk])
        G = (np.sqrt(xk) * (1 - xk))[:, None] * Bx
        out.append(np.linalg.lstsq(G, y[keep], rcond=None)[0])
    return out


def certificate_text(cell, z, order, note):
    up, lo, alpha = z[:order + 1], z[order + 1:2 * order + 2], z[2 * order + 2] * ALPHA_SCALE
    f = lambda v: f"{float(v):.10g}"
    return (f"# {cell['id']}: {note}\n# QV-Foil 1 (a numerical model, not a wind tunnel)\n"
            f"alpha {f(alpha)}\nupper {' '.join(f(v) for v in up)}\nlower {' '.join(f(v) for v in lo)}\n")


def run_checker(cell, path):
    args = cell["checker_args"]
    r = subprocess.run([sys.executable, "-I", CHECKER] + args + [path], capture_output=True, text=True)
    lines = r.stdout.strip().splitlines()
    return r.returncode, (lines[-1] if lines else ""), r.stdout


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        return 2
    cells_path, outdir = args[0], args[1]
    opts = dict(zip(args[2::2], args[3::2]))
    only = set(opts["--cells"].split(",")) if "--cells" in opts else None
    evals = int(opts.get("--evals", "1500"))
    order = int(opts.get("--order", "7"))
    rng = np.random.default_rng(int(opts.get("--seed", "1")))
    os.makedirs(outdir, exist_ok=True)
    for line in open(cells_path):
        if not line.strip():
            continue
        cell = json.loads(line)
        if only and cell["id"] not in only:
            continue
        prob = Problem(cell, order)
        base = (cell.get("baseline") or {}).get("naca") or "4412"
        alpha0 = float((cell.get("baseline") or {}).get("alpha", 4.0))
        up, lo = fit_naca(base, order)
        f0, x0 = None, None
        for da in (0.0, -0.5, -1.0, -1.5, -2.0, -3.0, 1.0):        # a start the model accepts, if there is one near
            z = np.concatenate([up, lo, [(alpha0 + da) / ALPHA_SCALE]])
            f0 = prob.score(z)
            x0 = z
            if f0 is not None:
                break
        x, fbest = cma(prob.score, lambda: prob.last_ok, x0, 0.02, evals, rng)
        if x is None:
            print(json.dumps({"cell": cell["id"], "start": f0, "found": False}), flush=True)
            continue
        path = os.path.join(outdir, cell["id"] + ".txt")
        with open(path, "w") as fh:
            fh.write(certificate_text(cell, x, order, f"CST design, CMA-ES from the CST fit of NACA {base} "
                                                          f"({evals} evaluations, order {order}, tools/airfoil_search.py)"))
        code, last, text = run_checker(cell, path)
        print(json.dumps({"cell": cell["id"], "start": f0, "search_best": fbest, "checker_exit": code,
                          "result": last, "file": path}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
