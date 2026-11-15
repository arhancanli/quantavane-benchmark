"""combwiki_dd_cells.py: the Combinatorics Wiki's tables of the largest known circulant graphs and bipartite graphs of
given maximum degree and diameter as the benchmark families circulant-degree-diameter (checked by
checkers/circulant_check.py) and bipartite-degree-diameter (checkers/degdiam_check.py --bipartite).

  python3 -I combwiki_dd_cells.py PAGES_DIR READ REVISION

PAGES_DIR holds The_Degree_Diameter_Problem_for_Circulant_Graphs.html and
The_Degree_Diameter_Problem_for_Bipartite_Graphs.html saved from combinatoricswiki.org/wiki/. In each page's first
table (degree d by rows, diameter k by columns) bold numbers are known to be optimal; a cell is an entry not in bold.
The colour of an entry names who found the graph (the page's colour key). Bipartite cells have at most 20,000
vertices (degdiam_check.py keeps a bit set per vertex); circulant graphs are checked from one vertex, so all are
kept."""
import hashlib
import html
import json
import os
import re
import sys

PAGES = {"circulant": "The_Degree_Diameter_Problem_for_Circulant_Graphs.html",
         "bipartite": "The_Degree_Diameter_Problem_for_Bipartite_Graphs.html"}


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def parse(page):
    tabs = re.findall(r"<table.*?</table>", page, re.S)
    rows = re.findall(r"<tr.*?</tr>", tabs[0], re.S)
    ks = [int(x) for x in [text(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", rows[0], re.S)][1:]]
    cells = []
    for r in rows[1:]:
        tds = re.findall(r"<td([^>]*)>(.*?)</td>", r, re.S)
        d = int(text(tds[0][1]))
        for (attr, body), k in zip(tds[1:], ks):
            m = re.search(r"background-color:\s*([^;\"]+)", attr)
            val = text(body).replace(" ", "")
            if val:
                cells.append((d, k, int(val), "<b>" in body, m[1].strip().lower() if m else ""))
    key = {}
    for attr, desc in re.findall(r"<tr>\s*<td style=\"background-color:\s*([^;\"]+);[^\"]*\"[^>]*>.*?</td>\s*<td>(.*?)</td>",
                                 tabs[1], re.S):
        key[attr.strip().lower()] = text(desc).rstrip(".")
    return cells, key


def main():
    pages, read, revision = sys.argv[1:4]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for kind, fn in PAGES.items():
        raw = open(os.path.join(pages, fn), "rb").read()
        cells, key = parse(raw.decode("utf-8"))
        rows, stats = [], {"entries": len(cells), "optimal (bold)": 0, "more than 20,000 vertices": 0}
        for d, k, val, bold, colour in cells:
            if bold:
                stats["optimal (bold)"] += 1
                continue
            if kind == "bipartite" and val > 20000:
                stats["more than 20,000 vertices"] += 1
                continue
            holder = key.get(colour)
            assert holder, (kind, d, k, colour)
            prefix = "circdd" if kind == "circulant" else "bipdd"
            rows.append({"id": f"{prefix}-{d}-{k}", "params": {"d": d, "k": k}, "best": str(val), "holder": holder})
        stats["kept"] = len(rows)
        print(kind, stats)
        if kind == "circulant":
            fam = {
                "family": "circulant-degree-diameter",
                "title": "The degree-diameter problem for circulant graphs",
                "id_prefixes": ["circdd-"],
                "template": {
                    "title": "Circulant graph of degree {d} and diameter {k}",
                    "statement": "Find a circulant graph C_n(S) (vertices 0..n-1, x joined to x + s and x - s modulo n "
                                 "for every jump s in S) of degree at most {d} and diameter at most {k}, with as many "
                                 "vertices n as possible.",
                    "submission": "Text file: n on the first line, then the jumps (integers separated by spaces); see "
                                  "checkers/circulant_check.py.",
                    "args": ["{d}", "{k}"]},
                "checker": {"program": "circulant_check.py", "value": "result"},
                "best_text": "The largest known circulant graph in the Combinatorics Wiki's table has {best} vertices "
                             "({holder}); a graph with more vertices improves it.",
                "open_rule": f"every entry of the table (degree {min(c[0] for c in cells)} to {max(c[0] for c in cells)}, "
                             f"diameter {min(c[1] for c in cells)} to {max(c[1] for c in cells)}) not in bold (bold "
                             "entries are known to be optimal)",
            }
        else:
            fam = {
                "family": "bipartite-degree-diameter",
                "title": "The degree-diameter problem for bipartite graphs",
                "id_prefixes": ["bipdd-"],
                "template": {
                    "title": "Bipartite graph of maximum degree {d} and diameter {k}",
                    "statement": "Find a bipartite graph of maximum degree at most {d} and diameter at most {k}, with "
                                 "as many vertices as possible.",
                    "submission": "Text file: one graph in graph6 or sparse6, or an edge list (one edge \"u v\" per "
                                  "line, vertices numbered from 0).",
                    "args": ["{d}", "{k}", "--bipartite"]},
                "checker": {"program": "degdiam_check.py", "value": "result"},
                "best_text": "The largest known bipartite graph in the Combinatorics Wiki's table has {best} vertices "
                             "({holder}); a graph with more vertices improves it.",
                "open_rule": f"every entry of the table (degree {min(c[0] for c in cells)} to {max(c[0] for c in cells)}, "
                             f"diameter {min(c[1] for c in cells)} to {max(c[1] for c in cells)}) not in bold (bold "
                             "entries are optimal), with at most 20,000 vertices",
            }
        fam.update({
            "added": "2.2", "objective": "maximize",
            "keeper": "Combinatorics Wiki (E. Loz, H. Pérez-Rosés, G. Pineda-Villavicencio and contributors), "
                      f"The Degree Diameter Problem for {kind.capitalize()} Graphs",
            "page": "http://combinatoricswiki.org/wiki/" + fn[:-5],
            "read": read, "revision": revision, "page_sha256": hashlib.sha256(raw).hexdigest(),
            "score": "the number of vertices (larger is better)",
            "holder_unknown": "not named in the table's colour key",
            "holder_sources": "the colour of the entry in the table and the page's colour key",
            "left_out": ", ".join(f"{v} {k}" for k, v in stats.items() if k not in ("entries", "kept")),
            "cells": "cells.jsonl", "count": len(rows), "quantavane_records": 0, "single_problems_left_out": 0,
        })
        d = os.path.join(root, "families", fam["family"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "family.json"), "w") as f:
            f.write(json.dumps(fam, indent=1, ensure_ascii=False) + "\n")
        with open(os.path.join(d, "cells.jsonl"), "w") as f:
            for c in rows:
                f.write(json.dumps(c, ensure_ascii=False, separators=(", ", ": ")) + "\n")


if __name__ == "__main__":
    main()
