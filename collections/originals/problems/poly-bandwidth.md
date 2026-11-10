# Bandwidth of the regular 4-polytopes

`poly-bandwidth` · Combinatorics and graph theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **80** (minimize), Quantavane (Arhan Canli), 10 November 2026: 80 for the 120-cell, best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts

## Statement

The bandwidth of a graph is the smallest, over all numberings of its vertices by 1..n, of the largest difference between the numbers of two adjacent vertices. Determine the bandwidth for the graphs of the six regular convex 4-polytopes (the 5-cell K5; the tesseract, 16 vertices; the 16-cell, 8 vertices; the 24-cell, 24 vertices, 8-regular; the 600-cell, 120 vertices, 12-regular; the 120-cell, 600 vertices, 4-regular) and of the two E8 polytopes 3_21 (Gosset, 56 vertices, 27-regular) and 4_21 (the 240 roots of E8, 56-regular), each vertex adjacent to its nearest neighbours. First values (ours): the 5-cell 4 (exact); the tesseract (8-cell) 7 (exact); the 16-cell 6 (exact); the 24-cell 13; the 600-cell 43; the 120-cell 80; the Gosset polytope 3_21 43; the E8 root polytope 4_21 182. The headline cell is the 120-cell: find a certificate with value 79 or less ((n - 1)/diameter: >= 40 for the 120-cell), or prove 80 optimal.

## Why it is interesting

Bandwidth governs banded storage and elimination of sparse matrices and is NP-hard (Papadimitriou 1976); Harper (1966) determined it for the hypercubes with his vertex-isoperimetric theorem, so the tesseract cell is classical. A numbering has bandwidth at least (n - 1)/diameter, and at least the vertex-boundary of the best sets of each size; the polytope graphs have large, symmetric neighbourhoods, and nothing was found for them.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/poly-bandwidth.json`](../novelty/poly-bandwidth.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:bandwidth AND all:"600-cell"`: 0 results
  - `all:"bandwidth" AND all:"regular polytope" AND all:graph`: 0 results
  - `all:"cutwidth" AND all:polytope AND all:graph`: 1 result
  - `all:"bandwidth" AND (all:"E8" OR all:Gosset OR all:"E_8")`: 1 result
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `bandwidth of polytope graphs vertex ordering`: first results "Vertex Ordering Characterizations of Graphs of Bounded Asteroidal Number" (2014); "A vertex ordering characterization of simple-triangle graphs" (2018); "Optimal vertex ordering of graphs" (1999)
- Web search (general web search), `"L(2,1)" labeling OR "bandwidth" OR "bisection width" OR "cutwidth" of the 600-cell OR 120-cell OR 24-cell graph polytope 1-skeleton`: general L(2,1)-labelling papers, Deza-Grishukhin on the 120-cell skeleton (not an l1-graph) and the geometry of H4 polytopes; nothing on these invariants for the 4-polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no bandwidth family.

Closest work found, and how this problem differs:
- General results on bandwidth (the references) and its values for hypercubes, grids and products; none for these polytopes.
- Our polytope problems (polytope-ising, potts3-600, cell600-idcode, cell600-forest, cell120-coil, e8-idcode, e8-resolving): other invariants of the same graphs.

Verdict: new. No bandwidth result for the 600-cell, the 120-cell, the 24-cell or the E8 polytopes (searched with E8 and Gosset) was found on arXiv, in the journal literature (Crossref) or by web search; the known values for hypercubes and complete graphs cover only the small cells.

## Best known value

80 for the 120-cell, held by Quantavane (Arhan Canli), 10 November 2026: the certificate in `refs/poly-bandwidth.txt` (best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts). All cells: the 5-cell 4 (exact); the tesseract (8-cell) 7 (exact); the 16-cell 6 (exact); the 24-cell 13; the 600-cell 43; the 120-cell 80; the Gosset polytope 3_21 43; the E8 root polytope 4_21 182. Bound: 40 ((n - 1)/diameter, for the 120-cell).

## Cells

The same question at each value of its parameter (KIND, the polytope): 8 cells, 3 of them exact (an exhaustive search finished) and 5 best known (ours). Each cell has its certificate in `refs/cells/poly-bandwidth/` (the headline cell uses `collections/originals/refs/poly-bandwidth.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example poly-bandwidth-120-cell

| cell | KIND | value | status |
| --- | --- | --- | --- |
| `poly-bandwidth-120-cell` | 120-cell | 80 | best known (headline) |
| `poly-bandwidth-16-cell` | 16-cell | 6 | exact |
| `poly-bandwidth-24-cell` | 24-cell | 13 | best known |
| `poly-bandwidth-5-cell` | 5-cell | 4 | exact |
| `poly-bandwidth-600-cell` | 600-cell | 43 | best known |
| `poly-bandwidth-8-cell` | 8-cell | 7 | exact |
| `poly-bandwidth-e8` | e8 | 182 | best known |
| `poly-bandwidth-gosset` | gosset | 43 | best known |

Exact cells: proved optimal: CP-SAT (OR-Tools 9.15, one worker) closed the gap on the model of tools/polytope_sets.py, or, for zero forcing and power domination, the fort cuts (integer program over the forts found) met the best set found. Best known cells: best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts.

Bound on the other side: 40 (lower bound; (n - 1)/diameter, for the 120-cell).

## Submitting and checking

Format: Text file: every vertex number once, in the order of the numbering (the 120-cell).

Score: the bandwidth of the numbering (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check poly-bandwidth FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_graphs.py bandwidth 120-cell FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/poly-bandwidth.txt`.

## References

- L. H. Harper, Optimal numberings and isoperimetric problems on graphs, J. Combin. Theory 1 (1966) 385-393
- C. H. Papadimitriou, The NP-completeness of the bandwidth minimization problem, Computing 16 (1976) 263-270
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973)
- the vertex numbering of checkers/orig_phys.py (polytope_graph), shared by every polytope problem of the Originals
