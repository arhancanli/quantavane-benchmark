# Isosceles-free sets in the body-centred cubic crystal

`bcc-isosceles` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **14** (maximize), Quantavane (Arhan Canli), 10 November 2026: 14 points of the region of side 5 with no point equidistant from two others (no isosceles triangle, flat ones included), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the body-centred cubic crystal B_N be the points (x, y, z) with 0 <= x, y, z <= 2N - 2 whose coordinates are all even (the N^3 corners of an (N-1) x (N-1) x (N-1) block of cubes of edge 2) or all odd (the (N-1)^3 cube centres); squared distance dx^2 + dy^2 + dz^2, nearest neighbours at squared distance 3. Determine the largest number of points of the body-centred cubic crystal B_N such that no point is equidistant from two others (no isosceles triangle, flat ones included: no point is the midpoint of two others), as a function of N. The exact values are known (ours) for N <= 3; the headline cell is N = 5: find 15 or more such points of the region of side 5 (an upper bound is 47).

## Why it is interesting

A set of points is isosceles-free when no point of it is equidistant from two others: no three of its points form an isosceles triangle, counting the flat case of a point midway between two others. For the n x n square grid the largest such sets have become a test bed for machine-assisted constructions: PatternBoost (Charton, Ellenberg, Wagner and Williamson, 2024) and AlphaEvolve (Georgiev, Gomez-Serrano, Tao and Wagner, 2025) found sets of 108 to 112 points in the 64 x 64 grid, the first values are OEIS A271907, and the best lower bound proved, of order n sqrt(log log n / log n) (arXiv:2610.04194, 2026), is far from the subquadratic upper bounds (the grid question is Erdos problem #1207). The body-centred cubic crystal (iron, tungsten, the alkali metals) gives each site 8 nearest neighbours at the surrounding cube corners or centres and 6 next-nearest along the axes, so equal distances abound. How fast the largest isosceles-free sets grow is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/bcc-isosceles.json`](../novelty/bcc-isosceles.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:isosceles AND all:"body-centered cubic" AND all:subset`: 0 results
  - `all:"isosceles-free" AND all:lattice`: 0 results
  - `all:"isosceles" AND all:"body-centred cubic"`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `isosceles triangle free subsets body-centred cubic lattice`: first results "II. The simple cubic lattice and the body-centred cubic lattice" (1938); "Isosceles right triangle tiling"; "Isosceles Pythagorean right triangle tiling"
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no isosceles-free family.

Closest work found, and how this problem differs:
- The n x n square grid (OEIS A271907; PatternBoost arXiv:2411.00566; AlphaEvolve arXiv:2511.02864; arXiv:2610.04194): the same question in another lattice.
- Erdos-type questions on isosceles sets in the plane and in space: point sets in which every three points form an isosceles triangle, the opposite extreme.

Verdict: new question for this lattice: isosceles-free subsets are studied for the n x n square grid (OEIS A271907, PatternBoost, AlphaEvolve, arXiv:2610.04194); no result was found for the body-centred cubic crystal, and it is not in the OEIS by name (too few exact values are known to search by terms).

## Best known value

14 for N = 5, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/bcc-isosceles.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..3: 4, 8 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py). Upper bound for N = 5: 47 (every chosen point sees the others at different distances, and no point of the region sees more than 46 different distances).

## Cells

The same question at each value of its parameter (N, the side of the body-centred cubic crystal): 4 cells, 2 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/bcc-isosceles/` (the headline cell uses `collections/originals/refs/bcc-isosceles.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example bcc-isosceles-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `bcc-isosceles-2` | 2 | 4 | exact |
| `bcc-isosceles-3` | 3 | 8 | exact |
| `bcc-isosceles-4` | 4 | 10 | best known |
| `bcc-isosceles-5` | 5 | 14 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

Bound on the other side: 47 (upper bound; every chosen point sees the others at different distances, and no point of the region sees more than 46 different distances).

## Submitting and checking

Format: Text file: one point 'x y z' per line, a point of the region of side 5 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check bcc-isosceles FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py bcc-isosceles 5 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/bcc-isosceles.txt`.

## References

- F. Charton, J. S. Ellenberg, A. Z. Wagner, G. Williamson, PatternBoost: constructions in mathematics with a little help from AI, arXiv:2411.00566 (2024)
- B. Georgiev, J. Gomez-Serrano, T. Tao, A. Z. Wagner, Mathematical exploration and discovery at scale, arXiv:2511.02864 (2025)
- Sparse coloring for isosceles-free grids: an AI-assisted proof case study, arXiv:2610.04194 (2026)
- OEIS A271907 (largest subsets of the n x n grid with no isosceles triangle)
