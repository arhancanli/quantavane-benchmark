"""Exact checkers for graph invariants of the regular 4-polytopes and the E8 polytopes (Quantavane Originals;
standard library only).

  python3 -I orig_graphs.py PROBLEM KIND FILE
  python3 -I orig_graphs.py code KIND D FILE

KIND names the graph, built exactly by polytope_graph in checkers/orig_phys.py (loaded from this folder, so the
vertex numbering is the one every polytope problem of the Originals uses): 5-cell, 8-cell, 16-cell, 24-cell,
600-cell and 120-cell (or 5, 8, 16, 24, 600, 120) for the six regular 4-polytopes (the 5-cell K5; the tesseract,
vertices 0..15 as bit vectors; the 16-cell; the 24-cell; the 600-cell, 120 vertices in the order of their exact
coordinates in Q(sqrt 5); the 120-cell, 600 vertices, the cells of the 600-cell), gosset (the Gosset polytope 3_21,
56 vertices), e8 (the E8 root polytope 4_21, 240 vertices) and assoc-M for M = 4..12 (the associahedron of the
convex M-gon: its triangulations, as sorted tuples of diagonals (i, j) in lexicographic order, adjacent when they
differ by one flip; Catalan(M - 2) vertices, (M - 3)-regular), cyclo-N for N = 2..7 (the cyclohedron W_N: the
centrally symmetric triangulations of the 2N-gon, adjacent by a centrally symmetric flip; C(2N - 2, N - 1) vertices,
(N - 1)-regular) and perm-N for N = 2..7 (the permutahedron: the permutations of 1..N in lexicographic order,
adjacent when they differ by exchanging the values k and k + 1; N! vertices, (N - 1)-regular).
FILE lists vertex numbers (spaces or newlines; lines starting with # are skipped) unless said otherwise. The check
prints what it verified and ends with "RESULT v"; it exits 0 only for a valid certificate. Problems:

  zero-forcing     a zero forcing set: colour the listed vertices black; while a black vertex has exactly one white
                   neighbour, that neighbour turns black. Valid when every vertex ends black. Value: the number of
                   listed vertices (minimize).
  power-domination a power dominating set: the listed vertices and all their neighbours are observed, then the
                   zero forcing rule runs on the observed set. Valid when every vertex ends observed. Value: the number
                   of listed vertices (minimize).
  locating-dom     a locating-dominating set D: every vertex outside D has a neighbour in D, and the sets N(v) & D are
                   different for different vertices v outside D. Value: |D| (minimize).
  induced-matching FILE: one edge "u v" per line; valid when the edges are edges of the graph, pairwise disjoint, and
                   no edge of the graph joins two of them (an induced matching). Value: the number of edges (maximize).
  burning          a burning sequence v_1, ..., v_k (in order): valid when every vertex lies within distance k - i of
                   some v_i (the fire started at v_i in round i spreads one step per round, and k rounds burn the
                   graph). Value: k (minimize).
  l21              FILE: one label (a non-negative integer) per vertex, in vertex order; valid when adjacent vertices
                   get labels at least 2 apart and vertices at distance 2 different labels (an L(2,1)-labelling).
                   Value: the largest label, the span (minimize).
  bandwidth        FILE: every vertex once, in the order of a numbering; value: the largest difference of positions
                   over the edges (minimize).
  bisection        FILE: one bit 0 or 1 per vertex, in vertex order, as many 0s as 1s (one more of either when the
                   number of vertices is odd); value: the number of edges between the two halves (minimize).
  resolving        a resolving set W: the vectors of distances from each vertex to the vertices of W (in the listed
                   order) are all different. Value: |W| (minimize; the minimum is the metric dimension).
  ising            FILE: one spin per vertex in vertex order, + or - (or 1 and -1); value: the energy of the Ising
                   antiferromagnet, the sum over the edges uv of s_u s_v (minimize; -|E| + 2 x the number of
                   frustrated edges).
  domination       a dominating set D: every vertex outside D has a neighbour in D. Value: |D| (minimize).
  independent      an independent set: no two listed vertices adjacent. Value: the number of listed vertices
                   (maximize; the maximum is the independence number).
  total-dom        a total dominating set D: every vertex (in D or not) has a neighbour in D. Value: |D| (minimize).
  independent-dom  an independent dominating set: no two listed vertices adjacent, every other vertex adjacent to one
                   of them. Value: the number of listed vertices (minimize).
  induced-bipartite FILE: one character per vertex in vertex order, 0 or 1 (the side of a chosen vertex) or . (not
                   chosen); valid when no edge joins two chosen vertices on the same side, so the chosen vertices
                   induce a bipartite subgraph. Value: the number of chosen vertices (maximize).
  distance2-colouring FILE: one colour (a non-negative integer) per vertex in vertex order; valid when vertices at
                   distance 1 or 2 get different colours (a proper colouring of the square of the graph). Value: the
                   number of different colours used (minimize).
  max-leaf         FILE: one edge "u v" per line; valid when the edges are edges of the graph forming a spanning tree
                   (n - 1 edges, connected). Value: the number of leaves of the tree (maximize).
  code D           a code of minimum distance D: valid when every two listed vertices are at distance at least D in the
                   graph. Value: the number of listed vertices (maximize).
  roman            FILE: one value 0, 1 or 2 per vertex in vertex order; valid when every vertex with 0 has a
                   neighbour with 2 (a Roman dominating function). Value: the sum of the values (minimize).
  2-domination     a set D in which every vertex outside D has at least two neighbours. Value: |D| (minimize).
  grundy           FILE: one colour 1, 2, ... per vertex in vertex order; valid when the colouring is proper and every
                   vertex of colour c has neighbours of every colour 1..c-1 (so first-fit, in order of colour, produces
                   it). Value: the number of colours (maximize; the maximum is the Grundy number).
  b-colouring      FILE: one colour per vertex in vertex order; valid when the colouring is proper and every colour
                   class has a vertex adjacent to all the other classes. Value: the number of colours (maximize).
  linear-arrangement FILE: every vertex once, in the order of a numbering; value: the sum over the edges of the
                   difference of positions (minimize).
  strong-edge      FILE: one line "u v c" per edge, every edge once with a colour c >= 0; valid when two edges of the
                   same colour never share a vertex and are never joined by an edge (each class an induced matching).
                   Value: the number of colours (minimize; the minimum is the strong chromatic index).
  domatic          FILE: one class number per vertex in vertex order (non-negative integers); valid when every class
                   is a dominating set. Value: the number of classes (maximize; the maximum is the domatic number)."""
import importlib.util
import itertools
import os
import sys
from collections import deque

_spec = importlib.util.spec_from_file_location("orig_phys", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                          "orig_phys.py"))
_phys = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_phys)
KINDS = ("5", "8", "16", "24", "600", "120", "gosset", "e8")
ALIASES = {"5-cell": "5", "8-cell": "8", "16-cell": "16", "24-cell": "24", "600-cell": "600", "120-cell": "120"}


def associahedron(m):
    """The flip graph of the triangulations of a convex m-gon (vertices 0..m-1), the graph of the associahedron.
    A triangulation is the sorted tuple of its m - 3 diagonals (i, j), i < j; the triangulations are numbered in
    lexicographic order of these tuples; two are adjacent when they differ in exactly one diagonal (a flip)."""
    def tri(lo, hi):                         # triangulations of the polygon lo, lo + 1, ..., hi (as lists of diagonals)
        if hi - lo < 2:
            return [[]]
        out = []
        for k in range(lo + 1, hi):          # the triangle lo, k, hi
            for a in tri(lo, k):
                for b in tri(k, hi):
                    d = list(a) + list(b)
                    if k - lo >= 2:
                        d.append((lo, k))
                    if hi - k >= 2:
                        d.append((k, hi))
                    out.append(d)
        return out
    ts = sorted(tuple(sorted(t)) for t in tri(0, m - 1))
    idx = {t: i for i, t in enumerate(ts)}
    edges = set()
    for i, t in enumerate(ts):
        st = set(t)
        for d in t:
            rest = st - {d}
            for e in ((a, b) for a in range(m) for b in range(a + 2, m) if (a, b) != (0, m - 1) and (a, b) != d):
                j = idx.get(tuple(sorted(rest | {e})))
                if j is not None and j != i:
                    edges.add((min(i, j), max(i, j)))
    return len(ts), sorted(edges)


def triangulations(m):
    """All triangulations of the convex m-gon (vertices 0..m-1), each as a sorted tuple of its diagonals (i, j), i < j."""
    def tri(lo, hi):
        if hi - lo < 2:
            return [[]]
        out = []
        for k in range(lo + 1, hi):
            for a in tri(lo, k):
                for b in tri(k, hi):
                    d = list(a) + list(b)
                    if k - lo >= 2:
                        d.append((lo, k))
                    if hi - k >= 2:
                        d.append((k, hi))
                    out.append(d)
        return out
    return sorted(tuple(sorted(t)) for t in tri(0, m - 1))


def cyclohedron(n):
    """The graph of the cyclohedron W_n: the centrally symmetric triangulations of the convex 2n-gon (those mapped to
    themselves by i -> i + n mod 2n), numbered in lexicographic order of their sorted diagonal tuples; two are adjacent
    when one is obtained from the other by a centrally symmetric flip (one diameter replaced by another, or a pair of
    opposite diagonals flipped together), i.e. when their diagonal sets differ in 2 or 4 diagonals."""
    m = 2 * n
    rot = lambda d: tuple(sorted(((d[0] + n) % m, (d[1] + n) % m)))
    ts = [t for t in triangulations(m) if set(map(rot, t)) == set(t)]
    edges = []
    for i in range(len(ts)):
        si = set(ts[i])
        for j in range(i + 1, len(ts)):
            if len(si ^ set(ts[j])) <= 4:
                edges.append((i, j))
    return len(ts), edges


def permutahedron(n):
    """The graph of the permutahedron of order n: the permutations of 1..n as vectors, in lexicographic order; two are
    adjacent when one is obtained from the other by exchanging the values k and k + 1 (the edges of the convex hull)."""
    perms = sorted(itertools.permutations(range(1, n + 1)))
    idx = {p: i for i, p in enumerate(perms)}
    edges = []
    for i, p in enumerate(perms):
        pos = {v: k for k, v in enumerate(p)}
        for v in range(1, n):
            q = list(p)
            q[pos[v]], q[pos[v + 1]] = v + 1, v
            j = idx[tuple(q)]
            if i < j:
                edges.append((i, j))
    return len(perms), sorted(edges)


def graph(kind):
    kind = ALIASES.get(kind, kind)
    for prefix, build, lo, hi in (("cyclo-", cyclohedron, 2, 7), ("perm-", permutahedron, 2, 7)):
        if kind.startswith(prefix) and kind[len(prefix):].isdigit() and lo <= int(kind[len(prefix):]) <= hi:
            n, edges = build(int(kind[len(prefix):]))
            adj = [set() for _ in range(n)]
            for a, b in edges:
                adj[a].add(b)
                adj[b].add(a)
            return n, edges, adj
    if kind.startswith("assoc-") and kind[6:].isdigit() and 4 <= int(kind[6:]) <= 12:
        n, edges = associahedron(int(kind[6:]))
        adj = [set() for _ in range(n)]
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        return n, edges, adj
    if kind not in KINDS:
        raise ValueError(f"KIND must be one of {', '.join(KINDS)} (or 5-cell, 8-cell, 16-cell, 24-cell, 600-cell, "
                         f"120-cell)")
    n, edges = _phys.polytope_graph(kind)
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return n, edges, adj


def numbers(path):
    return [int(t) for t in " ".join(l.split("#")[0] for l in open(path, encoding="ascii", errors="replace")).split()]


def vertex_set(path, n):
    v = numbers(path)
    if any(not 0 <= x < n for x in v) or len(set(v)) != len(v):
        raise ValueError(f"the vertices must be distinct numbers 0..{n - 1}")
    return v


def bfs(adj, s):
    d = [-1] * len(adj)
    d[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if d[w] < 0:
                d[w] = d[u] + 1
                q.append(w)
    return d


def force(adj, black):
    black = set(black)
    active = deque(black)
    while active:
        u = active.popleft()
        if u not in black:
            continue
        white = [w for w in adj[u] if w not in black]
        if len(white) == 1:
            w = white[0]
            black.add(w)
            active.append(w)
            active.extend(x for x in adj[w] if x in black)
    return black


def zero_forcing(n, edges, adj, path):
    z = vertex_set(path, n)
    b = force(adj, z)
    if len(b) < n:
        return None, f"{n - len(b)} vertices stay white"
    return len(z), f"{len(z)} vertices force all {n}"


def power_domination(n, edges, adj, path):
    s = vertex_set(path, n)
    obs = set(s)
    for v in s:
        obs |= adj[v]
    b = force(adj, obs)
    if len(b) < n:
        return None, f"{n - len(b)} vertices are not observed"
    return len(s), f"{len(s)} vertices observe all {n}"


def locating_dom(n, edges, adj, path):
    d = set(vertex_set(path, n))
    seen = {}
    for v in range(n):
        if v in d:
            continue
        key = frozenset(adj[v] & d)
        if not key:
            return None, f"vertex {v} has no neighbour in the set"
        if key in seen:
            return None, f"vertices {seen[key]} and {v} have the same neighbours in the set"
        seen[key] = v
    return len(d), f"{len(d)} vertices locate and dominate all {n}"


def induced_matching(n, edges, adj, path):
    v = numbers(path)
    if len(v) % 2:
        raise ValueError("an odd number of vertex numbers")
    m = [(v[i], v[i + 1]) for i in range(0, len(v), 2)]
    used = set()
    for a, b in m:
        if not (0 <= a < n and 0 <= b < n) or b not in adj[a]:
            return None, f"{a} {b} is not an edge"
        if a in used or b in used:
            return None, f"the edges are not disjoint at {a} {b}"
        used |= {a, b}
    owner = {}
    for i, (a, b) in enumerate(m):
        owner[a] = owner[b] = i
    for i, (a, b) in enumerate(m):
        for x in (a, b):
            for y in adj[x]:
                if y in owner and owner[y] != i:
                    return None, f"the edge {x} {y} joins two matching edges"
    return len(m), f"{len(m)} edges, pairwise at distance at least 2 (an induced matching)"


def burning(n, edges, adj, path):
    seq = vertex_set(path, n)
    k = len(seq)
    burnt = set()
    for i, v in enumerate(seq, 1):
        d = bfs(adj, v)
        burnt |= {u for u in range(n) if 0 <= d[u] <= k - i}
    if len(burnt) < n:
        return None, f"{n - len(burnt)} vertices are not burnt after {k} rounds"
    return k, f"the sequence burns all {n} vertices in {k} rounds"


def l21(n, edges, adj, path):
    f = numbers(path)
    if len(f) != n or min(f) < 0:
        raise ValueError(f"expected {n} non-negative labels")
    for a, b in edges:
        if abs(f[a] - f[b]) < 2:
            return None, f"adjacent vertices {a} and {b} have labels {f[a]} and {f[b]}"
    for v in range(n):
        for a in adj[v]:
            for b in adj[v]:
                if a < b and b not in adj[a] and f[a] == f[b]:
                    return None, f"vertices {a} and {b} at distance 2 share the label {f[a]}"
    return max(f), f"an L(2,1)-labelling of all {n} vertices with span {max(f)}"


def bandwidth(n, edges, adj, path):
    order = numbers(path)
    if sorted(order) != list(range(n)):
        raise ValueError(f"expected every vertex 0..{n - 1} exactly once")
    pos = {v: i for i, v in enumerate(order)}
    w = max(abs(pos[a] - pos[b]) for a, b in edges)
    return w, f"a numbering of the {n} vertices with bandwidth {w}"


def bisection(n, edges, adj, path):
    s = numbers(path)
    if len(s) != n or any(x not in (0, 1) for x in s) or abs(2 * sum(s) - n) > 1:
        raise ValueError(f"expected {n} bits, as many 0s as 1s (one more of either when {n} is odd)")
    cut = sum(1 for a, b in edges if s[a] != s[b])
    return cut, f"two halves of {n // 2} vertices with {cut} edges between them"


def resolving(n, edges, adj, path):
    w = vertex_set(path, n)
    dist = [bfs(adj, x) for x in w]
    seen = {}
    for v in range(n):
        key = tuple(d[v] for d in dist)
        if key in seen:
            return None, f"vertices {seen[key]} and {v} have the same distances to the set"
        seen[key] = v
    return len(w), f"{len(w)} vertices resolve all {n}"


def ising(n, edges, adj, path):
    txt = "".join(l.split("#")[0] for l in open(path, encoding="ascii", errors="replace"))
    import re
    toks = re.findall(r"[+-]?1|[+-]", txt)
    if len(toks) != n or re.sub(r"[+-]?1|[+-]|\s", "", txt):
        raise ValueError(f"expected {n} spins, + or - (or 1 and -1)")
    sp = [-1 if t.startswith("-") else 1 for t in toks]
    e = sum(sp[a] * sp[b] for a, b in edges)
    return e, f"{n} spins, {sum(1 for a, b in edges if sp[a] == sp[b])} of {len(edges)} edges frustrated, energy {e}"


def domination(n, edges, adj, path):
    d = set(vertex_set(path, n))
    bad = next((v for v in range(n) if v not in d and not adj[v] & d), None)
    if bad is not None:
        return None, f"vertex {bad} is not dominated"
    return len(d), f"{len(d)} vertices dominate all {n}"


def independent(n, edges, adj, path):
    d = set(vertex_set(path, n))
    for v in d:
        if adj[v] & d:
            return None, f"vertices {v} and {min(adj[v] & d)} of the set are adjacent"
    return len(d), f"{len(d)} pairwise non-adjacent vertices"


def total_dom(n, edges, adj, path):
    d = set(vertex_set(path, n))
    bad = next((v for v in range(n) if not adj[v] & d), None)
    if bad is not None:
        return None, f"vertex {bad} has no neighbour in the set"
    return len(d), f"{len(d)} vertices totally dominate all {n}"


def independent_dom(n, edges, adj, path):
    d = set(vertex_set(path, n))
    for v in d:
        if adj[v] & d:
            return None, f"vertices {v} and {min(adj[v] & d)} of the set are adjacent"
    bad = next((v for v in range(n) if v not in d and not adj[v] & d), None)
    if bad is not None:
        return None, f"vertex {bad} is not dominated"
    return len(d), f"{len(d)} independent vertices dominate all {n}"


def induced_bipartite(n, edges, adj, path):
    s = "".join("".join(l.split("#")[0].split()) for l in open(path, encoding="ascii", errors="replace"))
    if len(s) != n or any(c not in "01." for c in s):
        raise ValueError(f"expected {n} characters 0, 1 or .")
    for a, b in edges:
        if s[a] != "." and s[a] == s[b]:
            return None, f"the edge {a} {b} joins two chosen vertices on side {s[a]}"
    k = sum(c != "." for c in s)
    return k, f"{k} vertices inducing a bipartite subgraph (sides {s.count('0')} and {s.count('1')})"


def distance2_colouring(n, edges, adj, path):
    c = numbers(path)
    if len(c) != n or min(c) < 0:
        raise ValueError(f"expected {n} non-negative colours")
    for v in range(n):
        near = adj[v] | {w for u in adj[v] for w in adj[u]}
        near.discard(v)
        clash = next((w for w in near if c[w] == c[v]), None)
        if clash is not None:
            return None, f"vertices {v} and {clash} at distance at most 2 share the colour {c[v]}"
    k = len(set(c))
    return k, f"a colouring of the square of the graph with {k} colours"


def max_leaf(n, edges, adj, path):
    v = numbers(path)
    if len(v) != 2 * (n - 1):
        raise ValueError(f"expected {n - 1} edges")
    tree = [(v[i], v[i + 1]) for i in range(0, len(v), 2)]
    parent = list(range(n))
    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    deg = [0] * n
    for a, b in tree:
        if not (0 <= a < n and 0 <= b < n) or b not in adj[a]:
            return None, f"{a} {b} is not an edge"
        ra, rb = root(a), root(b)
        if ra == rb:
            return None, f"the edge {a} {b} closes a cycle"
        parent[ra] = rb
        deg[a] += 1
        deg[b] += 1
    leaves = sum(1 for x in deg if x == 1)
    return leaves, f"a spanning tree with {leaves} leaves"


def code(n, edges, adj, path, d):
    c = vertex_set(path, n)
    for i, v in enumerate(c):
        dist = bfs(adj, v)
        close = next((w for w in c[i + 1:] if dist[w] < d), None)
        if close is not None:
            return None, f"vertices {v} and {close} are at distance {dist[close]} < {d}"
    return len(c), f"{len(c)} vertices pairwise at distance at least {d}"


def colours(path, n):
    c = numbers(path)
    if len(c) != n or min(c) < 0:
        raise ValueError(f"expected {n} non-negative colours")
    return c


def proper(edges, c):
    return next(((a, b) for a, b in edges if c[a] == c[b]), None)


def roman(n, edges, adj, path):
    f = numbers(path)
    if len(f) != n or any(x not in (0, 1, 2) for x in f):
        raise ValueError(f"expected {n} values 0, 1 or 2")
    bad = next((v for v in range(n) if f[v] == 0 and not any(f[w] == 2 for w in adj[v])), None)
    if bad is not None:
        return None, f"vertex {bad} has value 0 and no neighbour with value 2"
    return sum(f), f"a Roman dominating function of weight {sum(f)}"


def two_domination(n, edges, adj, path):
    d = set(vertex_set(path, n))
    bad = next((v for v in range(n) if v not in d and len(adj[v] & d) < 2), None)
    if bad is not None:
        return None, f"vertex {bad} has fewer than two neighbours in the set"
    return len(d), f"{len(d)} vertices 2-dominate all {n}"


def grundy(n, edges, adj, path):
    c = colours(path, n)
    e = proper(edges, c)
    if e:
        return None, f"the edge {e[0]} {e[1]} is monochromatic"
    if min(c) < 1:
        raise ValueError("colours start at 1")
    for v in range(n):
        seen = {c[w] for w in adj[v]}
        miss = next((k for k in range(1, c[v]) if k not in seen), None)
        if miss is not None:
            return None, f"vertex {v} has colour {c[v]} but no neighbour of colour {miss}"
    k = len(set(c))
    if sorted(set(c)) != list(range(1, k + 1)):
        return None, "the colours are not 1..k"
    return k, f"a Grundy colouring with {k} colours"


def b_colouring(n, edges, adj, path):
    c = colours(path, n)
    e = proper(edges, c)
    if e:
        return None, f"the edge {e[0]} {e[1]} is monochromatic"
    k = set(c)
    for x in k:
        if not any(c[v] == x and {c[w] for w in adj[v]} >= k - {x} for v in range(n)):
            return None, f"colour {x} has no vertex adjacent to all the other colours"
    return len(k), f"a b-colouring with {len(k)} colours"


def linear_arrangement(n, edges, adj, path):
    order = numbers(path)
    if sorted(order) != list(range(n)):
        raise ValueError(f"expected every vertex 0..{n - 1} exactly once")
    pos = {v: i for i, v in enumerate(order)}
    w = sum(abs(pos[a] - pos[b]) for a, b in edges)
    return w, f"a numbering of the {n} vertices with total edge length {w}"


def strong_edge(n, edges, adj, path):
    v = numbers(path)
    if len(v) != 3 * len(edges):
        raise ValueError(f"expected {len(edges)} lines 'u v c'")
    col = {}
    for i in range(0, len(v), 3):
        a, b, k = v[i:i + 3]
        if not (0 <= a < n and 0 <= b < n) or b not in adj[a] or k < 0:
            return None, f"{a} {b} is not an edge (or its colour is negative)"
        e = (min(a, b), max(a, b))
        if e in col:
            return None, f"the edge {a} {b} is listed twice"
        col[e] = k
    at = {}
    for (a, b), k in col.items():
        for x in (a, b):
            at.setdefault((x, k), []).append((a, b))
    for (a, b), k in col.items():
        near = set()
        for x in (a, b):
            for y in adj[x] | {x}:
                near.update(at.get((y, k), []))
        near.discard((a, b))
        if near:
            return None, f"the edges {(a, b)} and {min(near)} of colour {k} are at distance less than 2"
    k = len(set(col.values()))
    return k, f"a strong edge colouring with {k} colours"


def domatic(n, edges, adj, path):
    c = colours(path, n)
    for x in set(c):
        cls = {v for v in range(n) if c[v] == x}
        bad = next((v for v in range(n) if v not in cls and not adj[v] & cls), None)
        if bad is not None:
            return None, f"class {x} does not dominate vertex {bad}"
    k = len(set(c))
    return k, f"a partition into {k} dominating sets"


PROBLEMS = {"ising": ising, "domination": domination, "independent": independent, "roman": roman, "2-domination": two_domination, "grundy": grundy, "b-colouring": b_colouring,
            "linear-arrangement": linear_arrangement, "strong-edge": strong_edge, "domatic": domatic,
            "total-dom": total_dom, "independent-dom": independent_dom, "induced-bipartite": induced_bipartite,
            "distance2-colouring": distance2_colouring, "max-leaf": max_leaf, "resolving": resolving, "zero-forcing": zero_forcing, "power-domination": power_domination, "locating-dom": locating_dom,
            "induced-matching": induced_matching, "burning": burning, "l21": l21, "bandwidth": bandwidth,
            "bisection": bisection}


def main():
    if not ((len(sys.argv) == 4 and sys.argv[1] in PROBLEMS) or (len(sys.argv) == 5 and sys.argv[1] == "code")):
        print(__doc__)
        return 2
    try:
        n, edges, adj = graph(sys.argv[2])
        if sys.argv[1] == "code":
            d = int(sys.argv[3])
            if d < 2:
                raise ValueError("D must be at least 2")
            value, msg = code(n, edges, adj, sys.argv[4], d)
        else:
            value, msg = PROBLEMS[sys.argv[1]](n, edges, adj, sys.argv[3])
    except (ValueError, OSError) as e:
        print(f"unreadable certificate: {e}")
        return 1
    if value is None:
        print(f"not valid: {msg}")
        return 1
    print(f"polytope {sys.argv[2]}: {msg}")
    print(f"RESULT {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
