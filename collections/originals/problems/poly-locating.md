# Locating-dominating sets of the regular 4-polytopes

`poly-locating` · Combinatorics and graph theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **205** (minimize), Quantavane (Arhan Canli), 10 November 2026: 205 for the 120-cell, best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts

## Statement

A set D of vertices is locating-dominating when every vertex outside D has a neighbour in D and no two vertices outside D have the same set of neighbours in D; the locating-domination number is the smallest size of such a set. Determine the locating-domination number for the graphs of the six regular convex 4-polytopes (the 5-cell K5; the tesseract, 16 vertices; the 16-cell, 8 vertices; the 24-cell, 24 vertices, 8-regular; the 600-cell, 120 vertices, 12-regular; the 120-cell, 600 vertices, 4-regular) and of the two E8 polytopes 3_21 (Gosset, 56 vertices, 27-regular) and 4_21 (the 240 roots of E8, 56-regular), each vertex adjacent to its nearest neighbours. First values (ours): the 5-cell 4 (exact); the tesseract (8-cell) 6 (exact); the 16-cell 4 (exact); the 24-cell 7 (exact); the 600-cell 20; the 120-cell 205; the Gosset polytope 3_21 9; the E8 root polytope 4_21 15. The headline cell is the 120-cell: find a certificate with value 204 or less (the counting bound 2n/(Delta + 3): >= 172 for the 120-cell), or prove 205 optimal.

## Why it is interesting

Locating-dominating sets were introduced by Slater (1987) to locate a faulty processor or an intruder from the detectors that see it; for a graph of maximum degree Delta the counting bound is |D| >= 2n/(Delta + 3) (Slater), here 16 for the 600-cell, 172 for the 120-cell, 4 for 3_21 and 9 for 4_21. Exact values are known for paths, cycles, some grids and hypercubes in small dimensions; these symmetric polytope graphs are natural test cases for how close the counting bound can be.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/poly-locating.json`](../novelty/poly-locating.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"locating-dominating" AND all:polytope`: 0 results
  - `all:"locating-dominating" AND all:"600-cell"`: 0 results
  - `all:"locating-dominating" AND (all:"E8" OR all:Gosset OR all:"E_8")`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `locating dominating sets polytope graphs`: first results "Polyhedra associated with locating-dominating, open locating-dominating and locating total-dominating sets in graphs" (2022); "Locating-dominating sets: From graphs to oriented graphs" (2023); "The n/2-Bound for Locating-Dominating Sets in Subcubic Graphs" (2026)
- Web search (general web search), `"locating-dominating" OR "induced matching" OR "burning number" OR "metric dimension" graph of the 600-cell OR 120-cell OR 24-cell polytope`: surveys of metric dimension and Bailey's metric dimension of small distance-regular graphs; nothing on locating-dominating sets, induced matchings or burning of the 4-polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no locating-dominating family.

Closest work found, and how this problem differs:
- General results on locating-dominating (the references) and its values for hypercubes, grids and products; none for these polytopes.
- Our polytope problems (polytope-ising, potts3-600, cell600-idcode, cell600-forest, cell120-coil, e8-idcode, e8-resolving): other invariants of the same graphs.

Verdict: new. No locating-dominating result for the 600-cell, the 120-cell, the 24-cell or the E8 polytopes (searched with E8 and Gosset) was found on arXiv, in the journal literature (Crossref) or by web search; the known values for hypercubes and complete graphs cover only the small cells.

## Best known value

205 for the 120-cell, held by Quantavane (Arhan Canli), 10 November 2026: the certificate in `refs/poly-locating.txt` (best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts). All cells: the 5-cell 4 (exact); the tesseract (8-cell) 6 (exact); the 16-cell 4 (exact); the 24-cell 7 (exact); the 600-cell 20; the 120-cell 205; the Gosset polytope 3_21 9; the E8 root polytope 4_21 15. Bound: 172 (the counting bound 2n/(Delta + 3), for the 120-cell).

## Cells

The same question at each value of its parameter (KIND, the polytope): 8 cells, 4 of them exact (an exhaustive search finished) and 4 best known (ours). Each cell has its certificate in `refs/cells/poly-locating/` (the headline cell uses `collections/originals/refs/poly-locating.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example poly-locating-120-cell

| cell | KIND | value | status |
| --- | --- | --- | --- |
| `poly-locating-120-cell` | 120-cell | 205 | best known (headline) |
| `poly-locating-16-cell` | 16-cell | 4 | exact |
| `poly-locating-24-cell` | 24-cell | 7 | exact |
| `poly-locating-5-cell` | 5-cell | 4 | exact |
| `poly-locating-600-cell` | 600-cell | 20 | best known |
| `poly-locating-8-cell` | 8-cell | 6 | exact |
| `poly-locating-e8` | e8 | 15 | best known |
| `poly-locating-gosset` | gosset | 9 | best known |

Exact cells: proved optimal: CP-SAT (OR-Tools 9.15, one worker) closed the gap on the model of tools/polytope_sets.py, or, for zero forcing and power domination, the fort cuts (integer program over the forts found) met the best set found. Best known cells: best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts.

Bound on the other side: 172 (lower bound; the counting bound 2n/(Delta + 3), for the 120-cell).

## Submitting and checking

Format: Text file: the vertex numbers of the set (spaces or newlines), in the checker's vertex order (the 120-cell).

Score: the number of vertices in the set (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check poly-locating FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_graphs.py locating-dom 120-cell FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/poly-locating.txt`.

## References

- P. J. Slater, Domination and location in acyclic graphs, Networks 17 (1987) 55-64
- P. J. Slater, Dominating and reference sets in a graph, J. Math. Phys. Sci. 22 (1988) 445-455
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973)
- the vertex numbering of checkers/orig_phys.py (polytope_graph), shared by every polytope problem of the Originals
