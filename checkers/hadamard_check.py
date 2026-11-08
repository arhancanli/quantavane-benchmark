"""Exact check of a Hadamard matrix (standard library only).

  python3 -I hadamard_check.py N FILE

FILE holds N rows of N entries +1 or -1, written as + and - characters or as integers 1 and -1 separated by spaces
or commas. A Hadamard matrix H has H H^T = N I: any two rows agree in exactly N/2 positions. Each row is held as a bit
set of its -1 entries, and two rows are orthogonal exactly when they differ in N/2 positions. Prints the order and
"RESULT 1" (a Hadamard matrix of order N exists); exits 0 for a Hadamard matrix, 1 otherwise."""
import re
import sys


def parse_row(line):
    s = line.strip()
    if re.fullmatch(r"[+\-]+", s):
        return [1 if c == "+" else -1 for c in s]
    vals = [int(v) for v in s.replace(",", " ").split()]
    return vals


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    n = int(sys.argv[1])
    rows = []
    for line in open(sys.argv[2], encoding="ascii", errors="replace"):
        if line.strip() and not line.lstrip().startswith("#"):
            try:
                rows.append(parse_row(line))
            except ValueError:
                print("rows must be + and - characters or integers 1 and -1")
                return 1
    if len(rows) != n or any(len(r) != n for r in rows):
        print(f"{len(rows)} rows of lengths {sorted(set(len(r) for r in rows))}, expected {n} rows of {n}")
        return 1
    if any(v not in (1, -1) for r in rows for v in r):
        print("every entry must be +1 or -1")
        return 1
    bits = [int("".join("1" if v == -1 else "0" for v in r), 2) for r in rows]
    half = n // 2
    if n > 2 and n % 4:
        print(f"no Hadamard matrix of order {n} > 2 exists unless 4 divides it; the rows below are not one")
    for i in range(n):
        bi = bits[i]
        for j in range(i + 1, n):
            if 2 * bin(bi ^ bits[j]).count("1") != n:
                print(f"rows {i + 1} and {j + 1} are not orthogonal")
                return 1
    print(f"order {n}: H H^T = {n} I")
    print("RESULT 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
