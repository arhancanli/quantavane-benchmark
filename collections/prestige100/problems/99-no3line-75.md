# 99. 150 points on the 75 × 75 grid with no three in a line

Family: No-three-in-line. Benchmark problem: `no3line-75`.

**Best known:** 148 points, the 74 × 74 solution (T. Prellberg, 2026) placed in the 75 × 75 grid. Also known: 150 (two per row).

**To beat it:** 150 points of the 75 × 75 grid, no three on any line.

**Keeper:** [No-three-in-line records (A. Flammenkamp), via Leaps in Bounds](http://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html), read 2026-11-09 15:49 +04 (as recorded by Leaps in Bounds at commit a5bbf82). Also read: [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Place as many points as possible on the 75 x 75 grid with no three on a line; at most 150 are possible. Solutions with 2n points are known for every n from 2 to 78 except 75 and 77; for n = 75 the best known has 148 points, from the 148-point set for n = 74 (Prellberg, 2026), which fits in the 75 x 75 grid. A set with more points improves it, and 150 would settle the cell.

## Why it matters

Dudeney's no-three-in-line puzzle (1917) asks whether 2n points with no three collinear fit on every n × n grid; it is conjectured to fail for large n. On 9 Nov 2026, 75 is the smallest n for which no 2n solution is listed, with 74, 76 and 78 solved in 2026.

Sources: [A. Flammenkamp, no-three-in-line records](http://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html); [Leaps in Bounds, no-three-in-line](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1917 | - | - | H. E. Dudeney | Amusements in Mathematics (1917): the puzzle for the 8 × 8 board |
| 2026-07-20 | lower | 148 (74 × 74 grid) | T. Prellberg | recorded on the no-three-in-line records page; as recorded by Leaps in Bounds (via Leaps in Bounds) |
| 2026-08-10 | lower | 152 (76 × 76 grid) | M. Heule | recorded on the no-three-in-line records page; as recorded by Leaps in Bounds (via Leaps in Bounds) |
| 2026-10-28 | lower | 156 (78 × 78 grid) | T. Prellberg | recorded on the no-three-in-line records page; as recorded by Leaps in Bounds (via Leaps in Bounds) |
| 2026-11-09 | lower | 148 (75 × 75 grid) | the 74 × 74 solution placed in the larger grid | no 150-point solution is listed for n = 75 (Leaps in Bounds at a5bbf82) (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the points separated by whitespace, each written x,y with 0 <= x, y < 75.

Score: the number of points (larger is better).

```
python3 -I obb.py check no3line-75 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/no3line_check.py 75 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 148 | embedding of the smaller grid's record (certificate from Leaps in Bounds, MIT) | record | 2026-11-08 | certs/lib_no-three-in-line-75-lower-148.txt (3dd21be9210f...) |
