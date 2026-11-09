# Distinct triangle areas in the triangular grid

`tri-areas` · Discrete geometry · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **9** (maximize), Quantavane (Arhan Canli), 9 November 2026: 9 points of T_30 with distinct nonzero triangle areas, found by randomized greedy construction with local search (tools/tri_distinct_search.py, mode areas)

## Statement

In the triangular grid T_n (the points a + b e^(i pi/3) with integers a, b >= 0 and a + b <= n - 1), the area of a triangle with vertices in T_n is an integer multiple |da1 db2 - da2 db1| of the unit triangle's area sqrt(3)/4. Let t(n) be the largest number of points of T_n such that every three of them span a triangle of nonzero area and all these C(t,3) areas are different. Determine t(n); the headline cell is n = 30: find 10 or more points of T_30 with all triangle areas distinct and nonzero.

## Why it is interesting

Erdos and Purdy asked how many distinct areas the triangles of n points must span; the grid version, choosing as many grid points as possible with all triangle areas different, is a two-dimensional relative of Sidon sets (all sums different) and Golomb rulers, and its square-grid form appears in the OEIS (A322740, smallest rectangle containing n points with distinct triangle areas). In the triangular grid areas are measured in units of the unit triangle and are the absolute values of 2 x 2 determinants of lattice vectors, so the problem asks for point sets whose determinant triples never repeat; with all areas at most (n - 1)^2, C(t,3) <= (n - 1)^2 gives t(n) = O(n^(2/3)), and how close the truth is to that bound is open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/tri-areas.json`](../novelty/tri-areas.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"distinct areas" AND all:triangles AND all:lattice`: 0 results
  - `all:"distinct areas" AND all:grid AND all:points`: 0 results
- OEIS, 3 searches:
  - `1,3,3,4,4,5,5,5,6,6,6,7,7,7`: 0 results
  - `3,3,4,4,5,5,5,6,6,6,7,7,7`: 10 results (A000267, A353090, A249728, A096137, A166872)
  - `triangles distinct areas grid`: 10 results (A320544, A322740, A372915, A272624, A272625)
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no entry.

Closest work found, and how this problem differs:
- OEIS A322740: least area of a grid rectangle containing n points whose triangles all have distinct areas (square grid; a different objective on a different lattice).

Verdict: new. The sequence t(n) is not in the OEIS and no paper on distinct triangle areas in the triangular grid was found; the square-grid question in A322740 is the closest.

## First values

| n | t(n) | how |
| --- | --- | --- |
| 1 | 1 | exact (exhaustive) |
| 2 | 3 | exact (exhaustive) |
| 3 | 3 | exact (exhaustive) |
| 4 | 4 | exact (exhaustive) |
| 5 | 4 | exact (exhaustive) |
| 6 | 5 | exact (exhaustive) |
| 7 | 5 | exact (exhaustive) |
| 8 | 5 | exact (exhaustive) |
| 9 | 6 | exact (exhaustive) |
| 10 | 6 | exact (exhaustive) |
| 11 | 6 | exact (exhaustive) |
| 12 | 7 | exact (exhaustive) |
| 13 | 7 | exact (exhaustive) |
| 14 | 7 | exact (exhaustive) |
| 30 | 9 | best known (ours) |

Exact values by exhaustive search over subsets of T_n (tools/src/trigrid.c areas); n = 30 is our best known lower bound.

## Best known value

9 for n = 30, held by Quantavane (Arhan Canli), 9 November 2026: the points in `refs/tri-areas.txt`. Upper bound: the C(t,3) areas are distinct integers between 1 and 29^2 = 841, so C(t,3) <= 841 and t(30) <= 18.

Bound on the other side: 18 (upper bound; C(t,3) <= 841 distinct nonzero areas (in units of sqrt(3)/4)).

## Submitting and checking

Format: Text file: one point per line, 'a b' with a, b >= 0 and a + b <= 29.

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check tri-areas FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_geom.py tri-areas 30 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/tri-areas.txt`.

## References

- P. Brass, W. Moser, J. Pach, Research Problems in Discrete Geometry (Springer, 2005): problems of Erdos and Purdy on distinct areas
- OEIS A322740 (the square-grid relative: least rectangle area from which n points with distinct triangle areas can be chosen)
