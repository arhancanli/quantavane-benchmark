"""Exact check of a (k,g)-graph: a k-regular simple graph whose girth is at least g (standard library only).

  python3 -I cage_check.py K G FILE

FILE holds one graph in graph6 or sparse6 (as on House of Graphs; an optional >>graph6<< or >>sparse6<< header is
allowed) or as an edge list, one edge "u v" per line with vertices numbered from 0. The checker decodes the graph,
rejects loops and repeated edges, checks that every vertex has degree K, and searches for a cycle of length below G.
A k-regular graph of girth at least g on n vertices shows n(k,g) <= n, since cages grow with the girth.

The cycle search runs a breadth-first search from every vertex r inside the vertices numbered r or more: a shortest
cycle lies in that part for its smallest vertex r, and a breadth-first search from a vertex of a shortest cycle meets
it again at depth half its length (two parents at one depth for an even cycle, an edge inside one depth for an odd
one). Any such meeting is a closed walk without backtracking, so a cycle at most that long exists. Prints the order,
the degree and the girth bound, then "RESULT n"; exits 0 for a valid graph, 1 otherwise."""
import sys


def bits6(data):
    for ch in data:
        c = ch - 63
        if not 0 <= c < 64:
            raise ValueError(f"character {chr(ch)!r} is not graph6/sparse6 data")
        for s in (5, 4, 3, 2, 1, 0):
            yield (c >> s) & 1


def read_n(data):
    """N(n) of graph6/sparse6: returns (n, bytes used)."""
    if data[0] != 126:
        return data[0] - 63, 1
    if len(data) > 1 and data[1] == 126:
        n = 0
        for ch in data[2:8]:
            n = (n << 6) | (ch - 63)
        return n, 8
    n = 0
    for ch in data[1:4]:
        n = (n << 6) | (ch - 63)
    return n, 4


def decode(text):
    """(n, edge list) from graph6, sparse6 or an edge list."""
    lines = [x.strip() for x in text.splitlines() if x.strip() and not x.strip().startswith("#")]
    if not lines:
        raise ValueError("empty file")
    first = lines[0]
    for head in (">>graph6<<", ">>sparse6<<"):
        if first.startswith(head):
            first = first[len(head):]
    if first[:1] == ":" or (first[:1].isascii() and not first[:1].isdigit() and len(lines) == 1):
        if len(lines) != 1:
            raise ValueError("one graph per file")
        data = first.encode("ascii")
        if data[:1] == b":":                                   # sparse6
            n, used = read_n(data[1:])
            k = max(1, (n - 1).bit_length())
            bits = list(bits6(data[1 + used:]))
            edges, v, i = [], 0, 0
            while i + 1 + k <= len(bits):
                b = bits[i]
                x = 0
                for t in bits[i + 1:i + 1 + k]:
                    x = (x << 1) | t
                i += 1 + k
                if b:
                    v += 1
                if v >= n:
                    break
                if x > v:
                    v = x
                else:
                    edges.append((x, v))
            return n, edges
        n, used = read_n(data)                                 # graph6
        need = n * (n - 1) // 2
        bits = bits6(data[used:])
        edges = []
        try:
            for j in range(1, n):
                for i in range(j):
                    if next(bits):
                        edges.append((i, j))
        except StopIteration:
            raise ValueError("graph6 data too short") from None
        if len(data) - used != (need + 5) // 6:
            raise ValueError("graph6 data has the wrong length")
        return n, edges
    edges = []                                                 # edge list
    for line in lines:
        parts = line.replace(",", " ").split()
        if len(parts) != 2:
            raise ValueError(f"not an edge: {line[:60]!r}")
        u, v = int(parts[0]), int(parts[1])
        if u < 0 or v < 0:
            raise ValueError("vertices are numbered from 0")
        edges.append((u, v))
    n = 1 + max(max(e) for e in edges)
    return n, edges


def short_cycle(n, adj, g):
    """A vertex on a cycle of length < g, or None."""
    maxl = g - 1                     # forbidden cycle lengths 3..g-1
    stamp = [0] * n
    depth = [0] * n
    parent = [-1] * n
    for r in range(n):
        tag = r + 1
        stamp[r], depth[r], parent[r] = tag, 0, -1
        frontier, d = [r], 0
        while frontier and 2 * d + 1 <= maxl:
            keep = 2 * d + 2 <= maxl
            nxt = []
            for u in frontier:
                pu = parent[u]
                for w in adj[u]:
                    if w < r or w == pu:
                        continue
                    if stamp[w] == tag:
                        dw = depth[w]
                        if dw == d or (dw == d + 1 and 2 * d + 2 <= maxl) or dw < d:
                            return r
                    elif keep:
                        stamp[w], depth[w], parent[w] = tag, d + 1, u
                        nxt.append(w)
            frontier, d = nxt, d + 1
    return None


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    k, g = int(sys.argv[1]), int(sys.argv[2])
    try:
        n, edges = decode(open(sys.argv[3], encoding="ascii", errors="strict").read())
    except (ValueError, UnicodeDecodeError) as e:
        print(f"cannot read the graph: {e}")
        return 1
    adj = [[] for _ in range(n)]
    seen = set()
    for u, v in edges:
        if u == v:
            print(f"loop at vertex {u}")
            return 1
        if not (0 <= u < n and 0 <= v < n):
            print(f"edge {u} {v} outside 0..{n - 1}")
            return 1
        e = (u, v) if u < v else (v, u)
        if e in seen:
            print(f"repeated edge {e[0]} {e[1]}")
            return 1
        seen.add(e)
        adj[u].append(v)
        adj[v].append(u)
    bad = [v for v in range(n) if len(adj[v]) != k]
    if bad:
        print(f"vertex {bad[0]} has degree {len(adj[bad[0]])}, not {k} ({len(bad)} such vertices)")
        return 1
    hit = short_cycle(n, adj, g)
    if hit is not None:
        print(f"a cycle of length below {g} passes through vertex {hit}")
        return 1
    print(f"n {n} edges {len(seen)} every degree {k} girth >= {g}")
    print(f"RESULT {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
