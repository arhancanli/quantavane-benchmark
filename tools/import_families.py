#!/usr/bin/env python3
"""Build the problem families of the Open Problems Benchmark from the keepers' tables (standard library only).

A family is one statement and one exact checker with many cells: families/NAME/family.json (the statement as a
template, the checker, the keeper, the date the table was read, how open cells were chosen) and
families/NAME/cells.jsonl (one cell per line: its parameters, the best known value read from the keeper's table, the
bound on the other side when the table or a standard bound gives one, and who holds the value when the table names
them). Only values are stored, with the keeper credited; no keeper's file is copied. The inputs are files saved from
the keepers' pages; they are read here as text, never run.

  import_families.py covering-design EXPORT.csv LAJOLLA.json OURS.json READ REVISION DIFF.tsv...
  import_families.py spherical-code FRONT.html READ REVISION
  import_families.py covering-array CA_TABLE.csv READ REVISION
  import_families.py linear-code READ REVISION Q2.html Q3.html ...
  import_families.py constant-weight-code ANDW.html READ REVISION
  import_families.py project-scheduling READ REVISION DATASET.csv[:BKS.csv]...
  import_families.py index

A cell whose problem is already a single problem in problems/ (same id) is left out of the family, so every problem
is counted once."""
import csv
import hashlib
import html
import html.parser
import json
import math
import os
import re
import sys
from functools import lru_cache

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILIES = os.path.join(ROOT, "families")
OURS = "Quantavane (Arhan Canli)"


def single_ids():
    return {f[:-5] for f in os.listdir(os.path.join(ROOT, "problems")) if f.endswith(".json")}


def make_cell(cid, params, best, bound=None, holder=None, ours=False, variant=None):
    c = {"id": cid, "params": params}
    if variant:
        c["variant"] = variant
    c["best"] = str(best)
    if bound is not None:
        c["bound"] = str(bound)
    if holder:
        c["holder"] = holder
    if ours:
        c["quantavane_record"] = True
    return c


def write_family(defn, rows):
    singles = single_ids()
    kept = [c for c in rows if c["id"] not in singles]
    ids = [c["id"] for c in kept]
    assert len(ids) == len(set(ids)), "duplicate cell ids"
    d = os.path.join(FAMILIES, defn["family"])
    os.makedirs(d, exist_ok=True)
    defn = dict(defn)
    defn["cells"] = "cells.jsonl"
    defn["count"] = len(kept)
    defn["quantavane_records"] = sum(1 for c in kept if c.get("quantavane_record"))
    defn["single_problems_left_out"] = len(rows) - len(kept)
    with open(os.path.join(d, "cells.jsonl"), "w") as f:
        for c in kept:
            f.write(json.dumps(c, ensure_ascii=False, separators=(", ", ": ")) + "\n")
    with open(os.path.join(d, "family.json"), "w") as f:
        f.write(json.dumps(defn, indent=1, ensure_ascii=False) + "\n")
    print(f"{defn['family']}: {len(kept)} cells ({defn['quantavane_records']} held by Quantavane; "
          f"{len(rows) - len(kept)} already single problems)")


def plain(s):
    s = re.sub(r"<math>.*?</math>", " ", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", "; ", s)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip(" ;")


def short(s, n=160):
    s = s.strip()
    return s if len(s) <= n else s[:n - 3].rstrip() + "..."


# ------------------------------------------------------------------------------------------------ covering designs

@lru_cache(None)
def schoenheim(v, k, t):
    return 1 if t == 0 else -(-v * schoenheim(v - 1, k - 1, t - 1) // k)


def counting_bound(v, k, t, m):
    hit = sum(math.comb(k, i) * math.comb(v - k, m - i) for i in range(t, min(k, m) + 1))
    return -(-math.comb(v, m) // hit)


def turan_edges(v, r):
    """Edges of the Turan graph T(v, r): r parts as equal as possible."""
    q, s = divmod(v, r)
    return (v * v - s * (q + 1) ** 2 - (r - s) * q ** 2) // 2


def lotto_bound(v, k, t, m):
    """(bound, how) for C(v,k,t,m), m > t: the counting bound; for t = 2 also Turan's theorem (the pairs inside
    blocks form a graph with no independent m-set, so it has at least C(v,2) - t(v, m-1) edges, and each block holds
    C(k,2) of them; exact when k = 2)."""
    lb, how = counting_bound(v, k, t, m), "counting"
    if t == 2:
        tb = -(-(math.comb(v, 2) - turan_edges(v, m - 1)) // math.comb(k, 2))
        if tb > lb:
            lb, how = tb, "Turán"
    return lb, how


def covering_design(export, lajolla, ours_path, read, revision, diffs):
    lj = json.load(open(lajolla))
    ours = {}
    for r in json.load(open(ours_path)):
        ours[(r["v"], r["k"], r["t"], r.get("m", r["t"]))] = r["blocks"]
    changed = {}                         # (v,k,t,m) -> (new value, author, date) from the site's recent-uploads list
    for path in diffs:
        for row in csv.DictReader(open(path, newline=""), delimiter="\t"):
            if row.get("change") in ("improved", "new"):
                key = tuple(int(row[x]) for x in "vktm")
                changed[key] = (int(row["new_b"]), (row.get("author") or "").strip(), row.get("date", ""))
    rows, n_plain, n_lotto, closed, heavy, tiny = [], 0, 0, 0, 0, 0
    for r in csv.DictReader(open(export, newline="", encoding="utf-8-sig")):
        v, k, t, m, b = (int(r[x]) for x in "vktmb")
        if m == t:
            lb, how = schoenheim(v, k, t), "Schönheim"
            e = lj.get(f"C({v},{k},{t})")
            if e and e.get("low_bd") and int(e["low_bd"]) > lb:
                lb, how = int(e["low_bd"]), "La Jolla"
        else:
            lb, how = lotto_bound(v, k, t, m)
        if b <= lb:
            closed += 1
            continue
        if m > t and b <= 3:
            tiny += 1
            continue
        if m == t and b * math.comb(k, t) > 10 ** 8:
            heavy += 1
            continue
        if m > t and b > 1000:
            heavy += 1
            continue
        holder, mine = None, False
        if ours.get((v, k, t, m)) == b:
            holder, mine = OURS, True
        elif (v, k, t, m) in changed and changed[(v, k, t, m)][0] == b:
            _, author, date = changed[(v, k, t, m)]
            if author.startswith("Known design"):
                holder = f"derived on the site from a known design ({date})"
            elif "Canli" in author:
                holder, mine = OURS, True
            elif author:
                holder = f"{author} ({date})"
        elif m == t:
            e = lj.get(f"C({v},{k},{t})")
            if e and e.get("imps") and int(e["imps"][0][0]) == b:
                size, method, credit, date = e["imps"][0][:4]
                credit = credit.strip()
                if credit == "LJCR":
                    credit = "La Jolla Covering Repository"
                elif credit == "JCD article":
                    credit = "Gordon, Kuperberg and Patashnik, J. Combin. Des. 3 (1995)"
                holder = f"{credit}, {date[:4]}" + (f" ({method.strip()})" if method.strip() else "")
        variant = None if m == t else "lotto"
        cid = f"covering-{v}-{k}-{t}" if m == t else f"covering-{v}-{k}-{t}-{m}"
        rows.append(make_cell(cid, {"v": v, "k": k, "t": t, "m": m}, b, f"{lb} ({how})", holder, mine, variant))
        n_plain += m == t
        n_lotto += m > t
    defn = {
        "family": "covering-design",
        "title": "Covering designs C(v,k,t) and C(v,k,t,m)",
        "added": "2.0",
        "objective": "minimize",
        "id_prefixes": ["covering-"],
        "keeper": "Covering Repository (coveringrepository.com), successor of D. Gordon's La Jolla Covering Repository",
        "page": "https://www.coveringrepository.com/",
        "read": read,
        "revision": revision,
        "template": {
            "title": "Covering design C({v},{k},{t})",
            "statement": "Find {k}-subsets (blocks) of {{1, ..., {v}}} such that every {t}-subset lies in some block, "
                         "with as few blocks as possible.",
            "submission": "Text file: one block per line, {k} distinct points from 1..{v} separated by spaces.",
            "args": ["{v}", "{k}", "{t}", "{m}"],
        },
        "variants": {"lotto": {
            "title": "Covering design C({v},{k},{t},{m})",
            "statement": "Find {k}-subsets (blocks) of {{1, ..., {v}}} such that every {m}-subset meets some block in "
                         "at least {t} points, with as few blocks as possible.",
        }},
        "checker": {"program": "covering_check.py", "value": "blocks"},
        "score": "the number of blocks (smaller is better)",
        "best_text": "The best known size in the Covering Repository is {best} blocks ({holder}); a design with fewer "
                     "blocks improves it.",
        "bound_kind": "lower bound",
        "bound_source": "the larger of Schönheim's bound and the La Jolla Covering Repository's listed lower bound "
                        "(m = t); for m > t the counting bound C(v,m) / (the m-subsets one block meets in at least t "
                        "points) and, for t = 2, Turán's theorem (the pairs inside blocks form a graph with no "
                        "independent m-set: at least C(v,2) - t(v,m-1) edges, C(k,2) per block); the method is named "
                        "after the value",
        "holder_unknown": "not named in the site's export; see the entry on coveringrepository.com",
        "holder_sources": "our own records (quantavane-covering-records); the site's list of recent uploads and "
                          "derived coverings, read with each daily export since 1 Nov 2026; for entries unchanged since "
                          "then, the credit in the La Jolla Covering Repository's final data (frozen 1 March 2026)",
        "open_rule": "every entry whose best known size is above the lower bound named in the cell; entries that "
                     "equal it are solved and left out. A cell may still be optimal by a sharper bound than these.",
        "left_out": f"{closed} entries equal to their lower bound (solved); {tiny} entries with m > t and at most 3 "
                    f"blocks (a short case analysis settles them); {heavy} entries whose check would be very long: "
                    "t = m with more than 10^8 t-subsets to mark (blocks x C(k,t)), or m > t with more than 1,000 "
                    "blocks",
        "counts": {"t = m": n_plain, "m > t": n_lotto},
    }
    write_family(defn, rows)


# ------------------------------------------------------------------------------------------------ spherical codes

SPH_ROW = re.compile(r"<tr>\s*<td>(\d+)</td>\s*<td><a href=\"(/data/\d+/\d+)\">(\d+)</a>(&ast;)?</td>\s*"
                     r"<td>([^<]*)</td>\s*<td>(.*?)</td>\s*</tr>", re.S)


def spherical_code(front, read, revision):
    t = open(front, encoding="utf-8").read()
    body = t[t.find("<tbody>"):t.find("</tbody>")]
    found = SPH_ROW.findall(body)
    assert len(found) == body.count("<tr>"), "unparsed rows"
    rows, optimal = [], 0
    for d, link, n, star, cos, notes in found:
        d, n = int(d), int(n)
        if star:
            optimal += 1
            continue
        cos = cos.strip()
        assert re.fullmatch(r"-?\d+(\.\d{1,12})?", cos), cos
        whole, _, frac = cos.partition(".")
        best = f"{whole}.{frac.ljust(12, '0')}"      # printed rounded up to 12 decimals; trailing zeros dropped
        note = plain(notes)
        holder = short(note.split("; ")[0])
        mine = note.startswith("Arhan Canli")
        rows.append(make_cell(f"sphere-d{d}-n{n}", {"d": d, "n": n}, best, None, holder, mine))
    defn = {
        "family": "spherical-code",
        "title": "Spherical codes: N points on the sphere in R^d with the smallest largest cosine",
        "added": "2.0",
        "objective": "minimize",
        "id_prefixes": ["sphere-"],
        "keeper": "H. Cohn, table of spherical codes (spherical-codes.org)",
        "page": "https://spherical-codes.org/",
        "cell_url": "https://spherical-codes.org/data/{d}/{n}",
        "read": read,
        "revision": revision,
        "exact_values": False,
        "template": {
            "title": "Spherical code: {n} points on the sphere in R^{d}",
            "statement": "Place {n} points on the unit sphere in R^{d} so that the largest cosine between two distinct "
                         "points is as small as possible.",
            "submission": "Text file: {n} lines, each one point given by its {d} coordinates separated by commas (any "
                          "length: the checker normalises every point in 50-digit decimal arithmetic); other lines "
                          "are ignored, as on spherical-codes.org.",
            "args": ["{d}", "{n}"],
        },
        "checker": {"program": "sph_check.py", "value": "spherical"},
        "score": "the largest cosine between two of the points (smaller is better)",
        "best_text": "The best known value in Henry Cohn's table is {best} ({holder}), rounded up to 12 decimals; a "
                     "code improves it when its largest cosine is smaller by at least one unit in the 12th decimal.",
        "holder_unknown": "not named in the table",
        "holder_sources": "the first reference or credit in the entry's notes on the table's front page",
        "open_rule": "every entry not marked optimal (*) in the table",
        "left_out": f"{optimal} entries marked optimal",
    }
    write_family(defn, rows)


# ------------------------------------------------------------------------------------------------ covering arrays

def covering_array(table, read, revision):
    rows_in = list(csv.DictReader(open(table, newline="")))
    by_cell, by_tv = {}, {}
    for r in rows_in:
        if r["tier"] not in ("CITED", "VERIFIED"):
            continue
        t, v, k, n = int(r["t"]), int(r["v"]), int(r["k"]), int(r["N"])
        by_cell.setdefault((t, v, k), []).append((n, r))
        by_tv.setdefault((t, v), []).append((k, n, r))
    rows, dominated, solved, heavy = [], 0, 0, 0
    for (t, v, k) in sorted(by_cell):
        best_n, best_row = min(((n, r) for kk, n, r in by_tv[(t, v)] if kk >= k), key=lambda x: (x[0], -int(x[1]["k"])))
        own_n = min(n for n, _ in by_cell[(t, v, k)])
        if own_n > best_n:
            dominated += 1          # an array with more columns and no more rows exists: not a step of the table
            continue
        if best_n <= v ** t or (t == 2 and v == 2):
            solved += 1
            continue
        if math.comb(k, t) * v ** t > 2 * 10 ** 8:
            heavy += 1
            continue
        src = best_row["source_detail"].strip()
        mine = src.startswith("Canli 2026")
        holder = short(src + (" (verified by the table)" if best_row["tier"] == "VERIFIED" else ""))
        rows.append(make_cell(f"ca-{t}-{k}-{v}", {"t": t, "k": k, "v": v}, best_n, f"{v ** t} (v^t)",
                              OURS + ", " + holder if mine else holder, mine))
    defn = {
        "family": "covering-array",
        "title": "Covering arrays CAN(t,k,v)",
        "added": "2.0",
        "objective": "minimize",
        "id_prefixes": ["ca-"],
        "keeper": "C. Smolen's ca-tools table (github.com/chrispbsmolen/ca-tools), the live successor of C. J. "
                  "Colbourn's covering array tables",
        "page": "https://github.com/chrispbsmolen/ca-tools",
        "read": read,
        "revision": revision,
        "template": {
            "title": "Covering array CAN({t},{k},{v})",
            "statement": "Find an array with {k} columns over {v} symbols (the integers below {v}) in which every {t} "
                         "columns show all {v}^{t} tuples of symbols in some row (a covering array of strength {t}), "
                         "with as few rows as possible.",
            "submission": "Text file: one row per line, {k} symbols (integers below {v}) separated by spaces.",
            "args": ["{t}", "{k}", "{v}"],
        },
        "checker": {"program": "ca_check.py", "value": "result"},
        "score": "the number of rows (smaller is better)",
        "best_text": "The best known size in the ca-tools table is {best} rows ({holder}); an array with fewer rows "
                     "improves it.",
        "bound_kind": "lower bound",
        "bound_source": "v^t, the number of tuples every t columns must show",
        "holder_unknown": "not named in the table",
        "holder_sources": "the table's source of the row that gives the best value (by its own rule: the fewest rows "
                          "among CITED and VERIFIED rows with at least k columns)",
        "open_rule": "every row of the table (CITED or VERIFIED) that is a step of its staircase (no row with more "
                     "columns has as few rows), above v^t, leaving out strength 2 over 2 symbols (solved exactly by "
                     "Kleitman and Spencer and by Katona)",
        "left_out": f"{dominated} rows beaten by a row with more columns; {solved} cells solved (v^t rows, or t = v = "
                    f"2); {heavy} cells whose check would take more than 2 x 10^8 set intersections (C(k,t) v^t)",
    }
    write_family(defn, rows)


# ------------------------------------------------------------------------------------------------ linear codes

CODE_CELL = re.compile(r'<TD([^>]*)><A[^>]*title="n=(\d+), k=(\d+)"[^>]*>([^<]*)</A></TD>')


def linear_code(read, revision, pages):
    rows, solved, heavy = [], 0, 0
    for page in pages:
        t = open(page, encoding="latin-1").read()
        q = int(re.search(r"<TITLE>Bounds on the minimum distance of linear codes over GF\((\d+)\)</TITLE>", t).group(1))
        n_cells = 0
        for attrs, n, k, txt in CODE_CELL.findall(t):
            n, k = int(n), int(k)
            m = re.fullmatch(r"(\d+)(?:-(\d+))?", txt.strip())
            lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
            n_cells += 1
            if lo >= hi:
                solved += 1
                continue
            r = min(k, n - k)
            if (q ** r - 1) // (q - 1) > 2 ** 25:
                heavy += 1
                continue
            rows.append(make_cell(f"code-q{q}-n{n}-k{k}", {"q": q, "n": n, "k": k}, lo, hi, None, False))
        assert n_cells > 1000, page
    defn = {
        "family": "linear-code",
        "title": "Linear codes [n,k] over GF(q) with the largest minimum distance",
        "added": "2.0",
        "objective": "maximize",
        "id_prefixes": ["code-"],
        "keeper": "M. Grassl, bounds on the minimum distance of linear codes (codetables.de)",
        "page": "https://www.codetables.de/",
        "cell_url": "https://www.codetables.de/BKLC/BKLC.php?q={q}&n={n}&k={k}",
        "read": read,
        "revision": revision,
        "template": {
            "title": "Linear code [{n},{k}] over GF({q})",
            "statement": "Find a linear code of length {n} and dimension {k} over GF({q}) whose minimum distance is as "
                         "large as possible.",
            "submission": "Text file: a generator matrix, {k} rows of {n} elements of GF({q}) written as integers "
                          "below {q} (for q = 4, 8, 9 the base-p digits of the integer are the coefficients of a "
                          "polynomial in x modulo the Conway polynomial; see checkers/lincode_check.py).",
            "args": ["{q}", "{n}", "{k}"],
        },
        "checker": {"program": "lincode_check.py", "value": "result"},
        "score": "the minimum distance (larger is better)",
        "best_text": "The best known lower bound in Markus Grassl's tables is {best}; a code with a larger minimum "
                     "distance improves it.",
        "bound_kind": "upper bound",
        "bound_source": "the upper bound in the same table",
        "holder_unknown": "the construction and its source are on the entry's page at codetables.de",
        "holder_sources": "the bounds tables list values only; each entry's page names its construction",
        "open_rule": "every entry whose lower bound is below its upper bound",
        "left_out": f"{solved} entries with equal bounds (solved); {heavy} entries whose check would list more than "
                    "2^25 codewords (the work grows as q^min(k, n-k))",
    }
    write_family(defn, rows)


# ------------------------------------------------------------------------------------------------ constant weight codes

class Cells(html.parser.HTMLParser):
    """Tables of a page as rows of cells (tag, text, sup, href, class), with the heading before each table."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables, self.heading, self.in_h, self.hbuf = [], "", False, []
        self.table = self.row = self.cell = None
        self.in_sup = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h1", "h2", "h3"):
            self.in_h, self.hbuf = True, []
        elif tag == "table":
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = {"tag": tag, "text": [], "sup": [], "href": None, "cls": a.get("class")}
        elif tag == "sup" and self.cell is not None:
            self.in_sup = True
        elif tag == "a" and self.cell is not None and a.get("href"):
            self.cell["href"] = a.get("href")

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3") and self.in_h:
            self.in_h = False
            self.heading = " ".join("".join(self.hbuf).split())
        elif tag == "table" and self.table is not None:
            self.tables.append((self.heading, self.table))
            self.table = None
        elif tag == "tr" and self.row is not None:
            if self.table is not None:
                self.table.append(self.row)
            self.row = None
        elif tag in ("td", "th") and self.cell is not None:
            c = self.cell
            c["text"], c["sup"] = "".join(c["text"]).strip(), "".join(c["sup"]).strip()
            self.row.append(c)
            self.cell = None
        elif tag == "sup":
            self.in_sup = False

    def handle_data(self, data):
        if self.in_h:
            self.hbuf.append(data)
        if self.cell is not None:
            (self.cell["sup"] if self.in_sup else self.cell["text"]).append(data)


def cw_value(c):
    """'1920', '7084.' (optimal), '315-364' -> (lower, optimal, upper)."""
    t = c["text"].replace("–", "-").replace(" ", "")
    if t == "" or re.fullmatch(r"-\d+", t):
        return None
    m = re.fullmatch(r"(\d+)(\.)?(?:-(\d+|\.\.\.))?", t)
    if not m:
        raise ValueError(f"cell {c!r}")
    lb, opt = int(m.group(1)), bool(m.group(2))
    ub = int(m.group(3)) if m.group(3) and m.group(3).isdigit() else (lb if opt else None)
    return lb, opt, ub


def cw_cells(text):
    p = Cells()
    p.feed(text)
    out = []
    for heading, rows in p.tables:
        m = re.match(r"Bounds on A\(n,(\d+),w\)$", heading)
        if m and rows and rows[0] and rows[0][0]["text"] == "n\\w":
            d = int(m.group(1))
            ws = [int(c["text"]) for c in rows[0][1:]]
            for r in rows[1:]:
                if not r or r[0]["tag"] != "th" or not r[0]["text"].isdigit():
                    continue
                n = int(r[0]["text"])
                for c, w in zip(r[1:], ws):
                    v = cw_value(c)
                    if v:
                        out.append((n, d, w, v, c["sup"]))
            continue
        m = re.match(r"(?:Values of|Bounds on|Lower bounds for) A\(n,(\d+),(\d+)\)", heading)
        if m:
            d, w = int(m.group(1)), int(m.group(2))
            i = 0
            while i < len(rows):
                r = rows[i]
                if r and all(c["text"].isdigit() for c in r) and i + 1 < len(rows) and len(rows[i + 1]) == len(r):
                    for n, c in zip([int(c["text"]) for c in r], rows[i + 1]):
                        v = cw_value(c)
                        if v:
                            out.append((n, d, w, v, c["sup"]))
                    i += 2
                    continue
                i += 1
    return out


def cw_legend(text):
    """Label -> who or what it stands for, from the sections 'Constructions' and 'References for labels'."""
    out = {}
    i, j = text.find("<h3>Constructions</h3>"), text.find("<h3>Upper bounds</h3>")
    for key, body in re.findall(r"\n([a-zA-Z]{1,3}): (.*?)(?=\n\n|\n[a-zA-Z]{1,3}: )", plain_keep_lines(text[i:j])):
        out[key] = "construction: " + short(body.strip().rstrip("."), 80)
    i = text.find("<h3>References for labels</h3>")
    j = text.find("<h3>", i + 10)
    for key, body in re.findall(r"<p>\s*([^\s:<>]{1,8}):\s*(.*?)(?=<p>|$)", text[i:j], flags=re.S):
        who = plain(body.split("<i>")[0]).rstrip(" ,.")
        out[key] = short(who, 120)
    return out


def plain_keep_lines(s):
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def cw_holder(label, legend):
    if not label:
        return None
    parts, rest = [], label
    while rest:
        key = next((rest[:n] for n in range(min(8, len(rest)), 0, -1) if rest[:n] in legend), None)
        if key is None:
            return f"label {label} in the table"
        parts.append(legend[key])
        rest = rest[len(key):]
    return "; ".join(parts)


def constant_weight_code(andw, read, revision):
    text = open(andw, encoding="utf-8").read()
    legend = cw_legend(text)
    best = {}
    for n, d, w, (lb, opt, ub), label in cw_cells(text):
        key = (n, d, w)
        old = best.get(key)
        if old is None:
            best[key] = [lb, opt, ub, label]
        else:   # an entry shown in two tables: keep the stronger bounds
            if lb > old[0]:
                old[0], old[3] = lb, label
            old[1] = old[1] or opt
            if ub is not None and (old[2] is None or ub < old[2]):
                old[2] = ub
    rows, solved = [], 0
    for (n, d, w), (lb, opt, ub, label) in sorted(best.items()):
        if opt or (ub is not None and lb >= ub):
            solved += 1
            continue
        holder = cw_holder(label, legend)
        mine = bool(label) and "Can" in re.findall(r"[A-Z][a-z]*", label)
        rows.append(make_cell(f"cw-{n}-{d}-{w}", {"n": n, "d": d, "w": w}, lb, ub, holder, mine))
    defn = {
        "family": "constant-weight-code",
        "title": "Binary constant weight codes A(n,d,w)",
        "added": "2.0",
        "objective": "maximize",
        "id_prefixes": ["cw-"],
        "keeper": "A. E. Brouwer, bounds for binary constant weight codes (aeb.win.tue.nl/codes/Andw.html)",
        "page": "https://aeb.win.tue.nl/codes/Andw.html",
        "read": read,
        "revision": revision,
        "template": {
            "title": "Constant weight code A({n},{d},{w})",
            "statement": "Find binary words of length {n}, each with exactly {w} ones and any two differing in at "
                         "least {d} positions, as many as possible: a lower bound on A({n},{d},{w}).",
            "submission": "Text file: one word per line, the {w} positions of its ones, distinct integers from 1..{n} "
                          "separated by spaces.",
            "args": ["{n}", "{d}", "{w}"],
        },
        "checker": {"program": "cw_check.py", "value": "words"},
        "score": "the number of code words (more is better)",
        "best_text": "The best known lower bound in Andries Brouwer's table is {best} ({holder}); a code with more "
                     "words improves it.",
        "bound_kind": "upper bound",
        "bound_source": "the upper bound in the same table, when it gives one",
        "holder_unknown": "the table gives no label for this entry",
        "holder_sources": "the entry's label, read with the table's own key (sections Constructions and References "
                          "for labels)",
        "open_rule": "every entry not marked optimal whose lower bound is below its upper bound (or has none)",
        "left_out": f"{solved} entries marked optimal or with equal bounds",
    }
    write_family(defn, rows)


# ------------------------------------------------------------------------------------------------ project scheduling

def ghent_rows(path):
    """(format, rows of the instance table, {reference id: authors}) of a Solutions Update dataset file."""
    lines = open(path, encoding="latin-1").read().splitlines()
    fmt, header, rows, refs, cur = None, None, [], {}, None
    for line in lines:
        p = [x.strip() for x in line.split(";")]
        if p[0] == "Format":
            fmt = p[1]
        elif p[0] == "ID" and len(p) > 10 and header is None:
            header = p
        elif header and p[0].isdigit() and len(p) >= 11 and cur is None:
            rows.append(dict(zip(header, p)))
        elif p[0] == "ID" and len(p) >= 2 and p[1].isdigit():
            cur = int(p[1])
        elif cur is not None and p[0] == "# Author(s)":
            refs[cur] = p[1] if len(p) > 1 else ""
    return fmt, rows, refs


def ghent_bks(path):
    out = {}
    if path:
        for line in open(path, encoding="latin-1"):
            p = line.strip().split(";")
            if p and p[0].isdigit() and len(p) >= 3 and p[2].strip().isdigit():
                i, kind, val = int(p[0]), p[1].strip().lower(), int(p[2])
                if i not in out or val < out[i][1] or (val == out[i][1] and kind == "optimal"):
                    out[i] = (kind, val)
    return out


def project_scheduling(read, revision, files):
    rows, closed, total, per_set = [], 0, 0, {}
    digests = {}
    for spec in files:
        bks_path = spec.partition(":")[2]
        if bks_path:
            digests.setdefault(hashlib.sha256(open(bks_path, "rb").read()).hexdigest(), []).append(spec)
    twins = {x for group in digests.values() if len(group) > 1 for x in group}
    left_sets = sorted(os.path.basename(x.partition(":")[0])[:-4] for x in twins)
    for spec in files:
        if spec in twins:
            continue
        ds_path, _, bks_path = spec.partition(":")
        name = os.path.basename(ds_path)[:-4]
        fmt, table, refs = ghent_rows(ds_path)
        bks = ghent_bks(bks_path)
        n_open = 0
        for r in table:
            total += 1
            try:
                lb, ub = int(r["LB value"]), int(r["UB value"])
            except (KeyError, ValueError):
                continue
            i = int(r["ID"])
            best, holder = ub, None
            ref = r.get("UB ref", "")
            if ref.isdigit() and int(ref) in refs:
                holder = refs[int(ref)]
            if i in bks and bks[i][1] < best:
                best, holder = bks[i][1], "the site's best known solutions file (no author given there)"
            if (i in bks and bks[i][0] == "optimal" and bks[i][1] == best) or best <= lb:
                closed += 1
                continue
            params = {"set": name, "id": i, "file": r["Ref1"].replace("\\", "/")}
            if fmt == "rcp+res":
                assert params["file"].count("/") == 1, params["file"]
                params.update(resources=r["Ref2"], profile=int(r["Ref3"]))
                variant = "netres"
            elif fmt == "sm":
                variant = "sm"
            else:
                variant = None
            mine = bool(holder) and ("Quantavane" in holder or "Canli" in holder)
            rows.append(make_cell(f"rcpsp-{name.lower()}-{i}", params, best, lb, holder, mine, variant))
            n_open += 1
        per_set[name] = n_open
    defn = {
        "family": "project-scheduling",
        "title": "Resource-constrained project scheduling (RCPSP), shortest makespan",
        "added": "2.0",
        "objective": "minimize",
        "id_prefixes": ["rcpsp-"],
        "keeper": "Solutions Update (solutionsupdate.ugent.be), M. Vanhoucke and J. Coelho, OR&S group, Ghent "
                  "University",
        "page": "http://solutionsupdate.ugent.be/index.php/rcpsp",
        "cell_url": "http://solutionsupdate.ugent.be/",
        "read": read,
        "revision": revision,
        "template": {
            "title": "RCPSP instance {file} ({set})",
            "statement": "Schedule the activities of instance {file} of the {set} set so that every activity starts "
                         "after its predecessors finish and no renewable resource is used beyond its capacity, "
                         "finishing as early as possible (the instance file is on the set's page of the Solutions "
                         "Update site).",
            "submission": "Text file: the start time of every activity of the instance, in its order (the dummy first "
                          "and last activities included), integers separated by spaces, commas or semicolons.",
            "args": ["rcp", "instances/rcpsp/{set}/{file}"],
        },
        "variants": {
            "sm": {"args": ["sm", "instances/rcpsp/{set}/{file}"]},
            "netres": {
                "title": "RCPSP instance {id} of {set} (NetRes network {file}, resource profile {profile} of "
                         "{resources})",
                "statement": "Schedule the activities of instance {id} of the NetRes set {set} (network {file} of "
                             "NetRes.zip, with resource profile {profile} of {resources}) so that every activity "
                             "starts after its predecessors finish and no renewable resource is used beyond its "
                             "capacity, finishing as early as possible.",
                "args": ["rcp+res", "instances/rcpsp/NetRes/MT30/{file}", "instances/rcpsp/NetRes/ResSet/{resources}",
                         "{profile}"]},
        },
        "checker": {"program": "rcpsp_check.py", "value": "result"},
        "score": "the makespan (smaller is better)",
        "best_text": "The best known makespan on the Solutions Update site is {best} ({holder}); a feasible schedule "
                     "that finishes earlier improves it.",
        "bound_kind": "lower bound",
        "bound_source": "the lower bound in the set's dataset file",
        "holder_unknown": "not named in the dataset file",
        "holder_sources": "the reference of the upper bound in the set's dataset file (its list of references); when "
                          "the set's best known solutions file holds a smaller makespan, that value, with no author",
        "open_rule": "every instance whose best known makespan is above its lower bound and which neither file marks "
                     "optimal",
        "left_out": f"{closed} closed instances of {total} in the sets read"
                    + (f"; the sets {', '.join(left_sets)}, whose best known solutions files are byte-identical, so "
                       "that which set a file's values belong to is unclear" if left_sets else ""),
        "sets_not_read": "the highRD, lowRU and 1k variants of the sets (Vanhoucke and Coelho, 2021): their dataset "
                         "files date from April 2021, many of their upper bounds are the trivial sum of all durations, "
                         "and some pairs of their best known solutions files are byte-identical; the 1k subsets of "
                         "NetRes and the sets J30, DC1, Patterson, sD and VNR, which have no open instance",
        "instances": "Instance files are not copied here. Download a set's archive from its page on the Solutions "
                     "Update site and unpack it under instances/rcpsp/SET/ (the NetRes sets: NetRes.zip under "
                     "instances/rcpsp/NetRes/, so that MT30/<folder>/<file> and ResSet/<file> exist, with each folder's own zip "
                     "unpacked in MT30).",
        "open_by_set": per_set,
    }
    write_family(defn, rows)


# ------------------------------------------------------------------------------------------------ index

def index():
    version = open(os.path.join(ROOT, "VERSION")).read().strip()
    shards, by_family = [], {}
    singles = sorted(single_ids())
    for pid in singles:
        fam = json.load(open(os.path.join(ROOT, "problems", pid + ".json")))["family"]
        by_family[fam] = by_family.get(fam, 0) + 1
    shards.append({"kind": "problems", "path": "problems", "count": len(singles),
                   "about": "single problems, one JSON file each"})
    total = len(singles)
    for name in sorted(os.listdir(FAMILIES)):
        dpath = os.path.join(FAMILIES, name, "family.json")
        if not os.path.exists(dpath):
            continue
        fam = json.load(open(dpath))
        cpath = os.path.join(FAMILIES, name, fam["cells"])
        n = sum(1 for line in open(cpath) if line.strip())
        assert n == fam["count"], name
        h = hashlib.sha256(open(cpath, "rb").read()).hexdigest()
        shards.append({"kind": "family", "family": name, "path": f"families/{name}/{fam['cells']}",
                       "definition": f"families/{name}/family.json", "count": n, "sha256": h,
                       "keeper": fam["keeper"], "read": fam["read"], "checker": fam["checker"]["program"]})
        by_family[name] = by_family.get(name, 0) + n
        total += n
    out = {"benchmark_version": version, "problems": total, "by_family": dict(sorted(by_family.items())),
           "shards": shards}
    with open(os.path.join(ROOT, "index.json"), "w") as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"index.json: {total} problems ({len(singles)} single problems and {total - len(singles)} family cells)")


def main():
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    if cmd == "covering-design" and len(args) >= 5:
        covering_design(args[0], args[1], args[2], args[3], args[4], args[5:])
    elif cmd == "spherical-code" and len(args) == 3:
        spherical_code(*args)
    elif cmd == "covering-array" and len(args) == 3:
        covering_array(*args)
    elif cmd == "linear-code" and len(args) >= 3:
        linear_code(args[0], args[1], args[2:])
    elif cmd == "constant-weight-code" and len(args) == 3:
        constant_weight_code(*args)
    elif cmd == "project-scheduling" and len(args) >= 3:
        project_scheduling(args[0], args[1], args[2:])
    elif cmd == "index":
        index()
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
