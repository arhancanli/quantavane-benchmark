# 2-domination in the regular 4-polytopes

`poly-2-domination` · Combinatorics and graph theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **243** (minimize), Quantavane (Arhan Canli), 10 November 2026: 243 for the 120-cell, best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts

## Statement

A set D of vertices is 2-dominating when every vertex outside D has at least two neighbours in D; the 2-domination number gamma_2 is the smallest size of such a set. Determine gamma_2 for the graphs of the six regular convex 4-polytopes (the 5-cell K5; the tesseract, 16 vertices; the 16-cell, 8 vertices; the 24-cell, 24 vertices, 8-regular; the 600-cell, 120 vertices, 12-regular; the 120-cell, 600 vertices, 4-regular) and of the two E8 polytopes 3_21 (Gosset, 56 vertices, 27-regular) and 4_21 (the 240 roots of E8, 56-regular), each vertex adjacent to its nearest neighbours. First values (ours): the 5-cell 2 (exact); the tesseract (8-cell) 7 (exact); the 16-cell 2 (exact); the 24-cell 6 (exact); the 600-cell 18; the 120-cell 243; the Gosset polytope 3_21 4 (exact); the E8 root polytope 4_21 10. The headline cell is the 120-cell: find a certificate with value 242 or less (gamma_2 >= 2n/(d + 2) for a d-regular graph: >= 200 for the 120-cell), or prove 243 optimal.

## Why it is interesting

Multiple domination (Fink and Jacobson 1985) asks for fault tolerance: every vertex left out sees two members of the set. Counting the edges between D and the rest gives 2(n - |D|) <= d |D|, so gamma_2 >= 2n/(d + 2): 18 for the 600-cell, 200 for the 120-cell, 4 for 3_21 and 9 for 4_21. For these polytope graphs nothing was found.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/poly-2-domination.json`](../novelty/poly-2-domination.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"2-domination" AND all:polytope`: 0 results
  - `all:"double domination" AND all:"600-cell"`: 0 results
  - `all:"2-domination" AND (all:"E8" OR all:Gosset OR all:"E_8")`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `2-domination number 600-cell 120-cell graph`: first results "600-Cell 120-Cell Duality" (2007); "600-Cell 120-Cell Duality" (2007); "On $f$-domination number of a graph" (1996)
- Web search (general web search), `"Roman domination" OR "domatic number" OR "Grundy number" OR "achromatic number" 600-cell OR 120-cell OR 24-cell polytope graph`: surveys of Roman domination and the Roman domatic number, Roman domination of comets and combs; nothing on these invariants for the 4-polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no 2-domination family.

Closest work found, and how this problem differs:
- General results on 2-domination (the references) and its values for hypercubes, grids and products; none for these polytopes.
- Our polytope problems (polytope-ising, potts3-600, cell600-idcode, cell600-forest, cell120-coil, e8-idcode, e8-resolving): other invariants of the same graphs.

Verdict: new. No 2-domination result for the 600-cell, the 120-cell, the 24-cell or the E8 polytopes (searched with E8 and Gosset) was found on arXiv, in the journal literature (Crossref) or by web search; the known values for hypercubes and complete graphs cover only the small cells.

## Best known value

243 for the 120-cell, held by Quantavane (Arhan Canli), 10 November 2026: the certificate in `refs/poly-2-domination.txt` (best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts). All cells: the 5-cell 2 (exact); the tesseract (8-cell) 7 (exact); the 16-cell 2 (exact); the 24-cell 6 (exact); the 600-cell 18; the 120-cell 243; the Gosset polytope 3_21 4 (exact); the E8 root polytope 4_21 10. Bound: 200 (gamma_2 >= 2n/(d + 2) for a d-regular graph, for the 120-cell).

## Cells

The same question at each value of its parameter (KIND, the polytope): 8 cells, 5 of them exact (an exhaustive search finished) and 3 best known (ours). Each cell has its certificate in `refs/cells/poly-2-domination/` (the headline cell uses `collections/originals/refs/poly-2-domination.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example poly-2-domination-120-cell

| cell | KIND | value | status |
| --- | --- | --- | --- |
| `poly-2-domination-120-cell` | 120-cell | 243 | best known (headline) |
| `poly-2-domination-16-cell` | 16-cell | 2 | exact |
| `poly-2-domination-24-cell` | 24-cell | 6 | exact |
| `poly-2-domination-5-cell` | 5-cell | 2 | exact |
| `poly-2-domination-600-cell` | 600-cell | 18 | best known |
| `poly-2-domination-8-cell` | 8-cell | 7 | exact |
| `poly-2-domination-e8` | e8 | 10 | best known |
| `poly-2-domination-gosset` | gosset | 4 | exact |

Exact cells: proved optimal: CP-SAT (OR-Tools 9.15, one worker) closed the gap on the model of tools/polytope_sets.py, or, for zero forcing and power domination, the fort cuts (integer program over the forts found) met the best set found. Best known cells: best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts.

Bound on the other side: 200 (lower bound; gamma_2 >= 2n/(d + 2) for a d-regular graph, for the 120-cell).

## Submitting and checking

Format: Text file: the vertex numbers of the set (spaces or newlines), in the checker's vertex order (the 120-cell).

Score: the number of vertices in the set (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check poly-2-domination FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_graphs.py 2-domination 120-cell FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/poly-2-domination.txt`.

## References

- J. F. Fink, M. S. Jacobson, n-domination in graphs, in Graph Theory with Applications to Algorithms and Computer Science (Wiley 1985) 283-300
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973)
- the vertex numbering of checkers/orig_phys.py (polytope_graph), shared by every polytope problem of the Originals
