# 17. Ramsey number R(5,15)

Family: Ramsey numbers. Benchmark problem: `ramsey-5-15`.

**Best known:** R(5,15) ≥ 283, A. Canli (Quantavane), 5 Nov 2026. Also known: R(5,15) ≤ 1341 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_283 with no red K_5 and no blue K_15, which would show R(5,15) ≥ 284.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

**Quantavane holds this record.** Quantavane's circulant colouring of K_282 (5 Nov 2026), published with a checker in github.com/arhancanli/quantavane-ramsey-records and sent to S. Radziszowski on 6 Nov 2026; Leaps in Bounds verified the certificate and lists 283 (merged 9 Nov 2026).

## The problem

Find a two-colouring of the edges of K_n with no red K_5 and no blue K_15; it shows R(5,15) > n. The best known lower bound is R(5,15) >= 283, so a colouring of K_282 is known and one of K_283 or more would improve it.

## Why it matters

R(5,15) is a cell of DS1's Table Ia, where revision 18 prints the bound 275 obtained from a general inequality (item 2.3.h) rather than from a colouring. Quantavane's circulant colourings raised it to 279 and then to 283; Leaps in Bounds verified the certificate and lists 283.

Sources: [Small Ramsey Numbers, rev. 18, Table Ia](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1); [Leaps in Bounds, ramsey-5-15](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| undated | lower | 275 | a standard bound | Trivial or easy according to the secondary source. (via Leaps in Bounds) |
| 2007 | upper | 1878 | Huang Yi Ru, Wang Yuandi, Sheng Wancheng, Yang Jiansheng, Zhang Ke Min and Huang Jian | Huang Yi Ru, Wang Yuandi, Sheng Wancheng, Yang Jiansheng, Zhang Ke Min and Huang Jian, New Upper Bound Formulas with Parameters for Ramsey Numbers, Discrete Mathematics, 307 (2007) 760-763. (via Leaps in Bounds) |
| 2020 | upper | 1341 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, personal communication (2019-2024). (via Leaps in Bounds) |
| 2026-10-25 | lower | 279 | A. Canli (Quantavane) | A. Canli (Quantavane), Ramsey number lower bounds from Quantavane, GitHub repository, 2026-10-25. (via Leaps in Bounds) |
| 2026-11-05 | lower | 283 | A. Canli (Quantavane) | A. Canli (Quantavane), Ramsey number lower bounds from Quantavane, GitHub repository, 2026-11-05. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(5,15) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-5-15 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 5 15 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 282 | Quantavane (Arhan Canli) | record | 2026-11-08 | refs/ours_ramsey_5_15_n282.txt (9c678813f4ac...) |
