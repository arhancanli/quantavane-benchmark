# Fewest monochromatic triangles in the E8 root graph

`e8-goodman` · Combinatorics and graph theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **10385** (minimize), Quantavane (Arhan Canli), 9 November 2026: simulated annealing over edge colourings, each move scored by the 27 triangles through the edge (tools/mono_triangles.py, 1500 sweeps)

## Statement

Let G be the graph on the 240 roots of E8, two roots adjacent when their inner product is 1 (6720 edges, 60480 triangles; every edge lies in 27 triangles and every vertex neighbourhood is the Gosset graph). Colour each edge red or blue. What is the least possible number of monochromatic triangles? Known: 10080 <= minimum <= 10385; find a colouring with fewer than 10385 monochromatic triangles, or improve the lower bound.

## Why it is interesting

Goodman's theorem (1959) gives the exact minimum number of monochromatic triangles in a 2-colouring of the complete graph, and Ramsey multiplicity problems ask the same for other graphs; on host graphs other than complete graphs the minimum is a property of the host. The E8 root graph is the most symmetric dense graph in eight dimensions (its automorphism group is the Weyl group W(E8), of order 696,729,600). A local version of Goodman's count gives a lower bound: a triangle that is not monochromatic has exactly two vertices where its two edges differ in colour, and at a vertex v those pairs are the cut edges of a 2-colouring of the Gosset graph on N(v), whose maximum cut is exactly 420 (an eigenvalue bound that a configuration attains); so at least 60480 - 240 * 420 / 2 = 10080 triangles are monochromatic. Equality would need every neighbourhood split by a maximum cut at once; our best colouring has 10385.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/e8-goodman.json`](../novelty/e8-goodman.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"monochromatic triangles" AND all:E8`: 0 results
  - `all:Goodman AND all:"monochromatic triangles" AND all:"strongly regular"`: 0 results
  - `all:"monochromatic triangles" AND all:"root system"`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no Ramsey-multiplicity family.

Closest work found, and how this problem differs:
- Goodman's theorem and Ramsey multiplicity on complete graphs; the host graph here is the E8 root graph, and the bound and the answer differ.

Verdict: new. No study of monochromatic triangles (or Ramsey multiplicity) in edge colourings of the E8 root graph was found on arXiv; Goodman-type problems are studied for complete graphs and random or pseudo-random hosts.

## Best known value

10385, held by Quantavane (Arhan Canli), 9 November 2026: the colouring in `refs/e8-goodman.txt`. Lower bound 10080 from the local count above, using the exact maximum cut 420 of the Gosset graph (our configuration attains its eigenvalue bound 56 (27 + 3) / 4 = 420).

Bound on the other side: 10080 (lower bound; 60480 - (1/2) * 240 * 420: each vertex sees at most 420 bichromatic pairs (the maximum cut of the Gosset graph)).

## Submitting and checking

Format: Text file: 6720 digits 0 or 1, the colours of the edges in the checker's order (roots doubled to integer vectors and sorted; edges (a, b), a < b, in lexicographic order; see e8_edges in checkers/orig_comb.py).

Score: the number of monochromatic triangles (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check e8-goodman FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comb.py e8-goodman FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/e8-goodman.txt`.

## References

- A. W. Goodman, On sets of acquaintances and strangers at any party, Amer. Math. Monthly 66 (1959) 778-783
- J. H. Conway, N. J. A. Sloane, Sphere Packings, Lattices and Groups (Springer, 1999), chapter 4 (the E8 root system)
- B. Mohar, S. Poljak, Eigenvalues and the max-cut problem, Czechoslovak Math. J. 40 (1990) 343-352
