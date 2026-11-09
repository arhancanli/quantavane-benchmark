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
    if "hp-tri" in P:
        L = lines_of(certificates(P["hp-tri"]))
        refuse("hp-tri", "\n".join(L[:-1] + ["99 99"]) + "\n", "a chain with a broken bond")


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
