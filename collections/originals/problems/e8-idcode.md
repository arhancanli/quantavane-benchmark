# Identifying codes of the E8 root polytope

`e8-idcode` · Coding theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **15** (minimize), Quantavane (Arhan Canli), 9 November 2026: an identifying code of 15 roots found by simulated annealing on the number of unidentified vertices (tools/graph_sets.py, 120 s)

## Statement

Let G be the graph on the 240 roots of E8 in which two roots are adjacent when their inner product is 1 (the 1-skeleton of the Gosset polytope 4_21; 56 neighbours each). A set C of roots is an identifying code if the sets N[v] & C, where N[v] is v together with its neighbours, are nonempty and pairwise different for all 240 roots v. Determine the smallest size of an identifying code of G. Known: 9 <= minimum <= 15; find an identifying code with 14 or fewer roots, or prove a better lower bound.

## Why it is interesting

Identifying codes (Karpovsky, Chakrabarty and Levitin, IEEE Trans. Inform. Theory 1998) locate a single faulty node from the set of codewords that see it; their counting bound gives |C| >= 2n/(Delta + 2) = 480/58 for this graph, so at least 9 roots. The E8 root system is the most symmetric configuration in eight dimensions (its graph is distance-regular with spectrum 56, 28, 8, -2, -4), and its large automorphism group (the Weyl group of order 696,729,600) suggests that orbit constructions could give much smaller codes than the 15 found by local search; the gap between 9 and 15 is wide. The 600-cell version of the question is the separate problem cell600-idcode.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/e8-idcode.json`](../novelty/e8-idcode.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"identifying code" AND all:E8`: 0 results
  - `all:"identifying codes" AND all:"root system"`: 0 results
  - `all:"Gosset" AND all:"identifying"`: 37 results
- Web search (general web search), `"identifying code" OR "identifying codes" OR "locating-dominating" "600-cell" OR "120-cell" OR "regular 4-polytope" graph`: nothing on polytope or root-system graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no identifying-code family.

Closest work found, and how this problem differs:
- Identifying codes of hypercubes, grids and other standard families; none for root-system or polytope graphs.

Verdict: new. Our arXiv searches found no identifying, locating or dominating code of the E8 root graph (the Gosset polytope 4_21), and a web search on identifying codes of polytope graphs found none either.

## Best known value

15, held by Quantavane (Arhan Canli), 9 November 2026: the code in `refs/e8-idcode.txt` (simulated annealing, tools/graph_sets.py). Lower bound 9 from the counting bound 2n/(Delta + 2) = 480/58.

Bound on the other side: 9 (lower bound; counting bound |C| >= 2n/(Delta + 2) = 8.27...).

## Submitting and checking

Format: Text file: the vertex numbers (0 to 239) of the code in the checker's order: the roots doubled to integer vectors (two entries +-2 and six zeros, or eight entries +-1 with an even number of minus signs), sorted as tuples; see e8_graph in checkers/orig_codes.py.

Score: the number of roots in the code (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check e8-idcode FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_codes.py e8-idcode FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/e8-idcode.txt`.

## References

- M. G. Karpovsky, K. Chakrabarty, L. B. Levitin, On a new class of codes for identifying vertices in graphs, IEEE Trans. Inform. Theory 44 (1998) 599-611
- J. H. Conway, N. J. A. Sloane, Sphere Packings, Lattices and Groups (Springer, 3rd ed. 1999), chapter 4 (the E8 root system)
