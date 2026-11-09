# 60. 3 × 3 matrix multiplication with 22 multiplications

Family: Matrix multiplication. Benchmark problem: `matmul-3x3x3`.

**Best known:** rank ≤ 23, J. D. Laderman (1976). Also known: rank ≥ 19 (M. Bläser, 2003).

**To beat it:** a bilinear algorithm for 3 × 3 matrices with 22 multiplications over any field (non-commutative, so it applies recursively).

**Keeper:** [Yet another catalogue of fast matrix multiplication algorithms (A. Sedoglavic)](https://fmm.univ-lille.fr/), read 2026-11-09 15:58 +04 (version 1c55fea; algorithm pages read 16:13).

## The problem

Find a bilinear algorithm that multiplies two 3 x 3 matrices with non-commuting entries using as few multiplications as possible: a decomposition of the matrix multiplication tensor <3,3,3> into R products. Laderman's 1976 algorithm uses 23; the lower bound is 19 (Bläser 2003). Any field is accepted.

## Why it matters

Fifty years after Laderman found 23 multiplications for 3 × 3 matrices, nobody has found 22, though the best lower bound is 19 (Bläser 2003). Many different 23-multiplication algorithms are now known, none with 22, so 22 would be a landmark for fast matrix multiplication.

Sources: [Sedoglavic, catalogue of fast matrix multiplication algorithms, ⟨3×3×3:23⟩](https://fmm.univ-lille.fr/3x3x3.html); [Laderman, Bull. AMS 82 (1976)](https://doi.org/10.1090/S0002-9904-1976-13988-2).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| undated | upper | 27 | the schoolbook method | the catalogue's naive tensor decomposition rank (via fmm.univ-lille.fr) |
| 1976 | upper | 23 | J. D. Laderman | A noncommutative algorithm for multiplying 3×3 matrices using 23 multiplications, Bull. AMS 82 (1976) 126-128 (via fmm.univ-lille.fr) |
| 2003 | lower | 19 | M. Bläser | On the complexity of the multiplication of matrices of small formats, J. Complexity 19 (2003) 43-60 |

## Check a certificate

Certificate format: JSON {"field": F, "terms": [[U, V, W], ...]}: F is "Q", "Q(i)" or "GF(p)"; U is N x M, V is M x P and W is N x P, lists of rows; entries are integers or strings "a/b" (over Q(i) also pairs [re, im]); product r is (sum U_r[i][j] A[i][j]) (sum V_r[j][k] B[j][k]) and C[i][k] = sum_r W_r[i][k] times product r.

Score: R, the number of multiplications (smaller is better).

```
python3 -I obb.py check matmul-3x3x3 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/matmul_check.py 3 3 3 any CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 23 | J. D. Laderman (1976) | record | 2026-11-09 | certs/fmm_3x3x3_23.json (c453ae32b9d8...) |
