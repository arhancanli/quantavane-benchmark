# Isosceles-free sets in the kagome grid

`kagome-isosceles` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **14** (maximize), Quantavane (Arhan Canli), 10 November 2026: 14 points of the region of side 13 with no point equidistant from two others (no isosceles triangle, flat ones included), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the kagome grid K_N be the points (a, b) of the triangular grid T_N (the points a + b w, w = e^(i pi/3), a, b >= 0, a + b <= N - 1) with a and b not both even. Removing the sublattice 2Z[w] from the triangular lattice leaves the kagome lattice (corner-sharing triangles, four unit bonds at every site); the squared distance is da^2 + da db + db^2. Determine the largest number of points of the kagome grid K_N such that no point is equidistant from two others (no isosceles triangle, flat ones included: no point is the midpoint of two others), as a function of N. The exact values are known (ours) for N <= 11; the headline cell is N = 13: find 15 or more such points of the region of side 13 (an upper bound is 40).

## Why it is interesting

A set of points is isosceles-free when no point of it is equidistant from two others: no three of its points form an isosceles triangle, counting the flat case of a point midway between two others. For the n x n square grid the largest such sets have become a test bed for machine-assisted constructions: PatternBoost (Charton, Ellenberg, Wagner and Williamson, 2024) and AlphaEvolve (Georgiev, Gomez-Serrano, Tao and Wagner, 2025) found sets of 108 to 112 points in the 64 x 64 grid, the first values are OEIS A271907, and the best lower bound proved, of order n sqrt(log log n / log n) (arXiv:2610.04194, 2026), is far from the subquadratic upper bounds (the grid question is Erdos problem #1207). The kagome lattice (corner-sharing triangles; the lattice of the frustrated kagome antiferromagnets) keeps three quarters of the triangular lattice, with its unit equilateral triangles; the isosceles-free sets of the kagome grid are among those of the triangular grid. How fast they grow is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/kagome-isosceles.json`](../novelty/kagome-isosceles.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:isosceles AND all:kagome`: 4 results
  - `all:"isosceles" AND all:"kagome lattice" AND all:points`: 3 results
  - `all:"isosceles" AND all:"triangular lattice" AND all:"no three"`: 4 results
- OEIS, 1 searches:
  - `2,2,4,4,6,6,9,9,11,13`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `isosceles free subsets kagome lattice`: first results "Kagome lattice"; "Kagome lattice"; "Isosceles Planar Subsets" (1998)
- Web search (general web search), `no isosceles triangle OR no right angle subset kagome lattice OR body-centered cubic lattice points largest set combinatorial geometry`: the square-grid isosceles-free problem (Erdos problem #1207, Solymosi's notes, PatternBoost, AlphaEvolve) and lattice-point counting in triangles; nothing on the kagome or body-centred cubic lattices
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no isosceles-free family.

Closest work found, and how this problem differs:
- The n x n square grid (OEIS A271907; PatternBoost arXiv:2411.00566; AlphaEvolve arXiv:2511.02864; arXiv:2610.04194): the same question in another lattice.
- Erdos-type questions on isosceles sets in the plane and in space: point sets in which every three points form an isosceles triangle, the opposite extreme.

Verdict: new question for this lattice: isosceles-free subsets are studied for the n x n square grid (OEIS A271907, PatternBoost, AlphaEvolve, arXiv:2610.04194); no result was found for the kagome grid, and its first values are not in the OEIS.

## Best known value

14 for N = 13, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/kagome-isosceles.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..11: 2, 2, 4, 4, 6, 6, 9, 9, 11, 13 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py). Upper bound for N = 13: 40 (every chosen point sees the others at different distances, and no point of the region sees more than 39 different distances).

## Cells

The same question at each value of its parameter (N, the side of the kagome grid): 12 cells, 10 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/kagome-isosceles/` (the headline cell uses `collections/originals/refs/kagome-isosceles.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example kagome-isosceles-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `kagome-isosceles-2` | 2 | 2 | exact |
| `kagome-isosceles-3` | 3 | 2 | exact |
| `kagome-isosceles-4` | 4 | 4 | exact |
| `kagome-isosceles-5` | 5 | 4 | exact |
| `kagome-isosceles-6` | 6 | 6 | exact |
| `kagome-isosceles-7` | 7 | 6 | exact |
| `kagome-isosceles-8` | 8 | 9 | exact |
| `kagome-isosceles-9` | 9 | 9 | exact |
| `kagome-isosceles-10` | 10 | 11 | exact |
| `kagome-isosceles-11` | 11 | 13 | exact |
| `kagome-isosceles-12` | 12 | 13 | best known |
| `kagome-isosceles-13` | 13 | 14 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

Bound on the other side: 40 (upper bound; every chosen point sees the others at different distances, and no point of the region sees more than 39 different distances).

## Submitting and checking

Format: Text file: one point 'a b' per line, a point of the region of side 13 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check kagome-isosceles FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py kagome-isosceles 13 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/kagome-isosceles.txt`.

## References

- F. Charton, J. S. Ellenberg, A. Z. Wagner, G. Williamson, PatternBoost: constructions in mathematics with a little help from AI, arXiv:2411.00566 (2024)
- B. Georgiev, J. Gomez-Serrano, T. Tao, A. Z. Wagner, Mathematical exploration and discovery at scale, arXiv:2511.02864 (2025)
- Sparse coloring for isosceles-free grids: an AI-assisted proof case study, arXiv:2610.04194 (2026)
- OEIS A271907 (largest subsets of the n x n grid with no isosceles triangle)
