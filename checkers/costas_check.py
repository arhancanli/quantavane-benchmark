"""Exact check of a Costas array (standard library only).

  python3 -I costas_check.py N FILE

FILE holds a permutation of 1..N (or of 0..N-1): N integers separated by spaces, commas or newlines; the i-th number
is the row of the dot in column i. A Costas array of order N is an N x N permutation matrix in which the vectors
joining pairs of dots are all distinct: for every horizontal shift d = 1..N-1, the vertical differences p(i+d) - p(i)
are pairwise distinct. The checker tests all N(N-1)/2 vectors. Prints the order and "RESULT 1" (a Costas array of
order N exists); exits 0 for a Costas array of order N, 1 otherwise."""
import sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    n = int(sys.argv[1])
    vals = []
    for line in open(sys.argv[2], encoding="ascii", errors="replace"):
        s = line.split("#")[0].replace(",", " ").split()
        try:
            vals.extend(int(x) for x in s)
        except ValueError:
            print(f"not a list of integers: {line.strip()[:60]!r}")
            return 1
    if len(vals) != n:
        print(f"{len(vals)} numbers, expected {n}")
        return 1
    if sorted(vals) == list(range(1, n + 1)):
        p = [v - 1 for v in vals]
    elif sorted(vals) == list(range(n)):
        p = vals
    else:
        print(f"not a permutation of 1..{n} or of 0..{n - 1}")
        return 1
    for d in range(1, n):
        seen = set()
        for i in range(n - d):
            diff = p[i + d] - p[i]
            if diff in seen:
                print(f"shift {d}: the vertical difference {diff} occurs twice (column {i + 1 + d} and an earlier one)")
                return 1
            seen.add(diff)
    print(f"order {n}: all {n * (n - 1) // 2} displacement vectors are distinct")
    print("RESULT 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
