# 91. Largest cap set in dimension 7

Family: Cap sets. Benchmark problem: `capset-n7`.

**Best known:** 236 points, A. R. Calderbank and P. C. Fishburn (1994).

**To beat it:** 237 points of F_3^7 with no three on a line (no x + y + z = 0 for distinct x, y, z).

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find as many points as possible in F_3^7 with no three distinct points on a line (no x + y + z = 0). The largest known cap set in dimension 7, by Calderbank and Fishburn (1994), has 236 points; a larger one improves it.

## Why it matters

Cap sets are the subject of the Ellenberg-Gijswijt breakthrough (2016) on their asymptotic size; the exact maximum is known only up to dimension 6. In dimension 7 the largest known cap set has 236 points (Calderbank and Fishburn 1994) against an upper bound of 288 (Thackeray 2022).

Sources: [Romera-Paredes et al., Nature 625 (2024)](https://doi.org/10.1038/s41586-023-06924-6); [Leaps in Bounds, cap-set](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1994-07 | lower | 236 | A. R. Calderbank and P. C. Fishburn | A.R. Calderbank and P.C. Fishburn, Maximal three-independent subsets of {0, 1, 2}^n, Designs, Codes and Cryptography 4 (1994) 203-211. (via Leaps in Bounds) |
| 2017-07 | upper | 291 | N. D. Versluis | N.D. Versluis, On the cap set problem: upper bounds on maximal cardinalities of caps in dimensions seven to ten, Bachelor's thesis, Delft University of Technology (2017). (via Leaps in Bounds) |
| 2022-06-20 | upper | 288 | H. R. Thackeray | H.(M.)R. Thackeray, The cap set problem: up to dimension 7, arXiv:2206.09804. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the points separated by whitespace, each as 7 digits 0-2 with nothing between them.

Score: the number of points (larger is better).

```
python3 -I obb.py check capset-n7 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/capset_check.py 7 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 236 | Calderbank and Fishburn (1994) (certificate from Leaps in Bounds, MIT) | record | 2026-11-08 | certs/lib_cap-set-7-lower-236.txt (3c3fc5029a61...) |
