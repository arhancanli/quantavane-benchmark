# 08. Ramsey number R(3,10)

Family: Ramsey numbers. Benchmark problem: `ramsey-3-10`.

**Best known:** R(3,10) ≥ 40, G. Exoo (1989). Also known: R(3,10) ≤ 41 (V. Angeltveit, 2024).

**To beat it:** a red-blue colouring of the edges of K_40 with no red K_3 and no blue K_10, which would show R(3,10) ≥ 41.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_3 and no blue K_10; it shows R(3,10) > n. The best known lower bound is R(3,10) >= 40, so a colouring of K_39 is known and one of K_40 or more would improve it.

## Why it matters

R(3,10) is either 40 or 41 (Exoo 1989; Angeltveit 2024), the narrowest open gap among the classical two-colour numbers (DS1 Table Ia). A triangle-free graph on 40 vertices with no independent set of 10 vertices would settle it as 41.

Sources: [Small Ramsey Numbers, rev. 18, Table Ia](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1); Angeltveit, R(3,10) ≤ 41, Electron. J. Combin. 32(4) (2025) P4.30.

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1989 | lower | 40 | G. Exoo | G. Exoo, On Two Classical Ramsey Numbers of the Form R(3, n), SIAM Journal on Discrete Mathematics, 2 (1989) 488-490. (via Leaps in Bounds) |
| 2024 | upper | 41 | V. Angeltveit | V. Angeltveit, R(3, 10) ≤ 41, Electronic Journal of Combinatorics 32(4) (2025) #P4.30. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(3,10) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-3-10 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 3 10 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
