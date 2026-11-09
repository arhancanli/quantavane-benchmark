# 80. Largest graph of maximum degree 4 and diameter 3

Family: Degree-diameter problem. Benchmark problem: `degdiam-4-3`.

**Best known:** 41 vertices, J. Allwright (1992). Also known: the Moore bound 53.

**To beat it:** a graph with maximum degree 4 and diameter at most 3 on more than 41 vertices.

**Keeper:** [The (Degree, Diameter) Problem for Graphs (F. Comellas)](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), read 2026-11-09 15:51 +04 (last changed 4 Nov 2026). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a graph with maximum degree at most 4 and diameter at most 3, with as many vertices n as possible; it shows N(4,3) >= n. The largest known such graph, by Allwright (1992), has 41 vertices; a graph with more vertices improves it.

## Why it matters

The largest known 4-regular graph of diameter 3 has 41 vertices (Allwright 1992), far below the Moore bound of 53 (Comellas's table, last changed 4 Nov 2026). The degree-diameter problem models networks with few links per node and short routes, and its table has been kept since 1995.

Sources: [F. Comellas, table of the largest known (Δ,D)-graphs](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1985-12 | lower | 40 | C. Delorme | Delorme, C. (1985). Grands graphes de degré et diametre donnés. European Journal of Combinatorics, 6(4), 291-302. (via Leaps in Bounds) |
| 1992-07-15 | lower | 41 | J. Allwright | Allwright, J. (1992). New (Δ, D) graphs discovered by heuristic search. Discrete Applied Mathematics, 37, 3-8. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one graph in graph6 or sparse6 (as House of Graphs gives them; an optional >>graph6<< or >>sparse6<< header is allowed), or an edge list, one edge "u v" per line, vertices numbered from 0.

Score: n, the number of vertices of a graph with maximum degree at most 4 and diameter at most 3 (larger is better).

```
python3 -I obb.py check degdiam-4-3 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/degdiam_check.py 4 3 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 41 | Allwright (1992) (certificate from Leaps in Bounds, MIT) | record | 2026-11-08 | certs/lib_degree-diameter-4-3-lower-41.s6 (72f1be69af43...) |
