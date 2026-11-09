# 26. Schur number S(7)

Family: Schur and van der Waerden numbers. Benchmark problem: `schur-7`.

**Best known:** S(7) ≥ 1696, F. Rowley (2021).

**To beat it:** a partition of 1, ..., 1697 into 7 sum-free sets, which would show S(7) ≥ 1697.

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Colour 1, 2, ..., n with 7 colours so that no colour holds a solution of x + y = z (x = y allowed), with n as large as possible; it shows S(7) >= n. The best known lower bound is S(7) >= 1696, by Rowley (2021); a colouring of 1..1697 or more would improve it.

## Why it matters

S(7) is the second open Schur number; Rowley's 2021 templates raised it from 1680 (Fredricksen and Sweet 2000) to 1696. Every partition for S(7) also colours a complete graph without monochromatic triangles in 7 colours, so it bounds R_7(3) too (DS1 section 6.1.1).

Sources: [Rowley, An improved lower bound for S(7) and some interesting templates, arXiv:2107.03560](https://arxiv.org/abs/2107.03560); [Leaps in Bounds, Schur and weak Schur numbers](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2000-05-18 | lower | 1680 | H. Fredricksen and M. M. Sweet | H. Fredricksen and M.M. Sweet, Symmetric Sum-Free Partitions and Lower Bounds for Schur Numbers, Electronic Journal of Combinatorics 7 (2000) #R32. (via Leaps in Bounds) |
| 2021-07-08 | lower | 1696 | F. Rowley | F. Rowley, An Improved Lower Bound for S(7) and Some Interesting Templates, arXiv:2107.03560. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the colours of 1..n in order, digits 0..6 (whitespace ignored).

Score: n, the length of the colouring; it proves S(7) >= n (larger is better).

```
python3 -I obb.py check schur-7 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/schur_check.py schur 7 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 1696 | Rowley (2021) (certificate from Leaps in Bounds, MIT) | record | 2026-11-08 | certs/lib_schur-7-lower-1696.txt (6d4794df0f86...) |
