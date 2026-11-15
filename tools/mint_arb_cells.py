"""mint_arb_cells.py: the MinT cells for arbitrary (not necessarily linear) objects with few runs, as the benchmark
family orthogonal-array, checked by checkers/oa_check.py (the runs themselves).

  python3 -I mint_arb_cells.py PAGES_DIR READ REVISION     (writes families/orthogonal-array/)

PAGES_DIR holds the MinT pages saved by mint_fetch.py (both kinds: arbitrary objects and, with the suffix _lin, linear
ones). A cell (b, T, m, k) of the tables for arbitrary objects is open when the best known object has fewer factors
than MinT's bound for arbitrary objects. It is kept when (1) b^m <= 2^16 runs (a submission lists every run),
(2) checking one more factor than the best known takes at most 2^33 steps (the number of choices of depths times b^m),
and (3) its best known value or its bound differs from those of the same cell for linear objects: where both agree,
the cell of the family ordered-orthogonal-array (linear objects) asks nearly the same question, and the cell is left
out here so that no question is asked twice in effect."""
import glob
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS, WORK = 2 ** 16, 2 ** 33


def main():
    pages, read, revision = sys.argv[1:4]
    src = open(os.path.join(HERE, "mint_cells.py")).read().split("anyc, cells = {}, {}")[0]
    ns = {"__name__": "mint_cells_parse"}
    saved = sys.argv
    sys.argv = ["mint_cells.py", pages, os.devnull]
    exec(compile(src, "mint_cells.py", "exec"), ns)
    sys.argv = saved
    parse, count_depth_vectors = ns["parse"], ns["count_depth_vectors"]
    anyc, lin = {}, {}
    for fn in sorted(glob.glob(os.path.join(pages, "b*_de*_m3_k*.html"))):
        (lin if fn.endswith("_lin.html") else anyc).update(parse(fn))
    stats = dict(read=len(anyc), solved=0, small_k=0, many_runs=0, too_costly=0, same_as_linear=0, kept=0)
    rows = []
    for (b, T, m, k), (lo, hi) in sorted(anyc.items(), key=lambda x: (x[0][0], str(x[0][1]), x[0][2], x[0][3])):
        if k < 3 or m < k:
            stats["small_k"] += 1
            continue
        if lo >= hi:
            stats["solved"] += 1
            continue
        if b ** m > RUNS:
            stats["many_runs"] += 1
            continue
        s = lo + 1
        t = k if T == "net" else min(T, k)
        if count_depth_vectors(s, t, k, WORK) * b ** m > WORK:
            stats["too_costly"] += 1
            continue
        if lin.get((b, T, m, k)) == (lo, hi):
            stats["same_as_linear"] += 1
            continue
        cell = {"id": f"oa-b{b}-T{T}-m{m}-k{k}", "params": {"b": b, "T": T, "m": m, "k": k}, "best": str(lo),
                "bound": str(hi)}
        if (b, T, m, k) in lin:
            cell["linear"] = f"{lin[(b, T, m, k)][0]}-{lin[(b, T, m, k)][1]}"
        rows.append(cell)
        stats["kept"] += 1
    print(stats)
    fam = {
        "family": "orthogonal-array",
        "title": "Ordered orthogonal arrays and nets of any kind (not necessarily linear) with the largest number of factors",
        "added": "2.2", "objective": "maximize", "id_prefixes": ["oa-"],
        "keeper": "W. Ch. Schmid and R. Schuerer, MinT, the database of optimal net, code, OA and OOA parameters (mint.sbg.ac.at)",
        "page": "http://mint.sbg.ac.at/",
        "cell_url": "http://mint.sbg.ac.at/query.php?i=x&b={b}&m={m}&k={k}&p=mks&de={T}",
        "read": read, "revision": revision,
        "template": {
            "title": "Ordered orthogonal array of any kind with {b}^{m} runs, depth {T}, strength {k}",
            "statement": "Find an ordered orthogonal array (any array, linear or not) with {b}^{m} runs over {b} symbols, depth {T} and strength {k} that has as many factors as possible. Depth 1 is an orthogonal array; depth net is a ({m}-{k}, {m}, s)-net in base {b}, written by the first {k} base-{b} digits of each coordinate.",
            "submission": "Text file: the {b}^{m} runs, one per line, each the symbols (below {b}) of every factor in turn, {T} coordinates per factor in order of depth ({k} for depth net); see checkers/oa_check.py.",
            "args": ["{b}", "{T}", "{m}", "{k}"]},
        "checker": {"program": "oa_check.py", "value": "result"},
        "score": "the number of factors (larger is better)",
        "best_text": "The best known object of any kind in MinT has {best} factors; an array with more factors improves it.",
        "bound_kind": "upper bound", "bound_source": "MinT's bound for arbitrary objects in the same cell",
        "holder_unknown": "the construction and its source are on the cell's page at MinT",
        "holder_sources": "the tables list values only; each cell's page names its construction",
        "open_rule": "every cell with 3 <= k <= m of the MinT tables for arbitrary objects whose best known object has fewer factors than MinT's bound for arbitrary objects, with at most 2^16 runs, whose check takes at most 2^33 steps, and whose best known value or bound differs from the linear cell's (field linear: the linear cell's values)",
        "left_out": f"{stats['solved']} solved cells; {stats['many_runs']} open cells with more than 2^16 runs; {stats['too_costly']} open cells whose check would take more than 2^33 steps; {stats['same_as_linear']} open cells whose best known value and bound equal those of the linear cell (asked in ordered-orthogonal-array); cells with k < 3 or m < k",
        "cells": "cells.jsonl", "count": len(rows), "quantavane_records": 0, "single_problems_left_out": 0,
    }
    root = os.path.dirname(HERE)
    d = os.path.join(root, "families", "orthogonal-array")
    os.makedirs(d, exist_ok=True)
    json.dump(fam, open(os.path.join(d, "family.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(d, "cells.jsonl"), "w") as f:
        for c in rows:
            f.write(json.dumps(c) + "\n")
    print("family written:", len(rows))


if __name__ == "__main__":
    main()
