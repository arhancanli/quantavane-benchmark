"""packomania_alg_cells.py: the Packomania sections whose check needs algebraic numbers, as two benchmark families
checked by checkers/pack_alg_check.py.

  python3 -I packomania_alg_cells.py PAGES_DIR READ REVISION

  families/polygon-circle-packing   equal circles in the regular n-gons, n = 5..17 (largest radius)
  families/unequal-circle-packing   circles of radii i^(1/2), i^(-1/2), i^(-2/3), i^(-1/5) in the smallest circle,
                                    and of radii i^(1/2) and (N/i)^(1/2) in the smallest square (container size)

PAGES_DIR holds the section pages saved as SECTION_SECTION.html (coc.html for the octagon). A cell is one N whose value
is not in bold (Packomania: proven optimal packings are in bold; these sections mark none). Left out: N <= 2 for the
polygons (one circle: the incircle; two: a one-dimensional question), N <= 3 for the squares (as for csqn); the
circle sections list N from 5. The section csqc (radii i^(-2/3) in a square) is left out: its page's radius and ratio
columns do not agree with each other for every N (for N = 20 their product is 7.4392, against 7.3681 for N = 5's
convention), so its frame could not be fixed."""
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pc", os.path.join(HERE, "packomania_cells.py"))
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)

POLY = {"cpt": (5, "pentagon"), "chx": (6, "hexagon"), "chp": (7, "heptagon"), "coc": (8, "octagon"),
        "cno": (9, "nonagon"), "cdc": (10, "decagon"), "chd": (11, "hendecagon"), "cdd": (12, "dodecagon"),
        "ctd": (13, "tridecagon"), "crd": (14, "tetradecagon"), "cpd": (15, "pentadecagon"),
        "cxd": (16, "hexadecagon"), "ced": (17, "heptadecagon")}
RAD = {"ccir": ("i^(1/2)", "a circle of radius V centred at 0", 0), "ccis": ("i^(-1/2)", "a circle of radius V centred at 0", 0),
       "ccic": ("i^(-2/3)", "a circle of radius V centred at 0", 0), "ccib": ("i^(-1/5)", "a circle of radius V centred at 0", 0),
       "csqr": ("i^(1/2)", "the square [0,V]^2", 3), "csqs": ("(N/i)^(1/2)", "the square [0,V]^2", 3)}


def main():
    pages, read, revision = sys.argv[1], sys.argv[2], sys.argv[3]
    pc.GROWING.update({s: "" for s in RAD})     # parse() then takes the second number, the ratio: V in our frames
    root = os.path.dirname(HERE)
    out = {"polygon-circle-packing": [], "unequal-circle-packing": []}
    stats, shas = {}, {}
    for sec in list(POLY) + list(RAD):
        fn = os.path.join(pages, "coc.html" if sec == "coc" else f"{sec}_{sec}.html")
        raw = open(fn, "rb").read()
        shas[sec] = hashlib.sha256(raw).hexdigest()
        rows, refs = pc.parse(sec, raw.decode("latin-1"))
        assert rows, sec
        best = {}
        for r in rows:
            best.setdefault(r["n"], r)
        kept = proven = small = 0
        fam = "polygon-circle-packing" if sec in POLY else "unequal-circle-packing"
        for n in sorted(best):
            r = best[n]
            if r["proven"]:
                proven += 1
                continue
            if (sec in POLY and n <= 2) or (sec in RAD and n <= RAD[sec][2]):
                small += 1
                continue
            cell = {"id": f"pack-{sec}-n{n}", "params": {"section": sec, "n": n}, "variant": sec,
                    "best": r["value"]}
            if r["ref"] in refs:
                cell["holder"] = refs[r["ref"]]
            out[fam].append(cell)
            kept += 1
        stats[sec] = dict(rows=len(rows), kept=kept, proven=proven, small=small, repeated=len(rows) - len(best))
        print(f"{sec:5s} rows {len(rows):5d} kept {kept:5d} proven {proven:3d} small {small:3d} repeated {len(rows) - len(best)}")
    common = {"keeper": "E. Specht, Packomania (packomania.com)", "page": "https://www.packomania.com/",
              "read": read, "revision": revision, "exact_values": False, "added": "2.2", "id_prefixes": ["pack-"],
              "cell_url": "https://www.packomania.com/{section}/{section}.html",
              "holder_unknown": "not named in the section's table",
              "holder_sources": "the reference in the last column of the section's table, from its list of references",
              "single_problems_left_out": 0, "quantavane_records": 0, "cells": "cells.jsonl",
              "checker": {"program": "pack_alg_check.py", "value": "result"},
              "pending_queue": ("Packomania's list of pending requests (pending.html, dated 9 Nov 2026, read 14 Nov) holds "
                                "unreviewed candidates for several of these sections (among them the pentagon, hexagon, "
                                "heptagon, decagon, tetradecagon, pentadecagon, hexadecagon, heptadecagon and ccis); their "
                                "values are not published, so a cell's best known value is the table's, and a candidate in "
                                "the queue may already beat it")}
    poly = dict(common)
    poly.update({
        "family": "polygon-circle-packing", "title": "Equal circles in a regular polygon with the largest radius",
        "objective": "maximize",
        "template": {"title": "{n} equal circles in the regular polygon of Packomania section {section}",
                     "statement": "Place {n} non-overlapping circles of equal radius in the regular polygon of section {section} (circumradius 1) so that the radius is as large as possible.",
                     "submission": "Text file: the radius on the first line, then {n} lines with the centres (decimal numbers), in the frame of checkers/pack_alg_check.py: the polygon centred at 0 with a vertex at (1, 0).",
                     "args": ["{section}", "{n}"]},
        "variants": {s: {"title": f"{{n}} equal circles in the regular {POLY[s][1]} with circumradius 1 (Packomania {s})",
                         "statement": f"Place {{n}} non-overlapping circles of equal radius in the regular {POLY[s][1]} ({POLY[s][0]} sides) with circumradius 1 so that the radius is as large as possible."}
                     for s in POLY},
        "score": "the common radius (larger is better)",
        "best_text": "The best known radius in Packomania's table is {best} ({holder}); a valid packing with a larger radius improves it.",
        "open_rule": "every N >= 3 of the regular-polygon sections cpt, chx, chp, coc, cno, cdc, chd, cdd, ctd, crd, cpd, cxd and ced whose radius is not in bold (proven optimal; none is)",
        "left_out": "; ".join(f"{s}: {v['proven']} proven, {v['small']} small N" for s, v in stats.items() if s in POLY),
        "section_info": {s: {"sides": POLY[s][0], "page_sha256": shas[s]} for s in POLY},
        "frames": "checked on Packomania's coordinate files cpt30, chx30, coc30, ced30 and cxd30 (rotated by a multiple of pi/2n into our frame): each passes 10^-9 below the listed radius and fails 10^-9 above",
        "count": len(out["polygon-circle-packing"])})
    rad = dict(common)
    rad.update({
        "family": "unequal-circle-packing", "title": "Circles of radii i^(1/2), i^(-1/2), i^(-2/3), i^(-1/5) in the smallest circle or square",
        "objective": "minimize",
        "template": {"title": "Circles i = 1..{n} with the radii of Packomania section {section} in the smallest container",
                     "statement": "Place {n} non-overlapping circles, circle i of the radius given by section {section}, in the container of that section whose size V is as small as possible.",
                     "submission": "Text file: V on the first line, then {n} lines with the centres of circles 1, 2, ..., {n} in that order (decimal numbers), in the frame of checkers/pack_alg_check.py for section {section}.",
                     "args": ["{section}", "{n}"]},
        "variants": {s: {"title": f"Circles of radii {RAD[s][0]}, i = 1..{{n}}, in {RAD[s][1]} (Packomania {s})",
                         "statement": f"Place {{n}} non-overlapping circles, circle i of radius {RAD[s][0]}, in {RAD[s][1]} with V as small as possible."}
                     for s in RAD},
        "score": "the size V of the container (smaller is better)",
        "best_text": "The best known container in Packomania's table has size {best} ({holder}); a valid packing in a smaller one improves it.",
        "open_rule": "every listed N of the sections ccir, ccis, ccic and ccib (N = 5..100) and every N >= 4 of csqr and csqs whose value is not in bold (none is)",
        "left_out": "; ".join(f"{s}: {v['proven']} proven, {v['small']} small N" for s, v in stats.items() if s in RAD)
                    + "; the section csqc, whose radius and ratio columns disagree for some N",
        "section_info": {s: {"radii": RAD[s][0], "container": RAD[s][1], "page_sha256": shas[s]} for s in RAD},
        "frames": "checked on Packomania's coordinate files ccir20, ccis20, ccic20, ccib20, csqr20 and csqs20 (Packomania's ratio is V; for csqs it is the side over the smallest radius, hence the radii (N/i)^(1/2)): each passes with the coordinates spread by 10^-9 and V 10^-8 above the listed value, and fails 10^-8 below",
        "count": len(out["unequal-circle-packing"])})
    for fam, defn in (("polygon-circle-packing", poly), ("unequal-circle-packing", rad)):
        d = os.path.join(root, "families", fam)
        os.makedirs(d, exist_ok=True)
        json.dump(defn, open(os.path.join(d, "family.json"), "w"), indent=1, ensure_ascii=False)
        with open(os.path.join(d, "cells.jsonl"), "w") as f:
            for c in out[fam]:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(fam, len(out[fam]))


if __name__ == "__main__":
    main()
