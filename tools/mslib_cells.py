"""mslib_cells.py: the open instances of the multi-skilled resource-constrained project scheduling library MSLIB
(J. Snauwaert and M. Vanhoucke, 2023), basic version, as the benchmark family mslib-scheduling (checked by
checkers/msrcpsp_check.py).

  python3 -I mslib_cells.py MSLIB_ZIP READ REVISION

MSLIB_ZIP is the library's release MSLIB_v2_2.zip (github.com/MarioVanhoucke/MSLIB-Multi-Skilled-Resource-Constrained-
Project-Library). Its spreadsheet "MSLIB (Parameters and BKS).xlsx", sheet "MSRCPSP (basic)", gives for every instance
of MSLIB1 to MSLIB4 a lower bound, the best known makespan and whether it is open. A cell is an instance the sheet
marks Open (its lower bound is below its best known makespan); the best known makespan is the smallest makespan the
release reports for it: the sheet's best known column, the sheet's columns of the procedures (PR40, PR ALL, GA, SA,
CPLEX, SAT; for MSLIB_Set2_3309 the column PR ALL gives 108 where the best known column gives 109) and the instance
file's informative best known solution (line 2 of its Project Module). MSLIB5 (empirical instances, no status) is
left out. Only values are stored; the instance files are not copied."""
import hashlib
import io
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from import_families import write_family  # noqa: E402
from mmrcpsp_cells import xlsx_sheets  # noqa: E402


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    zpath, read, revision = sys.argv[1:]
    zdata = open(zpath, "rb").read()
    Z = zipfile.ZipFile(io.BytesIO(zdata))
    rows = xlsx_sheets(Z.read("MSLIB_v2_2/MSLIB (Parameters and BKS).xlsx"))["MSRCPSP (basic)"]
    H = next(r for r in rows if r[:2] == ["Dataset", "Name"])
    ix = {h: H.index(h) for h in ("Dataset", "Name", "LB", "UB", "Open?")}
    # the first UB is the best known column; the later ones are the procedures' (0 or empty: no schedule found)
    proc_ub = [i for i, h in enumerate(H) if h == "UB"][1:]
    assert len(proc_ub) == 10, H
    above = rows[rows.index(H) - 1]     # the procedures' names, each above its first column
    group = {i: next(g for g in reversed(above[:i + 1]) if g) for i in proc_ub}
    inner = {}
    cells, st = [], {}
    for r in rows:
        r = r + [""] * (len(H) - len(r))
        ds = r[ix["Dataset"]]
        if not ds.startswith("MSLIB") or not r[ix["Name"]].endswith(".msrcp"):
            continue
        s = st.setdefault(ds, {"instances": 0, "open": 0, "closed": 0, "no status": 0, "best from the instance file": 0,
                               "best from a procedure's column": 0})
        s["instances"] += 1
        status = r[ix["Open?"]]
        if status != "Open":
            s["closed" if status == "Closed" else "no status"] += 1
            continue
        lb, ub = int(float(r[ix["LB"]])), int(float(r[ix["UB"]]))
        assert lb < ub, r[:2]
        if ds not in inner:
            inner[ds] = zipfile.ZipFile(io.BytesIO(Z.read(f"MSLIB_v2_2/{ds}.zip")))
        text = inner[ds].read(f"{ds}/{r[ix['Name']]}").decode("latin-1").splitlines()
        nums = [l.split() for l in text if l.strip() and l.strip()[0].isdigit()]
        file_best = int(nums[1][0])
        best, holder = ub, "MSLIB release v2.2, sheet MSRCPSP (basic) (J. Snauwaert and M. Vanhoucke)"
        p_best = min((int(float(r[i])), group[i]) for i in proc_ub if r[i] not in ("", None) and float(r[i]) > 0)
        if p_best[0] < best:
            best = p_best[0]
            holder = (f"MSLIB release v2.2, sheet MSRCPSP (basic), column {p_best[1]} (the sheet's best known column "
                      f"gives {ub}) (J. Snauwaert and M. Vanhoucke)")
            s["best from a procedure's column"] += 1
        if file_best < best:
            best, holder = file_best, "MSLIB release v2.2, the instance file's best known solution"
            s["best from the instance file"] += 1
        s["open"] += 1
        num = r[ix["Name"]].rsplit("_", 1)[1].split(".")[0]
        cells.append({"id": f"mslib-{ds[5:]}-{num}", "params": {"set": ds, "file": r[ix["Name"]]}, "best": str(best),
                      "bound": str(lb), "holder": holder})
    defn = {
        "family": "mslib-scheduling",
        "title": "Multi-skilled resource-constrained project scheduling (MSRCPSP, basic), shortest makespan",
        "added": "2.2",
        "objective": "minimize",
        "id_prefixes": ["mslib-"],
        "keeper": ("MSLIB, J. Snauwaert and M. Vanhoucke, OR&S group, Ghent University (A classification and new "
                   "benchmark instances for the multi-skilled resource-constrained project scheduling problem, EJOR "
                   "307 (2023) 1-19)"),
        "page": "https://github.com/MarioVanhoucke/MSLIB-Multi-Skilled-Resource-Constrained-Project-Library",
        "cell_url": "https://www.projectmanagement.ugent.be/research/project_scheduling/MSRCPSP",
        "read": read,
        "revision": revision,
        "template": {
            "title": "MSRCPSP instance {file} ({set})",
            "statement": ("Schedule the activities of instance {file} of {set} and assign to each activity, for every "
                          "skill type, as many resources mastering that skill as it requires, so that every activity "
                          "starts after its predecessors finish and no resource works on two activities at once, "
                          "finishing as early as possible (the basic multi-skilled RCPSP; the instance file is in the "
                          "MSLIB release, MSLIB_v2_2.zip)."),
            "submission": ("Text file: one line per activity in the instance's order (the dummies included): the start "
                           "time, then 'resource:skill' for every resource the activity uses (numbered from 1); see "
                           "checkers/msrcpsp_check.py."),
            "args": ["instances/mslib/{set}/{file}"],
        },
        "checker": {"program": "msrcpsp_check.py", "value": "result"},
        "score": "the makespan (smaller is better)",
        "best_text": "The best known makespan is {best} ({holder}); a feasible schedule that finishes earlier improves it.",
        "bound_kind": "lower bound",
        "bound_source": "the lower bound in MSLIB's sheet MSRCPSP (basic)",
        "holder_unknown": "MSLIB release v2.2",
        "holder_sources": ("MSLIB's sheet (the procedures that found the values are its columns: PR, GA, SA, CPLEX, "
                           "SAT); the best known value is the smallest makespan the release reports, which is the "
                           "best known column's except for MSLIB_Set2_3309 (PR ALL 108, best known column 109)"),
        "open_rule": "every instance of MSLIB1 to MSLIB4 that the sheet marks Open (lower bound below the best known makespan)",
        "left_out": ("the closed instances and MSLIB5 (empirical instances with no status); MSLIB publishes values, not "
                     "schedules, so no published schedule is replayed"),
        "literature": "families/mslib-scheduling/literature.json",
        "instances": ("Instance files are not copied here: unpack MSLIB1.zip to MSLIB4.zip from MSLIB_v2_2.zip (the "
                      "library's GitHub release) under instances/mslib/, so that "
                      "instances/mslib/MSLIB1/MSLIB_Set1_1.msrcp exists."),
        "source_sha256": {"MSLIB_v2_2.zip": hashlib.sha256(zdata).hexdigest()},
        "counts": st,
    }
    return defn, cells


if __name__ == "__main__":
    res = main()
    if isinstance(res, int):
        sys.exit(res)
    defn, cells = res
    write_family(defn, cells)
    print(json.dumps(defn["counts"]))
