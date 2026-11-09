# 22. Ramsey number R(4,4,4)

Family: Multicolour Ramsey numbers. Benchmark problem: `multiramsey-4-4-4`.

**Best known:** R(4,4,4) ≥ 128, R. Hill and R. W. Irving (1982). Also known: R(4,4,4) ≤ 229 (Boza, 2026).

**To beat it:** a colouring of the edges of K_128 with 3 colours and no monochromatic forbidden clique, which would show R(4,4,4) ≥ 129.

**Keeper:** [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04 (revision 18 (24 Apr 2026); the PDF downloaded on 9 Nov 2026 (SHA-256 9519a676ee381f02...) is identical to our copy of 4 Nov).

## The problem

Find a colouring of the edges of K_n with 3 colours 0..2 in which colour c holds no complete graph K_(S_(c+1)), for (S_1, ..., S_3) = (4,4,4); it shows R(4,4,4) > n. The best known lower bound is R(4,4,4) >= 128, so a colouring of K_127 is known and one of K_128 or more would improve it.

## Why it matters

R_3(4) = R(4,4,4), the three-colour Ramsey number of K_4, lies between 128 and 229 (DS1 section 6.1.1). The lower bound is Hill and Irving's 1982 cubic-residue colouring of K_127.

Sources: [Small Ramsey Numbers, rev. 18, section 6.1.1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1982 | lower | 128 | R. Hill and R. W. Irving | DS1 rev. 18, Table XIa [HiIr] (via DS1) |
| undated | upper | 230 | inequality 6.1.a | DS1 rev. 18, section 6.1.1 (via DS1) |
| 2026 | upper | 229 | L. Boza | DS1 rev. 18, section 6.1.1 [Boza9] (via DS1) |

## Check a certificate

Certificate format: Text file: the n x n colour matrix, one line of n characters per vertex; the character in row i, column j (i != j) is the colour of the edge {i,j}, a digit from 0 to r-1 (colour c must avoid K_(S_(c+1))), symmetric; diagonal characters are ignored (write 0 or -). n <= 2048 is practical.

Score: n, the number of vertices of the colouring; it proves R(4,4,4) >= n + 1 (larger is better).

```
python3 -I obb.py check multiramsey-4-4-4 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/multiramsey_check.py 4 4 4 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 127 | [HiIr] (reference key of the survey) (file built by Quantavane's code) | record | 2026-11-08 | refs/classic_multiramsey_444_n127.txt (2c97e6ba4074...) |
