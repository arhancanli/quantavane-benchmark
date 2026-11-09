# 30. Weak Schur number WS(8)

Family: Schur and van der Waerden numbers. Benchmark problem: `weak-schur-8`.

**Best known:** WS(8) ≥ 7002, A. Canli (Quantavane), 8 Nov 2026.

**To beat it:** a partition of 1, ..., 7003 into 8 weakly sum-free sets (no x + y = z with x ≠ y inside one set), which would show WS(8) ≥ 7003.

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

**Quantavane holds this record.** Quantavane's partition of 1..7002 (8 Nov 2026), built with Rowley's published construction on A. McKenna's partition for S(6) ≥ 538 and checked by three programs; Leaps in Bounds verified and merged the certificate on 9 Nov 2026 (its table of published values still shows 6976).

## The problem

Colour 1, 2, ..., n with 8 colours so that no colour holds a solution of x + y = z with x != y, with n as large as possible; it shows WS(8) >= n. The best known lower bound is WS(8) >= 7002, by Quantavane (8 Nov 2026); a colouring of 1..7003 or more would improve it.

## Why it matters

WS(8) was 6976 from Rowley's 2020 construction until the new six-colour Schur partitions of 2026. Weak Schur numbers relax Schur's condition to sums of two distinct numbers, and each new Schur partition feeds the recursive constructions that bound them.

Sources: [Rowley, New lower bounds for weak Schur partitions, Integers 21 (2021) A59](https://arxiv.org/abs/2011.11292); [Leaps in Bounds, Schur and weak Schur numbers](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2015-09-17 | lower | 5105 | B. Bouzy | B. Bouzy, An Abstract Procedure to Compute Weak Schur Number Lower Bounds, LIPADE technical report TR-2 (2015). (via Leaps in Bounds) |
| 2017 | lower | 5201 | F. Rafilipojaona | F. Rafilipojaona, Lower bounds on the weak Schur numbers up to 9 colors, Integers 17 (2017) #A39. (via Leaps in Bounds) |
| 2020-11-23 | lower | 6976 | F. Rowley | F. Rowley, New lower bounds for weak Schur partitions, Integers 21 (2021) #A59, arXiv:2011.11292. (via Leaps in Bounds) |
| 2026-11-08 | lower | 6989 | A. Canli (Quantavane) | Rowley's and Ageron et al.'s constructions on Chen, Zhu and Long's S(6) ≥ 537 partition (the first version of Leaps in Bounds pull request #50) |
| 2026-11-08 | lower | 7002 | A. Canli (Quantavane) | the same constructions on McKenna's S(6) ≥ 538 partition; certificate merged into Leaps in Bounds on 9 Nov 2026 (pull request #50) (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the colours of 1..n in order, digits 0..7 (whitespace ignored).

Score: n, the length of the colouring; it proves WS(8) >= n (larger is better).

```
python3 -I obb.py check weak-schur-8 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/schur_check.py weak 8 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 7002 | A. Canli (Quantavane), 8 Nov 2026 | record | 2026-11-09 | certs/lib_weak-schur-8-lower-7002.txt (c2d529a4f41b...) |
