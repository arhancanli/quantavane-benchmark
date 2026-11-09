# 57. Kissing number in dimension 29

Family: Kissing numbers. Benchmark problem: `kissing-d29`.

**Best known:** κ(29) ≥ 231697, A. Kravatskiy (2026). Also known: κ(29) ≤ 1075991 (N. Leijenhorst and D. de Laat, 2022).

**To beat it:** 231698 or more vectors in R^29 with pairwise angles of at least 60 degrees.

**Keeper:** [Kissing numbers (H. Cohn)](https://cohn.mit.edu/kissing-numbers/), read 2026-11-09 15:51 +04 (table of lower and upper bounds, dimensions 1 to 48). Also read: [A. Kravatskiy, KissingNumbers (GitHub)](https://github.com/alexlegeartis/KissingNumbers), 2026-11-09 15:56 +04 (README at commit c0b3f9a (8 Nov 2026, 19:43 UTC)).

## The problem

Find as many nonzero vectors as possible in R^29 with pairwise angles of at least 60 degrees; k such vectors show that the kissing number in dimension 29 is at least k. The best known configuration, by A. Kravatskiy (2026), has 231697 vectors; one with more vectors improves it. The upper bound is 1075991 (Leijenhorst and de Laat).

## Why it matters

The kissing problem (Newton and Gregory, 1694) asks how many unit spheres can touch a central one; it is solved only in dimensions 1-4, 8 and 24. Dimension 29 lies between 231697 and 1075991 in Cohn's table (read 9 Nov 2026); the lower bound is due to A. Kravatskiy (2026). It is one of the dimensions improved in 2026.

Sources: [H. Cohn, Kissing numbers](https://cohn.mit.edu/kissing-numbers/); [Conway and Sloane, Sphere Packings, Lattices and Groups, 3rd ed. (1999)](https://doi.org/10.1007/978-1-4757-6568-7).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| undated | lower | 209496 | Ma et al., PackingStar (arXiv:2511.13391) | the comparison value recorded in Kravatskiy's table (via A. Kravatskiy, KissingNumbers) |
| 2026-10-29 | lower | 231697 | A. Kravatskiy | github.com/alexlegeartis/KissingNumbers (verifications/improved); listed by H. Cohn (via A. Kravatskiy, KissingNumbers) |
| 2022 | upper | 1075991 | N. Leijenhorst and D. de Laat | H. Cohn's table, reference [12] (via H. Cohn) |

## Check a certificate

Certificate format: Text file: one vector per line, integer coordinates separated by spaces or commas, all with the same squared norm N; more than 29 coordinates are allowed when the vectors span a space of dimension at most 29. Every inner product between two vectors must be at most N/2. With 231,697 vectors or more the check is long (hours) in pure Python.

Score: k, the number of vectors (larger is better).

```
python3 -I obb.py check kissing-d29 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/kissing_check.py 29 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
