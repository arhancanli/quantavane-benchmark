"""brouwer_codes_cells.py: A. E. Brouwer's tables of unrestricted codes as the benchmark family unrestricted-code,
checked by checkers/ucode_check.py.

  python3 -I brouwer_codes_cells.py PAGES_DIR READ REVISION

PAGES_DIR holds binary-1.html, ternary-1.html, quaternary-1.html and 5ary-1.html (A_q(n,d): the largest q-ary code of
length n and minimum distance d) and 23codes.html (N(m,n,d): the largest code with m binary and n ternary coordinates
and minimum distance d), saved from aeb.win.tue.nl/codes/. A cell is open when its lower bound is below its upper
bound. The mixed tables' row m = 0 and column n = 0 are ternary and binary codes, which the A_q tables already hold;
they are left out. Cells whose lower bound is 2^17 or more are left out (the check compares every pair of words)."""
import hashlib
import html
import json
import os
import re
import sys

LIMIT = 2 ** 17


def parse_aq(text):
    i = text.lower().find("<table")
    j = text.lower().find("</table>", i)
    rows = re.findall(r"<tr>(.*?)(?=<tr>|$)", text[i:j], re.S | re.I)
    grid = [[re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", "", c))).strip()
             for c in re.findall(r"<td>(.*?)(?=<td>|</tr>|$)", r, re.S | re.I)] for r in rows]
    hdr = [x.replace("d=", "").strip() for x in grid[0]]
    ds = {j: int(h) for j, h in enumerate(hdr) if h.isdigit()}
    ub, lb = {}, {}
    for r in grid[1:]:
        if not r or not r[0]:
            continue
        m = re.fullmatch(r"(\d+)\s*(ub|lb)?", r[0])
        if not m:
            continue
        n, kind = int(m.group(1)), m.group(2)
        for j, v in enumerate(r):
            if j not in ds or not v:
                continue
            v = v.replace(" ", "")
            mm = re.fullmatch(r"(\d+)-(\d+)", v)
            key = (n, ds[j])
            if kind is None:
                if mm:
                    lb[key], ub[key] = int(mm.group(1)), int(mm.group(2))
                elif v.isdigit():
                    lb[key] = ub[key] = int(v)
            elif kind == "ub" and v.isdigit():
                ub[key] = int(v)
            elif kind == "lb":
                if v == "=":
                    lb[key] = ub.get(key)
                elif v.isdigit():
                    lb[key] = int(v)
    return {k: (lb.get(k), ub.get(k)) for k in set(lb) | set(ub)}


def parse_mixed(text):
    cells, cur = {}, None
    for part in re.split(r"(<h\d[^>]*>.*?</h\d>)", text, flags=re.S | re.I):
        h = re.match(r"<h\d[^>]*>(.*?)</h\d>", part, re.S | re.I)
        if h:
            m = re.search(r"d\s*=\s*(\d+)", re.sub("<[^>]+>", "", h.group(1)))
            cur = int(m.group(1)) if m else cur
            continue
        for tab in re.findall(r"<table.*?</table>", part, re.S | re.I):
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", tab, re.S | re.I)
            hdr = [re.sub("<[^>]+>", "", x).strip() for x in re.findall(r"<th[^>]*>(.*?)</th>", rows[0], re.S | re.I)]
            ns = [int(x) for x in hdr[1:]]
            for r in rows[1:]:
                th = re.findall(r"<th[^>]*>(.*?)</th>", r, re.S | re.I)
                if not th:
                    continue
                mrow = int(re.sub("<[^>]+>", "", th[0]).strip())
                for j, td in enumerate(re.findall(r"<td[^>]*>(.*?)</td>", r, re.S | re.I)):
                    v = re.sub(r"\s+", "", html.unescape(re.sub("<[^>]+>", "", td)))
                    mm = re.fullmatch(r"(\d+)(?:-(\d+))?", v)
                    if mm and cur is not None:
                        cells[(cur, mrow, ns[j])] = (int(mm.group(1)), int(mm.group(2) or mm.group(1)))
    return cells


def main():
    pages, read, revision = sys.argv[1:4]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rows, shas, stats = [], {}, {}
    for q, fn in ((2, "binary-1.html"), (3, "ternary-1.html"), (4, "quaternary-1.html"), (5, "5ary-1.html")):
        raw = open(os.path.join(pages, fn), "rb").read()
        shas[fn] = hashlib.sha256(raw).hexdigest()
        cells = parse_aq(raw.decode("latin-1"))
        st = {"entries": len(cells), "solved": 0, "too large": 0, "kept": 0}
        for (n, d), (lo, hi) in sorted(cells.items()):
            assert lo is not None and hi is not None, (fn, n, d)
            if lo >= hi:
                st["solved"] += 1
                continue
            if lo >= LIMIT:
                st["too large"] += 1
                continue
            rows.append({"id": f"ucode-q{q}-n{n}-d{d}", "params": {"q": q, "n": n, "d": d, "alph": f"{q}^{n}"},
                         "variant": "aq", "best": str(lo), "bound": str(hi)})
            st["kept"] += 1
        stats[fn] = st
    raw = open(os.path.join(pages, "23codes.html"), "rb").read()
    shas["23codes.html"] = hashlib.sha256(raw).hexdigest()
    cells = parse_mixed(raw.decode("latin-1"))
    st = {"entries": len(cells), "m = 0 or n = 0 (in the A_q tables)": 0, "solved": 0, "too large": 0, "kept": 0}
    for (d, m, n), (lo, hi) in sorted(cells.items()):
        if m == 0 or n == 0:
            st["m = 0 or n = 0 (in the A_q tables)"] += 1
            continue
        if lo >= hi:
            st["solved"] += 1
            continue
        if lo >= LIMIT:
            st["too large"] += 1
            continue
        rows.append({"id": f"mixcode-m{m}-n{n}-d{d}", "params": {"m": m, "n": n, "d": d, "alph": f"2^{m}.3^{n}"},
                     "variant": "mixed", "best": str(lo), "bound": str(hi)})
        st["kept"] += 1
    stats["23codes.html"] = st
    for k, v in stats.items():
        print(k, v)
    fam = {
        "family": "unrestricted-code",
        "title": "Unrestricted codes (q-ary and mixed binary/ternary) with the most words",
        "added": "2.2", "objective": "maximize", "id_prefixes": ["ucode-", "mixcode-"],
        "keeper": "A. E. Brouwer, tables of bounds on codes (aeb.win.tue.nl/codes)",
        "page": "https://aeb.win.tue.nl/codes/",
        "read": read, "revision": revision,
        "template": {"title": "Code over an alphabet of {q} symbols, length {n}, minimum distance {d}",
                     "statement": "Find a code of length {n} over an alphabet of {q} symbols in which every two words differ in at least {d} coordinates, with as many words as possible (A_{q}({n},{d})).",
                     "submission": "Text file: one word per line, {n} symbols below {q} (separated by spaces or written as one string of digits); see checkers/ucode_check.py.",
                     "args": ["{alph}", "{d}"]},
        "variants": {"aq": {"title": "Code over an alphabet of {q} symbols, length {n}, minimum distance {d}"},
                     "mixed": {"title": "Mixed code with {m} binary and {n} ternary coordinates, minimum distance {d}",
                               "statement": "Find a code whose words have {m} binary coordinates followed by {n} ternary ones, in which every two words differ in at least {d} coordinates, with as many words as possible (N({m},{n},{d}) of Brouwer, Hamalainen, Ostergard and Sloane).",
                               "submission": "Text file: one word per line, {m} binary symbols then {n} ternary symbols (separated by spaces or written as one string of digits); see checkers/ucode_check.py."}},
        "checker": {"program": "ucode_check.py", "value": "result"},
        "score": "the number of words (larger is better)",
        "best_text": "The best known lower bound in Brouwer's table is {best}; a code with more words improves it.",
        "bound_kind": "upper bound", "bound_source": "the upper bound in the same table",
        "holder_unknown": "the tables give values; the references and notes on each page name the constructions",
        "holder_sources": "the notes and references on the page of the table",
        "open_rule": "every entry of the tables of A_2(n,d), A_3(n,d), A_4(n,d), A_5(n,d) and N(m,n,d) (m, n >= 1) whose lower bound is below its upper bound, with a lower bound below 2^17",
        "left_out": "; ".join(f"{k}: " + ", ".join(f"{v2} {k2}" for k2, v2 in v.items() if k2 not in ("entries", "kept")) for k, v in stats.items()),
        "page_sha256": shas, "cells": "cells.jsonl", "count": len(rows),
        "quantavane_records": 0, "single_problems_left_out": 0,
    }
    d = os.path.join(root, "families", "unrestricted-code")
    os.makedirs(d, exist_ok=True)
    json.dump(fam, open(os.path.join(d, "family.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(d, "cells.jsonl"), "w") as f:
        for c in rows:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print("family written:", len(rows))


if __name__ == "__main__":
    main()
