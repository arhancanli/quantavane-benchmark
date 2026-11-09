"""Exact check of mutually orthogonal Latin squares (standard library only).

  python3 -I mols_check.py N FILE

FILE holds K Latin squares of order N, one after another: N rows per square, each row N symbols 0..N-1 (or 1..N)
separated by spaces or commas; blank lines between squares are allowed. Each square must be Latin (every symbol once
in every row and every column), and every two squares must be orthogonal: superimposed, they show each of the N^2
ordered pairs of symbols exactly once. Prints the order, the number of squares and "RESULT K"; exits 0 when the K
squares are mutually orthogonal Latin squares, 1 otherwise. K is the score (three MOLS of order 10 would be new)."""
import sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    n = int(sys.argv[1])
    rows = []
    for text in open(sys.argv[2], encoding="ascii", errors="replace"):
        s = text.split("#")[0].replace(",", " ").split()
        if not s:
            continue
        try:
            rows.append([int(x) for x in s])
        except ValueError:
            print(f"not a row of integers: {text.strip()[:60]!r}")
            return 1
    if not rows or len(rows) % n or any(len(r) != n for r in rows):
        print(f"{len(rows)} rows, expected a multiple of {n}, each of {n} symbols")
        return 1
    symbols = {x for r in rows for x in r}
    if symbols <= set(range(1, n + 1)) and n in symbols:
        rows = [[x - 1 for x in r] for r in rows]
    elif not symbols <= set(range(n)):
        print(f"symbols must be 0..{n - 1} or 1..{n}")
        return 1
    squares = [rows[i:i + n] for i in range(0, len(rows), n)]
    full = set(range(n))
    for t, sq in enumerate(squares):
        for i in range(n):
            if set(sq[i]) != full:
                print(f"square {t + 1}: row {i + 1} is not a permutation of the symbols")
                return 1
            if {sq[r][i] for r in range(n)} != full:
                print(f"square {t + 1}: column {i + 1} is not a permutation of the symbols")
                return 1
    for a in range(len(squares)):
        for b in range(a + 1, len(squares)):
            pairs = {(squares[a][i][j], squares[b][i][j]) for i in range(n) for j in range(n)}
            if len(pairs) != n * n:
                print(f"squares {a + 1} and {b + 1} are not orthogonal ({len(pairs)} distinct pairs of {n * n})")
                return 1
    k = len(squares)
    print(f"order {n}: {k} mutually orthogonal Latin square{'s' if k != 1 else ''}")
    print(f"RESULT {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
