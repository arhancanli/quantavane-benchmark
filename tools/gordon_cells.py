"""gordon_cells.py: D. Gordon's La Jolla Difference Set Repository and La Jolla Circulant Weighing Matrices Repository
as the benchmark families difference-set (checked by checkers/ds_check.py) and circulant-weighing-matrix (checked by
checkers/cwm_check.py).

  python3 -I gordon_cells.py DS.json DS_REVISION CWM.json CWM_REVISION SDS.json SDS_REVISION READ

DS.json, CWM.json and SDS.json are the files ds.json, cwm.json and sds.json of the repositories' Zenodo releases
(difference-sets 1.3, circulant-weighing-matrices v2.0 and signed-difference-sets v2.0, CC BY 4.0); the third gives the
family signed-difference-set, also checked by ds_check.py (--signed). Every entry has a status: All or Yes (known to exist), No (known not
to exist) or Open. A cell is an Open entry: for difference sets, one abelian group of one parameter set (v,k,lambda)
(the repository lists every abelian group of order v for parameter sets that pass the counting, Schutzenberger and
Bruck-Ryser-Chowla tests; its README says v < 100,000, and release 1.3 lists v up to 749,997); for circulant weighing matrices, one proper CW(n, s^2), n < 1,000,
s < 20. The group Z_n1 x ... x Z_nr is named as in the repository (its label) and written for the checker as its
primary decomposition, cyclic groups of prime-power order sorted by prime and then by order, the form of most of the
repository's own sets. Cells that are single problems in problems/ are left out of the family."""
import hashlib
import json
import os
import re
import sys


def factor(n):
    out, p = [], 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            out.append((p, e))
        p += 1
    if n > 1:
        out.append((n, 1))
    return out


def primary(orders):
    return [p ** e for p, e in sorted(c for n in orders for c in factor(n))]


def check_seconds(orders, k):
    """The time ds_check.py's C helper takes for a set of k elements of the group with these primary orders, from its
    measured rates (15 Nov 2026, one core, random sets of the largest sizes): 1.2 ns per ordered pair for cyclic
    groups and Z_2^r (1.4 x 10^11 pairs in Z_749967 in 163 s) and for groups whose padded table (prod (2 f_i - 1)
    entries over the invariant factors f_i) has at most 2^20 entries (0.9 ns measured), 4 ns per pair up to 2^26
    entries (2.7 x 10^10 pairs in 107 s with 6.7 x 10^7 entries; 1.4 x 10^11 pairs in 297 s with 2.9 x 10^6), and
    2.5 ns per pair and coordinate digit by digit beyond (2.3 ns measured)."""
    by_p = {}
    for q in orders:
        p = next(d for d in range(2, q + 1) if q % d == 0)
        by_p.setdefault(p, []).append(q)
    s = max(len(x) for x in by_p.values())
    f = [1] * s
    for qs in by_p.values():
        for i, q in enumerate(sorted(qs, reverse=True)):
            f[i] *= q
    pairs = k * (k - 1)
    if s == 1 or all(x == 2 for x in f):
        return pairs * 1.2e-9
    pad = 1
    for x in f:
        pad *= 2 * x - 1
    if pad <= 2 ** 20:
        return pairs * 1.2e-9
    if pad <= 2 ** 26:
        return pairs * 4e-9
    return pairs * 2.5e-9 * len(orders)


CAP_SECONDS = 600


def write(root, fam, rows):
    singles = {f[:-5] for f in os.listdir(os.path.join(root, "problems")) if f.endswith(".json")}
    kept = [c for c in rows if c["id"] not in singles]
    assert len({c["id"] for c in kept}) == len(kept), "duplicate ids"
    fam = dict(fam, cells="cells.jsonl", count=len(kept), quantavane_records=0,
               single_problems_left_out=len(rows) - len(kept))
    d = os.path.join(root, "families", fam["family"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "family.json"), "w") as f:
        f.write(json.dumps(fam, indent=1, ensure_ascii=False) + "\n")
    with open(os.path.join(d, "cells.jsonl"), "w") as f:
        for c in kept:
            f.write(json.dumps(c, ensure_ascii=False, separators=(", ", ": ")) + "\n")
    print(fam["family"], len(kept), "cells;", len(rows) - len(kept), "single problems left out")


def main():
    ds_path, ds_rev, cw_path, cw_rev, sds_path, sds_rev, read = sys.argv[1:8]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # ---------------------------------------------------------------------------------------- difference sets
    raw = open(ds_path, "rb").read()
    ds = json.loads(raw)
    stats, rows = {}, []
    for key, e in ds.items():
        st = e["status"]
        stats[st] = stats.get(st, 0) + 1
        if st != "Open":
            continue
        m = re.fullmatch(r"DS\((\d+),(\d+),(\d+),\[([\d,]+)\]\)", key)
        assert m, key
        v, k, lam = int(m[1]), int(m[2]), int(m[3])
        label = [int(x) for x in m[4].split(",")]
        prod = 1
        for n in label:
            prod *= n
        assert prod == v and lam * (v - 1) == k * (k - 1), key
        orders = primary(label)
        if check_seconds(orders, k) > CAP_SECONDS:
            stats["Open, check above ten minutes"] = stats.get("Open, check above ten minutes", 0) + 1
            continue
        rows.append({"id": f"ds-{v}-{k}-{lam}-{'x'.join(map(str, label))}",
                     "params": {"v": v, "k": k, "l": lam, "group": " x ".join(f"Z_{n}" for n in label),
                                "primary": " x ".join(f"Z_{n}" for n in orders),
                                "orders": ",".join(map(str, orders))},
                     "best": "0"})
    print("difference sets:", stats)
    write(root, {
        "family": "difference-set",
        "title": "Difference sets in abelian groups whose existence is unknown",
        "added": "2.2", "objective": "maximize", "id_prefixes": ["ds-"],
        "keeper": "D. Gordon, La Jolla Difference Set Repository (dmgordon.org/difference-sets; data on Zenodo, "
                  "CC BY 4.0)",
        "page": "https://dmgordon.org/difference-sets/",
        "read": read, "revision": ds_rev,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "template": {
            "title": "({v},{k},{l}) difference set in {group}",
            "statement": "Find {k} distinct elements of the abelian group G = {group} (written {primary}) such that "
                         "every nonzero element of G is a difference of two of them in exactly {l} ways: a "
                         "({v},{k},{l}) difference set in G.",
            "submission": "Text file: {k} lines, one element per line as its coordinates in {primary} (integers "
                          "0 <= a_c < n_c separated by spaces, in that order).",
            "args": ["{orders}", "{k}", "{l}"]},
        "checker": {"program": "ds_check.py", "value": "result"},
        "score": "1 for a difference set with these parameters in this group; none is known, so the best known "
                 "value is 0",
        "best_text": "Its existence is Open in Gordon's repository: no such set is known and none has been ruled out, "
                     "so the best known value is {best}; a valid set scores 1.",
        "holder_unknown": "none known (existence open)",
        "holder_sources": "the repository's entry for these parameters and group",
        "open_rule": "every entry with status Open: one abelian group of one parameter set (v,k,lambda) (release 1.3 "
                     "lists v up to 749,997)",
        "left_out": f"{stats.get('All', 0) + stats.get('Yes', 0)} entries known to exist (All or Yes), "
                    f"{stats.get('No', 0)} known not to exist (No), and "
                    f"{stats.get('Open, check above ten minutes', 0)} open entries whose check would take more than "
                    "ten minutes in ds_check.py's C helper (check_seconds in tools/gordon_cells.py: k(k - 1) ordered "
                    "pairs at the measured rate of the method the group allows)",
        "counts": dict(stats, **{"distinct open parameter sets (v,k,lambda)": len({r["id"].rsplit("-", 1)[0]
                                                                                 for r in rows})}),
    }, rows)
    # ---------------------------------------------------------------------------------------- circulant weighing
    raw = open(cw_path, "rb").read()
    cw = json.loads(raw)
    stats, rows = {}, []
    for key, e in cw.items():
        st = e["status"]
        stats[st] = stats.get(st, 0) + 1
        if st != "Open":
            continue
        m = re.fullmatch(r"CW\((\d+),(\d+)\)", key)
        assert m, key
        n, s = int(m[1]), int(m[2])
        rows.append({"id": f"cwm-{n}-{s * s}", "params": {"n": n, "s": s, "k": s * s}, "best": "0"})
    print("circulant weighing matrices:", stats)
    write(root, {
        "family": "circulant-weighing-matrix",
        "title": "Proper circulant weighing matrices whose existence is unknown",
        "added": "2.2", "objective": "maximize", "id_prefixes": ["cwm-"],
        "keeper": "D. Gordon, La Jolla Circulant Weighing Matrices Repository (dmgordon.org/circulant-weighing-matrices; "
                  "data on Zenodo, CC BY 4.0)",
        "page": "https://dmgordon.org/circulant-weighing-matrices/",
        "read": read, "revision": cw_rev,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "template": {
            "title": "Proper circulant weighing matrix CW({n}, {s}^2)",
            "statement": "Find a proper circulant weighing matrix CW({n},{k}): a circulant {n} x {n} matrix W with "
                         "entries -1, 0, 1 and W W^T = {k} I whose first row's support is not inside a coset of a "
                         "proper subgroup of Z_{n} (an improper one comes from a smaller order).",
            "submission": "Text file: the first row, {n} entries -1, 0, 1 separated by spaces (or the characters -, "
                          "0, +).",
            "args": ["{n}", "{k}"]},
        "checker": {"program": "cwm_check.py", "value": "result"},
        "score": "1 for a proper CW of these parameters; none is known, so the best known value is 0",
        "best_text": "Its existence is Open in Gordon's repository: no proper matrix is known and none has been "
                     "ruled out, so the best known value is {best}; a valid first row scores 1.",
        "holder_unknown": "none known (existence open)",
        "holder_sources": "the repository's entry CW(n,s)",
        "open_rule": "every entry CW(n,s) with status Open (n < 1,000, s < 20; the repository's statuses are about "
                     "proper matrices)",
        "left_out": f"{stats.get('All', 0) + stats.get('Yes', 0)} entries known to exist (All or Yes) and "
                    f"{stats.get('No', 0)} known not to exist (No)",
        "counts": stats,
    }, rows)

    # ---------------------------------------------------------------------------------------- signed difference sets
    raw = open(sds_path, "rb").read()
    sds = json.loads(raw)
    stats, rows = {}, []
    for key, e in sds.items():
        st = e["status"]
        stats[st] = stats.get(st, 0) + 1
        if st != "Open":
            continue
        m = re.fullmatch(r"SDS\((\d+),(\d+),(-?\d+),\[([\d,]+)\]\)", key)
        assert m, key
        v, k, lam = int(m[1]), int(m[2]), int(m[3])
        label = [int(x) for x in m[4].split(",")]
        prod = 1
        for n in label:
            prod *= n
        assert prod == v and k <= v, key
        orders = primary(label)
        rows.append({"id": f"sds-{v}-{k}-{lam}-{'x'.join(map(str, label))}".replace("--", "-m"),
                     "params": {"v": v, "k": k, "l": lam, "n": k - lam,
                                "group": " x ".join(f"Z_{n}" for n in label),
                                "primary": " x ".join(f"Z_{n}" for n in orders),
                                "orders": ",".join(map(str, orders))},
                     "best": "0"})
    print("signed difference sets:", stats)
    write(root, {
        "family": "signed-difference-set",
        "title": "Signed difference sets in abelian groups whose existence is unknown",
        "added": "2.2", "objective": "maximize", "id_prefixes": ["sds-"],
        "keeper": "D. Gordon, La Jolla Signed Difference Set Repository (dmgordon.org/signed-difference-sets; data on "
                  "Zenodo, CC BY 4.0)",
        "page": "https://dmgordon.org/signed-difference-sets/",
        "read": read, "revision": sds_rev,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "template": {
            "title": "Signed ({v},{k},{l}) difference set in {group}",
            "statement": "Find {k} distinct elements d_i of the abelian group G = {group} (written {primary}) and "
                         "signs s_i = +1 or -1 such that D = sum s_i d_i satisfies D D^(-1) = {n} + {l} G in the "
                         "group ring: for every nonzero g in G, the sum of s_i s_j over the ordered pairs with "
                         "d_i - d_j = g is {l}. A signed ({v},{k},{l}) difference set (Gordon, 2023).",
            "submission": "Text file: {k} lines, one element per line: its sign + or -, then its coordinates in "
                          "{primary} (integers 0 <= a_c < n_c separated by spaces, in that order).",
            "args": ["{orders}", "{k}", "{l}", "--signed"]},
        "checker": {"program": "ds_check.py", "value": "result"},
        "score": "1 for a signed difference set with these parameters in this group; none is known, so the best "
                 "known value is 0",
        "best_text": "Its existence is Open in Gordon's repository: no such set is known and none has been ruled out, "
                     "so the best known value is {best}; a valid set scores 1.",
        "holder_unknown": "none known (existence open)",
        "holder_sources": "the repository's entry for these parameters and group",
        "open_rule": "every entry SDS(v,k,lambda,G) with status Open (v < 500 in release v2.0)",
        "left_out": f"{stats.get('All', 0) + stats.get('Yes', 0)} entries known to exist (All or Yes) and "
                    f"{stats.get('No', 0)} known not to exist (No)",
        "counts": dict(stats, **{"distinct open parameter sets (v,k,lambda)": len({r["id"].rsplit("-", 1)[0]
                                                                                 for r in rows})}),
    }, rows)


if __name__ == "__main__":
    main()
