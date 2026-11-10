# Right-angle-free sets in the body-centred cubic crystal

`bcc-right` · Discrete geometry · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **15** (maximize), Quantavane (Arhan Canli), 10 November 2026: 15 points of the region of side 5 with no right angle (no three points p, q, r with (q - p).(r - p) = 0), the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)

## Statement

Let the body-centred cubic crystal B_N be the points (x, y, z) with 0 <= x, y, z <= 2N - 2 whose coordinates are all even (the N^3 corners of an (N-1) x (N-1) x (N-1) block of cubes of edge 2) or all odd (the (N-1)^3 cube centres); squared distance dx^2 + dy^2 + dz^2, nearest neighbours at squared distance 3. Determine the largest number of points of the body-centred cubic crystal B_N such that no three of them form a right angle (no three points p, q, r with (q - p).(r - p) = 0), as a function of N. The exact values are known (ours) for N <= 3; the headline cell is N = 5: find 16 or more such points of the region of side 5.

## Why it is interesting

A set of points is right-angle-free when no three of its points form a right angle. Gamble, Pulleyblank, Reed and Shepherd (1995) studied the largest right-angle-free subsets of the plane and of the square lattice, and related work (Junger and Pulleyblank) shows the problem NP-hard for general point sets; sets without isosceles right triangles in the n x n grid are a separate, active question (OEIS A271906; arXiv:2607.22828, 2026). In the body-centred cubic crystal the cube axes are perpendicular, and so are many face and body diagonals (for example (1, 1, 1) and (1, -1, 0)); how fast the largest right-angle-free sets grow is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/bcc-right.json`](../novelty/bcc-right.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"right angle" AND all:"body-centered cubic" AND all:subset`: 0 results
  - `all:"right-angle-free"`: 0 results
  - `all:"right angle" AND all:"body-centred cubic" AND all:points`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `right angle free subsets body-centred cubic lattice points`: first results "II. The simple cubic lattice and the body-centred cubic lattice" (1938); "959. Behaviour of lithium atoms on the faces of single crystal refractory metals with body centred cubic lattice" (1972); "STATISTICAL THEORY OF SUPERLATTICES OF THE TYPE AB IN A BODY-CENTRED CUBIC LATTICE" (1956)
- Web search (general web search), `no isosceles triangle OR no right angle subset kagome lattice OR body-centered cubic lattice points largest set combinatorial geometry`: the square-grid isosceles-free problem (Erdos problem #1207, Solymosi's notes, PatternBoost, AlphaEvolve) and lattice-point counting in triangles; nothing on the kagome or body-centred cubic lattices
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no right-angle-free family.

Closest work found, and how this problem differs:
- B. Gamble, W. Pulleyblank, B. Reed and B. Shepherd (1995): right-angle-free subsets of the plane and of the square lattice; another lattice.
- OEIS A271906 and arXiv:2607.22828: no isosceles right triangle in the square grid, a weaker condition in another lattice.

Verdict: new question for this lattice: right-angle-free subsets are studied for the square lattice (Gamble, Pulleyblank, Reed and Shepherd 1995; Junger and Pulleyblank) and isosceles right triangles in the square grid (A271906); no result was found for the body-centred cubic crystal, and it is not in the OEIS by name (too few exact values are known to search by terms).

## Best known value

15 for N = 5, held by Quantavane (Arhan Canli), 10 November 2026: the points in `refs/bcc-right.txt` (the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py)). Exact values for N = 2..3: 5, 9 (CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py).

## Cells

The same question at each value of its parameter (N, the side of the body-centred cubic crystal): 4 cells, 2 of them exact (an exhaustive search finished) and 2 best known (ours). Each cell has its certificate in `refs/cells/bcc-right/` (the headline cell uses `collections/originals/refs/bcc-right.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example bcc-right-2

| cell | N | value | status |
| --- | --- | --- | --- |
| `bcc-right-2` | 2 | 5 | exact |
| `bcc-right-3` | 3 | 9 | exact |
| `bcc-right-4` | 4 | 12 | best known |
| `bcc-right-5` | 5 | 15 | best known (headline) |

Exact cells: CP-SAT (OR-Tools 9.15, one worker) proved the optimum of the 0/1 model in tools/lattice_sets.py. Best known cells: the best set CP-SAT found in 10 seconds, started from the set for side N - 1 (tools/lattice_sets.py).

## Submitting and checking

Format: Text file: one point 'x y z' per line, a point of the region of side 5 (lines starting with # are ignored).

Score: the number of points (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check bcc-right FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_lattice.py bcc-right 5 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/bcc-right.txt`.

## References

- B. Gamble, W. Pulleyblank, B. Reed, B. Shepherd, Right angle free subsets in the plane, Graphs and Combinatorics 11 (1995) 121-129
- A Salem-Spencer-type construction for large subsets of integer grids with no isosceles right triangles, arXiv:2607.22828 (2026)
- OEIS A271906 (largest subsets of the n x n grid with no right isosceles triangle)
