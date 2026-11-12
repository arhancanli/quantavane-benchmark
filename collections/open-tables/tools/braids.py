"""Braid words for the unknotting table (standard library only): closures, the Alexander polynomial from the reduced
Burau representation, a fast unknot filter, and moves written in the format of checkers/unknot_check.py.

A braid word is a list of non-zero integers (i for sigma_i, -i for its inverse) on n strands. Every function that
changes a word appends the moves it made to a list `log` of certificate lines, so that the checker can replay them."""
import random

# ---------------------------------------------------------------- the Alexander polynomial (exact, Laurent)


def lp_add(a, b, s=1):
    out = dict(a)
    for e, c in b.items():
        out[e] = out.get(e, 0) + s * c
        if out[e] == 0:
            del out[e]
    return out


def lp_mul(a, b):
    out = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            out[e1 + e2] = out.get(e1 + e2, 0) + c1 * c2
    return {e: c for e, c in out.items() if c}


def burau_generator(i, sign, m):
    """The reduced Burau matrix (m = n - 1) of sigma_i (sign 1) or its inverse (sign -1), as a dict {(r, c): lp}.
    Convention: sigma_i acts on the basis by a 3 x 3 block at rows/columns i-2, i-1, i (0-based), cut at the edges."""
    one, t, mt = {0: 1}, {1: 1}, {1: -1}
    ti, mti = {-1: 1}, {-1: -1}
    g = {(r, r): one for r in range(m)}
    k = i - 1                                   # 0-based row of the generator's own basis vector
    if sign > 0:                                # block [[1, t, 0], [0, -t, 0], [0, 1, 1]] centred at k
        g[(k, k)] = mt
        if k - 1 >= 0:
            g[(k - 1, k)] = t
        if k + 1 < m:
            g[(k + 1, k)] = one
    else:                                       # the inverse block [[1, 1, 0], [0, -1/t, 0], [0, 1/t, 1]]
        g[(k, k)] = mti
        if k - 1 >= 0:
            g[(k - 1, k)] = one
        if k + 1 < m:
            g[(k + 1, k)] = ti
    return g


def mat_mul(A, B, m):
    out = {}
    for (r, k), a in A.items():
        for c in range(m):
            b = B.get((k, c))
            if b:
                cur = lp_add(out.get((r, c), {}), lp_mul(a, b))
                if cur:
                    out[(r, c)] = cur
                elif (r, c) in out:
                    del out[(r, c)]
    return out


def det(M, m):
    """Determinant of an m x m matrix of Laurent polynomials (expansion along rows, memoised on used columns)."""
    memo = {}

    def f(r, used):
        if r == m:
            return {0: 1}
        if (r, used) in memo:
            return memo[(r, used)]
        acc, sign = {}, 1
        for c in range(m):
            if used >> c & 1:
                continue
            s = (-1) ** bin(used & ((1 << c) - 1)).count("1")
            e = M.get((r, c))
            if e:
                acc = lp_add(acc, lp_mul(e, f(r + 1, used | 1 << c)), s)
        memo[(r, used)] = acc
        return acc
    return f(0, 0)


def lp_divexact(a, b):
    """a / b for Laurent polynomials when b divides a exactly (b with leading coefficient +-1)."""
    a, q = dict(a), {}
    bmax, bmin = max(b), min(b)
    lowest = min(a) - bmin if a else 0
    while a:
        amax = max(a)
        c, r = divmod(a[amax], b[bmax])
        if r or amax - bmax < lowest:
            raise ValueError("not divisible")
        q[amax - bmax] = c
        a = lp_add(a, lp_mul({amax - bmax: c}, b), -1)
    return q


def normalize(p):
    """p * (+-t^k) with lowest exponent 0 and positive constant term: the normal form of an Alexander polynomial."""
    lo = min(p)
    p = {e - lo: c for e, c in p.items()}
    if p[0] < 0:
        p = {e: -c for e, c in p.items()}
    return p


def alexander(w, n):
    """The Alexander polynomial of the closure of w (a knot), normalized, as a coefficient list from t^0 up."""
    m = n - 1
    if m == 0:
        return [1]
    M = {(r, r): {0: 1} for r in range(m)}
    for x in w:
        M = mat_mul(M, burau_generator(abs(x), 1 if x > 0 else -1, m), m)
    IM = {}
    for r in range(m):
        for c in range(m):
            e = lp_add({0: 1} if r == c else {}, M.get((r, c), {}), -1)
            if e:
                IM[(r, c)] = e
    d = det(IM, m)
    q = normalize(lp_divexact(d, {k: 1 for k in range(n)}))
    return [q.get(e, 0) for e in range(max(q) + 1)]


# ---------------------------------------------------------------- a fast unknot filter (Burau at t0 modulo a prime)

P = (1 << 61) - 1


class Filter:
    """Delta(t0) modulo P for a few values t0: the closure can be the unknot only if Delta(t0) = +-t0^k."""

    def __init__(self, n, max_len, t0s=(2, 3, 1234567891)):
        self.n, self.t0s = n, t0s
        self.ok = []
        for t0 in t0s:
            s = (pow(t0, n, P) - 1) * pow(t0 - 1, P - 2, P) % P      # 1 + t0 + ... + t0^(n-1)
            allowed = set()
            for k in range(-2 * max_len - n, 2 * max_len + n + 1):
                v = pow(t0, k % (P - 1), P)
                allowed.add(v * s % P)
                allowed.add((-v * s) % P)
            self.ok.append(allowed)

    def maybe_unknot(self, w):
        m = self.n - 1
        if m == 0:
            return True
        for t0, allowed in zip(self.t0s, self.ok):
            ti = pow(t0, P - 2, P)
            M = [[int(r == c) for c in range(m)] for r in range(m)]
            for x in w:
                k = abs(x) - 1
                # right-multiply M by the generator: only column k changes (it depends on columns k-1, k, k+1)
                if x > 0:
                    for r in range(m):
                        row = M[r]
                        v = -t0 * row[k]
                        if k - 1 >= 0:
                            v += row[k - 1] * t0
                        if k + 1 < m:
                            v += row[k + 1]
                        row[k] = v % P
                else:
                    for r in range(m):
                        row = M[r]
                        v = -ti * row[k]
                        if k - 1 >= 0:
                            v += row[k - 1]
                        if k + 1 < m:
                            v += row[k + 1] * ti
                        row[k] = v % P
            A = [[((r == c) - M[r][c]) % P for c in range(m)] for r in range(m)]
            d = 1
            for c in range(m):
                piv = next((r for r in range(c, m) if A[r][c]), None)
                if piv is None:
                    d = 0
                    break
                if piv != c:
                    A[c], A[piv] = A[piv], A[c]
                    d = -d
                d = d * A[c][c] % P
                inv = pow(A[c][c], P - 2, P)
                for r in range(c + 1, m):
                    if A[r][c]:
                        f = A[r][c] * inv % P
                        A[r] = [(a - f * b) % P for a, b in zip(A[r], A[c])]
            if d % P not in allowed:
                return False
        return True


# ---------------------------------------------------------------- moves (each appends certificate lines to log)


def components(w, n):
    perm = list(range(n))
    for x in w:
        i = abs(x) - 1
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
    seen, cyc = [False] * n, 0
    for s in range(n):
        if not seen[s]:
            cyc += 1
            j = s
            while not seen[j]:
                seen[j] = True
                j = perm[j]
    return cyc


class Braid:
    def __init__(self, w, n, log=None):
        self.w, self.n = list(w), n
        self.log = [] if log is None else log

    def copy(self):
        return Braid(self.w, self.n, list(self.log))

    def X(self, p):
        self.w[p] = -self.w[p]
        self.log.append(f"X {p}")

    def I(self, p, a):
        self.w[p:p] = [a, -a]
        self.log.append(f"I {p} {a}")

    def D(self, p):
        assert self.w[p + 1] == -self.w[p]
        del self.w[p:p + 2]
        self.log.append(f"D {p}")

    def C(self, p):
        assert abs(abs(self.w[p]) - abs(self.w[p + 1])) >= 2
        self.w[p], self.w[p + 1] = self.w[p + 1], self.w[p]
        self.log.append(f"C {p}")

    def B(self, p):
        a, b, c = self.w[p:p + 3]
        assert a == c and abs(abs(a) - abs(b)) == 1 and (a > 0) == (b > 0)
        self.w[p:p + 3] = [b, a, b]
        self.log.append(f"B {p}")

    def R(self, k):
        k %= max(1, len(self.w))
        if k:
            self.w = self.w[k:] + self.w[:k]
            self.log.append(f"R {k}")

    def F(self):
        self.w = [(self.n - abs(x)) * (1 if x > 0 else -1) for x in self.w]
        self.log.append("F")

    def S(self, e):
        self.w.append(e * self.n)
        self.n += 1
        self.log.append(f"S {e}")

    def U(self):
        assert abs(self.w[-1]) == self.n - 1 and all(abs(x) != self.n - 1 for x in self.w[:-1])
        self.w.pop()
        self.n -= 1
        self.log.append("U")

    # derived moves, written as primitive ones

    def mixed(self, p):
        """a b -a -> -b a b, or -a b a -> b a -b (a, b of one sign, adjacent indices): a braid relation with a pair
        inserted and deleted. Returns False when w[p:p+3] has neither form."""
        if p + 3 > len(self.w):
            return False
        a, b, c = self.w[p:p + 3]
        if abs(abs(a) - abs(b)) != 1 or c != -a:
            return False
        if (a > 0) == (b > 0):                  # a b -a -> -b a b
            self.I(p, -b)
            self.B(p + 1)
            self.D(p + 3)
            return True
        if (-a > 0) == (b > 0):                 # -a b a, written with A = -a: A b -A where A, b have one sign
            # here w = [x, b, -x] with x = a of the other sign than b: -x b x with -x, b of one sign
            self.I(p + 3, b)
            self.B(p + 1)
            self.D(p)
            return True
        return False

    def reduce(self):
        """Free and cyclic reduction, cancellation across commuting letters, destabilization; True if it changed."""
        changed = False
        while True:
            w = self.w
            done = False
            for p in range(len(w) - 1):
                if w[p + 1] == -w[p]:
                    self.D(p)
                    done = True
                    break
            if done:
                changed = True
                continue
            if len(w) >= 2 and w[0] == -w[-1]:
                self.R(len(w) - 1)
                self.D(0)
                changed = True
                continue
            # a letter and its inverse separated only by letters that commute with it
            for p in range(len(w)):
                i = abs(w[p])
                q = p + 1
                while q < len(w) and abs(abs(w[q]) - i) >= 2:
                    q += 1
                if q < len(w) and w[q] == -w[p] and q > p + 1:
                    for r in range(q - 1, p, -1):
                        self.C(r)
                    self.D(p)
                    done = True
                    break
            if done:
                changed = True
                continue
            if self.destabilize():
                changed = True
                continue
            return changed

    def destabilize(self):
        if self.n < 2:
            return False
        for flip in (False, True):
            top = self.n - 1
            pos = [p for p, x in enumerate(self.w) if abs(x) == top]
            if len(pos) == 1:
                self.R(pos[0] + 1)
                self.U()
                return True
            if not pos:                          # the last strand is a split unknot: cannot happen for a knot
                return False
            if not flip:
                low = [p for p, x in enumerate(self.w) if abs(x) == 1]
                if len(low) == 1 and self.n > 2:
                    self.F()
                    continue
            break
        return False

    def random_neutral(self, rng):
        """One random move that keeps the closure (commutation, braid relation, mixed relation, conjugation)."""
        w = self.w
        L = len(w)
        if L < 2:
            return
        kind = rng.random()
        if kind < 0.15:
            self.R(rng.randrange(1, L))
            return
        if kind < 0.18 and self.n > 2:
            self.F()
            return
        opts = []
        for p in range(L - 1):
            if abs(abs(w[p]) - abs(w[p + 1])) >= 2:
                opts.append(("C", p))
        for p in range(L - 2):
            a, b, c = w[p:p + 3]
            if a == c and abs(abs(a) - abs(b)) == 1 and (a > 0) == (b > 0):
                opts.append(("B", p))
            if c == -a and abs(abs(a) - abs(b)) == 1:
                opts.append(("M", p))
        if not opts:
            self.R(rng.randrange(1, L))
            return
        op, p = rng.choice(opts)
        if op == "C":
            self.C(p)
        elif op == "B":
            self.B(p)
        else:
            self.mixed(p)

    def random_grow(self, rng):
        """A random move that keeps the closure and adds crossings: a cancelling pair or a stabilization."""
        if rng.random() < 0.7 or self.n >= 9:
            p = rng.randrange(len(self.w) + 1)
            a = rng.randrange(1, self.n) * rng.choice((1, -1))
            self.I(p, a)
        else:
            self.S(rng.choice((1, -1)))


def simplify(br, rng, budget=4000):
    """Try to bring a closed braid to the empty word on one strand; True on success (br.log holds the moves)."""
    best = len(br.w) + 2 * br.n
    stall = 0
    for _ in range(budget):
        br.reduce()
        if not br.w and br.n == 1:
            return True
        size = len(br.w) + 2 * br.n
        if size < best:
            best, stall = size, 0
        else:
            stall += 1
            if stall > 600:
                return False
        br.random_neutral(rng)
    return False


# ---------------------------------------------------------------- the Jones polynomial (Temperley-Lieb transfer)


def jones(w, n):
    """The Jones polynomial of the closure of w as {exponent of t: coefficient} (exponents may be halves for links;
    for a knot they are integers). Kauffman bracket through planar matchings of the 2n ends, level by level:
    sigma_i = A + A^-1 e_i and sigma_i^-1 = A^-1 + A e_i; then V(t) = (-A^3)^-w <D> with t = A^-4."""
    d = {2: -1, -2: -1}                                   # -A^2 - A^-2
    start = tuple(list(range(n, 2 * n)) + list(range(n)))
    states = {start: {0: 1}}
    for x in w:
        i = abs(x) - 1
        a_id, a_e = (1, -1) if x > 0 else (-1, 1)        # exponents of A on the identity and on e_i
        new = {}
        for m, coef in states.items():
            # identity smoothing: the matching is unchanged
            new[m] = lp_add(new.get(m, {}), lp_mul(coef, {a_id: 1}))
            # e_i: join the partners of bottom points i and i+1 (or close a loop), then cap them together
            p, q = n + i, n + i + 1
            mm = list(m)
            f = {a_e: 1}
            if mm[p] == q:
                f = lp_mul(f, d)
            else:
                a, b = mm[p], mm[q]
                mm[a], mm[b] = b, a
            mm[p], mm[q] = q, p
            key = tuple(mm)
            new[key] = lp_add(new.get(key, {}), lp_mul(coef, f))
        states = {k: v for k, v in new.items() if v}
    bracket = {}
    for m, coef in states.items():
        seen, loops = [False] * (2 * n), 0
        for s in range(2 * n):
            if not seen[s]:
                loops += 1
                j = s
                while not seen[j]:
                    seen[j] = True
                    k = m[j]                             # along the matching
                    seen[k] = True
                    j = k + n if k < n else k - n        # along the closure strand
        term = coef
        for _ in range(loops - 1):
            term = lp_mul(term, d)
        bracket = lp_add(bracket, term)
    writhe = sum(1 if x > 0 else -1 for x in w)
    pre = {-3 * writhe: (-1) ** (writhe % 2)}            # (-A^3)^-w
    poly = lp_mul(pre, bracket)
    out = {}
    for e, c in poly.items():                             # A^e = t^(-e/4)
        out[-e / 4] = c
    return {(int(k) if k == int(k) else k): v for k, v in sorted(out.items())}
