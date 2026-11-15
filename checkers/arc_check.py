"""Exact check of a complete arc (or, with --saturating, a 1-saturating set) in the projective plane PG(2,q)
(standard library only, with a C helper for large inputs).

  python3 -I arc_check.py Q FILE [--saturating] [--python | --native | --brute] [--max-work STEPS]

Q is a prime power p^h. FILE has one point per line: three integers x y z, 0 <= x, y, z < Q, not all 0 (homogeneous
coordinates; '#' starts a comment). For prime Q the integers are residues modulo Q. For Q = p^h with h > 1 the first
line must be "poly c_0 c_1 ... c_h": a monic irreducible polynomial f = c_0 + c_1 x + ... + c_h x^h over GF(p) (c_h
= 1), checked by the checker; an element of GF(Q) = GF(p)[x]/(f) is written as the integer whose base-p digits, from
the lowest, are its coefficients of 1, x, ..., x^(h-1). Any irreducible f may be used: the fields are isomorphic.

A complete arc is a set K of points of PG(2,Q), no three on a line, such that every other point of the plane lies on a
line through two points of K (a secant). With --saturating the condition "no three on a line" is dropped: a
1-saturating set is a set S such that every point of the plane is in S or on a line through two points of S. The
result is the number of points (smaller is better).

How it is checked: points are scaled so that their first nonzero coordinate is 1 and must be distinct. The line
through every pair of points is computed exactly; for an arc no line may come from two pairs. A point P off the set
that is on no secant lies on a line through the first point x0 of the set that holds no other point of the set (a
tangent at x0), so it suffices to check the points of the tangents at x0: for each tangent the intersections with
every secant not through x0 are marked, and all Q of its points other than x0 must be marked. This takes about
Q n^2 / 2 steps for n points; above 2 x 10^6 steps it runs in the C helper arc_scan.c (built with cc -O3 on first use;
for prime Q one addition and one comparison per step). --brute tests every triple of points and every point of the
plane directly (small Q only, for the tests). Prints "RESULT n" and exits 0 for a valid set; exits 1 otherwise."""
import os
import subprocess
import sys

NATIVE_FROM = 2 * 10 ** 6
MAX_WORK = 2 ** 39


def helper():
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", "arc_scan"), os.path.join(here, "arc_scan.c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    return exe


def prime_power(q):
    """(p, h) with q = p^h, or None"""
    if q < 2:
        return None
    p = next((d for d in range(2, int(q ** 0.5) + 1) if q % d == 0), q)
    h = 0
    while q % p == 0:
        q //= p
        h += 1
    return (p, h) if q == 1 else None


def prime_factors(n):
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    return out + ([n] if n > 1 else [])


# polynomials over GF(p) as coefficient lists, lowest first
def pmod(a, f, p):
    a = [c % p for c in a]
    while len(a) >= len(f):
        c = a[-1]
        if c:
            s = len(a) - len(f)
            for i, fc in enumerate(f):
                a[s + i] = (a[s + i] - c * fc) % p
        a.pop()
    while a and a[-1] == 0:
        a.pop()
    return a


def pmulmod(a, b, f, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return pmod(r, f, p)


def ppowmod(a, e, f, p):
    r, a = [1], pmod(a, f, p)
    while e:
        if e & 1:
            r = pmulmod(r, a, f, p)
        a = pmulmod(a, a, f, p)
        e >>= 1
    return r


def pgcd(a, b, p):
    a, b = a[:], b[:]
    while b:
        inv = pow(b[-1], p - 2, p)
        while len(a) >= len(b) and a:
            c = a[-1] * inv % p
            s = len(a) - len(b)
            for i, bc in enumerate(b):
                a[s + i] = (a[s + i] - c * bc) % p
            while a and a[-1] == 0:
                a.pop()
        a, b = b, a
    return a


def irreducible(f, p):
    """Rabin's test: f of degree h is irreducible over GF(p) iff x^(p^h) = x mod f and gcd(x^(p^(h/r)) - x, f) = 1
    for every prime r dividing h."""
    h = len(f) - 1
    def xpow(k):                  # x^(p^k) mod f, by k p-th powers
        r = [0, 1]
        for _ in range(k):
            r = ppowmod(r, p, f, p)
        return r
    def minus_x(a):
        a = a + [0] * max(0, 2 - len(a))
        a[1] = (a[1] - 1) % p
        while a and a[-1] == 0:
            a.pop()
        return a
    if minus_x(xpow(h)):
        return False
    for r in prime_factors(h):
        g = pgcd(f[:], minus_x(xpow(h // r)), p)
        if len(g) > 1:
            return False
    return True


class Field:
    """GF(q): residues for prime q; for q = p^h integers whose base-p digits are polynomial coefficients mod f, with
    tables of the powers of a primitive element (exp) and of logarithms."""

    def __init__(self, q, p, h, f=None):
        self.q, self.p, self.h = q, p, h
        if h == 1:
            return
        def to_int(a):
            return sum(c * p ** i for i, c in enumerate(a))
        def times(a, g):          # a * g mod f; a a digit list of length h, g without leading zeros
            r = [0] * (h + len(g) - 1)
            for i, x in enumerate(a):
                if x:
                    for j, y in enumerate(g):
                        if y:
                            r[i + j] += x * y
            return (pmod(r, f, p) + [0] * h)[:h]
        for k in [p] + list(range(2, q)):     # k = p is the polynomial x
            g = pmod([(k // p ** i) % p for i in range(h)], f, p)
            if all(ppowmod(g, (q - 1) // r, f, p) != [1] for r in prime_factors(q - 1)):
                break                         # g has order q - 1: a primitive element
        exp, a = [], [1] + [0] * (h - 1)
        for _ in range(q - 1):
            exp.append(to_int(a))
            a = times(a, g)
        self.exp = exp
        self.log = [0] * q
        for k, e in enumerate(exp):
            self.log[e] = k

    def add(self, a, b):
        if self.h == 1:
            return (a + b) % self.q
        p, r, m = self.p, 0, 1
        while a or b:
            r += ((a % p + b % p) % p) * m
            a //= p
            b //= p
            m *= p
        return r

    def neg(self, a):
        if self.h == 1:
            return (-a) % self.q
        p, r, m = self.p, 0, 1
        while a:
            r += ((-a) % p) * m
            a //= p
            m *= p
        return r

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul(self, a, b):
        if self.h == 1:
            return a * b % self.q
        if not a or not b:
            return 0
        return self.exp[(self.log[a] + self.log[b]) % (self.q - 1)]

    def inv(self, a):
        if self.h == 1:
            return pow(a, self.q - 2, self.q)
        return self.exp[(-self.log[a]) % (self.q - 1)]

    def normalize(self, v):
        k = 0 if v[0] else 1 if v[1] else 2
        i = self.inv(v[k])
        return tuple(self.mul(x, i) for x in v)

    def cross(self, a, b):
        F = self
        return (F.sub(F.mul(a[1], b[2]), F.mul(a[2], b[1])), F.sub(F.mul(a[2], b[0]), F.mul(a[0], b[2])),
                F.sub(F.mul(a[0], b[1]), F.mul(a[1], b[0])))


def check_python(F, pts, saturating, count=False):
    """(True, message) or (False, reason): the method of arc_scan.c in Python; with count, the number of points of the
    plane that are not covered (after the arc test)."""
    q, n = F.q, len(pts)
    lines = {}
    for i in range(n):
        for j in range(i + 1, n):
            l = F.normalize(F.cross(pts[i], pts[j]))
            if l in lines:
                if not saturating:
                    a, b = lines[l]
                    c = a if a not in (i, j) else b
                    return False, f"points {i + 1}, {j + 1} and {c + 1} (in the order given) are on one line"
                continue
            lines[l] = (i, j)
    x0 = pts[0]
    K = 0 if x0[0] else 1 if x0[1] else 2
    A, B = (1, 2) if K == 0 else (0, 2) if K == 1 else (0, 1)
    secdir = set()
    for y in pts[1:]:
        g = y[K]
        al, be = F.sub(y[A], F.mul(g, x0[A])), F.sub(y[B], F.mul(g, x0[B]))
        secdir.add(F.mul(be, F.inv(al)) if al else q)
    sec = []
    for l in lines:
        w = F.add(F.add(F.mul(l[0], x0[0]), F.mul(l[1], x0[1])), F.mul(l[2], x0[2]))
        if w:
            iw = F.neg(F.inv(w))
            sec.append((F.mul(l[A], iw), F.mul(l[B], iw)))
    uncovered = 0
    for b in range(q + 1):
        if b in secdir:
            continue
        seen = {d for c, d in sec} if b == q else {F.add(c, F.mul(d, b)) for c, d in sec}
        if count:
            uncovered += q - len(seen)
            continue
        if len(seen) < q:
            t = min(set(range(q)) - seen)
            v = [F.mul(t, x) for x in x0]
            if b < q:
                v[A], v[B] = F.add(v[A], 1), F.add(v[B], b)
            else:
                v[B] = F.add(v[B], 1)
            return False, f"the point {F.normalize(v)} is " + (
                "neither in the set nor on a line through two of its points" if saturating else
                "on no line through two points of the arc: the arc is not complete")
    if count:
        return uncovered
    return True, f"{len(lines)} lines through two points; every point is covered"


def check_brute(F, pts, saturating):
    """Every triple and every point of the plane, directly (small q only)."""
    q, n = F.q, len(pts)
    def det(a, b, c):
        return F.add(F.add(F.mul(a[0], F.sub(F.mul(b[1], c[2]), F.mul(b[2], c[1]))),
                           F.mul(a[1], F.sub(F.mul(b[2], c[0]), F.mul(b[0], c[2])))),
                     F.mul(a[2], F.sub(F.mul(b[0], c[1]), F.mul(b[1], c[0]))))
    if not saturating:
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if det(pts[i], pts[j], pts[k]) == 0:
                        return False, f"points {i + 1}, {j + 1} and {k + 1} are on one line"
    s = set(pts)
    plane = [(1, y, z) for y in range(q) for z in range(q)] + [(0, 1, z) for z in range(q)] + [(0, 0, 1)]
    for P in plane:
        if P in s:
            continue
        dirs = set()
        for y in pts:
            d = F.normalize(F.cross(P, y))
            if d in dirs:
                break
            dirs.add(d)
        else:
            return False, f"the point {P} is on no line through two points of the set"
    return True, "every triple and every point checked directly"


def main():
    flags = [a for a in sys.argv[1:] if a in ("--saturating", "--python", "--native", "--brute")]
    args = [a for a in sys.argv[1:] if a not in flags]
    max_work = MAX_WORK
    if "--max-work" in args:
        i = args.index("--max-work")
        max_work = int(args[i + 1])
        del args[i:i + 2]
    if len(args) != 2:
        print(__doc__)
        return 2
    saturating = "--saturating" in flags
    try:
        q = int(args[0])
    except ValueError:
        print("Q must be an integer")
        return 1
    ph = prime_power(q)
    if not ph:
        print(f"{q} is not a prime power")
        return 1
    p, h = ph
    poly, pts = None, []
    with open(args[1]) as fh:
        for ln, line in enumerate(fh, 1):
            line = line.split("#")[0].strip()
            if not line:
                continue
            tok = line.replace(",", " ").split()
            if tok[0] == "poly":
                if poly is not None or pts:
                    print(f"line {ln}: the poly line must come first, once")
                    return 1
                try:
                    poly = [int(t) for t in tok[1:]]
                except ValueError:
                    print(f"line {ln}: the coefficients must be integers")
                    return 1
                continue
            if len(tok) != 3:
                print(f"line {ln}: a point has three coordinates")
                return 1
            try:
                v = tuple(int(t) for t in tok)
            except ValueError:
                print(f"line {ln}: the coordinates must be integers")
                return 1
            if any(x < 0 or x >= q for x in v) or not any(v):
                print(f"line {ln}: coordinates must be in 0..{q - 1} and not all 0")
                return 1
            pts.append(v)
    if h > 1:
        if poly is None:
            print(f"GF({q}) = GF({p}^{h}): the first line must give the field's polynomial, poly c_0 ... c_{h}")
            return 1
        if len(poly) != h + 1 or poly[-1] != 1 or any(c < 0 or c >= p for c in poly):
            print(f"the polynomial must be monic of degree {h} with coefficients 0..{p - 1}")
            return 1
        if not irreducible(poly, p):
            print(f"the polynomial {poly} is not irreducible over GF({p})")
            return 1
    elif poly is not None and poly != [0, 1]:
        print(f"{q} is prime: no polynomial is needed (or give 'poly 0 1')")
        return 1
    n = len(pts)
    if n < 3:
        print("at least three points are needed")
        return 1
    kind = "1-saturating set" if saturating else "complete arc"
    work = (q + 2) * n * (n - 1) // 2
    print(f"PG(2,{q}), {n} points; about {work} steps")
    if work > max_work and "--brute" not in flags:
        print(f"refused: more than --max-work {max_work} steps")
        return 1
    F = Field(q, p, h, poly)
    if "--brute" in flags:
        ok, msg = check_brute(F, [F.normalize(v) for v in pts], saturating)
        normed = [F.normalize(v) for v in pts]
        if ok and len(set(normed)) != n:
            ok, msg = False, "two points are the same point of PG(2,q)"
    elif "--python" in flags or ("--native" not in flags and work <= NATIVE_FROM):
        normed = [F.normalize(v) for v in pts]
        if len(set(normed)) != n:
            ok, msg = False, "two points are the same point of PG(2,q)"
        else:
            ok, msg = check_python(F, normed, saturating)
    else:
        text = [f"{q} {p} {h} {1 if saturating else 0} {n}"]
        if h > 1:
            text.append(" ".join(map(str, F.exp)))
        text += [f"{a} {b} {c}" for a, b, c in pts]
        r = subprocess.run([helper()], input="\n".join(text) + "\n", capture_output=True, text=True)
        out = r.stdout.strip().splitlines()
        for line in out[:-1]:
            print("  " + line)
        last = out[-1] if out else "FAIL no output from arc_scan " + r.stderr
        ok, msg = last == f"OK {n}" and r.returncode == 0, last[5:] if last.startswith("FAIL") else last
    if not ok:
        print(f"NOT a {kind} of PG(2,{q}): {msg}")
        return 1
    print(f"{kind} of {n} points in PG(2,{q}) ({msg})")
    print(f"RESULT {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
