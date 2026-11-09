# 10. Ramsey number R(3,12)

Family: Ramsey numbers. Benchmark problem: `ramsey-3-12`.

**Best known:** R(3,12) ≥ 53, M. Kolodyazhny (2015). Also known: R(3,12) ≤ 59 (A. Lesser, 2001).

**To beat it:** a red-blue colouring of the edges of K_53 with no red K_3 and no blue K_12, which would show R(3,12) ≥ 54.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a two-colouring of the edges of K_n with no red K_3 and no blue K_12; it shows R(3,12) > n. The best known lower bound is R(3,12) >= 53, so a colouring of K_52 is known and one of K_53 or more would improve it.

## Why it matters

R(3,12) lies between 53 and 59 (DS1 Table Ia). The numbers R(3,k) ask for triangle-free graphs with no large independent set, the case studied most closely in Ramsey theory, and a better graph raises the lower bound directly.

Sources: [Small Ramsey Numbers, rev. 18, Table Ia](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2001 | upper | 59 | A. Lesser | A. Lesser, Theoretical and Computational Aspects of Ramsey Theory, Examensarbeten i Matematik, Matematiska Institutionen, Stockholms Universitet, 3, http://www2.math.su.se/gemensamt/grund/exjobb/matte/2001 (2001). (via Leaps in Bounds) |
| 2015 | lower | 53 | M. Kolodyazhny | M. Kolodyazhny, Novye Nizhnie Granitsy Chisel Ramseya R(3, 12) i R(3, 13) (in Russian), Matematicheskoye i Informacionnoe Modelirovanie, Tyumen, 14 (2015) 126-130. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the n x n adjacency matrix of the red graph, one line of n characters 0/1 per vertex (1 red, 0 blue), symmetric with a zero diagonal; n <= 2048.

Score: n, the number of vertices of the colouring; it proves R(3,12) >= n + 1 (larger is better).

```
python3 -I obb.py check ramsey-3-12 CERTIFICATE        # the checker, and the comparison with the best known value
cc -O3 -o ramsey_check checkers/ramsey_check.c && ./ramsey_check 3 12 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
