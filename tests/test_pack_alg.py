"""Tests of checkers/pack_alg_check.py (standard library only; run by test.sh).

- Each regular polygon (n = 5..17): one circle at the centre with a radius 10^-30 below the apothem cos(pi/n) passes,
  10^-30 above fails.
- Exact equality is settled by algebra: a circle touching an edge of the hexagon exactly (centre (1, -2r)) is found
  to touch, and moved by 10^-40 it is found inside or outside; the identity cos(pi/5) - cos(2pi/5) = 1/2 is found
  exact and 1/2 + 10^-40 is not.
- Radii: circles 2 and 8 of ccir (radii sqrt 2 and sqrt 8) at distance sqrt 18 touch exactly (sqrt 2 + sqrt 8 =
  sqrt 18) and pass, 10^-30 closer they overlap; circles 1 and 8 of ccic (radii 1 and 8^(-2/3) = 1/4) at distance 5/4
  touch exactly; containers just large enough and 10^-30 too small; csqs's radii (N/i)^(1/2); malformed inputs.

  python3 -I tests/test_pack_alg.py"""
import math
import os
import subprocess
import sys
import tempfile
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "pack_alg_check.py")
sys.path.insert(0, os.path.join(ROOT, "checkers"))
import pack_alg_check as pa  # noqa: E402

failures = []


def run(section, n, lines):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("\n".join(lines) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, section, str(n), f.name], capture_output=True, text=True)
    os.unlink(f.name)
    return r.returncode


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def dec(q, d=60):
    q = Fraction(q)
    v = q.numerator * 10 ** d // q.denominator
    s = str(abs(v)).rjust(d + 1, "0")
    return ("-" if v < 0 else "") + s[:-d] + "." + s[-d:]


for sec, n in pa.POLYGON.items():
    lo, hi = pa.Cosines(n).interval(2, 300)                 # the apothem cos(pi/n), to 300 bits
    below, above = lo - Fraction(1, 10 ** 30), hi + Fraction(1, 10 ** 30)
    expect(f"{sec}: one circle, radius 1e-30 below the apothem", run(sec, 1, [dec(below), "0 0"]), 0)
    expect(f"red: {sec}: one circle, radius 1e-30 above the apothem", run(sec, 1, [dec(above), "0 0"]), 1)

hexagon = pa.Polygon(6)
r = Fraction(1, 10)
expect("hexagon: centre (1, -2r) touches edge 1 exactly", hexagon.is_zero(-r, Fraction(1), -2 * r, 2), True)
expect("hexagon: moved by 1e-40 it does not touch", hexagon.is_zero(-r, Fraction(1), -2 * r + Fraction(1, 10 ** 40), 2), False)
pent = pa.Polygon(5)
expect("pentagon: cos(pi/5) - cos(2pi/5) - 1/2 = 0", pent.is_zero(Fraction(-1, 2), Fraction(1), Fraction(0), 4), True)
expect("pentagon: cos(pi/5) - cos(2pi/5) - 1/2 - 1e-40 != 0", pent.is_zero(Fraction(-1, 2) - Fraction(1, 10 ** 40), Fraction(1), Fraction(0), 4), False)
# a circle of radius 0.1 at the hexagon's centre shifted towards edge 1's normal: inside, touching edge 1 exactly is
# impossible with rational numbers there, but the edge test must agree with the float picture on each side
ok, _ = hexagon.inside(Fraction(1, 10), Fraction(0), Fraction(0))
expect("hexagon: a small circle at the centre is inside", ok, True)

# ccir: radii sqrt(i); circles 2 and 8 at distance sqrt(18) touch exactly; the others far away on a line
def ccir_lines(N, gap_fix):
    pts = [None] * N
    pts[1] = (Fraction(0), Fraction(0))
    pts[7] = (Fraction(3) - gap_fix, Fraction(3))
    x = Fraction(20)
    for i in range(N):
        if pts[i] is None:
            pts[i] = (x, Fraction(0))
            x += 10
    return [" ".join(dec(c, 40) for c in p) for p in pts]

V = Fraction(200)
expect("ccir: circles 2 and 8 touching exactly (sqrt 2 + sqrt 8 = sqrt 18)", run("ccir", 8, [str(V)] + ccir_lines(8, 0)), 0)
expect("red: ccir: circle 8 moved 1e-30 closer", run("ccir", 8, [str(V)] + ccir_lines(8, Fraction(1, 10 ** 30))), 1)
# ccic: radii i^(-2/3); circle 8 has radius 1/4; circles 1 and 8 at distance 5/4 touch exactly
lines = ["0 0", "10 0", "20 0", "30 0", "40 0", "50 0", "60 0", "1.25 0"]
expect("ccic: circles 1 and 8 (radii 1 and 1/4) touching exactly", run("ccic", 8, ["100"] + lines), 0)
expect("red: ccic: circle 8 at 1.2499999999999999999999999999999", run("ccic", 8, ["100"] + lines[:-1] + ["1.2499999999999999999999999999999 0"]), 1)
# containers: one circle of radius 1 (ccis, i = 1) at the centre of a circle of radius 1 fits exactly; 1 - 1e-30 not
expect("ccis: N = 1 in a circle of radius 1", run("ccis", 1, ["1", "0 0"]), 0)
expect("red: ccis: container 1 - 1e-30", run("ccis", 1, [dec(1 - Fraction(1, 10 ** 30)), "0 0"]), 1)
# ccib: circle 2 has radius 2^(-1/5) = 0.8705505632961241...; at (0, 0) in a circle of radius 0.8705505633 it fits
expect("red: ccib: a container of radius 0.8705505633 cannot hold circle 1 (radius 1)", run("ccib", 2, ["0.8705505633", "100 100", "0 0"]), 1)
expect("ccib: both circles in a container of radius 3 at (-1.5, 0) and (1.1, 0)", run("ccib", 2, ["3", "-1.5 0", "1.1 0"]), 0)
expect("red: ccib: the same at (-1, 0) and (0.8, 0) (overlap)", run("ccib", 2, ["3", "-1 0", "0.8 0"]), 1)
# csqr: radii sqrt(i) in [0,V]^2; circle 4 (radius 2) touching two sides at (2, 2) of the square of side 4
expect("csqr: circle 4 of radius 2 at (2, 2), with 1..3 elsewhere, side 20", run("csqr", 4, ["20", "10 10", "15 5", "5 15", "2 2"]), 0)
expect("red: csqr: circle 4 at (1.9999999999, 2)", run("csqr", 4, ["20", "10 10", "15 5", "5 15", "1.9999999999 2"]), 1)
# csqs: radii (N/i)^(1/2): for N = 4, circle 1 has radius 2 and circle 4 radius 1; side 4 holds circle 1 at (2, 2)
expect("csqs: N = 4, circle 1 (radius 2) at (2, 2) in a square of side 4, the rest outside -> refused",
       run("csqs", 4, ["4", "2 2", "3 3.5", "3.5 0.5", "0.5 3.5"]), 1)
expect("csqs: N = 1, radius 1 at (1, 1), side 2", run("csqs", 1, ["2", "1 1"]), 0)
expect("red: csqs: N = 1, side 1.9999999999", run("csqs", 1, ["1.9999999999", "1 1"]), 1)
# malformed
expect("malformed: unknown section", run("csqc", 1, ["1", "0 0"]), 1)
expect("malformed: three coordinates", run("cpt", 1, ["0.1", "0 0 0"]), 1)
expect("malformed: exponent", run("cpt", 1, ["1e-1", "0 0"]), 1)
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
