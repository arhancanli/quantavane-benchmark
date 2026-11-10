# Isosceles-free sets in the triangular grid

`tri-isosceles` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **14** (maximize), Quantavane (Arhan Canli), 10 November 2026: 14 points of the region of side 14 with no point equidistant from two others (no isosceles triangle, flat ones included), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the triangular grid T_N be the points a + b w (w = e^(i pi/3)) with integers a, b >= 0 and a + b <= N - 1, N(N+1)/2 points forming a triangle of side N - 1 in the Eisenstein lattice; the squared distance between two of them is da^2 + da db + db^2. Determine the largest number of points of the triangular grid T_N such that no point is equidistant from two others (no isosceles triangle, flat ones included: no point is the midpoint of two others), as a function of N. The exact values are known (ours) for N <= 10; the headline cell is N = 14: find 15 or more such points of the region of side 14 (an upper bound is 53).

## Why it is interesting

A set of points is isosceles-free when no point of it is equidistant from two others: no three of its points form an isosceles triangle, counting the flat case of a point midway between two others. For the n x n square grid the largest such sets have become a test bed for machine-assisted constructions: PatternBoost (Charton, Ellenberg, Wagner and Williamson, 2024) and AlphaEvolve (Georgiev, Gomez-Serrano, Tao and Wagner, 2025) found sets of 108 to 112 points in the 64 x 64 grid, the first values are OEIS A271907, and the best lower bound proved, of order n sqrt(log log n / log n) (arXiv:2610.04194, 2026), is far from the subquadratic upper bounds (the grid question is Erdos problem #1207). In the triangular (Eisenstein) lattice every interior point has six neighbours at the same distance, every equilateral triangle is isosceles, and the squared distances are the Loschian numbers a^2 + ab + b^2, so equal distances are frequent and the extremal sets are sparse. The exact values grow roughly like N (2, 3, 4, 5, 6, 8, 9, 10, 11 for N = 2..10); whether the growth stays linear, and at what rate, is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/tri-isosceles.json`](../novelty/tri-isosceles.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:isosceles AND all:"triangular lattice" AND all:subset`: 0 results
  - `all:"isosceles" AND all:"triangular grid"`: 0 results
  - `all:"isosceles-free"`: 2 results
  - `all:"no isosceles" AND all:grid`: 12 results
- OEIS, 5 searches:
  - `isosceles triangular`: 10 results (A180314, A194024, A389363, A391193, A194021)
  - `isosceles grid`: 10 results (A186434, A187452, A271910, A189978, A271907)
  - `isosceles hexagonal`: 10 results (A241228, A241237, A241229, A241230, A292148)
  - `1,2,3,4,5,6,8,9,10,11`: 10 results (A000378, A302478, A367906, A390673, A020658)
  - `2,3,4,5,6,8,9,10,11`: 10 results (A000378, A302478, A367906, A390673, A020658)
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `isosceles triangle free subsets of grid points`: first results "Isosceles right triangle tiling"; "Isosceles Pythagorean right triangle tiling"; "Largest Isosceles Triangle Inscribed in a Circle" (2008)
- Web search (general web search), `largest subset of triangular grid with no isosceles triangle (no three points isosceles) triangular lattice hexagonal honeycomb`: only the square-grid problem (PatternBoost arXiv:2411.00566, arXiv:2503.11061, AlphaEvolve arXiv:2511.02864, OEIS A271907, Solymosi's talk); nothing on the triangular or honeycomb lattice
- Web search (general web search), `"isosceles" "triangular lattice" OR "triangular grid" subset AlphaEvolve OR PatternBoost OR "Geometry-Aware MCTS" no isosceles triangle`: the same square-grid papers and an open-problem page for the n x n grid; no triangular-lattice variant
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no isosceles-free family.

Closest work found, and how this problem differs:
- The n x n square grid (OEIS A271907; PatternBoost arXiv:2411.00566; AlphaEvolve arXiv:2511.02864; arXiv:2610.04194): the same question in another lattice.
- Erdos-type questions on isosceles sets in the plane and in space: point sets in which every three points form an isosceles triangle, the opposite extreme.

Verdict: new question for this lattice: isosceles-free subsets are studied for the n x n square grid (OEIS A271907, PatternBoost, AlphaEvolve, arXiv:2610.04194); no result was found for the triangular grid, and its first values are not in the OEIS as such (the first ten agree with the sums of three squares, A000378, by coincidence; the value 13 for N = 11 already differs).

## Best known value

14 for N = 14, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/tri-isosceles.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..10: 2, 3, 4, 5, 6, 8, 9, 10, 11 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py). Upper bound for N = 14: 53 (every chosen point sees the others at different distances, and no point of the region sees more than 52 different distances).

## Cells

The same question at each value of its parameter (N, the side of the triangular grid): 13 cells, 9 of them exact (an exhaustive search finished) and 4 best known (ours). Each cell has its certificate in `refs/cells/tri-isosceles/` (the headline cell uses `collections/originals/refs/tri-isosceles.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example tri-isosceles-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `tri-isosceles-2` | 2 | 2 | exact |
| `tri-isosceles-3` | 3 | 3 | exact |
| `tri-isosceles-4` | 4 | 4 | exact |
| `tri-isosceles-5` | 5 | 5 | exact |
| `tri-isosceles-6` | 6 | 6 | exact |
| `tri-isosceles-7` | 7 | 8 | exact |
| `tri-isosceles-8` | 8 | 9 | exact |
| `tri-isosceles-9` | 9 | 10 | exact |
| `tri-isosceles-10` | 10 | 11 | exact |
| `tri-isosceles-11` | 11 | 13 | best known |
| `tri-isosceles-12` | 12 | 14 | best known |
| `tri-isosceles-13` | 13 | 14 | best known |
| `tri-isosceles-14` | 14 | 14 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

Bound on the other side: 53 (upper bound; every chosen point sees the others at different distances, and no point of the region sees more than 52 different distances).

## Submitting and checking

Format: Text file: one point 'a b' per line, a point of the region of side 14 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check tri-isosceles FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py tri-isosceles 14 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/tri-isosceles.txt`.

## References

- F. Charton, J. S. Ellenberg, A. Z. Wagner, G. Williamson, PatternBoost: constructions in mathematics with a little help from AI, arXiv:2411.00566 (2024)
- B. Georgiev, J. Gomez-Serrano, T. Tao, A. Z. Wagner, Mathematical exploration and discovery at scale, arXiv:2511.02864 (2025)
- Sparse coloring for isosceles-free grids: an AI-assisted proof case study, arXiv:2610.04194 (2026)
- OEIS A271907 (largest subsets of the n x n grid with no isosceles triangle)
