"""Exact check of a counterexample to Erdos problem #993 (standard library only).

  python3 -I tree_unimodal_check.py FILE

Alavi, Malde, Schwenk and Erdos (1987) asked whether the independent set sequence i_0, i_1, i_2, ... of every tree or
forest is unimodal, where i_k counts the independent sets of k vertices. FILE holds a forest as an edge list, one edge
"u v" per line with vertices numbered 0..n-1 (an optional first line "n N" sets the number of vertices, so that
isolated vertices can be included). The checker refuses loops, repeated edges and cycles, computes the independence
polynomial of every component exactly (rooted dynamic programme with integer polynomials: I_in(v) = x * prod I_out(c)
and I_out(v) = prod (I_in(c) + I_out(c)) over the children c) and multiplies them. The sequence is unimodal when it
never rises again after it has fallen. Prints n, the length of the sequence and the first place it rises after a fall;
for a sequence that is not unimodal prints "RESULT 1" and exits 0 (a counterexample), otherwise exits 1."""
import sys


def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def padd(a, b):
    if len(a) < len(b):
        a, b = b, a
    out = list(a)
    for i, y in enumerate(b):
        out[i] += y
    return out


def independence_polynomial(n, adj):
    """Coefficients i_0, i_1, ... of the independence polynomial of a forest."""
    total = [1]
    seen = [False] * n
    for root in range(n):
        if seen[root]:
            continue
        order, parent = [root], {root: -1}
        seen[root] = True
        k = 0
        while k < len(order):
            v = order[k]
            k += 1
            for w in adj[v]:
                if not seen[w]:
                    seen[w] = True
                    parent[w] = v
                    order.append(w)
        p_in, p_out = {}, {}
        for v in reversed(order):
            a, b = [0, 1], [1]
            for w in adj[v]:
                if parent.get(w) == v:
                    a = pmul(a, p_out[w])
                    b = pmul(b, padd(p_in[w], p_out[w]))
            p_in[v], p_out[v] = a, b
        total = pmul(total, padd(p_in[root], p_out[root]))
    while len(total) > 1 and total[-1] == 0:
        total.pop()
    return total


def first_rise_after_fall(seq):
    """The index k with seq[k] > seq[k-1] after some earlier strict fall, or None (unimodal)."""
    fallen = False
    for k in range(1, len(seq)):
        if seq[k] < seq[k - 1]:
            fallen = True
        elif seq[k] > seq[k - 1] and fallen:
            return k
    return None


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    n, edges = None, []
    for line in open(sys.argv[1], encoding="ascii", errors="replace"):
        s = line.split("#")[0].replace(",", " ").split()
        if not s:
            continue
        if s[0] == "n" and len(s) == 2 and n is None and not edges:
            n = int(s[1])
            continue
        if len(s) != 2:
            print(f"not an edge: {line.strip()[:60]!r}")
            return 1
        try:
            edges.append((int(s[0]), int(s[1])))
        except ValueError:
            print(f"vertices must be integers: {line.strip()[:60]!r}")
            return 1
    if n is None:
        n = 1 + max((max(e) for e in edges), default=-1)
    adj = [[] for _ in range(n)]
    seen_edges = set()
    root = list(range(n))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n) or u == v:
            print(f"edge ({u}, {v}) is a loop or leaves the vertex range 0..{n - 1}")
            return 1
        key = (min(u, v), max(u, v))
        if key in seen_edges:
            print(f"edge {key} is repeated")
            return 1
        seen_edges.add(key)
        ru, rv = find(u), find(v)
        if ru == rv:
            print(f"edge ({u}, {v}) closes a cycle: not a forest")
            return 1
        root[ru] = rv
        adj[u].append(v)
        adj[v].append(u)
    seq = independence_polynomial(n, adj)
    k = first_rise_after_fall(seq)
    print(f"forest on {n} vertices, {len(edges)} edges; independence number {len(seq) - 1}")
    if k is None:
        print("the independent set sequence is unimodal: not a counterexample")
        return 1
    print(f"the sequence falls and then rises again at k = {k}: i_{k - 1} = {seq[k - 1]} < i_{k} = {seq[k]}")
    print("RESULT 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
