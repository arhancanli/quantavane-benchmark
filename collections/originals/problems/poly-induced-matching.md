# Induced matchings in the regular 4-polytopes

`poly-induced-matching` · Combinatorics and graph theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **139** (maximize), Quantavane (Arhan Canli), 10 November 2026: 139 for the 120-cell, best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts

## Statement

An induced (strong) matching is a set of edges, no two sharing a vertex and no two joined by an edge of the graph. Determine the largest size of an induced matching for the graphs of the six regular convex 4-polytopes (the 5-cell K5; the tesseract, 16 vertices; the 16-cell, 8 vertices; the 24-cell, 24 vertices, 8-regular; the 600-cell, 120 vertices, 12-regular; the 120-cell, 600 vertices, 4-regular) and of the two E8 polytopes 3_21 (Gosset, 56 vertices, 27-regular) and 4_21 (the 240 roots of E8, 56-regular), each vertex adjacent to its nearest neighbours. First values (ours): the 5-cell 1 (exact); the tesseract (8-cell) 4 (exact); the 16-cell 1 (exact); the 24-cell 4 (exact); the 600-cell 13; the 120-cell 139; the Gosset polytope 3_21 3 (exact); the E8 root polytope 4_21 7. The headline cell is the 120-cell: find a certificate with value 140 or more (the packing bound |M| (2d - 1) <= nd/2: <= 171 for the 120-cell), or prove 139 optimal.

## Why it is interesting

Induced matchings (Stockmeyer and Vazirani 1982, Cameron 1989) bound the strong chromatic index, model interference-free transmissions in radio networks, and are NP-hard to maximise. Their values are known for hypercubes and grids; for the other regular 4-polytopes and the E8 polytopes nothing was found. In a d-regular graph the 2d - 1 edges touching one edge of an induced matching touch no other edge of it (an edge between two of them is forbidden), so |M| (2d - 1) <= nd/2: at most 31 for the 600-cell, 171 for the 120-cell, 14 for 3_21 and 60 for 4_21. How close the matchings come to this packing bound is open.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/poly-induced-matching.json`](../novelty/poly-induced-matching.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:"induced matching" AND all:"600-cell"`: 0 results
  - `all:"induced matching" AND all:polytope`: 1 result
  - `all:"strong matching" AND all:"regular polytope"`: 0 results
  - `all:"induced matching" AND (all:"E8" OR all:Gosset OR all:"E_8")`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `maximum induced matching regular polytope graph`: first results "Core index of perfect matching polytope for a 2-connected cubic graph" (2018); "Maximum Matching in Regular and Almost Regular Graphs" (2012); "Tight Lower Bounds on the Size of a Maximum Matching in a Regular Graph" (2007)
- Web search (general web search), `"locating-dominating" OR "induced matching" OR "burning number" OR "metric dimension" graph of the 600-cell OR 120-cell OR 24-cell polytope`: surveys of metric dimension and Bailey's metric dimension of small distance-regular graphs; nothing on locating-dominating sets, induced matchings or burning of the 4-polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no induced matching family.

Closest work found, and how this problem differs:
- General results on induced matching (the references) and its values for hypercubes, grids and products; none for these polytopes.
- Our polytope problems (polytope-ising, potts3-600, cell600-idcode, cell600-forest, cell120-coil, e8-idcode, e8-resolving): other invariants of the same graphs.

Verdict: new. No induced matching result for the 600-cell, the 120-cell, the 24-cell or the E8 polytopes (searched with E8 and Gosset) was found on arXiv, in the journal literature (Crossref) or by web search; the known values for hypercubes and complete graphs cover only the small cells.

## Best known value

139 for the 120-cell, held by Quantavane (Arhan Canli), 10 November 2026: the certificate in `refs/poly-induced-matching.txt` (best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts). All cells: the 5-cell 1 (exact); the tesseract (8-cell) 4 (exact); the 16-cell 1 (exact); the 24-cell 4 (exact); the 600-cell 13; the 120-cell 139; the Gosset polytope 3_21 3 (exact); the E8 root polytope 4_21 7. Bound: 171 (the packing bound |M| (2d - 1) <= nd/2, for the 120-cell).

## Cells

The same question at each value of its parameter (KIND, the polytope): 8 cells, 5 of them exact (an exhaustive search finished) and 3 best known (ours). Each cell has its certificate in `refs/cells/poly-induced-matching/` (the headline cell uses `collections/originals/refs/poly-induced-matching.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example poly-induced-matching-120-cell

| cell | KIND | value | status |
| --- | --- | --- | --- |
| `poly-induced-matching-120-cell` | 120-cell | 139 | best known (headline) |
| `poly-induced-matching-16-cell` | 16-cell | 1 | exact |
| `poly-induced-matching-24-cell` | 24-cell | 4 | exact |
| `poly-induced-matching-5-cell` | 5-cell | 1 | exact |
| `poly-induced-matching-600-cell` | 600-cell | 13 | best known |
| `poly-induced-matching-8-cell` | 8-cell | 4 | exact |
| `poly-induced-matching-e8` | e8 | 7 | best known |
| `poly-induced-matching-gosset` | gosset | 3 | exact |

Exact cells: proved optimal: CP-SAT (OR-Tools 9.15, one worker) closed the gap on the model of tools/polytope_sets.py, or, for zero forcing and power domination, the fort cuts (integer program over the forts found) met the best set found. Best known cells: best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts.

Bound on the other side: 171 (upper bound; the packing bound |M| (2d - 1) <= nd/2, for the 120-cell).

## Submitting and checking

Format: Text file: one edge 'u v' per line (vertex numbers in the checker's vertex order) (the 120-cell).

Score: the number of edges (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check poly-induced-matching FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_graphs.py induced-matching 120-cell FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/poly-induced-matching.txt`.

## References

- L. J. Stockmeyer, V. V. Vazirani, NP-completeness of some generalizations of the maximum matching problem, Inform. Process. Lett. 15 (1982) 14-19
- K. Cameron, Induced matchings, Discrete Appl. Math. 24 (1989) 97-102
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973)
- the vertex numbering of checkers/orig_phys.py (polytope_graph), shared by every polytope problem of the Originals
