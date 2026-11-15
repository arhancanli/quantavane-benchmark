"""golomb_cells.py: T. Rokicki and G. Dogon's table of possibly optimal Golomb rulers (cube20.org/golomb) as the
benchmark family golomb-ruler, checked by checkers/golomb_check.py.

  python3 -I golomb_cells.py LENGTHS.json READ REVISION     (writes families/golomb-ruler/)

LENGTHS.json: {marks: [length, [construction, prime power, multiplier]]}, read from the table's 41 metadata files
golomb-all-00 .. golomb-all-40 (zip archives of text lines "marks length type prime multiplier"). A cell is a number of
marks from 31 to 40,000: optimal rulers are proven only up to 28 marks (distributed.net, 2022), 29 and 30 are single
problems of the benchmark, and the table's authors offer a reward for beating any length from 36 to 40,000 marks."""
import hashlib
import json
import os
import sys

TYPES = {"pp": "projective plane (Singer)", "ap": "affine plane (Bose)"}


def main():
    path, read, revision = sys.argv[1:4]
    raw = open(path, "rb").read()
    rows = {int(k): v for k, v in json.loads(raw).items()}
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    singles = {f[:-5] for f in os.listdir(os.path.join(root, "problems")) if f.endswith(".json")}
    out = []
    for n in range(31, 40001):
        length, meta = rows[n]
        cid = f"golomb-{n}"
        if cid in singles:
            continue
        kind = TYPES.get(meta[0], meta[0]) if meta else "construction"
        holder = f"modular ruler from the {kind} construction over GF({meta[1]}), multiplier {meta[2]}" if len(meta) == 3 else None
        cell = {"id": cid, "params": {"n": n}, "best": str(length)}
        if holder:
            cell["holder"] = holder
        out.append(cell)
    fam = {
        "family": "golomb-ruler", "title": "Golomb rulers with the shortest length",
        "added": "2.2", "objective": "minimize", "id_prefixes": ["golomb-"],
        "keeper": "T. Rokicki and G. Dogon, possibly optimal Golomb rulers calculated for 160 to 40,000 marks (cube20.org/golomb; data from 5 marks)",
        "page": "https://cube20.org/golomb/",
        "read": read, "revision": revision,
        "template": {"title": "Golomb ruler with {n} marks",
                     "statement": "Find {n} integer marks whose pairwise differences are all distinct, with the largest mark minus the smallest (the length) as small as possible.",
                     "submission": "Text file: the {n} marks, integers separated by spaces, commas or new lines; see checkers/golomb_check.py.",
                     "args": ["{n}"]},
        "checker": {"program": "golomb_check.py", "value": "result"},
        "score": "the length (smaller is better)",
        "best_text": "The shortest known ruler in Rokicki and Dogon's table has length {best} ({holder}); a Golomb ruler with {n} marks that is shorter improves it.",
        "holder_unknown": "the construction is named in the table's metadata",
        "holder_sources": "the metadata files: construction type (projective or affine plane), prime power and multiplier",
        "open_rule": "every number of marks from 31 to 40,000 (optimality is proven only up to 28 marks; 29 and 30 are single problems)",
        "left_out": "29 and 30 marks (single problems golomb-29 and golomb-30); 40,001 to 40,178 marks (beyond the range the table's authors name); up to 28 marks (proven optimal)",
        "reward": "the table's authors offer USD 250 for beating any length from 36 to 40,000 marks",
        "check_cost": "checkers/golomb_check.py marks the M(M-1)/2 differences in C above 3,000 marks, in a bit array of length + 1 bits: about 200 MB and a few seconds for 40,000 marks",
        "replayed": "the table's own explicit rulers (rulers-all-00.zip, 5 to 999 marks) agree with its metadata for all 995 sizes, and those for 31, 50, 100, 159, 160, 500 and 999 marks certify the listed lengths through obb.py",
        "data_sha256": hashlib.sha256(raw).hexdigest(),
        "cells": "cells.jsonl", "count": len(out), "quantavane_records": 0, "single_problems_left_out": 2,
    }
    d = os.path.join(root, "families", "golomb-ruler")
    os.makedirs(d, exist_ok=True)
    json.dump(fam, open(os.path.join(d, "family.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(d, "cells.jsonl"), "w") as f:
        for c in out:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print("family written:", len(out))


if __name__ == "__main__":
    main()
