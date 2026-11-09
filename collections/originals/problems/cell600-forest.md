# The decycling number of the 600-cell

`cell600-forest` · Combinatorics and graph theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **37** (maximize), Quantavane (Arhan Canli), 9 November 2026: an induced forest on 37 vertices found by randomized greedy construction with exchange moves and by simulated annealing (tools/graph_sets.py, tools/forest_sa.py; both reach 37)

## Statement

A decycling set (feedback vertex set) of a graph is a set of vertices whose removal leaves a forest. Determine the decycling number of the graph of the 600-cell {3,3,5} (120 vertices, 12-regular), equivalently the largest number of its vertices that induce a forest. Known: the largest induced forest has between 37 and 60 vertices (decycling number between 60 and 83); find an induced forest with 38 or more vertices.

## Why it is interesting

The decycling number was introduced by Beineke and Vandell (Decycling graphs, J. Graph Theory 25 (1997) 59-77) and is known exactly for few families; for hypercubes only bounds and small cases are known, and for random regular graphs it is studied asymptotically (e.g. arXiv:2003.00538 for 4-regular random graphs). In the 600-cell every edge lies in 5 triangles and every vertex in 20 tetrahedral cells, so an induced forest can take at most 2 vertices of each cell (three would form a triangle); counting cells gives at most 600 x 2 / 20 = 60 forest vertices, while our searches stop at 37. The gap is large, and a symmetric construction could close much of it.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/cell600-forest.json`](../novelty/cell600-forest.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:"decycling number" AND all:polytope`: 0 results
  - `all:"feedback vertex set" AND all:"600-cell"`: 0 results
  - `all:"induced forest" AND all:polytope`: 0 results
  - `all:"decycling number" AND all:regular AND all:graphs`: 2 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no decycling family.

Closest work found, and how this problem differs:
- Decycling numbers of hypercubes, grids and random regular graphs; the 600-cell graph is none of these.

Verdict: new. No decycling, feedback-vertex-set or induced-forest result for the 600-cell (or other regular 4-polytopes) was found in our arXiv searches.

## Best known value

37 (decycling set of 83), held by Quantavane (Arhan Canli), 9 November 2026: the forest in `refs/cell600-forest.txt`. Upper bound 60: each of the 600 tetrahedral cells holds at most 2 forest vertices and each vertex lies in 20 cells.

Bound on the other side: 60 (upper bound; each tetrahedral cell holds at most 2 vertices of an induced forest; 20 cells per vertex).

## Submitting and checking

Format: Text file: the vertex numbers (0 to 119) of the forest, separated by spaces or newlines, in the checker's vertex order (see cell600_graph in checkers/orig_comb.py).

Score: the number of vertices of the induced forest (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check cell600-forest FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comb.py cell600-forest FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/cell600-forest.txt`.

## References

- L. W. Beineke, R. C. Vandell, Decycling graphs, J. Graph Theory 25 (1997) 59-77
- On the decycling number of 4-regular random graphs, arXiv:2003.00538
