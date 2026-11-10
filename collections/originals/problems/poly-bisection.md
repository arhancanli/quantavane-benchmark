# Bisection width of the regular 4-polytopes

`poly-bisection` · Combinatorics and graph theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **120** (minimize), Quantavane (Arhan Canli), 10 November 2026: 120 for the 120-cell, best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts

## Statement

The bisection width is the smallest number of edges between two halves of the vertex set of equal size. Determine the bisection width for the graphs of the six regular convex 4-polytopes (the 5-cell K5; the tesseract, 16 vertices; the 16-cell, 8 vertices; the 24-cell, 24 vertices, 8-regular; the 600-cell, 120 vertices, 12-regular; the 120-cell, 600 vertices, 4-regular) and of the two E8 polytopes 3_21 (Gosset, 56 vertices, 27-regular) and 4_21 (the 240 roots of E8, 56-regular), each vertex adjacent to its nearest neighbours. First values (ours): the 5-cell 6 (exact); the tesseract (8-cell) 8 (exact); the 16-cell 12 (exact); the 24-cell 32; the 600-cell 176; the 120-cell 120; the Gosset polytope 3_21 306; the E8 root polytope 4_21 2292. The headline cell is the 120-cell: find a certificate with value 119 or less, or prove 120 optimal.

## Why it is interesting

Bisection width measures the communication bottleneck of an interconnection network and is NP-hard (Garey, Johnson and Stockmeyer 1976); the spectral bound (Fiedler; Donath and Hoffman) gives width >= mu_2 n/4 with mu_2 the second smallest Laplacian eigenvalue, about 69 for the 600-cell and 22 for the 120-cell. For hypercubes the answer is classical (2^(n-1)); for the other polytopes nothing was found.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/poly-bisection.json`](../novelty/poly-bisection.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:"bisection width" AND all:polytope`: 0 results
  - `all:"bisection width" AND all:"600-cell"`: 0 results
  - `all:"edge isoperimetric" AND all:"600-cell"`: 0 results
  - `all:"bisection" AND (all:"E8" OR all:Gosset OR all:"E_8")`: 1 result
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `bisection width polytope graph`: first results "On the Graph Bisection Cut Polytope" (2008); "On Alliance Partitions and Bisection Width for Planar Graphs" (2013); "Calculation on the Bisection Width of H-Torus Topology" (2009)
- Web search (general web search), `"L(2,1)" labeling OR "bandwidth" OR "bisection width" OR "cutwidth" of the 600-cell OR 120-cell OR 24-cell graph polytope 1-skeleton`: general L(2,1)-labelling papers, Deza-Grishukhin on the 120-cell skeleton (not an l1-graph) and the geometry of H4 polytopes; nothing on these invariants for the 4-polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no bisection width family.

Closest work found, and how this problem differs:
- General results on bisection width (the references) and its values for hypercubes, grids and products; none for these polytopes.
- Our polytope problems (polytope-ising, potts3-600, cell600-idcode, cell600-forest, cell120-coil, e8-idcode, e8-resolving): other invariants of the same graphs.

Verdict: new. No bisection width result for the 600-cell, the 120-cell, the 24-cell or the E8 polytopes (searched with E8 and Gosset) was found on arXiv, in the journal literature (Crossref) or by web search; the known values for hypercubes and complete graphs cover only the small cells.

## Best known value

120 for the 120-cell, held by Quantavane (Arhan Canli), 10 November 2026: the certificate in `refs/poly-bisection.txt` (best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts). All cells: the 5-cell 6 (exact); the tesseract (8-cell) 8 (exact); the 16-cell 12 (exact); the 24-cell 32; the 600-cell 176; the 120-cell 120; the Gosset polytope 3_21 306; the E8 root polytope 4_21 2292.

## Cells

The same question at each value of its parameter (KIND, the polytope): 8 cells, 3 of them exact (an exhaustive search finished) and 5 best known (ours). Each cell has its certificate in `refs/cells/poly-bisection/` (the headline cell uses `collections/originals/refs/poly-bisection.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example poly-bisection-120-cell

| cell | KIND | value | status |
| --- | --- | --- | --- |
| `poly-bisection-120-cell` | 120-cell | 120 | best known (headline) |
| `poly-bisection-16-cell` | 16-cell | 12 | exact |
| `poly-bisection-24-cell` | 24-cell | 32 | best known |
| `poly-bisection-5-cell` | 5-cell | 6 | exact |
| `poly-bisection-600-cell` | 600-cell | 176 | best known |
| `poly-bisection-8-cell` | 8-cell | 8 | exact |
| `poly-bisection-e8` | e8 | 2292 | best known |
| `poly-bisection-gosset` | gosset | 306 | best known |

Exact cells: proved optimal: CP-SAT (OR-Tools 9.15, one worker) closed the gap on the model of tools/polytope_sets.py, or, for zero forcing and power domination, the fort cuts (integer program over the forts found) met the best set found. Best known cells: best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts.

## Submitting and checking

Format: Text file: one bit 0 or 1 per vertex in the checker's vertex order, as many 0s as 1s (the 120-cell).

Score: the number of edges between the halves (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check poly-bisection FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_graphs.py bisection 120-cell FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/poly-bisection.txt`.

## References

- M. R. Garey, D. S. Johnson, L. Stockmeyer, Some simplified NP-complete graph problems, Theoret. Comput. Sci. 1 (1976) 237-267
- W. E. Donath, A. J. Hoffman, Lower bounds for the partitioning of graphs, IBM J. Res. Develop. 17 (1973) 420-425
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973)
- the vertex numbering of checkers/orig_phys.py (polytope_graph), shared by every polytope problem of the Originals
