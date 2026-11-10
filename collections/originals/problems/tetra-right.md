# Right-angle-free sets in the tetrahedral grid

`tetra-right` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **16** (maximize), Quantavane (Arhan Canli), 10 November 2026: 16 points of the region of side 8 with no right angle (no three points p, q, r with (q - p).(r - p) = 0), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the tetrahedral grid F_N be the points a e1 + b e2 + c e3 with integers a, b, c >= 0 and a + b + c <= N - 1, where e1, e2, e3 are unit vectors at 60 degrees to each other: N(N+1)(N+2)/6 points of the face-centred cubic lattice forming a tetrahedron of side N - 1; the squared distance is da^2 + db^2 + dc^2 + da db + db dc + dc da. Determine the largest number of points of the tetrahedral grid F_N such that no three of them form a right angle (no three points p, q, r with (q - p).(r - p) = 0), as a function of N. The exact values are known (ours) for N <= 6; the headline cell is N = 8: find 17 or more such points of the region of side 8.

## Why it is interesting

A set of points is right-angle-free when no three of its points form a right angle. Gamble, Pulleyblank, Reed and Shepherd (1995) studied the largest right-angle-free subsets of the plane and of the square lattice, and related work (Junger and Pulleyblank) shows the problem NP-hard for general point sets; sets without isosceles right triangles in the n x n grid are a separate, active question (OEIS A271906; arXiv:2607.22828, 2026). In the face-centred cubic lattice right angles occur in many directions (the three cube axes of the crystal, for example, are lattice directions perpendicular to each other); how fast the largest right-angle-free sets of the tetrahedral grid grow is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/tetra-right.json`](../novelty/tetra-right.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:"right angle" AND all:"face-centered cubic" AND all:subset`: 0 results
  - `all:"right triangle" AND all:"tetrahedral" AND all:grid`: 0 results
  - `all:"right angle" AND all:"fcc lattice"`: 0 results
  - `all:"right angle" AND all:"tetrahedral grid"`: 0 results
- OEIS, 1 searches:
  - `4,4,8,10,14`: 6 results (A014687, A125204, A305594, A172022, A039879)
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `right angle free subsets face-centred cubic lattice tetrahedral grid`: first results "The ordering of a face-centred cubic lattice" (1963); "Lattice Dynsamics of Face Centred Cubic Crystals" (2018); "Equilibrium and non-equilibrium statistical mechanics of alloys in a face centred cubic lattice" (2002)
- Web search (general web search), `"face-centered cubic" OR "fcc lattice" OR "tetrahedral grid" largest subset no isosceles triangle OR no right angle points`: square-grid results only (A271907, PatternBoost, AlphaEvolve, Erdos problem #1207, axis-parallel right triangles in a seminar abstract); nothing on the face-centred cubic lattice or the tetrahedral grid
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no right-angle-free family.

Closest work found, and how this problem differs:
- B. Gamble, W. Pulleyblank, B. Reed and B. Shepherd (1995): right-angle-free subsets of the plane and of the square lattice; another lattice.
- OEIS A271906 and arXiv:2607.22828: no isosceles right triangle in the square grid, a weaker condition in another lattice.

Verdict: new question for this lattice: right-angle-free subsets are studied for the square lattice (Gamble, Pulleyblank, Reed and Shepherd 1995; Junger and Pulleyblank) and isosceles right triangles in the square grid (A271906); no result was found for the tetrahedral grid, and its first values are not in the OEIS as such (the sequences matching them, A014687, A125204, A305594, A172022, are unrelated and agree on these few terms by coincidence).

## Best known value

16 for N = 8, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/tetra-right.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..6: 4, 4, 8, 10, 14 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py).

## Cells

The same question at each value of its parameter (N, the side of the tetrahedral grid): 7 cells, 5 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/tetra-right/` (the headline cell uses `collections/originals/refs/tetra-right.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example tetra-right-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `tetra-right-2` | 2 | 4 | exact |
| `tetra-right-3` | 3 | 4 | exact |
| `tetra-right-4` | 4 | 8 | exact |
| `tetra-right-5` | 5 | 10 | exact |
| `tetra-right-6` | 6 | 14 | exact |
| `tetra-right-7` | 7 | 16 | best known |
| `tetra-right-8` | 8 | 16 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

## Submitting and checking

Format: Text file: one point 'a b c' per line, a point of the region of side 8 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check tetra-right FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py tetra-right 8 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/tetra-right.txt`.

## References

- B. Gamble, W. Pulleyblank, B. Reed, B. Shepherd, Right angle free subsets in the plane, Graphs and Combinatorics 11 (1995) 121-129
- A Salem-Spencer-type construction for large subsets of integer grids with no isosceles right triangles, arXiv:2607.22828 (2026)
- OEIS A271906 (largest subsets of the n x n grid with no right isosceles triangle)
