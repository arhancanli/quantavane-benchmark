# 31. Weak Schur number WS(9)

Family: Schur and van der Waerden numbers. Benchmark problem: `weak-schur-9`.

**Best known:** WS(9) ≥ 22620, A. Canli (Quantavane), 8 Nov 2026.

**To beat it:** a partition of 1, ..., 22621 into 9 weakly sum-free sets (no x + y = z with x ≠ y inside one set), which would show WS(9) ≥ 22621.

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

**Quantavane holds this record.** Quantavane's partition of 1..22620 (8 Nov 2026), built with Ageron et al.'s published construction on A. McKenna's partition for S(6) ≥ 538 and checked by three programs; Leaps in Bounds verified and merged the certificate on 9 Nov 2026 (its table of published values still shows 22536).

## The problem

Colour 1, 2, ..., n with 9 colours so that no colour holds a solution of x + y = z with x != y, with n as large as possible; it shows WS(9) >= n. The best known lower bound is WS(9) >= 22620, by Quantavane (8 Nov 2026); a colouring of 1..22621 or more would improve it.

## Why it matters

WS(9) was 22536 from Ageron and coauthors' 2021 templates until the new six-colour Schur partitions of 2026. Weak Schur numbers relax Schur's condition to sums of two distinct numbers, and each new Schur partition feeds the recursive constructions that bound them.

Sources: [Rowley, New lower bounds for weak Schur partitions, Integers 21 (2021) A59](https://arxiv.org/abs/2011.11292); [Leaps in Bounds, Schur and weak Schur numbers](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2017 | lower | 15596 | F. Rafilipojaona | F. Rafilipojaona, Lower bounds on the weak Schur numbers up to 9 colors, Integers 17 (2017) #A39. (via Leaps in Bounds) |
| 2020-11-23 | lower | 21848 | F. Rowley | F. Rowley, New lower bounds for weak Schur partitions, Integers 21 (2021) #A59, arXiv:2011.11292. (via Leaps in Bounds) |
| 2021-12-06 | lower | 22536 | R. Ageron, P. Casteras, T. Pellerin, Y. Portella, A. Rimmel and J. Tomasik | R. Ageron, P. Casteras, T. Pellerin, Y. Portella, A. Rimmel and J. Tomasik, New lower bounds for Schur and weak Schur numbers, arXiv:2112.03175. (via Leaps in Bounds) |
| 2026-11-08 | lower | 22578 | A. Canli (Quantavane) | Rowley's and Ageron et al.'s constructions on Chen, Zhu and Long's S(6) ≥ 537 partition (the first version of Leaps in Bounds pull request #50) |
| 2026-11-08 | lower | 22620 | A. Canli (Quantavane) | the same constructions on McKenna's S(6) ≥ 538 partition; certificate merged into Leaps in Bounds on 9 Nov 2026 (pull request #50) (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the colours of 1..n in order, digits 0..8 (whitespace ignored).

Score: n, the length of the colouring; it proves WS(9) >= n (larger is better).

```
python3 -I obb.py check weak-schur-9 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/schur_check.py weak 9 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 22620 | A. Canli (Quantavane), 8 Nov 2026 | record | 2026-11-09 | certs/lib_weak-schur-9-lower-22620.txt (5b6e7c96b0a8...) |
