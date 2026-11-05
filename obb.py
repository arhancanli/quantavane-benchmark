#!/usr/bin/env python3
"""Open Problems Benchmark v0: open problems with exact checkers (private draft, Quantavane).

  python3 -I obb.py list                        the problems, their objective, the best known value and its source
  python3 -I obb.py check PROBLEM SUBMISSION    check a submission exactly and compare it with the best known values

Every problem has a file in problems/ and an exact checker in checkers/ (our own code, from the definitions on the
constant pages; standard library only). A submission scores the exact value its checker proves; it "improves" a
problem when that value beats the best known one. Two reference values are kept apart: the best value on the
constant page (the repository's main branch, with its source) and the best verified value still in review (an open
pull request whose certificate has been replayed independently), so a result is never compared with a claim that
nobody has checked."""
import json
import os
import re
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def problems():
    out = {}
    for f in sorted(os.listdir(os.path.join(HERE, "problems"))):
        if f.endswith(".json"):
            p = json.load(open(os.path.join(HERE, "problems", f)))
            out[p["id"]] = p
    return out


def exact(text):
    """A decimal string as an exact fraction."""
    return Fraction(text)


def run_checker(p, path):
    """Run the problem's checker on a submission; return (exact value proved, the checker's output)."""
    c = p["checker"]
    cmd = [sys.executable, "-I", os.path.join(HERE, "checkers", c["program"])] + c["args"] + [path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    text = r.stdout + r.stderr
    if r.returncode != 0:
        return None, text
    if c["value"] == "bound":                       # autocorr_check.py: "bound = num/den"
        m = re.search(r"bound = (\d+)/(\d+)", text)
        return (Fraction(int(m.group(1)), int(m.group(2))) if m else None), text
    if c["value"] == "c68":                         # c68_check.py: "RESULT C68 >= p/q = ...: all hypotheses hold"
        m = re.search(r"RESULT C68 >= (\d+)/(\d+) = \S+: all hypotheses hold", text)
        return (Fraction(int(m.group(1)), int(m.group(2))) if m else None), text
    raise ValueError("unknown value kind " + c["value"])


def threshold(p, entry):
    """The value a submission must beat: the exact value when known; otherwise the printed value moved by one unit in
    its last printed decimal, so that a value equal to the unrounded original never counts as an improvement."""
    if entry.get("exact"):
        return Fraction(entry["exact"])
    v = entry["value"]
    unit = Fraction(1, 10 ** len(v.split(".")[1])) if "." in v else Fraction(1)
    return Fraction(v) - unit if p["objective"] == "minimize" else Fraction(v) + unit


def better(p, a, b):
    return a < b if p["objective"] == "minimize" else a > b


def cmd_list():
    for pid, p in problems().items():
        vp = p.get("verified_pending") or []
        best_v = vp[0]["value"] if vp else "-"
        print(f"{pid:10s} {p['objective']:8s} page {p['best_known']['value']:>22s}   verified in review {best_v}")
        print(f"{'':10s} {p['title']}")


def cmd_check(pid, path):
    p = problems()[pid]
    value, text = run_checker(p, path)
    if value is None:
        print(f"{pid}: NOT CERTIFIED (the checker did not prove a value)")
        print(text[-2000:])
        return 1
    page = threshold(p, p["best_known"])
    print(f"{pid}: certified value {value.numerator}/{value.denominator}")
    print(f"  = {float(value):.15f}... ({p['objective']})")
    print(f"  page best {p['best_known']['value']} ({p['best_known']['source']}): "
          f"{'IMPROVES' if better(p, value, page) else 'does not improve'}")
    for v in p.get("verified_pending") or []:
        print(f"  verified in review {v['value']} ({v['source']}): "
              f"{'IMPROVES' if better(p, value, threshold(p, v)) else 'does not improve'}")
    return 0


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "list":
        cmd_list()
        return 0
    if len(sys.argv) == 4 and sys.argv[1] == "check":
        return cmd_check(sys.argv[2], sys.argv[3])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
