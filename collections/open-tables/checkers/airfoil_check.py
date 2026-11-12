#!/usr/bin/env python3
"""QV-Foil 1: lift and drag of a two-dimensional airfoil in a pinned numerical flow model (Quantavane Open Tables;
standard library only).

  python3 -I airfoil_check.py MODE RE TMIN CLMIN SUBMISSION

THIS IS A NUMERICAL MODEL, NOT A WIND TUNNEL. The score is what this program computes; it says nothing more about a
real wing. The model is classical and simple (a 1960s-70s design-office method), fixed here so that every
submission is scored the same way:

- Incompressible potential flow by the Hess-Smith panel method (J. L. Hess, A. M. O. Smith, Prog. Aerospace Sci. 8
  (1967) 1-138): constant-strength sources on each panel, one vortex strength shared by all panels, the Kutta
  condition as equal tangential speeds on the two trailing-edge panels. 160 panels: 80 per surface, nodes at
  x = (1 - cos(pi i / 80)) / 2. Lift and the moment about the quarter chord from the surface pressures.
- Laminar boundary layer from the stagnation point by Thwaites' method (B. Thwaites, Aeronaut. Q. 1 (1949) 245-280)
  with the Cebeci-Bradshaw fits for H and l; transition by Michel's criterion (R. Michel, ONERA Rep. 1/1578A, 1951),
  or at laminar separation (lambda < -0.09), whichever comes first.
- Turbulent boundary layer by Head's entrainment method (M. R. Head, ARC R&M 3152, 1958) with the Ludwieg-Tillmann
  skin friction (Ing.-Arch. 17 (1949) 288-299), started with H = 1.4, integrated station to station by Heun's method.
- Profile drag by the Squire-Young formula (H. B. Squire, A. D. Young, ARC R&M 1838, 1938) at the last station of
  each surface, the last control point with x <= 0.99 (closer to the sharp trailing edge the potential flow slows
  towards its stagnation point and no boundary-layer method applies). Viscous effects do not feed back on the
  pressures (one-way coupling).

A submission is REFUSED when: the shape is not a simple closed curve with the upper surface above the lower one; its
largest thickness is below TMIN (thickness of the 160-panel polygon, measured vertically); the trailing-edge wedge
angle (between the two panels at the trailing edge) is below 4 degrees; the pitching moment about the quarter chord
is below -0.10 (a nose-down limit, as in most design problems: without it the one-way model rewards extreme aft
camber, whose real lift it overstates); the angle of attack is
outside [-5, 15] degrees; the turbulent boundary layer separates (H >= 2.4) on either surface; or, in mode cd, the
lift coefficient is below CLMIN.

MODE ld: the score is the lift-to-drag ratio Cl/Cd (larger is better), rounded DOWN to 0.01. MODE cd: the score is
the drag coefficient (smaller is better) with Cl >= CLMIN, rounded UP to 0.000001. RE is the chord Reynolds number.

The arithmetic is IEEE-754 double precision with only +, -, *, /, sqrt and our own logarithm, exponential and
arctangent (written below from those operations), so the result is the same on every machine running CPython 3.

SUBMISSION, a text file ('#' starts a comment):
    alpha A                 the angle of attack in degrees
    naca DDDD | naca DDDDD  a NACA 4-digit section or a 5-digit section of the 230 type (non-reflexed camber lines
                            2L0..5L0), the 4-digit thickness form with the closed trailing edge (-0.1036 x^4)
  or
    upper a0 a1 ... aN      class-shape (CST) coefficients of the upper surface, 1 <= N <= 15:
    lower b0 b1 ... bM      y(x) = sqrt(x) (1 - x) sum_i a_i C(N, i) x^i (1 - x)^(N - i)  (B. M. Kulfan, J. Aircraft 45
                            (2008) 142-158), |a_i| <= 1, sharp trailing edge
Output: Cl, Cd, Cm, transition points and the score; the last line is 'RESULT v' (v an exact fraction); exit status
0 only for a scored submission."""
import math
import sys

PI = math.pi
TWO_PI = 2.0 * PI
HALF_PI = 0.5 * PI
LN2_HI = 6.93147180369123816490e-01          # ln 2 split as in fdlibm: k * LN2_HI is exact for |k| < 2048
LN2_LO = 1.90821492927058770002e-10
LN10 = 2.302585092994046
ATAN_K8 = (0.0, 0.12435499454676144, 0.24497866312686414, 0.35877067027057225, 0.4636476090008061,
           0.5585993153435624, 0.6435011087932844, 0.7188299996216245, 0.7853981633974483)   # atan(k/8), rounded
N_SIDE = 80
H_SEP = 2.4
X_END = 0.99
TE_MIN_DEG = 4.0
CM_MIN = -0.10
H_START = 1.4


class Refused(Exception):
    pass


def sq(x):
    return x * x


def p5(x):
    x2 = x * x
    return x2 * x2 * x


def p6(x):
    x3 = x * x * x
    return x3 * x3


# ------------------------------------------------------------------ elementary functions from + - * / sqrt only


def qv_log(x):
    if not x > 0.0:
        raise Refused(f"logarithm of {x}")
    m, e = math.frexp(x)                     # x = m 2^e, 0.5 <= m < 1 (exact)
    if m < 0.7071067811865476:
        m *= 2.0
        e -= 1
    s = (m - 1.0) / (m + 1.0)                # |s| <= 0.1716
    s2 = s * s
    acc = 0.0
    for k in range(29, 0, -2):               # 2 (s + s^3/3 + ... + s^29/29)
        acc = acc * s2 + 1.0 / k
    return e * LN2_HI + (e * LN2_LO + 2.0 * s * acc)


def qv_exp(x):
    if x > 700.0 or x < -700.0:
        raise Refused(f"exponential of {x}")
    k = math.floor(x * 1.4426950408889634 + 0.5)
    r = (x - k * LN2_HI) - k * LN2_LO         # |r| <= 0.347
    acc = 1.0
    for i in range(24, 0, -1):
        acc = 1.0 + acc * r / i
    return math.ldexp(acc, k)


def qv_pow(a, b):
    return qv_exp(b * qv_log(a))


def qv_atan01(t):
    """atan(t) for 0 <= t <= 1: atan(c) + atan((t - c)/(1 + c t)) with c = k/8 nearest, then a series."""
    k = math.floor(t * 8.0 + 0.5)
    c = k / 8.0
    u = (t - c) / (1.0 + c * t)               # |u| <= 1/16
    u2 = u * u
    acc = 0.0
    for j in range(19, 0, -2):
        acc = acc * u2 + (1.0 / j if j % 4 == 1 else -1.0 / j)
    return ATAN_K8[k] + u * acc


def qv_atan2(y, x):
    if x == 0.0 and y == 0.0:
        return 0.0
    ax, ay = abs(x), abs(y)
    if ay <= ax:
        a = qv_atan01(ay / ax)
    else:
        a = HALF_PI - qv_atan01(ax / ay)
    if x < 0.0:
        a = PI - a
    return -a if y < 0.0 else a


def qv_sincos(x):
    """sin and cos of a small angle (|x| < 0.5 rad) by their series."""
    x2 = x * x
    s, c = 1.0, 1.0
    for i in range(23, 1, -2):
        s = 1.0 - s * x2 / (i * (i - 1))
    for i in range(22, 0, -2):
        c = 1.0 - c * x2 / (i * (i - 1))
    return x * s, c


# ------------------------------------------------------------------ geometry


def parse(path):
    alpha = naca = None
    upper = lower = None
    try:
        lines = open(path).read().splitlines()
    except (OSError, UnicodeDecodeError) as e:
        raise Refused(f"cannot read the submission: {e}")
    for raw in lines:
        tok = raw.split("#", 1)[0].split()
        if not tok:
            continue
        key, vals = tok[0].lower(), tok[1:]
        try:
            if key == "alpha" and len(vals) == 1 and alpha is None:
                alpha = float(vals[0])
            elif key == "naca" and len(vals) == 1 and naca is None:
                naca = vals[0]
            elif key == "upper" and upper is None:
                upper = [float(v) for v in vals]
            elif key == "lower" and lower is None:
                lower = [float(v) for v in vals]
            else:
                raise Refused(f"unexpected line: {raw.strip()}")
        except ValueError:
            raise Refused(f"not a number in: {raw.strip()}")
    if alpha is None or not math.isfinite(alpha):
        raise Refused("no angle of attack (a line 'alpha A')")
    if not -5.0 <= alpha <= 15.0:
        raise Refused(f"angle of attack {alpha} outside [-5, 15] degrees")
    if (naca is None) == (upper is None and lower is None):
        raise Refused("give either one 'naca' line or both 'upper' and 'lower' lines")
    if naca is None:
        if upper is None or lower is None:
            raise Refused("give both 'upper' and 'lower' lines")
        for name, a in (("upper", upper), ("lower", lower)):
            if not 2 <= len(a) <= 16:
                raise Refused(f"{name}: between 2 and 16 coefficients (N from 1 to 15)")
            if not all(math.isfinite(v) and abs(v) <= 1.0 for v in a):
                raise Refused(f"{name}: coefficients must be finite with |a| <= 1")
    return alpha, naca, upper, lower


def stations():
    out = []
    for i in range(N_SIDE + 1):
        s, c = qv_sincos(PI * i / N_SIDE - HALF_PI)  # cos(pi i / N) = -sin(pi i / N - pi/2): no large angles
        out.append(0.5 * (1.0 + s))
    out[0], out[-1] = 0.0, 1.0
    return out


def binom(n, k):
    return math.comb(n, k) if hasattr(math, "comb") else math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def cst(a, x):
    n = len(a) - 1
    if x == 0.0 or x == 1.0:
        return 0.0
    acc = 0.0
    for i, ai in enumerate(a):
        b = float(binom(n, i))
        for _ in range(i):
            b *= x
        for _ in range(n - i):
            b *= 1.0 - x
        acc += ai * b
    return math.sqrt(x) * (1.0 - x) * acc


FIVE = {1: (0.0580, 361.4), 2: (0.1260, 51.640), 3: (0.2025, 15.957), 4: (0.2900, 6.643), 5: (0.3910, 3.230)}


def naca_surfaces(code, xs):
    if not code.isdigit() or len(code) not in (4, 5):
        raise Refused(f"NACA designation {code}: 4 or 5 digits")
    t = int(code[-2:]) / 100.0
    if not 0.01 <= t <= 0.40:
        raise Refused(f"NACA {code}: thickness {t} outside [0.01, 0.40]")
    if len(code) == 4:
        m, p = int(code[0]) / 100.0, int(code[1]) / 10.0
        if m > 0.0 and p == 0.0:
            raise Refused(f"NACA {code}: camber without a camber position")

        def camber(x):
            if m == 0.0:
                return 0.0, 0.0
            if x < p:
                return m / (p * p) * (2.0 * p * x - x * x), 2.0 * m / (p * p) * (p - x)
            q = 1.0 - p
            return m / (q * q) * ((1.0 - 2.0 * p) + 2.0 * p * x - x * x), 2.0 * m / (q * q) * (p - x)
    else:
        L, P, Q = int(code[0]), int(code[1]), int(code[2])
        if Q != 0 or P not in FIVE or L == 0:
            raise Refused(f"NACA {code}: 5-digit sections of the form L P 0 XX with P from 1 to 5 and L >= 1")
        r, k1 = FIVE[P]
        k1 = k1 * L / 2.0                       # the tabulated k1 is for the design lift 0.3 (L = 2)

        def camber(x):
            if x < r:
                return k1 / 6.0 * (x * x * x - 3.0 * r * x * x + r * r * (3.0 - r) * x), \
                    k1 / 6.0 * (3.0 * x * x - 6.0 * r * x + r * r * (3.0 - r))
            return k1 * r * r * r / 6.0 * (1.0 - x), -k1 * r * r * r / 6.0
    up, lo = [], []
    for x in xs:
        yt = 5.0 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x * x + 0.2843 * x * x * x
                        - 0.1036 * x * x * x * x)
        if x == 1.0:
            yt = 0.0
        yc, dy = camber(x)
        h = math.sqrt(1.0 + dy * dy)
        s, c = dy / h, 1.0 / h
        up.append((x - yt * s, yc + yt * c))
        lo.append((x + yt * s, yc - yt * c))
    return up, lo


def geometry(naca, upper, lower):
    xs = stations()
    if naca is not None:
        up, lo = naca_surfaces(naca, xs)
    else:
        up = [(x, cst(upper, x)) for x in xs]
        lo = [(x, cst(lower, x)) for x in xs]
    nodes = list(reversed(lo)) + up[1:]          # clockwise: lower trailing edge -> leading edge -> upper -> TE
    simple_polygon(nodes)
    area2 = 0.0
    for (x0, y0), (x1, y1) in zip(nodes, nodes[1:]):
        area2 += x0 * y1 - x1 * y0
    if not area2 < 0.0:
        raise Refused("the upper surface must lie above the lower one (the outline must run clockwise)")
    (x0, y0), (x1, y1), (xn, yn) = nodes[0], nodes[1], nodes[-2]
    ux, uy, vx, vy = x1 - x0, y1 - y0, xn - x0, yn - y0
    wedge = qv_atan2(uy * vx - ux * vy, ux * vx + uy * vy)      # from the lower TE panel to the upper one
    if not wedge >= TE_MIN_DEG * PI / 180.0:
        raise Refused(f"trailing-edge wedge angle {wedge * 180.0 / PI:.3f} degrees is below {TE_MIN_DEG} (the Kutta "
                      f"condition of the panel method is not reliable at a cusp)")
    return nodes, vertical_thickness(nodes), up, lo


def orient(a, b, c):
    """The sign of the cross product (b - a) x (c - a), computed exactly (floats are exact fractions)."""
    from fractions import Fraction as Fr
    ax, ay, bx, by, cx, cy = (Fr(v) for v in (a[0], a[1], b[0], b[1], c[0], c[1]))
    v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    return (v > 0) - (v < 0)


def segments_meet(p, q, r, s):
    if (max(p[0], q[0]) < min(r[0], s[0]) or max(r[0], s[0]) < min(p[0], q[0]) or
            max(p[1], q[1]) < min(r[1], s[1]) or max(r[1], s[1]) < min(p[1], q[1])):
        return False
    d1, d2, d3, d4 = orient(p, q, r), orient(p, q, s), orient(r, s, p), orient(r, s, q)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return 0 in (d1, d2, d3, d4)          # touching or collinear overlap within the boxes: refused as not simple


def simple_polygon(nodes):
    """Refuses a polygon (nodes[0] = nodes[-1]) with repeated nodes or two non-adjacent edges that meet."""
    if nodes[0] != nodes[-1]:
        raise Refused("the outline is not closed")
    n = len(nodes) - 1
    if len(set(nodes[:-1])) != n:
        raise Refused("repeated points in the outline")
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            if segments_meet(nodes[i], nodes[i + 1], nodes[j], nodes[j + 1]):
                raise Refused(f"the outline crosses itself (edges {i} and {j})")


def vertical_thickness(nodes):
    """The longest vertical chord inside the polygon, over the x of its nodes (it is piecewise linear in x)."""
    xs = sorted(set(x for x, _ in nodes))
    best = 0.0
    for x in xs[1:-1]:
        ys = []
        for (x0, y0), (x1, y1) in zip(nodes, nodes[1:]):
            if x0 != x1 and min(x0, x1) <= x < max(x0, x1):
                ys.append(y0 + (y1 - y0) * (x - x0) / (x1 - x0))
        ys.sort()
        chord = 0.0
        for k in range(0, len(ys) - 1, 2):
            chord += ys[k + 1] - ys[k]
        best = max(best, chord)
    return best


# ------------------------------------------------------------------ Hess-Smith panel method


def solve(A, rhs_list):
    """Gaussian elimination with partial pivoting (ties: the first row), several right-hand sides."""
    n = len(A)
    M = [row[:] + [r[i] for r in rhs_list] for i, row in enumerate(A)]
    k = len(rhs_list)
    for c in range(n):
        piv = c
        for r in range(c + 1, n):
            if abs(M[r][c]) > abs(M[piv][c]):
                piv = r
        if M[piv][c] == 0.0:
            raise Refused("singular panel system")
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
        rowc = M[c]
        inv = 1.0 / rowc[c]
        for r in range(c + 1, n):
            row = M[r]
            f = row[c] * inv
            if f != 0.0:
                for j in range(c, n + k):
                    row[j] -= f * rowc[j]
    out = []
    for s in range(k):
        x = [0.0] * n
        for r in range(n - 1, -1, -1):
            row = M[r]
            acc = row[n + s]
            for j in range(r + 1, n):
                acc -= row[j] * x[j]
            x[r] = acc / row[r]
        out.append(x)
    return out


def panel_solution(nodes):
    """Influence coefficients and the two basic solutions (alpha = 0 and 90 degrees) of the Hess-Smith system."""
    N = len(nodes) - 1
    X = [p[0] for p in nodes]
    Y = [p[1] for p in nodes]
    xm = [0.5 * (X[j] + X[j + 1]) for j in range(N)]
    ym = [0.5 * (Y[j] + Y[j + 1]) for j in range(N)]
    ln_ = [math.sqrt(sq(X[j + 1] - X[j]) + sq(Y[j + 1] - Y[j])) for j in range(N)]
    if min(ln_) <= 0.0:
        raise Refused("a panel of zero length")
    sn = [(Y[j + 1] - Y[j]) / ln_[j] for j in range(N)]
    cs = [(X[j + 1] - X[j]) / ln_[j] for j in range(N)]
    inv2pi = 1.0 / TWO_PI
    An = [[0.0] * (N + 1) for _ in range(N)]            # normal velocity: N sources + the vortex
    At = [[0.0] * (N + 1) for _ in range(N)]            # tangential velocity
    for i in range(N):
        xi, yi, si, ci = xm[i], ym[i], sn[i], cs[i]
        rowN, rowT = An[i], At[i]
        bn = bt = 0.0
        for j in range(N):
            if i == j:
                lnr, beta = 0.0, PI
            else:
                dx0, dy0 = xi - X[j], yi - Y[j]
                dx1, dy1 = xi - X[j + 1], yi - Y[j + 1]
                lnr = 0.5 * qv_log((dx1 * dx1 + dy1 * dy1) / (dx0 * dx0 + dy0 * dy0))
                beta = qv_atan2(dy1 * dx0 - dx1 * dy0, dx1 * dx0 + dy1 * dy0)
            sij = si * cs[j] - ci * sn[j]               # sin(theta_i - theta_j)
            cij = ci * cs[j] + si * sn[j]               # cos(theta_i - theta_j)
            rowN[j] = inv2pi * (sij * lnr + cij * beta)
            rowT[j] = inv2pi * (sij * beta - cij * lnr)
            bn += inv2pi * (cij * lnr - sij * beta)
            bt += inv2pi * (sij * lnr + cij * beta)
        rowN[N], rowT[N] = bn, bt
    # equations: normal velocity zero at each control point; Kutta: Vt(first) + Vt(last) = 0
    A = [An[i][:] for i in range(N)] + [[At[0][j] + At[N - 1][j] for j in range(N + 1)]]
    rhs0 = [sn[i] for i in range(N)] + [-(cs[0] + cs[N - 1])]          # alpha = 0: -sin(0 - th) = sin th
    rhs90 = [-cs[i] for i in range(N)] + [-(sn[0] + sn[N - 1])]        # alpha = 90: -sin(90 - th) = -cos th
    sol0, sol90 = solve(A, [rhs0, rhs90])
    return {"N": N, "At": At, "sol0": sol0, "sol90": sol90, "xm": xm, "ym": ym, "len": ln_, "sn": sn, "cs": cs}


def panel_flow(ps, alpha_deg):
    """Surface speeds, lift and moment at one angle of attack, by superposition of the two basic solutions."""
    N, At, sol0, sol90 = ps["N"], ps["At"], ps["sol0"], ps["sol90"]
    xm, ym, ln_, sn, cs = ps["xm"], ps["ym"], ps["len"], ps["sn"], ps["cs"]
    sa, ca = qv_sincos(alpha_deg * PI / 180.0)
    sol = [ca * a + sa * b for a, b in zip(sol0, sol90)]
    vt = []
    for i in range(N):
        acc = ca * cs[i] + sa * sn[i]                    # cos(alpha - theta_i)
        row = At[i]
        for j in range(N + 1):
            acc += row[j] * sol[j]
        vt.append(acc)
    # forces from the pressures: Cp = 1 - vt^2 on each panel, normal (-sin, cos) points out (clockwise order)
    fx = fy = mz = 0.0
    for i in range(N):
        cp = 1.0 - vt[i] * vt[i]
        nx, ny = -sn[i], cs[i]
        dfx, dfy = -cp * ln_[i] * nx, -cp * ln_[i] * ny
        fx += dfx
        fy += dfy
        mz += (xm[i] - 0.25) * dfy - ym[i] * dfx       # moment about (0.25, 0), nose up positive below
    cl = fy * ca - fx * sa
    cd_p = fx * ca + fy * sa
    cm = -mz
    return {"vt": vt, "xm": xm, "ym": ym, "len": ln_, "cl": cl, "cd_pressure": cd_p, "cm": cm, "gamma": sol[N]}


# ------------------------------------------------------------------ boundary layer


def thwaites_HL(lam):
    if lam > 0.1:
        lam = 0.1
    if lam >= 0.0:
        return 2.61 - 3.75 * lam + 5.24 * lam * lam, 0.22 + 1.57 * lam - 1.8 * lam * lam
    if lam < -0.1:
        lam = -0.1
    return 2.088 + 0.0731 / (lam + 0.14), 0.22 + 1.402 * lam + 0.018 * lam / (lam + 0.107)


def h1_of_h(H):
    if H <= 1.6:
        return 3.3 + 0.8234 * qv_pow(H - 1.1, -1.287)
    return 3.3 + 1.5501 * qv_pow(H - 0.6778, -3.064)


def h_of_h1(H1):
    if H1 <= 3.3001:
        return 99.0
    if H1 >= 5.3:
        return 1.1 + qv_pow((H1 - 3.3) / 0.8234, -1.0 / 1.287)
    return 0.6778 + qv_pow((H1 - 3.3) / 1.5501, -1.0 / 3.064)


def surface_layer(s, ue, re):
    """One surface from the stagnation point: s (arc length, s[0] > 0) and edge speed ue at the stations.
    Returns theta and H at the last station, the transition station and the laminar or turbulent state."""
    n = len(s)
    due = []
    for k in range(n):
        if k == 0:
            due.append(ue[0] / s[0])                     # from the stagnation point (ue = 0 at s = 0)
        elif k == n - 1:
            due.append((ue[k] - ue[k - 1]) / (s[k] - s[k - 1]))
        else:
            due.append((ue[k + 1] - ue[k - 1]) / (s[k + 1] - s[k - 1]))
    # Thwaites: theta^2 = 0.45 / (re ue^6) * integral of ue^5 ds, ue linear between stations
    integ = s[0] * p5(ue[0]) / 6.0
    k_tr, theta, H = None, 0.0, 0.0
    for k in range(n):
        if k > 0:
            a, b, ds = ue[k - 1], ue[k], s[k] - s[k - 1]
            if b != a:
                integ += ds * (p6(b) - p6(a)) / (6.0 * (b - a))
            else:
                integ += ds * p5(a)
        theta = math.sqrt(0.45 * integ / (re * p6(ue[k])))
        lam = theta * theta * due[k] * re
        H, _ = thwaites_HL(lam)
        re_theta = re * ue[k] * theta
        re_s = re * ue[k] * s[k]
        michel = 1.174 * (1.0 + 22400.0 / re_s) * qv_pow(re_s, 0.46)
        if lam < -0.09 or re_theta >= michel:
            k_tr = k
            break
    if k_tr is None:
        return theta, H, None, "laminar"
    # Head's method from the transition station
    H = H_START
    Y = ue[k_tr] * theta * h1_of_h(H)

    def deriv(k, th, Yv):
        H1 = Yv / (ue[k] * th)
        Hk = h_of_h1(H1)
        if Hk >= H_SEP:
            raise Refused(f"turbulent separation (H = {Hk:.3f}) at s = {s[k]:.4f}")
        rt = re * ue[k] * th
        if rt <= 0.0:
            raise Refused("non-positive momentum-thickness Reynolds number")
        cf = 0.246 * qv_exp(-0.678 * Hk * LN10) * qv_pow(rt, -0.268)
        dth = 0.5 * cf - (Hk + 2.0) * th / ue[k] * due[k]
        if H1 <= 3.0:
            raise Refused("entrainment shape factor out of range (separated)")
        dY = ue[k] * 0.0306 * qv_pow(H1 - 3.0, -0.6169)
        return dth, dY, Hk

    for k in range(k_tr, n - 1):
        ds = s[k + 1] - s[k]
        d1, e1, _ = deriv(k, theta, Y)
        th_p, Y_p = theta + ds * d1, Y + ds * e1
        if th_p <= 0.0 or Y_p <= 0.0:
            raise Refused("boundary layer integration failed (non-positive thickness)")
        d2, e2, _ = deriv(k + 1, th_p, Y_p)
        theta, Y = theta + 0.5 * ds * (d1 + d2), Y + 0.5 * ds * (e1 + e2)
        if theta <= 0.0 or Y <= 0.0:
            raise Refused("boundary layer integration failed (non-positive thickness)")
    _, _, H = deriv(n - 1, theta, Y)
    return theta, H, k_tr, "turbulent"


def viscous(flow, re):
    vt, xm, ym = flow["vt"], flow["xm"], flow["ym"]
    N = len(vt)
    ks = None
    for i in range(N - 1):
        if vt[i] < 0.0 <= vt[i + 1]:
            if ks is not None:
                raise Refused("more than one stagnation point")
            ks = i
    if ks is None:
        raise Refused("no stagnation point")
    # stagnation point by linear interpolation between control points ks and ks + 1
    f = -vt[ks] / (vt[ks + 1] - vt[ks])
    sx = xm[ks] + f * (xm[ks + 1] - xm[ks])
    sy = ym[ks] + f * (ym[ks + 1] - ym[ks])
    out = {}
    for name, idx in (("upper", list(range(ks + 1, N))), ("lower", list(range(ks, -1, -1)))):
        cut = [k for k, i in enumerate(idx) if xm[i] > X_END]
        if cut:
            idx = idx[:cut[0]]                       # stop before the trailing-edge stagnation of potential flow
        s, ue = [], []
        px, py, acc = sx, sy, 0.0
        for i in idx:
            acc += math.sqrt(sq(xm[i] - px) + sq(ym[i] - py))
            px, py = xm[i], ym[i]
            s.append(acc)
            ue.append(abs(vt[i]))
        if len(s) < 3 or min(ue) <= 0.0:
            raise Refused(f"{name} surface: too short or a second stagnation point")
        theta, H, k_tr, state = surface_layer(s, ue, re)
        cd = 2.0 * theta * qv_pow(ue[-1], 0.5 * (H + 5.0))
        x_tr = xm[idx[k_tr]] if k_tr is not None else None
        out[name] = {"theta": theta, "H": H, "x_tr": x_tr, "state": state, "cd": cd}
    out["cd"] = out["upper"]["cd"] + out["lower"]["cd"]
    return out


def evaluate(path, re):
    alpha, naca, upper, lower = parse(path)
    nodes, th, _, _ = geometry(naca, upper, lower)
    flow = panel_flow(panel_solution(nodes), alpha)
    visc = viscous(flow, re)
    return alpha, th, flow, visc


def exact_text(fr):
    return f"{fr.numerator}" if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"


def main():
    from fractions import Fraction
    if len(sys.argv) != 6:
        print(__doc__)
        return 2
    mode, re_s, tmin_s, clmin_s, path = sys.argv[1:]
    try:
        re, tmin, clmin = float(int(re_s)), float(tmin_s), float(clmin_s)
        if mode not in ("ld", "cd") or not 1e4 <= re <= 1e9:
            raise ValueError
        alpha, th, flow, visc = evaluate(path, re)
        if th < tmin:
            raise Refused(f"largest thickness {th:.6f} is below {tmin}")
        cl, cd, cm = flow["cl"], visc["cd"], flow["cm"]
        if not (cd > 0.0 and math.isfinite(cd) and math.isfinite(cl)):
            raise Refused("drag not positive")
        if cm < CM_MIN:
            raise Refused(f"pitching moment Cm(c/4) {cm:.6f} is below {CM_MIN} (nose-down limit)")
        print(f"QV-Foil 1 (a numerical model, not a wind tunnel): Re {int(re)}, alpha {alpha} deg, "
              f"largest thickness {th:.6f}")
        print(f"Cl {cl:.6f}  Cd {cd:.7f}  Cm(c/4) {cm:.6f}  L/D {cl / cd:.4f}")
        for side in ("upper", "lower"):
            v = visc[side]
            print(f"{side}: {v['state']} at the trailing edge, transition at x = "
                  f"{'none' if v['x_tr'] is None else format(v['x_tr'], '.4f')}, theta {v['theta']:.7f}, H {v['H']:.4f}")
        if mode == "ld":
            if cl <= 0.0:
                raise Refused("lift is not positive")
            score = Fraction(math.floor(Fraction(cl) / Fraction(cd) * 100), 100)
            print(f"score: L/D rounded down to 0.01 = {float(score):.2f}")
        else:
            if cl < clmin:
                raise Refused(f"Cl {cl:.6f} is below the required {clmin}")
            score = Fraction(math.ceil(Fraction(cd) * 1000000), 1000000)
            print(f"score: Cd rounded up to 0.000001 = {float(score):.6f}")
        print(f"RESULT {exact_text(score)}")
        return 0
    except Refused as e:
        print(f"NOT SCORED: {e}")
        return 1
    except ValueError:
        print("usage: airfoil_check.py ld|cd RE TMIN CLMIN SUBMISSION (RE an integer from 10^4 to 10^9)")
        return 2


if __name__ == "__main__":
    sys.exit(main())
