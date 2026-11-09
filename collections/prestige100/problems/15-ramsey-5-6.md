# 15. Ramsey number R(5,6)

Family: Ramsey numbers. Benchmark problem: `ramsey-5-6`.

**Best known:** R(5,6) ≥ 59, G. Exoo (2023). Also known: R(5,6) ≤ 85 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_59 with no red K_5 and no blue K_6, which would show R(5,6) ≥ 60.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_5 and no blue K_6; it shows R(5,6) > n. The best known lower bound is R(5,6) >= 59, so a colouring of K_58 is known and one of K_59 or more would improve it.

## Why it matters

R(5,6) lies between 59 and 85 (DS1 Tables Ia and Ib); Exoo raised the lower bound from 58 to 59 in 2023, one of the newest improvements of a small lower bound (DS1 item 2.1.p). It neighbours R(5,5) in the table.

Sources: [Small Ramsey Numbers, rev. 18, item 2.1(p)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1993 | upper | 87 | Huang Yi Ru and Zhang Ke Min | Huang Yi Ru and Zhang Ke Min, A New Upper Bound Formula on Ramsey Numbers, Journal of Shanghai University, Natural Science, 7 (1993) 1-3. (via Leaps in Bounds) |
| 2020 | upper | 85 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, personal communication (2019-2024). (via Leaps in Bounds) |
| 2023 | lower | 59 | G. Exoo | G. Exoo, Indiana State University, A Lower Bound for R(5, 6), manuscript (2023). (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(5,6) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-5-6 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 5 6 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
