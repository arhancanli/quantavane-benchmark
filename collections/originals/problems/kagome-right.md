# Right-angle-free sets in the kagome grid

`kagome-right` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **17** (maximize), Quantavane (Arhan Canli), 10 November 2026: 17 points of the region of side 13 with no right angle (no three points p, q, r with (q - p).(r - p) = 0), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the kagome grid K_N be the points (a, b) of the triangular grid T_N (the points a + b w, w = e^(i pi/3), a, b >= 0, a + b <= N - 1) with a and b not both even. Removing the sublattice 2Z[w] from the triangular lattice leaves the kagome lattice (corner-sharing triangles, four unit bonds at every site); the squared distance is da^2 + da db + db^2. Determine the largest number of points of the kagome grid K_N such that no three of them form a right angle (no three points p, q, r with (q - p).(r - p) = 0), as a function of N. The exact values are known (ours) for N <= 11; the headline cell is N = 13: find 18 or more such points of the region of side 13.

## Why it is interesting

A set of points is right-angle-free when no three of its points form a right angle. Gamble, Pulleyblank, Reed and Shepherd (1995) studied the largest right-angle-free subsets of the plane and of the square lattice, and related work (Junger and Pulleyblank) shows the problem NP-hard for general point sets; sets without isosceles right triangles in the n x n grid are a separate, active question (OEIS A271906; arXiv:2607.22828, 2026). The kagome lattice (corner-sharing triangles; the lattice of the frustrated kagome antiferromagnets) keeps three quarters of the triangular lattice; right angles occur in the same directions as there. How fast the largest right-angle-free sets grow is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/kagome-right.json`](../novelty/kagome-right.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"right angle" AND all:kagome AND all:subset`: 0 results
  - `all:"right triangle" AND all:kagome`: 0 results
  - `all:"right angle" AND all:"triangular lattice" AND all:"no three"`: 0 results
- OEIS, 1 searches:
  - `2,3,4,6,9,9,11,12,14,15`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `right angle free subsets kagome lattice`: first results "Right angle free subsets in the plane" (1995); "Kagome lattice"; "Kagome lattice"
- Web search (general web search), `no isosceles triangle OR no right angle subset kagome lattice OR body-centered cubic lattice points largest set combinatorial geometry`: the square-grid isosceles-free problem (Erdos problem #1207, Solymosi's notes, PatternBoost, AlphaEvolve) and lattice-point counting in triangles; nothing on the kagome or body-centred cubic lattices
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no right-angle-free family.

Closest work found, and how this problem differs:
- B. Gamble, W. Pulleyblank, B. Reed and B. Shepherd (1995): right-angle-free subsets of the plane and of the square lattice; another lattice.
- OEIS A271906 and arXiv:2607.22828: no isosceles right triangle in the square grid, a weaker condition in another lattice.

Verdict: new question for this lattice: right-angle-free subsets are studied for the square lattice (Gamble, Pulleyblank, Reed and Shepherd 1995; Junger and Pulleyblank) and isosceles right triangles in the square grid (A271906); no result was found for the kagome grid, and its first values are not in the OEIS.

## Best known value

17 for N = 13, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/kagome-right.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..11: 2, 3, 4, 6, 9, 9, 11, 12, 14, 15 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py).

## Cells

The same question at each value of its parameter (N, the side of the kagome grid): 12 cells, 10 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/kagome-right/` (the headline cell uses `collections/originals/refs/kagome-right.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example kagome-right-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `kagome-right-2` | 2 | 2 | exact |
| `kagome-right-3` | 3 | 3 | exact |
| `kagome-right-4` | 4 | 4 | exact |
| `kagome-right-5` | 5 | 6 | exact |
| `kagome-right-6` | 6 | 9 | exact |
| `kagome-right-7` | 7 | 9 | exact |
| `kagome-right-8` | 8 | 11 | exact |
| `kagome-right-9` | 9 | 12 | exact |
| `kagome-right-10` | 10 | 14 | exact |
| `kagome-right-11` | 11 | 15 | exact |
| `kagome-right-12` | 12 | 17 | best known |
| `kagome-right-13` | 13 | 17 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

## Submitting and checking

Format: Text file: one point 'a b' per line, a point of the region of side 13 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check kagome-right FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py kagome-right 13 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/kagome-right.txt`.

## References

- B. Gamble, W. Pulleyblank, B. Reed, B. Shepherd, Right angle free subsets in the plane, Graphs and Combinatorics 11 (1995) 121-129
- A Salem-Spencer-type construction for large subsets of integer grids with no isosceles right triangles, arXiv:2607.22828 (2026)
- OEIS A271906 (largest subsets of the n x n grid with no right isosceles triangle)
