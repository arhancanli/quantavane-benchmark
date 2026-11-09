# The metric dimension of the E8 root graph

`e8-resolving` · Combinatorics and graph theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **12** (minimize), Quantavane (Arhan Canli), 9 November 2026: local search over sets of 12 vertices that replaces one vertex at a time by the one leaving the fewest pairs of vertices with equal distance vectors, with a tabu list and random restarts (tools/src/resolve.c)

## Statement

The E8 root graph has the 240 roots of E8 as vertices, two roots adjacent when their inner product is 1 (roots of norm 2); every vertex has 56 neighbours, and the graph distance between two roots is 1, 2 or 3 according as their inner product is 1, 0 or -1, or -2. A set W of vertices resolves the graph when every vertex is determined by its list of distances to the vertices of W. The metric dimension is the smallest size of a resolving set. Best known: 12 (ours); a counting argument shows that at least 11 are needed. Is the metric dimension 11 or 12?

## Why it is interesting

The metric dimension (Slater 1975; Harary and Melter 1976) is the least number of landmarks that locate every vertex by its distances; for the hypercube and Hamming graphs it is the coin-weighing and Mastermind problem, and for symmetric graphs it is tied to the base size of their automorphism groups (Bailey and Cameron 2011). Bailey (2013) computed it for small distance-regular and strongly regular graphs. The E8 root graph, the 1-skeleton of the Gosset polytope 4_21 with the symmetry group W(E8) of order 696,729,600, is neither: two vertices at distance 2 have 12 common neighbours when orthogonal and only 1 when their inner product is -1. Its distances are very uneven (from any vertex: 56 at distance 1, 182 at distance 2, 1 at distance 3), which makes resolving it expensive. A count gives at least 11 landmarks: at most k vertices outside W are opposite to a landmark, every other vertex has a distance vector in {1, 2}^k, these vectors are different, there are only C(k, j) of them with j entries equal to 1, and the landmarks have 56k neighbours in all; for k = 10 the vectors cannot be placed. Local search finds resolving sets of 12 vertices in seconds and none of 11 in ten minutes. Settling 11 or 12 is open, and the symmetry group is large enough that an exhaustive search might do it.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/e8-resolving.json`](../novelty/e8-resolving.json) with its address, the time it ran and its first results.

- arXiv API, 7 searches:
  - `all:"metric dimension" AND all:E8`: 0 results
  - `all:"metric dimension" AND all:"root system"`: 0 results
  - `all:"resolving set" AND all:polytope`: 1 result
  - `all:"metric dimension" AND all:"600-cell"`: 0 results
  - `all:"metric dimension" AND all:"Gosset"`: 0 results
  - `all:"metric dimension" AND all:"strongly regular"`: 4 results
  - `all:"metric dimension" AND all:polytope AND all:"4-dimensional"`: 0 results
- Web search (general web search), `"metric dimension" E8 root system graph OR "Gosset polytope" OR "4_21" OR "600-cell" resolving set`: general results on metric dimension (hierarchical and rooted products, infinite graphs); nothing on root-system or polytope graphs
- Web search (arXiv abstract (read)), `arXiv:2607.05152 (Bailey and Pittman, 2026)`: metric dimension of directed analogues of strongly regular graphs; no root systems or polytopes
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no metric-dimension family in the benchmark.

Closest work found, and how this problem differs:
- R. F. Bailey (2013): metric dimension of small distance-regular and strongly regular graphs; the E8 root graph is neither.
- Our problem e8-idcode: identifying codes of the same graph (vertices told apart by their closed neighbourhoods inside the code, not by distances).

Verdict: new question: the metric dimension is known for many graph families and for small distance-regular graphs; no result was found for the E8 root graph, which is not distance-regular.

## Best known value

12, held by Quantavane (Arhan Canli), 9 November 2026: the set in `refs/e8-resolving.txt`. Lower bound 11 (counting distance vectors, see above).

Bound on the other side: 11 (lower bound; counting: with k landmarks, at most k vertices outside W have a coordinate 3, the others have different vectors in {1, 2}^k, of which C(k, j) have j ones, and the total number of ones is at most 56k; for k = 10 the 220 vertices need at least 636 ones, more than 560).

## Submitting and checking

Format: Text file: the vertex numbers (0..239) of W, the roots doubled to integer vectors and sorted as in checkers/orig_comb.py (the numbering of problem e8-goodman).

Score: the size of the resolving set (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check e8-resolving FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comb.py e8-resolving FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/e8-resolving.txt`.

## References

- P. J. Slater, Leaves of trees, Congressus Numerantium 14 (1975) 549-559
- F. Harary, R. A. Melter, On the metric dimension of a graph, Ars Combin. 2 (1976) 191-195
- R. F. Bailey, P. J. Cameron, Base size, metric dimension and other invariants of groups and graphs, Bull. London Math. Soc. 43 (2011) 209-242
- R. F. Bailey, The metric dimension of small distance-regular and strongly regular graphs (arXiv:1312.4973)
- J. H. Conway, N. J. A. Sloane, Sphere Packings, Lattices and Groups, 3rd ed., Springer (1999), chapter 4 (the E8 root system)
