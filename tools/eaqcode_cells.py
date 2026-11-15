"""eaqcode_cells.py: Markus Grassl's tables of entanglement-assisted quantum codes (eaqecc.codetables.de) as the
benchmark family ea-quantum-code, checked by checkers/qcode_check.py --ebits C.

  python3 -I eaqcode_cells.py QUBIT.html QUTRIT.html READ REVISION     (writes families/ea-quantum-code/)

A cell [[n,k;c]] (c >= 1) is open when its lower bound is below its upper bound. Entries with c = 0 are left out: they
are the stabilizer codes of the family quantum-code. A cell is kept when the exact check lists at most 2^34 elements
(2^(n-k+c), qubits) or 2^31 lines through the origin ((3^(n-k+c) - 1)/2, qutrits), or, from 15 Nov 2026, when its
estimated time with the faster lister (the time model of qcode_cells.py, for S and its isotropic part) is at most 60 s.
The table names each entry's
construction (a propagation rule or a source) in the cell's title; it is kept as the holder. Only values are stored."""
import collections
import hashlib
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qcode_cells import LIMIT_SECONDS, check_seconds  # noqa: E402

CELL = re.compile(r'<TD[^>]*title="([^"]*)"[^>]*>\[\[(\d+),(\d+),(\d+)(?:-(\d+))?;(\d+)\]\]')


def main():
    qubit, qutrit, read, revision = sys.argv[1:5]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rows, stats, shas = [], {}, {}
    for Q, path in ((2, qubit), (3, qutrit)):
        raw = open(path, "rb").read()
        shas[str(Q)] = hashlib.sha256(raw).hexdigest()
        text = raw.decode("latin-1")
        st = collections.Counter()
        seen = {}
        for title, n, k, lo, hi, c in CELL.findall(text):
            n, k, lo, c = int(n), int(k), int(lo), int(c)
            hi = int(hi) if hi else lo
            seen[(n, k, c)] = (lo, hi, html.unescape(title).strip())
        assert len(seen) > 1000, path
        for (n, k, c), (lo, hi, title) in sorted(seen.items()):
            st["entries"] += 1
            if c == 0:
                st["c = 0 (stabilizer codes, in quantum-code)"] += 1
                continue
            if lo >= hi:
                st["solved"] += 1
                continue
            r = n - k + c
            work = 2 ** r if Q == 2 else (3 ** r - 1) // 2
            if work > (2 ** 34 if Q == 2 else 2 ** 31):
                sec = check_seconds(Q, n, r)
                if sec is None or sec * (1 + Q ** (-2 * c)) > LIMIT_SECONDS:
                    st["too costly to check"] += 1
                    continue
                st["kept with the faster lister (15 Nov 2026)"] += 1
            rows.append({"id": f"eaqcode-q{Q}-n{n}-k{k}-c{c}", "params": {"q": Q, "n": n, "k": k, "c": c},
                         "best": str(lo), "bound": str(hi), "holder": f"construction in the table: {title}"})
            st["kept"] += 1
        stats[Q] = st
        print(Q, dict(st))
    fam = {
        "family": "ea-quantum-code",
        "title": "Entanglement-assisted quantum codes [[n,k;c]] with the largest minimum distance",
        "added": "2.2", "objective": "maximize", "id_prefixes": ["eaqcode-"],
        "keeper": "M. Grassl, bounds on the minimum distance of entanglement-assisted quantum codes (eaqecc.codetables.de)",
        "page": "https://eaqecc.codetables.de/",
        "read": read, "revision": revision,
        "template": {
            "title": "Entanglement-assisted quantum code [[{n},{k};{c}]] over GF({q})",
            "statement": "Find an entanglement-assisted quantum code of length {n} with local dimension {q} that encodes {k} qudits "
                         "with the help of {c} maximally entangled pairs and whose minimum distance is as large as possible. It "
                         "is given by an additive group S of {q}^({n}-{k}+{c}) elements of GF({q})^(2 x {n}) on which the "
                         "trace-symplectic form has rank 2 x {c}; the distance is the least symplectic weight of "
                         "an element of the trace-symplectic dual S' of S that is not in S (for k = 0: of a nonzero element "
                         "of S', or n + 1 when S' = 0), as in Luo, Ezerman, Grassl and Ling, arXiv:2207.05647.",
            "submission": "Text file: the generators of S, one per line, 2 x {n} elements of GF({q}) (the X part, then the Z part; "
                          "a '|' between them is allowed) written as integers below {q}; see checkers/qcode_check.py.",
            "args": ["{q}", "{n}", "{k}", "--ebits", "{c}"],
        },
        "checker": {"program": "qcode_check.py", "value": "result"},
        "score": "the minimum distance (larger is better)",
        "best_text": "The best known lower bound in the table is {best} ({holder}); a code with a larger minimum distance improves it.",
        "bound_kind": "upper bound", "bound_source": "the upper bound in the same table",
        "holder_unknown": "the table names the construction of each entry",
        "holder_sources": "the construction named in the entry's cell of the table (a propagation rule from another entry, a "
                          "known family, or a source)",
        "open_rule": "every entry with c >= 1 whose lower bound is below its upper bound",
        "work_rule": "kept when the check lists at most 2^34 elements of S (qubits, n - k + c <= 34) or 2^31 lines through the "
                     "origin (qutrits, n - k + c <= 20); from 15 Nov 2026 also when the estimated check with the faster "
                     "lister (S and its isotropic part; the measured time model of tools/qcode_cells.py) takes at most 60 s",
        "left_out": "; ".join(f"q = {Q}: " + ", ".join(f"{v} {k}" for k, v in st.items() if k not in ("entries", "kept", "kept with the faster lister (15 Nov 2026)"))
                              for Q, st in stats.items()),
        "page_sha256": shas,
        "cells": "cells.jsonl", "count": len(rows), "quantavane_records": 0, "single_problems_left_out": 0,
    }
    d = os.path.join(root, "families", "ea-quantum-code")
    os.makedirs(d, exist_ok=True)
    json.dump(fam, open(os.path.join(d, "family.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(d, "cells.jsonl"), "w") as f:
        for c in rows:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print("family written:", len(rows))


if __name__ == "__main__":
    main()
