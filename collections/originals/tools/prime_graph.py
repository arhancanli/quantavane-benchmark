"""The graph of the n-digit primes joined when they differ in one digit, for tools/src/dominate.c (our own code,
Quantavane Originals, problem prime-cover).

  python3 -I prime_graph.py edges N OUT.edges          vertices: the n-digit primes in increasing order (0, 1, ...)
  python3 -I prime_graph.py primes N CODE.txt OUT.txt  vertex numbers written by dominate.c, back to the primes

EDGES: a first line "n m", then m lines "u v" (u < v). A code of radius 1 is a set of primes such that every n-digit
prime is in it or one digit away from one of its primes (the leading digit stays nonzero)."""
import sys


def primes(n):
    lo, hi = 10 ** (n - 1), 10 ** n
    sieve = bytearray([1]) * hi
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(hi ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [p for p in range(lo, hi) if sieve[p]]


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    mode, n = sys.argv[1], int(sys.argv[2])
    P = primes(n)
    idx = {p: i for i, p in enumerate(P)}
    if mode == "edges":
        E = []
        for i, p in enumerate(P):
            s = str(p)
            for k in range(n):
                for d in "0123456789":
                    if d != s[k] and not (k == 0 and d == "0"):
                        q = int(s[:k] + d + s[k + 1:])
                        if q in idx and idx[q] > i:
                            E.append((i, idx[q]))
        with open(sys.argv[3], "w") as f:
            f.write(f"{len(P)} {len(E)}\n" + "".join(f"{a} {b}\n" for a, b in E))
        return 0
    if mode == "primes":
        code = [int(t) for line in open(sys.argv[3]) if not line.startswith("#") for t in line.split()]
        with open(sys.argv[4], "w") as f:
            f.write(f"# covering code of radius 1 inside the {n}-digit primes: {len(code)} primes\n")
            f.write("".join(f"{P[v]}\n" for v in sorted(code)))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
