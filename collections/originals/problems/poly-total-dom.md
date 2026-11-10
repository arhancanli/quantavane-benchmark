# Total domination in the regular 4-polytopes

`poly-total-dom` · Combinatorics and graph theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **194** (minimize), Quantavane (Arhan Canli), 10 November 2026: 194 for the 120-cell, best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts

## Statement

A set D of vertices is totally dominating when every vertex, in D or not, has a neighbour in D; the total domination number gamma_t is the smallest size of such a set. Determine gamma_t for the graphs of the six regular convex 4-polytopes (the 5-cell K5; the tesseract, 16 vertices; the 16-cell, 8 vertices; the 24-cell, 24 vertices, 8-regular; the 600-cell, 120 vertices, 12-regular; the 120-cell, 600 vertices, 4-regular) and of the two E8 polytopes 3_21 (Gosset, 56 vertices, 27-regular) and 4_21 (the 240 roots of E8, 56-regular), each vertex adjacent to its nearest neighbours. First values (ours): the 5-cell 2 (exact); the tesseract (8-cell) 4 (exact); the 16-cell 2 (exact); the 24-cell 4 (exact); the 600-cell 16; the 120-cell 194; the Gosset polytope 3_21 4 (exact); the E8 root polytope 4_21 9. The headline cell is the 120-cell: find a certificate with value 193 or less (gamma_t >= n/d for a d-regular graph: >= 150 for the 120-cell), or prove 194 optimal.

## Why it is interesting

Total domination (Cockayne, Dawes and Hedetniemi 1980) asks for monitors that are themselves monitored; for a d-regular graph gamma_t >= n/d, with equality exactly when the graph has a total perfect code (every vertex has exactly one neighbour in D): the bound is 10 for the 600-cell, 150 for the 120-cell, 3 for 3_21 and 5 for 4_21. Henning and Yeo's monograph collects the known values (paths, cycles, grids, some products and hypercubes); for these polytope graphs nothing was found.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/poly-total-dom.json`](../novelty/poly-total-dom.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"total domination" AND all:polytope`: 2 results
  - `all:"total domination" AND all:"600-cell"`: 0 results
  - `all:"total domination" AND (all:"E8" OR all:Gosset OR all:"E_8")`: 0 results
- Crossref (the journal literature, ranked by relevance), 2 searches:
  - `total domination number regular polytopes`: first results "Fractal Graph of Total Regular Fractional Domination Number" (2024); "Grundy total domination number of bipartite k-regular graphs" (2017); "Regular Polytopes" (2002)
  - `total domination number 600-cell 120-cell polytope graph`: first results "Bounds on the locating-domination number and differentiating-total domination number in trees" (2018); "Total domination and total domination subdivision number of a graph and its complement" (2008); "Graphs with large total domination number" (2000)
- Web search (general web search), `"total domination" OR "independent domination" OR "odd cycle transversal" OR "distance-2 coloring" OR "connected domination" 600-cell OR 120-cell OR 24-cell graph`: general results (Henning and Yeo's book, total dominator colourings of Moore graphs, Dejter on efficient domination in vertex-transitive graphs, TI-partitions); nothing on these invariants for the 4-polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no total domination family.

Closest work found, and how this problem differs:
- General results on total domination (the references) and its values for hypercubes, grids and products; none for these polytopes.
- Our polytope problems (polytope-ising, potts3-600, cell600-idcode, cell600-forest, cell120-coil, e8-idcode, e8-resolving): other invariants of the same graphs.

Verdict: new. No total domination result for the 600-cell, the 120-cell, the 24-cell or the E8 polytopes (searched with E8 and Gosset) was found on arXiv, in the journal literature (Crossref) or by web search; the known values for hypercubes and complete graphs cover only the small cells.

## Best known value

194 for the 120-cell, held by Quantavane (Arhan Canli), 10 November 2026: the certificate in `refs/poly-total-dom.txt` (best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts). All cells: the 5-cell 2 (exact); the tesseract (8-cell) 4 (exact); the 16-cell 2 (exact); the 24-cell 4 (exact); the 600-cell 16; the 120-cell 194; the Gosset polytope 3_21 4 (exact); the E8 root polytope 4_21 9. Bound: 150 (gamma_t >= n/d for a d-regular graph, for the 120-cell).

## Cells

The same question at each value of its parameter (KIND, the polytope): 8 cells, 5 of them exact (an exhaustive search finished) and 3 best known (ours). Each cell has its certificate in `refs/cells/poly-total-dom/` (the headline cell uses `collections/originals/refs/poly-total-dom.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example poly-total-dom-120-cell

| cell | KIND | value | status |
| --- | --- | --- | --- |
| `poly-total-dom-120-cell` | 120-cell | 194 | best known (headline) |
| `poly-total-dom-16-cell` | 16-cell | 2 | exact |
| `poly-total-dom-24-cell` | 24-cell | 4 | exact |
| `poly-total-dom-5-cell` | 5-cell | 2 | exact |
| `poly-total-dom-600-cell` | 600-cell | 16 | best known |
| `poly-total-dom-8-cell` | 8-cell | 4 | exact |
| `poly-total-dom-e8` | e8 | 9 | best known |
| `poly-total-dom-gosset` | gosset | 4 | exact |

Exact cells: proved optimal: CP-SAT (OR-Tools 9.15, one worker) closed the gap on the model of tools/polytope_sets.py, or, for zero forcing and power domination, the fort cuts (integer program over the forts found) met the best set found. Best known cells: best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts.

Bound on the other side: 150 (lower bound; gamma_t >= n/d for a d-regular graph, for the 120-cell).

## Submitting and checking

Format: Text file: the vertex numbers of the set (spaces or newlines), in the checker's vertex order (the 120-cell).

Score: the number of vertices in the set (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check poly-total-dom FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_graphs.py total-dom 120-cell FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/poly-total-dom.txt`.

## References

- E. J. Cockayne, R. M. Dawes, S. T. Hedetniemi, Total domination in graphs, Networks 10 (1980) 211-219
- M. A. Henning, A. Yeo, Total Domination in Graphs (Springer 2013)
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973)
- the vertex numbering of checkers/orig_phys.py (polytope_graph), shared by every polytope problem of the Originals
