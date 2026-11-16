"""arcs_cells.py: the smallest known complete arcs in the projective planes PG(2,q) as the benchmark family
complete-arc (checked by checkers/arc_check.py).

  python3 -I arcs_cells.py SMALLEST_TXT LEXI_TXT READ SMALLEST_PDF LEXI_PDF

SMALLEST_TXT and LEXI_TXT are the text of the two table papers of D. Bartoli, A. A. Davydov, G. Faina, A. A.
Kreshchuk, S. Marcugini and F. Pambianco, extracted page by page (pypdf's extract_text) from arxiv.org/pdf/1312.2155v3
("Tables, bounds and graphics of the smallest known sizes of complete arcs in the plane PG(2,q) for all q <= 160001
and sporadic q in [160801 ... 430007]", smallest known sizes up to June 2015) and arxiv.org/pdf/1404.0469v3 (the sizes
of complete lexiarcs, the arcs of the algorithm FOP with the lexicographical order, for all q <= 321007). Every row of
their appendix tables is a list of pairs q, size. The two PDFs are named to record their SHA-256.

A cell is a prime power q > 32 (the paper: the exact values of t_2(2,q) are known only for q <= 32), with the best
known value the smallest size in either paper (no lexiarc is smaller than the smallest known size), kept when the
check of a complete arc one point smaller is estimated at most ten minutes (arc_check_seconds). The bound on the
other side is the paper's lower bound (1.2): t_2(2,q) > sqrt(2q) + 1, and t_2(2,q) > sqrt(3q) + 1/2 for q = p^h with
h <= 3."""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from import_families import write_family  # noqa: E402

LIMIT_SECONDS = 600     # ten minutes, as for the family difference-set (raised from three minutes on 15 Nov 2026)
# nanoseconds per step of arc_scan.c at the top of the ten-minute range, wall clock on this machine under the load of
# other jobs, sets of points checked in full (ARC_SCAN_ALL counts every uncovered point): prime q 1.128 (q = 180001,
# 2550 points, 5.71 x 10^11 steps in 643.8 s; 0.851 to 0.875 on the complete lexiarcs of PG(2,60013) and PG(2,90001)),
# q = 2^17 1.425 (2140 points, 2.92 x 10^11 steps in 415.5 s), odd q = p^h (h > 1) 3.084 (q = 317^2, 1846 points,
# 1.66 x 10^11 steps in 511.2 s); the time per step grows with the arrays, so the largest measured rates are used,
# with a factor 1.15
NS_PER_STEP = {"prime": 1.13, "two": 1.43, "odd": 3.08}
SAFETY = 1.15


def prime_powers(hi):
    sieve = bytearray([1]) * (hi + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(hi ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    pp = {}
    for p in range(2, hi + 1):
        if sieve[p]:
            q, h = p, 1
            while q <= hi:
                pp[q] = (p, h)
                q *= p
                h += 1
    return pp


def pairs(lines, start):
    """(table, q, size) for every pair of every all-number row after line START"""
    out, table = [], None
    for line in lines[start:]:
        m = re.match(r"\s*T\s?able (\d)\.", line)
        if m:
            table = int(m.group(1))
            continue
        tok = line.split()
        if len(tok) >= 2 and len(tok) % 2 == 0 and all(re.fullmatch(r"\d+", t) for t in tok):
            out += [(table, int(a), int(b)) for a, b in zip(tok[0::2], tok[1::2])]
    return out


def steps(q, n):
    """arc_scan.c's steps for an n-point complete arc: tangents at the first point times secants not through it"""
    return (q + 2 - n) * (n - 1) * (n - 2) // 2


def arc_check_seconds(q, n, ph):
    kind = "prime" if ph[1] == 1 else "two" if ph[0] == 2 else "odd"
    return steps(q, n) * NS_PER_STEP[kind] * 1e-9 * SAFETY


def lower_bound(q, ph):
    """the least integer above the paper's lower bound (1.2), exactly: m > sqrt(3q) + 1/2 iff (2m - 1)^2 > 12q, and
    m > sqrt(2q) + 1 iff (m - 1)^2 > 2q"""
    m = 1
    while (m - 1) ** 2 <= 2 * q:
        m += 1
    if ph[1] <= 3:
        m3 = 1
        while (2 * m3 - 1) ** 2 <= 12 * q:
            m3 += 1
        m = max(m, m3)
    return m


AUTHORS = "D. Bartoli, A. A. Davydov, G. Faina, A. A. Kreshchuk, S. Marcugini and F. Pambianco"
LMP = {37: 15, 61: 20, 71: 22}   # Lisonek, Marcugini and Pambianco, Contrib. Discrete Math. 3 (2008), Props. 2.1-4.1


def holder(q, tabs):
    """who holds a smallest known size, as far as arXiv:1312.2155v3 says (its Section 2 and table notes)"""
    t = ", ".join(f"Table {k}" for k in sorted(tabs))
    if q in LMP:
        return (f"P. Lisonek, S. Marcugini and F. Pambianco, Contrib. Discrete Math. 3 (2008); arXiv:1312.2155v3, {t}")
    if 1 in tabs and q <= 151:
        return f"N. Pace, J. Combin. Des. 22 (2014); arXiv:1312.2155v3, {t}"
    if 1 in tabs:
        return f"{AUTHORS} (arXiv:1312.2155v1, 2013); arXiv:1312.2155v3, {t}"
    if q <= 13627:
        return ("collected by D. Bartoli, A. A. Davydov, G. Faina, S. Marcugini and F. Pambianco, J. Geom. 104 (2013), "
                f"from the sources there; arXiv:1312.2155v3, {t}")
    return f"{AUTHORS}, computer search; arXiv:1312.2155v3, {t}"


def main():
    if len(sys.argv) != 6:
        print(__doc__)
        return 2
    small_path, lex_path, read, small_pdf, lex_pdf = sys.argv[1:]
    L = open(small_path).read().split("\n")
    A = pairs(L, next(k for k, line in enumerate(L) if "Appendix. Tables of the smallest known" in line))
    L2 = open(lex_path).read().split("\n")
    B = pairs(L2, [k for k, line in enumerate(L2) if line.startswith("Table 1. The sizes tL")][1])
    PP = prime_powers(430007)
    small, lex, tables = {}, {}, {}
    for name, rows, d in (("smallest", A, small), ("lexiarc", B, lex)):
        for table, q, v in rows:
            assert q in PP, (name, q)
            assert d.get(q, v) == v, (name, q, d[q], v)   # a q listed in two tables has one size
            d[q] = v
            if name == "smallest":
                tables.setdefault(q, set()).add(table)
    assert all(q in small for q in PP if q <= 160001), "the smallest known sizes cover every prime power <= 160001"
    assert all(q in lex for q in PP if 3 <= q <= 321007), "the lexiarc sizes cover every prime power 3..321007"
    assert not any(lex[q] < small[q] for q in small if q in lex)
    best = dict(lex)
    best.update(small)
    rows, out_slow, solved = [], [], []
    for q in sorted(best):
        ph = PP[q]
        if q <= 32:
            solved.append(q)
            continue
        if arc_check_seconds(q, best[q] - 1, ph) > LIMIT_SECONDS:
            out_slow.append(q)
            continue
        b = lower_bound(q, ph)
        assert best[q] > b
        src = holder(q, tables.get(q, set())) if q in small else "complete lexiarc, arXiv:1404.0469v3"
        rows.append({"id": f"arc-{q}", "params": {"q": q, "p": ph[0], "h": ph[1]}, "best": str(best[q]),
                     "bound": f"{b} (t_2(2,q) > " + ("sqrt(3q) + 1/2" if ph[1] <= 3 else "sqrt(2q) + 1") + ")",
                     "holder": src})
    defn = {
        "family": "complete-arc",
        "title": "Smallest complete arcs in the projective planes PG(2,q)",
        "added": "2.2",
        "objective": "minimize",
        "id_prefixes": ["arc-"],
        "keeper": ("D. Bartoli, A. A. Davydov, G. Faina, A. A. Kreshchuk, S. Marcugini and F. Pambianco, tables of the "
                   "smallest known sizes of complete arcs in PG(2,q) (arXiv:1312.2155v3) and of complete lexiarcs "
                   "(arXiv:1404.0469v3)"),
        "page": "https://arxiv.org/abs/1312.2155v3",
        "cell_url": "https://arxiv.org/abs/1312.2155v3",
        "read": read,
        "revision": ("arXiv:1312.2155v3 (28 Jun 2015; smallest known sizes collected up to June 2015; Tables 1-6) and "
                     "arXiv:1404.0469v3 (3 Jan 2018; complete lexiarcs for all q <= 321007; Tables 1-6), both PDFs "
                     f"downloaded {read} (SHA-256 in pdf_sha256)"),
        "template": {
            "title": "Complete arc in PG(2,{q})",
            "statement": ("Find a complete arc in the projective plane PG(2,{q}) with as few points as possible: a set "
                          "of points of PG(2,{q}), no three on a line, such that every other point of the plane lies "
                          "on a line through two of them. The smallest size t_2(2,{q}) is not known (exact values are "
                          "known only for q <= 32)."),
            "submission": ("Text file: one point per line, three integers x y z (homogeneous coordinates in GF({q}), "
                           "0 <= x, y, z < {q}, not all 0). For q = p^h with h > 1 the first line is \"poly c_0 c_1 "
                           "... c_h\", a monic irreducible polynomial over GF(p) (lowest coefficient first), and an "
                           "element is the integer whose base-p digits are its coefficients. See "
                           "checkers/arc_check.py."),
            "args": ["{q}"],
        },
        "checker": {"program": "arc_check.py", "value": "result"},
        "score": "the number of points of a complete arc (smaller is better)",
        "best_text": ("The smallest known complete arc in PG(2,{q}) has {best} points ({holder}); a complete arc with "
                      "fewer points improves it."),
        "bound_kind": "lower bound",
        "bound_source": ("t_2(2,q) > sqrt(2q) + 1 for every q, and t_2(2,q) > sqrt(3q) + 1/2 for q = p^h with h <= 3 "
                         "(arXiv:1312.2155v3, (1.2), with its references)"),
        "holder_unknown": "the authors' collection (the sources of each size are in arXiv:1312.2155v3, Section 2)",
        "holder_sources": ("arXiv:1312.2155v3 collects the smallest known sizes from many papers (its Section 2 and "
                           "references); most are the authors' own randomized greedy searches, Table 1's sizes for q "
                           "<= 151 are N. Pace's (J. Combin. Des. 22, 2014)"),
        "open_rule": ("every prime power 32 < q whose best known size (the smallest in either paper) is above the "
                      "lower bound (all are), kept when the check of a complete arc one point smaller is estimated at "
                      f"most {LIMIT_SECONDS} s (arc_check_seconds in tools/arcs_cells.py)"),
        "left_out": (f"{len(solved)} prime powers q <= 32 (t_2(2,q) known exactly); {len(out_slow)} prime powers "
                     f"q from {min(out_slow)} to {max(out_slow)} whose check is estimated above {LIMIT_SECONDS} s "
                     "(the papers list every prime power to 321007 and sporadic q to 430007)"),
        "literature": "families/complete-arc/literature.json",
        "pdf_sha256": {"1312.2155v3.pdf": hashlib.sha256(open(small_pdf, "rb").read()).hexdigest(),
                       "1404.0469v3.pdf": hashlib.sha256(open(lex_pdf, "rb").read()).hexdigest()},
        "counts": {"smallest known sizes": len(small), "lexiarc sizes": len(lex), "prime powers listed": len(best),
                   "solved (q <= 32)": len(solved), "check too long": len(out_slow), "cells": len(rows),
                   "cells with q = p^h, h > 1": sum(1 for r in rows if r["params"]["h"] > 1)},
    }
    return defn, rows


if __name__ == "__main__":
    res = main()
    if isinstance(res, int):
        sys.exit(res)
    defn, rows = res
    write_family(defn, rows)
    print(json.dumps(defn["counts"]))
