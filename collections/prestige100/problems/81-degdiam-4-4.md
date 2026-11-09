# 81. Largest graph of maximum degree 4 and diameter 4

Family: Degree-diameter problem. Benchmark problem: `degdiam-4-4`.

**Best known:** 104 vertices, N. Bhakar (Aug 2026). Also known: the Moore bound 161.

**To beat it:** a graph with maximum degree 4 and diameter at most 4 on more than 104 vertices.

**Keeper:** [The (Degree, Diameter) Problem for Graphs (F. Comellas)](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), read 2026-11-09 15:51 +04 (last changed 4 Nov 2026). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a graph with maximum degree at most 4 and diameter at most 4, with as many vertices n as possible; it shows N(4,4) >= n. The largest known such graph, by Bhakar (Aug 2026), has 104 vertices; a graph with more vertices improves it.

## Why it matters

The (4,4) entry rose from 98 (Exoo 2010) to 104 in August 2026, far below the Moore bound of 161 (Comellas's table, last changed 4 Nov 2026). The degree-diameter problem models networks with few links per node and short routes, and its table has been kept since 1995.

Sources: [F. Comellas, table of the largest known (Δ,D)-graphs](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1985-12 | lower | 95 | C. Delorme | Delorme, C. (1985). Grands graphes de degré et diametre donnés. European Journal of Combinatorics, 6(4), 291-302. (via Leaps in Bounds) |
| 2001-05-25 | lower | 96 | G. Exoo | Exoo, G. (2001). A family of graphs and the degree/diameter problem. Journal of Graph Theory, 37(2), 118-124. (via Leaps in Bounds) |
| 2010-05-19 | lower | 98 | G. Exoo | Geoffrey Exoo, communicated to F. Comellas on May 19, 2010, as listed in the archived table of largest known (Δ,D)-graphs. (via Leaps in Bounds) |
| 2026-08 | lower | 104 | N. Bhakar | Nishant Bhakar in August 2026 (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one graph in graph6 or sparse6 (as House of Graphs gives them; an optional >>graph6<< or >>sparse6<< header is allowed), or an edge list, one edge "u v" per line, vertices numbered from 0.

Score: n, the number of vertices of a graph with maximum degree at most 4 and diameter at most 4 (larger is better).

```
python3 -I obb.py check degdiam-4-4 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/degdiam_check.py 4 4 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
