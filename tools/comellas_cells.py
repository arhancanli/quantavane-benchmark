"""comellas_cells.py: F. Comellas's table of the largest known (degree, diameter) graphs as the benchmark family
degree-diameter, checked by checkers/degdiam_check.py.

  python3 -I comellas_cells.py TABLE.html READ REVISION     (writes families/degree-diameter/)

TABLE.html is the page delta-d/table_degree_diameter.html (degree 3 to 16, diameter 2 to 10). A cell is open when its
entry is not in boldface (the page: "Entries in boldface are optimal"). Cells whose best known graph has more than
20,000 vertices are left out (the check keeps a ball of every vertex as a bit set: n^2 bits). Cells that are already
single problems (degdiam-D-K in problems/) are kept only there."""
import hashlib
import html
import json
import os
import re
import sys

LIMIT = 20000


def main():
    page, read, revision = sys.argv[1:4]
    raw = open(page, "rb").read()
    s = raw.decode("utf-8", "replace")
    i = s.lower().find("<table")
    j = s.lower().find("</table>", i)
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", s[i:j], re.S | re.I)
    grid = [[(c, re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", "", c))).strip())
             for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S | re.I)] for r in rows]
    diams = [int(x[1]) for x in grid[0][1:]]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    singles = {f[:-5] for f in os.listdir(os.path.join(root, "problems")) if f.endswith(".json")}
    out, stats = [], {"entries": 0, "optimal (bold)": 0, "more than 20,000 vertices": 0, "single problems": 0}
    for g in grid[1:]:
        delta = int(g[0][1])
        for col, (cell, txt) in enumerate(g[1:]):
            num = re.sub(r"[^0-9]", "", txt)
            if not num:
                continue
            stats["entries"] += 1
            d = diams[col]
            n = int(num)
            if re.search(r"<b>|<strong>", cell, re.I):
                stats["optimal (bold)"] += 1
                continue
            if n > LIMIT:
                stats["more than 20,000 vertices"] += 1
                continue
            cid = f"degdiam-{delta}-{d}"
            if cid in singles:
                stats["single problems"] += 1
                continue
            cell_out = {"id": cid, "params": {"delta": delta, "d": d}, "best": str(n)}
            if "*" in txt or "∗" in txt:
                cell_out["holder"] = "a Cayley graph (the table's mark); see the entry's page"
            out.append(cell_out)
    print(stats, len(out))
    fam = {
        "family": "degree-diameter", "title": "The degree-diameter problem: large graphs of given maximum degree and diameter",
        "added": "2.2", "objective": "maximize", "id_prefixes": ["degdiam-"],
        "keeper": "F. Comellas, The (Degree, Diameter) Problem for Graphs (web.mat.upc.edu/francesc.comellas/delta-d)",
        "page": "https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html",
        "read": read, "revision": revision,
        "template": {"title": "Degree-diameter problem ({delta},{d}): a large graph of maximum degree {delta} and diameter {d}",
                     "statement": "Find a graph with maximum degree at most {delta} and diameter at most {d}, with as many vertices as possible.",
                     "submission": "Text file: one graph in graph6 or sparse6, or an edge list, one edge \"u v\" per line, vertices numbered from 0; see checkers/degdiam_check.py.",
                     "args": ["{delta}", "{d}"]},
        "checker": {"program": "degdiam_check.py", "value": "result"},
        "score": "the number of vertices (larger is better)",
        "best_text": "The largest known graph in Comellas's table has {best} vertices ({holder}); a graph with more vertices improves it.",
        "bound_kind": "upper bound", "bound_source": "the Moore bound 1 + delta (sum of (delta-1)^i, i < d), not reached (not a cell field)",
        "holder_unknown": "named on the entry's page in the table",
        "holder_sources": "each entry's page (desc_g/...) names the graph and its authors",
        "open_rule": "every entry of the table (degree 3 to 16, diameter 2 to 10) not in boldface, with at most 20,000 vertices",
        "left_out": ", ".join(f"{v} {k}" for k, v in stats.items() if k != "entries"),
        "page_sha256": hashlib.sha256(raw).hexdigest(),
        "cells": "cells.jsonl", "count": len(out), "quantavane_records": 0, "single_problems_left_out": stats["single problems"],
    }
    d = os.path.join(root, "families", "degree-diameter")
    os.makedirs(d, exist_ok=True)
    json.dump(fam, open(os.path.join(d, "family.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(d, "cells.jsonl"), "w") as f:
        for c in out:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
