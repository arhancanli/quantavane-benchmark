# 48. Kissing number in dimension 19

Family: Kissing numbers. Benchmark problem: `kissing-d19`.

**Best known:** κ(19) ≥ 12460, K. Li (2026). Also known: κ(19) ≤ 24417 (N. Leijenhorst and D. de Laat, 2022).

**To beat it:** 12461 or more vectors in R^19 with pairwise angles of at least 60 degrees.

**Keeper:** [Kissing numbers (H. Cohn)](https://cohn.mit.edu/kissing-numbers/), read 2026-11-09 15:51 +04 (table of lower and upper bounds, dimensions 1 to 48). Also read: [A. Kravatskiy, KissingNumbers (GitHub)](https://github.com/alexlegeartis/KissingNumbers), 2026-11-09 15:56 +04 (README at commit c0b3f9a (8 Nov 2026, 19:43 UTC)).

## The problem

Find as many nonzero vectors as possible in R^19 with pairwise angles of at least 60 degrees (unit spheres centred at twice the normalised vectors then all touch a central unit sphere without overlapping); k such vectors show that the kissing number in dimension 19 is at least k. The best known configuration, by K. Li (2026), has 12460 vectors; one with more vectors improves it. Some of the best known configurations in dimensions 17 to 21 need irrational coordinates, so they cannot be given here as integer vectors.

## Why it matters

The kissing problem (Newton and Gregory, 1694) asks how many unit spheres can touch a central one; it is solved only in dimensions 1-4, 8 and 24. Dimension 19 lies between 12460 and 24417 in Cohn's table (read 9 Nov 2026); the lower bound is due to K. Li (2026). It is one of the dimensions improved in 2026.

Sources: [H. Cohn, Kissing numbers](https://cohn.mit.edu/kissing-numbers/); [Conway and Sloane, Sphere Packings, Lattices and Groups, 3rd ed. (1999)](https://doi.org/10.1007/978-1-4757-6568-7).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1967 | lower | 10668 | J. Leech | J. Leech, Notes on sphere packings, Canadian Journal of Mathematics 19 (1967) 251-267. (via Leaps in Bounds) |
| 2022-02-24 | upper | 24417 | N. Leijenhorst and D. de Laat | N. Leijenhorst and D. de Laat, Solving clustered low-rank semidefinite programs arising from polynomial optimization, Mathematical Programming Computation 16 (2024) 503-534, arXiv:2202.12077. (via Leaps in Bounds) |
| 2024-11-07 | lower | 11692 | H. Cohn and A. Li | H. Cohn and A. Li, Improved kissing numbers in seventeen through twenty-one dimensions, arXiv:2411.04916. (via Leaps in Bounds) |
| 2026-03-11 | lower | 11948 | B. S. Ho | B.S. Ho, A new lower bound for the kissing number in 19 dimensions, arXiv:2603.10425. (via Leaps in Bounds) |
| 2026-10-14 | lower | 12460 | K. Li | K. Li, Improved Kissing Numbers in Nineteen and Twenty-One Dimensions, Hexagon hexagon:2610.00248. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one vector per line, integer coordinates separated by spaces or commas, all with the same squared norm N; more than 19 coordinates are allowed when the vectors span a space of dimension at most 19. Every inner product between two vectors must be at most N/2.

Score: k, the number of vectors (larger is better).

```
python3 -I obb.py check kissing-d19 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/kissing_check.py 19 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
