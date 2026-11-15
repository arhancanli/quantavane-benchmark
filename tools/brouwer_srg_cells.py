"""brouwer_srg_cells.py: A. E. Brouwer's table of strongly regular graphs (parameters of srg(v,k,lambda,mu) with v up to
1300) as the benchmark family strongly-regular-graph, checked by checkers/srg_check.py.

  python3 -I brouwer_srg_cells.py PAGES_DIR READ REVISION

PAGES_DIR holds the 26 pages srgtab1-50.html ... srgtab1251-1300.html saved from aeb.win.tue.nl/graphs/srg/. Each
feasible parameter set is a row, followed by the row of its complement (same v, left blank); the first column says
'!' (exists and is unique), '+' (exists), '-' (does not exist) or '?' (existence unknown), and the row colour agrees
(green, red, yellow). A cell is a '?' row: one open existence question, its complement counted with it (a graph
settles both). Each '?' row is checked: integer eigenvalue data agree with v, k, lambda, mu (k(k - lambda - 1) =
(v - k - 1) mu), and its complement row, when the page lists one, has the complementary parameters."""
import hashlib
import html
import json
import os
import re
import sys

PAGES = ["1-50"] + [f"{a}-{a + 49}" for a in range(51, 1300, 50)]
ROW = re.compile(r'<tr bgcolor="(#[0-9a-f]{6})">(.*?)</tr>', re.S | re.I)
COLOUR = {"!": "#b0ffb0", "+": "#b0ffb0", "-": "#ffb0b0", "?": "#ffffb0"}


def cells_of(text):
    """(status, v, k, l, m, comment) for every row; a blank v is the previous row's."""
    out, last_v = [], None
    for colour, body in ROW.findall(text):
        tds = [html.unescape(re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ").strip()
               for c in re.findall(r"<td[^>]*>(.*?)</td>", body, re.S | re.I)]
        assert len(tds) >= 5, body[:200]
        status, v, k, l, m = tds[:5]
        v = int(v) if v else last_v
        last_v = v
        mark = "!" if re.fullmatch(r"\d*!", status) else status      # '78!': exists, 78 graphs known
        assert mark in ("", "!", "+", "-", "?"), (status, v, k)
        if mark:
            assert COLOUR[mark] == colour.lower(), (status, colour, v, k)
        out.append((mark, colour.lower(), v, int(k), int(l), int(m), tds[7] if len(tds) > 7 else ""))
    return out


def complement(v, k, l, m):
    return v - k - 1, v - 2 - 2 * k + m, v - 2 * k + l


def main():
    pages, read, revision = sys.argv[1:4]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rows, shas = [], {}
    stats = {"rows": 0, "parameter sets": 0, "exist": 0, "do not exist": 0, "open": 0, "self-complementary open": 0}
    seen = set()
    for p in PAGES:
        fn = f"srgtab{p}.html"
        raw = open(os.path.join(pages, fn), "rb").read()
        shas[fn] = hashlib.sha256(raw).hexdigest()
        lo, hi = (int(x) for x in p.split("-"))
        cs = cells_of(raw.decode("utf-8"))
        stats["rows"] += len(cs)
        for i, (mark, colour, v, k, l, m, note) in enumerate(cs):
            assert lo <= v <= hi, (fn, v)
            assert k * (k - l - 1) == (v - k - 1) * m, (fn, v, k, l, m)
            if not mark:                     # the complement row of the row before it
                pv, pk, pl, pm = cs[i - 1][2:6]
                assert (v, k, l, m) == (pv,) + complement(pv, pk, pl, pm) and colour == cs[i - 1][1], (fn, v, k)
                continue
            stats["parameter sets"] += 1
            if mark in "!+":
                stats["exist"] += 1
                continue
            if mark == "-":
                stats["do not exist"] += 1
                continue
            key = (v, k, l, m)
            assert key not in seen and (v,) + complement(v, k, l, m) not in seen, key
            seen.add(key)
            kc, lc, mc = complement(v, k, l, m)
            listed = i + 1 < len(cs) and not cs[i + 1][0]
            if (kc, lc, mc) == (k, l, m):
                stats["self-complementary open"] += 1
                assert not listed, key
            else:
                assert listed, key
            stats["open"] += 1
            rows.append({"id": f"srg-{v}-{k}-{l}-{m}", "params": {"v": v, "k": k, "l": l, "m": m, "kc": kc, "lc": lc,
                                                                   "mc": mc}, "best": "0"})
    singles = {f[:-5] for f in os.listdir(os.path.join(root, "problems")) if f.endswith(".json")}
    kept = [c for c in rows if c["id"] not in singles]
    print(stats, "single problems left out:", len(rows) - len(kept))
    fam = {
        "family": "strongly-regular-graph",
        "title": "Strongly regular graphs whose existence is unknown",
        "added": "2.2", "objective": "maximize", "id_prefixes": ["srg-"],
        "keeper": "A. E. Brouwer, Parameters of strongly regular graphs (aeb.win.tue.nl/graphs/srg)",
        "page": "https://aeb.win.tue.nl/graphs/srg/srgtab.html",
        "cell_url": "https://aeb.win.tue.nl/graphs/srg/srgtab.html",
        "read": read, "revision": revision,
        "template": {
            "title": "Strongly regular graph srg({v}, {k}, {l}, {m})",
            "statement": "Find a graph on {v} vertices, {k}-regular, in which every two adjacent vertices have exactly "
                         "{l} common neighbours and every two non-adjacent vertices exactly {m}: a strongly regular "
                         "graph srg({v}, {k}, {l}, {m}). Its complement would be an srg({v}, {kc}, {lc}, {mc}), so "
                         "either graph settles the question; submit the one with the parameters above.",
            "submission": "Text file: the graph in graph6 or sparse6 (as on House of Graphs), as an edge list (one edge "
                          "\"u v\" per line, vertices numbered from 0) or as a 0/1 adjacency matrix.",
            "args": ["{v}", "{k}", "{l}", "{m}"]},
        "checker": {"program": "srg_check.py", "value": "result"},
        "score": "1 for a valid graph; none is known, so the best known value is 0",
        "best_text": "Brouwer's table marks these parameters '?': no graph is known and none has been ruled out, so "
                     "the best known value is {best}; a valid graph scores 1.",
        "holder_unknown": "none known (existence open)",
        "holder_sources": "the table's comments and references (srgtabrefs.html) give what is known about each case",
        "open_rule": "every parameter set the table marks '?' (existence unknown), counted once with its "
                     "complement",
        "left_out": f"{stats['exist']} parameter sets marked '!' or '+' (a graph exists) and {stats['do not exist']} "
                    "marked '-' (ruled out), each with its complement",
        "counts": stats,
        "page_sha256": shas, "cells": "cells.jsonl", "count": len(kept),
        "quantavane_records": 0, "single_problems_left_out": len(rows) - len(kept),
    }
    d = os.path.join(root, "families", "strongly-regular-graph")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "family.json"), "w") as f:
        f.write(json.dumps(fam, indent=1, ensure_ascii=False) + "\n")
    with open(os.path.join(d, "cells.jsonl"), "w") as f:
        for c in kept:
            f.write(json.dumps(c, ensure_ascii=False, separators=(", ", ": ")) + "\n")
    print("family written:", len(kept))


if __name__ == "__main__":
    main()
