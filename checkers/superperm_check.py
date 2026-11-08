"""Exact check of a superpermutation (standard library only).

  python3 -I superperm_check.py N FILE

FILE holds a string of digits from 1 to N (whitespace ignored; the format of Leaps in Bounds). It is a superpermutation
when every permutation of 1..N occurs in it as N consecutive characters. The checker slides a window of N characters
along the string and collects the windows with N distinct digits; there must be N! of them. A superpermutation of
length L shows L(N) <= L. Prints the length and "RESULT L"; exits 0 when valid, 1 otherwise."""
import math
import sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    n = int(sys.argv[1])
    if not 1 <= n <= 9:
        print("N must be 1..9")
        return 2
    s = "".join("\n".join(line.split("#")[0] for line in open(sys.argv[2], encoding="ascii", errors="replace")).split())
    if not s or any(c not in "123456789"[:n] for c in s):
        print(f"the string must hold only digits 1..{n}")
        return 1
    found = set()
    for i in range(len(s) - n + 1):
        w = s[i:i + n]
        if len(set(w)) == n:
            found.add(w)
    need = math.factorial(n)
    if len(found) != need:
        print(f"{len(found)} of the {need} permutations of 1..{n} occur")
        return 1
    print(f"length {len(s)}: all {need} permutations of 1..{n} occur")
    print(f"RESULT {len(s)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
