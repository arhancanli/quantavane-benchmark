"""Exact check of a van der Waerden colouring (standard library only).

  python3 -I vdw_check.py R K FILE

FILE holds the colours of n consecutive integers as a string of digits from 0 to R-1 (whitespace ignored; the format
of Leaps in Bounds). The checker looks for a monochromatic arithmetic progression of K terms: for each colour, the
positions of that colour form a bit set S, and S & (S >> d) & (S >> 2d) & ... & (S >> (K-1)d) is empty for every
step d exactly when the colour holds no such progression. A colouring of n integers without one shows
W(R,K) > n. Prints the length and "RESULT n"; exits 0 for a valid colouring, 1 otherwise."""
import sys


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    r, k = int(sys.argv[1]), int(sys.argv[2])
    if not (1 <= r <= 10 and k >= 2):
        print("R must be 1..10 and K at least 2")
        return 2
    text = "".join("\n".join(line.split("#")[0] for line in open(sys.argv[3], encoding="ascii", errors="replace")).split())
    if not text or any(c not in "0123456789"[:r] for c in text):
        print(f"the file must hold only digits 0..{r - 1} (and whitespace)")
        return 1
    n = len(text)
    for c in range(r):
        s = int(text[::-1].translate({ord(str(x)): ("1" if x == c else "0") for x in range(10)}), 2)
        for d in range(1, (n - 1) // (k - 1) + 1):
            t = s
            for j in range(1, k):
                t &= s >> (j * d)
                if not t:
                    break
            if t:
                a = (t & -t).bit_length()          # position (from 1) of the first term
                print(f"colour {c} holds the progression {a}, {a + d}, ..., {a + (k - 1) * d} (positions from 1)")
                return 1
    print(f"n {n} colours {r}: no monochromatic arithmetic progression of {k} terms")
    print(f"RESULT {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
