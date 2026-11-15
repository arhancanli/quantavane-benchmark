"""Exact check of mutually orthogonal Latin squares (standard library only).

  python3 -I mols_check.py N FILE

FILE holds K Latin squares of order N, one after another: N rows per square, each row N symbols 0..N-1 (or 1..N)
separated by spaces or commas; blank lines between squares are allowed. Each square must be Latin (every symbol once
in every row and every column), and every two squares must be orthogonal: superimposed, they show each of the N^2
ordered pairs of symbols exactly once. Prints the order, the number of squares and "RESULT K"; exits 0 when the K
squares are mutually orthogonal Latin squares, 1 otherwise. K is the score (three MOLS of order 10 would be new).

The first line may be a header "N K" (the format of github.com/Constructive-Codes/MOLS): N must be the order and K
the number of squares in the file. Files above 2 MB are checked by the C helper mols_scan.c (built with cc -O3 on
first use; the same rules, with every ordered pair of symbols marked in an array of N^2 stamps); --python or
--native forces one way.

A difference matrix may be given instead of the squares: a first line "group n_1 n_2 ... n_r" naming the abelian group
G = Z_n1 x ... x Z_nr of order N, then K' rows of N elements of G, each written as the integer a_1 + n_1 (a_2 + n_2
(a_3 + ...)) of its coordinates 0 <= a_i < n_i. It is an (N, K'; 1) difference matrix when for every two rows the N
differences, column by column, are N distinct elements of G. Every two rows then give each element of G once, the
N^2 translates of its columns form an orthogonal array OA(K', N) of strength 2 and index 1, that is a transversal
design TD(K', N), and its columns 3 to K' are K' - 2 mutually orthogonal Latin squares of order N (L_t(x, y) is the
entry in column t of the row whose first two entries are x and y). The result is K' - 2."""


def difference_matrix(n, lines):
    """(K' - 2, None) for a valid difference matrix, or (None, reason)."""
    head = lines[0]
    try:
        orders = [int(x) for x in head[1:]]
    except ValueError:
        return None, "the group line must list integers"
    if not orders or any(o < 2 for o in orders):
        return None, "the group needs cyclic factors of order 2 or more"
    prod = 1
    for o in orders:
        prod *= o
    if prod != n:
        return None, f"the group has order {prod}, not {n}"
    rows = []
    for t in lines[1:]:
        try:
            r = [int(x) for x in t]
        except ValueError:
            return None, "the rows must be integers"
        if len(r) != n or any(x < 0 or x >= n for x in r):
            return None, f"row {len(rows) + 1}: expected {n} elements of G written as integers 0..{n - 1}"
        rows.append(r)
    if len(rows) < 3:
        return None, "a difference matrix with fewer than 3 rows gives no Latin square"
    # coordinates of every entry (a_1 is the least significant digit)
    weights, w = [], 1
    for o in orders:
        weights.append(w)
        w *= o
    digits = [[[(x // weights[c]) % orders[c] for x in r] for c in range(len(orders))] for r in rows]
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            code = [0] * n
            for c, o in enumerate(orders):
                a, b, wc = digits[i][c], digits[j][c], weights[c]
                for col in range(n):
                    code[col] += ((a[col] - b[col]) % o) * wc
            if len(set(code)) != n:
                return None, f"rows {i + 1} and {j + 1}: the differences repeat an element of G"
    return len(rows) - 2, None
import os
import subprocess
import sys

NATIVE_FROM = 2 * 10 ** 6


def helper():
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", "mols_scan"), os.path.join(here, "mols_scan.c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    return exe


def main():
    flags = [a for a in sys.argv[1:] if a in ("--python", "--native")]
    args = [a for a in sys.argv[1:] if a not in flags]
    if len(args) != 2:
        print(__doc__)
        return 2
    n = int(args[0])
    with open(args[1], encoding="ascii", errors="replace") as fh:
        first = next((t.split("#")[0].replace(",", " ").split() for t in fh if t.split("#")[0].strip()), [])
    if first and first[0] == "group":
        with open(args[1], encoding="ascii", errors="replace") as fh:
            lines = [t.split("#")[0].replace(",", " ").split() for t in fh]
        k, why = difference_matrix(n, [t for t in lines if t])
        if k is None:
            print(f"not an ({n}, K'; 1) difference matrix: {why}")
            return 1
        print(f"order {n}: an ({n}, {k + 2}; 1) difference matrix, so {k} mutually orthogonal Latin squares")
        print(f"RESULT {k}")
        return 0
    if "--native" in flags or ("--python" not in flags and os.path.getsize(args[1]) > NATIVE_FROM):
        r = subprocess.run([helper(), str(n), args[1]], capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or ["FAIL no output from mols_scan"])[-1]
        if r.returncode != 0 or not last.startswith("OK "):
            print(last[5:] if last.startswith("FAIL ") else last)
            return 1
        k = int(last.split()[1])
        print(f"order {n}: {k} mutually orthogonal Latin square{'s' if k != 1 else ''} (checked in C)")
        print(f"RESULT {k}")
        return 0
    rows, header = [], None
    for text in open(args[1], encoding="ascii", errors="replace"):
        s = text.split("#")[0].replace(",", " ").split()
        if not s:
            continue
        try:
            row = [int(x) for x in s]
        except ValueError:
            print(f"not a row of integers: {text.strip()[:60]!r}")
            return 1
        if not rows and header is None and len(row) == 2 and n != 2:
            header = row
            continue
        rows.append(row)
    if header is not None and header[0] != n:
        print(f"the file is for order {header[0]}, not {n}")
        return 1
    if header is not None and rows and len(rows) % n == 0 and header[1] != len(rows) // n:
        print(f"the header announces {header[1]} squares, the file has {len(rows) // n}")
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
