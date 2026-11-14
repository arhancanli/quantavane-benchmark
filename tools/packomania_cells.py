"""packomania_cells.py: the Packomania sections whose geometry is rational, as two benchmark families.

  python3 -I packomania_cells.py PAGES_DIR READ REVISION       (writes families/circle-packing and
                                                                 families/growing-circle-packing)

PAGES_DIR holds the section pages as saved by fetch (file names SECTION_SECTION.html, e.g. csq_csq.html; coc.html,
ccq.html, crt.html for the three read on 14 Nov before the others). A cell is one N of one section whose packing is
not marked proven optimal (Packomania: "Proven optimal packings are indicated by a radius in bold face type").
Sections that mark nothing as proven leave out their small N, where optimality is known or trivial (see SMALL)."""
import hashlib, html, json, os, re, sys

EQUAL = {"csq": ("circles", "the unit square [0,1]^2", 2), "cci": ("circles", "a circle of radius 1", 2),
         "csc": ("circles", "a half disc of radius 1", 2), "ccq": ("circles", "a quarter disc of radius 1", 2),
         "crt": ("circles", "an isosceles right triangle with legs of length 1", 2),
         "scu": ("balls", "the unit cube [0,1]^3", 3), "ssp": ("balls", "a ball of radius 1 in R^3", 3),
         "hsp4": ("balls", "a ball of radius 1 in R^4", 4), "hsp5": ("balls", "a ball of radius 1 in R^5", 5),
         "hsp6": ("balls", "a ball of radius 1 in R^6", 6)}
GROWING = {"ccin": "a circle centred at 0", "csqn": "a square [0,V]^2"}
# Sections without bold entries: N at or below this are left out (known or trivial optimal packings).
SMALL = {"scu": 10, "ssp": 12, "hsp4": 5, "hsp5": 6, "hsp6": 7, "ccin": 3, "csqn": 3, "csc": 3, "ccq": 2, "crt": 3}
FILES = {"csq": "csq_csq.html", "cci": "cci_cci.html", "csc": "csc_csc.html", "ccq": "ccq.html", "crt": "crt.html",
         "scu": "scu_scu.html", "ssp": "ssp_ssp.html", "hsp4": "hsp4_hsp4.html", "hsp5": "hsp5_hsp5.html",
         "hsp6": "hsp6_hsp6.html", "ccin": "ccin_ccin.html", "csqn": "csqn_csqn.html"}
NUM = r'\s*(<strong>)?\s*([0-9]+\.[0-9]+)\s*(</strong>)?\s*'
ROW_LINK = r'<a href="{p}(\d+)\.html"\s+name="[^"]*">\s*(?:<strong>)?\s*(\d+)\s*(?:</strong>)?\s*</a>\s*</td>\s*<td[^>]*>' + NUM + r'</td>\s*<td[^>]*>' + NUM + r'</td>(.*?)</tr>'
ROW_PLAIN = r'<tr><td[^>]*>\s*(\d+)\s*</td>\s*<td[^>]*>' + NUM + r'</td>\s*<td[^>]*>\s*(?:<strong>)?\s*([0-9.]*)\s*(?:</strong>)?\s*</td>(.*?)</tr>'
REF = re.compile(r'<tr><td align="right" valign="top">\[(\d+)\]<td valign="top">(.*?)(?=<tr><td align="right"|</table>)', re.S)


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def parse(sec, text):
    refs = {int(n): clean(t)[:240] for n, t in REF.findall(text)}
    rows = []
    for m in re.finditer(ROW_LINK.format(p=sec), text, re.S | re.I):
        n = int(m.group(2))
        v1, b1, v2, b2 = m.group(4), bool(m.group(3)), m.group(7), bool(m.group(6))
        rest = m.group(9)
        ref = re.findall(r"\[(\d+)\]", rest)
        value = v2 if sec in GROWING else v1
        rows.append(dict(n=n, value=value, proven=b1 or b2, ref=int(ref[-1]) if ref else None))
    if not rows:
        for m in re.finditer(ROW_PLAIN, text, re.S | re.I):
            n = int(m.group(1))
            ref = re.findall(r"\[(\d+)\]", m.group(6))
            rows.append(dict(n=n, value=m.group(3), proven=bool(m.group(2)), ref=int(ref[-1]) if ref else None))
    return rows, refs


def main():
    pages, read, revision = sys.argv[1], sys.argv[2], sys.argv[3]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = {"circle-packing": [], "growing-circle-packing": []}
    stats = {}
    shas = {}
    for sec, fn in FILES.items():
        raw = open(os.path.join(pages, fn), "rb").read()
        shas[sec] = hashlib.sha256(raw).hexdigest()
        rows, refs = parse(sec, raw.decode("latin-1"))
        assert rows, sec
        any_bold = any(r["proven"] for r in rows)
        kept = proven = small = 0
        for r in rows:
            if r["proven"]:
                proven += 1
                continue
            if r["n"] <= 1 or (not any_bold and r["n"] <= SMALL.get(sec, 1)) or (sec in SMALL and r["n"] <= SMALL[sec] and sec in GROWING):
                small += 1
                continue
            cell = {"id": f"pack-{sec}-n{r['n']}", "params": {"section": sec, "n": r["n"]}, "variant": sec, "best": r["value"]}
            if r["ref"] in refs:
                cell["holder"] = refs[r["ref"]]
            out["growing-circle-packing" if sec in GROWING else "circle-packing"].append(cell)
            kept += 1
        stats[sec] = dict(rows=len(rows), kept=kept, proven=proven, small=small)
        print(f"{sec:5s} rows {len(rows):5d} kept {kept:5d} proven {proven:3d} small {small:3d}")
    common = {"keeper": "E. Specht, Packomania (packomania.com)", "page": "https://www.packomania.com/",
              "read": read, "revision": revision, "exact_values": False,
              "holder_unknown": "not named in the section's table",
              "holder_sources": "the reference in the last column of the section's table, from its list of references",
              "single_problems_left_out": 0, "quantavane_records": 0, "cells": "cells.jsonl"}
    eq_tpl = {"title": "{n} equal {shape} in {container} (Packomania {section})",
              "statement": "Place {n} non-overlapping {shape} of equal radius in {container} so that the radius is as large as possible.",
              "submission": "Text file: the radius on the first line, then {n} lines with the coordinates of the centres (decimal numbers separated by spaces or commas), in the frame given by checkers/pack_check.py for section {section}.",
              "args": ["{section}", "{n}"]}
    gr_tpl = {"title": "Circles of radii 1 to {n} in {container} (Packomania {section})",
              "statement": "Place {n} non-overlapping circles of radii 1, 2, ..., {n} in {container} whose size V (the radius of the circle, or the side of the square) is as small as possible.",
              "submission": "Text file: V on the first line, then {n} lines with the centres of the circles of radius 1, 2, ..., {n} in that order (decimal numbers), in the frame given by checkers/pack_check.py for section {section}.",
              "args": ["{section}", "{n}"]}
    eq = dict(common)
    eq.update({
        "family": "circle-packing", "title": "Equal circles and balls packed in a container with the largest radius",
        "added": "2.2", "objective": "maximize", "id_prefixes": ["pack-"],
        "cell_url": "https://www.packomania.com/{section}/{section}.html",
        "template": {"title": "{n} equal circles or balls in the container of Packomania section {section}",
                     "statement": "Place {n} non-overlapping circles (balls) of equal radius in the container of section {section} so that the radius is as large as possible.",
                     "submission": "Text file: the radius on the first line, then {n} lines with the coordinates of the centres (decimal numbers separated by spaces or commas), in the frame given by checkers/pack_check.py for section {section}.",
                     "args": ["{section}", "{n}"]},
        "checker": {"program": "pack_check.py", "value": "result"},
        "score": "the common radius (larger is better)",
        "best_text": "The best known radius in Packomania's table is {best} ({holder}); a valid packing with a larger radius improves it.",
        "open_rule": "every N of the sections csq, cci, csc, ccq, crt, scu, ssp, hsp4, hsp5 and hsp6 whose radius is not in bold (proven optimal)",
        "left_out": "; ".join(f"{s}: {v['proven']} proven, {v['small']} small N" for s, v in stats.items() if s in EQUAL)
                    + "; the regular-polygon sections and the sections with irrational radii (exact checks need algebraic numbers)",
        "variants": {s: {k: v.replace("{shape}", EQUAL[s][0]).replace("{container}", EQUAL[s][1])
                         for k, v in eq_tpl.items() if k != "args"} for s in EQUAL},
        "section_info": {s: {"shape": EQUAL[s][0], "container": EQUAL[s][1], "dimension": EQUAL[s][2],
                             "page_sha256": shas[s]} for s in EQUAL},
        "count": len(out["circle-packing"])})
    gr = dict(common)
    gr.update({
        "family": "growing-circle-packing", "title": "Circles of radii 1, 2, ..., N packed in the smallest circle or square",
        "added": "2.2", "objective": "minimize", "id_prefixes": ["pack-"],
        "cell_url": "https://www.packomania.com/{section}/{section}.html",
        "template": {"title": "Circles of radii 1 to {n} in the container of Packomania section {section}",
                     "statement": "Place {n} non-overlapping circles of radii 1, 2, ..., {n} in the container of section {section} whose size V (the radius of the circle, or the side of the square) is as small as possible.",
                     "submission": "Text file: V on the first line, then {n} lines with the centres of the circles of radius 1, 2, ..., {n} in that order (decimal numbers), in the frame given by checkers/pack_check.py for section {section}.",
                     "args": ["{section}", "{n}"]},
        "checker": {"program": "pack_check.py", "value": "result"},
        "score": "the size V of the container (smaller is better)",
        "best_text": "The best known container in Packomania's table has size {best} ({holder}); a valid packing in a smaller one improves it.",
        "open_rule": "every N of the sections ccin and csqn whose value is not in bold (proven optimal), N >= 4",
        "left_out": "; ".join(f"{s}: {v['proven']} proven, {v['small']} small N" for s, v in stats.items() if s in GROWING)
                    + "; the sections with radii i^(1/2), i^(-1/2), i^(-2/3) and i^(-1/5) (irrational radii)",
        "variants": {s: {k: v.replace("{container}", GROWING[s]) for k, v in gr_tpl.items() if k != "args"}
                     for s in GROWING},
        "section_info": {s: {"container": GROWING[s], "page_sha256": shas[s]} for s in GROWING},
        "count": len(out["growing-circle-packing"])})
    for fam, defn in (("circle-packing", eq), ("growing-circle-packing", gr)):
        d = os.path.join(root, "families", fam)
        os.makedirs(d, exist_ok=True)
        json.dump(defn, open(os.path.join(d, "family.json"), "w"), indent=1, ensure_ascii=False)
        with open(os.path.join(d, "cells.jsonl"), "w") as f:
            for c in out[fam]:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(fam, len(out[fam]))


if __name__ == "__main__":
    main()
