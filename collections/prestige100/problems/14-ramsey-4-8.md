# 14. Ramsey number R(4,8)

Family: Ramsey numbers. Benchmark problem: `ramsey-4-8`.

**Best known:** R(4,8) ≥ 59, G. Exoo and M. Tatarevic (2015). Also known: R(4,8) ≤ 79 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_59 with no red K_4 and no blue K_8, which would show R(4,8) ≥ 60.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_4 and no blue K_8; it shows R(4,8) > n. The best known lower bound is R(4,8) >= 59, so a colouring of K_58 is known and one of K_59 or more would improve it.

## Why it matters

R(4,8) lies between 59 and 79 (DS1 Tables Ia and Ib). It sits next to R(4,6) in the smallest open corner of the table, where every upper bound came from large computations and every lower bound from one explicit colouring.

Sources: [Small Ramsey Numbers, rev. 18, Tables Ia and Ib](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1994 | upper | 84 | J. Mackey | J. Mackey, Combinatorial Remedies, Ph.D. thesis, Department of Mathematics, University of Hawaii, 1994. (via Leaps in Bounds) |
| 2015 | lower | 59 | G. Exoo and M. Tatarevic | G. Exoo and M. Tatarevic, New Lower Bounds for 28 Classical Ramsey Numbers, Electronic Journal of Combinatorics, http:// www.combinatorics.org, #P3.11, 22(3) (2015), 12 pages. Graphs available at the journal site and at http://cs.indstate.edu/ge/RAMSEY/ExTa. (via Leaps in Bounds) |
| 2020 | upper | 79 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, personal communication (2019-2024). (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(4,8) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-4-8 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 4 8 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
