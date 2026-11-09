# 11. Ramsey number R(3,13)

Family: Ramsey numbers. Benchmark problem: `ramsey-3-13`.

**Best known:** R(3,13) ≥ 61, Google Research, ramsey_number_bounds (2026). Also known: R(3,13) ≤ 68 (J. Goedgebeur and S. P. Radziszowski, 2013).

**To beat it:** a red-blue colouring of the edges of K_61 with no red K_3 and no blue K_13, which would show R(3,13) ≥ 62.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_3 and no blue K_13; it shows R(3,13) > n. The best known lower bound is R(3,13) >= 61, so a colouring of K_60 is known and one of K_61 or more would improve it.

## Why it matters

R(3,13) lies between 61 and 68; the lower bound rose from 60 to 61 in February 2026 (DS1 Table Ia). The numbers R(3,k) ask for triangle-free graphs with no large independent set, the case studied most closely in Ramsey theory, and a better graph raises the lower bound directly.

Sources: [Small Ramsey Numbers, rev. 18, Table Ia](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2013 | upper | 68 | J. Goedgebeur and S. P. Radziszowski | J. Goedgebeur and S.P. Radziszowski, New Computational Upper Bounds for Ramsey Numbers R(3, k), Electronic Journal of Combinatorics, http://www.combinatorics.org, #P30, 20(1) (2013), 28 pages. (via Leaps in Bounds) |
| 2015 | lower | 60 | M. Kolodyazhny | M. Kolodyazhny, Novye Nizhnie Granitsy Chisel Ramseya R(3, 12) i R(3, 13) (in Russian), Matematicheskoye i Informacionnoe Modelirovanie, Tyumen, 14 (2015) 126-130. (via Leaps in Bounds) |
| 2026-02-12 | lower | 61 | Google Research (ramsey_number_bounds) | Google Research, ramsey_number_bounds: improved lower bounds on Ramsey numbers, GitHub repository, 2026. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(3,13) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-3-13 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 3 13 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
