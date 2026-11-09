# 82. Largest graph of maximum degree 5 and diameter 3

Family: Degree-diameter problem. Benchmark problem: `degdiam-5-3`.

**Best known:** 72 vertices, G. Exoo (2001). Also known: the Moore bound 106.

**To beat it:** a graph with maximum degree 5 and diameter at most 3 on more than 72 vertices.

**Keeper:** [The (Degree, Diameter) Problem for Graphs (F. Comellas)](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), read 2026-11-09 15:51 +04 (last changed 4 Nov 2026). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a graph with maximum degree at most 5 and diameter at most 3, with as many vertices n as possible; it shows N(5,3) >= n. The largest known such graph, by Exoo (2001), has 72 vertices; a graph with more vertices improves it.

## Why it matters

The largest known 5-regular graph of diameter 3 has 72 vertices (Exoo 2001), far below the Moore bound of 106 (Comellas's table, last changed 4 Nov 2026). The degree-diameter problem models networks with few links per node and short routes, and its table has been kept since 1995.

Sources: [F. Comellas, table of the largest known (Δ,D)-graphs](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1985-12 | lower | 60 | C. Delorme | Delorme, C. (1985). Grands graphes de degré et diametre donnés. European Journal of Combinatorics, 6(4), 291-302. (via Leaps in Bounds) |
| 1995-02 | lower | 70 | F. Comellas and C. Delorme (table) | Comellas, F., & Delorme, C. Table of largest known (Δ,D)-graphs, version of February 1995 (archived December 1, 1996). (via Leaps in Bounds) |
| 2001-05-25 | lower | 72 | G. Exoo | Exoo, G. (2001). A family of graphs and the degree/diameter problem. Journal of Graph Theory, 37(2), 118-124. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one graph in graph6 or sparse6 (as House of Graphs gives them; an optional >>graph6<< or >>sparse6<< header is allowed), or an edge list, one edge "u v" per line, vertices numbered from 0.

Score: n, the number of vertices of a graph with maximum degree at most 5 and diameter at most 3 (larger is better).

```
python3 -I obb.py check degdiam-5-3 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/degdiam_check.py 5 3 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
