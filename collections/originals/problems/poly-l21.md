# L(2,1)-labellings of the regular 4-polytopes

`poly-l21` · Combinatorics and graph theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **9** (minimize), Quantavane (Arhan Canli), 10 November 2026: 9 for the 120-cell, best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts

## Statement

An L(2,1)-labelling gives every vertex a non-negative integer label so that adjacent vertices get labels at least 2 apart and vertices at distance 2 get different labels; its span is the largest label, and lambda(G) is the smallest span. Determine lambda(G) for the graphs of the six regular convex 4-polytopes (the 5-cell K5; the tesseract, 16 vertices; the 16-cell, 8 vertices; the 24-cell, 24 vertices, 8-regular; the 600-cell, 120 vertices, 12-regular; the 120-cell, 600 vertices, 4-regular) and of the two E8 polytopes 3_21 (Gosset, 56 vertices, 27-regular) and 4_21 (the 240 roots of E8, 56-regular), each vertex adjacent to its nearest neighbours. First values (ours): the 5-cell 8 (exact); the tesseract (8-cell) 7 (exact); the 16-cell 10 (exact); the 24-cell 13; the 600-cell 24; the 120-cell 9; the Gosset polytope 3_21 55. The headline cell is the 120-cell: find a certificate with value 8 or less (lambda >= Delta + 1 (Griggs and Yeh): >= 5 for the 120-cell), or prove 9 optimal.

## Why it is interesting

L(2,1)-labellings model frequency assignment, where nearby transmitters need different and adjacent ones well-separated channels (Griggs and Yeh 1992, after Roberts); lambda >= Delta + 1, and the Griggs-Yeh conjecture lambda <= Delta^2 is proved for large Delta (Havet, Reed and Sereni). Values are known for paths, cycles, grids and many products, and bounds for hypercubes; for these polytope graphs nothing was found.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/poly-l21.json`](../novelty/poly-l21.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"L(2,1)-labeling" AND all:polytope`: 0 results
  - `all:"L(2,1)" AND all:"600-cell"`: 0 results
  - `all:"L(2,1)" AND (all:"E8" OR all:Gosset OR all:"E_8")`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `L(2,1) labelling regular polytope graphs`: first results "Fence facets from non-regular graphs for the linear ordering polytope" (2013); "Polytope Typology A: The separation of facial polytopes in the morphology of the regular and semi-regular polyhedra and tessellations" (2025); "Polytope Propagation on Graphs" (2005)
- Web search (general web search), `"L(2,1)" labeling OR "bandwidth" OR "bisection width" OR "cutwidth" of the 600-cell OR 120-cell OR 24-cell graph polytope 1-skeleton`: general L(2,1)-labelling papers, Deza-Grishukhin on the 120-cell skeleton (not an l1-graph) and the geometry of H4 polytopes; nothing on these invariants for the 4-polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no L(2,1) family.

Closest work found, and how this problem differs:
- General results on L(2,1) (the references) and its values for hypercubes, grids and products; none for these polytopes.
- Our polytope problems (polytope-ising, potts3-600, cell600-idcode, cell600-forest, cell120-coil, e8-idcode, e8-resolving): other invariants of the same graphs.

Verdict: new. No L(2,1) result for the 600-cell, the 120-cell, the 24-cell or the E8 polytopes (searched with E8 and Gosset) was found on arXiv, in the journal literature (Crossref) or by web search; the known values for hypercubes and complete graphs cover only the small cells.

## Best known value

9 for the 120-cell, held by Quantavane (Arhan Canli), 10 November 2026: the certificate in `refs/poly-l21.txt` (best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts). All cells: the 5-cell 8 (exact); the tesseract (8-cell) 7 (exact); the 16-cell 10 (exact); the 24-cell 13; the 600-cell 24; the 120-cell 9; the Gosset polytope 3_21 55. Bound: 5 (lambda >= Delta + 1 (Griggs and Yeh), for the 120-cell).

## Cells

The same question at each value of its parameter (KIND, the polytope): 7 cells, 3 of them exact (an exhaustive search finished) and 4 best known (ours). Each cell has its certificate in `refs/cells/poly-l21/` (the headline cell uses `collections/originals/refs/poly-l21.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example poly-l21-120-cell

| cell | KIND | value | status |
| --- | --- | --- | --- |
| `poly-l21-120-cell` | 120-cell | 9 | best known (headline) |
| `poly-l21-16-cell` | 16-cell | 10 | exact |
| `poly-l21-24-cell` | 24-cell | 13 | best known |
| `poly-l21-5-cell` | 5-cell | 8 | exact |
| `poly-l21-600-cell` | 600-cell | 24 | best known |
| `poly-l21-8-cell` | 8-cell | 7 | exact |
| `poly-l21-gosset` | gosset | 55 | best known |

Exact cells: proved optimal: CP-SAT (OR-Tools 9.15, one worker) closed the gap on the model of tools/polytope_sets.py, or, for zero forcing and power domination, the fort cuts (integer program over the forts found) met the best set found. Best known cells: best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts.

Bound on the other side: 5 (lower bound; lambda >= Delta + 1 (Griggs and Yeh), for the 120-cell).

## Submitting and checking

Format: Text file: one label per vertex, in the checker's vertex order (the 120-cell).

Score: the span, the largest label (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check poly-l21 FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_graphs.py l21 120-cell FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/poly-l21.txt`.

## References

- J. R. Griggs, R. K. Yeh, Labelling graphs with a condition at distance 2, SIAM J. Discrete Math. 5 (1992) 586-595
- F. Havet, B. Reed, J.-S. Sereni, L(2,1)-labelling of graphs, Proc. SODA 2008
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973)
- the vertex numbering of checkers/orig_phys.py (polytope_graph), shared by every polytope problem of the Originals
