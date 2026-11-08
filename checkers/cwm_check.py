"""Exact check of a proper circulant weighing matrix CW(N, K) (standard library only).

  python3 -I cwm_check.py N K FILE

FILE holds the first row, N entries -1, 0 or 1 separated by spaces or commas (or written as the characters -, 0 and
+). The circulant matrix W with this first row has W W^T = K I exactly when the row has K nonzero entries and its
periodic autocorrelation vanishes at every shift 1..N-1. It is proper, as in Gordon's La Jolla repository, when its
support is not inside a coset of a proper subgroup of Z_N (the gcd of N and the differences of the support is 1); an
improper one comes from a smaller order. Prints the result and "RESULT 1" (a proper CW(N, K) exists); exits 0 when
valid, 1 otherwise."""
import math
import re
import sys


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    n, k = int(sys.argv[1]), int(sys.argv[2])
    text = " ".join(x for x in open(sys.argv[3], encoding="ascii", errors="replace").read().splitlines()
                    if not x.lstrip().startswith("#"))
    s = "".join(text.split())
    if re.fullmatch(r"[+\-0]+", s):
        row = [{"+": 1, "-": -1, "0": 0}[c] for c in s]
    else:
        try:
            row = [int(v) for v in text.replace(",", " ").split()]
        except ValueError:
            print("the row must be integers -1, 0, 1 or the characters -, 0, +")
            return 1
    if len(row) != n or any(v not in (-1, 0, 1) for v in row):
        print(f"the row must have {n} entries from -1, 0, 1 (it has {len(row)})")
        return 1
    support = [i for i, v in enumerate(row) if v]
    if len(support) != k:
        print(f"weight {len(support)}, expected {k}")
        return 1
    for shift in range(1, n):
        acc = 0
        for i in support:
            acc += row[i] * row[(i + shift) % n]
        if acc:
            print(f"periodic autocorrelation {acc} at shift {shift}: W W^T is not {k} I")
            return 1
    g = n
    for i in support:
        g = math.gcd(g, i - support[0])
    if g != 1:
        print(f"not proper: the support lies in a coset of the subgroup of index {g}")
        return 1
    print(f"proper CW({n}, {k}): weight {k}, W W^T = {k} I")
    print("RESULT 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
