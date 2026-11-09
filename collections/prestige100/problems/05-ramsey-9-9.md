# 05. Ramsey number R(9,9)

Family: Ramsey numbers. Benchmark problem: `ramsey-9-9`.

**Best known:** R(9,9) ≥ 565, R. Mathon (1987). Also known: R(9,9) ≤ 4956 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_565 with no red K_9 and no blue K_9, which would show R(9,9) ≥ 566.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_9 and no blue K_9; it shows R(9,9) > n. The best known lower bound is R(9,9) >= 565, so a colouring of K_564 is known and one of K_565 or more would improve it.

## Why it matters

R(9,9) lies between 565 and 4956; the lower bound is Mathon's 1987 construction (DS1 Tables Ia and Ib). Diagonal Ramsey numbers are the classical form of Ramsey's theorem, and their lower bounds have resisted computer search for decades.

Sources: [Small Ramsey Numbers, rev. 18, Tables Ia and Ib](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1987 | lower | 565 | R. Mathon | R. Mathon, Lower Bounds for Ramsey Numbers and Association Schemes, Journal of Combinatorial Theory, Series B, 42 (1987) 122-127. (via Leaps in Bounds) |
| 2001 | upper | 6588 | Shi Lingsheng and Zhang Ke Min | Shi Ling Sheng and Zhang Ke Min, An Upper Bound Formula for Ramsey Numbers, manuscript (2001). (via Leaps in Bounds) |
| 2020 | upper | 4956 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, personal communication (2019-2024). (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(9,9) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-9-9 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 9 9 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
