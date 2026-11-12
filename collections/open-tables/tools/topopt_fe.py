#!/usr/bin/env python3
"""numpy finite elements for the QV-Topo 1 searches (tools/topopt_search.py): the same model as
checkers/topopt_check.py (plane stress, E0 = 1, nu = 0.3, EMIN = 1e-9, unit square bilinear elements, the same
boundary conditions, the same density filter), with a block-banded Cholesky solver so that a solve takes milliseconds.
Only the searches use it; every value in the tables is the checker's (standard library only) on the written design."""
import numpy as np

E0, EMIN, NU = 1.0, 1e-9, 0.3


def element_stiffness():
    a11 = [[12, 3, -6, -3], [3, 12, 3, 0], [-6, 3, 12, -3], [-3, 0, -3, 12]]
    a12 = [[-6, -3, 0, 3], [-3, -6, -3, -6], [0, -3, -6, 3], [3, -6, 3, -6]]
    b11 = [[-4, 3, -2, 9], [3, -4, -9, 4], [-2, -9, -4, -3], [9, 4, -3, -4]]
    b12 = [[2, -3, 4, -9], [-3, 2, 9, -2], [4, 9, 2, 3], [-9, -2, 3, 2]]
    A = np.block([[np.array(a11), np.array(a12)], [np.array(a12).T, np.array(a11)]]).astype(float)
    B = np.block([[np.array(b11), np.array(b12)], [np.array(b12).T, np.array(b11)]]).astype(float)
    return (A + NU * B) / (24.0 * (1.0 - NU * NU))


KE = element_stiffness()


class BlockBanded:
    """SPD solver for a matrix whose degrees of freedom split into nb consecutive blocks of size m, block I coupled
    only to blocks I-w..I+w. Fixed degrees of freedom are replaced by identity rows."""

    def __init__(self, ndof, m, w, edof, fixed):
        self.ndof, self.m, self.w = ndof, m, w
        self.nb = ndof // m
        assert self.nb * m == ndof
        self.edof = edof                                    # (nel, 8)
        self.fixed = np.array(sorted(fixed), dtype=int)
        self.free_mask = np.ones(ndof, bool)
        self.free_mask[self.fixed] = False
        ii = np.repeat(edof, 8, axis=1).ravel()             # row index of each KE entry, element by element
        jj = np.tile(edof, (1, 8)).ravel()
        keep = (ii >= jj) & self.free_mask[ii] & self.free_mask[jj]
        self.keep = keep
        bi, bj = ii[keep] // m, jj[keep] // m
        assert np.all(bi - bj <= w) and np.all(bi >= bj)
        self.idx = (bj, bi - bj, ii[keep] % m, jj[keep] % m)
        self.ke_flat = np.tile(KE.ravel(), edof.shape[0])[keep]
        self.elem_of = np.repeat(np.arange(edof.shape[0]), 64)[keep]

    def factor(self, moduli):
        m, w, nb = self.m, self.w, self.nb
        Kb = np.zeros((nb, w + 1, m, m))
        np.add.at(Kb, self.idx, self.ke_flat * moduli[self.elem_of])
        diag = Kb[:, 0]                                     # symmetric fill of the diagonal blocks
        diag[:] = np.tril(diag) + np.transpose(np.tril(diag, -1), (0, 2, 1))
        fb, fl = self.fixed // m, self.fixed % m
        Kb[fb, 0, fl, fl] = 1.0
        L = np.zeros_like(Kb)                               # L[I, d] = L_{I+d, I}
        for I in range(nb):
            S = Kb[I, 0].copy()
            for J in range(max(0, I - w), I):
                X = L[J, I - J]
                S -= X @ X.T
            LII = np.linalg.cholesky(S)
            L[I, 0] = LII
            for R in range(I + 1, min(nb, I + w + 1)):
                T = Kb[I, R - I].copy()
                for J in range(max(0, R - w), I):
                    T -= L[J, R - J] @ L[J, I - J].T
                L[I, R - I] = np.linalg.solve(LII, T.T).T
        self.L = L

    def solve(self, F):
        """F: (ndof,) or (ndof, r); returns the same shape (fixed degrees of freedom 0)."""
        m, w, nb, L = self.m, self.w, self.nb, self.L
        one = F.ndim == 1
        Y = (F.reshape(-1, 1) if one else F).copy()
        Y[self.fixed] = 0.0
        Y = Y.reshape(nb, m, -1)
        for I in range(nb):
            r = Y[I]
            for J in range(max(0, I - w), I):
                r = r - L[J, I - J] @ Y[J]
            Y[I] = np.linalg.solve(L[I, 0], r)
        for I in range(nb - 1, -1, -1):
            r = Y[I]
            for R in range(I + 1, min(nb, I + w + 1)):
                r = r - L[I, R - I].T @ Y[R]
            Y[I] = np.linalg.solve(L[I, 0].T, r)
        Y = Y.reshape(self.ndof, -1)
        Y[self.fixed] = 0.0
        return Y[:, 0] if one else Y


# ------------------------------------------------------------------ structures (compliance)


class Structure:
    def __init__(self, case, nx, ny):
        self.case, self.nx, self.ny = case, nx, ny
        node = lambda ix, iy: (ny + 1) * ix + iy
        ndof = 2 * (nx + 1) * (ny + 1)
        IX, IY = np.meshgrid(np.arange(nx), np.arange(ny))     # arrays indexed [iy, ix]
        bl, br, tr, tl = node(IX, IY + 1), node(IX + 1, IY + 1), node(IX + 1, IY), node(IX, IY)
        edof = np.stack([2 * bl, 2 * bl + 1, 2 * br, 2 * br + 1, 2 * tr, 2 * tr + 1, 2 * tl, 2 * tl + 1], -1)
        self.edof = edof.reshape(-1, 8)                         # element e = iy * nx + ix
        self.design = np.ones((ny, nx), bool)
        if case == "mbb":
            fixed = {2 * node(0, iy) for iy in range(ny + 1)} | {2 * node(nx, ny) + 1}
            self.load = 2 * node(0, 0) + 1
            self.load_elems = [(0, 0)]
            self.supports = [[(0, iy) for iy in range(ny)], [(nx - 1, ny - 1)]]
        elif case == "cantilever":
            fixed = {2 * node(0, iy) + c for iy in range(ny + 1) for c in (0, 1)}
            self.load = 2 * node(nx, ny) + 1
            self.load_elems = [(nx - 1, ny - 1)]
            self.supports = [[(0, iy) for iy in range(ny)]]
        elif case == "lbracket":
            a = 2 * nx // 5
            self.design = (IX < a) | (IY >= nx - a)
            fixed = {2 * node(ix, 0) + c for ix in range(a + 1) for c in (0, 1)}
            yl = nx - a // 2
            self.load = 2 * node(nx, yl) + 1
            self.load_elems = [(nx - 1, yl - 1), (nx - 1, yl)]
            self.supports = [[(ix, 0) for ix in range(a)]]
        else:
            raise ValueError(case)
        self.fixed = fixed
        self.ndof = ndof
        self.solver = BlockBanded(ndof, 2 * (ny + 1), 1, self.edof, fixed)
        self.F = np.zeros(ndof)
        self.F[self.load] = -1.0
        self.n_design = int(self.design.sum())

    def analyse(self, moduli):
        """moduli (ny, nx) -> compliance, element energies u_e^T KE u_e (ny, nx)."""
        self.solver.factor(moduli.ravel())
        U = self.solver.solve(self.F)
        Ue = U[self.edof]
        ce = np.einsum("ij,jk,ik->i", Ue, KE, Ue).reshape(self.ny, self.nx)
        return float(-U[self.load]), ce


# ------------------------------------------------------------------ filters


def filter_weights(rmin):
    reach = int(np.ceil(rmin)) - 1
    out = []
    for dy in range(-reach, reach + 1):
        for dx in range(-reach, reach + 1):
            w = rmin - np.sqrt(dx * dx + dy * dy)
            if w > 0:
                out.append((dx, dy, w))
    return out


def shift(a, dx, dy, periodic):
    """b[iy, ix] = a[iy + dy, ix + dx] (0 outside unless periodic)."""
    if periodic:
        return np.roll(np.roll(a, -dy, axis=0), -dx, axis=1)
    ny, nx = a.shape
    b = np.zeros_like(a)
    ys, yd = (slice(dy, ny), slice(0, ny - dy)) if dy >= 0 else (slice(0, ny + dy), slice(-dy, ny))
    xs, xd = (slice(dx, nx), slice(0, nx - dx)) if dx >= 0 else (slice(0, nx + dx), slice(-dx, nx))
    b[yd, xd] = a[ys, xs]
    return b


class DensityFilter:
    def __init__(self, rmin, design, periodic=False):
        self.w = filter_weights(rmin)
        self.design = design.astype(float)
        self.periodic = periodic
        self.Hs = sum(w * shift(self.design, dx, dy, periodic) for dx, dy, w in self.w) * self.design
        self.Hs[self.Hs == 0] = 1.0

    def apply(self, x):
        xd = x * self.design
        return sum(w * shift(xd, dx, dy, self.periodic) for dx, dy, w in self.w) / self.Hs * self.design

    def transpose(self, g):
        gd = g / self.Hs * self.design
        return sum(w * shift(gd, -dx, -dy, self.periodic) for dx, dy, w in self.w) * self.design


# ------------------------------------------------------------------ periodic cells (homogenisation)


def fold(k, n):
    return 2 * k if 2 * k < n else 2 * (n - 1 - k) + 1


U0 = np.array([[0, 0, 1, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, .5, .5, .5, .5, 0]], float)


class Cell:
    def __init__(self, n):
        self.n = n
        fo = np.array([fold(k, n) for k in range(n)])
        nid = lambda c, r: fo[c % n] * n + fo[r % n]
        C_, R_ = np.meshgrid(np.arange(n), np.arange(n))      # [r, c]
        bl, br, tr, tl = nid(C_, R_ + 1), nid(C_ + 1, R_ + 1), nid(C_ + 1, R_), nid(C_, R_)
        edof = np.stack([2 * bl, 2 * bl + 1, 2 * br, 2 * br + 1, 2 * tr, 2 * tr + 1, 2 * tl, 2 * tl + 1], -1)
        self.edof = edof.reshape(-1, 8)                     # element e = r * n + c
        self.ndof = 2 * n * n
        self.solver = BlockBanded(self.ndof, 2 * n, 2, self.edof, {0, 1})
        self.keu0 = U0 @ KE                                 # (3, 8)

    def homogenise(self, moduli):
        """moduli (n, n) -> C (3, 3), and the element energy matrices e_ij (3, 3, n, n) with
        C_ij = sum_e moduli_e e_ij,e / n^2 (dC_ij / dmoduli_e = e_ij,e / n^2)."""
        n = self.n
        mod = moduli.ravel()
        self.solver.factor(mod)
        F = np.zeros((self.ndof, 3))
        for k in range(3):
            np.add.at(F[:, k], self.edof.ravel(), -(mod[:, None] * self.keu0[k][None, :]).ravel())
        chi = self.solver.solve(F)                          # (ndof, 3)
        W = U0[:, None, :] + np.transpose(chi[self.edof], (2, 0, 1))   # (3, nel, 8)
        KW = W @ KE                                         # (3, nel, 8)
        e = np.einsum("iea,jea->ije", W, KW)               # (3, 3, nel)
        C = (e * mod[None, None, :]).sum(-1) / (n * n)
        return C, e.reshape(3, 3, n, n)


# ------------------------------------------------------------------ rules (vectorised; the checker decides)


def square_maps(S, k, design, periodic):
    """full[oy, ox]: the k x k square with top-left (ox, oy) is all solid (inside the domain); empty: all void.
    For non-periodic grids the corner index is offset by k - 1 (corners from -(k-1))."""
    ny, nx = S.shape
    if periodic:
        P = S.astype(int)
        cnt = sum(np.roll(np.roll(P, -qy, 0), -qx, 1) for qy in range(k) for qx in range(k))
        return cnt == k * k, cnt == 0
    P = np.zeros((ny + 2 * (k - 1), nx + 2 * (k - 1)), int)
    P[k - 1:k - 1 + ny, k - 1:k - 1 + nx] = S & design
    D = np.zeros_like(P)
    D[k - 1:k - 1 + ny, k - 1:k - 1 + nx] = design
    H, W = ny + k - 1, nx + k - 1
    cnt = sum(P[qy:qy + H, qx:qx + W] for qy in range(k) for qx in range(k))
    dcnt = sum(D[qy:qy + H, qx:qx + W] for qy in range(k) for qx in range(k))
    return (cnt == k * k) & (dcnt == k * k), cnt == 0


def feature_ok(S, k, design, periodic):
    """(ok, bad mask): every solid in a full square, every void design element in an empty square, no point
    contact."""
    ny, nx = S.shape
    full, empty = square_maps(S, k, design, periodic)
    if periodic:
        cov_s = sum(np.roll(np.roll(full, qy, 0), qx, 1) for qy in range(k) for qx in range(k)) > 0
        cov_v = sum(np.roll(np.roll(empty, qy, 0), qx, 1) for qy in range(k) for qx in range(k)) > 0
    else:
        cov_s = sum(full[k - 1 - qy:k - 1 - qy + ny, k - 1 - qx:k - 1 - qx + nx]
                    for qy in range(k) for qx in range(k)) > 0
        cov_v = sum(empty[k - 1 - qy:k - 1 - qy + ny, k - 1 - qx:k - 1 - qx + nx]
                    for qy in range(k) for qx in range(k)) > 0
    bad = np.where(S, ~cov_s, ~cov_v) & design
    if periodic:
        a, b = S, np.roll(S, -1, 1)
        c, d = np.roll(S, -1, 0), np.roll(np.roll(S, -1, 0), -1, 1)
    else:
        a, b, c, d = S[:-1, :-1], S[:-1, 1:], S[1:, :-1], S[1:, 1:]
    pc = (a == d) & (b == c) & (a != b)
    return (not bad.any()) and (not pc.any()), bad, pc


def components(S, periodic):
    """Labels of the edge-connected components of S (BFS)."""
    ny, nx = S.shape
    lab = -np.ones((ny, nx), int)
    comps = 0
    for iy, ix in zip(*np.nonzero(S)):
        if lab[iy, ix] >= 0:
            continue
        stack = [(iy, ix)]
        lab[iy, ix] = comps
        while stack:
            y, x = stack.pop()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if periodic:
                    yy %= ny
                    xx %= nx
                elif not (0 <= yy < ny and 0 <= xx < nx):
                    continue
                if S[yy, xx] and lab[yy, xx] < 0:
                    lab[yy, xx] = comps
                    stack.append((yy, xx))
        comps += 1
    return lab, comps


def opening(S, k, design, periodic):
    """Union of the k x k solid squares inside S (removes thin solid parts)."""
    ny, nx = S.shape
    full, _ = square_maps(S, k, design, periodic)
    if periodic:
        return sum(np.roll(np.roll(full, qy, 0), qx, 1) for qy in range(k) for qx in range(k)) > 0
    return (sum(full[k - 1 - qy:k - 1 - qy + ny, k - 1 - qx:k - 1 - qx + nx]
                for qy in range(k) for qx in range(k)) > 0) & design


def closing(S, k, design, periodic):
    """Complement of the union of the k x k void squares (fills thin voids)."""
    ny, nx = S.shape
    _, empty = square_maps(S, k, design, periodic)
    if periodic:
        cov = sum(np.roll(np.roll(empty, qy, 0), qx, 1) for qy in range(k) for qx in range(k)) > 0
    else:
        cov = sum(empty[k - 1 - qy:k - 1 - qy + ny, k - 1 - qx:k - 1 - qx + nx]
                  for qy in range(k) for qx in range(k)) > 0
    return (~cov) & design


def write_binary(path, S, header):
    with open(path, "w") as f:
        for h in header:
            f.write(f"# {h}\n")
        for row in S:
            f.write("".join("1" if v else "0" for v in row) + "\n")


def write_simp(path, x, header):
    with open(path, "w") as f:
        for h in header:
            f.write(f"# {h}\n")
        for row in x:
            f.write(" ".join(f"{v:.6f}" if v > 0 else "0" for v in row) + "\n")
