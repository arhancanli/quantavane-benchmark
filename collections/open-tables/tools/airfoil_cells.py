#!/usr/bin/env python3
"""Writes cells/airfoil-ld.jsonl and cells/airfoil-cd.jsonl (standard library only).

  python3 -I tools/airfoil_cells.py SCAN.jsonl     baselines: the best NACA section of tools/airfoil_scan.py's output
                                                    for each cell, written as a certificate and checked by the checker
  python3 -I tools/airfoil_cells.py                 re-check every certificate in refs/cells/airfoil-*/ and rewrite the
                                                    cells (the best certified design is the cell's value)

No value has been published for this model, so every cell is a first entry. A cell keeps its baseline (the best NACA
4- or 5-digit section at the best angle of the scan, a published shape scored by the model) and, when a design of
ours scores better, that design as the cell's value. Every value is the checker's output on the certificate file."""
import json
import math
import os
import re
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(HERE))
CHECKER = os.path.join(HERE, "checkers", "airfoil_check.py")
DATE = "2026-11-12"
LD = [(re_, t) for re_ in (500000, 1000000, 3000000, 6000000, 9000000) for t in ("0.06", "0.09", "0.12", "0.15")]
CD = [(re_, cl, t) for re_ in (1000000, 3000000, 9000000) for cl in ("0.3", "0.6", "0.9") for t in ("0.09", "0.12")]
CM_MIN = -0.10


def re_tag(re_):
    return f"{re_ // 1000}k" if re_ < 1000000 else f"{re_ // 1000000}m"


def grid():
    for re_, t in LD:
        yield {"id": f"airfoil-ld-re{re_tag(re_)}-t{t[2:]}", "family": "airfoil-ld",
               "params": {"re": str(re_), "tmin": t, "mode": "ld", "clmin": "0"}, "checker_args": ["ld", str(re_), t, "0"]}
    for re_, cl, t in CD:
        yield {"id": f"airfoil-cd-re{re_tag(re_)}-cl{cl}-t{t[2:]}", "family": "airfoil-cd",
               "params": {"re": str(re_), "clmin": cl, "tmin": t, "mode": "cd"}, "checker_args": ["cd", str(re_), t, cl]}


def check(args, path):
    r = subprocess.run([sys.executable, "-I", CHECKER] + args + [path], capture_output=True, text=True)
    m = re.findall(r"^RESULT (\d+)(?:/(\d+))?$", r.stdout, re.M)
    if r.returncode != 0 or not m:
        return None, r.stdout
    return Fraction(int(m[-1][0]), int(m[-1][1] or 1)), r.stdout


def text(fr):
    return str(fr.numerator) if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"


def decimal(fr, mode):
    return f"{float(fr):.2f}" if mode == "ld" else f"{float(fr):.6f}"


def score(mode, cl, cd):
    if mode == "ld":
        return Fraction(math.floor(Fraction(cl) / Fraction(cd) * 100), 100)
    return Fraction(math.ceil(Fraction(cd) * 1000000), 1000000)


def baselines(scan_path):
    rows = {}
    for line in open(scan_path):
        r = json.loads(line)
        if "polar" in r:
            rows.setdefault(r["re"], []).append(r)
    cells = []
    for c in grid():
        p = c["params"]
        mode, re_, tmin, clmin = p["mode"], int(p["re"]), float(p["tmin"]), float(p["clmin"])
        best = None
        for r in rows.get(re_, []):
            if r["thickness"] < tmin:
                continue
            for a, cl, cd, cm in r["polar"]:
                if cd is None or cm < CM_MIN or (mode == "ld" and cl <= 0) or (mode == "cd" and cl < clmin):
                    continue
                v = score(mode, cl, cd)
                key = (-v if mode == "ld" else v, r["naca"], a)
                if best is None or key < best[0]:
                    best = (key, r["naca"], a, v)
        if best is None:
            c["baseline"] = None                          # no NACA section satisfies the cell: a design must
            cells.append(c)
            continue
        _, code, a, v = best
        rel = f"collections/open-tables/refs/cells/{c['family']}/{c['id']}.naca.txt"
        os.makedirs(os.path.dirname(os.path.join(ROOT, rel)), exist_ok=True)
        with open(os.path.join(ROOT, rel), "w") as f:
            f.write(f"# {c['id']}: baseline, the best NACA 4- or 5-digit section of the scan (tools/airfoil_scan.py) "
                    f"at its best angle\n# QV-Foil 1 (a numerical model, not a wind tunnel)\nalpha {a}\nnaca {code}\n")
        got, out = check(c["checker_args"], os.path.join(ROOT, rel))
        if got != v:
            sys.exit(f"{c['id']}: the checker gives {got} for NACA {code} at {a}, the scan {v}\n{out}")
        c["baseline"] = {"naca": code, "alpha": a, "value": text(v), "decimal": decimal(v, mode), "certificate": rel}
        cells.append(c)
    return cells


def finish(cells):
    out = {"airfoil-ld": [], "airfoil-cd": []}
    for c in cells:
        mode = c["params"]["mode"]
        b = c["baseline"]
        if b:
            best_v, holder, how, cert, ours = Fraction(b["value"]), \
                f"NACA {b['naca']} (a published section, NACA Reports 460/610/824), scored by QV-Foil 1", \
                f"the best NACA 4- or 5-digit section at the best angle of a scan from -2 to 12 degrees " \
                f"(alpha {b['alpha']})", b["certificate"], False
        else:
            best_v = holder = how = cert = None
            ours = False
        rel = f"collections/open-tables/refs/cells/{c['family']}/{c['id']}.txt"
        c["entry"] = None
        if os.path.exists(os.path.join(ROOT, rel)):
            v, outp = check(c["checker_args"], os.path.join(ROOT, rel))
            if v is None:
                sys.exit(f"{rel}: refused by the checker\n{outp}")
            first = open(os.path.join(ROOT, rel)).readline().strip("# \n")
            if first.startswith(c["id"] + ": "):
                first = first[len(c["id"]) + 2:]
            c["entry"] = {"value": text(v), "decimal": decimal(v, mode), "certificate": rel, "how": first}
            if best_v is None or ((v > best_v) if mode == "ld" else (v < best_v)):
                best_v, holder, how, cert, ours = v, "Quantavane (Arhan Canli)", first, rel, True
        if best_v is None:
            print(f"{c['id']}: no NACA baseline and no design yet: left out")
            continue
        c.update(best=text(best_v), best_decimal=decimal(best_v, mode), first_entry=True, published=None,
                 holder=holder, how=how, quantavane=ours, certificate=cert, certificate_value=text(best_v),
                 status="first entry", date=DATE,
                 baseline_text=(f"Baseline: NACA {b['naca']} at alpha {b['alpha']}, {b['decimal']} (published shape, "
                                f"scored by this model)." if b else "Baseline: no NACA 4- or 5-digit section satisfies "
                                "this cell in the model."))
        out[c["family"]].append(c)
    for fam, cs in out.items():
        with open(os.path.join(HERE, "cells", fam + ".jsonl"), "w") as f:
            for c in cs:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(os.path.join(HERE, "refs", "cells", "airfoil-grid.jsonl"), "w") as f:   # every cell, for the search
        for c in cells:
            f.write(json.dumps({k: c[k] for k in ("id", "family", "params", "checker_args", "baseline")}) + "\n")
    print(f"{sum(len(v) for v in out.values())} cells; {sum(1 for c in cells if c.get('quantavane'))} with a design of "
          f"ours above the NACA baseline")


def main():
    if len(sys.argv) > 1:
        finish(baselines(sys.argv[1]))
    else:
        cells = [json.loads(l) for l in open(os.path.join(HERE, "refs", "cells", "airfoil-grid.jsonl")) if l.strip()]
        for c in cells:
            if not c["baseline"]:
                continue
            v, out = check(c["checker_args"], os.path.join(ROOT, c["baseline"]["certificate"]))
            if v is None or text(v) != c["baseline"]["value"]:
                sys.exit(f"{c['id']}: baseline certificate gives {v}, cell says {c['baseline']['value']}")
        finish(cells)
    return 0


if __name__ == "__main__":
    sys.exit(main())
