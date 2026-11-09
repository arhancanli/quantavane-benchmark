# 23. Ramsey number R(3,3,5)

Family: Multicolour Ramsey numbers. Benchmark problem: `multiramsey-3-3-5`.

**Best known:** R(3,3,5) ≥ 45, G. Exoo (1989). Also known: R(3,3,5) ≤ 57 (inequality 6.1.a).

**To beat it:** a colouring of the edges of K_45 with 3 colours and no monochromatic forbidden clique, which would show R(3,3,5) ≥ 46.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov).

## The problem

Find a colouring of the edges of K_n with 3 colours 0..2 in which colour c holds no complete graph K_(S_(c+1)), for (S_1, ..., S_3) = (3,3,5); it shows R(3,3,5) > n. The best known lower bound is R(3,3,5) >= 45, so a colouring of K_44 is known and one of K_45 or more would improve it.

## Why it matters

After R(3,3,4) = 30 was settled by computer in 2016 (Codish, Frank, Itzhakov and Miller), R(3,3,5) is the smallest open three-colour case of the form R(3,3,k): 45 ≤ R(3,3,5) ≤ 57 (DS1 item 6.1.2.d). The lower bound is Exoo's colouring.

Sources: [Small Ramsey Numbers, rev. 18, items 6.1.2(b) and (d)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1989 | lower | 45 | G. Exoo | DS1 rev. 18, Table XIb [Ex2] (via DS1) |
| undated | upper | 57 | inequality 6.1.a | DS1 rev. 18, item 6.1.2(d) (via DS1) |

## Check a certificate

Certificate format: Text file: the n x n colour matrix, one line of n characters per vertex; the character in row i, column j (i != j) is the colour of the edge {i,j}, a digit from 0 to r-1 (colour c must avoid K_(S_(c+1))), symmetric; diagonal characters are ignored (write 0 or -). n <= 2048 is practical.

Score: n, the number of vertices of the colouring; it proves R(3,3,5) >= n + 1 (larger is better).

```
python3 -I obb.py check multiramsey-3-3-5 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/multiramsey_check.py 3 3 5 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
