# Zero forcing in the regular 4-polytopes

`poly-zero-forcing` · Combinatorics and graph theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **106** (minimize), Quantavane (Arhan Canli), 10 November 2026: 106 for the 120-cell, best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts

## Statement

Colour a set Z of vertices black; whenever a black vertex has exactly one white neighbour, that neighbour turns black. Z is a zero forcing set when this turns every vertex black, and the zero forcing number Z(G) is the smallest size of a zero forcing set. Determine Z(G) for the graphs of the six regular convex 4-polytopes (the 5-cell K5; the tesseract, 16 vertices; the 16-cell, 8 vertices; the 24-cell, 24 vertices, 8-regular; the 600-cell, 120 vertices, 12-regular; the 120-cell, 600 vertices, 4-regular) and of the two E8 polytopes 3_21 (Gosset, 56 vertices, 27-regular) and 4_21 (the 240 roots of E8, 56-regular), each vertex adjacent to its nearest neighbours. First values (ours): the 5-cell 4 (exact); the tesseract (8-cell) 8 (exact); the 16-cell 6 (exact); the 24-cell 14; the 600-cell 44; the 120-cell 106; the Gosset polytope 3_21 44; the E8 root polytope 4_21 182. The headline cell is the 120-cell: find a certificate with value 105 or less (the largest multiplicity of an adjacency eigenvalue (Z >= M >= that multiplicity): >= 48 for the 120-cell), or prove 106 optimal.

## Why it is interesting

Zero forcing was introduced by the AIM Minimum Rank-Special Graphs Work Group (2008) as an upper bound for the maximum nullity M(G) of the real symmetric matrices whose off-diagonal pattern is the graph, and independently in the control of quantum systems (Burgarth and Giovannetti 2007); computing it is NP-hard. Since A - tI has the graph's pattern for every eigenvalue t of the adjacency matrix A, Z(G) >= M(G) >= the largest eigenvalue multiplicity, a strong bound for these vertex-transitive graphs with highly degenerate spectra: 36 for the 600-cell, 48 for the 120-cell, 27 for 3_21 and 112 for 4_21. For the hypercubes Z(Q_n) = M(Q_n) = 2^(n-1) (AIM 2008), so the tesseract cell is known; for the other polytopes the question is how close Z comes to the spectral bound, i.e. whether the minimum rank of these graphs is attained by their adjacency matrices.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/poly-zero-forcing.json`](../novelty/poly-zero-forcing.json) with its address, the time it ran and its first results.

- arXiv API, 5 searches:
  - `all:"zero forcing" AND all:"600-cell"`: 0 results
  - `all:"zero forcing" AND all:polytope`: 1 result
  - `all:"zero forcing" AND all:"24-cell"`: 0 results
  - `all:"zero forcing" AND all:"root system"`: 0 results
  - `all:"zero forcing" AND (all:"E8" OR all:Gosset OR all:"E_8")`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `zero forcing number regular polytope graph`: first results "Zero forcing number: Results for computation and comparison with other graph parameters"; "The zero forcing number of graph powers" (2026); "Spectral bounds for the zero forcing number of a graph" (2024)
- Web search (general web search), `"zero forcing" OR "power domination" graph of the 600-cell OR 120-cell OR 24-cell OR "regular 4-polytope"`: general papers on zero forcing and power domination (arXiv:1510.02421, graph products, iterated line digraphs, a thesis on variations); nothing on the 4-polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no zero forcing family.

Closest work found, and how this problem differs:
- General results on zero forcing (the references) and its values for hypercubes, grids and products; none for these polytopes.
- Our polytope problems (polytope-ising, potts3-600, cell600-idcode, cell600-forest, cell120-coil, e8-idcode, e8-resolving): other invariants of the same graphs.

Verdict: new. No zero forcing result for the 600-cell, the 120-cell, the 24-cell or the E8 polytopes (searched with E8 and Gosset) was found on arXiv, in the journal literature (Crossref) or by web search; the known values for hypercubes and complete graphs cover only the small cells.

## Best known value

106 for the 120-cell, held by Quantavane (Arhan Canli), 10 November 2026: the certificate in `refs/poly-zero-forcing.txt` (best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts). All cells: the 5-cell 4 (exact); the tesseract (8-cell) 8 (exact); the 16-cell 6 (exact); the 24-cell 14; the 600-cell 44; the 120-cell 106; the Gosset polytope 3_21 44; the E8 root polytope 4_21 182. Bound: 48 (the largest multiplicity of an adjacency eigenvalue (Z >= M >= that multiplicity), for the 120-cell).

## Cells

The same question at each value of its parameter (KIND, the polytope): 8 cells, 3 of them exact (an exhaustive search finished) and 5 best known (ours). Each cell has its certificate in `refs/cells/poly-zero-forcing/` (the headline cell uses `collections/originals/refs/poly-zero-forcing.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example poly-zero-forcing-120-cell

| cell | KIND | value | status |
| --- | --- | --- | --- |
| `poly-zero-forcing-120-cell` | 120-cell | 106 | best known (headline) |
| `poly-zero-forcing-16-cell` | 16-cell | 6 | exact |
| `poly-zero-forcing-24-cell` | 24-cell | 14 | best known |
| `poly-zero-forcing-5-cell` | 5-cell | 4 | exact |
| `poly-zero-forcing-600-cell` | 600-cell | 44 | best known |
| `poly-zero-forcing-8-cell` | 8-cell | 8 | exact |
| `poly-zero-forcing-e8` | e8 | 182 | best known |
| `poly-zero-forcing-gosset` | gosset | 44 | best known |

Exact cells: proved optimal: CP-SAT (OR-Tools 9.15, one worker) closed the gap on the model of tools/polytope_sets.py, or, for zero forcing and power domination, the fort cuts (integer program over the forts found) met the best set found. Best known cells: best found: CP-SAT (one worker, 5 to 60 seconds) on the model of tools/polytope_sets.py, or, for zero forcing and power domination, greedy completion and pruning between rounds of fort cuts.

Bound on the other side: 48 (lower bound; the largest multiplicity of an adjacency eigenvalue (Z >= M >= that multiplicity), for the 120-cell).

## Submitting and checking

Format: Text file: the vertex numbers of the set (spaces or newlines), in the checker's vertex order (the 120-cell).

Score: the number of vertices in the set (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check poly-zero-forcing FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_graphs.py zero-forcing 120-cell FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/poly-zero-forcing.txt`.

## References

- AIM Minimum Rank-Special Graphs Work Group, Zero forcing sets and the minimum rank of graphs, Linear Algebra Appl. 428 (2008) 1628-1648
- D. Burgarth, V. Giovannetti, Full control by locally induced relaxation, Phys. Rev. Lett. 99 (2007) 100501
- B. Brimkov, C. C. Fast, I. V. Hicks, Computational approaches for zero forcing and related problems, European J. Oper. Res. (2019)
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973)
- the vertex numbering of checkers/orig_phys.py (polytope_graph), shared by every polytope problem of the Originals
