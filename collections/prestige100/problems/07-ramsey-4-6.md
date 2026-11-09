# 07. Ramsey number R(4,6)

Family: Ramsey numbers. Benchmark problem: `ramsey-4-6`.

**Best known:** R(4,6) ≥ 36, G. Exoo (2012). Also known: R(4,6) ≤ 40 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_36 with no red K_4 and no blue K_6, which would show R(4,6) ≥ 37.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_4 and no blue K_6; it shows R(4,6) > n. The best known lower bound is R(4,6) >= 36, so a colouring of K_35 is known and one of K_36 or more would improve it.

## Why it matters

With R(3,10) and R(5,5), R(4,6) is one of the three smallest open two-colour Ramsey numbers; it lies between 36 and 40 (DS1 Tables Ia and Ib). Exoo's 2012 graph on 35 vertices raised the lower bound from 35, which had stood since 1993.

Sources: [Small Ramsey Numbers, rev. 18](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1); Exoo, On the Ramsey number R(4,6), Electron. J. Combin. 19(1) (2012) P66.

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1993 | lower | 35 | G. Exoo | DS1 rev. 18, reference [Ex9]: Announcement: On the Ramsey Numbers R(4,6), R(5,6) and R(3,12), Ars Combinatoria 35 (1993) 85 (via DS1) |
| 1997 | upper | 41 | B. D. McKay and S. P. Radziszowski | B.D. McKay and S.P. Radziszowski, Subgraph Counting Identities and Ramsey Numbers, Journal of Combinatorial Theory, Series B, 69 (1997) 193-209. (via Leaps in Bounds) |
| 2012 | lower | 36 | G. Exoo | G. Exoo, On the Ramsey Number R(4, 6), Electronic Journal of Combinatorics, http://www.combinatorics.org, #P66, 19(1) (2012), 5 pages. (via Leaps in Bounds) |
| 2020 | upper | 40 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, personal communication (2019-2024). (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(4,6) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-4-6 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 4 6 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
