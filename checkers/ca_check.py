"""Exact check of a covering array CA(N; T, K, V) (standard library only).

  python3 -I ca_check.py T K V FILE

FILE has one row per line: K symbols from 0..V-1 separated by spaces or commas (for V <= 10 a row may also be
written as K digits with no separators). Blank lines and lines starting with '#' are ignored. The array is a
covering array of strength T when every choice of T of its K columns shows all V^T tuples of symbols in some row.

For each column and symbol, the rows holding that symbol form a bit set. The check goes through the T-sets of columns
in order, intersecting the bit sets one column at a time (the intersections of a set's first columns are shared by
all its extensions); a T-set is covered when none of its V^T intersections is empty. The first uncovered tuple, if
any, is printed with its columns. Prints "rows N" and, as its last line, "RESULT N", and exits 0 when the array is a
covering array of strength T with K columns over V symbols; exits 1 otherwise.

Above 5 x 10^7 row visits (C(K,T) x N) the check is done in C (built with cc -O3 on first use). For V <= 64 the helper
is ca_trie.c (16 Nov 2026): the rows are split by their symbols in the first T-2 chosen columns; within each group,
for every choice of the (T-1)-th column, each row's symbols in all later columns are OR-ed as one-hot bit masks into
the accumulator of its symbol in that column, and every accumulator must come out full; a row is visited once per
T-set, as one lane of a vector operation. For V > 64 the helper is ca_scan.c: for each T-set of columns it numbers
every row's tuple and marks it in a bit array of V^T bits, which must fill up. --native (ca_trie.c), --mark
(ca_scan.c) or --python forces one way."""
import math
import sys


def read_lines(path, k, v):
    """The rows, each as one string of K valid symbols (integers 0..V-1) separated by single spaces (one string per
    row keeps the memory small for large arrays)."""
    allowed = {str(i) for i in range(v)}
    rows = []
    for no, line in enumerate(open(path), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.replace(",", " ").split()
        if len(parts) == 1 and len(s) == k and v <= 10 and s.isdigit():
            parts = list(s)
        if len(parts) != k:
            raise SystemExit(f"line {no}: {len(parts)} symbols, not {k}")
        if not allowed.issuperset(parts):
            try:
                vals = [int(x) for x in parts]
            except ValueError:
                raise SystemExit(f"line {no}: not a row of integers")
            if not all(0 <= x < v for x in vals):
                raise SystemExit(f"line {no}: a symbol outside 0..{v - 1}")
            parts = [str(x) for x in vals]
        rows.append(" ".join(parts))
    return rows


def read_rows(path, k, v):
    return [[int(x) for x in r.split()] for r in read_lines(path, k, v)]


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


NATIVE_FROM = 5 * 10 ** 7          # above C(K,T) x N rows to visit, the check is done in C


def first_gap_native(rows, t, k, v, helper="ca_trie", extra=""):
    """The same question answered by checkers/ca_trie.c or checkers/ca_scan.c (built with cc -O3 on first use); the
    rows may be lists of ints or of tokens."""
    import os
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", helper), os.path.join(here, helper + ".c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    head = f"{t} {k} {v} {len(rows)}{extra}\n".encode()
    body = "\n".join(r if isinstance(r, str) else " ".join(map(str, r)) for r in rows).encode() + b"\n"
    out = subprocess.run([exe], input=head + body, capture_output=True, check=True).stdout.decode().split("\n")
    if out[0].startswith("covered"):
        sets = int(out[0].split()[1])
        assert sets == math.comb(k, t), f"{helper}: wrong number of t-sets"
        return None
    head, tail = out[0][4:].split(":")
    return [int(x) for x in head.split()], [int(x) for x in tail.split()]


def main():
    flags = [a for a in sys.argv[1:] if a in ("--native", "--python", "--mark")]
    args = [a for a in sys.argv[1:] if a not in flags]
    if len(args) != 4:
        print(__doc__)
        return 1
    t, k, v = (int(x) for x in args[:3])
    if not (1 <= t <= k and v >= 2):
        print(f"need 1 <= T <= K and V >= 2, got T={t} K={k} V={v}")
        return 1
    rows = read_lines(args[3], k, v)
    if len(rows) < v ** t:
        print(f"{len(rows)} rows cannot show all {v}^{t} = {v ** t} tuples")
        return 1
    big = math.comb(k, t) * len(rows) > NATIVE_FROM
    if "--python" in flags or (not flags and not big):
        gap = first_gap([[int(x) for x in r.split()] for r in rows], t, k, v)
    elif "--mark" in flags or (not flags and v > 64):
        if v ** t >= 2 ** 32:
            print(f"too large: v^t = {v ** t} does not fit the C helper ca_scan.c")
            return 2
        gap = first_gap_native(rows, t, k, v, "ca_scan")
    else:
        if v > 64:
            print("ca_trie.c takes at most 64 symbols")
            return 2
        gap = first_gap_native(rows, t, k, v, "ca_trie")
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
