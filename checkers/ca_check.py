"""Exact check of a covering array CA(N; T, K, V) (standard library only).

  python3 -I ca_check.py T K V FILE

FILE has one row per line: K symbols from 0..V-1 separated by spaces or commas (for V <= 10 a row may also be
written as K digits with no separators). Blank lines and lines starting with '#' are ignored. The array is a
covering array of strength T when every choice of T of its K columns shows all V^T tuples of symbols in some row.

For each column and symbol, the rows holding that symbol form a bit set. The check goes through the T-sets of columns
in order, intersecting the bit sets one column at a time (the intersections of a set's first columns are shared by
all its extensions); a T-set is covered when none of its V^T intersections is empty. The first uncovered tuple, if
any, is printed with its columns. Prints "rows N" and, as its last line, "RESULT N", and exits 0 when the array is a
covering array of strength T with K columns over V symbols; exits 1 otherwise."""
import sys


def read_rows(path, k, v):
    rows = []
    for no, line in enumerate(open(path), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.replace(",", " ").split()
        if len(parts) == 1 and len(s) == k and v <= 10 and s.isdigit():
            parts = list(s)
        try:
            row = [int(x) for x in parts]
        except ValueError:
            raise SystemExit(f"line {no}: not a row of integers")
        if len(row) != k:
            raise SystemExit(f"line {no}: {len(row)} symbols, not {k}")
        if not all(0 <= x < v for x in row):
            raise SystemExit(f"line {no}: a symbol outside 0..{v - 1}")
        rows.append(row)
    return rows


def first_gap(rows, t, k, v):
    """None when every T-set of columns shows every tuple; otherwise (columns, tuple) of an uncovered one."""
    masks = [[0] * v for _ in range(k)]
    for r, row in enumerate(rows):
        bit = 1 << r
        for c, s in enumerate(row):
            masks[c][s] |= bit
    everything = [(1 << len(rows)) - 1]

    def rec(start, depth, prev, cols):
        for c in range(start, k - (t - depth) + 1):
            cur = [a & b for a in prev for b in masks[c]]
            if 0 in cur:
                i = cur.index(0)
                tup = []
                for _ in range(depth + 1):
                    i, s = divmod(i, v)
                    tup.append(s)
                # the empty intersection may show at fewer than T columns; any T-set holding them is uncovered
                return cols + [c], tup[::-1]
            if depth + 1 < t:
                gap = rec(c + 1, depth + 1, cur, cols + [c])
                if gap:
                    return gap
        return None

    return rec(0, 0, everything, [])


def main():
    t, k, v = (int(x) for x in sys.argv[1:4])
    if not (1 <= t <= k and v >= 2):
        print(f"need 1 <= T <= K and V >= 2, got T={t} K={k} V={v}")
        return 1
    rows = read_rows(sys.argv[4], k, v)
    if len(rows) < v ** t:
        print(f"{len(rows)} rows cannot show all {v}^{t} = {v ** t} tuples")
        return 1
    gap = first_gap(rows, t, k, v)
    if gap:
        cols, tup = gap
        print(f"columns {[c + 1 for c in cols]} never show the symbols {tup} together: not a covering array of "
              f"strength {t}")
        return 1
    print(f"every {t} of the {k} columns show all {v ** t} tuples of symbols")
    print(f"rows {len(rows)}")
    print(f"RESULT {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
