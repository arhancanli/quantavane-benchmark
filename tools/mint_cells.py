"""mint_cells.py: turn the MinT pages read by mint_fetch.py into cells, and say which cells an exact check can decide.

A cell is (b, T, m, k): base b, depth T (1 = orthogonal array, 2..8 = ordered orthogonal array, 'net' = a digital
(m-k, m, s)-net, whose depth is k), b^m runs, strength k. Its value is the largest number of factors s of a known
LINEAR object (MinT type "Linear" / "Digital") and the upper bound for linear objects (type "Bound (linear)" /
"Bound (digital)"), because a linear object is what the checker reads. A cell is open when the two differ. The pages
for arbitrary objects are read too, only to note the cells where a non-linear object is already better.

Two exact ways to check a linear object with s factors (checkers/ooa_check.py has both):
  E  list the row space once per line through the origin and read the dual weights: about b^m * s * T' / (b - 1) steps,
  D  walk every depth vector of weight k with a running echelon basis: about N(s, T', k) * k steps,
where T' = min(T, k) and N counts the vectors d in [0, T']^s with sum k. A cell is kept when one more factor than the
best known (s = best + 1) can be checked within WORK steps by the cheaper way.

Cells of depth 1 over GF(2) to GF(9) are left out of the family: such an array is a linear code, and the family
linear-code (codetables.de) already asks for those codes, so every problem is counted once.

usage: python3 -I mint_cells.py PAGES_DIR [OUT.jsonl] [WORK]        (counts; cells as lines of OUT.jsonl)
       python3 -I mint_cells.py PAGES_DIR --family READ REVISION     (writes families/ordered-orthogonal-array/)
"""
import glob, html, json, os, re, sys
D = sys.argv[1]
FAMILY = len(sys.argv) > 2 and sys.argv[2] == '--family'
OUT = None if FAMILY else (sys.argv[2] if len(sys.argv) > 2 else None)
WORK = int(float(sys.argv[3])) if len(sys.argv) > 3 and not FAMILY else 2**27

def num(x):
    x = x.replace(' ', '').replace(' ', '')
    return int(x) if re.fullmatch(r'\d+', x) else None

def parse(fn):
    s = open(fn, encoding='utf-8', errors='replace').read()
    m = re.search(r'b(\d+)_de(\w+?)_m3', os.path.basename(fn)); b = int(m.group(1)); de = m.group(2)
    T = 'net' if de == 'net' else int(de)
    out = {}
    for row in re.findall(r'<tr>(<th[^>]*><i>k</i>.*?)</tr>', s, flags=re.S):      # complete rows only
        hk = re.match(r'<th[^>]*><i>k</i>&#160;=&#160;(\d+)</th>', row)
        if not hk: continue
        for href, title, txt in re.findall(r'<td[^>]*><a href="([^"]+)"(?: title="([^"]*)")?>(.*?)</a></td>', row, flags=re.S):
            q = dict(re.findall(r'(\w+)=(\w+)', html.unescape(href)))
            if not (q.get('m', '').isdigit() and q.get('k', '').isdigit()): continue     # the column m = infinity
            mm, kk = int(q['m']), int(q['k'])
            val = html.unescape(title) if title and re.fullmatch(r'[\d–  -]+', html.unescape(title)) else html.unescape(re.sub(r'<[^>]+>', '', txt))
            val = val.replace('–', '-')
            if '-' in val:
                lo, hi = (num(v) for v in val.split('-', 1))
            else:
                lo = hi = num(val)
            if lo is None or hi is None: continue                                    # blank, infinite, overflow, impossible
            out[(b, T, mm, kk)] = (lo, hi)
    return out

def count_depth_vectors(s, T, k, cap):
    """N(s, T, k) = number of d in [0, T]^s with sum k (stops early once above cap)."""
    row = [1] + [0] * k
    for _ in range(s):
        new = [0] * (k + 1); run = 0
        for j in range(k + 1):
            run += row[j]
            if j - T - 1 >= 0: run -= row[j - T - 1]
            new[j] = run
        row = new
        if row[k] > cap: return row[k]
    return row[k]

anyc, cells = {}, {}
for fn in sorted(glob.glob(os.path.join(D, 'b*_de*_m3_k*.html'))):
    (cells if fn.endswith('_lin.html') else anyc).update(parse(fn))
if not cells:
    sys.exit('no pages for linear objects (run mint_fetch.py OUTDIR lin)')
# the family is about linear objects, the kind the checker reads: best known linear object against the bound for linear ones
openc = {c: v for c, v in cells.items() if v[0] < v[1] and c[3] >= 3 and c[2] >= c[3]}
beaten = sum(1 for c in openc if c in anyc and anyc[c][0] > openc[c][0])
kept = []
ways = {}
by = {}
for (b, T, m, k), (lo, hi) in sorted(openc.items(), key=lambda x: (x[0][0], str(x[0][1]), x[0][2], x[0][3])):
    s = lo + 1; Te = k if T == 'net' else min(T, k)
    wE = (b ** m) * s * Te // (b - 1)
    wD = None
    if wE > WORK:
        n = count_depth_vectors(s, Te, k, WORK)
        wD = n * k
    w = wE if wE <= WORK else wD
    ok = w is not None and w <= WORK
    key = (b, str(T)); st = by.setdefault(key, [0, 0])
    st[0] += 1
    if ok:
        st[1] += 1
        cell = dict(id=f'ooa-b{b}-T{T}-m{m}-k{k}', params=dict(b=b, T=T, m=m, k=k), best=str(lo), bound=str(hi))
        a = anyc.get((b, T, m, k))
        if a and a[0] > lo:
            cell['note'] = f'a non-linear object with {a[0]} factors is known'
        kept.append(cell); ways[cell['id']] = 'E' if wE <= WORK else 'D'
print(f'{len(cells)} cells read for linear objects ({len(anyc)} for arbitrary ones), {len(openc)} open with 3 <= k <= m '
      f'({beaten} of them with a better non-linear object known), {len(kept)} checkable within {WORK:.3g} steps')
bases = sorted({b for b, _ in by})
for b in bases:
    print(f'  b={b}: ' + ', '.join(f'T={T}: {v[1]}/{v[0]}' for (bb, T), v in sorted(by.items()) if bb == b))
print('by way:', {w: sum(1 for v in ways.values() if v == w) for w in 'ED'})
if OUT:
    with open(OUT, 'w') as f:
        for c in kept: f.write(json.dumps(c) + '\n')
if FAMILY:
    read, revision = sys.argv[3], sys.argv[4]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fam_dir = os.path.join(root, 'families', 'ordered-orthogonal-array'); os.makedirs(fam_dir, exist_ok=True)
    dup = [c for c in kept if c['params']['T'] == 1 and c['params']['b'] <= 9]
    cells_out = [c for c in kept if not (c['params']['T'] == 1 and c['params']['b'] <= 9)]
    closed = sum(1 for c, v in cells.items() if v[0] == v[1] and c[3] >= 3 and c[2] >= c[3])
    fam = {
     "family": "ordered-orthogonal-array",
     "title": "Linear ordered orthogonal arrays and digital nets with the largest number of factors",
     "added": "2.2", "objective": "maximize", "id_prefixes": ["ooa-"],
     "keeper": "W. Ch. Schmid and R. Schuerer, MinT, the database of optimal net, code, OA and OOA parameters (mint.sbg.ac.at)",
     "page": "http://mint.sbg.ac.at/",
     "cell_url": "http://mint.sbg.ac.at/query.php?i=x&b={b}&m={m}&k={k}&p=mks&de={T}",
     "read": read, "revision": revision,
     "template": {
      "title": "Linear ordered orthogonal array over GF({b}), depth {T}: {b}^{m} runs, strength {k}",
      "statement": "Find a linear ordered orthogonal array of depth {T} and strength {k} with {b}^{m} runs over GF({b}) that has as many factors as possible. Depth 1 is a linear orthogonal array. Depth net is a digital net in base {b} with {b}^{m} points and strength {k}, that is a digital (t, {m}, s)-net with t = {m} - {k}, where s is the number of factors.",
      "submission": "Text file: a generator matrix with {m} rows. Each factor has as many columns as the depth, in order of depth ({k} columns for depth net), one factor after the other; the entries are integers below {b} (for a prime power the base-p digits of the integer are the coefficients of a polynomial in x modulo the polynomial listed in checkers/ooa_check.py).",
      "args": ["{b}", "{T}", "{m}", "{k}"]},
     "checker": {"program": "ooa_check.py", "value": "result"},
     "score": "the number of factors (larger is better)",
     "best_text": "The best known linear object in MinT has {best} factors; a linear object with more factors improves it.",
     "bound_kind": "upper bound",
     "bound_source": "MinT's bound for linear (digital) objects in the same cell",
     "holder_unknown": "the construction and its source are on the cell's page at MinT",
     "holder_sources": "the tables list values only; each cell's page names its construction",
     "open_rule": "every cell with 3 <= k <= m <= 51 whose best known linear object has fewer factors than MinT's bound for linear objects",
     "left_out": (f"{closed} cells with equal bounds (solved); {len(openc) - len(kept)} open cells where checking one more factor than the best known "
                  f"would take more than 2^27 steps by both methods of the checker (about b^m s T / (b - 1) for the row-space method, the number "
                  f"of depth vectors times k for the other); {len(dup)} cells of depth 1 over GF(2) to GF(9), which are linear codes already asked "
                  f"for by the family linear-code; cells with m above 51 (not read); arrays that are not linear (the checker reads generator "
                  f"matrices; {sum(1 for c in cells_out if 'note' in c)} kept cells carry a note that a non-linear object with more factors is known)"),
     "cells": "cells.jsonl", "count": len(cells_out), "quantavane_records": 0, "single_problems_left_out": 0}
    json.dump(fam, open(os.path.join(fam_dir, 'family.json'), 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(fam_dir, 'cells.jsonl'), 'w') as f:
        for c in cells_out: f.write(json.dumps(c) + '\n')
    print(f'family written: {len(cells_out)} cells ({len(dup)} depth-1 cells over GF(2)-GF(9) left to linear-code; {closed} solved; '
          f'{len(openc) - len(kept)} too costly to check)')
