"""scheduleopt_cells.py: the open job shop and flexible job shop instances of ScheduleOpt's benchmark library
(github.com/ScheduleOpt/benchmarks, CC BY-SA 4.0; its best-known-solutions archive records the best upper and lower
bounds from any source) as the families job-shop and flexible-job-shop, checked by checkers/jsp_check.py.

  python3 -I scheduleopt_cells.py RAW_DIR READ REVISION OPTIMIZIZER_DIR

RAW_DIR holds commit.txt (the commit read), tree.txt (the repository's file list at that commit), the two bks.json
files (saved as jobshop_solutions_bks.json and flexible-jobshop_solutions_bks.json) and, after a first run, the
instance files under jsp/ and fjsp/ (downloaded here, one at a time, from raw.githubusercontent.com at that commit).
OPTIMIZIZER_DIR holds O. Shylo's tables of bounds for Taillard's and Demirkol's instances and SWV, ABZ, YN
(optimizizer.com; TA.html, DMU.html, Extra.html). A job shop cell is open when ScheduleOpt's lower bound is below its
upper bound and, where Shylo's table lists the instance, his bounds differ as well; its best known value is the smaller
of the two upper bounds. Instances stored only as zip archives (the 1000-job tai and dct instances) are left out, and
so are the flexible assembly instances (yfjs, dafjs), whose format and model this checker does not read.
Prints the fetch.sh lines for the instance files."""
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def shylo(d):
    out = {}
    for p in ("TA", "DMU", "Extra"):
        s = open(os.path.join(d, p + ".html"), encoding="utf-8", errors="replace").read()
        t = re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S))))
        for name, a, b, lb, lr, ub, ur in re.findall(r"([A-Z][a-z]+\d+)(?:_[a-z]+_\d+_\d+_\d+)? (\d+)x(\d+) (\d+) \( ?([^)]*?) ?\) (\d+) \( ?([^)]*?) ?\)", t):
            nm = name.lower()
            m = re.fullmatch(r"([a-z]+)(\d+)", nm)
            pre, num = m.group(1), int(m.group(2))
            key = {"ta": f"ta{num:02d}js", "dmu": f"dmu{num:02d}", "swv": f"swv{num:02d}", "abz": f"abz{num}", "yn": f"yn{num}"}[pre]
            out[key] = (int(lb), int(ub), lr.strip(), ur.strip())
    return out


def holder_of(x):
    ub = x["upper_bound"]
    hits = [h for h in x["history"]["ub"] if h["value"] == ub]
    if not hits:
        return None
    h = min(hits, key=lambda h: h.get("date") or "9999")
    return f"{h.get('solver') or 'unnamed'}, {h.get('date') or 'undated'} (ScheduleOpt's archive)"


def fetch(url, path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        time.sleep(1)
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120) as r:
            data = r.read()
        open(path, "wb").write(data)
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    raw, read, revision, opt_dir = sys.argv[1:5]
    sha = open(os.path.join(raw, "commit.txt")).read().strip()
    tree = [l.strip() for l in open(os.path.join(raw, "tree.txt"))]
    sh = shylo(opt_dir)
    fetch_lines, fams = [], {}
    # job shop
    js = json.load(open(os.path.join(raw, "jobshop_solutions_bks.json")))
    jt = [p for p in tree if p.startswith("jobshop/instances/text/")]
    cells, st = [], {"instances": len(js), "closed": 0, "closed in Shylo's table": 0, "zip only": 0, "kept": 0}
    for x in js:
        name = x["instance"]
        if x["lower_bound"] >= x["upper_bound"]:
            st["closed"] += 1
            continue
        o = sh.get(name)
        if o and o[0] >= o[1]:
            st["closed in Shylo's table"] += 1
            continue
        c = [p for p in jt if re.search(r"/" + re.escape(name) + r"\.txt$", p)]
        if not c:
            st["zip only"] += 1
            continue
        best, holder, lb = x["upper_bound"], holder_of(x), x["lower_bound"]
        if o and o[1] < best:
            best, holder = o[1], f"{o[3] or 'unnamed'} (O. Shylo's table, optimizizer.com)"
        if o:
            lb = max(lb, o[0])
        local = f"instances/jsp/{name}.txt"
        digest = fetch(f"https://raw.githubusercontent.com/ScheduleOpt/benchmarks/{sha}/{c[0]}", os.path.join(raw, "jsp", name + ".txt"))
        fetch_lines.append(f"slow jsp/{name}.txt https://raw.githubusercontent.com/ScheduleOpt/benchmarks/{sha}/{c[0]} {digest}")
        cell = {"id": f"jsp-{name}", "params": {"name": name, "file": local}, "best": str(best), "bound": str(lb)}
        if holder:
            cell["holder"] = holder
        cells.append(cell)
        st["kept"] += 1
    fams["job-shop"] = (cells, st)
    # flexible job shop
    fx = json.load(open(os.path.join(raw, "flexible-jobshop_solutions_bks.json")))
    ft = [p for p in tree if p.startswith("flexible-jobshop/instances/fjsp/")]
    cells, st = [], {"instances": len(fx), "closed": 0, "flexible assembly (yfjs, dafjs)": 0, "kept": 0}
    for x in fx:
        name = x["instance"]
        if x["lower_bound"] >= x["upper_bound"]:
            st["closed"] += 1
            continue
        m = re.fullmatch(r"(.+)_(edata|rdata|vdata|sdata)", name)
        if m:
            pat = rf"/HurinkJurischThole1994/{m.group(2)}/{re.escape(m.group(1))}\.txt$"
        elif re.fullmatch(r"dpp\d+a", name):
            pat = rf"/DauzerePeresPaulli1994/{name[3:]}\.txt$"
        else:
            pat = r"/" + re.escape(name) + r"\.txt$"
        c = [p for p in ft if re.search(pat, p)]
        if not c:
            st["flexible assembly (yfjs, dafjs)"] += 1
            continue
        local = f"instances/fjsp/{name}.txt"
        digest = fetch(f"https://raw.githubusercontent.com/ScheduleOpt/benchmarks/{sha}/{c[0]}", os.path.join(raw, "fjsp", name + ".txt"))
        fetch_lines.append(f"slow fjsp/{name}.txt https://raw.githubusercontent.com/ScheduleOpt/benchmarks/{sha}/{c[0]} {digest}")
        cell = {"id": f"fjsp-{name}", "params": {"name": name, "file": local}, "best": str(x["upper_bound"]),
                "bound": str(x["lower_bound"])}
        h = holder_of(x)
        if h:
            cell["holder"] = h
        cells.append(cell)
        st["kept"] += 1
    fams["flexible-job-shop"] = (cells, st)
    for fam, (cells, st) in fams.items():
        flex = fam == "flexible-job-shop"
        defn = {
            "family": fam,
            "title": ("Flexible job shop" if flex else "Job shop") + " scheduling: the shortest makespan",
            "added": "2.2", "objective": "minimize", "id_prefixes": ["fjsp-" if flex else "jsp-"],
            "keeper": "ScheduleOpt, benchmark of scheduling problems (" + ("FJSPLib" if flex else "JSPLib") + "; github.com/ScheduleOpt/benchmarks, CC BY-SA 4.0)" + ("" if flex else ", with O. Shylo's table of bounds (optimizizer.com)"),
            "page": "https://scheduleopt.github.io/benchmarks/" + ("fjsplib/" if flex else "jsplib/"),
            "read": read, "revision": revision,
            "template": {"title": ("Flexible job shop" if flex else "Job shop") + " instance {name}",
                         "statement": ("Schedule the operations of instance {name}, each on one of its machines, " if flex else "Schedule the operations of instance {name} ")
                                      + "so that each job's operations run in order, no machine runs two operations at once, and the makespan (the latest end) is as small as possible.",
                         "submission": ("Text file: one line per job: for each of its operations the machine chosen and the start time" if flex else "Text file: one line per job: the start time of each of its operations, in order")
                                       + " (integers); the instance file is fetched by fetch.sh into {file}; see checkers/jsp_check.py.",
                         "args": (["--flexible", "{file}"] if flex else ["{file}"])},
            "checker": {"program": "jsp_check.py", "value": "result"},
            "score": "the makespan (smaller is better)",
            "best_text": "The best known makespan is {best} ({holder}); a valid schedule with a shorter makespan improves it.",
            "bound_kind": "lower bound", "bound_source": "the best known lower bound in the keeper's archive" + ("" if flex else " (the larger of ScheduleOpt's and Shylo's)"),
            "holder_unknown": "not named in the archive",
            "holder_sources": "the solver or publication of the archive's earliest entry with the best upper bound" + ("" if flex else ", or Shylo's reference where his upper bound is lower"),
            "open_rule": "every instance whose best known lower bound is below its best known upper bound in the keeper's archive" + ("" if flex else " and, where O. Shylo's table lists it, there as well"),
            "left_out": ", ".join(f"{v} {k}" for k, v in st.items() if k not in ("instances", "kept")) + f" (of {st['instances']} instances)",
            "instances": "fetched by fetch.sh from raw.githubusercontent.com/ScheduleOpt/benchmarks at commit " + sha + ", each checked against its SHA-256",
            "cells": "cells.jsonl", "count": len(cells), "quantavane_records": 0, "single_problems_left_out": 0,
        }
        d = os.path.join(ROOT, "families", fam)
        os.makedirs(d, exist_ok=True)
        json.dump(defn, open(os.path.join(d, "family.json"), "w"), indent=1, ensure_ascii=False)
        with open(os.path.join(d, "cells.jsonl"), "w") as f:
            for c in cells:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(fam, st)
    open(os.path.join(raw, "fetch_lines.txt"), "w").write("\n".join(fetch_lines) + "\n")
    print(len(fetch_lines), "instance files")


if __name__ == "__main__":
    main()
