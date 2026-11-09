# 38. Kissing number in dimension 9

Family: Kissing numbers. Benchmark problem: `kissing-d9`.

**Best known:** κ(9) ≥ 306, J. Leech and N. J. A. Sloane (1971). Also known: κ(9) ≤ 363 (F. C. Machado and F. M. de Oliveira Filho, 2018).

**To beat it:** 307 or more vectors in R^9 with pairwise angles of at least 60 degrees.

**Keeper:** [Kissing numbers (H. Cohn)](https://cohn.mit.edu/kissing-numbers/), read 2026-11-09 15:51 +04 (table of lower and upper bounds, dimensions 1 to 48). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find as many nonzero vectors as possible in R^9 with pairwise angles of at least 60 degrees (unit spheres centred at twice the normalised vectors then all touch a central unit sphere without overlapping); k such vectors show that the kissing number in dimension 9 is at least k. The best known configuration, by Leech and Sloane (1971), has 306 vectors; one with more vectors improves it.

## Why it matters

The kissing problem (Newton and Gregory, 1694) asks how many unit spheres can touch a central one; it is solved only in dimensions 1-4, 8 and 24. Dimension 9 lies between 306 and 363; Leech and Sloane's 1971 configuration of 306 is still the best known, just after the solved dimension 8 (240).

Sources: [H. Cohn, Kissing numbers](https://cohn.mit.edu/kissing-numbers/); [Conway and Sloane, Sphere Packings, Lattices and Groups, 3rd ed. (1999)](https://doi.org/10.1007/978-1-4757-6568-7).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1971 | lower | 306 | J. Leech and N. J. A. Sloane | J. Leech and N.J.A. Sloane, Sphere packings and error-correcting codes, Canadian Journal of Mathematics 23 (1971) 718-745. (via Leaps in Bounds) |
| 2018 | upper | 363 | F. C. Machado and F. M. de Oliveira Filho | F.C. Machado and F.M. de Oliveira Filho, Improving the semidefinite programming bound for the kissing number by exploiting polynomial symmetry, Experimental Mathematics 27 (2018) 362-369. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one vector per line, integer coordinates separated by spaces or commas, all with the same squared norm N; more than 9 coordinates are allowed when the vectors span a space of dimension at most 9. Every inner product between two vectors must be at most N/2.

Score: k, the number of vectors (larger is better).

```
python3 -I obb.py check kissing-d9 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/kissing_check.py 9 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
