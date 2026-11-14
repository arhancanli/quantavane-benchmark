"""Unit tests for checkers/pack_check.py (standard library only; run by test.sh): exact packings at the edge of
validity (touching circles, circles touching the container), each with a red control that moves one number by one unit
in its last decimal, and malformed inputs.

  python3 -I tests/test_pack.py"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "pack_check.py")
failures = []


def run(section, n, lines):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("\n".join(lines) + "\n")
    r = subprocess.run([sys.executable, "-I", CHECK, section, str(n), f.name], capture_output=True, text=True)
    os.unlink(f.name)
    return r.returncode, (r.stdout.strip().splitlines() or [""])[-1]


def expect(label, got, want_code, want_last=None):
    code, last = got
    ok = code == want_code and (want_last is None or last == want_last)
    print(f"{'ok   ' if ok else 'FAIL '} {label}: exit {code}, {last}")
    if not ok:
        failures.append(label)


# four circles of radius 1/4 fill the unit square exactly (each touches two sides and two neighbours)
sq = ["0.25", "0.25 0.25", "0.75 0.25", "0.25 0.75", "0.75 0.75"]
expect("csq 4 circles of radius 1/4 (touching)", run("csq", 4, sq), 0, "RESULT 1/4")
expect("red: radius 0.2500000000000000000001", run("csq", 4, ["0.2500000000000000000001"] + sq[1:]), 1)
expect("red: one centre moved by 1e-25", run("csq", 4, sq[:-1] + ["0.75 0.7499999999999999999999999"]), 1)
# two circles of radius 1/2 in the unit circle, touching each other and the circle
cc = ["0.5", "-0.5 0", "0.5 0"]
expect("cci 2 circles of radius 1/2", run("cci", 2, cc), 0, "RESULT 1/2")
expect("red: one centre at 0.5000000000000000000001", run("cci", 2, cc[:-1] + ["0.5000000000000000000001 0"]), 1)
# half disc: one circle of radius 1/2 at (0, 1/2) touches the diameter and the arc
expect("csc 1 circle of radius 1/2", run("csc", 1, ["0.5", "0 0.5"]), 0, "RESULT 1/2")
expect("red: y = 0.4999999999999999999999", run("csc", 1, ["0.5", "0 0.4999999999999999999999"]), 1)
# quarter disc: a circle of radius 2/5 at (2/5, 2/5): |c| = 2 sqrt(2)/5 = 0.5657 <= 3/5
expect("ccq 1 circle of radius 2/5", run("ccq", 1, ["0.4", "0.4 0.4"]), 0, "RESULT 2/5")
# triangle: the incircle has radius (2 - sqrt 2)/2 = 0.29289321881...; 0.2928932188 fits, 0.2928932189 does not
expect("crt incircle from below", run("crt", 1, ["0.2928932188", "0.2928932188 0.2928932188"]), 0, "RESULT 732233047/2500000000")
expect("red: crt 0.2928932189 (above the incircle)", run("crt", 1, ["0.2928932189", "0.2928932189 0.2928932189"]), 1)
# cube and balls
expect("scu 8 balls of radius 1/4", run("scu", 8, ["0.25"] + [f"{x} {y} {z}" for x in (0.25, 0.75) for y in (0.25, 0.75) for z in (0.25, 0.75)]), 0, "RESULT 1/4")
expect("ssp 2 balls of radius 1/2", run("ssp", 2, ["0.5", "0.5 0 0", "-0.5 0 0"]), 0, "RESULT 1/2")
expect("hsp4 2 balls of radius 1/2", run("hsp4", 2, ["0.5", "0.5 0 0 0", "-0.5 0 0 0"]), 0, "RESULT 1/2")
expect("red: hsp6 radius 0.50001", run("hsp6", 2, ["0.50001", "0.5 0 0 0 0 0", "-0.5 0 0 0 0 0"]), 1)
# radii 1 and 2 in a circle of radius 3 (centres -2 and 1), and in a square of side 4 at (3,2)? no: (1,1) and (2,2)
# overlap; radii 1, 2 side by side in a square of side 6: centres (1, 2) and (4, 2)
expect("ccin radii 1, 2 in a circle of radius 3", run("ccin", 2, ["3", "-2 0", "1 0"]), 0, "RESULT 3")
expect("red: ccin container 2.9999999999", run("ccin", 2, ["2.9999999999", "-2 0", "1 0"]), 1)
expect("csqn radii 1, 2 in a square of side 6", run("csqn", 2, ["6", "1 2", "4 2"]), 0, "RESULT 6")
expect("red: csqn circles 1 and 2 overlapping", run("csqn", 2, ["6", "1 2", "3.9999 2"]), 1)
# malformed inputs
expect("malformed: exponent", run("csq", 1, ["5e-1", "0.5 0.5"]), 1)
expect("malformed: one line too few", run("csq", 2, ["0.25", "0.25 0.25"]), 1)
expect("malformed: unknown section", run("cpt", 1, ["0.1", "0 0"]), 1)
# a grid of 10,000 touching circles of radius 1/200 in the unit square: the grid test must stay exact and fast
big = ["0.005"] + [f"{(2 * i + 1) / 200:.3f} {(2 * j + 1) / 200:.3f}" for i in range(100) for j in range(100)]
expect("csq 10,000 touching circles", run("csq", 10000, big), 0, "RESULT 1/200")
print(f"pack_check tests: {len(failures)} failures")
sys.exit(1 if failures else 0)
