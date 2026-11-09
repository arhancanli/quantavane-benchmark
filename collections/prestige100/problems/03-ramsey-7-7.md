# 03. Ramsey number R(7,7)

Family: Ramsey numbers. Benchmark problem: `ramsey-7-7`.

**Best known:** R(7,7) ≥ 205, R. Mathon (1987). Also known: R(7,7) ≤ 492 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_205 with no red K_7 and no blue K_7, which would show R(7,7) ≥ 206.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_7 and no blue K_7; it shows R(7,7) > n. The best known lower bound is R(7,7) >= 205, so a colouring of K_204 is known and one of K_205 or more would improve it.

## Why it matters

R(7,7) lies between 205 and 492; the lower bound is Mathon's 1987 construction from association schemes (DS1 Tables Ia and Ib). Diagonal Ramsey numbers are the classical form of Ramsey's theorem, and their lower bounds have resisted computer search for decades.

Sources: [Small Ramsey Numbers, rev. 18, Tables Ia and Ib](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1987 | lower | 205 | R. Mathon | R. Mathon, Lower Bounds for Ramsey Numbers and Association Schemes, Journal of Combinatorial Theory, Series B, 42 (1987) 122-127. (via Leaps in Bounds) |
| 1994 | upper | 540 | J. Mackey | J. Mackey, Combinatorial Remedies, Ph.D. thesis, Department of Mathematics, University of Hawaii, 1994. (via Leaps in Bounds) |
| 2020 | upper | 492 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, personal communication (2019-2024). (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(7,7) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-7-7 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 7 7 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 204 | R. Mathon (1987) | record | 2026-11-09 | certs/derived_lib_ramsey-7-7-lower-205.txt (7bcd6f7f8626...) |
