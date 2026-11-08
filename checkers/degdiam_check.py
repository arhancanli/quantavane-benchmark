"""Exact check of a graph for the degree-diameter problem (standard library only).

  python3 -I degdiam_check.py DELTA DIAMETER FILE

FILE holds one graph in graph6 or sparse6 (an optional >>graph6<< or >>sparse6<< header is allowed) or as an edge
list, one edge "u v" per line with vertices numbered from 0. The checker rejects loops and repeated edges, checks that
no vertex has more than DELTA neighbours, and that every two vertices are joined by a path of at most DIAMETER edges:
the ball of radius r around each vertex is kept as a bit set, B_{r+1}(v) = B_r(v) or the union of B_r(u) over the
neighbours u of v, and after DIAMETER rounds every ball must hold every vertex. A graph on n vertices with maximum
degree DELTA and diameter at most DIAMETER shows N(DELTA, DIAMETER) >= n. Prints the order and "RESULT n"; exits 0 for
a valid graph, 1 otherwise."""
import sys


def bits6(data):
    for ch in data:
        c = ch - 63
        if not 0 <= c < 64:
            raise ValueError(f"character {chr(ch)!r} is not graph6/sparse6 data")
        for s in (5, 4, 3, 2, 1, 0):
            yield (c >> s) & 1


def read_n(data):
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
    if first[:1] == ":" or (not first[:1].isdigit() and len(lines) == 1):
        if len(lines) != 1:
            raise ValueError("one graph per file")
        data = first.encode("ascii")
        if data[:1] == b":":
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
        n, used = read_n(data)
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
    edges = []
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


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    delta, diam = int(sys.argv[1]), int(sys.argv[2])
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
    top = max(len(a) for a in adj) if n else 0
    if top > delta:
        v = next(v for v in range(n) if len(adj[v]) == top)
        print(f"vertex {v} has degree {top} > {delta}")
        return 1
    full = (1 << n) - 1
    ball = [(1 << v) for v in range(n)]
    for _ in range(diam):
        nxt = []
        for v in range(n):
            b = ball[v]
            for u in adj[v]:
                b |= ball[u]
            nxt.append(b)
        ball = nxt
    for v in range(n):
        if ball[v] != full:
            miss = (full ^ ball[v]) & -(full ^ ball[v])
            print(f"vertices {v} and {miss.bit_length() - 1} are more than {diam} apart")
            return 1
    print(f"n {n} edges {len(seen)} maximum degree {top} <= {delta} diameter <= {diam}")
    print(f"RESULT {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
