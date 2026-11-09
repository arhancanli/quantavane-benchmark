#!/usr/bin/env python3
"""Open Problems Benchmark (version in VERSION): open problems with exact checkers (Quantavane).

  python3 -I obb.py list [FAMILY]               the problems, their objective, the best known value and its source
                                                (without FAMILY: the single problems and a count of each family)
  python3 -I obb.py families                    the families: keeper, date read, checker, number of cells
  python3 -I obb.py show PROBLEM                one problem in full (a family cell is written out like a problem file)
  python3 -I obb.py sample FAMILY [N] [SEED]    N problems of a family drawn at random (default 10, seed 0)
  python3 -I obb.py check PROBLEM SUBMISSION    check a submission exactly and compare it with the best known values
  python3 -I obb.py verify RECORD.json          check a submission record (SUBMITTING.md) and print its leaderboard row
  python3 -I obb.py leaderboard [PROBLEM]       the verified results in leaderboard.json, best first
  python3 -I obb.py index                       check index.json against the files it lists (counts and SHA-256)

A problem is either a single problem, with its own file in problems/, or a cell of a family: one statement and one
checker in families/NAME/family.json, and one line per cell in families/NAME/cells.jsonl (its parameters, the best
known value read from the keeper's table and who holds it). index.json lists both, with counts and SHA-256. Every
problem has an exact checker in checkers/ (our own code, from the definitions on the source pages; standard library
only). A submission scores the exact value its checker proves; it "improves" a
problem when that value beats the best known one. Two reference values are kept apart: the best value on the
source page (with its source) and the best verified value still in review (for instance an open pull request whose
certificate has been replayed independently), so a result is never compared with a claim that nobody has checked."""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(HERE, "VERSION")).read().strip()


def problems():
    out = {}
    for f in sorted(os.listdir(os.path.join(HERE, "problems"))):
        if f.endswith(".json"):
            p = json.load(open(os.path.join(HERE, "problems", f)))
            out[p["id"]] = p
    return out


FAMILIES = os.path.join(HERE, "families")


def families():
    """Family definitions (families/NAME/family.json), by name."""
    out = {}
    if os.path.isdir(FAMILIES):
        for name in sorted(os.listdir(FAMILIES)):
            path = os.path.join(FAMILIES, name, "family.json")
            if os.path.exists(path):
                out[name] = json.load(open(path))
    return out


def cells(fam):
    """The cells of a family, one dict per line of families/NAME/cells.jsonl."""
    with open(os.path.join(FAMILIES, fam["family"], fam["cells"])) as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def fill(template, values):
    if isinstance(template, list):
        return [fill(t, values) for t in template]
    return template.format(**values)


def materialize(fam, cell):
    """The problem a family cell stands for, written out like a problem file."""
    values = dict(cell["params"])
    tpl = dict(fam["template"])
    tpl.update(fam.get("variants", {}).get(cell.get("variant", ""), {}))
    holder = cell.get("holder") or fam["holder_unknown"]
    ours = bool(cell.get("quantavane_record"))
    read = cell.get("read", fam["read"])
    title = fill(tpl["title"], values)
    values.update(best=cell["best"], holder=holder, title=title)
    best_known = {
        "value": cell["best"],
        "source": f"{fam['keeper']}, {title}: {cell['best']} ({holder}); read {read}",
        "kind": "table entry",
        "provenance": {"keeper": fam["keeper"], "url": fill(fam.get("cell_url") or fam["page"], values), "read": read,
                       "revision": fam["revision"], "holder": holder, "quantavane": ours},
    }
    if fam.get("exact_values", True):
        best_known["exact"] = cell["best"]
    p = {
        "id": cell["id"], "family": fam["family"], "title": title, "page": fam["page"],
        "statement": fill(tpl["statement"], values) + " " + fill(fam["best_text"], values),
        "objective": fam["objective"], "submission": fill(tpl["submission"], values),
        "checker": {"program": fam["checker"]["program"], "args": fill(tpl.get("args", fam["checker"].get("args", [])),
                                                                       values), "value": fam["checker"]["value"]},
        "best_known": best_known, "verified_pending": [], "score": fam["score"], "added": fam["added"],
    }
    if "bound" in cell:
        p["bound"] = {"value": cell["bound"], "kind": fam["bound_kind"], "source": fam["bound_source"]}
    if ours:
        p["quantavane_record"] = True
        p["quantavane_note"] = "our object is the best known entry of the source table"
    return p


def find_problem(pid):
    """A single problem (problems/PID.json) or a family cell, or None."""
    path = os.path.join(HERE, "problems", pid + ".json")
    if re.fullmatch(r"[A-Za-z0-9_.+-]+", pid) and os.path.exists(path):
        p = json.load(open(path))
        if p["id"] == pid:
            return p
    key = '{"id": "' + pid + '"'
    for fam in families().values():
        if not any(pid.startswith(x) for x in fam["id_prefixes"]):
            continue
        with open(os.path.join(FAMILIES, fam["family"], fam["cells"])) as f:
            for line in f:
                if line.startswith(key + ",") or line.startswith(key + "}"):
                    return materialize(fam, json.loads(line))
    return None


def exact(text):
    """A decimal string as an exact fraction."""
    return Fraction(text)


def native(program):
    """Build a C checker from checkers/PROGRAM.c into checkers/bin/ on first use."""
    exe = os.path.join(HERE, "checkers", "bin", program)
    src = os.path.join(HERE, "checkers", program + ".c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    return exe


def run_checker(p, path):
    """Run the problem's checker on a submission; return (exact value proved, the checker's output)."""
    c = p["checker"]
    args = [os.path.join(HERE, a) if a.startswith("instances/") else a for a in c["args"]]  # fetched by fetch.sh
    if c["value"] == "ramsey":                      # ramsey_check S T FILE: exit 0 = no red K_S and no blue K_T
        r = subprocess.run([native(c["program"])] + args + [path], capture_output=True, text=True)
        m = re.search(r"^n (\d+) red_K\d+ none blue_K\d+ none", r.stdout, re.M)
        return (Fraction(int(m.group(1))) if r.returncode == 0 and m else None), r.stdout + r.stderr
    if c["value"] == "spherical":                  # sph_check.py FILE D N: the file comes first
        cmd = [sys.executable, "-I", os.path.join(HERE, "checkers", c["program"]), path] + args
    else:
        cmd = [sys.executable, "-I", os.path.join(HERE, "checkers", c["program"])] + args + [path]
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
    if c["value"] == "spherical":                  # sph_check.py: "max_cos X" (largest cosine, 50-digit decimals)
        m = re.search(r"max_cos (-?\d+\.\d+)", text)
        return (Fraction(m.group(1)) if m else None), text
    if c["value"] == "blocks":                     # covering_check.py V K T M FILE: "blocks B" for a valid design
        m = re.search(r"^blocks (\d+)$", text, re.M)
        return (Fraction(int(m.group(1))) if m else None), text
    if c["value"] == "c42":                        # c42_check.py FILE: "RESULT C42 <= num/den: PASS"
        m = re.search(r"RESULT C42 <= (\d+)/(\d+): PASS", text)
        return (Fraction(int(m.group(1)), int(m.group(2))) if m else None), text
    if c["value"] == "c59":                        # c59_check.py FILE: "RESULT K_2 < R/E: PASS"
        m = re.search(r"RESULT K_2 < (\d+)/(\d+): PASS", text)
        return (Fraction(int(m.group(1)), int(m.group(2))) if m else None), text
    if c["value"] == "c16":                        # c16_lower.py FILE: "RESULT C16 >= X" (lower end of the enclosure)
        m = re.search(r"RESULT C16 >= (\d+\.\d+)", text)
        return (Fraction(m.group(1)) if m else None), text
    if c["value"] == "cvrp":                       # cvrp_check.py INSTANCE FILE: "cost C" for a valid solution
        m = re.search(r"^cost (\d+)$", text, re.M)
        return (Fraction(int(m.group(1))) if m else None), text
    if c["value"] == "words":                      # cw_check.py N D W FILE: "words M" for a valid code
        m = re.search(r"^words (\d+)$", text, re.M)
        return (Fraction(int(m.group(1))) if m else None), text
    if c["value"] == "result":                     # every checker added in v1.1: last line "RESULT v" (v integer or p/q)
        m = re.search(r"^RESULT (-?\d+)(?:/(\d+))?$", text, re.M)
        return (Fraction(int(m.group(1)), int(m.group(2) or 1)) if m else None), text
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


def cmd_list(family=None):
    probs = problems()
    fams = families()
    shown = 0
    for pid, p in probs.items():
        if family and p.get("family") != family:
            continue
        shown += 1
        vp = p.get("verified_pending") or []
        best_v = vp[0]["value"] if vp else "-"
        mark = "  [Quantavane record]" if p.get("quantavane_record") else ""
        print(f"{pid:22s} {p['objective']:8s} page {p['best_known']['value']:>22s}   verified in review {best_v}{mark}")
        print(f"{'':22s} {p['title']}")
    n_cells = 0
    if family in fams:
        fam = fams[family]
        for c in cells(fam):
            shown += 1
            mark = "  [Quantavane record]" if c.get("quantavane_record") else ""
            print(f"{c['id']:22s} {fam['objective']:8s} best {c['best']:>22s}   {(c.get('holder') or '')[:60]}{mark}")
    counts = {}
    for p in probs.values():
        counts[p.get("family", "?")] = counts.get(p.get("family", "?"), 0) + 1
    for name, fam in fams.items():
        counts[name] = counts.get(name, 0) + fam["count"]
        n_cells += fam["count"]
    total = len(probs) + n_cells
    print(f"\nOpen Problems Benchmark v{VERSION}: {shown} of {total} problems shown ({len(probs)} single problems, "
          f"{n_cells} family cells); by family: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    if not family and fams:
        print("A family's cells: python3 -I obb.py list FAMILY (families: " + ", ".join(fams) + ")")


def cmd_families():
    fams = families()
    for name, fam in fams.items():
        print(f"{name:22s} {fam['count']:>7d} cells  {fam['objective']:8s} checker {fam['checker']['program']}")
        print(f"{'':22s} {fam['keeper']}; read {fam['read']}; {fam.get('quantavane_records', 0)} held by Quantavane")
    print(f"{len(fams)} families, {sum(f['count'] for f in fams.values())} cells")
    return 0


def cmd_show(pid):
    p = find_problem(pid)
    if p is None:
        print(f"unknown problem {pid}")
        return 1
    print(json.dumps(p, indent=1, ensure_ascii=False))
    return 0


def cmd_sample(name, n=10, seed=0):
    import random
    fam = families().get(name)
    if fam is None:
        print(f"unknown family {name}")
        return 1
    ids = [c["id"] for c in cells(fam)]
    for pid in random.Random(seed).sample(ids, min(n, len(ids))):
        print(pid)
    return 0


def cmd_index():
    """Check index.json against the files: every listed file exists with the stated SHA-256 and count."""
    idx = json.load(open(os.path.join(HERE, "index.json")))
    bad = 0
    for shard in idx["shards"]:
        path = os.path.join(HERE, shard["path"])
        if shard["kind"] == "problems":
            n = len([f for f in os.listdir(path) if f.endswith(".json")])
            digest = None
        else:
            n = sum(1 for line in open(path) if line.strip())
            digest = sha256(path)
        ok = n == shard["count"] and (digest is None or digest == shard["sha256"])
        bad += not ok
        print(f"{'ok  ' if ok else 'BAD '} {shard['path']:45s} {n:>7d} {'(' + shard['family'] + ')' if 'family' in shard else ''}")
    print(f"{idx['problems']} problems in index.json (benchmark v{idx['benchmark_version']})")
    return 1 if bad else 0


def cmd_check(pid, path):
    p = find_problem(pid)
    if p is None:
        print(f"unknown problem {pid}")
        return 1
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


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


RECORD_FIELDS = ("problem", "certificate", "sha256", "submitter", "source", "ai_assistance", "date")


def cmd_verify(record_path):
    """Check a submission record (SUBMITTING.md) and print the leaderboard row it earns."""
    rec = json.load(open(record_path))
    missing = [k for k in RECORD_FIELDS if not str(rec.get(k, "")).strip()]
    if missing:
        print("the record lacks: " + ", ".join(missing))
        return 1
    p = find_problem(rec["problem"])
    if p is None:
        print(f"unknown problem {rec['problem']}")
        return 1
    cert = os.path.join(os.path.dirname(os.path.abspath(record_path)), rec["certificate"])
    digest = sha256(cert)
    if digest != rec["sha256"].lower():
        print(f"the certificate's SHA-256 is {digest}, not {rec['sha256']}")
        return 1
    value, text = run_checker(p, cert)
    if value is None:
        print(f"{p['id']}: NOT CERTIFIED (the checker did not prove a value)")
        print(text[-2000:])
        return 1
    page = threshold(p, p["best_known"])
    row = {
        "problem": p["id"], "value": str(value.numerator) if value.denominator == 1 else
        f"{value.numerator}/{value.denominator}", "submitter": rec["submitter"], "source": rec["source"],
        "ai_assistance": rec["ai_assistance"], "certificate_sha256": digest, "submitted": rec["date"],
        "verified": datetime.date.today().isoformat(), "benchmark_version": VERSION,
        "checker": p["checker"]["program"],
        "improves_page_best": better(p, value, page),
        "page_best_then": p["best_known"]["value"],
    }
    print(json.dumps(row, indent=1, ensure_ascii=False))
    return 0


def cmd_leaderboard(pid=None):
    board = json.load(open(os.path.join(HERE, "leaderboard.json")))
    probs = problems()
    rows = [r for r in board["entries"] if pid is None or r["problem"] == pid]

    def key(r):
        p = probs.get(r["problem"]) or find_problem(r["problem"])
        v = Fraction(r["value"])
        return (r["problem"], -v if p and p["objective"] == "maximize" else v)
    for r in sorted(rows, key=key):
        flag = "above the page (in review)" if r.get("improves_page_best") else "record" if r.get("equals_page_best") else ""
        print(f"{r['problem']:22s} {r['value']:>12s}  {r['submitter'][:40]:40s} {r['verified']}  {flag}")
    print(f"{len(rows)} verified entries (leaderboard.json, benchmark v{board['benchmark_version']})")
    return 0


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "list":
        cmd_list(sys.argv[2] if len(sys.argv) > 2 else None)
        return 0
    if len(sys.argv) == 4 and sys.argv[1] == "check":
        return cmd_check(sys.argv[2], sys.argv[3])
    if len(sys.argv) == 3 and sys.argv[1] == "verify":
        return cmd_verify(sys.argv[2])
    if len(sys.argv) in (2, 3) and sys.argv[1] == "leaderboard":
        return cmd_leaderboard(sys.argv[2] if len(sys.argv) == 3 else None)
    if len(sys.argv) == 2 and sys.argv[1] == "families":
        return cmd_families()
    if len(sys.argv) == 3 and sys.argv[1] == "show":
        return cmd_show(sys.argv[2])
    if 3 <= len(sys.argv) <= 5 and sys.argv[1] == "sample":
        return cmd_sample(sys.argv[2], *(int(x) for x in sys.argv[3:]))
    if len(sys.argv) == 2 and sys.argv[1] == "index":
        return cmd_index()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
