"""Tests of the Quantavane Originals (standard library only; run by test.sh, or on its own):

  python3 -I collections/originals/tests/test_originals.py

1. Every problem's own certificate (refs/) is certified by its checker with exactly the stated best known value, and
   obb.py reports it as not improving (it is the best known value).
2. Red controls: a broken certificate for every problem must be refused (exit status 1).
3. Independent cross-checks on small cases: brute force against the checkers and the exact first values."""
import itertools
import json
import os
import random
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(HERE))
TMP = tempfile.mkdtemp(prefix="originals-tests-")
failures = []


def expect(label, ok, detail=""):
    print(f"{'ok   ' if ok else 'FAIL '} {label}" + ("" if ok else f": {detail}"))
    if not ok:
        failures.append(label)


def run(program, args):
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, program)] + [str(a) for a in args],
                       capture_output=True, text=True)
    res = re.findall(r"^RESULT (\S+)$", r.stdout, re.M)
    return r.returncode, (res[-1] if res else None), r.stdout + r.stderr


def write(name, text):
    path = os.path.join(TMP, name)
    with open(path, "w") as f:
        f.write(text)
    return path


def problems():
    out = []
    for f in sorted(os.listdir(os.path.join(HERE, "problems"))):
        if f.endswith(".json"):
            out.append(json.load(open(os.path.join(HERE, "problems", f))))
    return out


def problems_by_id():
    return {p["id"]: p for p in problems()}


def args_of(p):
    return [os.path.join(ROOT, a) if a.startswith("collections/") else a for a in p["checker"]["args"]]


def certificates(p):
    return open(os.path.join(ROOT, p["best_known"]["provenance"]["certificate"])).read()


def references():
    for p in problems():
        code, res, out = run(p["checker"]["program"], args_of(p) + [os.path.join(ROOT, p["best_known"]["provenance"]["certificate"])])
        expect(f"cert  {p['id']}: certified with value {p['best_known']['exact']}", code == 0 and res == p["best_known"]["exact"], f"exit {code}, RESULT {res}")
        r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "obb.py"), "check", p["id"],
                            os.path.join(ROOT, p["best_known"]["provenance"]["certificate"])], capture_output=True, text=True)
        expect(f"obb   {p['id']}: obb.py check says the certificate does not improve", "does not improve" in r.stdout, r.stdout[-300:])


def lines_of(text):
    return [l for l in text.splitlines() if l.strip() and not l.startswith("#")]


def controls():
    """One broken certificate per problem; each must be refused."""
    P = {p["id"]: p for p in problems()}

    def refuse(pid, text, why):
        p = P[pid]
        path = write(f"control_{pid}.txt", text)
        code, res, out = run(p["checker"]["program"], args_of(p) + [path])
        expect(f"red   {pid}: {why} is refused", code == 1, f"exit {code}: {out[-200:]}")
    if "gauss-admissible" in P:
        L = lines_of(certificates(P["gauss-admissible"]))
        x, y = map(int, L[0].split())
        refuse("gauss-admissible", "\n".join([f"{x + 1} {y}"] + L[1:]) + "\n", "a point of the other parity class (covers both classes modulo 1+i)")
    if "paley-ising" in P:
        s = "".join(lines_of(certificates(P["paley-ising"])))
        refuse("paley-ising", s[:-1] + "\n", "a configuration with 100 spins")
    if "autoconv-square" in P:
        L = lines_of(certificates(P["autoconv-square"]))
        refuse("autoconv-square", "\n".join(["-1 " + L[0].split(None, 1)[1]] + L[1:]) + "\n", "a negative value")
    if "overlap-square" in P:
        L = lines_of(certificates(P["overlap-square"]))
        row = L[0].split()
        row[0] = str(int(row[0]) + 1) if int(row[0]) < 64 else str(int(row[0]) - 1)
        refuse("overlap-square", "\n".join([" ".join(row)] + L[1:]) + "\n", "an integral different from 2")
    if "polytope-ising" in P:
        s = "".join(lines_of(certificates(P["polytope-ising"])))
        refuse("polytope-ising", s + "+\n", "121 spins")
    if "potts3-600" in P:
        t = " ".join(lines_of(certificates(P["potts3-600"]))).split()
        refuse("potts3-600", " ".join(["3"] + t[1:]) + "\n", "a colour outside 0..2")
    if "tri-distinct" in P:
        L = lines_of(certificates(P["tri-distinct"]))
        pts = [tuple(map(int, l.split())) for l in L]
        n = int(P["tri-distinct"]["checker"]["args"][1])
        d2 = lambda p, q: (p[0] - q[0]) ** 2 + (p[0] - q[0]) * (p[1] - q[1]) + (p[1] - q[1]) ** 2
        used = {d2(p, q) for p, q in itertools.combinations(pts, 2)}
        extra = next((a, b) for a in range(n) for b in range(n - a) if (a, b) not in pts and any(d2((a, b), q) in used for q in pts))
        refuse("tri-distinct", "\n".join(L + [f"{extra[0]} {extra[1]}"]) + "\n", "a point repeating a distance")
    if "sync-quadratic" in P:
        w = "".join(lines_of(certificates(P["sync-quadratic"])))
        refuse("sync-quadratic", w[:-1] + "\n", "the word without its last letter")
    if "benzenoid-kemeny" in P:
        L = lines_of(certificates(P["benzenoid-kemeny"]))
        refuse("benzenoid-kemeny", "\n".join(L[:-1] + ["40 40"]) + "\n", "a hexagon not connected to the others")
    if "cell600-idcode" in P:
        t = " ".join(lines_of(certificates(P["cell600-idcode"]))).split()
        refuse("cell600-idcode", " ".join(t[:-6]) + "\n", "the code with 6 vertices removed")
    if "cell600-forest" in P:
        refuse("cell600-forest", " ".join(map(str, range(120))) + "\n", "all 120 vertices")
    if "tsp-sunflower" in P:
        t = " ".join(lines_of(certificates(P["tsp-sunflower"]))).split()
        refuse("tsp-sunflower", " ".join(t[:-1] + [t[0]]) + "\n", "a tour visiting one point twice")
    if "qr-xor" in P:
        L = lines_of(certificates(P["qr-xor"]))
        a, b = L[1].split()
        refuse("qr-xor", "\n".join([L[0], f"{a} {int(b) ^ 1}"] + L[2:]) + "\n", "a circuit with one gate rewired")
    if "quad-admissible" in P:
        t = " ".join(lines_of(certificates(P["quad-admissible"]))).split()
        refuse("quad-admissible", " ".join(t[:-1] + [str(int(t[-1]) + 1)]) + "\n", "a shift of the other parity (n^2 + h is even for every n... at p = 2)")
    if "nussinov-degeneracy" in P:
        s = "".join(lines_of(certificates(P["nussinov-degeneracy"])))
        refuse("nussinov-degeneracy", "T" + s[1:] + "\n", "a sequence with the letter T")
    if "tri-areas" in P:
        L = lines_of(certificates(P["tri-areas"]))
        a, b = map(int, L[0].split())
        c, d = map(int, L[1].split())
        mid = ((a + c) // 2, (b + d) // 2) if (a + c) % 2 == 0 and (b + d) % 2 == 0 else None
        extra = f"{mid[0]} {mid[1]}" if mid and f"{mid[0]} {mid[1]}" not in L else L[0]
        refuse("tri-areas", "\n".join(L + [extra]) + "\n", "a repeated or collinear point")
    if "qr-sumfree" in P:
        t = " ".join(lines_of(certificates(P["qr-sumfree"]))).split()
        p = int(P["qr-sumfree"]["checker"]["args"][1])
        A = sorted(set(int(x) for x in t))
        s2 = next(((a + b) % p for a in A for b in A if (a + b) % p not in A and (a + b) % p != 0 and pow((a + b) % p, (p - 1) // 2, p) == 1), None)
        refuse("qr-sumfree", " ".join(map(str, A + [s2])) + "\n", "the set with a sum of two of its elements added")
    if "overlap-three" in P:
        L = lines_of(certificates(P["overlap-three"]))
        r = [int(x) for x in L[0].split()]
        r[0], r[1] = r[0] + 1, r[1] - 1 if r[1] > 0 else r[1] + 1
        refuse("overlap-three", "\n".join([" ".join(map(str, r))] + L[1:]) + "\n", "a line that no longer sums to DEN")
    if "e8-idcode" in P:
        t = " ".join(lines_of(certificates(P["e8-idcode"]))).split()
        refuse("e8-idcode", " ".join(t[:-5]) + "\n", "the code with 5 roots removed")
    if "snub24-ising" in P:
        sp = "".join(lines_of(certificates(P["snub24-ising"])))
        refuse("snub24-ising", sp[:-2] + "\n", "94 spins")
    if "ga-ising" in P:
        sp = "".join(lines_of(certificates(P["ga-ising"])))
        refuse("ga-ising", sp + "+\n", "101 spins")
    if "e8-goodman" in P:
        c = "".join(lines_of(certificates(P["e8-goodman"])))
        refuse("e8-goodman", c[:-1] + "2\n", "a colour 2")
    if "cata-kemeny" in P:
        L = lines_of(certificates(P["benzenoid-kemeny"])) if "benzenoid-kemeny" in P else []
        if len(L) == 19:
            refuse("cata-kemeny", "\n".join(L) + "\n", "circumcoronene (pericondensed: internal atoms)")
    if "ap-cover" in P:
        L = lines_of(certificates(P["ap-cover"]))
        refuse("ap-cover", "\n".join(L[1:]) + "\n", "the covering without one progression (a pair left uncovered)")
    if "cubic-admissible" in P:
        t = " ".join(lines_of(certificates(P["cubic-admissible"]))).split()
        refuse("cubic-admissible", " ".join(t[:-1] + [str(int(t[-1]) + 1)]) + "\n", "a shift of the other parity")
    if "hp-tri" in P:
        L = lines_of(certificates(P["hp-tri"]))
        refuse("hp-tri", "\n".join(L[:-1] + ["99 99"]) + "\n", "a chain with a broken bond")
    if "nrm-segments" in P:
        L = lines_of(certificates(P["nrm-segments"]))
        pts = [tuple(map(int, l.split())) for l in L]
        sv = int(P["nrm-segments"]["checker"]["args"][1])
        seg = [(a, b) for a in range(-sv, sv + 1) for b in range(-sv, sv + 1) if 1 <= max(abs(a), abs(b), abs(a + b)) <= sv]
        def cls(p, q):
            d = (p[0] - q[0], p[1] - q[1])
            return d if d > (0, 0) else (-d[0], -d[1])
        used = {cls(p, q) for p, q in itertools.combinations(pts, 2)}
        extra = next(r for r in seg if r not in pts and any(cls(r, q) in used for q in pts))
        refuse("nrm-segments", "\n".join(L + [f"{extra[0]} {extra[1]}"]) + "\n", "a mask with one more hole repeating a baseline")
        refuse("nrm-segments", "\n".join(L + ["0 0"]) + "\n", "a hole on the missing centre segment")
    if "eisenstein-triples" in P:
        c = list("".join(lines_of(certificates(P["eisenstein-triples"]))))
        c[2] = c[4] = c[6] = "0"
        refuse("eisenstein-triples", "".join(c) + "\n", "a colouring with 3, 5 and 7 the same colour (9 + 15 + 25 = 49)")
    if "cell120-coil" in P:
        L = lines_of(certificates(P["cell120-coil"]))
        refuse("cell120-coil", "\n".join(L[:5] + L[6:]) + "\n", "the coil with its sixth cell left out")
    if "six-frame" in P:
        sq = "".join(lines_of(certificates(P["six-frame"])))
        refuse("six-frame", "TAA" + sq + "\n", "the sequence with a stop codon TAA in front")
    if "cell120-great" in P:
        L = lines_of(certificates(P["cell120-great"]))
        sys.path.insert(0, os.path.join(HERE, "checkers"))
        import orig_geom
        pts600, _ = orig_geom.cell600_points()
        where = {v: i for i, v in enumerate(pts600)}
        first = [int(x) for x in L[0].split()]
        opposite = sorted(where[tuple((-c[0], -c[1]) for c in pts600[i])] for i in first)
        refuse("cell120-great", "\n".join(L + [" ".join(map(str, opposite))]) + "\n", "a set with a vertex and its opposite")
    if "y-array" in P:
        L = lines_of(certificates(P["y-array"]))
        arm = L[0].split()
        refuse("y-array", "\n".join([" ".join(arm + [arm[0]])] + L[1:]) + "\n", "an arm with one distance used twice")
    if "gauss-prime-ap" in P:
        L = lines_of(certificates(P["gauss-prime-ap"]))
        x0, y0 = map(int, L[0].split())
        x1, y1 = map(int, L[1].split())
        k = len(L)
        refuse("gauss-prime-ap", "\n".join(f"{x0 + j * (x1 - x0)} {y0 + j * (y1 - y0) + (1 if j == k - 1 else 0)}" for j in range(k)) + "\n", "a last term off the progression")
    if "e8-resolving" in P:
        t = " ".join(lines_of(certificates(P["e8-resolving"]))).split()
        refuse("e8-resolving", " ".join(t[:6]) + "\n", "6 of its vertices (at least 11 are needed)")
        refuse("e8-resolving", " ".join(["240"] + t[1:]) + "\n", "a vertex number out of range")
    if "lj-fcc" in P:
        L = lines_of(certificates(P["lj-fcc"]))
        x, y, z = map(int, L[0].split())
        refuse("lj-fcc", "\n".join([f"{x + 1} {y} {z}"] + L[1:]) + "\n", "a point with an odd coordinate sum (not a lattice site)")
        refuse("lj-fcc", "\n".join(L[:-1] + [L[0]]) + "\n", "an atom placed twice")
    if "align-ambiguity" in P:
        L = lines_of(certificates(P["align-ambiguity"]))
        refuse("align-ambiguity", L[0].replace("T", "U") + "\n" + L[1] + "\n", "an RNA letter U")
    if "tetra-distinct" in P:
        L = lines_of(certificates(P["tetra-distinct"]))
        pts = [tuple(map(int, l.split())) for l in L]
        nn = int(P["tetra-distinct"]["checker"]["args"][1])
        qf = lambda p, r: sum((p[k] - r[k]) ** 2 for k in range(3)) + (p[0] - r[0]) * (p[1] - r[1]) + (p[1] - r[1]) * (p[2] - r[2]) + (p[0] - r[0]) * (p[2] - r[2])
        used = {qf(p, r) for p, r in itertools.combinations(pts, 2)}
        extra = next((a, b, c) for a in range(nn) for b in range(nn - a) for c in range(nn - a - b) if (a, b, c) not in pts and any(qf((a, b, c), r) in used for r in pts))
        refuse("tetra-distinct", "\n".join(L + ["%d %d %d" % extra]) + "\n", "a point repeating a distance")
    if "prime-cover" in P:
        t = " ".join(lines_of(certificates(P["prime-cover"]))).split()
        refuse("prime-cover", " ".join(t[1:]) + "\n", "the code without its first prime (every prime of it is needed)")
        refuse("prime-cover", " ".join(t + ["10001"]) + "\n", "a code containing 10001 = 73 x 137")
    if "diamond-bonds" in P:
        L = lines_of(certificates(P["diamond-bonds"]))
        x, y, z = map(int, L[0].split())
        refuse("diamond-bonds", "\n".join([f"{x + 1} {y + 1} {z}"] + L[1:]) + "\n", "a point that is not a site of the diamond lattice")
        refuse("diamond-bonds", "\n".join(L[:-1] + ["40 40 40"]) + "\n", "a piece with one atom far away (not connected)")
    if "mclaughlin-ising" in P:
        sp = "".join(lines_of(certificates(P["mclaughlin-ising"])))
        refuse("mclaughlin-ising", sp[:-1] + "\n", "274 spins")
    if "prime-code" in P:
        t = " ".join(lines_of(certificates(P["prime-code"]))).split()
        first = t[0]
        isp = lambda m: m > 1 and all(m % d for d in range(2, int(m ** 0.5) + 1))
        near = next(str(q) for k in range(5) for dgt in "0123456789" for q in [int(first[:k] + dgt + first[k + 1:])]
                    if dgt != first[k] and not (k == 0 and dgt == "0") and isp(q) and str(q) not in t)
        refuse("prime-code", " ".join(t + [near]) + "\n", f"the code with {near}, one digit away from {first}")
        refuse("prime-code", " ".join(t + ["10001"]) + "\n", "a code containing 10001 = 73 x 137")
    if "gauss-jacobsthal" in P:
        x0, y0, side = lines_of(certificates(P["gauss-jacobsthal"]))[0].split()
        refuse("gauss-jacobsthal", f"1 0 {side}\n", "a square containing the unit 1, divisible by no prime")
        refuse("gauss-jacobsthal", f"{x0} {y0}\n", "a corner without the side")
        refuse("gauss-jacobsthal", f"0 1 {side}\n", "a square containing the unit i")
    if "diamond-knot" in P:
        L = lines_of(certificates(P["diamond-knot"]))
        chair = "0 0 0\n1 -1 -1\n2 0 -2\n3 1 -1\n2 2 0\n1 1 1\n"
        refuse("diamond-knot", chair, "a six-membered ring (cyclohexane chair, unknotted)")
        refuse("diamond-knot", "\n".join(["40 40 40"] + L[1:]) + "\n", "the ring with one atom moved far away (a broken bond)")
    if "diamond-link" in P:
        text = certificates(P["diamond-link"])
        ring1 = text.split("\n-\n")[0].strip()
        chair = "0 0 0\n1 -1 -1\n2 0 -2\n3 1 -1\n2 2 0\n1 1 1\n"
        far = "".join(f"{int(a) + 40} {int(b) + 40} {int(c)}\n" for a, b, c in (l.split() for l in chair.splitlines()))
        refuse("diamond-link", chair + "-\n" + far, "two separate chairs (linking number 0)")
        refuse("diamond-link", ring1 + "\n-\n" + ring1 + "\n", "a ring paired with itself (shared sites)")
    if "e8-coulomb" in P:
        L = lines_of(certificates(P["e8-coulomb"]))
        refuse("e8-coulomb", "\n".join(["2 2 2 0 0 0 0 0"] + L[1:]) + "\n", "a vector that is not a root of E8")
        refuse("e8-coulomb", "\n".join(L[:-1] + [L[0]]) + "\n", "a root used twice")


def cross_checks():
    """Small cases against brute force written here independently of the checkers."""
    # Paley energies: the checker's value against a direct sum for random configurations
    P = 13
    chi = lambda a: 0 if a % P == 0 else (1 if pow(a, (P - 1) // 2, P) == 1 else -1)
    rng = random.Random(1)
    for t in range(3):
        s = [rng.choice((1, -1)) for _ in range(P)]
        e = sum(chi(j - i) * s[i] * s[j] for i in range(P) for j in range(i + 1, P))
        code, res, _ = run("collections/originals/checkers/orig_phys.py", ["paley-ising", P, write("pal.txt", "".join("+" if v > 0 else "-" for v in s) + "\n")])
        expect(f"cross paley-ising p=13 random configuration {t}: {e}", res == str(e), res)
    # E_13 = -20 by brute force over all configurations with s_0 = +1
    best = min(sum(chi(j - i) * s[i] * s[j] for i in range(P) for j in range(i + 1, P))
               for bits in range(1 << (P - 1)) for s in [[1] + [1 if bits >> k & 1 else -1 for k in range(P - 1)]])
    expect(f"cross paley-ising p=13 ground state by brute force: {best}", best == -20, best)
    # admissible Gaussian sets: D(k) for k <= 5 by brute force over subsets of a box containing 0
    box = [(x, y) for x in range(-3, 4) for y in range(-3, 4)]
    def adm(H):
        k = len(H)
        if len({(x + y) % 2 for x, y in H}) == 2:
            return False
        if k >= 5:
            for r in (2, 3):     # the two prime ideals above 5: residues x + r y mod 5 (r^2 = -1)
                if len({(x + r * y) % 5 for x, y in H}) == 5:
                    return False
        return True
    for k, want in ((3, 4), (4, 4), (5, 10)):
        best = min(max((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for a, b in itertools.combinations(H, 2))
                   for rest in itertools.combinations([q for q in box if q != (0, 0)], k - 1) for H in [((0, 0),) + rest] if adm(H))
        expect(f"cross gauss-admissible D({k}) = {want} by brute force", best == want, best)
    # Nussinov counts against enumeration of all structures
    pairs = {("A", "U"), ("U", "A"), ("G", "C"), ("C", "G"), ("G", "U"), ("U", "G")}
    def structures(s, i, j):
        if j - i < 1:
            return [[]]
        out = [st for st in structures(s, i + 1, j)]
        for k in range(i + 4, j):
            if (s[i], s[k]) in pairs:
                for a in structures(s, i + 1, k):
                    for b in structures(s, k + 1, j):
                        out.append([(i, k)] + a + b)
        return out
    for s in ("UUACCUUGGAAGG", "GGGAAAUCCCAUU", "ACGUACGUACGU"):
        sts = structures(s, 0, len(s))
        m = max(len(x) for x in sts)
        want = sum(1 for x in sts if len(x) == m)
        code, res, _ = run("collections/originals/checkers/orig_bio.py", ["nussinov-degeneracy", len(s), write("nd.txt", s + "\n")])
        expect(f"cross nussinov-degeneracy {s}: {want} optimal structures by enumeration", res == str(want), res)
    # triangular grid distinct distances: g(6) = 5 by brute force
    n = 6
    pts = [(a, b) for a in range(n) for b in range(n - a)]
    d2 = lambda p, q: (p[0] - q[0]) ** 2 + (p[0] - q[0]) * (p[1] - q[1]) + (p[1] - q[1]) ** 2
    best = max(k for k in range(1, 7) for S in itertools.combinations(pts, k)
               if len({d2(p, q) for p, q in itertools.combinations(S, 2)}) == k * (k - 1) // 2)
    expect(f"cross tri-distinct g(6) = 5 by brute force", best == 5, best)
    # sync-quadratic: r(7) = 9 by brute force over all words of length <= 9
    def resets(w, p):
        S = set(range(p))
        for c in w:
            S = {(x + 1) % p for x in S} if c == "a" else {x * x % p for x in S}
        return len(S) == 1
    r7 = next(L for L in range(1, 12) if any(resets(w, 7) for w in itertools.product("ab", repeat=L)))
    expect(f"cross sync-quadratic r(7) = 9 by brute force over words", r7 == 9, r7)
    # quadratic admissible: m(5) = 13 by brute force
    def qadm(H):
        for p in (2, 3, 5, 7):
            if {x * x % p for x in range(p)} <= {(-h) % p for h in H}:
                return False
        return True
    m5 = min(max(H) for H in itertools.combinations(range(1, 16), 5) if qadm(H))
    expect(f"cross quad-admissible m(5) = 13 by brute force", m5 == 13, m5)
    # sum-free sets of quadratic residues: s(29) = 8 and s(37) = 10 by brute force
    for p, want in ((29, 8), (37, 10)):
        Q = sorted({x * x % p for x in range(1, p)})
        best = 0
        for mask in range(1 << len(Q)):
            A = [Q[i] for i in range(len(Q)) if mask >> i & 1]
            if len(A) <= best:
                continue
            S = set(A)
            if all((a + b) % p not in S for a in A for b in A):
                best = len(A)
        expect(f"cross qr-sumfree s({p}) = {want} by brute force", best == want, best)
    # distinct triangle areas: t(6) = 5 by brute force
    pts = [(a, b) for a in range(6) for b in range(6 - a)]
    ar = lambda p, q, r: abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]))
    best = max(k for k in range(3, 7) for S in itertools.combinations(pts, k)
               if all(ar(*T) for T in itertools.combinations(S, 3)) and len({ar(*T) for T in itertools.combinations(S, 3)}) == k * (k - 1) * (k - 2) // 6)
    expect(f"cross tri-areas t(6) = 5 by brute force", best == 5, best)
    # progressions covering Z_7: none with 8 blocks, one with 9 (A(7) = 9)
    p = 7
    aps = sorted({tuple(sorted(((a + i * d) % p) for i in range(3))) for a in range(p) for d in range(1, p)})
    allpairs = set(itertools.combinations(range(p), 2))
    def covers(bs):
        c = set()
        for b in bs:
            c.update(itertools.combinations(b, 2))
        return c == allpairs
    has8 = any(covers(bs) for bs in itertools.combinations(aps, 8))
    has9 = any(covers(bs) for bs in itertools.combinations(aps, 9))
    expect("cross ap-cover A(7) = 9 by brute force over sets of progressions", (not has8) and has9, (has8, has9))
    # cubic family: m(5) = 14 by brute force
    def cadm(H):
        for p in (2, 3, 5, 7, 11, 13):
            if {x ** 3 % p for x in range(p)} <= {(-h) % p for h in H}:
                return False
        return True
    m5 = min(max(H) for H in itertools.combinations(range(1, 18), 5) if cadm(H))
    expect(f"cross cubic-admissible m(5) = 14 by brute force", m5 == 14, m5)
    # catacondensed: triphenylene (h = 4) has Kemeny constant 50521/1386, the minimum over the five catacondensed systems
    code, res, _ = run("collections/originals/checkers/orig_chem.py", ["cata-kemeny", 4, write("triphenylene.txt", "0 1\n1 1\n1 2\n2 0\n")])
    expect(f"cross cata-kemeny triphenylene: 50521/1386", res == "50521/1386", res)
    # non-redundant masks: no 8 of the 18 segments of the 2-ring mirror (the JWST layout) are non-redundant, 7 are
    seg2 = [(a, b) for a in range(-2, 3) for b in range(-2, 3) if 1 <= max(abs(a), abs(b), abs(a + b)) <= 2]
    def nonred(S):
        seen = set()
        for p, q in itertools.combinations(S, 2):
            d = (p[0] - q[0], p[1] - q[1])
            d = d if d > (0, 0) else (-d[0], -d[1])
            if d in seen:
                return False
            seen.add(d)
        return True
    has8 = any(nonred(S) for S in itertools.combinations(seg2, 8))
    seven = next(S for S in itertools.combinations(seg2, 7) if nonred(S))
    code, res, _ = run("collections/originals/checkers/orig_astro.py", ["nrm-segments", 2, write("nrm7.txt", "\n".join(f"{a} {b}" for a, b in seven) + "\n")])
    expect("cross nrm-segments h(2) = 7 by brute force (JWST layout)", (not has8) and res == "7", (has8, res))
    # Eisenstein triples: the checker's divisor enumeration against a direct search up to 1500
    import math
    direct = sum(1 for x in range(1, 1501) for y in range(x + 1, 1501) if x * x + x * y + y * y <= 1500 ** 2 and math.isqrt(x * x + x * y + y * y) ** 2 == x * x + x * y + y * y)
    sys.path.insert(0, os.path.join(HERE, "checkers"))
    import orig_numth
    expect(f"cross eisenstein-triples {direct} triples with z <= 1500 by direct search", len(orig_numth.eisenstein_triples_upto(1500)) == direct, direct)
    # Gaussian prime progressions: least largest norm for K = 3..7 by brute force over a small disc
    gp = [(x, y) for x in range(-6, 7) for y in range(-6, 7) if x * x + y * y <= 40 and ((x and y and all((x * x + y * y) % d for d in range(2, x * x + y * y)) and x * x + y * y > 1) or ((x == 0) != (y == 0) and (abs(x) + abs(y)) % 4 == 3 and all((abs(x) + abs(y)) % d for d in range(2, abs(x) + abs(y)))))]
    gps = set(gp)
    for K, want in ((3, 9), (4, 9), (5, 17), (6, 17), (7, 29)):
        best = min((max((a[0] + j * (b[0] - a[0])) ** 2 + (a[1] + j * (b[1] - a[1])) ** 2 for j in range(K))
                    for a in gp for b in gp if a != b and all((a[0] + j * (b[0] - a[0]), a[1] + j * (b[1] - a[1])) in gps for j in range(K))), default=None)
        expect(f"cross gauss-prime-ap least largest norm {want} for {K} terms (brute force)", best == want, best)
    # E8 root graph: distances from a root are 0, 1, 2, 3 for 1, 56, 182 and 1 roots (inner products 2, 1, 0 or -1, -2)
    roots = sorted({tuple(v) for i, j in itertools.combinations(range(8), 2) for si in (2, -2) for sj in (2, -2)
                    for v in [[si if k == i else sj if k == j else 0 for k in range(8)]]} |
                   {s8 for s8 in itertools.product((1, -1), repeat=8) if s8.count(-1) % 2 == 0})
    ip = [sum(a * b for a, b in zip(roots[0], r)) for r in roots]
    predicted = [{8: 0, 4: 1, 0: 2, -4: 2, -8: 3}[x] for x in ip]
    nbr = [[j for j in range(240) if sum(a * b for a, b in zip(roots[i], roots[j])) == 4] for i in range(240)]
    bfs = [-1] * 240
    bfs[0], queue = 0, [0]
    for u in queue:
        for w in nbr[u]:
            if bfs[w] < 0:
                bfs[w] = bfs[u] + 1
                queue.append(w)
    expect("cross e8-resolving BFS distances from a root: 1, 56, 182, 1 at 0..3, as the inner products predict",
           bfs == predicted and [bfs.count(k) for k in range(4)] == [1, 56, 182, 1], [bfs.count(k) for k in range(4)])
    # Lennard-Jones on the fcc lattice (cutoff q <= 8): the regular tetrahedron (six nearest-neighbour pairs) has energy
    # exactly -6, and the certificate's exact energy agrees with an independent floating-point sum
    code, res, _ = run("collections/originals/checkers/orig_chem.py", ["lj-fcc", 4, write("tet.txt", "0 0 0\n1 1 0\n1 0 1\n0 1 1\n")])
    expect("cross lj-fcc the tetrahedron has energy -6", res == "-6", res)
    code, res, _ = run("collections/originals/checkers/orig_chem.py", ["lj-fcc", 2, write("far.txt", "0 0 0\n3 1 0\n")])
    expect("cross lj-fcc a pair at squared distance 10 (beyond the cutoff) has energy 0", res == "0", res)
    if "lj-fcc" in problems_by_id():
        pp = problems_by_id()["lj-fcc"]
        pts = [tuple(map(int, l.split())) for l in lines_of(certificates(pp))]
        fl = sum(64.0 / q ** 6 - 16.0 / q ** 3 for q in (sum((a - b) ** 2 for a, b in zip(u, v)) for u, v in itertools.combinations(pts, 2)) if q <= 8)
        from fractions import Fraction
        val = float(Fraction(pp["best_known"]["exact"]))
        expect(f"cross lj-fcc exact energy {val:.9f} agrees with a floating-point sum", abs(val - fl) < 1e-9, fl)
    # alignment counts: A(1..3) = 1, 3, 5 by enumerating every alignment path of every pair
    def paths(i, j):
        if i == 0 and j == 0:
            yield ()
            return
        if i and j:
            for p in paths(i - 1, j - 1):
                yield p + ("D",)
        if i:
            for p in paths(i - 1, j):
                yield p + ("H",)
        if j:
            for p in paths(i, j - 1):
                yield p + ("V",)
    def costs(x, y, p):
        i = j = c = 0
        for st in p:
            if st == "D":
                c += x[i] != y[j]
                i += 1
                j += 1
            elif st == "H":
                c += 1
                i += 1
            else:
                c += 1
                j += 1
        return c
    for n, want in ((1, 1), (2, 3), (3, 5)):
        allp = list(paths(n, n))
        best = 0
        for x in itertools.product("ACGT", repeat=n):
            for y in itertools.product("ACGT", repeat=n):
                cs = [costs(x, y, p) for p in allp]
                best = max(best, cs.count(min(cs)))
        expect(f"cross align-ambiguity A({n}) = {want} by enumerating all paths of all pairs", best == want, best)
    # tetrahedral grid: no 5 points of side 4 have distinct distances, 4 have (exhaustive)
    tp = [(a, b, c) for a in range(4) for b in range(4 - a) for c in range(4 - a - b)]
    qf = lambda p, r: sum((p[k] - r[k]) ** 2 for k in range(3)) + (p[0] - r[0]) * (p[1] - r[1]) + (p[1] - r[1]) * (p[2] - r[2]) + (p[0] - r[0]) * (p[2] - r[2])
    dd = lambda S: len({qf(p, r) for p, r in itertools.combinations(S, 2)}) == len(S) * (len(S) - 1) // 2
    has5 = any(dd(S) for S in itertools.combinations(tp, 5))
    has4 = any(dd(S) for S in itertools.combinations(tp, 4))
    expect("cross tetra-distinct side 4: 4 points but not 5 (exhaustive)", has4 and not has5, (has4, has5))
    # covering the two-digit primes by one-digit changes: no 3 primes do it, 4 do (brute force)
    p2 = [q for q in range(10, 100) if all(q % d for d in range(2, q))]
    nbh = {q: {r for r in p2 if r == q or sum(a != b for a, b in zip(str(q), str(r))) == 1} for q in p2}
    covers = lambda C: set().union(*(nbh[c] for c in C)) == set(p2)
    expect("cross prime-cover two-digit primes need 4 (brute force)", not any(covers(C) for C in itertools.combinations(p2, 3)) and any(covers(C) for C in itertools.combinations(p2, 4)))
    # 120-cell from the 600-cell's tetrahedra: 600 cells, each sharing a triangle with exactly 4 others; a 5-cycle
    # (the girth is 5) is accepted as a coil
    import orig_codes
    a6 = orig_codes.cell600_graph()
    tets = sorted({tuple(sorted((a, b, c, d))) for a in range(120) for b in a6[a] for c in a6[a] & a6[b] for d in a6[a] & a6[b] & a6[c]})
    tset = [set(t) for t in tets]
    nb = [[j for j in range(len(tets)) if j != i and len(tset[i] & tset[j]) == 3] for i in range(len(tets))]
    expect("cross cell120-coil 600 cells of the 600-cell, each adjacent to 4", len(tets) == 600 and all(len(x) == 4 for x in nb), len(tets))
    five = next([0, a, b, c, d] for a in nb[0] for b in nb[a] if b != 0 for c in nb[b] if c not in (0, a) for d in nb[c] if d not in (0, a, b) and 0 in nb[d])
    code, res, _ = run("collections/originals/checkers/orig_codes.py", ["cell120-coil", write("pent.txt", "".join(" ".join(map(str, tets[i])) + "\n" for i in five))])
    expect("cross cell120-coil a pentagon of the 120-cell is a coil of length 5", res == "5", res)
    # genetic code: the checker's table (built from codon lists) against the table written as one string in the order
    # A, C, G, T (index 16a + 4b + c); 64 codons, 3 stops, 20 amino acids
    import orig_bio
    order = "KNKNTTTTRSRSIIMIQHQHPPPPRRRRLLLLEDEDAAAAGGGGVVVV*Y*YSSSS*CWCLFLF"
    alt = {a + b + c: order[16 * i + 4 * j + k] for i, a in enumerate("ACGT") for j, b in enumerate("ACGT") for k, c in enumerate("ACGT")}
    expect("cross six-frame genetic code: two independent tables agree (64 codons, 3 stops, 20 amino acids)",
           alt == orig_bio.STANDARD_CODE and len(set(alt.values()) - {"*"}) == 20 and list(alt.values()).count("*") == 3)
    # great circles of the 600-cell through its vertices: 200 hexagons and 72 decagons (Coxeter), as our planes give
    import orig_geom
    g60, _ = orig_geom.great_points("600")
    sizes = [len(l) for l in orig_geom.great_lines(g60) if len(l) >= 3]
    expect("cross cell120-great the 600-cell has 200 great hexagons and 72 great decagons", (sizes.count(3), sizes.count(5), len(sizes)) == (200, 72, 272), (sizes.count(3), sizes.count(5)))
    # Y arrays: L(5) = 5 and L(6) = 6 by brute force over all placements
    def yok(S):
        seen = set()
        for (k1, a), (k2, b) in itertools.combinations(S, 2):
            q = (a - b) ** 2 if k1 == k2 else a * a + a * b + b * b
            if q in seen:
                return False
            seen.add(q)
        return True
    for n, want in ((5, 5), (6, 6)):
        least = next(Lm for Lm in range(1, 10) if any(yok(S) for S in itertools.combinations([(k, a) for k in range(3) for a in range(1, Lm + 1)], n)))
        expect(f"cross y-array L({n}) = {want} by brute force", least == want, least)
    # the uniform three-part splitting has largest overlap exactly 1/3
    code, res, _ = run("collections/originals/checkers/orig_comb.py", ["overlap-three", 3, 3, write("uni3.txt", "1 1 1\n1 1 1\n1 1 1\n")])
    expect(f"cross overlap-three the uniform splitting scores 1/3", res == "1/3", res)
    # diamond lattice: the connected pieces with up to 7 atoms, grown here set by set and identified up to translation,
    # number 2, 4, 12, 44, 182, 796, 3612 (OEIS A039740 from two atoms on) with at most 0, 1, 2, 3, 4, 6, 7 bonds,
    # as the exhaustive search (tools/src/diamond.c) and the problem page state
    def dnb(p):
        sg = 1 if p[0] % 2 == 0 else -1
        return [(p[0] + sg * a, p[1] + sg * b, p[2] + sg * c) for a, b, c in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]
    def dcanon(S):
        m = min(S)
        t = m if m[0] % 2 == 0 else (m[0] - 1, m[1] - 1, m[2] - 1)
        return tuple(sorted((a - t[0], b - t[1], c - t[2]) for a, b, c in S))
    level, counts, most = {dcanon([(0, 0, 0)]), dcanon([(1, 1, 1)])}, [], []
    for size in range(1, 8):
        counts.append(len(level))
        most.append(max(sum(1 for q in S for r in dnb(q) if r in set(S)) // 2 for S in level))
        if size < 7:
            level = {dcanon(set(S) | {r}) for S in level for q in S for r in dnb(q) if r not in S}
    expect("cross diamond-bonds pieces of 1..7 atoms: 2, 4, 12, 44, 182, 796, 3612 (A039740) with at most 0, 1, 2, 3, 4, 6, 7 bonds",
           counts == [2, 4, 12, 44, 182, 796, 3612] and most == [0, 1, 2, 3, 4, 6, 7], (counts, most))
    if "diamond-bonds" in problems_by_id():
        dp = problems_by_id()["diamond-bonds"]
        exact_rows = {r[0]: (r[1], r[2]) for r in dp["first_values"]["rows"] if str(r[4]).startswith("exact")}
        expect("cross diamond-bonds the page's exact rows for 1..7 atoms agree with the enumeration here",
               all(exact_rows[k] == (most[k - 1], 4 * k - 2 * most[k - 1]) for k in range(1, 8)), exact_rows)
    adam = "0 0 0\n1 -1 -1\n2 0 -2\n3 1 -1\n4 0 0\n3 -1 1\n2 0 2\n2 2 0\n2 -2 0\n1 1 1\n"
    code, res, _ = run("collections/originals/checkers/orig_chem.py", ["diamond-bonds", 10, write("adamantane.txt", adam)])
    expect("cross diamond-bonds adamantane: 10 atoms, 12 bonds, 16 hydrogens (C10H16)", res == "16", res)
    # McLaughlin graph: the checker's graph is strongly regular (275, 112, 30, 56) (checked for every pair through the
    # first 12 vertices), and the certificate's energy agrees with a recount from the graph tool's matrix
    import orig_phys
    mn, medges = orig_phys.mclaughlin_graph()
    madj = [set() for _ in range(mn)]
    for a, b in medges:
        madj[a].add(b)
        madj[b].add(a)
    srg_ok = all(len(madj[v]) == 112 for v in range(mn)) and all(len(madj[u] & madj[v]) == (30 if v in madj[u] else 56) for u in range(12) for v in range(mn) if v != u)
    expect("cross mclaughlin-ising the graph is srg(275, 112, 30, 56)", mn == 275 and srg_ok)
    if "mclaughlin-ising" in problems_by_id():
        sys.path.insert(0, os.path.join(HERE, "tools"))
        import mclaughlin_graph
        A = mclaughlin_graph.graph()
        sp = "".join(lines_of(certificates(problems_by_id()["mclaughlin-ising"])))
        sv = [1 if c == "+" else -1 for c in sp]
        e2 = sum(A[i][j] * sv[i] * sv[j] for i in range(275) for j in range(i + 1, 275))
        expect(f"cross mclaughlin-ising the certificate's energy {e2} from the tool's matrix equals the best known value",
               str(e2) == problems_by_id()["mclaughlin-ising"]["best_known"]["exact"], e2)
    # codes made of primes: a 36-prime code of four-digit primes meets the bound 9 x 4 (two codewords may agree in at most
    # one digit, so the pairs (first digit, last digit) are all different), and no five three-digit primes differ
    # pairwise in all three digits (only four possible last digits)
    code4 = "1009 1117 9859 1361 1583 2129 2207 2333 3037 3163 3251 3319 4073 4289 4327 4441 5101 5413 5557 5639 6469 6521 6653 6947 7477 7549 7681 7703 8731 8867 8999 9697 8243 9923 9011 2971"
    code, res, _ = run("collections/originals/checkers/orig_codes.py", ["prime-code", 4, 3, write("pc4.txt", code4 + "\n")])
    pairs4 = {(w[0], w[-1]) for w in code4.split()}
    expect("cross prime-code four-digit primes: a code of 36 meets the bound 9 x 4 = 36", res == "36" and len(pairs4) == 36, res)
    p3 = [q for q in range(100, 1000) if all(q % d for d in range(2, int(q ** 0.5) + 1))]
    far = lambda a, b: all(x != y for x, y in zip(str(a), str(b)))
    four = next(([a, b, c, d] for a in p3 for b in p3 if far(a, b) for c in p3 if far(a, c) and far(b, c)
                 for d in p3 if far(a, d) and far(b, d) and far(c, d)), None)
    expect("cross prime-code three-digit primes: 4 differing pairwise in every digit exist, 5 cannot (last digits 1, 3, 7, 9)",
           four is not None and {str(q)[-1] for q in p3} == {"1", "3", "7", "9"}, four)
    # Gaussian Jacobsthal: exhaustive search over one residue class per prime (independent of tools/src/gjacob.c) gives
    # s = 2 for norm <= 5 and s = 4 for norm <= 13 (the next sizes impossible); a 4 x 4 cover turned into a square by
    # the Chinese remainder theorem (brute force over corners modulo 2 x 3 x 5 x 13) is certified by the checker
    def gideals(X):
        out = []
        for q in range(2, X + 1):
            if any(q % d == 0 for d in range(2, q)):
                continue
            if q == 2:
                out.append((2, "r", lambda x, y: (x + y) % 2))
            elif q % 4 == 1:
                for r in [a for a in range(2, q) if (a * a + 1) % q == 0]:
                    out.append((q, "s", lambda x, y, q=q, r=r: (x + y * r) % q))
            elif q * q <= X:
                out.append((q, "i", lambda x, y, q=q: (x % q) * q + (y % q)))
        return out
    def gcover(X, side):
        ids = gideals(X)
        full = (1 << (side * side)) - 1
        opts = []
        for _, _, f in ids:
            m = {}
            for x in range(side):
                for y in range(side):
                    m.setdefault(f(x, y), [0, None])[0] |= 1 << (x * side + y)
                    m[f(x, y)][1] = f(x, y)
            opts.append(sorted((v[0], v[1]) for v in m.values()))
        for combo in itertools.product(*opts):
            acc = 0
            for v, _ in combo:
                acc |= v
            if acc == full:
                return ids, [c for _, c in combo]
        return None
    small = [(X, sd, gcover(X, sd) is not None) for X, sd in ((5, 2), (5, 3), (13, 4), (13, 5))]
    expect("cross gauss-jacobsthal exhaustive over residue classes: s(5) = 2, s(13) = 4", [o for _, _, o in small] == [True, False, True, False], small)
    ids, classes = gcover(13, 4)
    corner = next((x0, y0) for x0 in range(390) for y0 in range(390)
                  if all((x0 + y0) % 2 == c if kind == "r" else (f(-x0, -y0) == c) for (q, kind, f), c in zip(ids, classes)))
    code, res, _ = run("collections/originals/checkers/orig_numth.py", ["gauss-jacobsthal", 13, write("gj13.txt", f"{corner[0]} {corner[1]} 4\n")])
    expect(f"cross gauss-jacobsthal the cover found here, placed at {corner[0]} + {corner[1]}i, is certified with side 4", res == "4", res)
    # knot determinants: smooth trefoil, figure-eight and unknotted curves sampled at 120 integer points give 3, 5 and 1;
    # the mirror image of our ring (x and y swapped, sites stay on the lattice) is certified with the same length
    import math
    import orig_chem
    def curve(f, N=120, S=1000):
        return [tuple(int(round(S * c)) for c in f(2 * math.pi * k / N)) for k in range(N)]
    kd = [orig_chem.knot_determinant(curve(f)) for f in (
        lambda t: (math.sin(t) + 2 * math.sin(2 * t), math.cos(t) - 2 * math.cos(2 * t), -math.sin(3 * t)),
        lambda t: ((2 + math.cos(2 * t)) * math.cos(3 * t), (2 + math.cos(2 * t)) * math.sin(3 * t), math.sin(4 * t)),
        lambda t: (math.cos(t), math.sin(t), 0.3 * math.sin(2 * t)))]
    expect("cross diamond-knot knot determinants: trefoil 3, figure-eight 5, unknot 1", kd == [3, 5, 1], kd)
    if "diamond-knot" in problems_by_id():
        dk = problems_by_id()["diamond-knot"]
        mirror = "".join(f"{b} {a} {c}\n" for a, b, c in (l.split() for l in lines_of(certificates(dk))))
        code, res, _ = run("collections/originals/checkers/orig_chem.py", ["diamond-knot", write("mirror_knot.txt", mirror)])
        expect("cross diamond-knot the mirror image of our ring is certified with the same length", code == 0 and res == dk["best_known"]["exact"], res)
    # linking numbers: two circles forming a Hopf link give 1 up to sign, separate circles 0, and reversing one circle
    # flips the sign
    hopf_a = curve(lambda t: (math.cos(t), math.sin(t), 0.0), 80)
    hopf_b = curve(lambda t: (1 + math.cos(t), 0.0, math.sin(t)), 80)
    apart_b = curve(lambda t: (3 + math.cos(t), 0.0, math.sin(t)), 80)
    lk = (orig_chem.linking_number(hopf_a, hopf_b), orig_chem.linking_number(hopf_a, apart_b), orig_chem.linking_number(hopf_a[::-1], hopf_b))
    expect("cross diamond-link linking numbers: Hopf link +-1, separate circles 0, reversed circle opposite sign", abs(lk[0]) == 1 and lk[1] == 0 and lk[2] == -lk[0], lk)
    # E8: the 240 roots (each with 56, 126, 56, 1 others at inner products 1, 0, -1, -2) have energy
    # 6720/8 + 15120/64 + 6720/216 + 120/512, and the best three roots, found by brute force over pairs added to a fixed
    # root (the Weyl group is transitive), are three roots summing to zero, with energy 3/216 = 1/72
    import orig_geom
    from fractions import Fraction
    e8 = sorted({tuple(v) for i, j in itertools.combinations(range(8), 2) for si in (2, -2) for sj in (2, -2)
                 for v in [[si if k == i else sj if k == j else 0 for k in range(8)]]} |
                {s8 for s8 in itertools.product((1, -1), repeat=8) if s8.count(-1) % 2 == 0})
    allroots = "".join(" ".join(map(str, r)) + "\n" for r in e8)
    code, res, _ = run("collections/originals/checkers/orig_geom.py", ["e8-coulomb", 240, write("e8all.txt", allroots)])
    want = Fraction(6720, 8) + Fraction(15120, 64) + Fraction(6720, 216) + Fraction(120, 512)
    expect(f"cross e8-coulomb all 240 roots: energy {want}", res == f"{want.numerator}/{want.denominator}", res)
    w = lambda a, b: Fraction(1, (4 - 2 * (sum(x * y for x, y in zip(a, b)) // 4)) ** 3)
    best3 = min(w(e8[0], b) + w(e8[0], c) + w(b, c) for b, c in itertools.combinations(e8[1:], 2))
    expect("cross e8-coulomb three roots: the minimum energy is 1/72 (brute force)", best3 == Fraction(1, 72), best3)


def cell_lines(pid):
    path = os.path.join(HERE, "cells", pid + ".jsonl")
    return [json.loads(l) for l in open(path) if l.strip()] if os.path.exists(path) else []


def cells():
    """Cells (one question at each value of its parameter): tools/cells.py runs every cell's certificate through the
    family's checker and writes the cells files; they must come out unchanged, so every stated value is the value the
    checker proves. One cell per family through obb.py; a red control per family: the certificate of its largest cell
    checked as its smallest cell (the parameter must be enforced), and one broken certificate."""
    before = {f: open(os.path.join(HERE, "cells", f)).read() for f in os.listdir(os.path.join(HERE, "cells"))} \
        if os.path.isdir(os.path.join(HERE, "cells")) else {}
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "tools", "cells.py")], capture_output=True, text=True)
    after = {f: open(os.path.join(HERE, "cells", f)).read() for f in os.listdir(os.path.join(HERE, "cells"))}
    expect(f"cells every certificate is certified with its stated value; cells files up to date ({len(after)} families,"
           f" {sum(t.count(chr(10)) for t in after.values())} cells)", before == after and r.returncode == 0,
           (r.stdout + r.stderr)[-400:])
    P = problems_by_id()
    for f in sorted(after):
        pid = f[:-6]
        cs = cell_lines(pid)
        blk = P[pid]["cells"]
        expect(f"cells {pid}: every cell is under its family, with a unique id, parameters and a certificate",
               len({c["id"] for c in cs}) == len(cs) and all(c["family"] == pid and c["id"].startswith(pid + "-")
                                                             and set(c["params"]) == set(blk["params"]) for c in cs)
               and sum(bool(c.get("headline")) for c in cs) == 1, pid)
        sample = next((c for c in cs if not c.get("headline")), cs[0])
        rr = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "obb.py"), "check", sample["id"],
                             os.path.join(ROOT, sample["certificate"])], capture_output=True, text=True)
        expect(f"cells {sample['id']}: obb.py check certifies the cell and says it does not improve",
               "does not improve" in rr.stdout and f"certified value" in rr.stdout, rr.stdout[-300:])
        if len(cs) >= 2:
            lo, hi = (cs[0], cs[-1]) if pid not in SMALL_AS_LARGE else (cs[-1], cs[0])
            vals = {k: v for k, v in lo["params"].items()}
            args = [a.format(**vals) for a in blk["args"]]
            code, res, out = run(P[pid]["checker"]["program"], [os.path.join(ROOT, a) if a.startswith("collections/") else a
                                                                 for a in args] + [os.path.join(ROOT, hi["certificate"])])
            expect(f"red   {pid}: the certificate of {hi['id']} checked as {lo['id']} is refused", code == 1,
                   f"exit {code}: {out[-200:]}")
        broken = CELL_CONTROLS.get(pid)
        if broken:
            ex = [c for c in cs if c["exact"]]
            c = ex[len(ex) // 2] if pid in EXACT_CONTROL and ex else cs[len(cs) // 2]
            text, why = broken(open(os.path.join(ROOT, c["certificate"])).read(), c["params"])
            args = [a.format(**c["params"]) for a in blk["args"]]
            code, res, out = run(P[pid]["checker"]["program"], [os.path.join(ROOT, a) if a.startswith("collections/") else a
                                                                 for a in args] + [write(f"cellctl_{c['id']}.txt", text)])
            expect(f"red   {c['id']}: {why} is refused", code == 1, f"exit {code}: {out[-200:]}")


def _drop_last_line(text, params):
    L = lines_of(text)
    return "\n".join(L[:-1]) + "\n", "the certificate without its last line"


def _dup_first_point(text, params):
    L = lines_of(text)
    return "\n".join(L + [L[0]]) + "\n", "the certificate with its first point repeated"


def _flip_spin(text, params):
    s = "".join(lines_of(text))
    return s[:-1] + "\n", "a configuration with one spin missing"


SMALL_AS_LARGE = {"sync-quadratic"}     # a long reset word also resets a smaller automaton; a short one cannot reset a large
EXACT_CONTROL = {"sync-quadratic"}      # the control removes a letter from a shortest word (an exact cell)


def _drop_last_letter(text, params):
    return "".join(lines_of(text))[:-1] + "\n", "a shortest reset word without its last letter"


CELL_CONTROLS = {"sync-quadratic": _drop_last_letter, "tri-distinct": _dup_first_point, "tri-areas": _dup_first_point, "tetra-distinct": _dup_first_point,
                 "paley-ising": _flip_spin, "gauss-admissible": _dup_first_point, "e8-coulomb": _dup_first_point,
                 "diamond-bonds": _dup_first_point, "lj-fcc": _dup_first_point, "nrm-segments": _dup_first_point,
                 "hp-tri": _drop_last_line, "tsp-sunflower": _dup_first_point, "tsp-gaussian": _dup_first_point,
                 "quad-admissible": _dup_first_point, "cubic-admissible": _dup_first_point,
                 "y-array": lambda t, p: ("\n".join([lines_of(t)[0] + " " + lines_of(t)[0].split()[0]] + lines_of(t)[1:])
                                          + "\n", "an arm with one distance used twice")}


# first-values tables: (parameter columns, value column); a row is matched to the cell with those parameters
TABLE_SPEC = {"y-array": ((0,), 1), "paley-ising": ((0,), 1), "sync-quadratic": ((0,), 1), "tri-distinct": ((0,), 1),
              "tri-areas": ((0,), 1), "tetra-distinct": ((0,), 2), "qr-sumfree": ((0,), 2), "quad-admissible": ((0,), 1),
              "cubic-admissible": ((0,), 1), "diamond-bonds": ((0,), 2), "nussinov-degeneracy": ((0,), 1),
              "qr-xor": ((0,), 3), "lj-fcc": ((0,), 2), "align-ambiguity": ((0,), 1), "nrm-segments": ((0,), 2),
              "hp-tri": ((0,), 2), "benzenoid-kemeny": ((0,), 2), "cata-kemeny": ((0,), 2),
              "gauss-jacobsthal": ((0,), 2), "tsp-sunflower": ((0,), 1), "potts3-600": ((0,), 1),
              "prime-code": ((0, 1), 3), "prime-cover": ((0,), 2), "ap-cover": ((0,), 1), "e8-coulomb": ((0,), 1),
              "gauss-prime-ap": ((0,), 1), "gauss-admissible": ((0,), {"4": 1, "3": 2})}


def table_number(x, objective):
    """The value a table entry claims: '68 (exact)' -> 68, '<= 59 (ours)' -> 59, '46 to 48' -> our 48 (minimize),
    '9 or 10' -> our 9 (maximize), 'p/q = decimal' -> p/q; None for text and for decimals without a fraction."""
    from fractions import Fraction
    s = str(x).strip().replace(",", "")
    m = re.match(r"^(-?\d+) (to|or) (-?\d+)", s)
    if m:
        lo, hi = int(m.group(1)), int(m.group(3))
        return Fraction(hi if objective == "minimize" else lo)
    m = re.match(r"^(?:<=|>=)?\s*(-?\d+(?:/\d+)?)(?![\d.])", s)
    return Fraction(m.group(1)) if m else None


def tables():
    """Every value a first-values table publishes is backed by a certificate in the repository that passes its
    checker: the row's cell (same parameters, same value), the headline certificate, or a table certificate
    (first_values.certified: checker arguments and a file in refs/table/, run here); rows that publish someone else's
    value or no value are listed in first_values.context with the reason. Anything else fails."""
    from fractions import Fraction
    E8ALL, E8C = Fraction(637975, 576), 56 * Fraction(1, 8) + 126 * Fraction(1, 64) + 56 * Fraction(1, 216) + Fraction(1, 512)
    for p in problems():
        fv = p.get("first_values")
        if not fv:
            continue
        pid = p["id"]
        cells = {tuple(str(v) for v in c["params"].values()): Fraction(c["best"]) for c in cell_lines(pid)}
        certified, context = fv.get("certified", {}), fv.get("context", {})
        bad = []
        for key, entry in certified.items():
            code, res, out = run(entry.get("program", p["checker"]["program"]), [os.path.join(ROOT, a) if a.startswith("collections/") else a
                                                            for a in entry["args"]] + [os.path.join(ROOT, entry["certificate"])])
            if code != 0 or res is None or Fraction(res) != Fraction(entry["value"]):
                bad.append(f"table certificate {key}: exit {code}, RESULT {res}, stated {entry['value']}")
        spec = TABLE_SPEC.get(pid)
        for r in fv["rows"]:
            label = str(r[0])
            if spec is None:
                if label in context:
                    continue
                cv = next((e for k, e in certified.items() if e.get("row", k) == label), None)
                if cv is not None:
                    if any(table_number(x, p["objective"]) == Fraction(cv.get("row_value", cv["value"])) for x in r):
                        continue
                    bad.append(f"row {label}: the table does not show the certified value {cv.get('row_value', cv['value'])}")
                    continue
                if label in fv.get("headline_rows", []) and any(table_number(x, p["objective"]) == Fraction(p["best_known"]["exact"])
                                                                 for x in r):
                    continue
                bad.append(f"row {label}: no certificate and no reason")
                continue
            pc, vc = spec
            for ring, col in (vc.items() if isinstance(vc, dict) else [(None, vc)]):
                v = table_number(r[col], p["objective"])
                if v is None:
                    continue
                key = ((ring,) if ring else ()) + tuple(str(r[i]) for i in pc)
                stem = "_".join(key)
                cv = certified.get(stem)
                if cells.get(key) == v or (cv and Fraction(cv.get("row_value", cv["value"])) == v):
                    continue
                if pid == "e8-coulomb" and 120 < int(r[0]) < 240 and (str(240 - int(r[0])),) in cells and \
                        E8ALL - (240 - int(r[0])) * E8C + cells[(str(240 - int(r[0])),)] == v:
                    continue        # the complement of the cell for 240 - N
                if stem in context:
                    continue
                bad.append(f"row {stem}: {r[col]} (cell {cells.get(key)})")
        expect(f"table {pid}: every published value has a certificate ({len(fv['rows'])} rows, {len(certified)} table "
               f"certificates)", not bad, "; ".join(bad[:6]))


def pages():
    """The generated pages, index.json and README table match the problem files."""
    before = {f: open(os.path.join(HERE, f)).read() for f in ("index.json", "README.md")}
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "tools", "build.py")], capture_output=True, text=True)
    after = {f: open(os.path.join(HERE, f)).read() for f in ("index.json", "README.md")}
    expect("pages index.json and README.md are up to date (tools/build.py changes nothing)", before == after and r.returncode == 0, r.stderr[-300:])
    n = len(problems())
    mds = [f for f in os.listdir(os.path.join(HERE, "problems")) if f.endswith(".md")]
    expect(f"pages one page per problem ({n})", len(mds) == n, len(mds))


if __name__ == "__main__":
    references()
    controls()
    cross_checks()
    cells()
    pages()
    print(f"{len(failures)} failures" if failures else "all originals tests passed")
    sys.exit(1 if failures else 0)
