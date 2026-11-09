# 18. Ramsey number R(8,12)

Family: Ramsey numbers. Benchmark problem: `ramsey-8-12`.

**Best known:** R(8,12) ≥ 523, A. Canli (Quantavane), 6 Nov 2026. Also known: R(8,12) ≤ 10836 (V. Angeltveit and B. D. McKay, 2019-2024).

**To beat it:** a red-blue colouring of the edges of K_523 with no red K_8 and no blue K_12, which would show R(8,12) ≥ 524.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

**Quantavane holds this record.** Quantavane's colouring of K_522 (6 Nov 2026), grown from Google Research's K_510; published with a checker in github.com/arhancanli/quantavane-ramsey-records, sent to S. Radziszowski on 6 Nov 2026, and listed by Leaps in Bounds on our attestation (its exact check takes one to two hours).

## The problem

Find a two-colouring of the edges of K_n with no red K_8 and no blue K_12; it shows R(8,12) > n. The best known lower bound is R(8,12) >= 523, so a colouring of K_522 is known and one of K_523 or more would improve it.

## Why it matters

R(8,12) has no lower bound from a colouring in DS1 revision 18; Google Research's repository gave 511 in 2026. Quantavane's colourings raised it to 512, 519 and 523, and Leaps in Bounds lists 523 with our attested certificate.

Sources: [Leaps in Bounds, ramsey-8-12](https://github.com/daniel-munro/leaps-in-bounds); [Canli, New lower bounds for the Ramsey numbers R(5,15) and R(8,12), Zenodo](https://doi.org/10.5281/zenodo.23920916).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2007 | upper | 16944 | Huang Yi Ru, Wang Yuandi, Sheng Wancheng, Yang Jiansheng, Zhang Ke Min and Huang Jian | Huang Yi Ru, Wang Yuandi, Sheng Wancheng, Yang Jiansheng, Zhang Ke Min and Huang Jian, New Upper Bound Formulas with Parameters for Ramsey Numbers, Discrete Mathematics, 307 (2007) 760-763. (via Leaps in Bounds) |
| 2020 | upper | 10836 | V. Angeltveit and B. D. McKay | V. Angeltveit and B.D. McKay, personal communication (2019-2024). (via Leaps in Bounds) |
| 2026-10-22 | lower | 511 | Google Research (ramsey_number_bounds) | Google Research, ramsey_number_bounds: improved lower bounds on Ramsey numbers, GitHub repository, 2026. (via Leaps in Bounds) |
| 2026-10-25 | lower | 512 | A. Canli (Quantavane) | A. Canli (Quantavane), Ramsey number lower bounds from Quantavane, GitHub repository, 2026-10-25. (via Leaps in Bounds) |
| 2026-11-03 | lower | 519 | A. Canli (Quantavane) | A. Canli, New lower bounds for the Ramsey numbers R(5,15) and R(8,12), version 2, Zenodo. (via Leaps in Bounds) |
| 2026-11-06 | lower | 523 | A. Canli (Quantavane) | A. Canli (Quantavane), Ramsey number lower bounds from Quantavane, GitHub repository, 2026-11-06. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(8,12) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-8-12 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 8 12 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
