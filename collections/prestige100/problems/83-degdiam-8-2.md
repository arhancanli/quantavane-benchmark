# 83. Largest graph of maximum degree 8 and diameter 2

Family: Degree-diameter problem. Benchmark problem: `degdiam-8-2`.

**Best known:** 57 vertices, R. M. Storwick (1970). Also known: the Moore bound 65.

**To beat it:** a graph with maximum degree 8 and diameter at most 2 on more than 57 vertices.

**Keeper:** [The (Degree, Diameter) Problem for Graphs (F. Comellas)](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), read 2026-11-09 15:51 +04 (last changed 4 Nov 2026). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a graph with maximum degree at most 8 and diameter at most 2, with as many vertices n as possible; it shows N(8,2) >= n. The largest known such graph, by Storwick (1970), has 57 vertices; a graph with more vertices improves it.

## Why it matters

For degree 8 and diameter 2 the Moore bound is 65 and no graph larger than Storwick's 57 vertices from 1970 is known, far below the Moore bound of 65 (Comellas's table, last changed 4 Nov 2026). The degree-diameter problem models networks with few links per node and short routes, and its table has been kept since 1995.

Sources: [F. Comellas, table of the largest known (Δ,D)-graphs](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1970-12-31 | lower | 57 | R. M. Storwick | Storwick, R. M. (1970). Improved construction techniques for (d, k) graphs. IEEE Transactions on Computers, 100(12), 1214-1216. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one graph in graph6 or sparse6 (as House of Graphs gives them; an optional >>graph6<< or >>sparse6<< header is allowed), or an edge list, one edge "u v" per line, vertices numbered from 0.

Score: n, the number of vertices of a graph with maximum degree at most 8 and diameter at most 2 (larger is better).

```
python3 -I obb.py check degdiam-8-2 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/degdiam_check.py 8 2 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 57 | Storwick (1970) (certificate from Leaps in Bounds, MIT) | record | 2026-11-08 | certs/lib_degree-diameter-8-2-lower-57.s6 (f14a5ac69f47...) |
