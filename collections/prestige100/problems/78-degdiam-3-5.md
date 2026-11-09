# 78. Largest graph of maximum degree 3 and diameter 5

Family: Degree-diameter problem. Benchmark problem: `degdiam-3-5`.

**Best known:** 70 vertices, C. von Conta (1983); I. Alegre, M. A. Fiol and J. L. A. Yebra (1986). Also known: the Moore bound 94.

**To beat it:** a graph with maximum degree 3 and diameter at most 5 on more than 70 vertices.

**Keeper:** [The (Degree, Diameter) Problem for Graphs (F. Comellas)](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), read 2026-11-09 15:51 +04 (last changed 4 Nov 2026). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a graph with maximum degree at most 3 and diameter at most 5, with as many vertices n as possible; it shows N(3,5) >= n. The largest known such graph, by von Conta (1983), has 70 vertices; a graph with more vertices improves it.

## Why it matters

The largest known cubic graph of diameter 5 has 70 vertices and has stood since the 1980s, far below the Moore bound of 94 (Comellas's table, last changed 4 Nov 2026). The degree-diameter problem models networks with few links per node and short routes, and its table has been kept since 1995.

Sources: [F. Comellas, table of the largest known (Δ,D)-graphs](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1983-07 | lower | 70 | C. von Conta | von Conta, C. (1983). Torus and other networks as communication networks with up to some hundred points. IEEE Transactions on Computers, C-32(7), 657-666. (via Leaps in Bounds) |
| 1986 | lower | 70 | I. Alegre, M. A. Fiol and J. L. A. Yebra | Alegre, I., Fiol, M. A., & Yebra, J. L. A. (1986). Some large graphs with given degree and diameter. Journal of graph theory, 10(2), 219-224. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one graph in graph6 or sparse6 (as House of Graphs gives them; an optional >>graph6<< or >>sparse6<< header is allowed), or an edge list, one edge "u v" per line, vertices numbered from 0.

Score: n, the number of vertices of a graph with maximum degree at most 3 and diameter at most 5 (larger is better).

```
python3 -I obb.py check degdiam-3-5 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/degdiam_check.py 3 5 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
