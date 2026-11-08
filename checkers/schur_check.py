"""Exact check of a Schur or weak Schur colouring (standard library only).

  python3 -I schur_check.py schur|weak K FILE

FILE holds the colours of 1, ..., n as a string of digits from 0 to K-1 (whitespace ignored; the format of Leaps in
Bounds). A Schur colouring has no monochromatic solution of x + y = z (x = y allowed); a weak Schur colouring has
none with x != y. For each colour the checker forms the bit set S of its numbers and, for every x in S, tests whether
(S shifted up by x) meets S, leaving out y = x in the weak case. A valid colouring of 1..n shows S(K) >= n (or
WS(K) >= n). Prints the length and "RESULT n"; exits 0 for a valid colouring, 1 otherwise."""
import sys


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("schur", "weak"):
        print(__doc__)
        return 2
    weak, k = sys.argv[1] == "weak", int(sys.argv[2])
    if not 1 <= k <= 10:
        print("K must be 1..10")
        return 2
    text = "".join("\n".join(line.split("#")[0] for line in open(sys.argv[3], encoding="ascii", errors="replace")).split())
    if not text or any(c not in "0123456789"[:k] for c in text):
        print(f"the file must hold only digits 0..{k - 1} (and whitespace)")
        return 1
    n = len(text)
    for c in range(k):
        digit = str(c)
        s = 0
        for i, ch in enumerate(text, start=1):
            if ch == digit:
                s |= 1 << i                         # bit i: the number i has colour c
        x_bits = s
        while x_bits:
            x = (x_bits & -x_bits).bit_length() - 1
            x_bits &= x_bits - 1
            ys = (s & ~(1 << x)) if weak else s
            hit = (ys << x) & s
            if hit:
                z = (hit & -hit).bit_length() - 1
                print(f"colour {c}: {x} + {z - x} = {z}")
                return 1
    print(f"n {n} colours {k}: no monochromatic solution of x + y = z{' with x != y' if weak else ''}")
    print(f"RESULT {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
