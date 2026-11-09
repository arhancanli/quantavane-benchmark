"""Build the Quantavane Prestige 100 collection from its curated source (standard library only).

  python3 -I tools/build_prestige100.py          write collections/prestige100/{index.json, leaderboard.json, README.md,
                                                  problems/NN-ID.md} from curation.json and the problem files
  python3 -I tools/build_prestige100.py --check  check the collection without writing: exactly 100 problems, each with a
                                                  problem file, a checker, a credited holder and a keeper read on a
                                                  stated date, and every record consistent with its problem file

curation.json holds what the problem files do not: the short name, the record as a statement, its holders, the bound
on the other side, the history of the record with sources, why the problem matters, the keeper and when it was read,
whether Quantavane holds the record, and the record certificates we replayed (with their SHA-256). The statement,
objective, checker, certificate format and best known value in score units come from problems/ID.json, so the
collection and the benchmark cannot disagree. Leaderboard rows come from the replays in curation.json and from the
benchmark's leaderboard.json."""
import json
import os
import re
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COL = os.path.join(ROOT, "collections", "prestige100")
REPO = "https://github.com/arhancanli/quantavane-benchmark"

# record value (as printed in the curated statement) minus the best known value of the problem file, per family
OFFSET = {"ramsey": 1, "multicolour-ramsey": 1, "van-der-waerden": 1}


def load():
    cur = json.load(open(os.path.join(COL, "curation.json"), encoding="utf-8"))
    probs = {}
    for p in cur["problems"]:
        path = os.path.join(ROOT, "problems", p["id"] + ".json")
        probs[p["id"]] = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None
    board = json.load(open(os.path.join(ROOT, "leaderboard.json"), encoding="utf-8"))
    return cur, probs, board


def first_number(text):
    m = re.search(r"(\d[\d,]*(?:\.\d+)?)", text.replace("≥", " ").replace("≤", " "))
    return m.group(1).replace(",", "") if m else None


def record_number(text):
    """The number a record states: the one after its sign when it has one ("R(5,5) ≥ 43", "rank ≤ 23"), else the first."""
    t = text.split(" on the ")[0]
    for sign in ("≥", "≤"):
        if sign in t:
            t = t.split(sign, 1)[1]
            break
    return first_number(t)


def check(cur, probs):
    errors = []
    ps = cur["problems"]
    if len(ps) != 100:
        errors.append(f"{len(ps)} problems, not 100")
    if len({p["id"] for p in ps}) != len(ps):
        errors.append("repeated problem ids")
    if [p["slot"] for p in ps] != list(range(1, len(ps) + 1)):
        errors.append("slots are not 1..100 in order")
    for p in ps:
        q = probs[p["id"]]
        tag = f"{p['slot']:3d} {p['id']}"
        if q is None:
            errors.append(f"{tag}: no problem file")
            continue
        prog = q["checker"]["program"]
        if not (os.path.exists(os.path.join(ROOT, "checkers", prog)) or os.path.exists(os.path.join(ROOT, "checkers", prog + ".c"))):
            errors.append(f"{tag}: checker {prog} missing")
        for field in ("name", "record", "holders", "keeper", "history", "why", "why_sources", "to_beat"):
            if not p.get(field):
                errors.append(f"{tag}: no {field}")
        if not re.fullmatch(r"2026-11-09.*", p["keeper"].get("read", "")):
            errors.append(f"{tag}: keeper not read on 9 Nov 2026")
        if p["why"].count(". ") + p["why"].count(".\"") < 1:
            errors.append(f"{tag}: 'why' should be two sentences")
        best = q["best_known"]["value"]
        if p["record"] == "none known" or p["record"].startswith("no counterexample"):
            if best != "0":
                errors.append(f"{tag}: record says none known but the problem file has {best}")
            continue
        rec = record_number(p["record"])
        if rec is None:
            errors.append(f"{tag}: cannot read a number from the record {p['record']!r}")
            continue
        off = OFFSET.get(q["family"], 0)
        try:
            if Fraction(rec) != Fraction(best) + off:
                errors.append(f"{tag}: record {p['record']!r} vs problem file {best} (offset {off})")
        except ValueError:
            errors.append(f"{tag}: unreadable values {rec!r} / {best!r}")
        for r in p.get("replays", []):
            path = os.path.join(ROOT, r["certificate"])
            if not r.get("sha256") or not r.get("value"):
                errors.append(f"{tag}: replay without sha256 or value")
    return errors


def standing(q, value):
    best = Fraction(q["best_known"].get("exact") or q["best_known"]["value"])
    v = Fraction(value)
    if v == best:
        return "record"
    better = v < best if q["objective"] == "minimize" else v > best
    return "above the listed record (in review)" if better else "below the record"


def leaderboard(cur, probs, board):
    out = []
    for p in cur["problems"]:
        q = probs[p["id"]]
        rows = []
        for r in p.get("replays", []):
            rows.append({"value": r["value"], "holder": r["holder"], "certificate": r["certificate"], "source": r["source"],
                         "sha256": r["sha256"], "verified": r["verified"], "checker": q["checker"]["program"],
                         "standing": standing(q, r["value"])})
        seen = {r["sha256"] for r in rows}
        for e in board["entries"]:
            if e["problem"] == p["id"] and e.get("certificate_sha256") not in seen:
                rows.append({"value": e["value"], "holder": e["submitter"], "certificate": e.get("certificate", ""),
                             "source": "benchmark leaderboard.json", "sha256": e.get("certificate_sha256", ""),
                             "verified": e["verified"], "checker": e.get("checker", q["checker"]["program"]),
                             "standing": standing(q, e["value"])})
        rows.sort(key=lambda r: Fraction(r["value"]), reverse=q["objective"] == "maximize")
        out.append({"slot": p["slot"], "id": p["id"], "name": p["name"], "objective": q["objective"], "score": q["score"],
                    "record": {"statement": p["record"], "value": q["best_known"]["value"], "holders": p["holders"],
                               "listed_by": p["keeper"]["name"], "read": p["keeper"]["read"]},
                    "quantavane_record": bool(p.get("ours") and p["ours"].get("holds_record")),
                    "entries": rows})
    return {"collection": "prestige100", "version": cur["version"], "date": cur["date"],
            "about": ("For each problem, the record as its keeper lists it, and the certificates we have checked with the problem's checker. "
                      "standing: record = equals the listed record; above the listed record (in review) = better than the keeper lists, "
                      "verified by us and waiting for the keeper; below the record = valid but weaker. A record with no entry is listed by "
                      "its keeper but its certificate has not been replayed here yet."),
            "problems": out}


def command(q, file="CERTIFICATE"):
    c = q["checker"]
    prog = c["program"]
    args = " ".join(c["args"])
    if prog.endswith(".py"):
        own = f"python3 -I checkers/{prog} {args} {file}" if c["value"] != "spherical" else f"python3 -I checkers/{prog} {file} {args}"
    else:
        own = f"cc -O3 -o ramsey_check checkers/{prog}.c && ./ramsey_check {args} {file}"
    return own.replace("  ", " ")


def fmt_date(d):
    return d or "undated"


def page(p, q, lb):
    L = []
    L.append(f"# {p['slot']:02d}. {p['headline']}")
    L.append("")
    L.append(f"Family: {p['family']}. Benchmark problem: `{p['id']}`.")
    L.append("")
    L.append(f"**Best known:** {p['record']}, {p['holders']}." + (f" Also known: {p['other_bound']}." if p.get("other_bound") else ""))
    L.append("")
    L.append(f"**To beat it:** {p['to_beat']}.")
    L.append("")
    k = p["keeper"]
    L.append(f"**Keeper:** [{k['name']}]({k['url']}), read {k['read']} ({k['version']})."
             + "".join(f" Also read: [{a['name']}]({a['url']}), {a['read']} ({a['version']})." for a in p.get("also_read", [])))
    L.append("")
    if p.get("ours"):
        L.append(("**Quantavane holds this record.** " if p["ours"].get("holds_record") else "**Quantavane value in review.** ") + p["ours"]["note"])
        L.append("")
    L.append("## The problem")
    L.append("")
    L.append(q["statement"])
    L.append("")
    L.append("## Why it matters")
    L.append("")
    L.append(p["why"])
    L.append("")
    L.append("Sources: " + "; ".join(f"[{s['label']}]({s['url']})" if s.get("url") else s["label"] for s in p["why_sources"]) + ".")
    L.append("")
    L.append("## History")
    L.append("")
    L.append("As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.")
    L.append("")
    L.append("| Date | Bound | Value | By | Source |")
    L.append("| --- | --- | --- | --- | --- |")
    for h in p["history"]:
        src = h["source"] + (f" (via {h['via']})" if h.get("via") else "")
        L.append(f"| {fmt_date(h['date'])} | {h['bound'] or '-'} | {h['value'] or '-'} | {h['by']} | {src.replace('|', '/')} |")
    L.append("")
    L.append("## Check a certificate")
    L.append("")
    L.append(f"Certificate format: {q['submission']}")
    L.append("")
    L.append(f"Score: {q['score']}.")
    L.append("")
    L.append("```")
    L.append(f"python3 -I obb.py check {p['id']} CERTIFICATE        # the checker, and the comparison with the best known value")
    L.append(command(q) + "        # the checker on its own")
    L.append("```")
    L.append("")
    L.append("To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).")
    L.append("")
    L.append("## Leaderboard")
    L.append("")
    if lb["entries"]:
        L.append("| Value | Holder | Standing | Verified | Certificate (SHA-256) |")
        L.append("| --- | --- | --- | --- | --- |")
        for e in lb["entries"]:
            L.append(f"| {e['value']} | {e['holder']} | {e['standing']} | {e['verified']} | {e['certificate']} ({e['sha256'][:12]}...) |")
    else:
        L.append("No certificate has been checked here yet; the record above is as its keeper lists it.")
    L.append("")
    return "\n".join(L)


def readme(cur, probs):
    ps = cur["problems"]
    ours = [p for p in ps if p.get("ours") and p["ours"].get("holds_record")]
    fams = []
    for p in ps:
        if p["family"] not in fams:
            fams.append(p["family"])
    L = []
    L.append("# Quantavane Prestige 100")
    L.append("")
    L.append("One hundred famous open problems in which a single object, checked exactly by a program, settles the score: a better "
             "Ramsey colouring, a Hadamard matrix of order 668, a Costas array of order 32, a 3 × 3 matrix multiplication with 22 "
             "multiplications, a shorter Mona Lisa tour. Each problem has its statement, why it matters, the best known value with "
             "its holders and history as recorded by the table that keeps it, the checker, the certificate format and a leaderboard.")
    L.append("")
    L.append(f"Version {cur['version']}, {cur['date']}. Every keeper was read on 9 November 2026; the date and time of each "
             "reading are on the problem's page. Values change when the keepers' tables change: check the keeper before "
             "claiming a record.")
    L.append("")
    L.append("Choice. Fame first, then checkability: each problem has an exact checker in this benchmark and a certificate small "
             "enough to send. The list covers the smallest open Ramsey numbers and the diagonal ones, multicolour Ramsey numbers, "
             "Schur, weak Schur and van der Waerden numbers, the kissing numbers in every open dimension from 5 to 31, the "
             "smallest open cases of matrix multiplication, Hadamard matrices, Moore and strongly regular graphs, projective planes, "
             "Latin squares and Costas arrays, cages and the degree-diameter problem, sorting networks, Golomb rulers, cap sets, "
             "snake-in-the-box and superpermutations, two falsifiable Erdős problems, two optimization constants, the no-three-in-line "
             f"problem and the Mona Lisa TSP. Quantavane holds the best known value in {len(ours)} of them, marked below: R(5,15), R(8,12) and "
             "WS(7) to WS(9) are in Leaps in Bounds' records, and R(3,18) and R(4,18) are published with a checker for the survey's "
             "next revision. They are in the list because they are cells of the famous tables, not the other way round.")
    L.append("")
    L.append("Submitting: run `python3 -I obb.py check ID CERTIFICATE`, then send the certificate and a short record as in "
             "[SUBMITTING.md](../../SUBMITTING.md) (open an issue or write to arhan@quantavane.com). We rerun the check, add the "
             "result to `leaderboard.json` with your name or handle, and help you send it to the keeper of the table, who "
             "decides the listing. Machine-readable: `index.json` (everything) and `leaderboard.json`.")
    L.append("")
    for fam in fams:
        L.append(f"## {fam}")
        L.append("")
        L.append("| # | Problem | Best known | Holder | Checker |")
        L.append("| --- | --- | --- | --- | --- |")
        for p in ps:
            if p["family"] != fam:
                continue
            q = probs[p["id"]]
            mark = " (Quantavane)" if p.get("ours") and p["ours"].get("holds_record") else ""
            L.append(f"| {p['slot']} | [{p['name']}](problems/{p['slot']:02d}-{p['id']}.md) | {p['record']}{mark} | {p['holders']} | `{q['checker']['program']}` |")
        L.append("")
    L.append("## The keepers")
    L.append("")
    L.append("The records belong to the people who found them, and the tables to the people who keep them. This collection "
             "only gathers them, with credit:")
    L.append("")
    seen = set()
    for p in ps:
        for k in [p["keeper"]] + p.get("also_read", []):
            if k["name"] not in seen:
                seen.add(k["name"])
                L.append(f"- [{k['name']}]({k['url']}), read {k['read']}.")
    L.append("")
    L.append("Checkers are Quantavane's own code (MIT); the statements and data credit their sources. Corrections are welcome: open an issue.")
    L.append("")
    return "\n".join(L)


def main():
    cur, probs, board = load()
    errors = check(cur, probs)
    for e in errors:
        print("ERROR", e)
    if errors:
        return 1
    if "--check" in sys.argv:
        print(f"ok: {len(cur['problems'])} problems, every one with a problem file, a checker, a holder and a keeper read on 9 Nov 2026")
        return 0
    lb = leaderboard(cur, probs, board)
    by_slot = {x["slot"]: x for x in lb["problems"]}
    os.makedirs(os.path.join(COL, "problems"), exist_ok=True)
    index = {"collection": "prestige100", "title": cur["title"], "version": cur["version"], "date": cur["date"],
             "source": f"{REPO}/tree/main/collections/prestige100", "license": "data CC BY 4.0, checkers MIT", "problems": []}
    for p in cur["problems"]:
        q = probs[p["id"]]
        path = os.path.join(COL, "problems", f"{p['slot']:02d}-{p['id']}.md")
        open(path, "w", encoding="utf-8").write(page(p, q, by_slot[p["slot"]]))
        entry = {k: p[k] for k in ("slot", "id", "family", "name", "headline", "flagship", "record", "holders", "other_bound",
                                   "to_beat", "keeper", "also_read", "history", "why", "why_sources")}
        entry.update({"statement": q["statement"], "objective": q["objective"], "certificate_format": q["submission"], "score": q["score"],
                      "best_known_value": q["best_known"]["value"], "checker": q["checker"], "check_command": command(q),
                      "quantavane": p.get("ours"), "leaderboard_entries": len(by_slot[p["slot"]]["entries"]),
                      "page": f"problems/{p['slot']:02d}-{p['id']}.md"})
        index["problems"].append(entry)
    json.dump(index, open(os.path.join(COL, "index.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(lb, open(os.path.join(COL, "leaderboard.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(COL, "README.md"), "w", encoding="utf-8").write(readme(cur, probs))
    n_entries = sum(len(x["entries"]) for x in lb["problems"])
    print(f"wrote {len(index['problems'])} problem pages, index.json, leaderboard.json ({n_entries} verified entries), README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
