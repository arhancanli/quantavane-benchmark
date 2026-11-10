# Isosceles-free sets in the tetrahedral grid

`tetra-isosceles` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **12** (maximize), Quantavane (Arhan Canli), 10 November 2026: 12 points of the region of side 8 with no point equidistant from two others (no isosceles triangle, flat ones included), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the tetrahedral grid F_N be the points a e1 + b e2 + c e3 with integers a, b, c >= 0 and a + b + c <= N - 1, where e1, e2, e3 are unit vectors at 60 degrees to each other: N(N+1)(N+2)/6 points of the face-centred cubic lattice forming a tetrahedron of side N - 1; the squared distance is da^2 + db^2 + dc^2 + da db + db dc + dc da. Determine the largest number of points of the tetrahedral grid F_N such that no point is equidistant from two others (no isosceles triangle, flat ones included: no point is the midpoint of two others), as a function of N. The exact values are known (ours) for N <= 6; the headline cell is N = 8: find 13 or more such points of the region of side 8 (an upper bound is 31).

## Why it is interesting

A set of points is isosceles-free when no point of it is equidistant from two others: no three of its points form an isosceles triangle, counting the flat case of a point midway between two others. For the n x n square grid the largest such sets have become a test bed for machine-assisted constructions: PatternBoost (Charton, Ellenberg, Wagner and Williamson, 2024) and AlphaEvolve (Georgiev, Gomez-Serrano, Tao and Wagner, 2025) found sets of 108 to 112 points in the 64 x 64 grid, the first values are OEIS A271907, and the best lower bound proved, of order n sqrt(log log n / log n) (arXiv:2610.04194, 2026), is far from the subquadratic upper bounds (the grid question is Erdos problem #1207). The face-centred cubic lattice is the densest packing of spheres in space and each site has 12 nearest neighbours; the tetrahedral grid has about N^3/6 points but only O(N^2) distances. Our tetra-distinct asks for all distances different, a stronger condition; how fast the largest isosceles-free sets grow is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/tetra-isosceles.json`](../novelty/tetra-isosceles.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:isosceles AND all:"face-centered cubic"`: 2 results
  - `all:"isosceles" AND all:"tetrahedral grid"`: 0 results
  - `all:"isosceles" AND all:"fcc lattice"`: 0 results
- OEIS, 1 searches:
  - `2,4,5,8,8`: 10 results (A029935, A339560, A270566, A308902, A060244)
- Crossref (the journal literature, ranked by relevance), 2 searches:
  - `isosceles triangles face-centred cubic lattice subset`: first results "The ordering of a face-centred cubic lattice" (1963); "Chiral Redox-Active Isosceles Triangles"; "Chiral Redox-Active Isosceles Triangles"
  - `isosceles free subsets tetrahedral grid points`: first results "Isosceles Planar Subsets" (1998); "S M Nazmuz Sakib Two-Circle Right–Isosceles Points Theorem: A Constant Sum of Squared Chords (the Sakib constant)" (2025); "Adaptive Optimization of Bess and Grid Set Points: A Model-Free Framework for Energy Management Under Dynamic Tariff Pricing" (2024)
- Web search (general web search), `"face-centered cubic" OR "fcc lattice" OR "tetrahedral grid" largest subset no isosceles triangle OR no right angle points`: square-grid results only (A271907, PatternBoost, AlphaEvolve, Erdos problem #1207, axis-parallel right triangles in a seminar abstract); nothing on the face-centred cubic lattice or the tetrahedral grid
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no isosceles-free family.

Closest work found, and how this problem differs:
- The n x n square grid (OEIS A271907; PatternBoost arXiv:2411.00566; AlphaEvolve arXiv:2511.02864; arXiv:2610.04194): the same question in another lattice.
- Erdos-type questions on isosceles sets in the plane and in space: point sets in which every three points form an isosceles triangle, the opposite extreme.

Verdict: new question for this lattice: isosceles-free subsets are studied for the n x n square grid (OEIS A271907, PatternBoost, AlphaEvolve, arXiv:2610.04194); no result was found for the tetrahedral grid, and its first values are not in the OEIS as such (the sequences matching them, A029935, A339560, A270566, A308902, are unrelated and agree on these few terms by coincidence).

## Best known value

12 for N = 8, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/tetra-isosceles.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..6: 2, 4, 5, 8, 8 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py). Upper bound for N = 8: 31 (every chosen point sees the others at different distances, and no point of the region sees more than 30 different distances).

## Cells

The same question at each value of its parameter (N, the side of the tetrahedral grid): 7 cells, 5 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/tetra-isosceles/` (the headline cell uses `collections/originals/refs/tetra-isosceles.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example tetra-isosceles-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `tetra-isosceles-2` | 2 | 2 | exact |
| `tetra-isosceles-3` | 3 | 4 | exact |
| `tetra-isosceles-4` | 4 | 5 | exact |
| `tetra-isosceles-5` | 5 | 8 | exact |
| `tetra-isosceles-6` | 6 | 8 | exact |
| `tetra-isosceles-7` | 7 | 10 | best known |
| `tetra-isosceles-8` | 8 | 12 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

Bound on the other side: 31 (upper bound; every chosen point sees the others at different distances, and no point of the region sees more than 30 different distances).

## Submitting and checking

Format: Text file: one point 'a b c' per line, a point of the region of side 8 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check tetra-isosceles FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py tetra-isosceles 8 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/tetra-isosceles.txt`.

## References

- F. Charton, J. S. Ellenberg, A. Z. Wagner, G. Williamson, PatternBoost: constructions in mathematics with a little help from AI, arXiv:2411.00566 (2024)
- B. Georgiev, J. Gomez-Serrano, T. Tao, A. Z. Wagner, Mathematical exploration and discovery at scale, arXiv:2511.02864 (2025)
- Sparse coloring for isosceles-free grids: an AI-assisted proof case study, arXiv:2610.04194 (2026)
- OEIS A271907 (largest subsets of the n x n grid with no isosceles triangle)
