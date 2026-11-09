# 64. Hadamard matrix of order 892

Family: Hadamard matrices. Benchmark problem: `hadamard-892`.

**Best known:** none known, none.

**To beat it:** a 892 × 892 matrix of ±1 entries with H H^T = 892 I.

**Keeper:** [Optimization constants in mathematics, constant 23a (T. Tao et al.)](https://teorth.github.io/optimizationproblems/constants/23a.html), read 2026-11-09 15:58 +04 (page source at main (README at 87b4ebb)).

## The problem

Find a 892 x 892 matrix H with entries +1 and -1 and H H^T = 892 I. The Hadamard conjecture says one exists for every multiple of 4, but none of order 892 is known. A valid matrix scores 1 and settles the order.

## Why it matters

892 is the third smallest order with no known Hadamard matrix (Cati and Pasechnik, via Tao et al. 23a). The Hadamard conjecture predicts a matrix for every multiple of 4, and each settled order narrows the list of exceptions.

Sources: [Tao et al., optimization constants 23a](https://teorth.github.io/optimizationproblems/constants/23a.html); [Cati and Pasechnik, arXiv:2411.18897](https://arxiv.org/abs/2411.18897).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1893 | - | - | J. Hadamard | the determinant bound behind the definition |
| 2024 | - | 892 open | D. Cati and D. V. Pasechnik | A database of constructions of Hadamard matrices, arXiv:2411.18897 (open orders up to 1208: 668, 716, 892, 1132) (via Tao et al., 23a) |

## Check a certificate

Certificate format: Text file: 892 rows of 892 entries, written as + and - characters or as 1 and -1 separated by spaces.

Score: 1 for a Hadamard matrix of this order; nothing is known, so the best known value is 0.

```
python3 -I obb.py check hadamard-892 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/hadamard_check.py 892 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
