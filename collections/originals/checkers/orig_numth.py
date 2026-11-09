"""Exact checkers for the number theory problems of the Quantavane Originals (standard library only).

  python3 -I orig_numth.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved); it exits 0 only for a
valid certificate and 1 otherwise. Problems:

  gauss-admissible RING K FILE   FILE: K lattice points "x y", one per line (x + y*i in Z[i] for RING 4, x + y*w in
                                 Z[w], w = (-1 + sqrt(-3))/2, for RING 3). Valid when the points are distinct and, for
                                 every prime ideal P of norm at most K, they miss a residue class modulo P (admissible;
                                 prime ideals of larger norm cannot be covered by K points). Value: the diameter, the
                                 largest squared distance x^2 + y^2 (RING 4) or x^2 - xy + y^2 (RING 3) between two
                                 points.
  quad-admissible K FILE         FILE: K distinct positive integers h (separated by spaces or newlines). Valid when
                                 the polynomials n^2 + h are admissible: for every prime p some integer n makes every
                                 n^2 + h nonzero modulo p, i.e. the residues -h (mod p) miss one of the (p+1)/2
                                 values of n^2 (mod p), 0 included (only p <= 2K - 1 can fail). Value: the largest
                                 element of the set.
  cubic-admissible K FILE        the same for the cubic family n^3 + h: the residues -h (mod p) must miss one of the
                                 values of n^3 (mod p), 0 included (all p residues when p = 3 or p = 2 mod 3, (p+2)/3
                                 of them when p = 1 mod 3); only p <= 3K - 2 can fail. Value: the largest element.
  qr-sumfree P FILE              FILE: distinct nonzero squares modulo the prime P (integers in 1..P-1). Valid when no
                                 three of them, not necessarily distinct, satisfy a + b = c (mod P). Value: the number
                                 of elements.
  eisenstein-triples FILE        FILE: a string of n characters 0 and 1 (lines starting with # are skipped), the
                                 colours of 1, 2, ..., n. Valid when no triple x < y, z <= n with x^2 + xy + y^2 = z^2
                                 (the sides of a triangle with a 120-degree angle) has x, y and z of the same colour.
                                 Every triple is found from the factorisations u v = 3 x^2 with u = 2z - (2y + x),
                                 v = 2z + (2y + x). Value: n.
  gauss-prime-ap N FILE          FILE: lines "x y", the Gaussian integers x + yi of an arithmetic progression in
                                 order (at least 3 terms). Valid when the terms are distinct, the differences of
                                 consecutive terms are all equal and every term is a Gaussian prime of norm at most N:
                                 x^2 + y^2 is a prime when x and y are both nonzero, and |x + yi| is a prime congruent
                                 to 3 mod 4 when one of them is 0 (deterministic Miller-Rabin for large numbers).
                                 Value: the number of terms."""
import sys


def ints(path):
    rows = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].strip()
        if line:
            rows.append([int(t) for t in line.replace(",", " ").split()])
    return rows


def isprime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def prime_ideals(ring, kmax):
    """Prime ideals of norm <= kmax of Z[i] (ring 4) or Z[w] (ring 3), as (norm, name, residue function)."""
    out = []
    for p in range(2, kmax + 1):
        if not isprime(p):
            continue
        ram = 2 if ring == 4 else 3
        split = (p % 4 == 1) if ring == 4 else (p % 3 == 1)
        if p == ram:
            out.append((p, f"({'1+i' if ring == 4 else '1-w'})", lambda x, y, p=p: (x + y) % p))
        elif split:
            if ring == 4:
                r = next(a for a in range(2, p) if (a * a + 1) % p == 0)
                roots = [r, p - r]
            else:
                r = next(a for a in range(2, p) if (a * a + a + 1) % p == 0)
                roots = [r, (r * r) % p]
            for r in roots:   # the ideal (p, u - r): x + y*u has residue x + y*r mod p
                out.append((p, f"({p}, {'i' if ring == 4 else 'w'}-{r})", lambda x, y, p=p, r=r: (x + y * r) % p))
        elif p * p <= kmax:
            out.append((p * p, f"({p})", lambda x, y, p=p: (x % p, y % p)))
    return out


def gauss_admissible(args, path):
    ring, k = int(args[0]), int(args[1])
    if ring not in (3, 4):
        print("RING must be 4 (Gaussian integers) or 3 (Eisenstein integers)")
        return 1
    rows = ints(path)
    if any(len(r) != 2 for r in rows):
        print("each line must hold two integers x y")
        return 1
    pts = [tuple(r) for r in rows]
    if len(pts) != k or len(set(pts)) != k:
        print(f"{len(pts)} points ({len(set(pts))} distinct), expected {k} distinct points")
        return 1
    for norm, name, res in prime_ideals(ring, k):
        classes = {res(x, y) for x, y in pts}
        if len(classes) == norm:
            print(f"not admissible: the points cover all {norm} residue classes modulo the prime ideal {name}")
            return 1
    nrm = (lambda x, y: x * x + y * y) if ring == 4 else (lambda x, y: x * x - x * y + y * y)
    diam = max((nrm(a[0] - b[0], a[1] - b[1]) for i, a in enumerate(pts) for b in pts[i + 1:]), default=0)
    print(f"{k} distinct points of {'Z[i]' if ring == 4 else 'Z[w]'}, admissible: each of the "
          f"{len(prime_ideals(ring, k))} prime ideals of norm <= {k} misses a residue class; diameter {diam}")
    print(f"RESULT {diam}")
    return 0


def quad_admissible(args, path):
    k = int(args[0])
    hs = [int(t) for t in " ".join(line.split("#")[0] for line in open(path, encoding="ascii", errors="replace")).split()]
    if len(hs) != k or len(set(hs)) != k or min(hs) < 1:
        print(f"expected {k} distinct positive integers")
        return 1
    for p in range(2, max(3, 2 * k)):
        if not isprime(p):
            continue
        squares = {x * x % p for x in range(p)}
        if squares <= {(-h) % p for h in hs}:
            print(f"not admissible: modulo {p} some n^2 + h is divisible by {p} for every n")
            return 1
    print(f"{k} shifts h: the polynomials n^2 + h are admissible (every prime p <= {2 * k - 1} checked); "
          f"largest shift {max(hs)}")
    print(f"RESULT {max(hs)}")
    return 0


def cubic_admissible(args, path):
    k = int(args[0])
    hs = [int(t) for t in " ".join(line.split("#")[0] for line in open(path, encoding="ascii", errors="replace")).split()]
    if len(hs) != k or len(set(hs)) != k or min(hs) < 1:
        print(f"expected {k} distinct positive integers")
        return 1
    for p in range(2, max(3, 3 * k - 1)):
        if not isprime(p):
            continue
        cubes = {x ** 3 % p for x in range(p)}
        if cubes <= {(-h) % p for h in hs}:
            print(f"not admissible: modulo {p} some n^3 + h is divisible by {p} for every n")
            return 1
    print(f"{k} shifts h: the polynomials n^3 + h are admissible (every prime p <= {3 * k - 2} checked); "
          f"largest shift {max(hs)}")
    print(f"RESULT {max(hs)}")
    return 0


def qr_sumfree(args, path):
    p = int(args[0])
    if not isprime(p) or p < 3:
        print("P must be an odd prime")
        return 1
    A = [int(t) for t in " ".join(line.split("#")[0] for line in open(path, encoding="ascii", errors="replace")).split()]
    S = set(A)
    squares = {x * x % p for x in range(1, p)}
    if len(S) != len(A) or not S <= squares:
        print("the elements must be distinct nonzero squares modulo P")
        return 1
    for a in S:
        for b in S:
            if (a + b) % p in S:
                print(f"{a} + {b} = {(a + b) % p} (mod {p}): not sum-free")
                return 1
    print(f"{len(S)} quadratic residues modulo {p} with no solution of a + b = c among them")
    print(f"RESULT {len(S)}")
    return 0


def eisenstein_triples_upto(n):
    """All (x, y, z) with x < y, z <= n and x^2 + xy + y^2 = z^2: for each x, every factorisation 3 x^2 = u v with
    u < v and u + v = 0 mod 4 gives z = (u + v)/4 and y = ((v - u)/2 - x)/2 (kept when it is an integer > x)."""
    spf = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    out = []
    for x in range(1, n + 1):
        f, m = {3: 1}, x
        while m > 1:
            p = spf[m]
            m //= p
            f[p] = f.get(p, 0) + 2
        divs = [1]
        for p, e in f.items():
            divs = [d * p ** k for d in divs for k in range(e + 1)]
        N = 3 * x * x
        for u in divs:
            v = N // u
            if u >= v or (u + v) % 4:
                continue
            z, t = (u + v) // 4, (v - u) // 2 - x
            if z <= n and t > 0 and t % 2 == 0 and t // 2 > x:
                out.append((x, t // 2, z))
    return out


def eisenstein_triples(args, path):
    text = "".join("".join(l.split()) for l in open(path, encoding="ascii", errors="replace") if not l.startswith("#"))
    if not text or set(text) - {"0", "1"}:
        print("the colouring must be a nonempty string of 0 and 1")
        return 1
    n = len(text)
    T = eisenstein_triples_upto(n)
    for x, y, z in T:
        if text[x - 1] == text[y - 1] == text[z - 1]:
            print(f"monochromatic triple {x}^2 + {x}*{y} + {y}^2 = {z}^2 (colour {text[x - 1]})")
            return 1
    print(f"colouring of 1..{n}: none of the {len(T)} triples x^2 + xy + y^2 = z^2 with z <= {n} is monochromatic")
    print(f"RESULT {n}")
    return 0


def isprime_mr(n):
    """Deterministic Miller-Rabin for n < 3.3 * 10^24 (the first 12 primes as bases)."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def is_gaussian_prime(x, y):
    if x != 0 and y != 0:
        return isprime_mr(x * x + y * y)
    a = abs(x) + abs(y)
    return isprime_mr(a) and a % 4 == 3


def gauss_prime_ap(args, path):
    bound = int(args[0])
    rows = ints(path)
    k = len(rows)
    if k < 3 or any(len(r) != 2 for r in rows):
        print("expected at least 3 lines 'x y'")
        return 1
    dx, dy = rows[1][0] - rows[0][0], rows[1][1] - rows[0][1]
    if (dx, dy) == (0, 0) or any((rows[j + 1][0] - rows[j][0], rows[j + 1][1] - rows[j][1]) != (dx, dy) for j in range(k - 1)):
        print("the terms are not a progression with a nonzero common difference")
        return 1
    for x, y in rows:
        if x * x + y * y > bound:
            print(f"{x}{y:+d}i has norm {x * x + y * y} > {bound}")
            return 1
        if not is_gaussian_prime(x, y):
            print(f"{x}{y:+d}i is not a Gaussian prime (norm {x * x + y * y})")
            return 1
    m = max(x * x + y * y for x, y in rows)
    print(f"{k} Gaussian primes in arithmetic progression, first term {rows[0][0]}{rows[0][1]:+d}i, difference {dx}{dy:+d}i; largest norm {m} <= {bound}")
    print(f"RESULT {k}")
    return 0

PROBLEMS = {"gauss-admissible": (2, gauss_admissible), "quad-admissible": (1, quad_admissible),
            "cubic-admissible": (1, cubic_admissible), "qr-sumfree": (1, qr_sumfree),
            "eisenstein-triples": (0, eisenstein_triples), "gauss-prime-ap": (1, gauss_prime_ap)}


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in PROBLEMS:
        print(__doc__)
        return 2
    nargs, fn = PROBLEMS[sys.argv[1]]
    if len(sys.argv) != 3 + nargs:
        print(__doc__)
        return 2
    try:
        return fn(sys.argv[2:-1], sys.argv[-1])
    except (ValueError, OSError) as e:
        print(f"unreadable certificate: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
