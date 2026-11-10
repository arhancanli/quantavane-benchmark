# Distinct distances in the body-centred cubic crystal

`bcc-distinct` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **8** (maximize), Quantavane (Arhan Canli), 10 November 2026: 8 points of the region of side 5 with all pairwise distances different, the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the body-centred cubic crystal B_N be the points (x, y, z) with 0 <= x, y, z <= 2N - 2 whose coordinates are all even (the N^3 corners of an (N-1) x (N-1) x (N-1) block of cubes of edge 2) or all odd (the (N-1)^3 cube centres); squared distance dx^2 + dy^2 + dz^2, nearest neighbours at squared distance 3. Determine the largest number of points of the body-centred cubic crystal B_N such that all pairwise distances are different, as a function of N. The exact values are known (ours) for N <= 3; the headline cell is N = 5: find 9 or more such points of the region of side 5 (an upper bound is 10).

## Why it is interesting

Erdos and Guy asked for the largest subset of the n x n grid (and of the d-dimensional grid) with all pairwise distances different, a discrete relative of Golomb rulers and of Erdos's distinct distances problem; for the square grid the answer is of order n^(2/3) up to logarithmic factors (Erdos-Guy, Lefmann-Thiele). Our problems tri-distinct and tetra-distinct ask it for the triangular grid and the tetrahedral (face-centred cubic) grid. The body-centred cubic crystal (iron, tungsten, the alkali metals) is the union of two cubic grids offset by half a cube diagonal; its squared distances (in units of half the cube edge) are the numbers x^2 + y^2 + z^2 with x, y, z all even or all odd, and the counting bound C(k, 2) <= (number of distances) gives k = O(N). How fast the largest distinct-distance sets grow is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/bcc-distinct.json`](../novelty/bcc-distinct.json) with its address, the time it ran and its first results.

- arXiv API, 5 searches:
  - `all:"distinct distances" AND all:"body-centered cubic"`: 0 results
  - `all:"distinct distances" AND all:"cubic grid"`: 0 results
  - `all:"distinct distances" AND all:"three-dimensional grid"`: 0 results
  - `all:"distinct distances" AND all:"body-centred cubic"`: 0 results
  - `all:"distinct distances" AND all:"three-dimensional lattice"`: 0 results
- OEIS, 2 searches:
  - `distinct distances cube`: 10 results (A290190, A393008, A000125, A005282, A079766)
  - `distinct distances three dimensions`: 10 results (A000217, A007318, A000670, A000166, A001906)
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `distinct distances subsets three-dimensional integer grid`: first results "Three-Variable Expanding Polynomials and Higher-Dimensional Distinct Distances" (2018); "Distinct distances determined by subsets of a point set in space" (1991); "Three-Dimensional Point Cloud Recognition via Distributions of Geometric Distances" (2008)
- Web search (general web search), `largest set of points with all pairwise distances distinct honeycomb lattice OR kagome lattice OR body-centered cubic lattice Erdos Guy distinct distances subset`: Erdos-Guy (1970) for the d-dimensional integer grid, Lefmann-Thiele, Charalambides, the survey arXiv:1406.1949; nothing on the honeycomb, kagome or body-centred cubic lattices
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no distinct-distance family in the benchmark.

Closest work found, and how this problem differs:
- P. Erdos and R. K. Guy (1970): the square and d-dimensional grids.
- Our problems tri-distinct (triangular grid) and tetra-distinct (tetrahedral grid): the same question in other lattices.

Verdict: new question for this lattice: Erdos and Guy asked it for the d-dimensional grid and we for the triangular and tetrahedral grids (tri-distinct, tetra-distinct); no result was found for the body-centred cubic crystal, and it is not in the OEIS by name (too few exact values are known to search by terms).

## Best known value

8 for N = 5, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/bcc-distinct.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..3: 3, 5 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py). Upper bound for N = 5: 10 (the C(k, 2) distances are different among the 46 squared distances that occur in the region, so C(k, 2) <= 46).

## Cells

The same question at each value of its parameter (N, the side of the body-centred cubic crystal): 4 cells, 2 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/bcc-distinct/` (the headline cell uses `collections/originals/refs/bcc-distinct.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example bcc-distinct-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `bcc-distinct-2` | 2 | 3 | exact |
| `bcc-distinct-3` | 3 | 5 | exact |
| `bcc-distinct-4` | 4 | 7 | best known |
| `bcc-distinct-5` | 5 | 8 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

Bound on the other side: 10 (upper bound; the C(k, 2) distances are different among the 46 squared distances that occur in the region, so C(k, 2) <= 46).

## Submitting and checking

Format: Text file: one point 'x y z' per line, a point of the region of side 5 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check bcc-distinct FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py bcc-distinct 5 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/bcc-distinct.txt`.

## References

- P. Erdos, R. K. Guy, Distinct distances between lattice points, Elemente der Mathematik 25 (1970) 121-123
- H. Lefmann, T. Thiele, Point sets with distinct distances, Combinatorica 15 (1995) 379-408
