# 79. Largest graph of maximum degree 3 and diameter 6

Family: Degree-diameter problem. Benchmark problem: `degdiam-3-6`.

**Best known:** 132 vertices, G. Exoo (1998). Also known: the Moore bound 190.

**To beat it:** a graph with maximum degree 3 and diameter at most 6 on more than 132 vertices.

**Keeper:** [The (Degree, Diameter) Problem for Graphs (F. Comellas)](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), read 2026-11-09 15:51 +04 (last changed 4 Nov 2026). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a graph with maximum degree at most 3 and diameter at most 6, with as many vertices n as possible; it shows N(3,6) >= n. The largest known such graph, by Exoo (1998), has 132 vertices; a graph with more vertices improves it.

## Why it matters

The largest known cubic graph of diameter 6 has 132 vertices, Exoo's 1998 graph, far below the Moore bound of 190 (Comellas's table, last changed 4 Nov 2026). The degree-diameter problem models networks with few links per node and short routes, and its table has been kept since 1995.

Sources: [F. Comellas, table of the largest known (Δ,D)-graphs](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1985-12 | lower | 128 | C. Delorme | Delorme, C. (1985). Grands graphes de degré et diametre donnés. European Journal of Combinatorics, 6(4), 291-302. (via Leaps in Bounds) |
| 1993-04-28 | lower | 130 | J. Gómez, M. A. Fiol and O. Serra | Gómez, J., Fiol, M. A., & Serra, O. (1993). On large (Δ, D)-graphs. Discrete Mathematics, 114(1-3), 219-235. (via Leaps in Bounds) |
| 1998-05-22 | lower | 132 | G. Exoo | Geoffrey Exoo, communicated to F. Comellas on May 22, 1998. Construction in G. Exoo, A family of graphs and the degree/diameter problem, J. Graph Theory 37 (2001), 118-124. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one graph in graph6 or sparse6 (as House of Graphs gives them; an optional >>graph6<< or >>sparse6<< header is allowed), or an edge list, one edge "u v" per line, vertices numbered from 0.

Score: n, the number of vertices of a graph with maximum degree at most 3 and diameter at most 6 (larger is better).

```
python3 -I obb.py check degdiam-3-6 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/degdiam_check.py 3 6 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
