# Ising antiferromagnet on the McLaughlin graph

`mclaughlin-ising` · Physics · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **-2968** (minimize), Quantavane (Arhan Canli), 9 November 2026: simulated annealing with single-spin flips, 20,000 sweeps and 30 restarts, then single-flip descent (tools/src/ising.c, mode anneal); runs with other seeds and lengths stop at the same energy

## Statement

Put a spin s = +1 or -1 on each of the 275 vertices of the McLaughlin graph, the unique strongly regular graph with parameters (275, 112, 30, 56), whose automorphism group is the sporadic group McL:2 (built here from the Steiner system S(4,7,23) of the binary Golay code: 22 points, 77 heptads through a fixed point, 176 heptads avoiding it). The antiferromagnetic Ising energy is E(s) = sum over the 15,400 edges uv of s_u s_v, so -E counts the edges joining opposite spins minus the others; a ground state is a maximum cut. Every edge lies in 30 triangles, so the model is heavily frustrated. The headline cell: find a configuration with energy below -2968 (ours: 9,184 of the 15,400 edges joining opposite spins). The eigenvalue bound gives E >= -3848.

## Why it is interesting

The antiferromagnetic Ising model on a graph is the maximum cut problem in physical dress, and on strongly regular graphs it is a clean test of frustration: the Hoffman-type eigenvalue bound E >= m - n(k - theta_min)/2 (m edges, n vertices, degree k, least eigenvalue theta_min) is met exactly by many famous strongly regular graphs (the Gewirtz, Higman-Sims and Gosset graphs, which we checked and set aside, and here the two subconstituents of the McLaughlin graph). The McLaughlin graph (McLaughlin 1969), with spectrum 112, 2^252, (-28)^22, is different. Its bound, a cut of 9,625 edges, is out of reach for parity reasons (an eigenvector of -28 with entries +-1 would sum to zero, impossible for 275 vertices), and our best configurations stop far below it, at 9,184 edges cut, while the 112-vertex graph of the generalised quadrangle GQ(3,9) and the 162-vertex local McLaughlin graph, which are its neighbourhood and non-neighbourhood of a vertex, both reach their bounds. Whether the ground state is the configuration we found, or how far below the bound it lies, is open. The graph has a rank-3 automorphism group of order 1,796,256,000, which a search may exploit.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/mclaughlin-ising.json`](../novelty/mclaughlin-ising.json) with its address, the time it ran and its first results.

- arXiv API, 5 searches:
  - `all:"McLaughlin graph"`: 5 results
  - `all:"McLaughlin graph" AND all:cut`: 0 results
  - `all:"strongly regular" AND all:"max-cut"`: 3 results
  - `all:"strongly regular graphs" AND all:"maximum cut"`: 0 results
  - `all:"sporadic" AND all:graph AND all:"Ising"`: 0 results
- OEIS, 2 searches:
  - `McLaughlin graph`: 2 results (A006918, A007997)
  - `maximum cut McLaughlin`: 0 results
- Web search (general web search), `McLaughlin graph maximum cut OR max-cut OR bipartite subgraph OR Ising, strongly regular graph 275 vertices`: the parameters (275, 112, 30, 56), spectrum 112, 2^252, (-28)^22, independence number 22 (Brouwer) and constructions; nothing on its maximum cut or Ising ground state
- Web search (arXiv abstract), `arXiv:1507.06254 (Max-cut and extendability of matchings in distance-regular graphs)`: a general upper bound e(1 - 1/g) on the maximum cut of a distance-regular graph of odd girth g (2/3 of the edges here, weaker than the eigenvalue bound); no values for particular graphs
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no spin-glass or max-cut family in the benchmark.

Closest work found, and how this problem differs:
- Max-cut of distance-regular graphs (Cioaba, Koolen and Li, arXiv:1507.06254): a general bound of 2/3 of the edges for odd girth 3 here, weaker than the eigenvalue bound, with no values for particular graphs.
- Eigenvalue bounds for max-cut (Mohar and Poljak 1990) and our own checks of the Gewirtz, Higman-Sims and Gosset graphs, where the bound is met (listed in dropped.json).
- Our Ising problems on the Paley graph of order 101 and on 4-dimensional polytopes: the same model on other graphs.

Verdict: new question for this graph: the maximum cut (Ising antiferromagnet) of strongly regular and distance-regular graphs is studied through general bounds, but no value or search for the McLaughlin graph was found, as far as our searches show.

## First values

| graph | vertices | edges | lowest energy found | edges cut | eigenvalue bound on E | status |
| --- | --- | --- | --- | --- | --- | --- |
| McLaughlin graph, srg(275, 112, 30, 56) | 275 | 15400 | -2968 | 9184 | -3848 | open (ours) |
| its local graph: GQ(3,9), srg(112, 30, 2, 10) | 112 | 1680 | -560 | 1120 | -560 | solved: the bound is met |
| its second subconstituent: local McLaughlin graph, srg(162, 56, 10, 24) | 162 | 4536 | -1296 | 2916 | -1296 | solved: the bound is met |

Energies from the exact checker (checkers/orig_phys.py builds the graph from the Golay code and checks the parameters); configurations from tools/src/ising.c (simulated annealing, 20,000 sweeps, 20 to 30 restarts); the graph files from tools/mclaughlin_graph.py. The bound for the McLaughlin graph is m - 2 floor(n(k - theta_min)/4 - 1/2) = 15400 - 2 x 9624, the parity argument removing one edge from n(k - theta_min)/4 = 9625.

## Best known value

-2968 (9,184 of the 15,400 edges joining opposite spins), held by Quantavane (Arhan Canli), 9 November 2026: the configuration in `refs/mclaughlin-ising.txt`.

Bound on the other side: -3848 (lower bound; the eigenvalue bound: at most n(k - theta_min)/4 = 275 x 140 / 4 = 9625 edges joining opposite spins, with equality only for a +-1 eigenvector of -28, which would sum to zero; with 275 vertices at most 9624, so E >= 15400 - 2 x 9624).

## Submitting and checking

Format: Text file: 275 spins as + and - (or 1 and -1), in the checker's vertex order (mclaughlin_graph in checkers/orig_phys.py: the points 2..23, then the 77 heptads through 1, then the 176 heptads avoiding 1, heptads sorted).

Score: the antiferromagnetic Ising energy E(s), an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check mclaughlin-ising FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_phys.py mclaughlin-ising FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/mclaughlin-ising.txt`.

## References

- J. McLaughlin, A simple group of order 898,128,000, in: Theory of Finite Groups (Brauer, Sah, eds.), Benjamin, New York, 1969, 109-111
- A. E. Brouwer, The McLaughlin graph (22 + 77 + 176 construction from S(4,7,23)), https://aeb.win.tue.nl/graphs/McL.html
- B. Mohar, S. Poljak, Eigenvalues and the max-cut problem, Czechoslovak Math. J. 40 (1990) 343-352
- S. M. Cioaba, J. H. Koolen, W. Li, Max-cut and extendability of matchings in distance-regular graphs, arXiv:1507.06254
