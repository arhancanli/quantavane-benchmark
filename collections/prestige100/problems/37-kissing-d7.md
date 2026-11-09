# 37. Kissing number in dimension 7

Family: Kissing numbers. Benchmark problem: `kissing-d7`.

**Best known:** κ(7) ≥ 126, A. Korkine and G. Zolotareff (1873). Also known: κ(7) ≤ 132 (T. S. Tomar, 2026).

**To beat it:** 127 or more vectors in R^7 with pairwise angles of at least 60 degrees.

**Keeper:** [Kissing numbers (H. Cohn)](https://cohn.mit.edu/kissing-numbers/), read 2026-11-09 15:51 +04 (table of lower and upper bounds, dimensions 1 to 48). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find as many nonzero vectors as possible in R^7 with pairwise angles of at least 60 degrees (unit spheres centred at twice the normalised vectors then all touch a central unit sphere without overlapping); k such vectors show that the kissing number in dimension 7 is at least k. The best known configuration, by Korkine and Zolotareff (1873), has 126 vectors; one with more vectors improves it.

## Why it matters

The kissing problem (Newton and Gregory, 1694) asks how many unit spheres can touch a central one; it is solved only in dimensions 1-4, 8 and 24. Dimension 7 lies between 126 and 132; the E7 root system's 126 vectors date from 1873.

Sources: [H. Cohn, Kissing numbers](https://cohn.mit.edu/kissing-numbers/); [Conway and Sloane, Sphere Packings, Lattices and Groups, 3rd ed. (1999)](https://doi.org/10.1007/978-1-4757-6568-7).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1873 | lower | 126 | A. Korkine and G. Zolotareff | A. Korkine and G. Zolotareff, Sur les formes quadratiques, Mathematische Annalen 6 (1873) 366-389. (via Leaps in Bounds) |
| 2008 | upper | 135 | C. Bachoc and F. Vallentin | C. Bachoc and F. Vallentin, New upper bounds for kissing numbers from semidefinite programming, Journal of the American Mathematical Society 21 (2008) 909-924. (via Leaps in Bounds) |
| 2009-02-06 | upper | 134 | H. D. Mittelmann and F. Vallentin | H.D. Mittelmann and F. Vallentin, High accuracy semidefinite programming bounds for kissing numbers, Experimental Mathematics 19 (2010) 174-178, arXiv:0902.1105. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: one vector per line, integer coordinates separated by spaces or commas, all with the same squared norm N; more than 7 coordinates are allowed when the vectors span a space of dimension at most 7. Every inner product between two vectors must be at most N/2.

Score: k, the number of vectors (larger is better).

```
python3 -I obb.py check kissing-d7 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/kissing_check.py 7 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 126 | Korkine and Zolotareff (1873) (file built by Quantavane's code) | record | 2026-11-08 | refs/classic_kissing_d7_E7_n126.txt (1de0f162d310...) |
