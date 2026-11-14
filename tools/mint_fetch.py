"""mint_fetch.py: read the small-m corner of every MinT table (OA, OOA depths, nets) for the benchmark family.

MinT (mint.sbg.ac.at; W. Ch. Schmid and R. Schuerer, Salzburg) serves at most 2,500 cells per request. This reads one
window per table: m = 3..51 (columns), strength k = 3..52 (rows), value = the number of factors s, as "lower bound of the
best known object (type Arbitrary)" and "upper bound (type Bound)". One request every 6 seconds, 72 requests in all;
pages are kept as fetched in the directory given (outside the repository), with the time of each read in index.tsv.
Nothing is parsed here (tools/mint_cells.py does that), so a re-run after a failure only fetches what is missing.

With a second argument "lin" it reads the same windows for linear (digital) objects only: the best known linear
object (type "Linear" / "Digital") and the bound for linear objects; those pages get the suffix _lin. A page that
comes back cut (the server stops at some rows of large strength) is read again as two halves.

usage: python3 -I mint_fetch.py OUTDIR [lin]
"""
import os, sys, time, urllib.request, hashlib
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
LIN = len(sys.argv) > 2 and sys.argv[2] == 'lin'
MODE, SUF = ('mode=ed&opt=bd', '_lin') if LIN else ('mode=e&opt=b', '')
DEPTHS = {2: [1, 2, 3, 4, 5, 6, 7, 8, 'net'], 3: [1, 2, 3, 4, 5, 'net'], 256: [1, 2, 3, 4, 5, 6, 'net'],
          81: [1, 2, 3, 4, 'net'], 128: [1, 2, 3, 4, 'net']}
for b in (4, 5, 7, 8, 9, 49, 64): DEPTHS[b] = [1, 2, 3, 'net']
for b in (16, 25, 27, 32): DEPTHS[b] = [1, 2, 'net']
done = 0
for b in sorted(DEPTHS):
    for de in DEPTHS[b]:
        todo = [(3, 52, f'b{b}_de{de}_m3_k3{SUF}.html')]
        while todo:
            lo, hi, name = todo.pop(0)
            fn = os.path.join(OUT, name)
            if os.path.exists(fn) and os.path.getsize(fn) > 5000 and b'</html>' in open(fn, 'rb').read()[-200:]:
                continue
            url = f'http://mint.sbg.ac.at/table.php?i=x&b={b}&de={de}&p=mks&{MODE}&col=0&minx=3&maxx=51&miny={lo}&maxy={hi}'
            time.sleep(6)
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = r.read()
            except Exception as e:
                print(f'b={b} de={de} k={lo}..{hi}: FAILED {e}', flush=True); continue
            open(fn, 'wb').write(data)
            ok = b'</html>' in data[-200:] and b'ERROR' not in data
            with open(os.path.join(OUT, 'index.tsv'), 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{b}\t{de}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}\t{'ok' if ok else 'INCOMPLETE'}\t{url}\n")
            done += 1
            print(f'b={b} de={de} k={lo}..{hi}: {len(data)} bytes {"ok" if ok else "INCOMPLETE"}', flush=True)
            if not ok and (lo, hi) == (3, 52):          # cut by the server: the two halves (rows complete in a cut page are still used)
                todo += [(3, 27, f'b{b}_de{de}_m3_k3_27{SUF}.html'), (28, 52, f'b{b}_de{de}_m3_k28_52{SUF}.html')]
print(f'fetched {done} pages; {sum(len(v) for v in DEPTHS.values())} tables in all')
