# 01. Ramsey number R(5,5)

Family: Ramsey numbers. Benchmark problem: `ramsey-5-5`.

**Best known:** R(5,5) ≥ 43, G. Exoo (1989). Also known: R(5,5) ≤ 46 (V. Angeltveit and B. D. McKay, 2024).

**To beat it:** a red-blue colouring of the edges of K_43 with no red K_5 and no blue K_5, which would show R(5,5) ≥ 44.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_5 and no blue K_5; it shows R(5,5) > n. The best known lower bound is R(5,5) >= 43, so a colouring of K_42 is known and one of K_43 or more would improve it.

## Why it matters

R(5,5) is the smallest diagonal Ramsey number whose value is unknown: it lies between 43 and 46, and McKay and Radziszowski gave strong evidence that it equals 43, with exactly 656 critical graphs on 42 vertices (DS1, item 2.1.e). A colouring of K_43 with no monochromatic K_5 would overturn that conjecture; the lower bound has not moved since Exoo's 1989 colouring.

Sources: [Radziszowski, Small Ramsey Numbers, rev. 18, item 2.1(e)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1); Exoo, A lower bound for R(5,5), J. Graph Theory 13 (1989) 97-98.

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1989 | lower | 43 | G. Exoo | G. Exoo, A Lower Bound for R(5, 5), Journal of Graph Theory, 13 (1989) 97-98. (via Leaps in Bounds) |
| 1997 | upper | 49 | B. D. McKay and S. P. Radziszowski | DS1 rev. 18, item 2.1(e) [MR5] (via DS1) |
| 2018 | upper | 48 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, R(5, 5 ) ≤ 48, Journal of Graph Theory, 89 (2018) 5-13. (via Leaps in Bounds) |
| 2024-09-24 | upper | 46 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, R(5,5) ≤ 46, Journal of Graph Theory (2026), arXiv:2409.15709. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(5,5) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-5-5 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 5 5 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
