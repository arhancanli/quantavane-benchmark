# 27. Weak Schur number WS(5)

Family: Schur and van der Waerden numbers. Benchmark problem: `weak-schur-5`.

**Best known:** WS(5) ≥ 207, F. Rowley (2025).

**To beat it:** a partition of 1, ..., 208 into 5 weakly sum-free sets (no x + y = z with x ≠ y inside one set), which would show WS(5) ≥ 208.

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Colour 1, 2, ..., n with 5 colours so that no colour holds a solution of x + y = z with x != y, with n as large as possible; it shows WS(5) >= n. The best known lower bound is WS(5) >= 207, by Rowley (2025, in OEIS A072842); a colouring of 1..208 or more would improve it.

## Why it matters

WS(5) is the smallest open weak Schur number: the value 196 found by Eliahou and coauthors in 2012 was raised to 207 by Rowley in 2025 (a partition posted to OEIS A072842). Weak Schur numbers relax Schur's condition to sums of two distinct numbers, and each new Schur partition feeds the recursive constructions that bound them.

Sources: [Rowley, New lower bounds for weak Schur partitions, Integers 21 (2021) A59](https://arxiv.org/abs/2011.11292); [Leaps in Bounds, Schur and weak Schur numbers](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2006 | lower | 189 | P. F. Blanchard, F. Harary and R. Reis | P.F. Blanchard, F. Harary and R. Reis, Partitions into sum-free sets, Integers 6 (2006) #A7. (via Leaps in Bounds) |
| 2011-11 | lower | 196 | S. Eliahou, J. M. Marín, M. P. Revuelta and M. I. Sanz | S. Eliahou, J.M. Marín, M.P. Revuelta and M.I. Sanz, Weak Schur numbers and the search for G. W. Walker's lost partitions, Computers & Mathematics with Applications 63 (2012) 175-182. (via Leaps in Bounds) |
| 2025-08-29 | lower | 207 | F. Rowley | F. Rowley, comment with a partition of [1,207] into 5 weakly sum-free sets, Sequence A072842 in the OEIS, 2025-08-29. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the colours of 1..n in order, digits 0..4 (whitespace ignored).

Score: n, the length of the colouring; it proves WS(5) >= n (larger is better).

```
python3 -I obb.py check weak-schur-5 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/schur_check.py weak 5 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 207 | Rowley (2025, in OEIS A072842) (certificate from Leaps in Bounds, MIT) | record | 2026-11-08 | certs/lib_weak-schur-5-lower-207.txt (e35bcbb75659...) |
