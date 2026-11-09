# 89. Shortest Golomb ruler with 29 marks

Family: Golomb rulers. Benchmark problem: `golomb-29`.

**Best known:** length ≤ 623, M. D. Atkinson and A. Hassenklover (1984).

**To beat it:** 29 marks on a ruler of length 622 or less with all pairwise distances distinct.

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Place 29 marks on a ruler (integers) so that all differences between two marks are distinct, with the ruler as short as possible. The shortest known ruler with 29 marks has length 623 (Atkinson and Hassenklover, 1984, in J. B. Shearer's table); a shorter one improves it. Rulers with up to 28 marks are proved optimal.

## Why it matters

Optimal Golomb rulers are known up to 28 marks, the last ones by distributed.net's volunteer searches (OGR-24 to OGR-28, finished in 2022). For 29 marks the best known ruler, of length 623, dates from Atkinson and Hassenklover's 1984 report, and any shorter ruler would be a new record.

Sources: [distributed.net, OGR-28 completed (2022)](https://blogs.distributed.net/2022/11/23/03/28/bovine/); [Leaps in Bounds, golomb-ruler](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1984-10 | upper | 623 | M. D. Atkinson and A. Hassenklover | M.D. Atkinson and A. Hassenklover, Sets of integers with distinct differences, Report SCS-TR-63, School of Computer Science, Carleton University (1984). (via Leaps in Bounds) |
| 2022-11-23 | - | 28 marks solved | distributed.net | OGR-28 completed: the optimal 28-mark ruler has length 585 (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the 29 marks, integers separated by whitespace or commas.

Score: the length (largest minus smallest mark; smaller is better).

```
python3 -I obb.py check golomb-29 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/golomb_check.py 29 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
