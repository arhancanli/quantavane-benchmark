# Identifying codes of the 600-cell

`cell600-idcode` · Coding theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **20** (minimize), Quantavane (Arhan Canli), 9 November 2026: an identifying code of 20 vertices found by simulated annealing on the number of unidentified vertices (tools/graph_sets.py)

## Statement

Let G be the graph of the 600-cell {3,3,5}: 120 vertices, each adjacent to its 12 nearest neighbours. A set C of vertices is an identifying code if the sets N[v] & C, where N[v] is v together with its neighbours, are nonempty and pairwise different for all 120 vertices v; then every vertex is recognised from the set of codewords within distance 1 of it. Determine the smallest size of an identifying code of G. Known: 18 <= minimum <= 20; find an identifying code with 19 or fewer vertices, or prove that 20 is optimal.

## Why it is interesting

Identifying codes were introduced by Karpovsky, Chakrabarty and Levitin for locating faulty processors in multiprocessor networks (IEEE Trans. Inform. Theory 44 (1998) 599-611); their counting argument gives |C| >= 2n/(Delta + 2) for a graph of maximum degree Delta, here 240/14, so |C| >= 18. Exact values are known for few families (paths, cycles, some grids and hypercubes in small dimensions), and the highly symmetric polytope graphs are natural test cases where the counting bound might be close to tight: a code meeting it would need almost every vertex to see exactly two codewords. The 600-cell's graph is locally icosahedral and vertex-transitive, so symmetric constructions (orbits of subgroups of the icosians) are an obvious place to look.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/cell600-idcode.json`](../novelty/cell600-idcode.json) with its address, the time it ran and its first results.

- arXiv API, 5 searches:
  - `all:"identifying codes" AND all:polytope`: 0 results
  - `all:"identifying code" AND all:"600-cell"`: 0 results
  - `all:"domination" AND all:"600-cell"`: 0 results
  - `all:"identifying code" AND all:"regular polytope"`: 0 results
  - `all:"identifying codes" AND all:icosahedron`: 0 results
- Web search (general web search), `"identifying code" OR "identifying codes" OR "locating-dominating" "600-cell" OR "120-cell" OR "regular 4-polytope" graph`: general identifying-code literature (grids, cubic graphs, rook's graphs, vector-space graphs); nothing on the 600-cell or other 4-polytopes
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no identifying-code family.

Closest work found, and how this problem differs:
- Identifying codes of hypercubes and grids (the standard test families); the 600-cell graph is neither.

Verdict: new. No identifying code, domination or locating result for the 600-cell (or other regular 4-polytopes) was found on arXiv, in the OEIS or by web search.

## Best known value

20, held by Quantavane (Arhan Canli), 9 November 2026: the code in `refs/cell600-idcode.txt` (simulated annealing, tools/graph_sets.py). Lower bound 18 from the counting bound 2n/(Delta + 2) = 240/14.

Bound on the other side: 18 (lower bound; Karpovsky-Chakrabarty-Levitin counting bound |C| >= 2n/(Delta + 2) = 17.14...).

## Submitting and checking

Format: Text file: the vertex numbers (0 to 119) of the code, separated by spaces or newlines, in the checker's vertex order (the 600-cell's vertices as exact coordinates in Q(sqrt 5), sorted; see cell600_graph in checkers/orig_codes.py).

Score: the number of vertices in the code (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check cell600-idcode FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_codes.py cell600-idcode FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/cell600-idcode.txt`.

## References

- M. G. Karpovsky, K. Chakrabarty, L. B. Levitin, On a new class of codes for identifying vertices in graphs, IEEE Trans. Inform. Theory 44 (1998) 599-611
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973): the 600-cell
