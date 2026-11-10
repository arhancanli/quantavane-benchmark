# Distinct distances in the honeycomb grid

`hex-distinct` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **9** (maximize), Quantavane (Arhan Canli), 10 November 2026: 9 points of the region of side 15 with all pairwise distances different, the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the honeycomb grid H_N be the points (a, b) of the triangular grid T_N (the points a + b w, w = e^(i pi/3), a, b >= 0, a + b <= N - 1) with a - b not divisible by 3. Removing the index-3 sublattice of hexagon centres from the triangular lattice leaves the honeycomb lattice of graphene, with unit bonds; the squared distance is da^2 + da db + db^2. Determine the largest number of points of the honeycomb grid H_N such that all pairwise distances are different, as a function of N. The exact values are known (ours) for N <= 13; the headline cell is N = 15: find 10 or more such points of the region of side 15 (an upper bound is 11).

## Why it is interesting

Erdos and Guy asked for the largest subset of the n x n grid (and of the d-dimensional grid) with all pairwise distances different, a discrete relative of Golomb rulers and of Erdos's distinct distances problem; for the square grid the answer is of order n^(2/3) up to logarithmic factors (Erdos-Guy, Lefmann-Thiele). Our problems tri-distinct and tetra-distinct ask it for the triangular grid and the tetrahedral (face-centred cubic) grid. The honeycomb lattice of graphene has two sites per cell and is not closed under addition; its squared distances are Loschian numbers a^2 + ab + b^2, as in the triangular grid, but fewer pairs realise each one. How fast the largest distinct-distance sets grow, and how they compare with the triangular grid's, is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/hex-distinct.json`](../novelty/hex-distinct.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:"distinct distances" AND all:honeycomb`: 1 result
  - `all:"distinct distances" AND all:"hexagonal lattice"`: 0 results
  - `all:"distinct distances" AND all:"hexagonal grid"`: 0 results
  - `all:"distinct distances" AND all:graphene`: 0 results
- OEIS, 4 searches:
  - `distinct distances grid`: 10 results (A290190, A393008, A393009, A393010, A306385)
  - `distinct distances hexagonal`: 10 results (A000217, A000670, A006125, A002061, A001519)
  - `distinct distances triangular`: 10 results (A394698, A393796, A294745, A000217, A000108)
  - `2,3,3,4,5,5,6,6,6,7,8,8`: 4 results (A123579, A296020, A266350, A385584)
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `distinct distances subset honeycomb hexagonal lattice`: first results "A Family of Quasi-Two-Dimensional Honeycomb Lattice Magnets RE2Te4O11 (RE = GdEr and Yb) with Large Interlayer Distances"; "An acoustic-black-hole-empowered hexagonal honeycomb lattice for vibration attenuation" (2026); "Microwave study of planar honeycomb EBG lattice with hexagonal basis points" (2011)
- Web search (general web search), `largest set of points with all pairwise distances distinct honeycomb lattice OR kagome lattice OR body-centered cubic lattice Erdos Guy distinct distances subset`: Erdos-Guy (1970) for the d-dimensional integer grid, Lefmann-Thiele, Charalambides, the survey arXiv:1406.1949; nothing on the honeycomb, kagome or body-centred cubic lattices
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no distinct-distance family in the benchmark.

Closest work found, and how this problem differs:
- P. Erdos and R. K. Guy (1970): the square and d-dimensional grids.
- Our problems tri-distinct (triangular grid) and tetra-distinct (tetrahedral grid): the same question in other lattices.

Verdict: new question for this lattice: Erdos and Guy asked it for the d-dimensional grid and we for the triangular and tetrahedral grids (tri-distinct, tetra-distinct); no result was found for the honeycomb grid, and its first values are not in the OEIS as such (the sequences matching them, A123579, A296020, A266350, A385584, are unrelated and agree on these few terms by coincidence).

## Best known value

9 for N = 15, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/hex-distinct.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..13: 2, 3, 3, 4, 5, 5, 6, 6, 6, 7, 8, 8 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py). Upper bound for N = 15: 11 (the C(k, 2) distances are different among the 59 squared distances that occur in the region, so C(k, 2) <= 59).

## Cells

The same question at each value of its parameter (N, the side of the honeycomb grid): 14 cells, 12 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/hex-distinct/` (the headline cell uses `collections/originals/refs/hex-distinct.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example hex-distinct-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `hex-distinct-2` | 2 | 2 | exact |
| `hex-distinct-3` | 3 | 3 | exact |
| `hex-distinct-4` | 4 | 3 | exact |
| `hex-distinct-5` | 5 | 4 | exact |
| `hex-distinct-6` | 6 | 5 | exact |
| `hex-distinct-7` | 7 | 5 | exact |
| `hex-distinct-8` | 8 | 6 | exact |
| `hex-distinct-9` | 9 | 6 | exact |
| `hex-distinct-10` | 10 | 6 | exact |
| `hex-distinct-11` | 11 | 7 | exact |
| `hex-distinct-12` | 12 | 8 | exact |
| `hex-distinct-13` | 13 | 8 | exact |
| `hex-distinct-14` | 14 | 9 | best known |
| `hex-distinct-15` | 15 | 9 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

Bound on the other side: 11 (upper bound; the C(k, 2) distances are different among the 59 squared distances that occur in the region, so C(k, 2) <= 59).

## Submitting and checking

Format: Text file: one point 'a b' per line, a point of the region of side 15 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check hex-distinct FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py hex-distinct 15 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/hex-distinct.txt`.

## References

- P. Erdos, R. K. Guy, Distinct distances between lattice points, Elemente der Mathematik 25 (1970) 121-123
- H. Lefmann, T. Thiele, Point sets with distinct distances, Combinatorica 15 (1995) 379-408
