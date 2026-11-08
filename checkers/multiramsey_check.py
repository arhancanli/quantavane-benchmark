"""Exact check of an edge colouring of K_n for a multicolour Ramsey number R(S_1, ..., S_r) (standard library only).

  python3 -I multiramsey_check.py S_1 S_2 ... S_r FILE

FILE holds the n x n colour matrix, one line of n characters per vertex: the character in row i, column j (i != j) is
the colour of the edge {i, j}, a digit from 0 to r-1, and the matrix must be symmetric; diagonal characters are
ignored (write 0 or -). Colour c (counted from 0) must hold no complete graph K_{S_{c+1}}. A colouring of K_n with
none shows R(S_1, ..., S_r) > n. Each colour class is searched for its forbidden clique by branch and bound on bit
sets, written apart from ramsey_check.c: at each node it branches only on the candidates that are not neighbours of a
pivot (the candidate with the most neighbours among the candidates) and stops when the clique so far plus the number
of colours a greedy colouring of the candidates needs cannot reach the size sought; triangles are found directly
from common neighbours. Prints n and, for each colour, that its clique is absent, then "RESULT n"; exits 0 for a
valid colouring, 1 otherwise."""
import sys

sys.setrecursionlimit(10000)


def find_clique(adj, n, want):
    """A list of `want` vertices forming a clique in the graph with neighbour bit sets adj, or None."""
    if want <= 1:
        return [0] if n else None
    if want == 2:
        for v in range(n):
            if adj[v]:
                return [v, (adj[v] & -adj[v]).bit_length() - 1]
        return None
    if want == 3:
        for v in range(n):
            higher = adj[v] >> (v + 1) << (v + 1)
            rest = higher
            while rest:
                u = (rest & -rest).bit_length() - 1
                rest &= rest - 1
                common = higher & adj[u]
                if common:
                    return [v, u, (common & -common).bit_length() - 1]
        return None
    clique = []

    def colours(cand, enough):
        k, left = 0, cand
        while left and k < enough:
            k += 1
            avail = left
            while avail:
                low = avail & -avail
                v = low.bit_length() - 1
                left &= ~low
                avail &= ~low & ~adj[v]
        return k

    def search(cand, need):
        if need == 0:
            return True
        if bin(cand).count("1") < need or colours(cand, need) < need:
            return False
        if need == 1:
            clique.append((cand & -cand).bit_length() - 1)
            return True
        pivot, most, scan = -1, -1, cand
        while scan:
            v = (scan & -scan).bit_length() - 1
            scan &= scan - 1
            c = bin(cand & adj[v]).count("1")
            if c > most:
                pivot, most = v, c
        branch = cand & ~adj[pivot]
        while branch:
            low = branch & -branch
            v = low.bit_length() - 1
            branch &= branch - 1
            clique.append(v)
            if search(cand & adj[v], need - 1):
                return True
            clique.pop()
            cand &= ~low
            if bin(cand).count("1") < need:
                return False
        return False

    return clique if search((1 << n) - 1, want) else None


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    sizes = [int(x) for x in sys.argv[1:-1]]
    r = len(sizes)
    if r > 10 or min(sizes) < 2:
        print("between 2 and 10 colours, each clique size at least 2")
        return 2
    rows = [line.strip() for line in open(sys.argv[-1], encoding="ascii", errors="replace")
            if line.strip() and not line.lstrip().startswith("#")]
    n = len(rows)
    if n == 0 or any(len(row) != n for row in rows):
        print(f"{n} rows of lengths {sorted(set(len(row) for row in rows))}: not an n x n matrix")
        return 1
    digits = "0123456789"[:r]
    adj = [[0] * n for _ in range(r)]
    for i in range(n):
        row = rows[i]
        for j in range(n):
            if i == j:
                continue
            ch = row[j]
            if ch not in digits:
                print(f"entry ({i},{j}) is {ch!r}, not a colour from 0 to {r - 1}")
                return 1
            if rows[j][i] != ch:
                print(f"not symmetric at ({i},{j})")
                return 1
            adj[int(ch)][i] |= 1 << j
    for c in range(r):
        found = find_clique(adj[c], n, sizes[c])
        if found is not None:
            print(f"colour {c} holds a K_{sizes[c]}: vertices {' '.join(map(str, sorted(found)))}")
            return 1
        print(f"colour {c}: no K_{sizes[c]}")
    print(f"n {n} colours {r}: no colour c holds K_(S_c), so R({','.join(map(str, sizes))}) > {n}")
    print(f"RESULT {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
