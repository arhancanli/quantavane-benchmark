# 21. Ramsey number R(3,3,3,3)

Family: Multicolour Ramsey numbers. Benchmark problem: `multiramsey-3-3-3-3`.

**Best known:** R(3,3,3,3) ≥ 51, F. R. K. Chung (1973). Also known: R(3,3,3,3) ≤ 62 (Fettes, Kramer and Radziszowski, 2004).

**To beat it:** a colouring of the edges of K_51 with 4 colours and no monochromatic forbidden clique, which would show R(3,3,3,3) ≥ 52.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov).

## The problem

Find a colouring of the edges of K_n with 4 colours 0..3 in which colour c holds no complete graph K_(S_(c+1)), for (S_1, ..., S_4) = (3,3,3,3); it shows R(3,3,3,3) > n. The best known lower bound is R(3,3,3,3) >= 51, so a colouring of K_50 is known and one of K_51 or more would improve it.

## Why it matters

DS1 calls R_4(3) = R(3,3,3,3) 'the most studied and intriguing open case' of the multicolour Ramsey numbers (section 6.1.1): 51 ≤ R_4(3) ≤ 62. Chung's 1973 colouring has not been beaten, and group-partition constructions provably cannot beat it (DS1 cites Ana1, Ana2).

Sources: [Small Ramsey Numbers, rev. 18, section 6.1.1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1973 | lower | 51 | F. R. K. Chung | DS1 rev. 18 [Chu1] (with a typo in the displayed matrix found by C. Frederick in 2003) (via DS1) |
| 1973 | upper | 66 | inequality 6.1.a | DS1 rev. 18, section 6.1.1 (via DS1) |
| 1974 | upper | 65 | J. Folkman | DS1 rev. 18 [Fol] (via DS1) |
| 1995 | upper | 64 | A. Sánchez-Flores | DS1 rev. 18 [Sán] (via DS1) |
| 2004 | upper | 62 | S. Fettes, R. L. Kramer and S. P. Radziszowski | DS1 rev. 18 [FeKR] (via DS1) |

## Check a certificate

Certificate format: Text file: the n x n colour matrix, one line of n characters per vertex; the character in row i, column j (i != j) is the colour of the edge {i,j}, a digit from 0 to r-1 (colour c must avoid K_(S_(c+1))), symmetric; diagonal characters are ignored (write 0 or -). n <= 2048 is practical.

Score: n, the number of vertices of the colouring; it proves R(3,3,3,3) >= n + 1 (larger is better).

```
python3 -I obb.py check multiramsey-3-3-3-3 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/multiramsey_check.py 3 3 3 3 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
