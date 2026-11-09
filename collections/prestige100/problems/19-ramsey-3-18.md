# 19. Ramsey number R(3,18)

Family: Ramsey numbers. Benchmark problem: `ramsey-3-18`.

**Best known:** R(3,18) ≥ 101, A. Canli (Quantavane), 8 Nov 2026. Also known: R(3,18) ≤ 120 (S. Backelin [Back4]).

**To beat it:** a red-blue colouring of the edges of K_101 with no red K_3 and no blue K_18, which would show R(3,18) ≥ 102.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

**Quantavane holds this record.** Quantavane's triangle-free graph on 100 vertices with no independent set of 18 vertices (8 Nov 2026), checked by three separate programs and published with a checker in github.com/arhancanli/quantavane-ramsey-records; the survey lists 100 until its keeper adds ours.

## The problem

Find a two-colouring of the edges of K_n with no red K_3 and no blue K_18; it shows R(3,18) > n. The best known lower bound is R(3,18) >= 101, so a colouring of K_100 is known and one of K_101 or more would improve it.

## Why it matters

R(3,18) is in DS1's Table IIa of higher Ramsey numbers, where revision 18 prints 100 from Nagda, Raghavan and Thakurta's 2026 graph on 99 vertices. Quantavane added one vertex to that graph: a triangle-free graph on 100 vertices with no independent set of 18 vertices.

Sources: [Small Ramsey Numbers, rev. 18, Table IIa](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2026 | lower | 100 | S. Nagda, P. Raghavan and A. Thakurta (Google Research) | DS1 rev. 18, Table IIa [NaRT] (via DS1) |
| 2026-11-08 | lower | 101 | A. Canli (Quantavane) | github.com/arhancanli/quantavane-ramsey-records (K_100, one vertex added to NaRT's K_99) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(3,18) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-3-18 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 3 18 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 100 | Quantavane (Arhan Canli) | record | 2026-11-08 | refs/ours_ramsey_3_18_n100.txt (53679872bbd0...) |
