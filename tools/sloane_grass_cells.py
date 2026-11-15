"""sloane_grass_cells.py: N. J. A. Sloane's table of best Grassmannian packings as the benchmark family
grassmannian-packing (checked by checkers/grass_check.py).

  python3 -I sloane_grass_cells.py grassTab.html READ REVISION

grassTab.html is neilsloane.com/grass/grassTab.html (last modified 20 Jan 1997): rows "m n N D name", the largest
known least squared chordal distance D of N n-dimensional subspaces of R^m. A packing in G(m,n) and the complements of
its subspaces have the same distances, so (m, n) and (m, m - n) are one table; n is taken as min(n, m - n).

Per (m, n, N) the best known value is the largest D the table lists for N or MORE subspaces (any subset of a packing is
a packing; DHST 2008 note such cases, e.g. 11 to 16 planes in R^4), raised where families/grassmannian-packing/
literature.json gives a better published packing. Upper bound: Rankin's simplex bound n(m-n)/m * N/(N-1) and, for
N > m(m+1)/2, the orthoplex bound n(m-n)/m (Conway, Hardin and Sloane 1996, Corollary 5). A cell is open when its best
known value is below the bound by more than one unit of its last printed digit and no proof of optimality is listed in
literature.json. Fractions and decimals printed with fewer than 10 significant digits are exact values of constructions; longer
decimals are rounded (a value counts as better only beyond its last printed digit). Kept: certificates of at most 300,000 numbers (N n m) and at most 10^7 pairs. Rows whose value exceeds
the bound by more than their printed precision cannot be packings in this sense and are not used."""
import collections
import hashlib
import json
import os
import re
import sys
from fractions import Fraction as F

MAX_NUMBERS, MAX_PAIRS = 300_000, 10 ** 7


def unit(s):
    return F(1, 10 ** len(s.split(".")[1])) if "." in s and s.split(".")[1] else F(1)


def rounded(s):
    """A decimal printed with 10 or more significant digits is a rounded value; shorter ones (.5, .75, 1.) and
    fractions are exact values of constructions."""
    return "." in s and len(s.replace(".", "").lstrip("0")) >= 10


def norm(s):
    """A printed value as a decimal string with a leading digit; fractions p/q kept."""
    if "/" in s:
        return s
    if s.startswith("."):
        s = "0" + s
    if s.endswith("."):
        s = s[:-1]
    return s


def dec_down(x, digits=15):
    q = x.numerator * 10 ** digits // x.denominator
    return f"{q // 10 ** digits}.{q % 10 ** digits:0{digits}d}"


def root_near(coef, approx):
    """The root of the polynomial (coefficients from the highest degree) in (approx - 10^-4, approx], as an interval of
    width < 10^-40 (exact bisection; the polynomial must change sign there)."""
    def val(x):
        r = F(0)
        for c in coef:
            r = r * x + c
        return r
    lo, hi = F(approx) - F(1, 10 ** 4), F(approx)
    vlo, vhi = val(lo), val(hi)
    assert vlo * vhi <= 0, (coef, approx)
    while hi - lo > F(1, 10 ** 40):
        mid = (lo + hi) / 2
        if val(mid) * vlo <= 0:
            hi = mid
        else:
            lo, vlo = mid, val(mid)
    return lo, hi


def main():
    page, read, revision = sys.argv[1:4]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fam_dir = os.path.join(root, "families", "grassmannian-packing")
    lit = json.load(open(os.path.join(fam_dir, "literature.json")))
    raw = open(page, "rb").read()
    text = raw.decode("latin-1")
    pre = re.findall(r"<pre>(.*?)</pre>", text, re.S)
    assert len(pre) == 1
    rows = []
    for line in pre[0].splitlines():
        line = re.sub(r"<[^>]+>", "", line).strip()
        mm = re.match(r"^(\d+)\s+(\d+)\s+(\d+)\s+([\d./]+)\s*(.*)$", line)
        if mm:
            rows.append((int(mm[1]), int(mm[2]), int(mm[3]), norm(mm[4]), re.sub(r"\s+", " ", mm[5]).strip()))
    stats = collections.Counter(rows=len(rows))

    def bound(m, n, N):
        b, how = F(n * (m - n), m) * F(N, N - 1), "simplex bound n(m-n)/m N/(N-1)"
        if N > m * (m + 1) // 2 and F(n * (m - n), m) < b:
            b, how = F(n * (m - n), m), "orthoplex bound n(m-n)/m, N > m(m+1)/2"
        return b, how

    table = collections.defaultdict(list)          # (m, n) -> [(N, value, printed, source)]
    for m, n, N, D, name in rows:
        nn = min(n, m - n)
        val = F(D)
        b, _ = bound(m, nn, N)
        tol = unit(D) if rounded(D) else F(0)
        if val > b + tol:
            stats["rows above the bound (not used)"] += 1
            continue
        if name.startswith("/usr/rhh/"):
            src = f"computer search by R. H. Hardin and N. J. A. Sloane (file {name.rsplit('/', 1)[1]})"
        else:
            src = name.replace("\\cite{grass1}", "[CHS96]")
        table[(m, nn)].append((N, val, D, src))
    for m, N, coef, approx in lit["packings"]:
        lo, hi = root_near(coef, approx)
        dval = 1 - hi * hi                          # a lower bound on 1 - mu^2, within 10^-39
        table[(m, 1)].append((N, F(dec_down(dval)), dec_down(dval),
                              "M. Fickus, J. Jasper and D. G. Mixon, Packings in real projective spaces (2018), Table 1"))
    optimal = {(o["m"], o["n"], o["N"]): o["source"] for o in lit["optimal"]}
    cells, improved = [], []
    for (m, n), lst in sorted(table.items()):
        for N in sorted({x[0] for x in lst}):
            if N < 2:
                continue
            own = [x for x in lst if x[0] == N and not x[3].startswith("M. Fickus")]
            cand = [x for x in lst if x[0] >= N]
            bN, bval, bstr, bsrc = max(cand, key=lambda x: (x[1], not x[3].startswith("M. Fickus"), -x[0]))
            if not own:                             # only rows of the table make cells
                continue
            stats["(m, n, N) in the table"] += 1
            b, how = bound(m, n, N)
            if bval >= b - (unit(bstr) if rounded(bstr) else F(0)):
                stats["equal to the bound (solved)"] += 1
                continue
            if (m, n, N) in optimal:
                stats["proven optimal since 1997 (solved)"] += 1
                continue
            if N * n * m > MAX_NUMBERS or N * (N - 1) // 2 > MAX_PAIRS:
                stats["too large to check"] += 1
                continue
            # fractions, and decimals printed with fewer than 10 significant digits (.5, .75, 1.: values of constructions), are
            # exact: written with 15 decimals; longer decimals are rounded values, beaten only beyond their last digit
            best = bstr if rounded(bstr) else dec_down(bval)
            own_best = max(own, key=lambda x: x[1])
            holder = bsrc
            if bN != N:
                holder = f"{N} of the {bN} subspaces of the packing for N = {bN} ({bsrc})"
            if bsrc.startswith("M. Fickus") and bval > own_best[1] + F(1, 10 ** 9):
                improved.append((m, n, N))
                holder += f"; Sloane's table lists {own_best[2]}"
            elif bsrc.startswith("M. Fickus") and bval > own_best[1]:
                stats["exact forms of the table's own packings (Fickus, Jasper and Mixon)"] += 1
                holder += f"; their exact form of the table's packing, which the table lists as {own_best[2]}"
            elif bN != N and bval > own_best[1]:
                holder += f"; the table lists {own_best[2]} for N = {N}"
            cells.append({"id": f"grass-{m}-{n}-{N}", "params": {"m": m, "n": n, "N": N}, "best": best,
                          "bound": f"{b.numerator}/{b.denominator} ({how})", "holder": holder})
    stats["kept"] = len(cells)
    stats["raised by Fickus, Jasper and Mixon (2018)"] = len(improved)
    fam = {
        "family": "grassmannian-packing",
        "title": "Packings in real Grassmannian spaces: N n-dimensional subspaces of R^m with the largest least "
                 "squared chordal distance",
        "added": "2.2",
        "objective": "maximize",
        "id_prefixes": ["grass-"],
        "keeper": "N. J. A. Sloane, Table of best Grassmannian packings (with R. H. Hardin, J. H. Conway and others)",
        "page": "http://neilsloane.com/grass/grassTab.html",
        "cell_url": "http://neilsloane.com/grass/dim{m}/",
        "read": read,
        "revision": revision,
        "exact_values": False,
        "template": {
            "title": "Grassmannian packing: {N} subspaces of dimension {n} in R^{m}",
            "statement": "Find {N} subspaces of dimension {n} of R^{m} whose least squared chordal distance is as "
                         "large as possible. The squared chordal distance of two subspaces is the sum of the squares "
                         "of the sines of their {n} principal angles, {n} - tr(P_A P_B) for their orthogonal "
                         "projections (Conway, Hardin and Sloane, 1996).",
            "submission": "Text file: {N} x {n} x {m} numbers (integers, decimals or fractions p/q), the {n} spanning "
                          "vectors of {m} coordinates of each subspace one after the other, as in Sloane's files "
                          "(neilsloane.com/grass/dim{m}/); the vectors need not be orthonormal. See "
                          "checkers/grass_check.py.",
            "args": ["{m}", "{n}", "{N}"],
        },
        "checker": {"program": "grass_check.py", "value": "result"},
        "score": "the least squared chordal distance between two of the subspaces, exact (larger is better)",
        "best_text": "The best known value is {best} ({holder}); the table prints its values rounded, so a packing "
                     "improves it when its least squared chordal distance is larger by more than one unit in the last "
                     "printed decimal.",
        "bound_kind": "upper bound",
        "bound_source": "Rankin's simplex bound n(m-n)/m N/(N-1), and for N > m(m+1)/2 the orthoplex bound n(m-n)/m "
                        "(Conway, Hardin and Sloane 1996)",
        "holder_unknown": "the table's source for the entry",
        "holder_sources": "the name column of the table (Hardin and Sloane's computer searches, or the paper of a "
                          "construction); later packings from families/grassmannian-packing/literature.json",
        "open_rule": "every (m, n, N) of the table whose best known value (the largest the table lists for N or more "
                     "subspaces, or a later published packing) is below the bound by more than one unit of its last "
                     "printed decimal, unless optimality has been proven since (literature.json)",
        "left_out": "; ".join(f"{v} {k}" for k, v in stats.items() if k not in ("kept",)),
        "literature": "families/grassmannian-packing/literature.json (checked 16 Nov 2026)",
        "page_sha256": {os.path.basename(page): hashlib.sha256(raw).hexdigest()},
        "cells": "cells.jsonl",
        "count": len(cells),
        "quantavane_records": 0,
        "single_problems_left_out": 0,
    }
    json.dump(fam, open(os.path.join(fam_dir, "family.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(fam_dir, "cells.jsonl"), "w") as f:
        for c in cells:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(dict(stats))
    print("raised:", improved)


if __name__ == "__main__":
    main()
