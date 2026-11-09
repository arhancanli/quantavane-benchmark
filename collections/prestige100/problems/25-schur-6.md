# 25. Schur number S(6)

Family: Schur and van der Waerden numbers. Benchmark problem: `schur-6`.

**Best known:** S(6) ≥ 538, A. McKenna (4 Nov 2026).

**To beat it:** a partition of 1, ..., 539 into 6 sum-free sets (no x + y = z inside one set), which would show S(6) ≥ 539.

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Colour 1, 2, ..., n with 6 colours so that no colour holds a solution of x + y = z, with n as large as possible; it shows S(6) >= n. The best known lower bound is S(6) >= 538, by McKenna (2026); a colouring of 1..539 or more would improve it.

## Why it matters

Schur's 1916 theorem began Ramsey theory on the integers; S(5) = 160 was settled only in 2017 by a 2-petabyte SAT proof (Heule), so S(6) is the first open Schur number. Its lower bound stood at 536 from 2000 until October 2026 and has moved twice since.

Sources: [Heule, Schur Number Five, AAAI 2018, arXiv:1711.08076](https://arxiv.org/abs/1711.08076); [Leaps in Bounds, Schur and weak Schur numbers](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2000-05-18 | lower | 536 | H. Fredricksen and M. M. Sweet | H. Fredricksen and M.M. Sweet, Symmetric Sum-Free Partitions and Lower Bounds for Schur Numbers, Electronic Journal of Combinatorics 7 (2000) #R32. (via Leaps in Bounds) |
| 2026-10-22 | lower | 537 | Z. Chen, L. Zhu and F. Long | Z. Chen, L. Zhu and F. Long, A new lower bound for the sixth Schur number: S(6) >= 537, arXiv:2610.31362. (via Leaps in Bounds) |
| 2026-11-04 | lower | 538 | A. McKenna | A. McKenna, The sixth Schur number is at least 538, Zenodo. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the colours of 1..n in order, digits 0..5 (whitespace ignored).

Score: n, the length of the colouring; it proves S(6) >= n (larger is better).

```
python3 -I obb.py check schur-6 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/schur_check.py schur 6 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 538 | A. McKenna (4 Nov 2026) | record | 2026-11-09 | certs/derived_mckenna_schur6_538.txt (8ae15c5e54f0...) |
| 537 | Chen, Zhu and Long (2026) (certificate from Leaps in Bounds, MIT) | below the record | 2026-11-08 | certs/lib_schur-6-lower-537.txt (c6266f6d369e...) |
