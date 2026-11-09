# 16. Ramsey number R(5,7)

Family: Ramsey numbers. Benchmark problem: `ramsey-5-7`.

**Best known:** R(5,7) ≥ 80, N. J. Calkin, P. Erdős and C. A. Tovey (1997). Also known: R(5,7) ≤ 133 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_80 with no red K_5 and no blue K_7, which would show R(5,7) ≥ 81.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_5 and no blue K_7; it shows R(5,7) > n. The best known lower bound is R(5,7) >= 80, so a colouring of K_79 is known and one of K_80 or more would improve it.

## Why it matters

R(5,7) lies between 80 and 133 (DS1 Tables Ia and Ib); the lower bound is a cyclic graph of prime order found by Calkin, Erdős and Tovey in 1997. It is one of the few small cells still held by a construction from the 1990s.

Sources: [Small Ramsey Numbers, rev. 18](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1); Calkin, Erdős and Tovey, SIAM J. Discrete Math. 10 (1997) 381-387.

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1993 | upper | 143 | Huang Yi Ru and Zhang Ke Min | Huang Yi Ru and Zhang Ke Min, A New Upper Bound Formula on Ramsey Numbers, Journal of Shanghai University, Natural Science, 7 (1993) 1-3. (via Leaps in Bounds) |
| 1997 | lower | 80 | N. J. Calkin, P. Erdős and C. A. Tovey | N.J. Calkin, P. Erdős and C.A. Tovey, New Ramsey Bounds from Cyclic Graphs of Prime Order, SIAM Journal on Discrete Mathematics, 10 (1997) 381-387. (via Leaps in Bounds) |
| 2020 | upper | 133 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, personal communication (2019-2024). (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(5,7) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-5-7 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 5 7 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
