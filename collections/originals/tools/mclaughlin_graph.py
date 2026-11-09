"""The McLaughlin graph and its two subconstituents as coupling matrices (our own code, Quantavane Originals, problem
mclaughlin-ising).

  python3 -I mclaughlin_graph.py OUT.J [gq|local]

The extended binary Golay code is built from its generator matrix [I | B]; its octads through the point 0, with 0
removed, are the 253 heptads of the Steiner system S(4,7,23) on the points 1..23. Brouwer's 22 + 77 + 176
construction: the points 2..23 (a coclique), the 77 heptads through 1 and the 176 heptads avoiding 1 (sorted); a
point is adjacent to the heptads through 1 that miss it and to the heptads avoiding 1 that contain it; two heptads of
the same kind are adjacent when they meet in one point, a heptad through 1 and one avoiding it when they meet in three
points. The result is checked to be strongly regular with parameters (275, 112, 30, 56). OUT.J is the input of
tools/src/ising.c: n, then the n x n 0/1 adjacency matrix (antiferromagnetic couplings). With gq or local, only the
neighbours (112 vertices, the collinearity graph of GQ(3,9)) or the non-neighbours (162, the local McLaughlin graph)
of vertex 0 are kept. The vertex order is that of mclaughlin_graph in checkers/orig_phys.py."""
import sys

B = ["110111000101", "101110001011", "011100010111", "111000101101", "110001011011", "100010110111",
     "000101101111", "001011011101", "010110111001", "101101110001", "011011100011", "111111111110"]


def heptads():
    rows = [(1 << (23 - i)) | int(B[i], 2) for i in range(12)]
    words = set()
    for mask in range(1 << 12):
        w = 0
        for i in range(12):
            if mask >> i & 1:
                w ^= rows[i]
        if bin(w).count("1") == 8:
            words.add(w)
    octads = [frozenset(23 - j for j in range(24) if w >> j & 1) for w in words]
    assert len(octads) == 759
    hept = sorted(tuple(sorted(o - {0})) for o in octads if 0 in o)
    assert len(hept) == 253
    return hept


def graph():
    hept = heptads()
    verts = [("p", q) for q in range(2, 24)] + [("B", set(h)) for h in hept if 1 in h] + \
            [("C", set(h)) for h in hept if 1 not in h]
    n = len(verts)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        ti, a = verts[i]
        for j in range(i + 1, n):
            tj, b = verts[j]
            if ti == "p" and tj == "p":
                continue
            if ti == "p":
                ok = (a not in b) if tj == "B" else (a in b)
            else:
                k = len(a & b)
                ok = (k == 1) if ti == tj else (k == 3)
            if ok:
                A[i][j] = A[j][i] = 1
    return A


def main():
    A = graph()
    n = len(A)
    assert {sum(r) for r in A} == {112}
    for i in range(n):
        for j in range(i + 1, n):
            common = sum(a & b for a, b in zip(A[i], A[j]))
            assert common == (30 if A[i][j] else 56)
    keep = list(range(n))
    if len(sys.argv) > 2:
        keep = [j for j in range(n) if A[0][j]] if sys.argv[2] == "gq" else [j for j in range(1, n) if not A[0][j]]
    with open(sys.argv[1], "w") as f:
        f.write(f"{len(keep)}\n")
        for i in keep:
            f.write(" ".join(str(A[i][j]) for j in keep) + "\n")
    print(f"{len(keep)} vertices, {sum(A[i][j] for i in keep for j in keep) // 2} edges; srg(275, 112, 30, 56) checked")


if __name__ == "__main__":
    main()
