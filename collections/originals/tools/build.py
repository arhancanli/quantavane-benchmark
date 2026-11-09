"""Writes the Quantavane Originals pages from the problem files (standard library only).

  python3 -I tools/build.py          (run from collections/originals)

Reads problems/*.json (one file per problem: statement, context, novelty check, checker, first values, best known
value) and writes problems/ID.md for each problem, index.json and the table in README.md (between the markers
<!--table--> and <!--/table-->). The JSON files are the source; the pages are generated from them."""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIELDS = ["Combinatorics and graph theory", "Number theory", "Coding theory", "Discrete geometry", "Physics",
          "Chemistry and materials", "Astronomy", "Computing and operations research", "Biology"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def day(iso):
    y, m, d = (int(x) for x in iso[:10].split("-"))
    return f"{d} {MONTHS[m - 1]} {y}"


def load():
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, "problems", "*.json"))):
        out.append(json.load(open(f)))
    out.sort(key=lambda p: (FIELDS.index(p["field"]), p["id"]))
    return out


def novelty_md(p):
    nv = p["novelty"]
    rec = json.load(open(os.path.join(HERE, nv["file"])))
    lines = [f"Checked {day(nv['checked'])}, before the problem was added. Every search below is in "
             f"[`{nv['file']}`](../{nv['file']}) with its address, the time it ran and its first results.", ""]
    ax = [s for s in rec["searches"] if s["engine"] == "arXiv API"]
    oe = [s for s in rec["searches"] if s["engine"] == "OEIS"]
    if ax:
        lines.append(f"- arXiv API, {len(ax)} searches:")
        for s in ax:
            lines.append(f"  - `{s['query']}`: {s['results']} result{'s' if s['results'] != 1 else ''}")
    if oe:
        lines.append(f"- OEIS, {len(oe)} searches:")
        for s in oe:
            hits = ", ".join(h["oeis"] for h in s["top"][:5])
            lines.append(f"  - `{s['query']}`: {s['results']} result{'s' if s['results'] != 1 else ''}"
                         + (f" ({hits})" if hits else ""))
    for w in rec.get("web", []):
        lines.append(f"- Web search ({w['engine']}), `{w['query']}`: {w['found']}")
    lines.append(f"- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): "
                 f"{nv.get('benchmark', 'no entry for this quantity')}.")
    if nv.get("closest"):
        lines += ["", "Closest work found, and how this problem differs:"]
        lines += [f"- {c}" for c in nv["closest"]]
    lines += ["", f"Verdict: {nv['verdict']}"]
    return "\n".join(lines)


def table_md(fv):
    cols = fv["columns"]
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for r in fv["rows"]:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    if fv.get("note"):
        out += ["", fv["note"]]
    return "\n".join(out)


def page(p):
    bk = p["best_known"]
    c = p["checker"]
    prog = c["program"].split("/")[-1]
    parts = [f"# {p['title']}", "",
             f"`{p['id']}` · {p['field']} · status: **{p['status']}** · added {day(p['baseline']['date'])} "
             f"(Quantavane Originals)", "",
             f"Best known value: **{bk['value']}** ({p['objective']}), {bk['source']}", "",
             "## Statement", "", p["statement"], "",
             "## Why it is interesting", "", p["context"], "",
             "## Novelty check", "", novelty_md(p), ""]
    if p.get("first_values"):
        parts += ["## First values", "", table_md(p["first_values"]), ""]
    parts += ["## Best known value", "", p["baseline"]["text"], ""]
    if p.get("bound"):
        parts += [f"Bound on the other side: {p['bound']['value']} ({p['bound']['kind']}; {p['bound']['source']}).", ""]
    parts += ["## Submitting and checking", "", f"Format: {p['submission']}", "",
              f"Score: {p['score']}. A submission improves the problem when its exact value is "
              f"{'smaller' if p['objective'] == 'minimize' else 'larger'} than the best known value.", "",
              "    python3 -I obb.py check " + p["id"] + " FILE               # from the benchmark's root",
              "    python3 -I collections/originals/checkers/" + prog + " " + " ".join(c["args"]) + " FILE", "",
              f"The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` "
              f"and exits 0 only for a valid certificate. Our certificate: `{bk['provenance']['certificate']}`.", ""]
    if p.get("references"):
        parts += ["## References", ""] + [f"- {r}" for r in p["references"]] + [""]
    return "\n".join(parts)


def main():
    probs = load()
    for p in probs:
        with open(os.path.join(HERE, "problems", p["id"] + ".md"), "w") as f:
            f.write(page(p))
    by = {fld: [p for p in probs if p["field"] == fld] for fld in FIELDS}
    idx = {"collection": "Quantavane Originals", "problems": len(probs),
           "by_field": {k: len(v) for k, v in by.items() if v},
           "items": [{"id": p["id"], "field": p["field"], "title": p["title"], "status": p["status"],
                      "objective": p["objective"], "best_known": p["best_known"]["value"],
                      "holder": p["best_known"]["provenance"]["holder"], "date": p["baseline"]["date"],
                      "checker": p["checker"]["program"], "page": f"problems/{p['id']}.md"} for p in probs]}
    with open(os.path.join(HERE, "index.json"), "w") as f:
        json.dump(idx, f, indent=1, ensure_ascii=False)
        f.write("\n")
    rows = ["| Problem | Field | Objective | Best known (ours, " + day(probs[0]["baseline"]["date"]) + ") |",
            "| --- | --- | --- | --- |"] if probs else []
    for p in probs:
        rows.append(f"| [{p['title']}](problems/{p['id']}.md) | {p['field']} | {p['objective']} | "
                    f"{p['best_known']['value']} |")
    readme = os.path.join(HERE, "README.md")
    text = open(readme).read()
    text = re.sub(r"<!--table-->.*?<!--/table-->", "<!--table-->\n" + "\n".join(rows) + "\n<!--/table-->", text,
                  flags=re.S)
    text = re.sub(r"<!--count-->.*?<!--/count-->", f"<!--count-->{len(probs)}<!--/count-->", text)
    with open(readme, "w") as f:
        f.write(text)
    print(f"{len(probs)} problems: " + ", ".join(f"{k} {len(v)}" for k, v in by.items() if v))


if __name__ == "__main__":
    main()
