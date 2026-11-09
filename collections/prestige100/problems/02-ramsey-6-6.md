# 02. Ramsey number R(6,6)

Family: Ramsey numbers. Benchmark problem: `ramsey-6-6`.

**Best known:** R(6,6) ≥ 102, J. G. Kalbfleisch (1966). Also known: R(6,6) ≤ 160 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_102 with no red K_6 and no blue K_6, which would show R(6,6) ≥ 103.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_6 and no blue K_6; it shows R(6,6) > n. The best known lower bound is R(6,6) >= 102, so a colouring of K_101 is known and one of K_102 or more would improve it.

## Why it matters

R(6,6) is the next diagonal case after R(5,5); it lies between 102 and 160 (DS1 Tables Ia and Ib). The lower bound is the colouring in Kalbfleisch's 1966 thesis and has not been improved since.

Sources: [Small Ramsey Numbers, rev. 18, Tables Ia and Ib](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1966-01 | lower | 102 | J. G. Kalbfleisch | J.G. Kalbfleisch, Chromatic Graphs and Ramsey's Theorem, Ph.D. thesis, University of Waterloo, January 1966. (via Leaps in Bounds) |
| 1994 | upper | 165 | J. Mackey | J. Mackey, Combinatorial Remedies, Ph.D. thesis, Department of Mathematics, University of Hawaii, 1994. (via Leaps in Bounds) |
| 2023 | upper | 160 | V. Angeltveit and B. D. McKay | DS1 rev. 18, Table Ib and item 2.1 [AnM3] (via DS1) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(6,6) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-6-6 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 6 6 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 101 | J. G. Kalbfleisch (1966) | record | 2026-11-09 | certs/derived_lib_ramsey-6-6-lower-102.txt (a48a24af3508...) |
