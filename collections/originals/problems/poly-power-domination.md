# Power domination in the regular 4-polytopes

`poly-power-domination` · Combinatorics and graph theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **28** (minimize), Quantavane (Arhan Canli), 10 November 2026: 28 for the 120-cell, best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts

## Statement

A set S of vertices power dominates the graph when, starting from S and all neighbours of S as observed vertices, the rule 'an observed vertex with exactly one unobserved neighbour observes it' eventually observes every vertex; the power domination number is the smallest size of such a set. Determine the power domination number for the graphs of the six regular convex 4-polytopes (the 5-cell K5; the tesseract, 16 vertices; the 16-cell, 8 vertices; the 24-cell, 24 vertices, 8-regular; the 600-cell, 120 vertices, 12-regular; the 120-cell, 600 vertices, 4-regular) and of the two E8 polytopes 3_21 (Gosset, 56 vertices, 27-regular) and 4_21 (the 240 roots of E8, 56-regular), each vertex adjacent to its nearest neighbours. First values (ours): the 5-cell 1 (exact); the tesseract (8-cell) 2 (exact); the 16-cell 1 (exact); the 24-cell 2 (exact); the 600-cell 5; the 120-cell 28; the Gosset polytope 3_21 2; the E8 root polytope 4_21 6. The headline cell is the 120-cell: find a certificate with value 27 or less (Z(G) <= Delta * gamma_P(G) with the spectral bound for Z(G): >= 12 for the 120-cell), or prove 28 optimal.

## Why it is interesting

Power domination models the placement of phase measurement units that monitor an electrical network (Haynes, Hedetniemi, Hedetniemi and Henning 2002); it is zero forcing started from a closed neighbourhood, so Z(G) <= Delta * gamma_P(G) and the spectral bound for zero forcing gives gamma_P >= (largest eigenvalue multiplicity) / Delta: at least 3 for the 600-cell, 12 for the 120-cell, 1 for 3_21 and 2 for 4_21. Values are known for grids, hypercubes and products; for these polytopes nothing was found.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/poly-power-domination.json`](../novelty/poly-power-domination.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"power domination" AND all:polytope`: 0 results
  - `all:"power domination" AND all:"600-cell"`: 0 results
  - `all:"power domination" AND (all:"E8" OR all:Gosset OR all:"E_8")`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `power domination polytope graphs`: first results "Power Domination in Graphs" (2020); "On the Equality of Accurate Power Domination and Power Domination Numbers of Some Graphs" (2025); "Planar graphs : non-aligned drawings, power domination and enumeration of Eulerian orientations"
- Web search (general web search), `"zero forcing" OR "power domination" graph of the 600-cell OR 120-cell OR 24-cell OR "regular 4-polytope"`: general papers on zero forcing and power domination (arXiv:1510.02421, graph products, iterated line digraphs, a thesis on variations); nothing on the 4-polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no power domination family.

Closest work found, and how this problem differs:
- General results on power domination (the references) and its values for hypercubes, grids and products; none for these polytopes.
- Our polytope problems (polytope-ising, potts3-600, cell600-idcode, cell600-forest, cell120-coil, e8-idcode, e8-resolving): other invariants of the same graphs.

Verdict: new. No power domination result for the 600-cell, the 120-cell, the 24-cell or the E8 polytopes (searched with E8 and Gosset) was found on arXiv, in the journal literature (Crossref) or by web search; the known values for hypercubes and complete graphs cover only the small cells.

## Best known value

28 for the 120-cell, held by Quantavane (Arhan Canli), 10 November 2026: the certificate in `refs/poly-power-domination.txt` (best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts). All cells: the 5-cell 1 (exact); the tesseract (8-cell) 2 (exact); the 16-cell 1 (exact); the 24-cell 2 (exact); the 600-cell 5; the 120-cell 28; the Gosset polytope 3_21 2; the E8 root polytope 4_21 6. Bound: 12 (Z(G) <= Delta * gamma_P(G) with the spectral bound for Z(G), for the 120-cell).

## Cells

The same question at each value of its parameter (KIND, the polytope): 8 cells, 4 of them exact (an exhaustive search finished) and 4 best known (ours). Each cell has its certificate in `refs/cells/poly-power-domination/` (the headline cell uses `collections/originals/refs/poly-power-domination.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example poly-power-domination-120-cell

| cell | KIND | value | status |
| --- | --- | --- | --- |
| `poly-power-domination-120-cell` | 120-cell | 28 | best known (headline) |
| `poly-power-domination-16-cell` | 16-cell | 1 | exact |
| `poly-power-domination-24-cell` | 24-cell | 2 | exact |
| `poly-power-domination-5-cell` | 5-cell | 1 | exact |
| `poly-power-domination-600-cell` | 600-cell | 5 | best known |
| `poly-power-domination-8-cell` | 8-cell | 2 | exact |
| `poly-power-domination-e8` | e8 | 6 | best known |
| `poly-power-domination-gosset` | gosset | 2 | best known |

Exact cells: proved optimal: CP-SAT (OR-Tools 9.15, one worker) closed the gap on the model of tools/polytope_sets.py, or, for zero forcing and power domination, the fort cuts (integer program over the forts found) met the best set found. Best known cells: best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts.

Bound on the other side: 12 (lower bound; Z(G) <= Delta * gamma_P(G) with the spectral bound for Z(G), for the 120-cell).

## Submitting and checking

Format: Text file: the vertex numbers of the set (spaces or newlines), in the checker's vertex order (the 120-cell).

Score: the number of vertices in the set (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check poly-power-domination FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_graphs.py power-domination 120-cell FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/poly-power-domination.txt`.

## References

- T. W. Haynes, S. M. Hedetniemi, S. T. Hedetniemi, M. A. Henning, Domination in graphs applied to electric power networks, SIAM J. Discrete Math. 15 (2002) 519-529
- K. F. Benson, D. Ferrero, M. Flagg, V. Furst, L. Hogben, V. Vasilevska, B. Wissman, Zero forcing and power domination for graph products, Australas. J. Combin. 70 (2018) 221-235
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973)
- the vertex numbering of checkers/orig_phys.py (polytope_graph), shared by every polytope problem of the Originals
