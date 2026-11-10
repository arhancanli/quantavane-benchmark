# Isosceles-free sets in the honeycomb grid

`hex-isosceles` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **15** (maximize), Quantavane (Arhan Canli), 10 November 2026: 15 points of the region of side 14 with no point equidistant from two others (no isosceles triangle, flat ones included), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the honeycomb grid H_N be the points (a, b) of the triangular grid T_N (the points a + b w, w = e^(i pi/3), a, b >= 0, a + b <= N - 1) with a - b not divisible by 3. Removing the index-3 sublattice of hexagon centres from the triangular lattice leaves the honeycomb lattice of graphene, with unit bonds; the squared distance is da^2 + da db + db^2. Determine the largest number of points of the honeycomb grid H_N such that no point is equidistant from two others (no isosceles triangle, flat ones included: no point is the midpoint of two others), as a function of N. The exact values are known (ours) for N <= 12; the headline cell is N = 14: find 16 or more such points of the region of side 14 (an upper bound is 53).

## Why it is interesting

A set of points is isosceles-free when no point of it is equidistant from two others: no three of its points form an isosceles triangle, counting the flat case of a point midway between two others. For the n x n square grid the largest such sets have become a test bed for machine-assisted constructions: PatternBoost (Charton, Ellenberg, Wagner and Williamson, 2024) and AlphaEvolve (Georgiev, Gomez-Serrano, Tao and Wagner, 2025) found sets of 108 to 112 points in the 64 x 64 grid, the first values are OEIS A271907, and the best lower bound proved, of order n sqrt(log log n / log n) (arXiv:2610.04194, 2026), is far from the subquadratic upper bounds (the grid question is Erdos problem #1207). The honeycomb lattice (the carbon sites of graphene) is the triangular lattice with a third of its points removed; it has no unit equilateral triangles, but its distances are still Loschian numbers. The exact values grow roughly like N; whether the growth stays linear, and how it compares with the triangular grid (whose isosceles-free sets contain those of the honeycomb grid), is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/hex-isosceles.json`](../novelty/hex-isosceles.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:isosceles AND all:honeycomb`: 2 results
  - `all:isosceles AND all:"hexagonal lattice" AND all:points`: 0 results
  - `all:"isosceles" AND all:"hexagonal grid"`: 0 results
  - `all:"isosceles" AND all:graphene AND all:subset`: 0 results
- OEIS, 1 searches:
  - `2,3,4,5,6,7,8,10,10,13,14`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `isosceles free honeycomb hexagonal lattice`: first results "An acoustic-black-hole-empowered hexagonal honeycomb lattice for vibration attenuation" (2026); "Microwave study of planar honeycomb EBG lattice with hexagonal basis points" (2011); "A Honeycomb Transmit-Array Lens with Hexagonal Lattice for Generation of OAM Waves" (2018)
- Web search (general web search), `largest subset of triangular grid with no isosceles triangle (no three points isosceles) triangular lattice hexagonal honeycomb`: only the square-grid problem (PatternBoost arXiv:2411.00566, arXiv:2503.11061, AlphaEvolve arXiv:2511.02864, OEIS A271907, Solymosi's talk); nothing on the triangular or honeycomb lattice
- Web search (general web search), `"isosceles" "triangular lattice" OR "triangular grid" subset AlphaEvolve OR PatternBoost OR "Geometry-Aware MCTS" no isosceles triangle`: the same square-grid papers and an open-problem page for the n x n grid; no triangular-lattice variant
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no isosceles-free family.

Closest work found, and how this problem differs:
- The n x n square grid (OEIS A271907; PatternBoost arXiv:2411.00566; AlphaEvolve arXiv:2511.02864; arXiv:2610.04194): the same question in another lattice.
- Erdos-type questions on isosceles sets in the plane and in space: point sets in which every three points form an isosceles triangle, the opposite extreme.

Verdict: new question for this lattice: isosceles-free subsets are studied for the n x n square grid (OEIS A271907, PatternBoost, AlphaEvolve, arXiv:2610.04194); no result was found for the honeycomb grid, and its first values are not in the OEIS.

## Best known value

15 for N = 14, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/hex-isosceles.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..12: 2, 3, 4, 5, 6, 7, 8, 10, 10, 13, 14 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py). Upper bound for N = 14: 53 (every chosen point sees the others at different distances, and no point of the region sees more than 52 different distances).

## Cells

The same question at each value of its parameter (N, the side of the honeycomb grid): 13 cells, 11 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/hex-isosceles/` (the headline cell uses `collections/originals/refs/hex-isosceles.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example hex-isosceles-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `hex-isosceles-2` | 2 | 2 | exact |
| `hex-isosceles-3` | 3 | 3 | exact |
| `hex-isosceles-4` | 4 | 4 | exact |
| `hex-isosceles-5` | 5 | 5 | exact |
| `hex-isosceles-6` | 6 | 6 | exact |
| `hex-isosceles-7` | 7 | 7 | exact |
| `hex-isosceles-8` | 8 | 8 | exact |
| `hex-isosceles-9` | 9 | 10 | exact |
| `hex-isosceles-10` | 10 | 10 | exact |
| `hex-isosceles-11` | 11 | 13 | exact |
| `hex-isosceles-12` | 12 | 14 | exact |
| `hex-isosceles-13` | 13 | 14 | best known |
| `hex-isosceles-14` | 14 | 15 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

Bound on the other side: 53 (upper bound; every chosen point sees the others at different distances, and no point of the region sees more than 52 different distances).

## Submitting and checking

Format: Text file: one point 'a b' per line, a point of the region of side 14 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check hex-isosceles FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py hex-isosceles 14 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/hex-isosceles.txt`.

## References

- F. Charton, J. S. Ellenberg, A. Z. Wagner, G. Williamson, PatternBoost: constructions in mathematics with a little help from AI, arXiv:2411.00566 (2024)
- B. Georgiev, J. Gomez-Serrano, T. Tao, A. Z. Wagner, Mathematical exploration and discovery at scale, arXiv:2511.02864 (2025)
- Sparse coloring for isosceles-free grids: an AI-assisted proof case study, arXiv:2610.04194 (2026)
- OEIS A271907 (largest subsets of the n x n grid with no isosceles triangle)
