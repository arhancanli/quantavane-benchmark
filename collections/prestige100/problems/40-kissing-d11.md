# 40. Kissing number in dimension 11

Family: Kissing numbers. Benchmark problem: `kissing-d11`.

**Best known:** κ(11) ≥ 604, F. Bianchi, Y. Kwon, A. Pappu and J. Zou (2026). Also known: κ(11) ≤ 868 (N. Leijenhorst and D. de Laat, 2022).

**To beat it:** 605 or more vectors in R^11 with pairwise angles of at least 60 degrees.

**Keeper:** [Kissing numbers (H. Cohn)](https://cohn.mit.edu/kissing-numbers/), read 2026-11-09 15:51 +04 (table of lower and upper bounds, dimensions 1 to 48). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find as many nonzero vectors as possible in R^11 with pairwise angles of at least 60 degrees (unit spheres centred at twice the normalised vectors then all touch a central unit sphere without overlapping); k such vectors show that the kissing number in dimension 11 is at least k. The best known configuration, by Bianchi, Kwon, Pappu and Zou (2026), has 604 vectors; one with more vectors improves it.

## Why it matters

The kissing problem (Newton and Gregory, 1694) asks how many unit spheres can touch a central one; it is solved only in dimensions 1-4, 8 and 24. Dimension 11 lies between 604 and 868 in Cohn's table (read 9 Nov 2026); the lower bound is due to F. Bianchi, Y. Kwon, A. Pappu and J. Zou (2026). It is one of the dimensions improved in 2026.

Sources: [H. Cohn, Kissing numbers](https://cohn.mit.edu/kissing-numbers/); [Conway and Sloane, Sphere Packings, Lattices and Groups, 3rd ed. (1999)](https://doi.org/10.1007/978-1-4757-6568-7).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| undated | lower | 582 | not named | Leaps in Bounds table entry (via Leaps in Bounds) |
| 2022-02-24 | upper | 868 | N. Leijenhorst and D. de Laat | N. Leijenhorst and D. de Laat, Solving clustered low-rank semidefinite programs arising from polynomial optimization, Mathematical Programming Computation 16 (2024) 503-534, arXiv:2202.12077. (via Leaps in Bounds) |
| 2022-07-17 | lower | 592 | M. Ganzhinov | M. Ganzhinov, Highly symmetric lines, Linear Algebra and its Applications 722 (2025) 12-37, arXiv:2207.08266. (via Leaps in Bounds) |
| 2025-06-16 | lower | 593 | A. Novikov et al. (AlphaEvolve) | A. Novikov et al. (Google DeepMind), AlphaEvolve: A coding agent for scientific and algorithmic discovery, arXiv:2506.13131. (via Leaps in Bounds) |
| 2026-06-09 | lower | 604 | F. Bianchi, Y. Kwon, A. Pappu and J. Zou | F. Bianchi, Y. Kwon, A. Pappu, and J. Zou, Harnessing the Collective Intelligence of AI Agents in the Wild for New Discoveries, arXiv:2606.10402. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one vector per line, integer coordinates separated by spaces or commas, all with the same squared norm N; more than 11 coordinates are allowed when the vectors span a space of dimension at most 11. Every inner product between two vectors must be at most N/2.

Score: k, the number of vectors (larger is better).

```
python3 -I obb.py check kissing-d11 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/kissing_check.py 11 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
