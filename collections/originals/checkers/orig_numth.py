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
  qr-sumfree P FILE              FILE: distinct nonzero squares modulo the prime P (integers in 1..P-1). Valid when no
                                 three of them, not necessarily distinct, satisfy a + b = c (mod P). Value: the number
                                 of elements."""
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


PROBLEMS = {"gauss-admissible": (2, gauss_admissible), "quad-admissible": (1, quad_admissible),
            "qr-sumfree": (1, qr_sumfree)}


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
