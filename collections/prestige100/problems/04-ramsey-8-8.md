# 04. Ramsey number R(8,8)

Family: Ramsey numbers. Benchmark problem: `ramsey-8-8`.

**Best known:** R(8,8) ≥ 282, J. P. Burling and S. W. Reyner (1972). Also known: R(8,8) ≤ 1518 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_282 with no red K_8 and no blue K_8, which would show R(8,8) ≥ 283.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_8 and no blue K_8; it shows R(8,8) > n. The best known lower bound is R(8,8) >= 282, so a colouring of K_281 is known and one of K_282 or more would improve it.

## Why it matters

R(8,8) lies between 282 and 1518; the lower bound is Burling and Reyner's 1972 colouring, which DS1 calls weak but not easy to improve (item 2.1.q) (DS1 Tables Ia and Ib). Diagonal Ramsey numbers are the classical form of Ramsey's theorem, and their lower bounds have resisted computer search for decades.

Sources: [Small Ramsey Numbers, rev. 18, Tables Ia and Ib](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1972 | lower | 282 | J. P. Burling and S. W. Reyner | J.P. Burling and S.W. Reyner, Some Lower Bounds of the Ramsey Numbers n(k, k), Journal of Combinatorial Theory, Series B, 13 (1972) 168-169. (via Leaps in Bounds) |
| 1994 | upper | 1870 | J. Mackey | J. Mackey, Combinatorial Remedies, Ph.D. thesis, Department of Mathematics, University of Hawaii, 1994. (via Leaps in Bounds) |
| 2020 | upper | 1518 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, personal communication (2019-2024). (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(8,8) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-8-8 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 8 8 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 281 | J. P. Burling and S. W. Reyner (1972) | record | 2026-11-09 | certs/derived_lib_ramsey-8-8-lower-282.txt (06c7efc1865f...) |
