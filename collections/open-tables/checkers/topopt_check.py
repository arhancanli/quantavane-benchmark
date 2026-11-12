#!/usr/bin/env python3
"""QV-Topo 1: structures of least compliance and periodic material cells of extreme homogenised stiffness, scored in a
pinned finite-element model (Quantavane Open Tables; standard library only).

  python3 -I topopt_check.py compliance CASE NELX NELY VOLFRAC FORM PARAM SUBMISSION
  python3 -I topopt_check.py cell TARGET N VOLFRAC K FLOOR SUBMISSION

THIS IS A NUMERICAL MODEL. A score is what this program computes on the submitted design; it says nothing more about
a real part. The program never reads a reported value: it re-solves from the design alone.

The model (fixed; changing any of it makes a new model version, not an edit):
- Material: linear elastic, isotropic, plane stress, unit thickness, Young's modulus E0 = 1, Poisson's ratio 0.3.
  Void is the same material with E = EMIN = 1e-9 (an "ersatz" material, as in Andreassen et al. 2011), so that the
  stiffness matrix stays positive definite; it changes compliances by about one part in a billion.
- Mesh: square four-node bilinear elements of side 1, element stiffness matrix KE in closed form (the formula of
  E. Andreassen, A. Clausen, M. Schevenels, B. S. Lazarov, O. Sigmund, Struct. Multidisc. Optim. 43 (2011) 1-16,
  equivalent to exact integration). Element (ix, iy): column ix from the left, row iy from the top. Node (ix, iy) is
  the corner at x = ix, y = -iy.
- Solver: Cholesky factorisation of the stiffness matrix of the free degrees of freedom in profile (skyline) storage.
  The inner products of the factorisation and of the forward substitution, the filter sums and the energy sums are
  math.fsum of IEEE-754 products (correctly rounded, independent of the order); every other step is a single +, -, *,
  / or sqrt in a fixed order. So every machine with IEEE-754 double precision prints the same digits.

compliance CASE NELX NELY VOLFRAC FORM PARAM: least compliance under one unit load.
  CASE mbb         the half MBB beam of Sigmund (2001) and Andreassen et al. (2011): left edge fixed horizontally
                   (symmetry line), bottom-right corner node fixed vertically, unit downward load at the top-left node.
  CASE cantilever  left edge clamped, unit downward load at the bottom-right corner node (both papers, section 5.1).
  CASE lbracket    NELX = NELY = L, L a multiple of 5: an L-shaped domain, legs 2L/5 wide; the elements with
                   ix >= 2L/5 and iy < 3L/5 are passive (void, not part of the design); the top edge of the vertical
                   leg (nodes iy = 0, ix <= 2L/5) is clamped; unit downward load at the node ix = L, iy = 4L/5 (the
                   middle of the right end of the horizontal leg).
  FORM simp, PARAM = rmin: the design is a field x in [0, 1] on the design elements (passive ones 0). Physical
  densities xPhys = (H x) / Hs with the linear density filter of radius rmin, H_ei = max(0, rmin - |c_e - c_i|) over
  design elements i (the filter of the 88-line code; passive elements are outside it). Stiffness of element e:
  EMIN + xPhys_e^3 (E0 - EMIN) (SIMP, penalty 3). Volume: the sum of xPhys over the design elements is at most
  VOLFRAC times their number. Load path: the elements with xPhys >= 1/2 form one edge-connected piece that contains
  an element at the load node and elements at the supports (below).
  FORM binary, PARAM = k: the design is 0 (void) or 1 (solid) per element; at most VOLFRAC times the number of design
  elements are solid. Minimum feature size k: every solid element lies in a k x k square of solid elements inside the
  domain, and every void design element lies in a k x k square of void elements (squares may extend outside the domain
  or into the passive region, which count as void). No 2 x 2 window has its two solid elements on one diagonal only
  (no point contacts). The solid elements form one edge-connected piece that contains an element at the load node and
  elements at the supports.
  Supports, as elements: mbb, an element on the left edge and the bottom-right element; cantilever, an element on the
  left edge; lbracket, an element on the clamped edge.
  Score: the compliance F.U (work of the unit load), rounded UP to 0.001 (smaller is better).

cell TARGET N VOLFRAC K FLOOR: an N x N periodic cell of a two-dimensional material, 0/1 per element, at most
  VOLFRAC N^2 solid elements, minimum feature size K and no point contacts as above (periodically: squares and windows
  wrap around), the solid elements one edge-connected piece on the torus that wraps around in both directions (a
  connected material). The homogenised stiffness tensor C (Voigt notation, engineering shear strain, plane stress) by
  the energy method with periodic boundary conditions: for each unit average strain (1,0,0), (0,1,0), (0,0,1) the
  periodic fluctuation that minimises the energy (one node fixed), then
  C_ij = (1/N^2) sum_e (u0_i + chi_i)_e^T K_e (u0_j + chi_j)_e. No symmetry of the cell is required.
  TARGET bulk:    (C11 + C22 + 2 C12) / 4 (the bulk modulus under a hydrostatic strain), rounded DOWN to 1e-6, larger
                  is better. The Hashin-Shtrikman upper bound kappa_HS = f k1 m1 / ((1 - f) k1 + m1) (k1, m1: the
                  solid's plane-stress bulk and shear moduli, f = VOLFRAC) bounds the exact bulk modulus of every
                  cell, isotropic or not; bilinear elements are slightly too stiff, so on the grid it is a reference
                  that only discretisation error could pass.
  TARGET shear:   C33, rounded DOWN to 1e-6, larger is better (the Voigt bound f m1 bounds it, also on the grid; the
                  Hashin-Shtrikman shear bound holds only for isotropic cells and is printed for comparison).
  TARGET poisson: with S = C^-1, the Poisson's ratios of uniaxial stress along the two axes, nu12 = -S12/S11 and
                  nu21 = -S12/S22; the score is the larger, rounded UP to 1e-6, smaller is better. Refused if a Young's
                  modulus 1/S11 or 1/S22 is below FLOOR (a stiffness floor, so that a mechanism cannot score).

SUBMISSION, a text file ('#' starts a comment; blank lines ignored): NELY lines of NELX entries (cell: N lines of N),
row iy = 0 (the top) first. binary and cell: characters 0 and 1 (spaces allowed); simp: decimal numbers in [0, 1]
separated by spaces. Output: the computed values; the last line is 'RESULT v' (v an exact fraction); exit status 0
only for a scored design, 1 for a refused one, 2 for a usage error."""
import math
import sys
from fractions import Fraction
from operator import mul

E0 = 1.0
EMIN = 1e-9
NU = 0.3
PENAL = 3                    # SIMP penalty; x^3 is computed as x * x * x
CASES = ("mbb", "cantilever", "lbracket")
TARGETS = ("bulk", "shear", "poisson")
MAX_ELEMENTS = 40000
fsum = math.fsum


class Refused(Exception):
    pass


# ------------------------------------------------------------------ element stiffness (unit square, E = 1)


def element_stiffness():
    """KE of a unit square bilinear element, plane stress, E = 1, nu = NU; degrees of freedom (x, y) of the corners in
    the order bottom-left, bottom-right, top-right, top-left (Andreassen et al. 2011, lines 8-12 of their code)."""
    a11 = [[12, 3, -6, -3], [3, 12, 3, 0], [-6, 3, 12, -3], [-3, 0, -3, 12]]
    a12 = [[-6, -3, 0, 3], [-3, -6, -3, -6], [0, -3, -6, 3], [3, -6, 3, -6]]
    b11 = [[-4, 3, -2, 9], [3, -4, -9, 4], [-2, -9, -4, -3], [9, 4, -3, -4]]
    b12 = [[2, -3, 4, -9], [-3, 2, 9, -2], [4, 9, 2, 3], [-9, -2, 3, 2]]

    def block(m11, m12):
        top = [m11[i] + m12[i] for i in range(4)]
        bottom = [[m12[j][i] for j in range(4)] + m11[i] for i in range(4)]
        return top + bottom
    A, B = block(a11, a12), block(b11, b12)
    factor = 1.0 / (1.0 - NU * NU) / 24.0
    return [[factor * (A[i][j] + NU * B[i][j]) for j in range(8)] for i in range(8)]


KE = element_stiffness()


# ------------------------------------------------------------------ the linear solver


def solve(ndof, elements, fixed, rhs_list):
    """Solve K u = f for each f in rhs_list. elements: (modulus, dofs) with dofs the 8 global degrees of freedom in KE's
    order; fixed: degrees of freedom held at 0; rhs: dicts {dof: value}. Returns full displacement lists."""
    free = [d for d in range(ndof) if d not in fixed]
    red = [-1] * ndof
    for i, d in enumerate(free):
        red[d] = i
    n = len(free)
    start = list(range(n))
    for _, dofs in elements:
        r = [red[d] for d in dofs if red[d] >= 0]
        lo = min(r) if r else 0
        for i in r:
            if lo < start[i]:
                start[i] = lo
    rows = [[0.0] * (i - start[i] + 1) for i in range(n)]
    for E, dofs in elements:
        r = [red[d] for d in dofs]
        for a in range(8):
            i = r[a]
            if i < 0:
                continue
            row, si, Ka = rows[i], start[i], KE[a]
            for b in range(8):
                j = r[b]
                if 0 <= j <= i:
                    row[j - si] += E * Ka[b]
    # Cholesky factorisation in place, row by row (profile storage)
    for i in range(n):
        si, Ai = start[i], rows[i]
        Li = []
        for j in range(si, i):
            Lj, sj = rows[j], start[j]
            if sj >= si:
                s = fsum(map(mul, Li[sj - si:], Lj))
            else:
                s = fsum(map(mul, Li, Lj[si - sj:]))
            Li.append((Ai[j - si] - s) / Lj[-1])
        d = Ai[-1] - fsum(map(mul, Li, Li))
        if not d > 0.0:
            raise Refused("the stiffness matrix is not positive definite (the structure is not supported)")
        Li.append(math.sqrt(d))
        rows[i] = Li
    out = []
    for f in rhs_list:
        y = [0.0] * n
        for d, v in f.items():
            if red[d] >= 0:
                y[red[d]] = v
        for i in range(n):                                   # forward: L y = f
            si, Li = start[i], rows[i]
            y[i] = (y[i] - fsum(map(mul, Li[:-1], y[si:i]))) / Li[-1]
        for i in range(n - 1, -1, -1):                       # backward: L^T u = y
            si, Li = start[i], rows[i]
            y[i] = y[i] / Li[-1]
            yi = y[i]
            for j in range(si, i):
                y[j] -= Li[j - si] * yi
        u = [0.0] * ndof
        for i, d in enumerate(free):
            u[d] = y[i]
        out.append(u)
    return out


# ------------------------------------------------------------------ reading a design


def read_grid(path, ncols, nrows, kind):
    rows = []
    with open(path) as fh:
        for raw in fh:
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if len(rows) >= nrows:
                raise Refused(f"more than {nrows} rows")
            if kind == "binary":
                s = line.replace(" ", "").replace("\t", "")
                if len(s) != ncols or any(ch not in "01" for ch in s):
                    raise Refused(f"row {len(rows)}: expected {ncols} characters 0 or 1")
                rows.append([1 if ch == "1" else 0 for ch in s])
            else:
                toks = line.split()
                if len(toks) != ncols:
                    raise Refused(f"row {len(rows)}: expected {ncols} numbers, got {len(toks)}")
                vals = []
                for t in toks:
                    try:
                        v = float(t)
                    except ValueError:
                        raise Refused(f"row {len(rows)}: not a number: {t[:20]}")
                    if not (0.0 <= v <= 1.0):
                        raise Refused(f"row {len(rows)}: value {t[:20]} outside [0, 1]")
                    vals.append(v)
                rows.append(vals)
    if len(rows) != nrows:
        raise Refused(f"expected {nrows} rows, got {len(rows)}")
    return rows          # rows[iy][ix]


# ------------------------------------------------------------------ geometric rules


def components(cells, neighbours):
    """Edge-connected components of a set of cells (BFS in a fixed order)."""
    seen, comps = set(), []
    for c in sorted(cells):
        if c in seen:
            continue
        comp, stack = [c], [c]
        seen.add(c)
        while stack:
            u = stack.pop()
            for v in neighbours(u):
                if v in cells and v not in seen:
                    seen.add(v)
                    comp.append(v)
                    stack.append(v)
        comps.append(comp)
    return comps


def check_feature(solid, nx, ny, k, design, periodic):
    """Every solid element in a k x k solid square, every void design element in a k x k void square; no point
    contacts. solid(ix, iy) -> bool for in-range cells; design(ix, iy) -> bool (False: passive). Outside the domain
    counts as void (non-periodic); periodic squares and windows wrap around."""
    def is_solid(ix, iy):
        if periodic:
            return solid(ix % nx, iy % ny)
        if 0 <= ix < nx and 0 <= iy < ny and design(ix, iy):
            return solid(ix, iy)
        return False
    lo = 0 if periodic else -(k - 1)
    full, empty = set(), set()                           # top-left corners of all-solid and all-void k x k squares
    for oy in range(lo, ny):
        for ox in range(lo, nx):
            cnt = sum(1 for qy in range(oy, oy + k) for qx in range(ox, ox + k) if is_solid(qx, qy))
            if cnt == 0:
                empty.add((ox, oy))
            elif cnt == k * k and (periodic or (0 <= ox and ox + k <= nx and 0 <= oy and oy + k <= ny)):
                full.add((ox, oy))
    for iy in range(ny):
        for ix in range(nx):
            if not (periodic or design(ix, iy)):
                continue
            s = is_solid(ix, iy)
            pool = full if s else empty
            ok = False
            for oy in range(iy - k + 1, iy + 1):
                for ox in range(ix - k + 1, ix + 1):
                    key = (ox % nx, oy % ny) if periodic else (ox, oy)
                    if key in pool:
                        ok = True
                        break
                if ok:
                    break
            if not ok:
                raise Refused(f"minimum feature size {k}: the {'solid' if s else 'void'} element at column {ix}, row "
                              f"{iy} is not inside a {k} x {k} {'solid' if s else 'void'} square")
    last_x, last_y = (nx, ny) if periodic else (nx - 1, ny - 1)
    for iy in range(last_y):
        for ix in range(last_x):
            a, b = is_solid(ix, iy), is_solid(ix + 1, iy)
            c, d = is_solid(ix, iy + 1), is_solid(ix + 1, iy + 1)
            if a == d and b == c and a != b:
                raise Refused(f"point contact (a 2 x 2 checkerboard window) at column {ix}, row {iy}")


# ------------------------------------------------------------------ compliance problems


def case_setup(case, nx, ny):
    """Nodes, load, fixed degrees of freedom, design predicate, required elements."""
    def node(ix, iy):
        return (ny + 1) * ix + iy
    ndof = 2 * (nx + 1) * (ny + 1)
    if case == "mbb":
        fixed = {2 * node(0, iy) for iy in range(ny + 1)} | {2 * node(nx, ny) + 1}
        load = 2 * node(0, 0) + 1
        def design(ix, iy):
            return True
        load_elems = [(0, 0)]
        supports = [("left edge", [(0, iy) for iy in range(ny)]), ("bottom-right corner", [(nx - 1, ny - 1)])]
    elif case == "cantilever":
        fixed = {2 * node(0, iy) + c for iy in range(ny + 1) for c in (0, 1)}
        load = 2 * node(nx, ny) + 1
        def design(ix, iy):
            return True
        load_elems = [(nx - 1, ny - 1)]
        supports = [("clamped left edge", [(0, iy) for iy in range(ny)])]
    elif case == "lbracket":
        if nx != ny or nx % 5:
            raise ValueError("lbracket needs NELX = NELY, a multiple of 5")
        a = 2 * nx // 5
        def design(ix, iy):
            return ix < a or iy >= nx - a
        fixed = {2 * node(ix, 0) + c for ix in range(a + 1) for c in (0, 1)}
        yl = nx - a // 2
        load = 2 * node(nx, yl) + 1
        load_elems = [(nx - 1, yl - 1), (nx - 1, yl)]
        supports = [("clamped top edge", [(ix, 0) for ix in range(a)])]
    else:
        raise ValueError("unknown case")
    return ndof, node, fixed, load, design, load_elems, supports


def density_filter(x, nx, ny, rmin, design):
    """xPhys = (H x) / Hs, H_ei = max(0, rmin - distance), design elements only."""
    reach = int(math.ceil(rmin)) - 1
    weights = []
    for dy in range(-reach, reach + 1):
        for dx in range(-reach, reach + 1):
            w = rmin - math.sqrt(float(dx * dx + dy * dy))
            if w > 0.0:
                weights.append((dx, dy, w))
    phys = [[0.0] * nx for _ in range(ny)]
    for iy in range(ny):
        for ix in range(nx):
            if not design(ix, iy):
                continue
            num, den = [], []
            for dx, dy, w in weights:
                jx, jy = ix + dx, iy + dy
                if 0 <= jx < nx and 0 <= jy < ny and design(jx, jy):
                    num.append(w * x[jy][jx])
                    den.append(w)
            phys[iy][ix] = fsum(num) / fsum(den)
    return phys


def compliance(case, nx, ny, volfrac, form, param, path):
    ndof, node, fixed, load, design, load_elems, supports = case_setup(case, nx, ny)
    grid = read_grid(path, nx, ny, "binary" if form == "binary" else "simp")
    n_design = sum(1 for iy in range(ny) for ix in range(nx) if design(ix, iy))
    for iy in range(ny):
        for ix in range(nx):
            if not design(ix, iy) and grid[iy][ix] != 0:
                raise Refused(f"element at column {ix}, row {iy} is passive (outside the design domain) and must be 0")
    if form == "binary":
        k = param
        count = sum(grid[iy][ix] for iy in range(ny) for ix in range(nx))
        if Fraction(count) > volfrac * n_design:
            raise Refused(f"{count} solid elements, more than {volfrac} x {n_design}")
        check_feature(lambda ix, iy: grid[iy][ix] == 1, nx, ny, k, design, False)
        solid = {(ix, iy) for iy in range(ny) for ix in range(nx) if grid[iy][ix] == 1}
        moduli = [[E0 if grid[iy][ix] else EMIN for ix in range(nx)] for iy in range(ny)]
        vol_text = f"{count} solid elements of {n_design} (fraction {count / n_design:.6f}; limit {volfrac})"
    else:
        rmin = param
        dens = density_filter(grid, nx, ny, rmin, design)
        vol = fsum(dens[iy][ix] for iy in range(ny) for ix in range(nx))
        limit = float(volfrac * n_design)
        if not vol <= limit:
            raise Refused(f"volume {vol!r} of the filtered densities exceeds {volfrac} x {n_design} = {limit!r}")
        solid = {(ix, iy) for iy in range(ny) for ix in range(nx) if design(ix, iy) and dens[iy][ix] >= 0.5}
        moduli = [[EMIN + dens[iy][ix] * dens[iy][ix] * dens[iy][ix] * (E0 - EMIN) if design(ix, iy) else EMIN
                   for ix in range(nx)] for iy in range(ny)]
        grey = sum(1 for iy in range(ny) for ix in range(nx) if design(ix, iy) and 0.1 < dens[iy][ix] < 0.9)
        vol_text = (f"filtered volume {vol / n_design:.6f} (limit {volfrac}); {len(solid)} elements with xPhys >= 1/2, "
                    f"{grey} grey (0.1 < xPhys < 0.9)")
    # load path
    if not solid:
        raise Refused("no material")

    def nbrs(c):
        ix, iy = c
        return ((ix - 1, iy), (ix + 1, iy), (ix, iy - 1), (ix, iy + 1))
    comps = components(solid, nbrs)
    what = "solid elements" if form == "binary" else "elements with xPhys >= 1/2"
    if len(comps) != 1:
        raise Refused(f"the {what} form {len(comps)} separate pieces (sizes {sorted(len(c) for c in comps)[::-1][:6]}); "
                      f"one connected piece is required")
    if not any(e in solid for e in load_elems):
        raise Refused(f"no {what[:-1]} at the load node")
    for name, elems in supports:
        if not any(e in solid for e in elems):
            raise Refused(f"no {what[:-1]} at the support ({name})")
    elements = []
    for ix in range(nx):
        for iy in range(ny):
            bl, br, tr, tl = node(ix, iy + 1), node(ix + 1, iy + 1), node(ix + 1, iy), node(ix, iy)
            dofs = (2 * bl, 2 * bl + 1, 2 * br, 2 * br + 1, 2 * tr, 2 * tr + 1, 2 * tl, 2 * tl + 1)
            elements.append((moduli[iy][ix], dofs))
    (u,) = solve(ndof, elements, fixed, [{load: -1.0}])
    c = -u[load]
    if not (c > 0.0 and math.isfinite(c)):
        raise Refused("compliance not positive")
    print(f"QV-Topo 1 compliance: case {case}, {nx} x {ny} elements, {form} "
          f"({'filter radius' if form == 'simp' else 'minimum feature size'} {param})")
    print(vol_text)
    print(f"compliance {c!r} = {c:.9f}")
    score = Fraction(math.ceil(Fraction(c) * 1000), 1000)
    print(f"score: compliance rounded up to 0.001 = {float(score):.3f}")
    return score


# ------------------------------------------------------------------ periodic cells


def fold(k, n):
    """Position of row or column k in the folded order 0, n-1, 1, n-2, ... (neighbours on the circle are at most two
    positions apart, so the periodic stiffness matrix has a narrow profile)."""
    return 2 * k if 2 * k < n else 2 * (n - 1 - k) + 1


def homogenise(grid, n, moduli=None):
    """The homogenised tensor C (3 x 3, Voigt, engineering shear) of the periodic cell; grid[r][c] in {0, 1} or, with
    moduli given, moduli[r][c] the element moduli."""
    if moduli is None:
        moduli = [[E0 if grid[r][c] else EMIN for c in range(n)] for r in range(n)]

    def nid(c, r):
        return fold(c % n, n) * n + fold(r % n, n)
    ndof = 2 * n * n
    elements, edofs = [], []
    for r in range(n):
        for c in range(n):
            bl, br, tr, tl = nid(c, r + 1), nid(c + 1, r + 1), nid(c + 1, r), nid(c, r)
            dofs = (2 * bl, 2 * bl + 1, 2 * br, 2 * br + 1, 2 * tr, 2 * tr + 1, 2 * tl, 2 * tl + 1)
            elements.append((moduli[r][c], dofs))
            edofs.append(dofs)
    u0 = ([0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0],      # unit strain e11: u = (x, 0) at BL, BR, TR, TL
          [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0],      # unit strain e22: u = (0, y)
          [0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0])      # unit engineering shear g12: u = (y/2, x/2)
    ke_u0 = [[fsum(map(mul, KE[a], u)) for a in range(8)] for u in u0]
    rhs = []
    for k in range(3):
        parts = {}
        for E, dofs in elements:
            for a in range(8):
                parts.setdefault(dofs[a], []).append(-E * ke_u0[k][a])
        rhs.append({d: fsum(v) for d, v in parts.items()})
    fixed = {0, 1}                                         # node (0, 0): position 0 in the folded order
    chis = solve(ndof, elements, fixed, rhs)
    C = [[0.0] * 3 for _ in range(3)]
    tot = [[[] for _ in range(3)] for _ in range(3)]
    for (E, dofs) in elements:
        w = [[u0[k][a] + chis[k][dofs[a]] for a in range(8)] for k in range(3)]
        kw = [[fsum(map(mul, KE[a], w[k])) for a in range(8)] for k in range(3)]
        for i in range(3):
            for j in range(i, 3):
                tot[i][j].append(E * fsum(map(mul, w[i], kw[j])))
    area = float(n * n)
    for i in range(3):
        for j in range(i, 3):
            C[i][j] = C[j][i] = fsum(tot[i][j]) / area
    return C


def solid_moduli():
    k1 = E0 / (2.0 * (1.0 - NU))         # plane-stress bulk modulus
    m1 = E0 / (2.0 * (1.0 + NU))         # shear modulus
    return k1, m1


def hs_bounds(f):
    k1, m1 = solid_moduli()
    kappa = f * k1 * m1 / ((1.0 - f) * k1 + m1)
    mu = f * k1 * m1 / (k1 + (1.0 - f) * (k1 + 2.0 * m1))
    return kappa, mu


def wraps(cells, n):
    """Whether one edge-connected set of cells on the n x n torus wraps around in both directions: a search that
    records each cell's position in the plane finds two independent periods."""
    start = min(cells)
    lift = {start: start}
    stack = [start]
    periods = set()
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
    periods = sorted(periods)
    for i in range(len(periods)):
        for j in range(i + 1, len(periods)):
            if periods[i][0] * periods[j][1] - periods[i][1] * periods[j][0] != 0:
                return True
    return False


def cell(target, n, volfrac, k, floor, path):
    grid = read_grid(path, n, n, "binary")
    count = sum(map(sum, grid))
    if Fraction(count) > volfrac * n * n:
        raise Refused(f"{count} solid elements, more than {volfrac} x {n * n}")
    check_feature(lambda ix, iy: grid[iy][ix] == 1, n, n, k, lambda ix, iy: True, True)
    solid = {(c, r) for r in range(n) for c in range(n) if grid[r][c]}
    if not solid:
        raise Refused("no material")

    def nbrs(u):
        c, r = u
        return (((c - 1) % n, r), ((c + 1) % n, r), (c, (r - 1) % n), (c, (r + 1) % n))
    comps = components(solid, nbrs)
    if len(comps) != 1:
        raise Refused(f"the solid elements form {len(comps)} separate pieces on the torus; one is required")
    if not wraps(solid, n):
        raise Refused("the solid does not wrap around the cell in both directions (not a connected material)")
    C = homogenise(grid, n)
    f = count / (n * n)
    kappa_hs, mu_hs = hs_bounds(float(volfrac))
    k1, m1 = solid_moduli()
    print(f"QV-Topo 1 cell: {n} x {n} periodic, {count} solid elements (fraction {f:.6f}; limit {volfrac}), "
          f"minimum feature size {k}")
    print("homogenised C (Voigt, engineering shear):")
    for i in range(3):
        print("  " + "  ".join(f"{C[i][j]: .9f}" for j in range(3)))
    bulk = (C[0][0] + C[1][1] + 2.0 * C[0][1]) / 4.0
    print(f"bulk (C11 + C22 + 2 C12)/4 = {bulk:.9f} (Hashin-Shtrikman upper bound at {volfrac}: {kappa_hs:.9f}, ratio "
          f"{bulk / kappa_hs:.6f})")
    print(f"shear C33 = {C[2][2]:.9f} (Voigt bound {float(volfrac) * m1:.9f}; isotropic Hashin-Shtrikman bound "
          f"{mu_hs:.9f})")
    S = inverse3(C)
    nu12, nu21 = -S[0][1] / S[0][0], -S[0][1] / S[1][1]
    e1, e2 = 1.0 / S[0][0], 1.0 / S[1][1]
    print(f"uniaxial stress: Young's moduli E1 = {e1:.9f}, E2 = {e2:.9f}; Poisson's ratios nu12 = {nu12:.9f}, "
          f"nu21 = {nu21:.9f}")
    if target == "bulk":
        score = Fraction(math.floor(Fraction(bulk) * 1000000), 1000000)
        print(f"score: bulk modulus rounded down to 0.000001 = {float(score):.6f}")
    elif target == "shear":
        score = Fraction(math.floor(Fraction(C[2][2]) * 1000000), 1000000)
        print(f"score: shear modulus C33 rounded down to 0.000001 = {float(score):.6f}")
    else:
        if not (e1 >= float(floor) and e2 >= float(floor)):
            raise Refused(f"a Young's modulus ({min(e1, e2):.9f}) is below the stiffness floor {floor}")
        score = Fraction(math.ceil(Fraction(max(nu12, nu21)) * 1000000), 1000000)
        print(f"score: the larger Poisson's ratio rounded up to 0.000001 = {float(score):.6f}")
    return score


def inverse3(C):
    """The inverse of a symmetric positive definite 3 x 3 matrix by cofactors (fixed order of operations)."""
    a, b, c = C[0]
    _, d, e = C[1]
    f = C[2][2]
    A = d * f - e * e
    B = c * e - b * f
    D = b * e - c * d
    det = a * A + b * B + c * D
    if not det > 0.0:
        raise Refused("the homogenised tensor is singular")
    E_ = a * f - c * c
    F_ = b * c - a * e
    G = a * d - b * b
    return [[A / det, B / det, D / det], [B / det, E_ / det, F_ / det], [D / det, F_ / det, G / det]]


def exact_text(fr):
    return f"{fr.numerator}" if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"


def decimal_arg(s, lo, hi):
    v = Fraction(s)
    if not (lo <= v <= hi) or len(s) > 12:
        raise ValueError
    return v


def main():
    argv = sys.argv[1:]
    try:
        if len(argv) == 8 and argv[0] == "compliance":
            _, case, nx_s, ny_s, vf_s, form, param_s, path = argv
            nx, ny = int(nx_s), int(ny_s)
            vf = decimal_arg(vf_s, Fraction(1, 100), Fraction(99, 100))
            if case not in CASES or form not in ("simp", "binary") or not (2 <= nx and 2 <= ny and nx * ny <= MAX_ELEMENTS):
                raise ValueError
            if form == "binary":
                param = int(param_s)
                if not 1 <= param <= 6:
                    raise ValueError
            else:
                param = float(decimal_arg(param_s, Fraction(1), Fraction(20)))
            score = compliance(case, nx, ny, vf, form, param, path)
        elif len(argv) == 7 and argv[0] == "cell":
            _, target, n_s, vf_s, k_s, floor_s, path = argv
            n, k = int(n_s), int(k_s)
            vf = decimal_arg(vf_s, Fraction(1, 100), Fraction(99, 100))
            floor = decimal_arg(floor_s, Fraction(0), Fraction(1))
            if target not in TARGETS or not (4 <= n <= 96 and n % 2 == 0 and 1 <= k <= 6):
                raise ValueError
            score = cell(target, n, vf, k, floor, path)
        else:
            raise ValueError
        print(f"RESULT {exact_text(score)}")
        return 0
    except Refused as e:
        print(f"NOT SCORED: {e}")
        return 1
    except (ValueError, ZeroDivisionError):
        print(__doc__)
        print("usage error: see above")
        return 2
    except OSError as e:
        print(f"cannot read the submission: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
