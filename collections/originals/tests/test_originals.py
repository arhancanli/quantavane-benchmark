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
    # the uniform three-part splitting has largest overlap exactly 1/3
    code, res, _ = run("collections/originals/checkers/orig_comb.py", ["overlap-three", 3, 3, write("uni3.txt", "1 1 1\n1 1 1\n1 1 1\n")])
    expect(f"cross overlap-three the uniform splitting scores 1/3", res == "1/3", res)


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
    pages()
    print(f"{len(failures)} failures" if failures else "all originals tests passed")
    sys.exit(1 if failures else 0)
