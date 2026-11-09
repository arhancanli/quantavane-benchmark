# Three-state Potts antiferromagnet on the 600-cell

`potts3-600` · Physics · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **134** (minimize), Quantavane (Arhan Canli), 9 November 2026: simulated annealing over colourings (tools/potts.py, 6 restarts of 4,000 sweeps)

## Statement

Colour the 120 vertices of the 600-cell {3,3,5} with three colours (a 3-state Potts spin on each vertex) and count the monochromatic edges among its 720 edges: this is the energy of the 3-state Potts antiferromagnet, H(c) = number of edges uv with c_u = c_v. Determine the ground-state energy min H. Bounds: 120 <= min H <= 134; find a colouring with at most 133 monochromatic edges, or prove 134 optimal.

## Why it is interesting

Potts antiferromagnets on frustrated structures (the triangular, kagome and pyrochlore lattices) are a standard source of ground-state degeneracy and order by disorder. The 600-cell, the curved-space template of icosahedral order (Nelson 1983), is maximally frustrated for them: it is made of 600 tetrahedral cells, and in any 3-colouring each cell has a monochromatic edge; since each edge lies in 5 cells, at least 120 edges are monochromatic. With 5 colours the graph can be coloured properly (our annealer finds a proper 5-colouring, and 5 is needed because every vertex neighbourhood is an icosahedron, which needs 4 colours), so the 3- and 4-state models are the frustrated ones; for 4 colours our best colouring has 66 monochromatic edges. The Ising case (2 colours) is the separate problem polytope-ising.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/potts3-600.json`](../novelty/potts3-600.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:Potts AND all:"600-cell"`: 0 results
  - `all:"600-cell" AND all:coloring`: 2 results
  - `all:Potts AND all:antiferromagnet AND all:polytope`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no spin-model family.

Closest work found, and how this problem differs:
- Kochen-Specker colourings of the 600-cell's 60 rays (arXiv:0802.2533, arXiv:0911.2289): assignments to orthogonal tetrads, not vertex colourings of the polytope graph.

Verdict: new. Our arXiv searches found no paper or table on Potts antiferromagnets (or minimum monochromatic edges of colourings) of the 600-cell graph; the 600-cell colouring papers found on arXiv concern Kochen-Specker colourings of its rays, a different problem.

## First values

| colours q | fewest monochromatic edges | status |
| --- | --- | --- |
| 2 | 280 | open; equals the Ising problem polytope-ising (E = 2*280 - 720 = -160); lower bound 249 |
| 3 | 134 | open; lower bound 120 (one per tetrahedral cell, 5 cells per edge) |
| 4 | 66 | open; lower bound 18 (one per closed neighbourhood, 7 per edge) |
| 5 | 0 | exact: proper 5-colouring found; 5 colours are needed |

Upper bounds from our annealer (tools/potts.py); the checker scores any q (python3 -I collections/originals/checkers/orig_phys.py polytope-potts 600 Q FILE).

## Best known value

134, held by Quantavane (Arhan Canli), 9 November 2026: the colouring in `refs/potts3-600.txt`. Lower bound 120: each of the 600 tetrahedral cells (copies of K4) has a monochromatic edge in any 3-colouring, and each edge lies in exactly 5 cells.

Bound on the other side: 120 (lower bound; 600 tetrahedral cells, each with a monochromatic edge in any 3-colouring; 5 cells per edge).

## Submitting and checking

Format: Text file: 120 colours 0, 1 or 2, separated by spaces or newlines, one per vertex in the checker's vertex order (the 600-cell's vertices as exact coordinates in Q(sqrt 5), sorted; see polytope_graph in checkers/orig_phys.py).

Score: the number of monochromatic edges (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check potts3-600 FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_phys.py polytope-potts 600 3 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/potts3-600.txt`.

## References

- D. R. Nelson, Order, frustration, and defects in liquids and glasses, Phys. Rev. B 28 (1983) 5515
- R. J. Baxter, Exactly Solved Models in Statistical Mechanics (Academic Press, 1982): Potts models
- M. Waegell, P. K. Aravind et al., Critical noncolorings of the 600-cell proving the Bell-Kochen-Specker theorem, arXiv:0911.2289 (a different colouring problem on the 600-cell's rays)
