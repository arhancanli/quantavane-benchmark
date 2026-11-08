"""Exact check of an independent set in the strong power C_M^K of a cycle (standard library only).

  python3 -I strongpow_check.py M K FILE

FILE holds the vertices, one per line (or separated by whitespace), each written as K digits from 0 to M-1 (M <= 10)
with nothing between them. Two distinct vertices of the strong power are adjacent when in every coordinate they are
equal or adjacent on the cycle C_M (differ by 1 mod M). For every vertex the checker looks up its 3^K - 1 neighbours.
An independent set of size a shows alpha(C_M^K) >= a and Shannon capacity >= a^(1/K). Prints the size and
"RESULT a"; exits 0 for an independent set, 1 otherwise."""
import itertools
import sys


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    m, k = int(sys.argv[1]), int(sys.argv[2])
    if not (3 <= m <= 10 and k >= 1):
        print("M must be 3..10 and K at least 1")
        return 2
    words = "\n".join(line.split("#")[0] for line in open(sys.argv[3], encoding="ascii", errors="replace")).split()
    for w in words:
        if len(w) != k or any(c not in "0123456789"[:m] for c in w):
            print(f"{w[:40]!r} is not {k} digits from 0 to {m - 1}")
            return 1
    have = set(words)
    if len(have) != len(words):
        print("a vertex is repeated")
        return 1
    steps = [s for s in itertools.product((0, 1, m - 1), repeat=k) if any(s)]
    for w in words:
        v = [int(c) for c in w]
        for s in steps:
            u = "".join(str((a + b) % m) for a, b in zip(v, s))
            if u in have:
                print(f"{w} and {u} are adjacent in C_{m}^{k}")
                return 1
    print(f"independent set of {len(words)} vertices in the strong power C_{m}^{k}")
    print(f"RESULT {len(words)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
