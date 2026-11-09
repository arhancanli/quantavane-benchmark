# 65. The missing Moore graph (degree 57)

Family: Moore graph and strongly regular graphs. Benchmark problem: `moore-57`.

**Best known:** none known, none.

**To beat it:** a 57-regular graph on 3250 vertices with diameter 2 (equivalently girth 5): a strongly regular graph srg(3250, 57, 0, 1).

**Keeper:** [The (Degree, Diameter) Problem for Graphs (F. Comellas)](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), read 2026-11-09 15:51 +04 (last changed 4 Nov 2026). Also read: [Parameters of strongly regular graphs (A. E. Brouwer)](https://www.win.tue.nl/~aeb/graphs/srg/srgtab.html), 2026-11-09 15:52 +04 (tables for 1-50 and 51-100 vertices).

## The problem

Find a 57-regular graph on 3250 vertices with diameter 2, equivalently a strongly regular graph srg(3250, 57, 0, 1) (girth 5, every two non-adjacent vertices with exactly one common neighbour). Hoffman and Singleton (1960) showed that a Moore graph of diameter 2 has degree 2, 3, 7 or 57; the first three exist and degree 57 is open. A valid graph scores 1.

## Why it matters

Hoffman and Singleton proved in 1960 that a graph of diameter 2 meeting the Moore bound has degree 2, 3, 7 or 57; the first three exist (the pentagon, the Petersen graph and the Hoffman-Singleton graph), and degree 57 has been open for 66 years. Comellas's degree-diameter table still names it as the one possible Moore graph left (read 9 Nov 2026).

Sources: [Hoffman and Singleton, IBM J. Res. Dev. 4 (1960)](https://doi.org/10.1147/rd.45.0497); [F. Comellas, degree-diameter table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1960 | - | - | A. J. Hoffman and R. R. Singleton | On Moore graphs with diameters 2 and 3, IBM J. Res. Dev. 4 (1960) 497-504: a Moore graph of diameter 2 has degree 2, 3, 7 or 57 |
| 1971 | - | - | M. Aschbacher | The nonexistence of rank three permutation groups conjectured by Finkelstein, J. Algebra 19 (1971): such a graph is not rank 3 |
| 2010 | - | - | M. Mačaj and J. Širáň | Search for properties of the missing Moore graph, Linear Algebra Appl. 432 (2010) 2381-2398: its automorphism group has order at most 375 |

## Check a certificate

Certificate format: Text file: the graph in graph6 or sparse6 (as on House of Graphs), as an edge list (one edge "u v" per line, vertices numbered from 0) or as a 0/1 adjacency matrix.

Score: 1 for a valid graph; none is known, so the best known value is 0.

```
python3 -I obb.py check moore-57 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/srg_check.py 3250 57 0 1 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
