#!/usr/bin/env python3
"""Tests of the Quantavane Open Tables (standard library only; run from anywhere):

  python3 -I collections/open-tables/tests/test_open_tables.py

Unknotting table: every certificate replayed with its value; red controls (each broken certificate refused); the
Alexander polynomial of every cell's braid word (our reduced Burau computation) equal to KnotInfo's; random braid
moves keep the Alexander and Jones polynomials; the cells agree with the pinned KnotInfo file when it is present.
Airfoil tables: our logarithm, exponential and arctangent against the C library; the panel method against the exact
potential flow of Karman-Trefftz airfoils; Thwaites' method on a flat plate; the checker gives the same output twice;
red controls; every baseline and entry certificate replayed with its value, and a perturbed entry not reproducing it.
Topology optimisation (QV-Topo 1): the element matrix against Gauss integration; a plate in tension, a uniform cell
and two laminates against their exact values; translation and rotation of a cell; the Hashin-Shtrikman bound; the same
output twice; red controls (checkerboards, a broken load path, point contacts, too much material, a malformed or
mis-sized design, passive elements, a cell that does not wrap, a mechanism below the stiffness floor, corrupted
certificates); every certificate replayed with its value; our replay of the 88-line loop against the published values.
Pages, index and README in sync with the problem files and cells (tools/build.py --check)."""
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, "tools"))
sys.path.insert(0, os.path.join(HERE, "checkers"))
import braids  # noqa: E402
import airfoil_check as A  # noqa: E402
import topopt_check as T  # noqa: E402

UNKNOT = os.path.join(HERE, "checkers", "unknot_check.py")
TOPO = os.path.join(HERE, "checkers", "topopt_check.py")
FOIL = os.path.join(HERE, "checkers", "airfoil_check.py")
TMP = tempfile.mkdtemp(prefix="open-tables-")
failures = 0


def expect(label, ok, detail=""):
    global failures
    print(("ok    " if ok else "FAIL  ") + label + ("" if ok else f": {detail}"))
    failures += 0 if ok else 1


def run(checker, args, text=None, path=None):
    if text is not None:
        path = os.path.join(TMP, f"s{random.randrange(10 ** 9)}.txt")
        with open(path, "w") as f:
            f.write(text)
    r = subprocess.run([sys.executable, "-I", checker] + list(args) + [path], capture_output=True, text=True)
    m = re.findall(r"^RESULT (\S+)$", r.stdout, re.M)
    return r.returncode, (m[-1] if m else None), r.stdout


def cells(name):
    return [json.loads(l) for l in open(os.path.join(HERE, "cells", name + ".jsonl")) if l.strip()]


# ------------------------------------------------------------------------------------------- unknotting


def unknotting():
    cs = cells("unknotting")
    expect("unknotting: 67 open cells, each with an interval of length 1", len(cs) == 67 and
           all(int(c["best"]) - int(c["bound"]) == 1 for c in cs), str(len(cs)))
    # unit cases
    code, val, out = run(UNKNOT, ["1,1,1"], "X 1\nD 0\nU\n")
    expect("unit: the trefoil 1,1,1 unknots with one change", code == 0 and val == "1", out)
    code, val, out = run(UNKNOT, ["1"], "U\n")
    expect("unit: the closed braid sigma_1 on 2 strands is the unknot (0 changes)", code == 0 and val == "0", out)
    # every certificate replays with its value
    for c in cs:
        if not c.get("certificate"):
            continue
        code, val, out = run(UNKNOT, [c["params"]["braid"]], path=os.path.join(ROOT, c["certificate"]))
        expect(f"{c['id']}: certificate replays with {c['certificate_value']} crossing changes",
               code == 0 and val == c["certificate_value"], out[-300:])
    with_cert = [c for c in cs if c.get("certificate")]
    expect("unknotting: certificates for at least 60 cells", len(with_cert) >= 60, str(len(with_cert)))
    # red controls on a real certificate
    c0 = next(c for c in with_cert if c["params"]["knot"] == "10_6")
    lines = open(os.path.join(ROOT, c0["certificate"])).read().splitlines()
    braid = c0["params"]["braid"]

    def refuse(label, text, b=braid):
        code, val, out = run(UNKNOT, [b], text)
        expect("red control refused: " + label, code != 0 and val is None, out[-200:])
    refuse("a crossing change removed", "\n".join(l for i, l in enumerate(lines) if not (
        l.startswith("X") and i == next(j for j, m in enumerate(lines) if m.startswith("X")))) + "\n")
    other = next(c for c in cs if c["params"]["knot"] == "10_11")["params"]["braid"]
    refuse("10_6's certificate on 10_11's braid", "\n".join(lines) + "\n", other)
    refuse("an empty certificate (the knot is not the unknot)", "")
    refuse("commuting adjacent generators", "C 6\n")                 # 2,-1 at positions 6, 7
    refuse("a braid relation with mixed signs", "B 6\n")             # 2,-1,-3
    refuse("destabilizing while the top generator appears twice", "U\n")
    refuse("a generator beyond the strands", "I 0 4\n")
    refuse("a position out of range", "X 99\n")
    refuse("an unknown move", "Z 1\n")
    refuse("deleting a pair that does not cancel", "D 0\n")
    code, val, out = run(UNKNOT, ["1,1"], "U\n")
    expect("red control refused: a braid whose closure is a two-component link", code != 0, out)
    # the braid words are KnotInfo's knots: Alexander polynomials agree
    bad = []
    for c in cs:
        w = [int(x) for x in c["params"]["braid"].split(",")]
        n = max(abs(x) for x in w) + 1
        vec = json.loads(c["alexander_vector"])
        ki = vec[2:]
        ours = braids.alexander(w, n)
        if ours != ki and ours != [-x for x in ki]:
            bad.append(c["params"]["knot"])
    expect("unknotting: the Alexander polynomial of every braid word (reduced Burau) equals KnotInfo's", not bad,
           ",".join(bad))
    # our Jones polynomial against KnotInfo's for the first knots (t + t^3 - t^4; t^-2 - t^-1 + 1 - t + t^2; ...)
    expect("unknotting: Jones polynomials of 3_1, 4_1 and 5_1 from their braid words equal KnotInfo's",
           braids.jones([1, 1, 1], 2) == {1: 1, 3: 1, 4: -1} and
           braids.jones([1, -2, 1, -2], 3) == {-2: 1, -1: -1, 0: 1, 1: -1, 2: 1} and
           braids.jones([1] * 5, 2) == {2: 1, 4: 1, 5: -1, 6: 1, 7: -1})
    # random moves keep the knot: Alexander and Jones polynomials unchanged
    rng = random.Random(7)
    ok = True
    for c in cs[:12]:
        w = [int(x) for x in c["params"]["braid"].split(",")]
        n = max(abs(x) for x in w) + 1
        a0, j0 = braids.alexander(w, n), braids.jones(w, n)
        br = braids.Braid(w, n)
        for _ in range(30):
            (br.random_grow if rng.random() < 0.2 else br.random_neutral)(rng)
        if braids.alexander(br.w, br.n) != a0 or braids.jones(br.w, br.n) != j0:
            ok = False
        # and the moves replay in the checker up to that word: append the inverse? check the log is accepted
    expect("unknotting: 30 random braid moves keep the Alexander and Jones polynomials (12 knots)", ok)
    # the move log of a random walk followed by a simplification of a known unknot replays in the checker
    br = braids.Braid([1, 1, 1], 2)
    br.X(1)
    for _ in range(25):
        (br.random_grow if rng.random() < 0.3 else br.random_neutral)(rng)
    done = braids.simplify(br, rng)
    code, val, out = run(UNKNOT, ["1,1,1"], "\n".join(br.log) + "\n")
    expect("unknotting: a random walk on the changed trefoil, simplified, replays with 1 change", done and code == 0
           and val == "1", out[-200:])
    # the cells against the pinned KnotInfo file, when fetch.sh has fetched it
    ki = os.path.join(ROOT, "instances", "knotinfo", "knotinfo_data_complete.csv")
    if os.path.exists(ki):
        r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "tools", "knotinfo_cells.py"), "--check", ki],
                           capture_output=True, text=True)
        expect("unknotting: cells agree with the pinned KnotInfo file", r.returncode == 0, r.stdout + r.stderr)
    else:
        print("skip  unknotting: cells against the KnotInfo file (run fetch.sh to fetch it)")


# ------------------------------------------------------------------------------------------- airfoils


def kt_airfoil(eps, delta, tau_deg, n_side):
    """A Karman-Trefftz airfoil (exact potential flow known) as clockwise nodes, chord 1 along x; with R, c, beta and
    the rotation of the chord."""
    import cmath
    n = 2 - tau_deg / 180.0
    mu = complex(-eps, delta)
    R = abs(1 - mu)
    beta = math.asin(delta / R)
    pts = []
    for k in range(2 * n_side + 1):
        zeta = mu + R * cmath.exp(1j * (-beta + 2 * math.pi * k / (2 * n_side)))
        if k in (0, 2 * n_side):
            z = complex(n, 0)
        else:
            a, b = (zeta + 1) ** n, (zeta - 1) ** n
            z = n * (a + b) / (a - b)
        pts.append((z.real, z.imag))
    te = pts[0]
    le = max(pts, key=lambda p: (p[0] - te[0]) ** 2 + (p[1] - te[1]) ** 2)
    c = math.hypot(te[0] - le[0], te[1] - le[1])
    ang = math.atan2(te[1] - le[1], te[0] - le[0])
    out = []
    for x, y in pts:
        dx, dy = x - le[0], y - le[1]
        out.append(((dx * math.cos(ang) + dy * math.sin(ang)) / c, (-dx * math.sin(ang) + dy * math.cos(ang)) / c))
    out = list(reversed(out))
    out[0] = out[-1] = (1.0, 0.0)
    return out, R, c, beta, ang


def airfoils():
    rng = random.Random(3)
    worst = 0.0
    for _ in range(3000):
        x = math.exp(rng.uniform(-30, 30))
        worst = max(worst, abs(A.qv_log(x) - math.log(x)) / max(1.0, abs(math.log(x))))
        y = rng.uniform(-60, 60)
        worst = max(worst, abs(A.qv_exp(y) - math.exp(y)) / math.exp(y))
        u, v = rng.uniform(-5, 5), rng.uniform(-5, 5)
        worst = max(worst, abs(A.qv_atan2(u, v) - math.atan2(u, v)))
        t = rng.uniform(-1.6, 1.6)
        s, c = A.qv_sincos(t)
        worst = max(worst, abs(s - math.sin(t)), abs(c - math.cos(t)))
    expect("airfoil: our log, exp, atan2, sin and cos agree with the C library to 1e-15", worst < 1e-15, str(worst))
    # the panel method against exact potential flow (Karman-Trefftz airfoils, finite trailing-edge angle)
    for eps, delta, tau in ((0.1, 0.0, 10.0), (0.08, 0.05, 15.0)):
        errs = []
        for ns in (80, 160):
            nodes, R, c, beta, ang = kt_airfoil(eps, delta, tau, ns)
            f = A.panel_flow(A.panel_solution(nodes), 4.0)
            exact = 8 * math.pi * R * math.sin(math.radians(4.0) + ang + beta) / c
            errs.append(abs(f["cl"] - exact) / exact)
        expect(f"airfoil: Hess-Smith lift of a Karman-Trefftz airfoil (eps {eps}, delta {delta}, tau {tau}) within 2% "
               f"at 160 panels and closer at 320", errs[0] < 0.02 and errs[1] < errs[0], str(errs))
    # NACA 0012 at zero lift: the largest surface speed at the model's 160 panels against 640 panels (convergence)
    nodes, th, _, _ = A.geometry("0012", None, None)
    vmax = max(abs(v) for v in A.panel_flow(A.panel_solution(nodes), 0.0)["vt"])
    saved = A.N_SIDE
    A.N_SIDE = 320
    try:
        nodes4, _, _, _ = A.geometry("0012", None, None)
        vmax4 = max(abs(v) for v in A.panel_flow(A.panel_solution(nodes4), 0.0)["vt"])
    finally:
        A.N_SIDE = saved
    expect("airfoil: NACA 0012 at zero lift, largest surface speed at 160 panels within 0.2% of 640 panels, about 1.19",
           abs(vmax - vmax4) < 0.002 * vmax4 and 1.18 < vmax < 1.20, f"{vmax} {vmax4}")
    # Thwaites on a flat plate: theta^2 = 0.45 s / Re while laminar (Blasius: theta = 0.664 sqrt(s/Re)); the speed
    # rises linearly from the stagnation point to the first station, which counts s[0] / 6 instead of s[0]
    s = [0.001 * (k + 1) for k in range(200)]
    th, H, ktr, state = A.surface_layer(s[:20], [1.0] * 20, 1e6)
    want = math.sqrt(0.45 * (s[19] - s[0] + s[0] / 6.0) / 1e6)
    expect("airfoil: Thwaites on a flat plate gives theta^2 = 0.45 s / Re and H = 2.61",
           state == "laminar" and abs(th - want) < 1e-15 and abs(H - 2.61) < 1e-12, f"{th} {want} {H} {state}")
    s = [0.005 * (k + 1) for k in range(400)]
    th, H, ktr, state = A.surface_layer(s, [1.0] * 400, 1e6)
    first = next(k for k in range(400) if 1e6 * math.sqrt(0.45 * (s[k] - s[0] + s[0] / 6.0) / 1e6) >=
                 1.174 * (1 + 22400 / (1e6 * s[k])) * (1e6 * s[k]) ** 0.46)
    expect("airfoil: on a flat plate transition starts at the first station past Michel's criterion (Re_x 1.705e6 "
           "here)", state == "turbulent" and ktr == first, f"{ktr} {first} {state}")
    # the same output twice
    sub = "alpha 3.5\nnaca 2412\n"
    a1, a2 = run(FOIL, ["ld", "3000000", "0.10", "0"], sub), run(FOIL, ["ld", "3000000", "0.10", "0"], sub)
    expect("airfoil: the checker prints the same output twice", a1[2] == a2[2] and a1[0] == 0, a1[2][-200:])
    # red controls
    def refuse(label, args, text):
        code, val, out = run(FOIL, args, text)
        expect("red control refused: " + label, code != 0 and val is None, out[-200:])
    ld12 = ["ld", "3000000", "0.12", "0"]
    refuse("upper surface below the lower one", ld12, "alpha 2\nupper -0.1 -0.1 -0.1\nlower 0.1 0.1 0.1\n")
    refuse("surfaces that cross", ld12, "alpha 2\nupper 0.2 -0.2 0.2\nlower -0.2 0.2 -0.2\n")
    refuse("thickness below the cell's minimum", ld12, "alpha 2\nnaca 2410\n")
    refuse("angle of attack outside [-5, 15]", ld12, "alpha 16\nnaca 0012\n")
    refuse("a cusped trailing edge (wedge below 4 degrees)", ld12,
           "alpha 2\nupper 0.17 0.15 0.12 0.02\nlower -0.17 -0.12 -0.08 0.02\n")
    refuse("turbulent separation", ["ld", "1000000", "0.12", "0"], "alpha 12\nnaca 0012\n")
    refuse("lift below the cell's requirement", ["cd", "3000000", "0.12", "0.5"], "alpha 1\nnaca 0012\n")
    refuse("a coefficient above 1", ld12, "alpha 2\nupper 1.5 0.2 0.2\nlower -0.2 -0.2 -0.2\n")
    refuse("a malformed number", ld12, "alpha two\nnaca 0012\n")
    refuse("a NACA designation that is not a section", ld12, "alpha 2\nnaca 2N12\n")
    refuse("no angle of attack", ld12, "naca 0012\n")
    # every certificate of the airfoil cells replays with its value; a perturbed entry does not reproduce it
    grid = [json.loads(l) for l in open(os.path.join(HERE, "refs", "cells", "airfoil-grid.jsonl")) if l.strip()]
    for fam in ("airfoil-ld", "airfoil-cd"):
        cs = cells(fam)
        have = {c["id"] for c in cs}
        missing = [g["id"] for g in grid if g["family"] == fam and g["id"] not in have and g["baseline"]]
        expect(f"{fam}: {len(cs)} cells, every grid cell with a NACA baseline among them", not missing and
               len(cs) >= (20 if fam == "airfoil-ld" else 17), ",".join(missing))
        for c in cs:
            if c["baseline"]:
                code, val, out = run(FOIL, c["checker_args"], path=os.path.join(ROOT, c["baseline"]["certificate"]))
                expect(f"{c['id']}: baseline NACA {c['baseline']['naca']} replays with {c['baseline']['decimal']}",
                       code == 0 and val == c["baseline"]["value"], out[-200:])
            code, val, out = run(FOIL, c["checker_args"], path=os.path.join(ROOT, c["certificate"]))
            expect(f"{c['id']}: the cell's value {c['best_decimal']} replays from its certificate",
                   code == 0 and val == c["best"], out[-200:])
            if c.get("entry"):
                code, val, out = run(FOIL, c["checker_args"], path=os.path.join(ROOT, c["entry"]["certificate"]))
                expect(f"{c['id']}: entry replays with {c['entry']['decimal']}", code == 0 and
                       val == c["entry"]["value"], out[-200:])
        c = next((c for c in cs if c.get("entry")), None)
        if c:
            text = open(os.path.join(ROOT, c["entry"]["certificate"])).read()
            m = re.search(r"^upper (.*)$", text, re.M)
            bent = text.replace(m.group(0), "upper " + " ".join(repr(float(v) * 1.05) for v in m.group(1).split()), 1)
            code, val, out = run(FOIL, c["checker_args"], bent)
            expect(f"red control: {c['id']}'s entry with its upper surface 5% thicker does not reproduce its value",
                   val != c["entry"]["value"], out[-200:])


# ------------------------------------------------------------------------------------------- topology optimisation


def grid_text(rows):
    return "".join("".join("1" if v else "0" for v in row) + "\n" for row in rows)


def topopt():
    nu = T.NU
    # the element matrix against 2 x 2 Gauss integration of B^T D B (exact for this element)
    D = [[1 / (1 - nu * nu), nu / (1 - nu * nu), 0], [nu / (1 - nu * nu), 1 / (1 - nu * nu), 0], [0, 0, 1 / (2 * (1 + nu))]]
    corners = [(0, 0), (1, 0), (1, 1), (0, 1)]
    gp = [0.5 - 0.5 / math.sqrt(3), 0.5 + 0.5 / math.sqrt(3)]
    K = [[0.0] * 8 for _ in range(8)]
    for x in gp:
        for y in gp:
            B = [[0.0] * 8 for _ in range(3)]
            for a, (xa, ya) in enumerate(corners):
                nx_ = (1 if xa else -1) * (y if ya else 1 - y)
                ny_ = (1 if ya else -1) * (x if xa else 1 - x)
                B[0][2 * a], B[1][2 * a + 1], B[2][2 * a], B[2][2 * a + 1] = nx_, ny_, ny_, nx_
            for i in range(8):
                for j in range(8):
                    K[i][j] += 0.25 * sum(B[p][i] * D[p][q] * B[q][j] for p in range(3) for q in range(3))
    err = max(abs(K[i][j] - T.KE[i][j]) for i in range(8) for j in range(8))
    expect("topopt: the element stiffness matrix equals the Gauss-integrated one (to 1e-15)", err < 1e-15, str(err))
    # a plate in tension: left edge on rollers, unit load spread over the right edge; exact compliance L / (E H)
    nx, ny = 12, 5
    node = lambda ix, iy: (ny + 1) * ix + iy  # noqa: E731
    els = [(1.0, (2 * node(ix, iy + 1), 2 * node(ix, iy + 1) + 1, 2 * node(ix + 1, iy + 1), 2 * node(ix + 1, iy + 1) + 1,
                  2 * node(ix + 1, iy), 2 * node(ix + 1, iy) + 1, 2 * node(ix, iy), 2 * node(ix, iy) + 1))
           for ix in range(nx) for iy in range(ny)]
    fixed = {2 * node(0, iy) for iy in range(ny + 1)} | {2 * node(0, ny) + 1}
    f = {2 * node(nx, iy): (0.5 if iy in (0, ny) else 1.0) / ny for iy in range(ny + 1)}
    (u,) = T.solve(2 * (nx + 1) * (ny + 1), els, fixed, [f])
    c = math.fsum(v * u[d] for d, v in f.items())
    expect("topopt: a uniform plate in tension has the exact compliance 12/5 (to 1e-13)", abs(c - nx / ny) < 1e-13,
           repr(c))
    # periodic cells: a uniform cell, two laminates, translation and rotation
    n = 8
    C = T.homogenise([[1] * n for _ in range(n)], n)
    want = [[1 / (1 - nu * nu), nu / (1 - nu * nu), 0], [nu / (1 - nu * nu), 1 / (1 - nu * nu), 0], [0, 0, 1 / (2 * (1 + nu))]]
    expect("topopt: a uniform cell has the plane-stress tensor of the solid (to 1e-14)",
           max(abs(C[i][j] - want[i][j]) for i in range(3) for j in range(3)) < 1e-14, str(C))

    def q(E):
        return [[E / (1 - nu * nu), nu * E / (1 - nu * nu), 0], [nu * E / (1 - nu * nu), E / (1 - nu * nu), 0],
                [0, 0, E / (2 * (1 + nu))]]
    E1, E2, h = 1.0, 0.2, 3
    f1, f2 = h / n, 1 - h / n
    Q1, Q2 = q(E1), q(E2)
    C22 = 1 / (f1 / Q1[1][1] + f2 / Q2[1][1])
    C12 = C22 * (f1 * Q1[0][1] / Q1[1][1] + f2 * Q2[0][1] / Q2[1][1])
    C11 = f1 * (Q1[0][0] - Q1[0][1] ** 2 / Q1[1][1]) + f2 * (Q2[0][0] - Q2[0][1] ** 2 / Q2[1][1]) + C12 ** 2 / C22
    C33 = 1 / (f1 / Q1[2][2] + f2 / Q2[2][2])
    rows = T.homogenise(None, n, [[E1 if r < h else E2 for c in range(n)] for r in range(n)])
    cols = T.homogenise(None, n, [[E1 if c < h else E2 for c in range(n)] for r in range(n)])
    lam = [[C11, C12, 0], [C12, C22, 0], [0, 0, C33]]
    lamT = [[C22, C12, 0], [C12, C11, 0], [0, 0, C33]]
    e1 = max(abs(rows[i][j] - lam[i][j]) for i in range(3) for j in range(3))
    e2 = max(abs(cols[i][j] - lamT[i][j]) for i in range(3) for j in range(3))
    expect("topopt: laminates of two materials (E = 1 and 0.2, layers along x and along y) have their exact "
           "homogenised tensors (to 1e-13)", e1 < 1e-13 and e2 < 1e-13, f"{e1} {e2}")
    # every certificate replays with its value; baselines too
    fams = ("topopt-simp", "topopt-binary", "metacell-bulk", "metacell-shear", "metacell-poisson")
    allc = {fam: cells(fam) for fam in fams}
    for fam, cs in allc.items():
        expect(f"{fam}: cells present", len(cs) >= 3, str(len(cs)))
        for c in cs:
            for key in ("entry", "baseline"):
                e = c.get(key)
                if not e:
                    continue
                code, val, out = run(TOPO, c["checker_args"], path=os.path.join(ROOT, e["certificate"]))
                expect(f"{c['id']}: {key} replays with {e['decimal']}", code == 0 and val == e["value"], out[-300:])
            paper = {"topopt-simp-mbb-60x20-v0.5-r2.4": 233.71, "topopt-simp-mbb-150x50-v0.5-r6": 235.73}.get(c["id"])
            if paper:
                b = c["baseline"]
                expect(f"{c['id']}: our replay of the 88-line loop (its stopping rule, then scaled to the volume limit) "
                       f"scores {b['decimal']}, within 0.02 of the paper's printed {paper} (identical settings)",
                       abs(float(Fraction_(b["value"])) - paper) <= 0.02, b["decimal"])
    # the Hashin-Shtrikman bound holds for every bulk certificate
    worst = max(float(Fraction_(c["best"])) / float(c["bound"]) for c in allc["metacell-bulk"])
    expect("metacell-bulk: every value is below the Hashin-Shtrikman bound", worst < 1.0, str(worst))
    # translation and a quarter turn of a cell: the same tensor, C11 and C22 swapped
    c0 = allc["metacell-shear"][0]
    g = [[ch == "1" for ch in l.strip()] for l in open(os.path.join(ROOT, c0["certificate"])) if l[0] in "01"]
    N = len(g)
    Ca = T.homogenise(g, N)
    sh = [[g[(r + N // 2) % N][(c + N // 3) % N] for c in range(N)] for r in range(N)]
    rot = [[g[N - 1 - c][r] for c in range(N)] for r in range(N)]
    Cb, Cc = T.homogenise(sh, N), T.homogenise(rot, N)
    d1 = max(abs(Ca[i][j] - Cb[i][j]) for i in range(3) for j in range(3))
    d2 = max(abs(Ca[0][0] - Cc[1][1]), abs(Ca[1][1] - Cc[0][0]), abs(Ca[0][1] - Cc[0][1]), abs(Ca[2][2] - Cc[2][2]))
    expect("topopt: a translated cell has the same tensor and a turned cell swaps C11 and C22 (to 1e-12)",
           d1 < 1e-12 and d2 < 1e-12, f"{d1} {d2}")
    # the same output twice (and under another hash seed)
    for fam in ("topopt-simp", "topopt-binary", "metacell-poisson"):
        c = allc[fam][0]
        path = os.path.join(ROOT, c["certificate"])
        r1 = subprocess.run([sys.executable, "-I", TOPO] + c["checker_args"] + [path], capture_output=True, text=True)
        r2 = subprocess.run([sys.executable, "-I", TOPO] + c["checker_args"] + [path], capture_output=True, text=True,
                            env=dict(os.environ, PYTHONHASHSEED="12345"))
        expect(f"{c['id']}: the checker prints the same output twice", r1.stdout == r2.stdout and r1.returncode == 0,
               r1.stdout[-200:])

    # the same bytes under other Python versions, when they are installed (sum() of floats changed in 3.12; the
    # checker uses math.fsum, correctly rounded, so its output must not change)
    import shutil
    c = next(c for c in allc["topopt-simp"] if c["id"] == "topopt-simp-mbb-60x20-v0.5-r2.4")
    ref = subprocess.run([sys.executable, "-I", TOPO] + c["checker_args"] + [os.path.join(ROOT, c["certificate"])],
                         capture_output=True, text=True).stdout
    others = [shutil.which(f"python3.{v}") for v in range(9, 16)]
    others = [o for o in others if o and os.path.realpath(o) != os.path.realpath(sys.executable)]
    for exe in others:
        r = subprocess.run([exe, "-I", TOPO] + c["checker_args"] + [os.path.join(ROOT, c["certificate"])],
                           capture_output=True, text=True)
        ver = subprocess.run([exe, "--version"], capture_output=True, text=True).stdout.strip()
        expect(f"{c['id']}: the same output under {ver} as under this Python", r.stdout == ref, r.stdout[-200:])
    if not others:
        print("skip  topopt: no other Python version on the PATH for the cross-version check")

    def refuse(label, args, text, why=None):
        code, val, out = run(TOPO, args, text)
        ok = code == 1 and val is None and (why is None or why in out)
        expect("red control refused: " + label, ok, out[-200:])
    mbb2 = ["compliance", "mbb", "60", "20", "0.5", "binary", "2"]
    cb = [[(ix + iy) % 2 == 0 for ix in range(60)] for iy in range(20)]
    refuse("a 0/1 checkerboard", mbb2, grid_text(cb), "minimum feature size")
    refuse("a checkerboard density field (SIMP: its filtered field is a checkerboard about 1/2)",
           ["compliance", "mbb", "60", "20", "0.5", "simp", "2.4"],
           "".join(" ".join("1" if (ix + iy) % 2 == 0 else "0" for ix in range(60)) + "\n" for iy in range(20)),
           "separate pieces")
    two = [[(ix < 10 and iy < 10) or ix >= 40 for ix in range(60)] for iy in range(20)]
    refuse("a design in two pieces (the load cannot reach the bottom support)", mbb2, grid_text(two), "separate pieces")
    blocks = [[(r < 4) == (c < 4) for c in range(8)] for r in range(8)]
    refuse("two square blocks touching at a corner only (point contact)", ["cell", "bulk", "8", "0.6", "2", "0"],
           grid_text(blocks), "point contact")
    sp = next(c for c in allc["topopt-binary"] if c["checker_args"][1] == "mbb" and c["checker_args"][4] == "0.5")
    text = open(os.path.join(ROOT, sp["certificate"])).read()
    refuse("a design with more material than allowed", sp["checker_args"][:4] + ["0.3"] + sp["checker_args"][5:], text,
           "solid elements, more than")
    rows_ = [l for l in text.splitlines() if l and l[0] in "01"]
    refuse("a design with a row missing", sp["checker_args"], "\n".join(rows_[:-1]) + "\n", "expected")
    refuse("a design with a character other than 0 and 1", sp["checker_args"],
           "\n".join([rows_[0][:-1] + "2"] + rows_[1:]) + "\n", "characters 0 or 1")
    simp = next(c for c in allc["topopt-simp"] if c["id"] == "topopt-simp-mbb-60x20-v0.5-r2.4")
    stext = open(os.path.join(ROOT, simp["certificate"])).read()
    srows = [l for l in stext.splitlines() if l and l[0] in "0123456789"]
    refuse("a density above 1", simp["checker_args"], "\n".join(["1.5 " + srows[0].split(" ", 1)[1]] + srows[1:]) + "\n",
           "outside [0, 1]")
    refuse("a density that is not a number", simp["checker_args"],
           "\n".join(["nan " + srows[0].split(" ", 1)[1]] + srows[1:]) + "\n")
    more = "\n".join(" ".join(f"{min(1.0, float(v) * 1.02):.6f}" for v in r.split()) for r in srows) + "\n"
    refuse("a density field 2% denser than the certificate (volume above the limit)", simp["checker_args"], more,
           "exceeds")
    cut = "\n".join(" ".join("0" if ix < 8 and iy < 8 else v for ix, v in enumerate(r.split()))
                     for iy, r in enumerate(srows)) + "\n"
    refuse("the certificate with no material near the load", simp["checker_args"], cut)
    lb = next(c for c in allc["topopt-binary"] if c["checker_args"][1] == "lbracket")
    ltext = [l for l in open(os.path.join(ROOT, lb["certificate"])).read().splitlines() if l and l[0] in "01"]
    ltext[0] = ltext[0][:-1] + "1"
    refuse("solid material in the passive corner of the L-bracket", lb["checker_args"], "\n".join(ltext) + "\n",
           "passive")
    island = [[12 <= r < 28 and 12 <= c < 28 for c in range(40)] for r in range(40)]
    refuse("a cell whose solid does not wrap around (an island)", ["cell", "bulk", "40", "0.5", "2", "0"],
           grid_text(island), "wrap")
    xcell = [[abs(r - c) <= 1 or abs(r + c - 39) <= 1 for c in range(40)] for r in range(40)]
    refuse("a cell below the stiffness floor (diagonal bars: a mechanism along the axes)",
           ["cell", "poisson", "40", "0.2", "2", "0.01"], grid_text(xcell), "stiffness floor")
    code, val, out = run(TOPO, ["compliance", "bridge", "60", "20", "0.5", "binary", "2"], grid_text(cb))
    expect("usage error: an unknown load case exits with status 2", code == 2 and val is None, out[-100:])
    # corrupted certificates: one element flipped is refused or scores differently
    for fam in ("topopt-binary", "metacell-bulk", "metacell-poisson"):
        c = allc[fam][-1]
        lines = open(os.path.join(ROOT, c["certificate"])).read().splitlines()
        rows_ = [l for l in lines if l and l[0] in "01"]
        r = len(rows_) // 2
        flipped = rows_[r][:3] + ("0" if rows_[r][3] == "1" else "1") + rows_[r][4:]
        code, val, out = run(TOPO, c["checker_args"], "\n".join(rows_[:r] + [flipped] + rows_[r + 1:]) + "\n")
        expect(f"red control: {c['id']} with one element flipped is refused or scores differently",
               val != c["certificate_value"], out[-200:])
    # obb.py reads the cells
    for fam in fams:
        c = allc[fam][0]
        r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "obb.py"), "check", c["id"],
                            os.path.join(ROOT, c["certificate"])], capture_output=True, text=True)
        expect(f"obb.py check {c['id']} certifies its certificate", r.returncode == 0 and "certified value" in r.stdout,
               r.stdout[-300:])


def Fraction_(text):
    from fractions import Fraction
    return Fraction(text)


def main():
    unknotting()
    airfoils()
    topopt()
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "tools", "build.py"), "--check"],
                       capture_output=True, text=True)
    expect("pages, index.json and README in sync (tools/build.py --check)", r.returncode == 0, r.stdout)
    print(f"{'all tests passed' if not failures else str(failures) + ' FAILED'} (open tables)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
