#!/usr/bin/env python3
"""Tests of the Quantavane Open Tables (standard library only; run from anywhere):

  python3 -I collections/open-tables/tests/test_open_tables.py

Unknotting table: every certificate replayed with its value; red controls (each broken certificate refused); the
Alexander polynomial of every cell's braid word (our reduced Burau computation) equal to KnotInfo's; random braid
moves keep the Alexander and Jones polynomials; the cells agree with the pinned KnotInfo file when it is present.
Airfoil tables: our logarithm, exponential and arctangent against the C library; the panel method against the exact
potential flow of Karman-Trefftz airfoils; Thwaites' method on a flat plate; the checker gives the same output twice;
red controls; every baseline and entry certificate replayed with its value, and a perturbed entry not reproducing it.
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

UNKNOT = os.path.join(HERE, "checkers", "unknot_check.py")
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


def main():
    unknotting()
    airfoils()
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "tools", "build.py"), "--check"],
                       capture_output=True, text=True)
    expect("pages, index.json and README in sync (tools/build.py --check)", r.returncode == 0, r.stdout)
    print(f"{'all tests passed' if not failures else str(failures) + ' FAILED'} (open tables)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
