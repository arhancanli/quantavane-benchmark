"""Hoffman-Singleton graph and odd graphs O_k as coupling matrices for tools/src/ising.c (our own code).

  python3 -I moore_odd.py hs OUT.J            Robertson's construction: pentagons P_{h,j}, pentagrams Q_{i,j}
                                              (h, i, j in Z_5), P_{h,j} ~ P_{h,j+-1}, Q_{i,j} ~ Q_{i,j+-2},
                                              P_{h,j} ~ Q_{i,h*i+j}
  python3 -I moore_odd.py odd K OUT.J         the odd graph O_K: (K-1)-subsets of {0..2K-2}, adjacent when disjoint"""
import itertools
import sys


def hs():
    n = 50
    E = set()
    P = lambda h, j: 5 * h + j
    Q = lambda i, j: 25 + 5 * i + j
    for h in range(5):
        for j in range(5):
            E.add(tuple(sorted((P(h, j), P(h, (j + 1) % 5)))))
            E.add(tuple(sorted((Q(h, j), Q(h, (j + 2) % 5)))))
            for i in range(5):
                E.add(tuple(sorted((P(h, j), Q(i, (h * i + j) % 5)))))
    return n, sorted(E)


def odd(k):
    vs = list(itertools.combinations(range(2 * k - 1), k - 1))
    idx = {v: i for i, v in enumerate(vs)}
    E = [(idx[a], idx[b]) for a, b in itertools.combinations(vs, 2) if not set(a) & set(b)]
    return len(vs), E


def main():
    if sys.argv[1] == "hs":
        n, E = hs()
        out = sys.argv[2]
    else:
        n, E = odd(int(sys.argv[2]))
        out = sys.argv[3]
    deg = [0] * n
    for a, b in E:
        deg[a] += 1
        deg[b] += 1
    J = [[0] * n for _ in range(n)]
    for a, b in E:
        J[a][b] = J[b][a] = 1
    with open(out, "w") as f:
        f.write(f"{n}\n" + "".join(" ".join(map(str, r)) + "\n" for r in J))
    print(n, "vertices", len(E), "edges, degrees", sorted(set(deg)))


if __name__ == "__main__":
    main()
