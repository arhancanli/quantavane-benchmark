# Right-angle-free sets in the honeycomb grid

`hex-right` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **21** (maximize), Quantavane (Arhan Canli), 10 November 2026: 21 points of the region of side 15 with no right angle (no three points p, q, r with (q - p).(r - p) = 0), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the honeycomb grid H_N be the points (a, b) of the triangular grid T_N (the points a + b w, w = e^(i pi/3), a, b >= 0, a + b <= N - 1) with a - b not divisible by 3. Removing the index-3 sublattice of hexagon centres from the triangular lattice leaves the honeycomb lattice of graphene, with unit bonds; the squared distance is da^2 + da db + db^2. Determine the largest number of points of the honeycomb grid H_N such that no three of them form a right angle (no three points p, q, r with (q - p).(r - p) = 0), as a function of N. The exact values are known (ours) for N <= 12; the headline cell is N = 15: find 22 or more such points of the region of side 15.

## Why it is interesting

A set of points is right-angle-free when no three of its points form a right angle. Gamble, Pulleyblank, Reed and Shepherd (1995) studied the largest right-angle-free subsets of the plane and of the square lattice, and related work (Junger and Pulleyblank) shows the problem NP-hard for general point sets; sets without isosceles right triangles in the n x n grid are a separate, active question (OEIS A271906; arXiv:2607.22828, 2026). The honeycomb lattice (the carbon sites of graphene) is the triangular lattice with a third of its points removed, so fewer right angles are available. The exact values grow irregularly, with no closed form in sight; how fast they grow is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/hex-right.json`](../novelty/hex-right.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"right triangle" AND all:honeycomb`: 0 results
  - `all:"right angle" AND all:"hexagonal lattice" AND all:subset`: 0 results
  - `all:"right-angle-free" OR all:"right angle free"`: 0 results
- OEIS, 1 searches:
  - `2,3,3,6,8,8,10,11,11,14,16`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `right angle free honeycomb lattice`: first results "Honeycomb lattice"; "Photonic quantum spin Hall effect in angle perturbed honeycomb lattice" (2026); "Embroidery I: Honeycomb Lattice" (2008)
- Web search (general web search), `right angle free subset triangular grid OR hexagonal lattice OR "three-dimensional grid" largest set no right triangle Gamble Pulleyblank Reed Shepherd`: Gamble, Pulleyblank, Reed and Shepherd (Graphs Combin. 11 (1995)) and Juenger-Pulleyblank on right-angle-free subsets of the square lattice (NP-hard in general), a programming exercise for the m x n grid; nothing on triangular, honeycomb or three-dimensional grids
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no right-angle-free family.

Closest work found, and how this problem differs:
- B. Gamble, W. Pulleyblank, B. Reed and B. Shepherd (1995): right-angle-free subsets of the plane and of the square lattice; another lattice.
- OEIS A271906 and arXiv:2607.22828: no isosceles right triangle in the square grid, a weaker condition in another lattice.

Verdict: new question for this lattice: right-angle-free subsets are studied for the square lattice (Gamble, Pulleyblank, Reed and Shepherd 1995; Junger and Pulleyblank) and isosceles right triangles in the square grid (A271906); no result was found for the honeycomb grid, and its first values are not in the OEIS.

## Best known value

21 for N = 15, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/hex-right.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..12: 2, 3, 3, 6, 8, 8, 10, 11, 11, 14, 16 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py).

## Cells

The same question at each value of its parameter (N, the side of the honeycomb grid): 14 cells, 11 of them exact (an exhaustive search finished) and 3 best known (ours). Each cell has its certificate in `refs/cells/hex-right/` (the headline cell uses `collections/originals/refs/hex-right.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example hex-right-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `hex-right-2` | 2 | 2 | exact |
| `hex-right-3` | 3 | 3 | exact |
| `hex-right-4` | 4 | 3 | exact |
| `hex-right-5` | 5 | 6 | exact |
| `hex-right-6` | 6 | 8 | exact |
| `hex-right-7` | 7 | 8 | exact |
| `hex-right-8` | 8 | 10 | exact |
| `hex-right-9` | 9 | 11 | exact |
| `hex-right-10` | 10 | 11 | exact |
| `hex-right-11` | 11 | 14 | exact |
| `hex-right-12` | 12 | 16 | exact |
| `hex-right-13` | 13 | 16 | best known |
| `hex-right-14` | 14 | 19 | best known |
| `hex-right-15` | 15 | 21 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

## Submitting and checking

Format: Text file: one point 'a b' per line, a point of the region of side 15 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check hex-right FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py hex-right 15 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/hex-right.txt`.

## References

- B. Gamble, W. Pulleyblank, B. Reed, B. Shepherd, Right angle free subsets in the plane, Graphs and Combinatorics 11 (1995) 121-129
- A Salem-Spencer-type construction for large subsets of integer grids with no isosceles right triangles, arXiv:2607.22828 (2026)
- OEIS A271906 (largest subsets of the n x n grid with no right isosceles triangle)
