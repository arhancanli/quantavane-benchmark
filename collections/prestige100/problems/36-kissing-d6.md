# 36. Kissing number in dimension 6

Family: Kissing numbers. Benchmark problem: `kissing-d6`.

**Best known:** κ(6) ≥ 72, A. Korkine and G. Zolotareff (1873). Also known: κ(6) ≤ 77 (D. de Laat, N. M. Leijenhorst and W. H. H. de Muinck Keizer, 2024).

**To beat it:** 73 or more vectors in R^6 with pairwise angles of at least 60 degrees.

**Keeper:** [Kissing numbers (H. Cohn)](https://cohn.mit.edu/kissing-numbers/), read 2026-11-09 15:51 +04 (table of lower and upper bounds, dimensions 1 to 48). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find as many nonzero vectors as possible in R^6 with pairwise angles of at least 60 degrees (unit spheres centred at twice the normalised vectors then all touch a central unit sphere without overlapping); k such vectors show that the kissing number in dimension 6 is at least k. The best known configuration, by Korkine and Zolotareff (1873), has 72 vectors; one with more vectors improves it.

## Why it matters

The kissing problem (Newton and Gregory, 1694) asks how many unit spheres can touch a central one; it is solved only in dimensions 1-4, 8 and 24. Dimension 6 is pinned between 72 and 77; the E6 root system's 72 vectors (Korkine and Zolotareff 1873) have never been beaten.

Sources: [H. Cohn, Kissing numbers](https://cohn.mit.edu/kissing-numbers/); [Conway and Sloane, Sphere Packings, Lattices and Groups, 3rd ed. (1999)](https://doi.org/10.1007/978-1-4757-6568-7).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1873 | lower | 72 | A. Korkine and G. Zolotareff | A. Korkine and G. Zolotareff, Sur les formes quadratiques, Mathematische Annalen 6 (1873) 366-389. (via Leaps in Bounds) |
| 2008 | upper | 78 | C. Bachoc and F. Vallentin | C. Bachoc and F. Vallentin, New upper bounds for kissing numbers from semidefinite programming, Journal of the American Mathematical Society 21 (2008) 909-924. (via Leaps in Bounds) |
| 2024-04-29 | upper | 77 | D. de Laat, N. M. Leijenhorst and W. H. H. de Muinck Keizer | D. de Laat, N.M. Leijenhorst, and W.H.H. de Muinck Keizer, Optimality and uniqueness of the D4 root system, arXiv:2404.18794. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one vector per line, integer coordinates separated by spaces or commas, all with the same squared norm N; more than 6 coordinates are allowed when the vectors span a space of dimension at most 6. Every inner product between two vectors must be at most N/2.

Score: k, the number of vectors (larger is better).

```
python3 -I obb.py check kissing-d6 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/kissing_check.py 6 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 72 | Korkine and Zolotareff (1873) (file built by Quantavane's code) | record | 2026-11-08 | refs/classic_kissing_d6_E6_n72.txt (6a2bb2e4adc5...) |
