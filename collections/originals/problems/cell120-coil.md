# Coils in the 120-cell

`cell120-coil` · Coding theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **202** (maximize), Quantavane (Arhan Canli), 9 November 2026: randomised greedy growth of induced paths that prefers the step blocking the fewest free vertices, recording every closing induced cycle, many restarts (tools/src/coil.c)

## Statement

The 120-cell is the regular 4-dimensional polytope with 600 vertices; its graph is 4-regular with girth 5. Its vertices correspond to the 600 tetrahedral cells of the 600-cell, two vertices being adjacent when their cells share a triangle. A coil (coil-in-the-box) is an induced cycle: a cycle in the graph with no edge between two of its vertices other than the cycle's own edges. How long can a coil in the 120-cell be? Best known: 202 vertices (ours); every coil has at most 400.

## Why it is interesting

Snake-in-the-box codes (Kautz 1958) are long induced paths and cycles in the hypercube: read as codes, consecutive words differ in one coordinate and any two other words in at least two, so a single error is detected; exact values are known only up to dimension 8, and records in higher dimensions are still being improved (2026). The question makes sense in any graph, and the 120-cell, the four-dimensional analogue of the dodecahedron, is a natural one: sparse (degree 4), with girth 5 and a symmetry group of order 14,400. A coil there is a closed walk through its vertices in which no two walk vertices are neighbours unless consecutive. Our searches find coils through a third of the 600 vertices. Counting gives the bound 400: each coil vertex has two neighbours off the coil, and each of the other 600 - c vertices has at most four neighbours, so 2c <= 4(600 - c). The gap between our coils and 400, and the longest induced path (snake), are open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/cell120-coil.json`](../novelty/cell120-coil.json) with its address, the time it ran and its first results.

- arXiv API, 5 searches:
  - `all:"snake-in-the-box" AND all:polytope`: 0 results
  - `all:"induced path" AND all:"120-cell"`: 0 results
  - `all:"120-cell" AND all:graph AND all:code`: 0 results
  - `all:"snake-in-the-box" AND all:graph AND all:"induced cycle"`: 0 results
  - `all:"longest induced path" AND all:polytope`: 0 results
- Web search (general web search), `"snake-in-the-box" OR "coil-in-the-box" OR "longest induced cycle" OR "longest induced path" 120-cell OR "600-cell" OR "regular polytope" graph`: snake-in-the-box and coil-in-the-box in hypercubes (known values to dimension 8, 2025-2026 records, arXiv:2607.15270), induced paths in general; nothing on the 120-cell or other polytope graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no snake-in-the-box family in the benchmark.

Closest work found, and how this problem differs:
- Snake-in-the-box and coil-in-the-box in the hypercube (Kautz 1958; exhaustive values to dimension 8; records still improved in 2026): the same question in another graph.
- Snakes in Fibonacci cubes (in the OEIS; dropped by us) and our problem cell600-forest (largest induced forest of the 600-cell): other induced-subgraph questions.

Verdict: new question for this graph: snake-in-the-box and coil-in-the-box are studied for hypercubes and other cube-like graphs; nothing was found on induced cycles or paths of the 120-cell.

## First values

| quantity | best found (ours) | upper bound |
| --- | --- | --- |
| coil (induced cycle), vertices | 202 | 400 |
| snake (induced path), vertices | 214 |  |

tools/src/coil.c with 30 s and 400 s of search; the certificate lists the cells of the 600-cell.

## Best known value

202 vertices, held by Quantavane (Arhan Canli), 9 November 2026: the coil in `refs/cell120-coil.txt`. Upper bound 400 (counting edges between the coil and the rest).

Bound on the other side: 400 (upper bound; each of the c coil vertices has 2 neighbours off the coil and each of the other 600 - c vertices at most 4, so 2c <= 4(600 - c)).

## Submitting and checking

Format: Text file: one line 'a b c d' per vertex of the coil, in the order of the cycle, each vertex written as its tetrahedral cell of the 600-cell (four vertex numbers 0..119, numbered as in checkers/orig_codes.py).

Score: the number of vertices of the coil (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check cell120-coil FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_codes.py cell120-coil FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/cell120-coil.txt`.

## References

- W. H. Kautz, Unit-distance error-checking codes, IRE Trans. Electronic Computers EC-7 (1958) 179-180
- H. S. M. Coxeter, Regular Polytopes, 3rd ed., Dover (1973)
- P. R. J. Ostergard, V. H. Pettersson, Exhaustive search for snake-in-the-box codes, Graphs Combin. 31 (2015) 1019-1028
- A census of new snake-in-the-box records, arXiv:2607.15270 (2026)
