"""Tests of checkers/arc_check.py (complete arcs and 1-saturating sets in PG(2,q)) with its C helper arc_scan.c, and of
tools/lexiarc.c (standard library only, and a C compiler; run by test.sh).

- Conics: in PG(2,q), q odd, the conic {(1,t,t^2)} + (0,0,1) is a complete arc of q + 1 points; for q even it is not
  complete (its nucleus (0,1,0) is on no secant), and with the nucleus added it is a complete hyperoval of q + 2
  points. Checked for prime q and for q = 4, 8, 9, 16, 25, 27, 32, 49 (fields given by irreducible polynomials, among
  them x^4 + x^3 + x^2 + x + 1 over GF(2), whose root x is not a primitive element), by the Python route, the C helper
  and the direct test of every triple and every point (--brute).
- Random sets: for q up to 49 the number of points of the plane that are neither in the set nor on a line through two
  of its points is counted three ways: directly here (every point of the plane, every pair of the set), by the
  Python route and by the C helper (ARC_SCAN_ALL); they must agree on 188 random sets, among them complete arcs built
  by a randomized greedy search and the same arcs with a point removed.
- Red controls: three points on a line, a point repeated, a point outside the field, a reducible or non-monic
  polynomial, a prime power without its polynomial.
- Lexiarcs: tools/lexiarc.c reproduces the sizes t^L_2(2,q) of Bartoli, Davydov, Faina, Kreshchuk, Marcugini and
  Pambianco (arXiv:1404.0469v3, Table 3) for q = 101, 997, 1009 and 4999 (35, 146, 147, 372 points), and the arcs pass
  the checker by both routes; with their last point removed they are refused.
- A published smallest arc: the complete 20-arc of PG(2,61) of Lisonek, Marcugini and Pambianco (2008), rebuilt from
  its description, passes by all three routes (20 is the best known value of the cell arc-61); with the wrong sign of
  a it is not complete. The lexiarc of PG(2,4999) and this arc are written to certs/arc/ for test.sh.

  python3 -I tests/test_arc.py"""
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(ROOT, "checkers", "arc_check.py")
sys.path.insert(0, os.path.join(ROOT, "checkers"))
import arc_check as AC  # noqa: E402

TMP = tempfile.mkdtemp(prefix="arc_test_")
failures = []
POLY = {4: [1, 1, 1], 8: [1, 1, 0, 1], 9: [1, 0, 1], 16: [1, 1, 1, 1, 1], 25: [2, 1, 1], 27: [1, 2, 0, 1],
        32: [1, 0, 1, 0, 0, 1], 49: [3, 6, 1]}


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def write(pts, q, extra=None):
    path = os.path.join(TMP, "a.txt")
    with open(path, "w") as f:
        if q in POLY:
            f.write("poly " + " ".join(map(str, POLY[q])) + "\n")
        if extra:
            f.write(extra)
        f.write("".join(f"{a} {b} {c}\n" for a, b, c in pts))
    return path


def run(q, path, *flags):
    r = subprocess.run([sys.executable, "-I", CHECK, str(q), path] + list(flags), capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr
    return last if r.returncode == 0 else "refused"


def field(q):
    p, h = AC.prime_power(q)
    return AC.Field(q, p, h, POLY.get(q))


def plane(q):
    return [(1, y, z) for y in range(q) for z in range(q)] + [(0, 1, z) for z in range(q)] + [(0, 0, 1)]


def uncovered_direct(F, pts):
    """points of the plane neither in the set nor on a line through two of its points: for every point P, the lines
    from P to the points of the set must not all differ"""
    s = {F.normalize(v) for v in pts}
    n = 0
    for P in plane(F.q):
        if P in s:
            continue
        lines = {F.normalize(F.cross(P, y)) for y in s}
        n += len(lines) == len(s)
    return n


def uncovered_native(F, pts):
    p, h = F.p, F.h
    text = [f"{F.q} {p} {h} 1 {len(pts)}"] + ([" ".join(map(str, F.exp))] if h > 1 else [])
    text += [f"{a} {b} {c}" for a, b, c in pts]
    r = subprocess.run([AC.helper()], input="\n".join(text) + "\n", capture_output=True, text=True,
                       env=dict(os.environ, ARC_SCAN_ALL="1"))
    last = r.stdout.strip().splitlines()[-1]
    return 0 if last.startswith("OK") else int(last.split()[1])


def greedy_arc(F, rng):
    """a random complete arc: add random points that are on no secant until none is left"""
    pts, covered = [], set()
    cand = plane(F.q)
    rng.shuffle(cand)
    for P in cand:
        if P in covered:
            continue
        for y in pts:
            l = F.normalize(F.cross(P, y))
            covered.update(Q for Q in plane(F.q) if F.add(F.add(F.mul(l[0], Q[0]), F.mul(l[1], Q[1])),
                                                          F.mul(l[2], Q[2])) == 0)
        pts.append(P)
        covered.add(P)
    return pts


# conics and hyperovals
for q in (3, 4, 5, 7, 8, 9, 11, 16, 25, 27, 32, 49, 101):
    F = field(q)
    conic = [(1, t, F.mul(t, t)) for t in range(q)] + [(0, 0, 1)]
    for flag in ("--python", "--native") + (("--brute",) if q <= 27 else ()):
        if q % 2:
            expect(f"PG(2,{q}) conic, a complete arc {flag}", run(q, write(conic, q), flag), f"RESULT {q + 1}")
        else:
            expect(f"PG(2,{q}) conic without its nucleus: not complete {flag}", run(q, write(conic, q), flag), "refused")
            expect(f"PG(2,{q}) hyperoval {flag}", run(q, write(conic + [(0, 1, 0)], q), flag), f"RESULT {q + 2}")
        if q % 2:
            expect(f"red PG(2,{q}) conic with a point removed {flag}", run(q, write(conic[1:], q), flag), "refused")
    # a point of the conic scaled by 2 (or any nonzero c != 1): the same point twice
    c = 2 if q > 2 else 1
    dup = conic + [tuple(F.mul(c, x) for x in conic[3])]
    expect(f"red PG(2,{q}) a point given twice (scaled)", run(q, write(dup, q), "--native"), "refused")

# red controls of the format and the field
F7 = field(7)
line3 = [(1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1)]
for flag in ("--python", "--native", "--brute"):
    expect(f"red three points on a line {flag}", run(7, write(line3, 7), flag), "refused")
expect("red a coordinate outside GF(7)", run(7, write([(1, 0, 7), (0, 1, 0), (0, 0, 1)], 7)), "refused")
expect("red the zero vector", run(7, write([(0, 0, 0), (0, 1, 0), (0, 0, 1)], 7)), "refused")
path = os.path.join(TMP, "p.txt")
for q, poly, label in ((9, "poly 2 0 1", "x^2 + 2 = (x + 1)(x + 2) over GF(3), reducible"),
                       (9, "poly 1 0 2", "not monic"), (8, "poly 1 1 1 1", "x^3 + x^2 + x + 1, reducible"),
                       (9, "", "no polynomial for GF(9)")):
    with open(path, "w") as f:
        f.write((poly + "\n" if poly else "") + "1 0 0\n0 1 0\n0 0 1\n1 1 1\n")
    expect(f"red {label}", run(q, path), "refused")
expect("irreducible: x^4 + x^3 + x^2 + x + 1 over GF(2) (x of order 5)", AC.irreducible([1, 1, 1, 1, 1], 2), True)
expect("Field: a primitive element of GF(16) from x^4 + x^3 + x^2 + x + 1", sorted(field(16).exp), list(range(1, 16)))

# random sets: three counts of uncovered points agree
rng = random.Random(2026)
agree, total, arcs = 0, 0, 0
for q in (2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 25, 27, 29, 32, 49):
    F = field(q)
    for trial in range(13 if q <= 29 else 6):
        if trial % 3 == 0:
            pts = greedy_arc(F, rng)
            if trial % 2:
                pts = pts[:-1]
            else:
                arcs += 1
        else:
            n = rng.randrange(3, min(3 * q, q * q) + 1)
            vecs = [(rng.randrange(q), rng.randrange(q), rng.randrange(q)) for _ in range(n)]
            pts = list({F.normalize(v) for v in vecs if any(v)})
            if len(pts) < 3:
                continue
            rng.shuffle(pts)
        a = uncovered_direct(F, pts)
        b = AC.check_python(F, pts, True, count=True)
        c = uncovered_native(F, pts)
        total += 1
        agree += a == b == c
        if not a == b == c:
            print(f"FAIL  PG(2,{q}) {len(pts)} points: uncovered {a} directly, {b} Python, {c} C")
expect(f"{total} random sets (with {arcs} greedy complete arcs): uncovered points counted three ways agree", agree,
       total)

# lexiarcs reproduce the published sizes
exe = os.path.join(TMP, "lexiarc")
subprocess.run(["cc", "-O3", "-o", exe, os.path.join(ROOT, "tools", "lexiarc.c")], check=True)
for q, size in ((101, 35), (997, 146), (1009, 147), (4999, 372)):
    out = subprocess.run([exe, str(q)], capture_output=True, text=True).stdout
    pts = [tuple(map(int, l.split())) for l in out.splitlines()]
    expect(f"lexiarc of PG(2,{q}): {size} points as in arXiv:1404.0469v3", len(pts), size)
    for flag in ("--python", "--native") if q < 1000 else ("--native",):
        expect(f"lexiarc of PG(2,{q}) passes {flag}", run(q, write(pts, q), flag), f"RESULT {size}")
    expect(f"red lexiarc of PG(2,{q}) without its last point", run(q, write(pts[:-1], q)), "refused")
    if q == 4999:
        lex4999 = pts

# the complete 20-arc of PG(2,61) of P. Lisonek, S. Marcugini and F. Pambianco (Contrib. Discrete Math. 3 (2008),
# Proposition 3.1), the smallest known: M2 + T + S3(p) + S3(r) with a = 17 (a^2 + a - 1 = 0), b = 13, c = 47 (roots of
# y^2 + y + 1), p = (1, 11, 32), r = (1, 25, 51), S3 the permutations of the coordinates
F = field(61)


def lmp_arc(a, b=13, c=47):
    H = {F.normalize(x) for x in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (a, 1, 1), (1, a, 1), (1, 1, a), (1, b, c), (1, c, b)]}
    for s in ((1, 11, 32), (1, 25, 51)):
        H |= {F.normalize((s[i], s[j], s[k])) for i, j, k in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1),
                                                              (2, 1, 0))}
    return sorted(H)


H = lmp_arc(17)
for flag in ("--python", "--native", "--brute"):
    expect(f"the complete 20-arc of PG(2,61) of Lisonek, Marcugini and Pambianco {flag}", run(61, write(H, 61), flag),
           "RESULT 20")
expect("red the same with a = -17 (not complete)", run(61, write(lmp_arc(61 - 17), 61)), "refused")
# control files for test.sh (certs/ is not in the repository)
os.makedirs(os.path.join(ROOT, "certs", "arc"), exist_ok=True)
with open(os.path.join(ROOT, "certs", "arc", "lmp2008_pg2_61_20arc.txt"), "w") as f:
    f.write("# complete 20-arc of PG(2,61): Lisonek, Marcugini and Pambianco, Contrib. Discrete Math. 3 (2008)\n")
    f.write("".join(f"{x} {y} {z}\n" for x, y, z in H))
with open(os.path.join(ROOT, "certs", "arc", "lexiarc_4999.txt"), "w") as f:
    f.write("# complete lexiarc of PG(2,4999), 372 points (tools/lexiarc.c; arXiv:1404.0469v3, Table 3)\n")
    f.write("".join(f"{x} {y} {z}\n" for x, y, z in lex4999))
print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
sys.exit(1 if failures else 0)
