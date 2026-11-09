# 24. Ramsey number R(3,3,3,3,3)

Family: Multicolour Ramsey numbers. Benchmark problem: `multiramsey-3-3-3-3-3`.

**Best known:** R(3,3,3,3,3) ≥ 162, G. Exoo (1994). Also known: R(3,3,3,3,3) ≤ 307 (inequality 6.1.a).

**To beat it:** a colouring of the edges of K_162 with 5 colours and no monochromatic forbidden clique, which would show R(3,3,3,3,3) ≥ 163.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov).

## The problem

Find a colouring of the edges of K_n with 5 colours 0..4 in which colour c holds no complete graph K_(S_(c+1)), for (S_1, ..., S_5) = (3,3,3,3,3); it shows R(3,3,3,3,3) > n. The best known lower bound is R(3,3,3,3,3) >= 162, so a colouring of K_161 is known and one of K_162 or more would improve it.

## Why it matters

R_5(3), the five-colour triangle Ramsey number, lies between 162 and 307 (DS1 section 6.1.1). Exoo's 1994 colouring came from a Schur partition, the link between Schur numbers and multicolour Ramsey numbers of triangles.

Sources: [Small Ramsey Numbers, rev. 18, section 6.1.1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1); [Exoo, A lower bound for Schur numbers and multicolor Ramsey numbers of K3, Electron. J. Combin. 1 (1994) R8](https://doi.org/10.37236/1188).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1994 | lower | 162 | G. Exoo | DS1 rev. 18, Table XIa [Ex10] (via DS1) |
| undated | upper | 307 | inequality 6.1.a | DS1 rev. 18, section 6.1.1 (via DS1) |

## Check a certificate

Certificate format: Text file: the n x n colour matrix, one line of n characters per vertex; the character in row i, column j (i != j) is the colour of the edge {i,j}, a digit from 0 to r-1 (colour c must avoid K_(S_(c+1))), symmetric; diagonal characters are ignored (write 0 or -). n <= 2048 is practical.

Score: n, the number of vertices of the colouring; it proves R(3,3,3,3,3) >= n + 1 (larger is better).

```
python3 -I obb.py check multiramsey-3-3-3-3-3 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/multiramsey_check.py 3 3 3 3 3 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
