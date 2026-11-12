#!/usr/bin/env python3
"""Builds the pages, the index and the README table of the Quantavane Open Tables from the problem files and the
cells (standard library only).

  python3 -I tools/build.py            write problems/ID.json (best_known from the headline cell), problems/ID.md,
                                       index.json and the table in README.md
  python3 -I tools/build.py --check    exit 1 if any of these files is not what the build would write"""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ("unknotting", "airfoil-ld", "airfoil-cd")


def load_cells(pid):
    path = os.path.join(HERE, "cells", pid + ".jsonl")
    return [json.loads(l) for l in open(path) if l.strip()] if os.path.exists(path) else []


def headline(p, cells):
    want = {k: str(v) for k, v in p["cells"]["headline"].items()}
    for c in cells:
        if all(str(c["params"].get(k)) == v for k, v in want.items()):
            return c
    raise SystemExit(f"{p['id']}: no headline cell {want}")


def best_known(p, c):
    pub = c.get("published")
    if pub:
        return {"value": c["best"], "exact": c["best"], "source": pub["source"], "kind": "published value",
                "provenance": {"keeper": "Quantavane Open Tables (no keeper for this field)", "url": p["page"],
                               "read": c["date"], "holder": pub["holder"], "quantavane": False,
                               "certificate": c.get("certificate")}}
    return {"value": c["best"], "exact": c["best"], "source": f"{c['holder']}, {c['date']}: {c.get('how', '')}",
            "kind": "first entry (no published value)",
            "provenance": {"keeper": "Quantavane Open Tables (no keeper for this field)", "url": p["page"],
                           "read": c["date"], "holder": c["holder"], "quantavane": bool(c.get("quantavane")),
                           "certificate": c.get("certificate")}}


def fmt_params(p, c):
    if p["id"] == "unknotting":
        return f"{c['params']['knot']}"
    keys = [k for k in p["cells"]["params"] if k not in ("mode",)]
    return ", ".join(f"{k} {c['params'][k]}" for k in keys if k in c["params"] and not (k == "clmin" and
                                                                                       p["id"] == "airfoil-ld"))


def page(p, cells):
    bk = p["best_known"]
    head = headline(p, cells) if cells else {}
    shown = head.get("best_decimal", bk["value"])
    L = [f"# {p['title']}", "",
         f"`{p['id']}` · {p['field']} · status: **{p['status']}** · added 12 November 2026 (Quantavane Open Tables)", "",
         f"Headline cell `{head.get('id', p['id'])}`: **{shown}** ({p['objective']}), {bk['kind']}: {bk['source']}", "",
         "## Statement", "", p["statement"], "", "## Why it is interesting", "", p["context"], ""]
    n_pub = sum(1 for c in cells if c.get("published"))
    n_cert = sum(1 for c in cells if c.get("certificate"))
    L += ["## Cells", "",
          f"{len(cells)} cells: {n_pub} with a published best value, {len(cells) - n_pub} first entries (no published "
          f"value); {n_cert} with a certificate here that the checker replays.", ""]
    if p["id"] == "unknotting":
        L += ["| Cell | Knot | Upper bound (best known) | Lower bound | Our certificate | Source |",
              "| --- | --- | ---: | ---: | --- | --- |"]
        for c in cells:
            cert = (f"[{c['certificate_value']} changes](../refs/cells/unknotting/{c['params']['knot']}.txt)"
                    if c.get("certificate") else "none yet")
            L.append(f"| `{c['id']}` | {c['params']['knot']} | {c['best']} | {c['bound']} | {cert} | KnotInfo |")
    else:
        L += ["| Cell | Parameters | Best | Holder | NACA baseline (published shape, our evaluation) |",
              "| --- | --- | ---: | --- | --- |"]
        for c in cells:
            b = c.get("baseline") or {}
            base = f"{b.get('decimal', '-')} (NACA {b.get('naca', '-')}, alpha {b.get('alpha', '-')})" if b else "none"
            L.append(f"| `{c['id']}` | {fmt_params(p, c)} | {c.get('best_decimal', c['best'])} | {c['holder']} | {base} |")
    L += [""]
    if p.get("sources"):
        L += ["## Sources and licences", ""]
        for s in p["sources"]:
            L += [f"- {s['what']}: `{s['file']}`, fetched by `fetch.sh` from {s['url']} (SHA-256 `{s['sha256']}`). "
                  f"{s['licence']}"]
        L += [""]
    L += ["## References", ""] + [f"- {r}" for r in p["references"]] + [""]
    L += ["## Submitting and checking", "", f"Format: {p['submission']}", "", "```sh",
          f"python3 -I obb.py show {cells[0]['id'] if cells else p['id']}",
          f"python3 -I obb.py check {cells[0]['id'] if cells else p['id']} my_submission.txt",
          f"python3 -I {p['checker']['program']} {' '.join(p['checker']['args'])} my_submission.txt", "```", ""]
    return "\n".join(L)


def build():
    out = {}
    items, totals = [], {"cells": 0, "published": 0, "first": 0, "certified": 0}
    for pid in ORDER:
        path = os.path.join(HERE, "problems", pid + ".json")
        p = json.load(open(path))
        cells = load_cells(pid)
        if cells:
            p["best_known"] = best_known(p, headline(p, cells))
        out[path] = json.dumps(p, indent=1, ensure_ascii=False) + "\n"
        out[os.path.join(HERE, "problems", pid + ".md")] = page(p, cells)
        n_pub = sum(1 for c in cells if c.get("published"))
        n_cert = sum(1 for c in cells if c.get("certificate"))
        totals["cells"] += len(cells)
        totals["published"] += n_pub
        totals["first"] += len(cells) - n_pub
        totals["certified"] += n_cert
        items.append({"id": pid, "field": p["field"], "title": p["title"], "objective": p["objective"],
                      "cells": len(cells), "cells_published": n_pub, "cells_first_entry": len(cells) - n_pub,
                      "cells_certified_here": n_cert, "checker": p["checker"]["program"], "page": f"problems/{pid}.md"})
    index = {"collection": "Quantavane Open Tables", "version": "open-tables-1", "date": "2026-11-12",
             "counting": "tables: one per problem file; cells: one per instance (cells/ID.jsonl). A cell's best value is a "
                         "published one (with its source) or, where nothing is published, a first entry, counted apart.",
             "tables": len(items), "cells": totals["cells"], "cells_published": totals["published"],
             "cells_first_entry": totals["first"], "cells_certified_here": totals["certified"], "items": items}
    out[os.path.join(HERE, "index.json")] = json.dumps(index, indent=1, ensure_ascii=False) + "\n"
    readme_path = os.path.join(HERE, "README.md")
    if os.path.exists(readme_path):
        text = open(readme_path).read()
        rows = ["| Table | Field | Objective | Cells | Published values | First entries | Certified here |",
                "| --- | --- | --- | ---: | ---: | ---: | ---: |"]
        for it in items:
            rows.append(f"| [{it['title']}]({it['page']}) | {it['field']} | {it['objective']} | {it['cells']} | "
                        f"{it['cells_published']} | {it['cells_first_entry']} | {it['cells_certified_here']} |")
        a, b = text.index("<!--table-->") + len("<!--table-->"), text.index("<!--/table-->")
        out[readme_path] = text[:a] + "\n" + "\n".join(rows) + "\n" + text[b:]
    return out


def main():
    out = build()
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        bad = [p for p, t in out.items() if not os.path.exists(p) or open(p).read() != t]
        for p in bad:
            print("out of date:", os.path.relpath(p, HERE))
        return 1 if bad else 0
    for p, t in out.items():
        with open(p, "w") as f:
            f.write(t)
    print(f"wrote {len(out)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
