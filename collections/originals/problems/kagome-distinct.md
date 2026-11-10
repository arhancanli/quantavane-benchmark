# Distinct distances in the kagome grid

`kagome-distinct` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **8** (maximize), Quantavane (Arhan Canli), 10 November 2026: 8 points of the region of side 13 with all pairwise distances different, the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the kagome grid K_N be the points (a, b) of the triangular grid T_N (the points a + b w, w = e^(i pi/3), a, b >= 0, a + b <= N - 1) with a and b not both even. Removing the sublattice 2Z[w] from the triangular lattice leaves the kagome lattice (corner-sharing triangles, four unit bonds at every site); the squared distance is da^2 + da db + db^2. Determine the largest number of points of the kagome grid K_N such that all pairwise distances are different, as a function of N. The exact values are known (ours) for N <= 11; the headline cell is N = 13: find 9 or more such points of the region of side 13 (an upper bound is 9).

## Why it is interesting

Erdos and Guy asked for the largest subset of the n x n grid (and of the d-dimensional grid) with all pairwise distances different, a discrete relative of Golomb rulers and of Erdos's distinct distances problem; for the square grid the answer is of order n^(2/3) up to logarithmic factors (Erdos-Guy, Lefmann-Thiele). Our problems tri-distinct and tetra-distinct ask it for the triangular grid and the tetrahedral (face-centred cubic) grid. The kagome lattice (three sites per cell, corner-sharing triangles) is the lattice of the frustrated kagome antiferromagnets; it keeps three quarters of the triangular lattice. How fast the largest distinct-distance sets grow, and how they compare with the triangular grid's, is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/kagome-distinct.json`](../novelty/kagome-distinct.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"distinct distances" AND all:kagome`: 0 results
  - `all:"distinct distances" AND all:"kagome lattice"`: 0 results
  - `all:"distinct distances" AND all:"triangular lattice"`: 0 results
- OEIS, 1 searches:
  - `2,2,3,3,5,5,6,6,7,7`: 2 results (A350350, A038810)
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `distinct distances kagome lattice`: first results "Kagome lattice"; "Kagome lattice"; "Activity-Enhanced Self-Assembly of a Colloidal Kagome Lattice"
- Web search (general web search), `largest set of points with all pairwise distances distinct honeycomb lattice OR kagome lattice OR body-centered cubic lattice Erdos Guy distinct distances subset`: Erdos-Guy (1970) for the d-dimensional integer grid, Lefmann-Thiele, Charalambides, the survey arXiv:1406.1949; nothing on the honeycomb, kagome or body-centred cubic lattices
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no distinct-distance family in the benchmark.

Closest work found, and how this problem differs:
- P. Erdos and R. K. Guy (1970): the square and d-dimensional grids.
- Our problems tri-distinct (triangular grid) and tetra-distinct (tetrahedral grid): the same question in other lattices.

Verdict: new question for this lattice: Erdos and Guy asked it for the d-dimensional grid and we for the triangular and tetrahedral grids (tri-distinct, tetra-distinct); no result was found for the kagome grid, and its first values are not in the OEIS as such (the sequences matching them, A350350, A038810, are unrelated and agree on these few terms by coincidence).

## Best known value

8 for N = 13, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/kagome-distinct.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..11: 2, 2, 3, 3, 5, 5, 6, 6, 7, 7 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py). Upper bound for N = 13: 9 (the C(k, 2) distances are different among the 39 squared distances that occur in the region, so C(k, 2) <= 39).

## Cells

The same question at each value of its parameter (N, the side of the kagome grid): 12 cells, 10 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/kagome-distinct/` (the headline cell uses `collections/originals/refs/kagome-distinct.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example kagome-distinct-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `kagome-distinct-2` | 2 | 2 | exact |
| `kagome-distinct-3` | 3 | 2 | exact |
| `kagome-distinct-4` | 4 | 3 | exact |
| `kagome-distinct-5` | 5 | 3 | exact |
| `kagome-distinct-6` | 6 | 5 | exact |
| `kagome-distinct-7` | 7 | 5 | exact |
| `kagome-distinct-8` | 8 | 6 | exact |
| `kagome-distinct-9` | 9 | 6 | exact |
| `kagome-distinct-10` | 10 | 7 | exact |
| `kagome-distinct-11` | 11 | 7 | exact |
| `kagome-distinct-12` | 12 | 8 | best known |
| `kagome-distinct-13` | 13 | 8 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

Bound on the other side: 9 (upper bound; the C(k, 2) distances are different among the 39 squared distances that occur in the region, so C(k, 2) <= 39).

## Submitting and checking

Format: Text file: one point 'a b' per line, a point of the region of side 13 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check kagome-distinct FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py kagome-distinct 13 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/kagome-distinct.txt`.

## References

- P. Erdos, R. K. Guy, Distinct distances between lattice points, Elemente der Mathematik 25 (1970) 121-123
- H. Lefmann, T. Thiele, Point sets with distinct distances, Combinatorica 15 (1995) 379-408
