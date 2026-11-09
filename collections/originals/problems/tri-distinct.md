# Distinct distances in the triangular grid

`tri-distinct` · Discrete geometry · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **14** (maximize), Quantavane (Arhan Canli), 9 November 2026: 14 points of T_30 with distinct distances found by randomized greedy construction and local search (tools/tri_distinct_search.py)

## Statement

The triangular grid T_n is the set of points a + b*e^(i pi/3) with integers a, b >= 0 and a + b <= n - 1 (n(n+1)/2 points, a triangle of side n - 1 in the Eisenstein lattice); the squared distance between two of its points is da^2 + da*db + db^2. Let g(n) be the largest number of points of T_n whose pairwise distances are all different. Determine g(n); the headline cell is n = 30: find 15 or more points of T_30 with all distances distinct.

## Why it is interesting

Erdos and Guy asked for the largest subset of the n x n square grid with all pairwise distances distinct, a discrete relative of Golomb rulers and of Erdos's distinct distances problem; for the square grid the answer is of order n^(2/3) up to logarithmic factors. In the Eisenstein lattice the possible squared distances are the Loschian numbers a^2 + ab + b^2 (OEIS A003136), which, like sums of two squares, have density zero, so the triangular grid has fewer available distances than the square grid of the same size and the extremal sets should be sparser. The first values g(n) for n <= 16 below are exact; how fast g(n) grows, and whether it is of order n^(2/3) as for the square grid, is open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/tri-distinct.json`](../novelty/tri-distinct.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"distinct distances" AND all:"Eisenstein"`: 0 results
  - `all:"Erdos-Guy" OR all:"distinct distances" AND all:"lattice" AND all:subset`: 3 results
- OEIS, 3 searches:
  - `1,2,3,3,4,5,5,6,6,7,7,8,8,9,9,10`: 1 result (A027923)
  - `distinct distances triangular grid`: 9 results (A394698, A393796, A000217, A000012, A002061)
  - `distinct distances grid points`: 10 results (A290190, A393008, A393009, A393010, A306385)
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no entry; the benchmark's no-three-in-line and Golomb ruler problems are on the square grid and the line.

Closest work found, and how this problem differs:
- Erdos and Guy's distinct distances problem in the square grid (the analogue this problem transfers to the Eisenstein lattice).
- OEIS A027923 agrees with g(1..16) by coincidence (its definition, least k with e_2(1..k) >= 1^2 + ... + n^2, is unrelated).

Verdict: new. The sequence g(n) is not in the OEIS (the only match for its 16 known terms is A027923, an unrelated sequence defined by elementary symmetric functions that agrees on those terms by coincidence), and no paper on distinct-distance subsets of the triangular grid was found; the square-grid problem of Erdos and Guy is the closest.

## First values

| n | g(n) | how |
| --- | --- | --- |
| 1 | 1 | exact (exhaustive) |
| 2 | 2 | exact (exhaustive) |
| 3 | 3 | exact (exhaustive) |
| 4 | 3 | exact (exhaustive) |
| 5 | 4 | exact (exhaustive) |
| 6 | 5 | exact (exhaustive) |
| 7 | 5 | exact (exhaustive) |
| 8 | 6 | exact (exhaustive) |
| 9 | 6 | exact (exhaustive) |
| 10 | 7 | exact (exhaustive) |
| 11 | 7 | exact (exhaustive) |
| 12 | 8 | exact (exhaustive) |
| 13 | 8 | exact (exhaustive) |
| 14 | 9 | exact (exhaustive) |
| 15 | 9 | exact (exhaustive) |
| 16 | 10 | exact (exhaustive) |
| 20 | 11 | best known (ours) |
| 24 | 12 | best known (ours) |
| 30 | 14 | best known (ours) |

Exact values by exhaustive branch and bound over all subsets of T_n (tools/src/trigrid.c dist); larger n are our best known lower bounds.

## Best known value

14 for n = 30, held by Quantavane (Arhan Canli), 9 November 2026: the points in `refs/tri-distinct.txt`, found by randomized greedy construction with local search (tools/tri_distinct_search.py). Upper bound: the C(g, 2) squared distances are distinct nonzero Loschian numbers at most (n - 1)^2 = 841, and there are 236 of them, so C(g, 2) <= 236 and g(30) <= 22.

Bound on the other side: 22 (upper bound; C(g,2) <= 236, the number of nonzero Loschian numbers a^2 + ab + b^2 <= 841).

## Submitting and checking

Format: Text file: one point per line, 'a b' with a, b >= 0 and a + b <= 29 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check tri-distinct FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_geom.py tri-distinct 30 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/tri-distinct.txt`.

## References

- P. Erdos, R. K. Guy, Distinct distances between lattice points, Elemente der Mathematik 25 (1970) 121-123
- OEIS A003136 (Loschian numbers: norms x^2 + xy + y^2 of the A2 lattice)
