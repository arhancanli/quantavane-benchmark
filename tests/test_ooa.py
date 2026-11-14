"""Tests of checkers/ooa_check.py: known objects, red controls, and the two methods against a third program that works
from the definition (it counts every projection of the b^m runs). Run: python3 -I tests/test_ooa.py"""
import io, itertools, os, random, sys, tempfile, contextlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'checkers'))
import ooa_check as oc

def run(q, T, m, k, rows, way='both'):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        for r in rows: f.write(' '.join(map(str, r)) + '\n')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = oc.main([str(q), str(T), str(m), str(k), f.name, '--way', way])
    os.unlink(f.name)
    return code, buf.getvalue()

def by_definition(q, D, m, k, rows):
    """Strength k straight from the definition: every projection on the first d_i columns of each factor, sum k, uniform."""
    F = oc.Field(q); s = len(rows[0]) // D; t = min(D, k)
    words = []
    for x in itertools.product(range(q), repeat=m):
        w = [0] * len(rows[0])
        for c, row in zip(x, rows):
            if c: w = [F.add[a][F.mul[c][b]] for a, b in zip(w, row)]
        words.append(w)
    for d in itertools.product(range(t + 1), repeat=s):
        if sum(d) != k: continue
        idx = [i * D + j for i in range(s) for j in range(d[i])]
        seen = {}
        for w in words:
            key = tuple(w[c] for c in idx); seen[key] = seen.get(key, 0) + 1
        if len(seen) != q ** k or len(set(seen.values())) != 1: return False
    return True

checks = fails = 0
def expect(name, got, want):
    global checks, fails
    checks += 1
    if got != want:
        fails += 1; print('FAIL', name, 'got', got, 'want', want)

# 1. Hamming: the 7 nonzero binary columns of length 3: strength 2, not 3
ham = [[(c >> r) & 1 for c in range(1, 8)] for r in range(3)]
expect('hamming k=2', run(2, 1, 3, 2, ham)[0], 0); expect('hamming k=3', run(2, 1, 3, 3, ham)[0], 1)
code, out = run(2, 1, 3, 2, ham); expect('hamming result line', out.strip().splitlines()[-1], 'RESULT 7')
# 2. extended Hamming: columns (1, v), v in GF(2)^3: strength 3, not 4
ext = [[1] * 8] + [[(c >> r) & 1 for c in range(8)] for r in range(3)]
expect('ext hamming k=3', run(2, 1, 4, 3, ext)[0], 0); expect('ext hamming k=4', run(2, 1, 4, 4, ext)[0], 1)
# 3. Reed-Solomon over GF(5), 3 rows, 6 columns: strength 3 (MDS); one column doubled: fails
rs = [[1] * 5 + [0], list(range(5)) + [0], [a * a % 5 for a in range(5)] + [1]]
expect('RS5 k=3', run(5, 1, 3, 3, rs)[0], 0)
bad = [r[:] for r in rs]; 
for r in range(3): bad[r][5] = bad[r][0]
expect('RS5 repeated column', run(5, 1, 3, 3, bad)[0], 1)
# 4. Reed-Solomon over GF(9) and GF(16) (extension fields): all columns (1, a, a^2, a^3): strength 4
for q in (9, 16):
    F = oc.Field(q)
    rows = [[1] * q, list(range(q)), [F.mul[a][a] for a in range(q)], [F.mul[a][F.mul[a][a]] for a in range(q)]]
    expect(f'RS{q} k=4', run(q, 1, 4, 4, rows)[0], 0)
    rows2 = [r[:] for r in rows]; rows2[3][2] = F.add[rows2[3][2]][1]
    expect(f'RS{q} one entry changed', run(q, 1, 4, 4, rows2)[0], by_definition(q, 1, 4, 4, rows2) and 0 or 1)
# 5. a digital (0,4,2)-net in base 2: identity and reversal; the same matrix twice is not a net
m = 4
ident = [[1 if r == c else 0 for c in range(m)] for r in range(m)]            # row j of C_1
rev = [[1 if r == m - 1 - c else 0 for c in range(m)] for r in range(m)]      # row j of C_2
G = [[ident[j][r] for j in range(m)] + [rev[j][r] for j in range(m)] for r in range(m)]   # column (i, j) = row j of C_i
expect('(0,4,2)-net', run(2, 'net', 4, 4, G)[0], 0)
G2 = [[ident[j][r] for j in range(m)] + [ident[j][r] for j in range(m)] for r in range(m)]
expect('same matrix twice', run(2, 'net', 4, 4, G2)[0], 1)
# 6. malformed inputs
expect('entry too large', run(2, 1, 3, 2, [[0, 1, 2], [1, 0, 1], [1, 1, 0]])[0], 1)
expect('columns not a multiple of the depth', run(2, 2, 3, 2, [[0, 1, 1], [1, 0, 1], [1, 1, 0]])[0], 1)
expect('too few factors', run(2, 1, 3, 3, [[1, 0], [0, 1], [1, 1]])[0], 1)
# 7. random objects: D, E and the definition must agree
rng = random.Random(20261114)
agree = passed = 0
for trial in range(600):
    q = rng.choice([2, 2, 3, 4, 5, 7, 8, 9, 16])
    m = rng.randint(2, 5 if q <= 3 else (4 if q <= 5 else 3))
    k = rng.randint(1, m)
    T = rng.choice([1, 2, 3, 'net'])
    D = k if T == 'net' else T
    t = min(D, k)
    s = rng.randint(-(-k // t), -(-k // t) + 3)
    if q ** m * s * D > 40000 or (t + 1) ** s > 3000: continue
    rows = [[rng.randrange(q) for _ in range(s * D)] for _ in range(m)]
    if rng.random() < 0.5:                                      # help it pass sometimes: start from an identity
        for r in range(m):
            for c in range(min(m, s * D)): rows[r][c] = 1 if r == c else 0
    cd, _ = run(q, T, m, k, rows, 'D'); ce, _ = run(q, T, m, k, rows, 'E'); df = by_definition(q, D, m, k, rows)
    agree += 1; passed += df
    expect(f'random {trial} q={q} T={T} m={m} k={k} s={s}', (cd, ce), (0 if df else 1,) * 2)
print(f'random objects compared: {agree} ({passed} with the strength asked for, {agree - passed} without)')
print(f'{checks} checks, {fails} failed')
sys.exit(1 if fails else 0)
