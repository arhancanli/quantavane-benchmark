#!/usr/bin/env python3
"""Search for unknotting sequences of closed braids (Quantavane Open Tables; standard library only).

  python3 -I tools/unknot_search.py CELLS.jsonl OUTDIR [--mode replay|improve] [--seconds S] [--knots K1,K2,...]
                                    [--seed N] [--grow G]

For each cell (a knot with its braid word and its best known upper bound b on the unknotting number), look for k
crossing changes that turn the knot into the unknot, with k = b ('replay': a certificate for the published bound) or
k = b - 1 ('improve': a new upper bound). Diagrams are varied by random moves that keep the closed braid in its
isotopy class (commutations, braid relations, conjugations, cancelling pairs, stabilizations); in each diagram every
set of k crossings is tried, the closure is tested with the reduced Burau representation at three values of t
(Delta(t0) must be +-t0^j), and the survivors are simplified to the empty braid by braid moves. Every certificate found
is replayed by checkers/unknot_check.py before it is written to OUTDIR/KNOT.txt. A closure with Alexander polynomial 1
that the simplifier cannot finish is tested with the Jones polynomial: a non-trivial one proves it knotted (counted);
a trivial one gets a longer simplification and, failing that, is written to OUTDIR/KNOT.candidates.jsonl.
One line of JSON per knot on stdout."""
import itertools
import json
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import braids  # noqa: E402

CHECKER = os.path.join(os.path.dirname(HERE), "checkers", "unknot_check.py")
GROW = None                          # --grow G: add 0..G crossings (pairs or stabilizations) to each diagram


def parse(w):
    return [int(x) for x in w.strip("[]").split(",")]


def check(braid, path):
    r = subprocess.run([sys.executable, "-I", CHECKER, braid, path], capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    return r.returncode == 0 and last.startswith("RESULT "), last


def variant(w0, n0, rng, grow, neutral):
    br = braids.Braid(w0, n0)
    for _ in range(neutral):
        br.random_neutral(rng)
    for _ in range(grow):
        br.random_grow(rng)
        for _ in range(rng.randrange(0, 6)):
            br.random_neutral(rng)
    return br


def search(cell, k, seconds, rng, outdir):
    w0 = parse(cell["params"]["braid"])
    n0 = max(abs(x) for x in w0) + 1
    t_end = time.time() + seconds
    tried = passed = diagrams = knotted = jones_trivial = 0
    filt = {}
    first = True
    while time.time() < t_end:
        if first:
            br, first = braids.Braid(w0, n0), False
        else:
            grow = rng.choice((0, 0, 1, 1, 2, 2, 3, 4)) if GROW is None else rng.randrange(0, GROW + 1)
            br = variant(w0, n0, rng, grow, rng.randrange(0, 25))
        diagrams += 1
        L, n = len(br.w), br.n
        if (n, L) not in filt:
            filt[(n, L)] = braids.Filter(n, L + 4)
        F = filt[(n, L)]
        subsets = list(itertools.combinations(range(L), k))
        rng.shuffle(subsets)
        for S in subsets:
            if time.time() > t_end:
                break
            tried += 1
            w = list(br.w)
            for p in S:
                w[p] = -w[p]
            if braids.components(w, n) != 1 or not F.maybe_unknot(w):
                continue
            passed += 1
            cand = br.copy()
            for p in S:
                cand.X(p)
            if not braids.simplify(cand, rng):
                # Alexander polynomial 1 but not simplified: the Jones polynomial tells a knotted closure apart
                trivial_jones = braids.jones(w, n) == {0: 1}
                if trivial_jones:
                    jones_trivial += 1
                    cand = br.copy()
                    for p in S:
                        cand.X(p)
                    if braids.simplify(cand, rng, budget=60000):
                        trivial_jones = False
                    else:
                        with open(os.path.join(outdir, cell["params"]["knot"] + ".candidates.jsonl"), "a") as f:
                            f.write(json.dumps({"knot": cell["params"]["knot"], "k": k, "n": n, "word": w,
                                                "moves": br.log + [f"X {p}" for p in S]}) + "\n")
                        continue
                else:
                    knotted += 1
                    continue
            path = os.path.join(outdir, cell["params"]["knot"] + ".txt")
            tmp = path + ".tmp"
            with open(tmp, "w") as f:
                f.write(f"# {cell['params']['knot']}: {k} crossing changes in a closed braid diagram of the knot, "
                        f"then braid moves to the empty braid (checkers/unknot_check.py)\n")
                f.write("\n".join(cand.log) + "\n")
            ok, last = check(cell["params"]["braid"], tmp)
            if ok and last == f"RESULT {k}":
                os.replace(tmp, path)
                return {"knot": cell["params"]["knot"], "k": k, "found": True, "diagrams": diagrams,
                        "subsets": tried, "filter_passed": passed, "alexander_trivial_knotted": knotted,
                        "jones_trivial_unsimplified": jones_trivial, "moves": len(cand.log), "file": path}
            os.remove(tmp)
            return {"knot": cell["params"]["knot"], "k": k, "found": False, "error": "checker refused: " + last}
    return {"knot": cell["params"]["knot"], "k": k, "found": False, "diagrams": diagrams, "subsets": tried,
            "filter_passed": passed, "alexander_trivial_knotted": knotted, "jones_trivial_unsimplified": jones_trivial}


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        return 2
    cells_path, outdir = args[0], args[1]
    opts = dict(zip(args[2::2], args[3::2]))
    mode = opts.get("--mode", "replay")
    seconds = float(opts.get("--seconds", "60"))
    only = set(opts["--knots"].split(",")) if "--knots" in opts else None
    rng = random.Random(int(opts.get("--seed", "1")))
    global GROW
    GROW = int(opts["--grow"]) if "--grow" in opts else None
    os.makedirs(outdir, exist_ok=True)
    for line in open(cells_path):
        if not line.strip():
            continue
        cell = json.loads(line)
        if only and cell["params"]["knot"] not in only:
            continue
        b = int(cell["best"])
        k = b if mode == "replay" else b - 1
        res = search(cell, k, seconds, rng, outdir)
        res["mode"] = mode
        print(json.dumps(res), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
