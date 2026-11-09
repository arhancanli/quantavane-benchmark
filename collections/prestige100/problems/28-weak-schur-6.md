# 28. Weak Schur number WS(6)

Family: Schur and van der Waerden numbers. Benchmark problem: `weak-schur-6`.

**Best known:** WS(6) ≥ 650, S. E. Rodrigo (2026).

**To beat it:** a partition of 1, ..., 651 into 6 weakly sum-free sets (no x + y = z with x ≠ y inside one set), which would show WS(6) ≥ 651.

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Colour 1, 2, ..., n with 6 colours so that no colour holds a solution of x + y = z with x != y, with n as large as possible; it shows WS(6) >= n. The best known lower bound is WS(6) >= 650, by Rodrigo (2026); a colouring of 1..651 or more would improve it.

## Why it matters

WS(6) rose from 572 (2012) through 642, 646 and 650 as search methods improved; the newest value is Rodrigo's 2026 partition. Weak Schur numbers relax Schur's condition to sums of two distinct numbers, and each new Schur partition feeds the recursive constructions that bound them.

Sources: [Rowley, New lower bounds for weak Schur partitions, Integers 21 (2021) A59](https://arxiv.org/abs/2011.11292); [Leaps in Bounds, Schur and weak Schur numbers](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2011-11 | lower | 572 | S. Eliahou, J. M. Marín, M. P. Revuelta and M. I. Sanz | S. Eliahou, J.M. Marín, M.P. Revuelta and M.I. Sanz, Weak Schur numbers and the search for G. W. Walker's lost partitions, Computers & Mathematics with Applications 63 (2012) 175-182. (via Leaps in Bounds) |
| 2012 | lower | 574 | D. Robilliard, C. Fonlupt, V. Marion-Poty and A. Boumaza | D. Robilliard, C. Fonlupt, V. Marion-Poty and A. Boumaza, A Multilevel Tabu Search with Backtracking for Exploring Weak Schur Numbers, Artificial Evolution (EA 2011), Lecture Notes in Computer Science 7401 (2012) 109-119. (via Leaps in Bounds) |
| 2012-07 | lower | 581 | R. Le Bras, C. P. Gomes and B. Selman | R. Le Bras, C.P. Gomes and B. Selman, From Streamlined Combinatorial Search to Efficient Constructive Procedures, Proceedings of the AAAI Conference on Artificial Intelligence 26 (2012) 499-506. (via Leaps in Bounds) |
| 2013-04 | lower | 582 | S. Eliahou, C. Fonlupt, J. Fromentin, V. Marion-Poty, D. Robilliard and F. Teytaud | S. Eliahou, C. Fonlupt, J. Fromentin, V. Marion-Poty, D. Robilliard and F. Teytaud, Investigating Monte-Carlo Methods on the Weak Schur Problem, EvoCOP 2013, Lecture Notes in Computer Science 7832 (2013) 191-201. (via Leaps in Bounds) |
| 2020-11-23 | lower | 642 | F. Rowley | F. Rowley, New lower bounds for weak Schur partitions, Integers 21 (2021) #A59, arXiv:2011.11292. (via Leaps in Bounds) |
| 2021-12-06 | lower | 646 | R. Ageron, P. Casteras, T. Pellerin, Y. Portella, A. Rimmel and J. Tomasik | R. Ageron, P. Casteras, T. Pellerin, Y. Portella, A. Rimmel and J. Tomasik, New lower bounds for Schur and weak Schur numbers, arXiv:2112.03175. (via Leaps in Bounds) |
| 2026-06-10 | lower | 650 | S. E. Rodrigo | S.E. Rodrigo, A new lower bound for the sixth weak Schur number: WS(6) >= 650, Zenodo preprint. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the colours of 1..n in order, digits 0..5 (whitespace ignored).

Score: n, the length of the colouring; it proves WS(6) >= n (larger is better).

```
python3 -I obb.py check weak-schur-6 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/schur_check.py weak 6 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 650 | Rodrigo (2026) (certificate from Leaps in Bounds, MIT) | record | 2026-11-08 | certs/lib_weak-schur-6-lower-650.txt (300891d3d338...) |
