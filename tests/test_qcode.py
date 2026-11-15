"""Tests of checkers/qcode_check.py and its C helper qcode_enum.c (standard library only; run by test.sh).

- Known codes: the five-qubit code [[5,1,3]], Steane's [[7,1,3]], [[4,2,2]], the hexacode state [[6,0,4]], the cyclic
  five-qudit code [[5,1,3]] over GF(3), GF(5) and GF(7), and [[5,1,3]] over GF(4) and GF(8) given as two generators
  over GF(2) per generator.
- Random stabilizers over every field, small enough to list all of GF(Q)^(2N): the distance from the checker equals
  the distance found by brute force (every vector of the trace-symplectic dual tested directly).
- Larger random stabilizers: the weight counts listed by this program and by the C helper are identical.
- Red controls: a changed entry (generators that do not commute), a dropped and a repeated generator (wrong size),
  an entry out of range, a line of the wrong length.

  python3 -I tests/test_qcode.py"""
import os
import random
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "checkers"))
import qcode_check as qc  # noqa: E402

failures = []
TMP = tempfile.mkdtemp(prefix="qcode_test_")


def expect(label, got, want):
    ok = got == want
    print(f"{'ok   ' if ok else 'FAIL '} {label}: {got}" + ("" if ok else f" (expected {want})"))
    if not ok:
        failures.append(label)


def run(q, n, k, rows, extra=()):
    path = os.path.join(TMP, "code.txt")
    with open(path, "w") as f:
        for r in rows:
            f.write(" ".join(map(str, r[:n])) + " | " + " ".join(map(str, r[n:])) + "\n")
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "checkers", "qcode_check.py"), str(q), str(n), str(k),
                        path] + list(extra), capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    return r.returncode, last


def cyclic(xs, zs, n, shifts):
    rows = []
    for s in range(shifts):
        rows.append([xs[(i - s) % n] for i in range(n)] + [zs[(i - s) % n] for i in range(n)])
    return rows


def known():
    five = cyclic([1, 0, 0, 1, 0], [0, 1, 1, 0, 0], 5, 4)
    expect("[[5,1,3]] qubits", run(2, 5, 1, five), (0, "RESULT 3"))
    for q in (3, 5, 7):
        rows = cyclic([1, 0, 0, q - 1, 0], [0, 1, q - 1, 0, 0], 5, 4)
        expect(f"[[5,1,3]] over GF({q})", run(q, 5, 1, rows), (0, "RESULT 3"))
    for q in (4, 8):                        # GF(2)-generators g, x g, x^2 g, ... for each generator g of the binary code
        F = qc.Field(q)
        rows = []
        for g in five:
            c = 1
            for _ in range(F.e):
                rows.append([F.mul[c][a] for a in g])
                c = F.mul[c][2]
        expect(f"[[5,1,3]] over GF({q}) (additive generators)", run(q, 5, 1, rows), (0, "RESULT 3"))
        expect(f"[[5,1]] over GF({q}) given over GF(2) only: wrong size", run(q, 5, 1, five)[0], 1)
    ham = [[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]]
    steane = [h + [0] * 7 for h in ham] + [[0] * 7 + h for h in ham]
    expect("Steane [[7,1,3]]", run(2, 7, 1, steane), (0, "RESULT 3"))
    expect("[[4,2,2]]", run(2, 4, 2, [[1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1]]), (0, "RESULT 2"))
    # hexacode stabilizer state: GF(4)-linear [6,3,4] hexacode, X/Z from the two GF(2) coordinates of w-multiples
    F4 = qc.Field(4)
    hexa = [[1, 0, 0, 1, 2, 2], [0, 1, 0, 2, 1, 2], [0, 0, 1, 2, 2, 1]]       # 2 = x = w

    def to_xz(word):                       # GF(4) = {0,1,w,w^2} -> Pauli via a + b w  ->  X^a Z^b
        xs = [F4.dig[a][0] for a in word]
        zs = [F4.dig[a][1] for a in word]
        return xs + zs
    rows = []
    for g in hexa:
        rows.append(to_xz(g))
        rows.append(to_xz([F4.mul[2][a] for a in g]))
    expect("hexacode state [[6,0,4]]", run(2, 6, 0, rows), (0, "RESULT 4"))
    return five


def gram(F, n):
    """The trace-symplectic form on GF(p)^(2nm) (coordinate i: m digits of X_i then m of Z_i) as a matrix."""
    p, m = F.p, F.e
    L = 2 * n * m

    def unit(c):
        v = [0] * L
        v[c] = 1
        return v

    def to_field(v):
        x = [sum(v[i * 2 * m + j] * p ** j for j in range(m)) for i in range(n)]
        z = [sum(v[i * 2 * m + m + j] * p ** j for j in range(m)) for i in range(n)]
        return x, z

    def form(u, v):
        (a, b), (a2, b2) = to_field(u), to_field(v)
        s = 0
        for i in range(n):
            s = F.add[s][F.mul[a[i]][b2[i]]]
            s = F.add[s][F.neg[F.mul[a2[i]][b[i]]]]
        return F.trace[s]
    return [[form(unit(i), unit(j)) for j in range(L)] for i in range(L)], to_field


def kernel(rows, L, p):
    """A basis of {v : row . v = 0 for every row} over GF(p)."""
    rows = [r[:] for r in rows]
    piv_cols, R = [], []
    for r in rows:
        for pr, pc in zip(R, piv_cols):
            c = r[pc]
            if c:
                r = [(x - c * y) % p for x, y in zip(r, pr)]
        pc = next((i for i, x in enumerate(r) if x), None)
        if pc is None:
            continue
        inv = pow(r[pc], p - 2, p)
        r = [x * inv % p for x in r]
        for i, pr in enumerate(R):
            if pr[pc]:
                c = pr[pc]
                R[i] = [(x - c * y) % p for x, y in zip(pr, r)]
        R.append(r)
        piv_cols.append(pc)
    free = [c for c in range(L) if c not in piv_cols]
    basis = []
    for f in free:
        v = [0] * L
        v[f] = 1
        for pr, pc in zip(R, piv_cols):
            v[pc] = (-pr[f]) % p
        basis.append(v)
    return basis


def _rank(vecs, p):
    basis, piv = [], []
    for v in vecs:
        v = v[:]
        for b, pc in zip(basis, piv):
            if v[pc]:
                c = v[pc]
                v = [(x - c * y) % p for x, y in zip(v, b)]
        pc = next((i for i, x in enumerate(v) if x), None)
        if pc is None:
            continue
        inv = pow(v[pc], p - 2, p)
        basis.append([x * inv % p for x in v])
        piv.append(pc)
    return len(basis)


def random_stabilizer(F, n, r, rng):
    """r independent GF(p)-vectors, pairwise orthogonal in the trace-symplectic form."""
    p, m = F.p, F.e
    L = 2 * n * m
    G, to_field = gram(F, n)
    chosen = []
    while len(chosen) < r:
        cons = [[sum(c[i] * G[i][j] for i in range(L)) % p for j in range(L)] for c in chosen]
        ker = kernel(cons, L, p) if cons else [[int(i == j) for j in range(L)] for i in range(L)]
        v = [0] * L
        for b in ker:
            c = rng.randrange(p)
            v = [(x + c * y) % p for x, y in zip(v, b)]
        if any(v) and _rank(chosen + [v], p) == len(chosen) + 1:
            chosen.append(v)
    rows = []
    for v in chosen:
        x, z = to_field(v)
        rows.append(x + z)
    return chosen, rows, G


def brute_distance(F, n, k, chosen, G):
    p, m = F.p, F.e
    L = 2 * n * m
    best = None
    r0 = _rank(chosen, p)
    for idx in range(1, p ** L):
        v, t = [], idx
        for _ in range(L):
            v.append(t % p)
            t //= p
        if any(sum(v[i] * G[i][j] * c[j] for i in range(L) for j in range(L) if G[i][j] and c[j]) % p for c in chosen):
            continue                              # not in the dual
        if k > 0 and _rank(chosen + [v], p) == r0:
            continue                              # in S itself
        if k == 0 and _rank(chosen + [v], p) != r0:
            continue
        w = sum(1 for i in range(n) if any(v[i * 2 * m:(i + 1) * 2 * m]))
        best = w if best is None else min(best, w)
    return best


def random_small(rng):
    cases = [(2, 4, 1), (2, 4, 2), (2, 5, 1), (2, 5, 0), (2, 6, 2), (3, 3, 1), (3, 3, 0), (3, 4, 2), (5, 2, 0),
             (5, 3, 1), (4, 3, 1), (4, 2, 0), (8, 2, 1), (7, 2, 1)]
    for q, n, k in cases:
        F = qc.Field(q)
        r = F.e * (n - k)
        for trial in range(3 if q in (2, 3) else 2):
            chosen, rows, G = random_stabilizer(F, n, r, rng)
            want = brute_distance(F, n, k, chosen, G)
            got = run(q, n, k, rows, ["--python"])
            expect(f"random [[{n},{k}]] over GF({q}) #{trial}: distance against brute force", got, (0, f"RESULT {want}"))


def native_vs_python(rng):
    for q, n, k in ((2, 30, 12), (2, 40, 22), (3, 20, 10), (5, 12, 6), (7, 10, 5), (4, 16, 9), (8, 10, 5), (2, 70, 52)):
        F = qc.Field(q)
        r = F.e * (n - k)
        L = 2 * n * F.e
        # a random stabilizer with this rank: start from a random isotropic basis built greedily (cheap: CSS-like)
        chosen, rows, _ = random_stabilizer(F, n, r, rng) if L <= 80 else css_like(F, n, r, rng)
        basis = qc.prime_basis(F, rows, n)
        a = qc.weights_python(F.p, n, 2 * F.e, basis)
        b = qc.weights_native(F.p, n, 2 * F.e, basis)
        expect(f"[[{n},{k}]] over GF({q}): weight counts, Python = C", a == b, True)


def css_like(F, n, r, rng):
    """X-type generators from a random binary-like matrix, for a quick large isotropic set (Q = 2 only)."""
    rows = []
    while len(rows) < r:
        v = [rng.randrange(2) for _ in range(n)]
        cand = rows + [v + [0] * n]
        if _rank([c for c in cand], 2) == len(cand):
            rows.append(v + [0] * n)
    return None, rows, None


def red_controls(five):
    bad = [r[:] for r in five]
    bad[0][2] ^= 1
    expect("red: one entry changed (do not commute)", run(2, 5, 1, bad)[0], 1)
    expect("red: a generator dropped (wrong size)", run(2, 5, 1, five[:3])[0], 1)
    expect("red: a generator repeated (wrong size)", run(2, 5, 1, five[:3] + [five[0]])[0], 1)
    expect("red: [[5,1,3]] claimed as [[5,2]]", run(2, 5, 2, five)[0], 1)
    out = [r[:] for r in five]
    out[1][0] = 2
    expect("red: an entry out of range", run(2, 5, 1, out)[0], 1)
    path = os.path.join(TMP, "short.txt")
    with open(path, "w") as f:
        f.write("1 0 0 1 | 0 1 1 0\n")
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "checkers", "qcode_check.py"), "2", "5", "1", path],
                       capture_output=True, text=True)
    expect("red: a line of the wrong length", r.returncode, 1)
    expect("too large: exit status 2", run(2, 5, 1, five, ["--max-work", "4"])[0], 2)


if __name__ == "__main__":
    rng = random.Random(20261115)
    five = known()
    random_small(rng)
    native_vs_python(rng)
    red_controls(five)
    print(f"{'ALL OK' if not failures else str(len(failures)) + ' FAILED'}")
    sys.exit(1 if failures else 0)
