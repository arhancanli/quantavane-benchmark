# 62. Hadamard matrix of order 668

Family: Hadamard matrices. Benchmark problem: `hadamard-668`.

**Best known:** none known, none.

**To beat it:** a 668 × 668 matrix of ±1 entries with H H^T = 668 I.

**Keeper:** [Optimization constants in mathematics, constant 23a (T. Tao et al.)](https://teorth.github.io/optimizationproblems/constants/23a.html), read 2026-11-09 15:58 +04 (page source at main (README at 87b4ebb)).

## The problem

Find a 668 x 668 matrix H with entries +1 and -1 and H H^T = 668 I. The Hadamard conjecture says one exists for every multiple of 4, but none of order 668 is known. It is the smallest order for which none is known. A valid matrix scores 1 and settles the order.

## Why it matters

668 is the smallest order for which no Hadamard matrix is known (Tao et al., constant 23a, citing Cati and Pasechnik); the previous smallest open order, 428, was settled by Kharaghani and Tayfeh-Rezaie in 2005. The Hadamard conjecture, open since Paley (1933), says one exists for every multiple of 4, so a 668 × 668 matrix would remove its smallest exception.

Sources: [Tao et al., optimization constants 23a](https://teorth.github.io/optimizationproblems/constants/23a.html); [Cati and Pasechnik, arXiv:2411.18897](https://arxiv.org/abs/2411.18897).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1893 | - | - | J. Hadamard | the determinant bound behind the definition |
| 1933 | - | - | R. E. A. C. Paley | the conjecture that Hadamard matrices exist for every multiple of 4 |
| 2005 | - | 428 settled | H. Kharaghani and B. Tayfeh-Rezaie | A Hadamard matrix of order 428, J. Combin. Des. 13 (2005) 435-440; 668 became the smallest open order |
| 2024 | - | 668 open | D. Cati and D. V. Pasechnik | A database of constructions of Hadamard matrices, arXiv:2411.18897 (open orders up to 1208: 668, 716, 892, 1132) (via Tao et al., 23a) |

## Check a certificate

Certificate format: Text file: 668 rows of 668 entries, written as + and - characters or as 1 and -1 separated by spaces.

Score: 1 for a Hadamard matrix of this order; nothing is known, so the best known value is 0.

```
python3 -I obb.py check hadamard-668 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/hadamard_check.py 668 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
