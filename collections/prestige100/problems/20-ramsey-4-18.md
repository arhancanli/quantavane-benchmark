# 20. Ramsey number R(4,18)

Family: Ramsey numbers. Benchmark problem: `ramsey-4-18`.

**Best known:** R(4,18) ≥ 211, A. Canli (Quantavane), 8 Nov 2026.

**To beat it:** a red-blue colouring of the edges of K_211 with no red K_4 and no blue K_18, which would show R(4,18) ≥ 212.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

**Quantavane holds this record.** Quantavane's colouring of K_210 (8 Nov 2026), checked by three separate programs and published with a checker in github.com/arhancanli/quantavane-ramsey-records; the survey prints 205 until its keeper adds ours. Table IIa of the survey gives only lower bounds for k ≥ 4, so no upper bound is quoted.

## The problem

Find a two-colouring of the edges of K_n with no red K_4 and no blue K_18; it shows R(4,18) > n. The best known lower bound is R(4,18) >= 211, so a colouring of K_210 is known and one of K_211 or more would improve it.

## Why it matters

R(4,18) is in DS1's Table IIa, where revision 18 prints 205 from a general inequality (item 2.3.e); Google Research's repository later gave 209. Quantavane's colourings of K_209 and K_210 raised it to 210 and then 211 on 8 Nov 2026.

Sources: [Small Ramsey Numbers, rev. 18, Table IIa](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2026 | lower | 209 | Google Research (ramsey_number_bounds) | github.com/google-research/ramsey_number_bounds (as read on 8 Nov 2026) |
| 2026-04-24 | lower | 205 | inequality 2.3.e of the survey | DS1 rev. 18, Table IIa (via DS1) |
| 2026-11-08 | lower | 210 | A. Canli (Quantavane) | github.com/arhancanli/quantavane-ramsey-records (K_209) |
| 2026-11-08 | lower | 211 | A. Canli (Quantavane) | github.com/arhancanli/quantavane-ramsey-records (K_210) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(4,18) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-4-18 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 4 18 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 210 | Quantavane (Arhan Canli) | record | 2026-11-08 | refs/ours_ramsey_4_18_n210.txt (20ef93483f35...) |
