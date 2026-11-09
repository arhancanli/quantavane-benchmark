# 61. 4 × 4 matrix multiplication with 47 multiplications in characteristic 0

Family: Matrix multiplication. Benchmark problem: `matmul-4x4x4`.

**Best known:** rank ≤ 48 over the rationals, A. Novikov et al. (AlphaEvolve, 2025), as credited by the catalogue.

**To beat it:** a bilinear algorithm for 4 × 4 matrices with 47 multiplications over the rationals or the complex rationals.

**Keeper:** [Yet another catalogue of fast matrix multiplication algorithms (A. Sedoglavic)](https://fmm.univ-lille.fr/), read 2026-11-09 15:58 +04 (version 1c55fea; algorithm pages read 16:13).

## The problem

Find a bilinear algorithm that multiplies two 4 x 4 matrices with non-commuting entries over the rationals (or the Gaussian rationals) with as few multiplications as possible. The catalogue's best is 48 (credited to Novikov et al., AlphaEvolve, 2025; its explicit algorithm has rational coefficients); 47 is known only over GF(2) (Fawzi et al., 2022) and does not count here.

## Why it matters

Strassen's 1969 algorithm gives 49 multiplications for 4 × 4 matrices; AlphaTensor found 47 in 2022 but only over the two-element field, and AlphaEvolve's 48 in 2025 was the first improvement in characteristic 0. A 47 in characteristic 0 would improve AlphaEvolve's 48 and bring the GF(2) result to the rationals, for every recursive algorithm built on 4 × 4 blocks.

Sources: [Fawzi et al., Nature 610 (2022)](https://doi.org/10.1038/s41586-022-05172-4); [Novikov et al., AlphaEvolve, arXiv:2506.13131](https://arxiv.org/abs/2506.13131); [catalogue ⟨4×4×4:48⟩](https://fmm.univ-lille.fr/4x4x4.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1969 | upper | 49 | V. Strassen | Strassen's algorithm applied twice (7 × 7 = 49) |
| 2022 | upper | 47 (GF(2) only) | A. Fawzi et al. (AlphaTensor) | Nature 610 (2022) 47-53 |
| 2025 | upper | 48 | A. Novikov et al. (AlphaEvolve) | arXiv:2506.13131; the catalogue's explicit 48-term algorithm has rational coefficients (±1, ±1/2, ±1/4, ±1/8) (via fmm.univ-lille.fr) |

## Check a certificate

Certificate format: JSON {"field": F, "terms": [[U, V, W], ...]}: F is "Q", "Q(i)" or "GF(p)"; U is N x M, V is M x P and W is N x P, lists of rows; entries are integers or strings "a/b" (over Q(i) also pairs [re, im]); product r is (sum U_r[i][j] A[i][j]) (sum V_r[j][k] B[j][k]) and C[i][k] = sum_r W_r[i][k] times product r.

Score: R, the number of multiplications (smaller is better).

```
python3 -I obb.py check matmul-4x4x4 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/matmul_check.py 4 4 4 char0 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 48 | A. Novikov et al. (AlphaEvolve, 2025), the catalogue's rational form | record | 2026-11-09 | certs/fmm_4x4x4_48.json (a7908dd19279...) |
