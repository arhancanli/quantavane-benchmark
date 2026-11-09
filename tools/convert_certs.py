"""Turn fetched source files into the certificate formats of our checkers (standard library only; no code from the
sources is run, they are read as data).

  python3 -I tools/convert_certs.py fmm IN.mpl.bz2 OUT.json L        Sedoglavic's catalogue (maple tensor representation)
  python3 -I tools/convert_certs.py g6 IN.g6 OUT.txt                  a graph6 graph as the 0/1 matrix ramsey_check reads
  python3 -I tools/convert_certs.py dobbelaere PAGE N SIZE OUT        one network from B. Dobbelaere's list
  python3 -I tools/convert_certs.py shift IN OUT D                    every digit of a colouring lowered by D (1..k to 0..k-1)

fmm: the catalogue writes C = A.B = sum_i Trace(U_i^T A) Trace(V_i^T B) W_i^T, so the coefficient of product i in
C[r][c] is W_i[c][r]; the third factor is transposed into the layout of matmul_check.py. Entries may contain the
catalogue's free parameter l (any nonzero value gives a valid algorithm; L sets it)."""
import bz2
import html
import json
import re
import sys
from fractions import Fraction


def entry(tok, lval):
    m = re.fullmatch(r"([+-]?)(\d+|l)(?:/(\d+|l))?", tok.strip())
    if not m:
        raise ValueError(f"unexpected entry {tok!r}")
    num = lval if m.group(2) == "l" else Fraction(int(m.group(2)))
    den = Fraction(1) if m.group(3) is None else lval if m.group(3) == "l" else Fraction(int(m.group(3)))
    v = num / den
    return -v if m.group(1) == "-" else v


def fmm(src, out, lval):
    text = bz2.decompress(open(src, "rb").read()).decode("ascii")
    body = text[text.index("TriadSet("):]
    mats = []
    for r, c, rows in re.findall(r"Matrix\((\d+), (\d+), \[(\[.*?\])\]\)", body):
        m = [[entry(x, lval) for x in row.split(",")] for row in re.findall(r"\[([^\[\]]*)\]", rows)]
        if len(m) != int(r) or any(len(x) != int(c) for x in m):
            raise ValueError("a matrix does not have its stated shape")
        mats.append(m)
    if len(mats) % 3:
        raise ValueError("the factors do not come in triples")
    terms = []
    for i in range(0, len(mats), 3):
        U, V, W = mats[i:i + 3]
        Wt = [[W[k][j] for k in range(len(W))] for j in range(len(W[0]))]
        terms.append([[[str(x) for x in row] for row in M] for M in (U, V, Wt)])
    json.dump({"field": "Q", "source": f"fmm.univ-lille.fr maple tensor representation, parameter l = {lval}", "terms": terms}, open(out, "w"))
    print(f"{len(terms)} terms")


def g6(src, out):
    data = open(src, "rb").read().strip()
    if data.startswith(b">>graph6<<"):
        data = data[10:]
    if data[0] != 126:
        n, used = data[0] - 63, 1
    elif data[1] != 126:
        n, used = ((data[1] - 63) << 12) | ((data[2] - 63) << 6) | (data[3] - 63), 4
    else:
        n, used = 0, 8
        for ch in data[2:8]:
            n = (n << 6) | (ch - 63)
    bits = []
    for ch in data[used:]:
        c = ch - 63
        if not 0 <= c < 64:
            raise ValueError("not graph6 data")
        bits.extend((c >> s) & 1 for s in (5, 4, 3, 2, 1, 0))
    if len(bits) < n * (n - 1) // 2:
        raise ValueError("graph6 data too short")
    m = [[0] * n for _ in range(n)]
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                m[i][j] = m[j][i] = 1
            k += 1
    open(out, "w").write("".join("".join(map(str, r)) + "\n" for r in m))
    print(f"{n} vertices")


def dobbelaere(page, n, size, out):
    text = html.unescape(re.sub(r"<[^>]+>", "\n", open(page, encoding="utf-8").read()))
    m = re.search(r"Sorting network for %d inputs, %d CEs, (\d+) layers:(.*?)(?:Sorting network for|\Z)" % (n, size), text, re.S)
    if not m:
        raise ValueError(f"no network for {n} inputs with {size} comparators on the page")
    pairs = re.findall(r"\((\d+),(\d+)\)", m.group(2))
    if len(pairs) != size:
        raise ValueError(f"{len(pairs)} comparators read, {size} expected")
    with open(out, "w") as f:
        f.write(f"# {n} inputs, {size} comparators, {m.group(1)} layers: from B. Dobbelaere's list of sorting networks\n")
        f.write("".join(f"{a} {b}\n" for a, b in pairs))
    print(f"{n} inputs, {size} comparators")


def shift(src, out, d):
    s = "".join(open(src).read().split())
    if not s.isdigit():
        raise ValueError("not a string of digits")
    open(out, "w").write("".join(str(int(ch) - d) for ch in s) + "\n")
    print(f"{len(s)} digits")


def main():
    a = sys.argv[1:]
    if a[:1] == ["fmm"] and len(a) == 4:
        fmm(a[1], a[2], Fraction(a[3]))
    elif a[:1] == ["g6"] and len(a) == 3:
        g6(a[1], a[2])
    elif a[:1] == ["dobbelaere"] and len(a) == 5:
        dobbelaere(a[1], int(a[2]), int(a[3]), a[4])
    elif a[:1] == ["shift"] and len(a) == 4:
        shift(a[1], a[2], int(a[3]))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
