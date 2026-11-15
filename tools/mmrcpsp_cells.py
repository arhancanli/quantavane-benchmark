"""mmrcpsp_cells.py: the open instances of the multi-mode resource-constrained project scheduling sets MMLIB50,
MMLIB100 and MMLIB+ (V. Van Peteghem and M. Vanhoucke, 2014) as the benchmark family multi-mode-scheduling (checked by
checkers/rcpsp_check.py, format mm).

  python3 -I mmrcpsp_cells.py SITE_DIR MMLIB_ZIP READ REVISION

SITE_DIR holds the Solutions Update dataset files (solutionsupdate.ugent.be/sites/default/files/datasets/) MM50_7.csv,
MM100_6.csv and MMplus_2.csv with their best known solutions files *_BKS.csv; MMLIB_ZIP is the library's release
MMLIB_v2_1.zip (github.com/MarioVanhoucke/MMLIB-Multi-Mode-Resource-Constrained-Project-Library), whose spreadsheet
"MMLIB (Parameters and BKS).xlsx" gives a literature lower and upper bound per instance. The best known makespan is the
smallest upper bound of the three (dataset file, best known solutions file, spreadsheet) and the lower bound the
largest (with the dataset file's optimal values); an instance is open when the lower bound is below the best known
makespan. Only values are stored; the instance files are not copied."""
import hashlib
import io
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from import_families import ghent_bks, ghent_rows, write_family  # noqa: E402

SETS = (("MM50_7", "MMLIB50", "MMLIB50", 54), ("MM100_6", "MMLIB100", "MMLIB100", 114),
        ("MMplus_2", "MMLIB+", "MMLIB+", 1965))   # dataset file, spreadsheet sheet, folder, open in the site's table
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def xlsx_sheets(data):
    """{sheet name: rows of cell texts} of an .xlsx file (standard library only)."""
    Z = zipfile.ZipFile(io.BytesIO(data))
    strings = []
    if "xl/sharedStrings.xml" in Z.namelist():
        for si in ET.fromstring(Z.read("xl/sharedStrings.xml")).findall(NS + "si"):
            strings.append("".join(t.text or "" for t in si.iter(NS + "t")))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(Z.read("xl/_rels/workbook.xml.rels"))}
    out = {}
    for sh in ET.fromstring(Z.read("xl/workbook.xml")).find(NS + "sheets"):
        target = rels[sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")]
        rows = []
        for row in ET.fromstring(Z.read("xl/" + target.lstrip("/").replace("xl/", ""))).iter(NS + "row"):
            cells = {}
            for c in row.findall(NS + "c"):
                col = 0
                for ch in re.match(r"[A-Z]+", c.get("r")).group(0):
                    col = col * 26 + ord(ch) - 64
                v = c.find(NS + "v")
                cells[col - 1] = "" if v is None else (strings[int(v.text)] if c.get("t") == "s" else v.text)
            rows.append([cells.get(i, "") for i in range(max(cells) + 1)] if cells else [])
        out[sh.get("name")] = rows
    return out


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        return 2
    site, zpath, read, revision = sys.argv[1:]
    zdata = open(zpath, "rb").read()
    sheets = xlsx_sheets(zipfile.ZipFile(io.BytesIO(zdata)).read("MMLIB_v2_1/MMLIB (Parameters and BKS).xlsx"))
    rows, stats, sha = [], {}, {"MMLIB_v2_1.zip": hashlib.sha256(zdata).hexdigest()}
    for ds, sheet, folder, table_open in SETS:
        for fn in (ds + ".csv", ds + "_BKS.csv"):
            sha[fn] = hashlib.sha256(open(os.path.join(site, fn), "rb").read()).hexdigest()
        fmt, table, refs = ghent_rows(os.path.join(site, ds + ".csv"))
        assert fmt == "mm", fmt
        bks = ghent_bks(os.path.join(site, ds + "_BKS.csv"))
        sh = sheets[sheet]
        H = sh[1]
        lit = {r[H.index("FileName")]: (int(float(r[H.index("LB-lit")])), int(float(r[H.index("UB-lit")])))
               for r in sh[2:] if len(r) > H.index("UB-lit") and r[0].strip().isdigit() and r[H.index("UB-lit")]}
        st = {"instances": 0, "closed": 0, "open": 0, "best from the spreadsheet": 0, "lower bound from the spreadsheet": 0}
        for r in table:
            st["instances"] += 1
            i, file = int(r["ID"]), r["Ref1"]
            lb, ub = int(r["LB value"]), int(r["UB value"])
            opt = int(r["OPT value"] or 0)
            holder = None
            ref = r.get("UB ref", "")
            if ref.isdigit() and int(ref) in refs:
                holder = refs[int(ref)]
            best = ub
            if i in bks and bks[i][1] < best:
                best, holder = bks[i][1], "the site's best known solutions file (no author given there)"
            if file in lit:
                llb, lub = lit[file]
                if lub < best:
                    best, holder = lub, "MMLIB release v2.1, MMLIB (Parameters and BKS).xlsx"
                    st["best from the spreadsheet"] += 1
                if llb > lb:
                    lb = llb
                    st["lower bound from the spreadsheet"] += 1
            if opt:
                lb = max(lb, opt)
            if (i in bks and bks[i][0] == "optimal" and bks[i][1] == best) or best <= lb:
                st["closed"] += 1
                continue
            st["open"] += 1
            rows.append({"id": f"mmrcpsp-{folder.lower().replace('+', 'plus')}-{i}",
                         "params": {"set": folder, "id": i, "file": file}, "best": str(best), "bound": str(lb),
                         **({"holder": holder} if holder else {})})
        st["open in the site's table (September 2026)"] = table_open
        stats[folder] = st
    defn = {
        "family": "multi-mode-scheduling",
        "title": "Multi-mode resource-constrained project scheduling (MMRCPSP), shortest makespan",
        "added": "2.2",
        "objective": "minimize",
        "id_prefixes": ["mmrcpsp-"],
        "keeper": ("Solutions Update (solutionsupdate.ugent.be), M. Vanhoucke and J. Coelho, OR&S group, Ghent "
                   "University, with the MMLIB library (V. Van Peteghem and M. Vanhoucke)"),
        "page": "http://solutionsupdate.ugent.be/mrcpsp",
        "cell_url": "http://solutionsupdate.ugent.be/",
        "read": read,
        "revision": revision,
        "template": {
            "title": "MMRCPSP instance {file} ({set})",
            "statement": ("Choose a mode for every activity of instance {file} of the {set} set and schedule the "
                          "activities so that every activity starts after its predecessors finish, no renewable "
                          "resource is used beyond its capacity at any time and the chosen modes use no nonrenewable "
                          "resource beyond its capacity, finishing as early as possible (the instance file is in the "
                          "MMLIB release, MMLIB_v2_1.zip)."),
            "submission": ("Text file: the mode of every activity (from 1) and then the start time of every activity, "
                           "in the instance's order, integers separated by spaces, commas or semicolons; the dummy "
                           "first and last activities' modes may be left out, as in Solutions Update's best known "
                           "solutions files."),
            "args": ["mm", "instances/mmrcpsp/{set}/{file}"],
        },
        "checker": {"program": "rcpsp_check.py", "value": "result"},
        "score": "the makespan (smaller is better)",
        "best_text": ("The best known makespan is {best} ({holder}); a feasible schedule that finishes earlier "
                      "improves it."),
        "bound_kind": "lower bound",
        "bound_source": "the largest of the lower bounds in the set's dataset file and in the MMLIB spreadsheet",
        "holder_unknown": "not named in the dataset file",
        "holder_sources": ("the reference of the upper bound in the set's dataset file (its list of references); a "
                           "smaller makespan in the best known solutions file or the spreadsheet, with that source"),
        "open_rule": ("every instance whose best known makespan (the smallest upper bound of the dataset file, the best "
                      "known solutions file and the MMLIB spreadsheet) is above its lower bound (the largest of the "
                      "dataset file's lower bound and optimal value and the spreadsheet's lower bound), and which the "
                      "best known solutions file does not mark optimal"),
        "left_out": ("the closed instances; the Boctor sets (their instance files are not in the MMLIB release); the "
                     "site's table of September 2026 counts 54 and 114 open instances in MMLIB50 and MMLIB100 where "
                     "the dataset files give 55 and 115 (the difference could not be identified, so all are kept)"),
        "instances": ("Instance files are not copied here: unpack MMLIB50.zip, MMLIB100.zip and MMLIB+.zip from "
                      "MMLIB_v2_1.zip (the library's GitHub release) under instances/mmrcpsp/, so that "
                      "instances/mmrcpsp/MMLIB50/J501_1.mm exists."),
        "source_sha256": sha,
        "counts": stats,
    }
    return defn, rows


if __name__ == "__main__":
    res = main()
    if isinstance(res, int):
        sys.exit(res)
    defn, rows = res
    write_family(defn, rows)
    print(json.dumps(defn["counts"]))
