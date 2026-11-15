"""qcode_cells.py: Markus Grassl's tables of quantum codes (codetables.de) as the benchmark family quantum-code.

  python3 -I qcode_cells.py PAGES_DIR OUTSIDE.json READ REVISION     (writes families/quantum-code/)

PAGES_DIR holds the range pages of the tables (QECC/Tables_color.php, saved as tables_qTQ_nA-B_kC-D_DAY.html, where
TQ = Q^2 is the q of the site's URLs: 4 for qubits, 9 for qutrits, 16, 25, 49, 64 for local dimension 4, 5, 7, 8).
Only cell values are stored, with the keeper credited. A cell [[n,k]] is open when its lower bound is below its upper
bound. It is kept when an exact check of a code with these parameters (checkers/qcode_check.py: list the stabilizer,
then MacWilliams) takes at most a minute: until 15 Nov 2026 the rule was at most WORK steps, Q^(n-k) for Q = 2, 4, 8
(WORK = 2^34, 47 s for qubits of length <= 64 with the lister of that day) and (Q^(n-k) - 1)/(Q - 1) for Q = 3, 5, 7
(WORK = 2^31, 30 to 60 s). From 16 Nov 2026 the C helper qcode_enum.c tabulates the combinations of the last
generators (and slices GF(3) into bit planes), and a cell is kept when its estimated check time, the number of
elements listed times the measured time per element for its field and length (NS_PER, measured 16 Nov 2026 under
load, user time) plus the measured MacWilliams step, is at most 60 s; Q = 5, 7 keep the old rule (their lister is
unchanged).

OUTSIDE.json lists codes published outside the table after its last change, as {"q": Q, "n", "k", "d", "source"}: a
cell whose outside code reaches the table's upper bound is closed and left out; otherwise the cell's best known value
is the outside code's distance when larger, credited to its source, with the table's value named."""
import collections
import glob
import hashlib
import json
import os
import re
import sys

LOCAL = {4: 2, 9: 3, 16: 4, 25: 5, 49: 7, 64: 8}
PRIME = {2: 2, 3: 3, 4: 2, 5: 5, 7: 7, 8: 2}
WORK2, WORKODD = 2 ** 34, 2 ** 31
LIMIT_SECONDS = 60
# ns per listed element (p = 2: every element; p = 3: every line), by Q and words per plane W = ceil(n / 64)
# (C helper alone at 2^30 elements, raised where full runs of qcode_check.py on the largest shapes took longer:
#  [[64,28]] qubits 42.2 s, [[128,93]] 32.1 s, [[200,165]] 57.1 s, [[256,221]] 63.3 s, [[64,46]] over GF(4) 54.2 s,
#  [[64,41]] over GF(3) 52.8 s, [[100,78]] over GF(3) 28.6 s)
NS_PER = {(2, 1): 0.62, (2, 2): 0.93, (2, 3): 1.25, (2, 4): 1.70, (4, 1): 0.80, (4, 2): 1.32, (8, 1): 1.03,
          (8, 2): 1.85, (3, 1): 1.12, (3, 2): 1.82}


def work(Q, r):
    return Q ** r if PRIME[Q] == 2 else (Q ** r - 1) // (Q - 1)


def macwilliams_seconds(n):
    """qcode_check.py's MacWilliams step in exact integers (Krawtchouk sums): about (n / 256)^3 x 5 s, measured (4.6 s for n = 256)."""
    return 5.0 * (n / 256) ** 3


def check_seconds(Q, n, r):
    """Estimated time of qcode_check.py on [[n, n - r]] over GF(Q) (None: the rule is the old step count)."""
    ns = NS_PER.get((Q, (n + 63) // 64))
    if ns is None:
        return None
    elements = Q ** r if PRIME[Q] == 2 else (Q ** r - 1) // 2
    # x 1.05 on top of rates taken from full runs
    return 1.05 * (elements * ns * 1e-9 + macwilliams_seconds(n))


def kept(Q, n, k):
    sec = check_seconds(Q, n, n - k)
    if sec is None:
        return work(Q, n - k) <= (WORK2 if PRIME[Q] == 2 else WORKODD)
    return sec <= LIMIT_SECONDS or work(Q, n - k) <= (WORK2 if PRIME[Q] == 2 else WORKODD)


def main():
    pages, outside_path, read, revision = sys.argv[1:5]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cells, shas, kinds = {}, {}, {}
    for fn in sorted(glob.glob(os.path.join(pages, "tables_q*_n*_k*_*.html"))):
        m = re.search(r"tables_q(\d+)_n(\d+)-(\d+)_k", os.path.basename(fn))
        tq = int(m.group(1))
        Q = LOCAL[tq]
        raw = open(fn, "rb").read()
        shas[os.path.basename(fn)] = hashlib.sha256(raw).hexdigest()
        text = raw.decode("latin-1")
        title = re.search(r"<TITLE>(.*?)</TITLE>", text, re.S).group(1).strip()
        kinds[Q] = title
        n_here = 0
        for n, k, cell in re.findall(r'title="n=(\d+), k=(\d+)"[^>]*>([^<]*)</A>', text):
            lo, _, hi = cell.strip().partition("-")
            if not lo.strip().isdigit():
                continue
            cells[(Q, int(n), int(k))] = (int(lo), int(hi) if hi.strip().isdigit() else int(lo))
            n_here += 1
        assert n_here > 50, fn
    outside = {}
    for o in json.load(open(outside_path)):
        key = (o["q"], o["n"], o["k"])
        if key not in outside or o["d"] > outside[key]["d"]:
            outside[key] = o
    rows, stats = [], collections.defaultdict(collections.Counter)
    for (Q, n, k), (lo, hi) in sorted(cells.items()):
        st = stats[Q]
        st["cells"] += 1
        if lo >= hi:
            st["solved"] += 1
            continue
        o = outside.get((Q, n, k))
        if o and o["d"] >= hi:
            st["closed outside the table"] += 1
            continue
        if not kept(Q, n, k):
            st["too costly to check"] += 1
            continue
        if work(Q, n - k) > (WORK2 if PRIME[Q] == 2 else WORKODD):
            st["kept with the faster lister (16 Nov 2026)"] += 1
        cell = {"id": f"qcode-q{Q}-n{n}-k{k}", "params": {"q": Q, "n": n, "k": k, "tq": Q * Q}}
        if o and o["d"] > lo:
            cell["best"] = str(o["d"])
            cell["bound"] = str(hi)
            cell["holder"] = f"{o['source']}; the table lists {lo}"
            st["best known raised by an outside code"] += 1
        else:
            cell["best"] = str(lo)
            cell["bound"] = str(hi)
        rows.append(cell)
        st["kept"] += 1
    fam_dir = os.path.join(root, "families", "quantum-code")
    os.makedirs(fam_dir, exist_ok=True)
    left = "; ".join(f"Q = {Q}: {stats[Q]['solved']} solved, {stats[Q]['closed outside the table']} closed by a code "
                     f"published outside the table, {stats[Q]['too costly to check']} too costly to check"
                     for Q in sorted(stats))
    fam = {
        "family": "quantum-code",
        "title": "Additive (stabilizer) quantum codes [[n,k]] over GF(q) with the largest minimum distance",
        "added": "2.2",
        "objective": "maximize",
        "id_prefixes": ["qcode-"],
        "keeper": "M. Grassl, bounds on the minimum distance of quantum codes (codetables.de)",
        "page": "https://www.codetables.de/",
        "cell_url": "https://www.codetables.de/QECC.php?q={tq}&n={n}&k={k}",
        "read": read,
        "revision": revision,
        "template": {
            "title": "Quantum code [[{n},{k}]] over GF({q})",
            "statement": "Find an additive (stabilizer) quantum code of length {n} with local dimension {q} that encodes "
                         "{k} qudits (a code space of dimension {q}^{k}) and whose minimum distance is as large as "
                         "possible. The stabilizer is an additive group of {q}^({n}-{k}) elements of GF({q})^(2 x {n}), "
                         "commutative under the trace-symplectic form. The distance is the least symplectic weight (the "
                         "number of positions where X or Z is not zero) of an element of the trace-symplectic dual "
                         "of the stabilizer that is not in the stabilizer (when no qudit is encoded: of a nonzero "
                         "element of the stabilizer).",
            "submission": "Text file: a stabilizer matrix, one generator per line, 2 x {n} elements of GF({q}) (the X "
                          "part, then the Z part; a '|' between them is allowed) written as integers below {q} (for q = "
                          "4 and 8 the binary digits of the integer are the coefficients of a polynomial in x modulo "
                          "x^2 + x + 1 or x^3 + x + 1). The lines generate the stabilizer over the prime field; see "
                          "checkers/qcode_check.py.",
            "args": ["{q}", "{n}", "{k}"],
        },
        "checker": {"program": "qcode_check.py", "value": "result"},
        "score": "the minimum distance (larger is better)",
        "best_text": "The best known lower bound is {best} ({holder}); a code with a larger minimum distance improves "
                     "it.",
        "bound_kind": "upper bound",
        "bound_source": "the upper bound in the same table",
        "holder_unknown": "the construction is on the entry's page at codetables.de",
        "holder_sources": "the range tables list values only; each entry's page names its construction. Codes "
                          "published after the table's last change are credited to their source (families/"
                          "quantum-code/outside.json)",
        "tables": {str(Q): kinds[Q] for Q in sorted(kinds)},
        "open_rule": "every entry whose lower bound is below its upper bound, unless a code published outside the "
                     "table reaches the upper bound",
        "work_rule": "kept when listing the stabilizer takes at most 2^34 steps (Q^(n-k), for Q = 2, 4, 8) or 2^31 "
                     "steps ((Q^(n-k) - 1)/(Q - 1), for Q = 3, 5, 7): n - k at most 34 for qubits, 20 for Q = 3, 17 "
                     "for Q = 4, 14 for Q = 5, 11 for Q = 7 and 11 for Q = 8; from 16 Nov 2026 also when the "
                     "estimated check with the faster lister (qcode_enum.c tabulates the combinations of the last "
                     "generators; GF(3) in bit planes) takes at most 60 s: the elements listed times the time per "
                     "element measured for Q and the length (tools/qcode_cells.py, NS_PER), plus the MacWilliams "
                     "step. That admits n - k = 35 for all qubit lengths and 36 for lengths up to 64, n - k = 18 "
                     "over GF(4) for lengths up to 64, and n - k = 21 to 23 over GF(3) (23 for lengths up to 64)",
        "left_out": left,
        "outside_sources": sorted({o["source"] for o in outside.values()}),
        "page_sha256": shas,
        "cells": "cells.jsonl",
        "count": len(rows),
        "quantavane_records": 0,
        "single_problems_left_out": 0,
    }
    json.dump(fam, open(os.path.join(fam_dir, "family.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(fam_dir, "cells.jsonl"), "w") as f:
        for c in rows:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    for Q in sorted(stats):
        print(Q, dict(stats[Q]))
    print(f"family written: {len(rows)} cells")


if __name__ == "__main__":
    main()
