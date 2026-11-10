# Right-angle-free sets in the triangular grid

`tri-right` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **23** (maximize), Quantavane (Arhan Canli), 10 November 2026: 23 points of the region of side 13 with no right angle (no three points p, q, r with (q - p).(r - p) = 0), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the triangular grid T_N be the points a + b w (w = e^(i pi/3)) with integers a, b >= 0 and a + b <= N - 1, N(N+1)/2 points forming a triangle of side N - 1 in the Eisenstein lattice; the squared distance between two of them is da^2 + da db + db^2. Determine the largest number of points of the triangular grid T_N such that no three of them form a right angle (no three points p, q, r with (q - p).(r - p) = 0), as a function of N. The exact values are known (ours) for N <= 10; the headline cell is N = 13: find 24 or more such points of the region of side 13.

## Why it is interesting

A set of points is right-angle-free when no three of its points form a right angle. Gamble, Pulleyblank, Reed and Shepherd (1995) studied the largest right-angle-free subsets of the plane and of the square lattice, and related work (Junger and Pulleyblank) shows the problem NP-hard for general point sets; sets without isosceles right triangles in the n x n grid are a separate, active question (OEIS A271906; arXiv:2607.22828, 2026). In the triangular lattice the grid directions meet at 60 and 120 degrees, so no two of them are perpendicular, but right angles occur in many other directions (for example between (1, 0) and (-1, 2)). The exact values grow irregularly (3, 4, 5, 9, 12, 13, 13, 15, 16 for N = 2..10), with no closed form in sight; how fast they grow is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/tri-right.json`](../novelty/tri-right.json) with its address, the time it ran and its first results.

- arXiv API, 7 searches:
  - `all:"right triangle" AND all:"triangular lattice" AND all:subset`: 0 results
  - `all:"right angle" AND all:"triangular grid" AND all:points`: 0 results
  - `all:"right-triangle-free"`: 0 results
  - `ti:"Problems on the Triangular Lattice"`: 3 results
  - `all:"right angle" AND all:"triangular lattice"`: 2 results
  - `all:"right angles" AND all:"lattice points" AND all:subset`: 0 results
  - `all:"right-angle-free" OR all:"right angle free"`: 0 results
- OEIS, 4 searches:
  - `right triangle triangular grid`: 10 results (A292671, A290724, A397706, A121448, A334228)
  - `no right triangle`: 10 results (A292671, A272958, A061199, A272965, A271906)
  - `1,3,4,5,9,12,13,13,15,16`: 0 results
  - `3,4,5,9,12,13,13,15,16`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `subsets without right triangles grid points`: first results "Monochromatic Equilateral Right Triangles on the Integer Grid"; "Figure 5—figure supplement 2. Bootstrap analysis of Pearson correlation r between expression and methylation datasets over eight time points for each gene."; "Proof Without Words: Right Triangles and Geometric Series" (2006)
- Web search (general web search), `right angle free subset triangular grid OR hexagonal lattice OR "three-dimensional grid" largest set no right triangle Gamble Pulleyblank Reed Shepherd`: Gamble, Pulleyblank, Reed and Shepherd (Graphs Combin. 11 (1995)) and Juenger-Pulleyblank on right-angle-free subsets of the square lattice (NP-hard in general), a programming exercise for the m x n grid; nothing on triangular, honeycomb or three-dimensional grids
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no right-angle-free family.

Closest work found, and how this problem differs:
- B. Gamble, W. Pulleyblank, B. Reed and B. Shepherd (1995): right-angle-free subsets of the plane and of the square lattice; another lattice.
- OEIS A271906 and arXiv:2607.22828: no isosceles right triangle in the square grid, a weaker condition in another lattice.

Verdict: new question for this lattice: right-angle-free subsets are studied for the square lattice (Gamble, Pulleyblank, Reed and Shepherd 1995; Junger and Pulleyblank) and isosceles right triangles in the square grid (A271906); no result was found for the triangular grid, and its first values are not in the OEIS.

## Best known value

23 for N = 13, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/tri-right.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..10: 3, 4, 5, 9, 12, 13, 13, 15, 16 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py).

## Cells

The same question at each value of its parameter (N, the side of the triangular grid): 12 cells, 9 of them exact (an exhaustive search finished) and 3 best known (ours). Each cell has its certificate in `refs/cells/tri-right/` (the headline cell uses `collections/originals/refs/tri-right.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example tri-right-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `tri-right-2` | 2 | 3 | exact |
| `tri-right-3` | 3 | 4 | exact |
| `tri-right-4` | 4 | 5 | exact |
| `tri-right-5` | 5 | 9 | exact |
| `tri-right-6` | 6 | 12 | exact |
| `tri-right-7` | 7 | 13 | exact |
| `tri-right-8` | 8 | 13 | exact |
| `tri-right-9` | 9 | 15 | exact |
| `tri-right-10` | 10 | 16 | exact |
| `tri-right-11` | 11 | 18 | best known |
| `tri-right-12` | 12 | 19 | best known |
| `tri-right-13` | 13 | 23 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

## Submitting and checking

Format: Text file: one point 'a b' per line, a point of the region of side 13 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check tri-right FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py tri-right 13 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/tri-right.txt`.

## References

- B. Gamble, W. Pulleyblank, B. Reed, B. Shepherd, Right angle free subsets in the plane, Graphs and Combinatorics 11 (1995) 121-129
- A Salem-Spencer-type construction for large subsets of integer grids with no isosceles right triangles, arXiv:2607.22828 (2026)
- OEIS A271906 (largest subsets of the n x n grid with no right isosceles triangle)
