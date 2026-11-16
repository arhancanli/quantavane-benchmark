"""combwiki_cayley_cells.py: the Combinatorics Wiki's table of the largest known Cayley graphs of given degree and
diameter as the benchmark family cayley-degree-diameter (checked by checkers/cayley_check.py).

  python3 -I combwiki_cayley_cells.py PAGE COMELLAS_DIR READ REVISION

PAGE is The_Degree_Diameter_Problem_for_Cayley_Graphs.html saved from combinatoricswiki.org/wiki/ (its first table:
degree d by rows, diameter k by columns; bold entries are known to be optimal; the colour of an entry names who found
the graph, in the page's colour key). A cell is an entry not in bold with at most MAX_ORDER vertices (larger entries
would need their own reconciliation with Comellas's pages: for instance his (16,7) Cayley graph of 14,995,367 vertices is
worded in a way the patterns below do not read). COMELLAS_DIR holds F. Comellas's pages
desc_g2.html to desc_g10.html (web.mat.upc.edu/francesc.comellas/delta-d/desc_g/); with families/cayley-degree-diameter/
literature.json they raise the wiki's values where a larger Cayley graph is described (see literature.json)."""
import hashlib
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from combwiki_dd_cells import parse  # noqa: E402
from import_families import write_family  # noqa: E402

MAX_ORDER = 10 ** 7


POS = [r"Cayley graphs? (for|of|over) (the |a )?(semidirect|metacyclic)", r"\b(is|as) a Cayley graph\b(?! on)",
       r"Cayley graphs?\s*\.\s*(Found|Obtained)", r"Cayley \? True", r"This Cayley graph is constructed",
       r"Cayley graph found through", r"[Oo]rder\s*=?\s*\d+\s*\.?\s*Cayley graph", r"non-isomorphic Cayley graphs",
       r"Cayley graph Z ", r"Obtained as a Cayley graph"]
NEG = [r"bi-Cayley", r"not (a )?Cayley", r"Cayley controller", r"Cayley hexagon", r"Cayley \? False",
       r"controller is the Cayley"]
GROUP = re.compile(r"Z\s*_?\s*(\d+)\s*(?:\(\s*⋊\s*\d+\s*\)|⋉\s*\d+|\(x\d+\)|x\|_\d+|\(x\s*\d+\))\s*Z\s*_?\s*(\d+)")


def comellas_cayley(folder, excluded):
    """{(d, k): (order, page, first words)}: the largest graph Comellas's pages describe as a Cayley graph"""
    best, sha = {}, {}
    for k in range(2, 11):
        fn = f"desc_g{k}.html"
        raw = open(os.path.join(folder, fn), "rb").read()
        sha[fn] = hashlib.sha256(raw).hexdigest()
        t = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw.decode("utf-8", errors="replace"))))
        hdr = list(re.finditer(r"Degree\s*=\s*(\d+)\s*,\s*Diameter\s*=\s*(\d+)\s*;\s*Order\s*=\s*(\d+)", t))
        for i, m in enumerate(hdr):
            blk = t[m.start():hdr[i + 1].start() if i + 1 < len(hdr) else len(t)]
            d, kk, order = map(int, m.groups())
            cuts = list(re.finditer(r"Former result,?\s*[Oo]rder\s*=?\s*(\d+)", blk))
            segs = [(order, blk[:cuts[0].start()] if cuts else blk)]
            segs += [(int(c.group(1)), blk[c.start():cuts[j + 1].start() if j + 1 < len(cuts) else len(blk)])
                     for j, c in enumerate(cuts)]
            for o, seg in segs:
                if (d, kk, o) in excluded or not any(re.search(p, seg) for p in POS) or any(re.search(p, seg) for p in NEG):
                    continue
                g = GROUP.search(seg)
                if g and int(g.group(1)) * int(g.group(2)) != o:
                    continue
                if o > best.get((d, kk), (0,))[0]:
                    best[(d, kk)] = (o, fn, " ".join(seg.split()[:12]))
    return best, sha


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        return 2
    page, comellas_dir, read, revision = sys.argv[1:]
    raw = open(page, "rb").read()
    cells, key = parse(raw.decode("utf-8"))
    lit = json.load(open(os.path.join(ROOT, "families", "cayley-degree-diameter", "literature.json")))
    solved = {(x["d"], x["k"]): x for x in lit["solved"]}
    papers = {(x["d"], x["k"]): x for x in lit["values"]}
    excluded = {(x["d"], x["k"], x["order"]) for x in lit["excluded_from_comellas"]}
    com, com_sha = comellas_cayley(comellas_dir, excluded)
    rows, st = [], {"entries": len(cells), "optimal (bold)": 0, "proven optimal since (Macaj 2026)": 0,
                    "raised by Comellas's pages": 0, "raised by a paper": 0, f"more than {MAX_ORDER:,} vertices": 0}
    for d, k, val, bold, colour in cells:
        if bold:
            st["optimal (bold)"] += 1
            continue
        if (d, k) in solved:
            st["proven optimal since (Macaj 2026)"] += 1
            continue
        holder = key.get(colour)
        assert holder, (d, k, colour)
        holder, src = f"{holder} (Combinatorics Wiki)", "wiki"
        if (d, k) in com and com[(d, k)][0] > val:
            val, src = com[(d, k)][0], "comellas"
            holder = (f"a Cayley graph of order {val} described in F. Comellas's table of the largest known "
                      f"(degree, diameter)-graphs ({com[(d, k)][1]}; its finder is named there)")
        if (d, k) in papers and papers[(d, k)]["value"] > val:
            val, src, holder = papers[(d, k)]["value"], "paper", papers[(d, k)]["source"]
        if val > MAX_ORDER:
            st[f"more than {MAX_ORDER:,} vertices"] += 1
            continue
        if src == "comellas":
            st["raised by Comellas's pages"] += 1
        elif src == "paper":
            st["raised by a paper"] += 1
        rows.append({"id": f"caydd-{d}-{k}", "params": {"d": d, "k": k}, "best": str(val), "holder": holder})
    st["kept"] = len(rows)
    defn = {
        "family": "cayley-degree-diameter",
        "title": "The degree-diameter problem for Cayley graphs",
        "added": "2.2",
        "objective": "maximize",
        "id_prefixes": ["caydd-"],
        "keeper": ("Combinatorics Wiki (E. Loz, H. Pérez-Rosés, G. Pineda-Villavicencio and contributors), The Degree "
                   "Diameter Problem for Cayley Graphs"),
        "page": "http://combinatoricswiki.org/wiki/The_Degree_Diameter_Problem_for_Cayley_Graphs",
        "read": read,
        "revision": revision,
        "page_sha256": hashlib.sha256(raw).hexdigest(),
        "comellas_sha256": com_sha,
        "literature": "families/cayley-degree-diameter/literature.json",
        "template": {
            "title": "Cayley graph of degree {d} and diameter {k}",
            "statement": ("Find a group G and a generating set S of G, closed under inverses and without the identity, "
                          "with |S| <= {d}, such that the Cayley graph Cay(G, S) has diameter at most {k}, with as "
                          "many vertices |G| as possible."),
            "submission": ("Text file: either 'points m', then the generators as permutations of 0..m-1, one per "
                           "line (the images of 0, 1, ..., m - 1), or 'semidirect m n a' (the group Z_m x|_a Z_n of "
                           "the table, [x, y][u, v] = [x + u mod m, y a^u + v mod n]), then the generators as pairs "
                           "'x y', one per line; see checkers/cayley_check.py."),
            "args": ["{d}", "{k}"],
        },
        "checker": {"program": "cayley_check.py", "value": "result"},
        "score": "the number of vertices, the order of G (larger is better)",
        "best_text": ("The largest known Cayley graph in the Combinatorics Wiki's table has {best} vertices ({holder}); "
                      "a Cayley graph with more vertices improves it."),
        "holder_unknown": "not named in the table's colour key",
        "holder_sources": ("the colour of the entry in the wiki's table and the page's colour key; for a raised value, "
                           "Comellas's entry or the paper"),
        "open_rule": (f"every entry of the table (degree {min(c[0] for c in cells)} to {max(c[0] for c in cells)}, "
                      f"diameter {min(c[1] for c in cells)} to {max(c[1] for c in cells)}) not in bold (bold entries "
                      f"are optimal) and not proven optimal since, with at most {MAX_ORDER:,} vertices; the best known "
                      "value is the largest of the wiki's, Comellas's Cayley graphs and the papers in literature.json"),
        "left_out": ", ".join(f"{v} {k}" for k, v in st.items()
                              if k not in ("entries", "kept", "raised by Comellas's pages", "raised by a paper")),
        "raised": {k: v for k, v in st.items() if k.startswith("raised")},
    }
    return defn, rows


if __name__ == "__main__":
    res = main()
    if isinstance(res, int):
        sys.exit(res)
    defn, rows = res
    write_family(defn, rows)
