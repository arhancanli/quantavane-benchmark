# 92. Largest cap set in dimension 8

Family: Cap sets. Benchmark problem: `capset-n8`.

**Best known:** 512 points, B. Romera-Paredes et al. (FunSearch, 2023).

**To beat it:** 513 points of F_3^8 with no three on a line (no x + y + z = 0 for distinct x, y, z).

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find as many points as possible in F_3^8 with no three distinct points on a line (no x + y + z = 0). The largest known cap set in dimension 8, by Romera-Paredes et al. (2023, FunSearch), has 512 points; a larger one improves it.

## Why it matters

Cap sets are the subject of the Ellenberg-Gijswijt breakthrough (2016) on their asymptotic size; the exact maximum is known only up to dimension 6. In dimension 8 FunSearch's 512 points (2023), found by a search guided by a language model, beat Edel and Bierbrauer's 496 from 2001.

Sources: [Romera-Paredes et al., Nature 625 (2024)](https://doi.org/10.1038/s41586-023-06924-6); [Leaps in Bounds, cap-set](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2001-07 | lower | 496 | Y. Edel and J. Bierbrauer | Y. Edel and J. Bierbrauer, Large caps in small spaces, Designs, Codes and Cryptography 23 (2001) 197-212. (via Leaps in Bounds) |
| 2017-07 | upper | 771 | N. D. Versluis | N.D. Versluis, On the cap set problem: upper bounds on maximal cardinalities of caps in dimensions seven to ten, Bachelor's thesis, Delft University of Technology (2017). (via Leaps in Bounds) |
| 2023-12-14 | lower | 512 | B. Romera-Paredes et al. (FunSearch) | B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M.P. Kumar, E. Dupont, F.J.R. Ruiz, J.S. Ellenberg, P. Wang, O. Fawzi, P. Kohli and A. Fawzi, Mathematical discoveries from program search with large language models, Nature 625 (2024) 468-475. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the points separated by whitespace, each as 8 digits 0-2 with nothing between them.

Score: the number of points (larger is better).

```
python3 -I obb.py check capset-n8 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/capset_check.py 8 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 512 | Romera-Paredes et al. (2023, FunSearch) (certificate from Leaps in Bounds, MIT) | record | 2026-11-08 | certs/lib_cap-set-8-lower-512.txt (238d59d3199b...) |
