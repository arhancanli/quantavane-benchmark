"""mols_cells.py: lower bounds on the number N(n) of mutually orthogonal Latin squares of order n as the benchmark
family mols (checked by checkers/mols_check.py).

  python3 -I mols_cells.py MOLS_HANDBOOK_DATA_PY READ REVISION

MOLS_HANDBOOK_DATA_PY is SageMath's module src/sage/combinat/designs/MOLS_handbook_data.py: Table 3.87 of the
Handbook of Combinatorial Designs (2nd edition, 2007; R. J. R. Abel, C. J. Colbourn and J. H. Dinitz), lower bounds on
N(n) for n < 10,000, with the two updates of J. H. Dinitz's website. families/mols/literature.json holds the values
published since (Dukes and Ling 2014; Abel, Janiszczak and Staszewski 2024; Rosin 2026); the larger value counts.

N(n) = n - 1 for prime powers and N(6) = 1, and no other value is known: every other n is open (N(n) <= n - 1, and
<= n - 2 when the Bruck-Ryser theorem rules out a projective plane of order n). A cell is kept when n >= 500, or n <
500 and its current value is known from literature.json (the 2024 compilation for n < 500 could not be read). A
submission is either the squares or a difference matrix (checkers/mols_check.py), so every order below 10,000 can be
checked: a difference matrix for K squares of order n has (K + 2) n entries."""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from import_families import write_family  # noqa: E402

MAX_SYMBOLS = 10 ** 8


def handbook(path):
    src = open(path).read()
    body = src[src.index("_LOWER_BOUNDS = (") + len("_LOWER_BOUNDS = ("):]
    body = body[:body.index(")")]
    vals = [int(x) for x in re.sub(r"#[^\n]*", "", body).replace("\n", "").replace(" ", "").split(",") if x]
    assert len(vals) == 10000
    return vals


def prime_power(n):
    p = next((d for d in range(2, int(n ** 0.5) + 1) if n % d == 0), n)
    while n % p == 0:
        n //= p
    return n == 1


def sum_of_two_squares(n):
    return any(int((n - a * a) ** 0.5) ** 2 == n - a * a for a in range(int(n ** 0.5) + 1))


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    path, read, revision = sys.argv[1:]
    hb = handbook(path)
    lit = json.load(open(os.path.join(ROOT, "families", "mols", "literature.json")))
    upd = {u["n"]: u for u in lit["updates"]}
    known_below = set(lit["known_below_500"])
    assert all(hb[n] == n - 1 for n in range(2, 10000) if prime_power(n))
    rows, small, big, prime_powers = [], 0, 0, 0
    for n in range(10, 10000):
        if prime_power(n):
            prime_powers += 1
            continue
        if n < 500 and n not in known_below:
            small += 1
            continue
        best, holder = hb[n], "Handbook of Combinatorial Designs (2007), Table 3.87 (Abel, Colbourn and Dinitz)"
        if n in (60, 7968):
            holder = "Handbook Table 3.87 as updated on J. H. Dinitz's website (R. J. R. Abel)"
        if n in upd and upd[n]["value"] > best:
            best, holder = upd[n]["value"], upd[n]["source"].split(",")[0] + (
                ", arXiv:2611.16299 (2026)" if "Rosin" in upd[n]["source"] else
                ", arXiv:2412.00480 (2024)" if "Janiszczak" in upd[n]["source"] else
                ", arXiv:1401.1466 (2014)")
        if (best + 1) * n * n > MAX_SYMBOLS:
            big += 1          # counted only: these need a difference matrix in practice
        plane_ruled_out = n % 4 in (1, 2) and not sum_of_two_squares(n)
        bound = f"{n - 2} (no projective plane of order {n}: Bruck-Ryser)" if plane_ruled_out else f"{n - 1} (n - 1)"
        rows.append({"id": f"mols-{n}", "params": {"n": n}, "best": str(best), "bound": bound, "holder": holder})
    defn = {
        "family": "mols",
        "title": "Mutually orthogonal Latin squares: the most squares of order n",
        "added": "2.2",
        "objective": "maximize",
        "id_prefixes": ["mols-"],
        "keeper": ("Handbook of Combinatorial Designs, Table 3.87 (R. J. R. Abel, C. J. Colbourn and J. H. Dinitz), as "
                   "in SageMath's MOLS_handbook_data, with the later results of families/mols/literature.json"),
        "page": "https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/designs/MOLS_handbook_data.html",
        "cell_url": "https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/designs/MOLS_handbook_data.html",
        "read": read,
        "revision": revision,
        "template": {
            "title": "Mutually orthogonal Latin squares of order {n}",
            "statement": ("Find as many mutually orthogonal Latin squares of order {n} as possible: Latin squares "
                          "that, taken two at a time and superimposed, show each of the {n}^2 ordered pairs of "
                          "symbols exactly once. N({n}) is not known."),
            "submission": ("Text file: K Latin squares of order {n} one after another, each {n} rows of {n} symbols "
                           "0..{n_minus_1} (or 1..{n}) separated by spaces; '#' starts a comment; an optional first "
                           "line \"{n} K\". Or an ({n}, K + 2; 1) difference matrix: a first line \"group n_1 ... "
                           "n_r\" (an abelian group Z_n1 x ... x Z_nr of order {n}), then K + 2 rows of {n} elements "
                           "written as integers 0..{n_minus_1} in mixed radix. See checkers/mols_check.py."),
            "args": ["{n}"],
        },
        "checker": {"program": "mols_check.py", "value": "result"},
        "score": "K, the number of mutually orthogonal Latin squares (larger is better)",
        "best_text": "The best known lower bound is N({n}) >= {best} ({holder}); {best_plus_1} squares would improve it.",
        "bound_kind": "upper bound",
        "bound_source": ("N(n) <= n - 1, with equality exactly when a projective plane of order n exists; N(n) <= n - 2 "
                         "when the Bruck-Ryser theorem excludes a plane of order n"),
        "holder_unknown": "Handbook of Combinatorial Designs (2007), Table 3.87",
        "holder_sources": "the Handbook table (constructions in its Section III.3) and literature.json",
        "open_rule": ("every order n that is not a prime power, n > 6 (N(n) is known only for prime powers and n = 6), "
                      "with n >= 500 or a value for n < 500 known from literature.json; a submission is the squares or a "
                      "difference matrix"),
        "left_out": (f"{prime_powers} prime powers (N(n) = n - 1); n = 10 (the single problem mols-10); {small - 1} "
                     f"other orders below 500 whose current value is in the 2024 compilation, which could not be "
                     f"read (an owner step: the paper is open access)"),
        "literature": "families/mols/literature.json",
        "source_sha256": {"MOLS_handbook_data.py": hashlib.sha256(open(path, "rb").read()).hexdigest()},
        "counts": {"orders 10..9999 not prime powers": 9990 - prime_powers, "below 500 not known": small,
                   "cells needing a difference matrix in practice (an improving set of squares above 10^8 symbols)": big,
                   "cells": len(rows)},
    }
    for r in rows:
        r["params"]["n_minus_1"] = r["params"]["n"] - 1
        r["params"]["best_plus_1"] = int(r["best"]) + 1
    return defn, rows


if __name__ == "__main__":
    res = main()
    if isinstance(res, int):
        sys.exit(res)
    defn, rows = res
    write_family(defn, rows)
    print(json.dumps(defn["counts"]))
