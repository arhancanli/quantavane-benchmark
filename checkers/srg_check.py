"""Exact check of a strongly regular graph srg(v, k, lambda, mu) (standard library only).

  python3 -I srg_check.py V K L M FILE

FILE holds one graph in graph6 or sparse6 (an optional >>graph6<< or >>sparse6<< header is allowed), as an edge list
(one edge "u v" per line, vertices numbered from 0), or as an adjacency matrix (V lines of V characters 0/1). The
checker rejects loops and repeated edges, checks that there are V vertices, each of degree K, and computes the number
of common neighbours of every pair of distinct vertices exactly (neighbourhoods are held as bit sets): it must be L
for adjacent pairs and M for non-adjacent pairs. srg(3250, 57, 0, 1) is a Moore graph of degree 57 (diameter 2,
girth 5) and srg(99, 14, 1, 2) is Conway's 99-graph. Prints the parameters and "RESULT 1" (a graph with these
parameters exists); exits 0 for a valid graph, 1 otherwise."""
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
    """(n, edge list) from graph6, sparse6, an adjacency matrix or an edge list."""
    lines = [x.strip() for x in text.splitlines() if x.strip() and not x.strip().startswith("#")]
    if not lines:
        raise ValueError("empty file")
    if len(lines) > 1 and all(set(x) <= {"0", "1"} and len(x) == len(lines) for x in lines):
        n = len(lines)                                         # adjacency matrix
        for i in range(n):
            if lines[i][i] != "0":
                raise ValueError(f"loop at vertex {i}")
            for j in range(i + 1, n):
                if lines[i][j] != lines[j][i]:
                    raise ValueError(f"the matrix is not symmetric at ({i}, {j})")
        return n, [(i, j) for i in range(n) for j in range(i + 1, n) if lines[i][j] == "1"]
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


def main():
    if len(sys.argv) != 6:
        print(__doc__)
        return 2
    v, k, lam, mu = (int(x) for x in sys.argv[1:5])
    try:
        n, edges = decode(open(sys.argv[5], encoding="ascii", errors="strict").read())
    except (ValueError, UnicodeDecodeError) as e:
        print(f"cannot read the graph: {e}")
        return 1
    if n != v:
        print(f"the graph has {n} vertices, not {v}")
        return 1
    adj = [0] * n
    for a, b in edges:
        if a == b:
            print(f"loop at vertex {a}")
            return 1
        if not (0 <= a < n and 0 <= b < n):
            print(f"edge ({a}, {b}) leaves the vertex range 0..{n - 1}")
            return 1
        if adj[a] >> b & 1:
            print(f"edge ({a}, {b}) is repeated")
            return 1
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    for x in range(n):
        d = bin(adj[x]).count("1")
        if d != k:
            print(f"vertex {x} has degree {d}, not {k}")
            return 1
    for x in range(n):
        ax = adj[x]
        for y in range(x + 1, n):
            c = bin(ax & adj[y]).count("1")
            want = lam if ax >> y & 1 else mu
            if c != want:
                kind = "adjacent" if ax >> y & 1 else "non-adjacent"
                print(f"{kind} vertices {x} and {y} have {c} common neighbours, not {want}")
                return 1
    print(f"srg({v}, {k}, {lam}, {mu}): {len(edges)} edges; every pair of vertices checked")
    print("RESULT 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
