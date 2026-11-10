"""Writes the cells of the Quantavane Originals from their certificates (standard library only).

  python3 -I tools/cells.py [FAMILY ...]        (run from anywhere; no argument: every family with cells)

A family is one question (problems/ID.json); its cells are the same question at each value of its natural parameter
(the number of antennas, the side of a grid, the number of digits, ...), the way the benchmark's table families are
counted. The problem file's "cells" block names the parameters, the checker arguments and the statement of a cell
(templates with {PARAM} and {best}), which cells are exact (an exhaustive search finished) and how the others were
found. Each certificate is refs/cells/ID/P.txt (P the parameter values joined by '_'); the headline cell uses the
problem's own certificate. Every certificate is run through the family's checker, and the value it proves is the
cell's value: nothing is typed by hand. Output: cells/ID.jsonl, one line per cell, sorted by parameter."""
import datetime
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(HERE))


def fill(t, values):
    return [fill(x, values) for x in t] if isinstance(t, list) else t.format(**values)


def run_checker(program, args, path):
    full = [os.path.join(ROOT, a) if a.startswith("collections/") else a for a in args]
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, program)] + full + [path], capture_output=True,
                       text=True)
    m = re.findall(r"^RESULT (\S+)$", r.stdout, re.M)
    return r.returncode, (m[-1] if m else None)


def key(params, names):
    return tuple(int(params[n]) if re.fullmatch(r"-?\d+", str(params[n])) else str(params[n]) for n in names)


def family_cells(p, old=None):
    blk = p["cells"]
    names = blk["params"]
    old = {c["id"]: c for c in (old or [])}
    found = []
    d = os.path.join(HERE, "refs", "cells", p["id"])
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".txt"):
                vals = f[:-4].split("_")
                if len(vals) != len(names):
                    raise ValueError(f"{p['id']}: certificate name {f} does not give {names}")
                found.append((dict(zip(names, vals)), os.path.relpath(os.path.join(d, f), ROOT)))
    head = {n: str(v) for n, v in blk["headline"].items()}
    found = [x for x in found if x[0] != head] + [(head, p["best_known"]["provenance"]["certificate"])]
    exact = set(blk.get("exact", []))
    out = []
    for params, cert in found:
        stem = "_".join(params[n] for n in names)
        cid = p["id"] + "-" + stem.replace("_", "-")
        code, val = run_checker(p["checker"]["program"], fill(blk["args"], params), os.path.join(ROOT, cert))
        if code != 0 or val is None:
            raise ValueError(f"{cid}: the checker refused {cert}")
        prev = old.get(cid)
        date = prev["date"] if prev and prev["best"] == val else datetime.date.today().isoformat()
        line = {"id": cid, "family": p["id"], "params": {n: key(params, [n])[0] for n in names}, "best": val,
                "exact": stem in exact,
                "how": blk["exact_how"] if stem in exact else blk.get("how_by_cell", {}).get(stem, blk["how"]),
                "date": date, "certificate": cert}
        if params == head:
            line["headline"] = True
        out.append(line)
    out.sort(key=lambda c: key(c["params"], names))
    return out


def main():
    ids = sys.argv[1:]
    probs = {}
    for f in sorted(os.listdir(os.path.join(HERE, "problems"))):
        if f.endswith(".json"):
            p = json.load(open(os.path.join(HERE, "problems", f)))
            if "cells" in p and (not ids or p["id"] in ids):
                probs[p["id"]] = p
    os.makedirs(os.path.join(HERE, "cells"), exist_ok=True)
    for pid, p in probs.items():
        path = os.path.join(HERE, "cells", pid + ".jsonl")
        old = [json.loads(l) for l in open(path)] if os.path.exists(path) else []
        cells = family_cells(p, old)
        with open(path, "w") as fh:
            for c in cells:
                fh.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"{pid:22s} {len(cells):4d} cells, {sum(c['exact'] for c in cells):4d} exact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
