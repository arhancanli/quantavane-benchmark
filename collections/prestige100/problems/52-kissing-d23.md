# 52. Kissing number in dimension 23

Family: Kissing numbers. Benchmark problem: `kissing-d23`.

**Best known:** κ(23) ≥ 93150, J. Leech (1967). Also known: κ(23) ≤ 122351 (N. Leijenhorst and D. de Laat, 2022).

**To beat it:** 93151 or more vectors in R^23 with pairwise angles of at least 60 degrees.

**Keeper:** [Kissing numbers (H. Cohn)](https://cohn.mit.edu/kissing-numbers/), read 2026-11-09 15:51 +04 (table of lower and upper bounds, dimensions 1 to 48). Also read: [A. Kravatskiy, KissingNumbers (GitHub)](https://github.com/alexlegeartis/KissingNumbers), 2026-11-09 15:56 +04 (README at commit c0b3f9a (8 Nov 2026, 19:43 UTC)).

## The problem

Find as many nonzero vectors as possible in R^23 with pairwise angles of at least 60 degrees; k such vectors show that the kissing number in dimension 23 is at least k. The best known configuration, by J. Leech (1967), has 93150 vectors; one with more vectors improves it. The upper bound is 122351 (Leijenhorst and de Laat).

## Why it matters

The kissing problem (Newton and Gregory, 1694) asks how many unit spheres can touch a central one; it is solved only in dimensions 1-4, 8 and 24. Dimensions 22 and 23 are held by Leech's 1967 cross-sections of the Leech lattice, unbeaten for 59 years.

Sources: [H. Cohn, Kissing numbers](https://cohn.mit.edu/kissing-numbers/); [Conway and Sloane, Sphere Packings, Lattices and Groups, 3rd ed. (1999)](https://doi.org/10.1007/978-1-4757-6568-7).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1967 | lower | 93150 | J. Leech | J. Leech, Notes on sphere packings, Canadian Journal of Mathematics 19 (1967) 251-267. (via Leaps in Bounds) |
| 2022-02-24 | upper | 122351 | N. Leijenhorst and D. de Laat | N. Leijenhorst and D. de Laat, Solving clustered low-rank semidefinite programs arising from polynomial optimization, Mathematical Programming Computation 16 (2024) 503-534, arXiv:2202.12077. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one vector per line, integer coordinates separated by spaces or commas, all with the same squared norm N; more than 23 coordinates are allowed when the vectors span a space of dimension at most 23. Every inner product between two vectors must be at most N/2. With 93,150 vectors or more the check is long (hours) in pure Python.

Score: k, the number of vectors (larger is better).

```
python3 -I obb.py check kissing-d23 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/kissing_check.py 23 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
