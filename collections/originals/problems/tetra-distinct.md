# Distinct distances in the tetrahedral grid

`tetra-distinct` · Discrete geometry · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **16** (maximize), Quantavane (Arhan Canli), 9 November 2026: local search that moves one point at a time to the grid point creating the fewest repeated distances, with a tabu list (tools/src/tetradist.c, mode ls)

## Statement

The tetrahedral grid of side n is the set of the n(n + 1)(n + 2)/6 points a*e1 + b*e2 + c*e3 with integers a, b, c >= 0 and a + b + c <= n - 1, where e1, e2, e3 are unit vectors at 60 degrees to each other: a tetrahedral piece of the face-centred cubic lattice, in which the squared distance between two points is da^2 + db^2 + dc^2 + da*db + db*dc + da*dc. What is the largest set of grid points whose pairwise distances are all different? For n <= 10 the answer is n (exhaustive search). The headline cell is n = 20 (1,540 points): find more than 16 points with all distances different.

## Why it is interesting

Erdos's distinct distances problem asks how few distances n points can determine; its opposite, how many points can have all their distances different, is a Golomb-ruler question in higher dimensions. Erdos and Guy (1970) asked it for the n x n square grid, where the largest sets have order n^(2/3) up to logarithmic factors, and in the triangular grid (our problem tri-distinct) the answers stay below n. The face-centred cubic lattice is the densest lattice packing of spheres and the three-dimensional counterpart of the triangular lattice, and its tetrahedral pieces are the natural regions: the corners of a tetrahedron of side n - 1. Here the answer is exactly n for every n <= 10, by exhaustive search; beyond that our searches find fewer than n points (16 for n = 20), and whether the exact values stay at n for a while longer is open. Counting gives an upper bound: the squared distances are integers from 1 to (n - 1)^2, so k points need k(k - 1)/2 <= (n - 1)^2, which allows about 1.41n. Whether the largest sets grow like n, or like a larger multiple of n, is open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/tetra-distinct.json`](../novelty/tetra-distinct.json) with its address, the time it ran and its first results.

- arXiv API, 5 searches:
  - `all:"distinct distances" AND all:fcc`: 0 results
  - `all:"distinct distances" AND all:"three-dimensional" AND all:lattice AND all:subset`: 0 results
  - `all:"distinct distances" AND all:"cubic lattice" AND all:subset`: 0 results
  - `all:Golomb AND all:"three dimensions" AND all:distances`: 0 results
  - `all:"distinct distances" AND all:"face-centered cubic"`: 0 results
- OEIS, 4 searches:
  - `distinct distances grid 3 dimensions`: 4 results (A306385, A000217, A002061, A000931)
  - `no two pairs same distance cube`: 8 results (A000217, A000108, A007318, A000670, A001519)
  - `distinct distances tetrahedral`: 2 results (A000217, A001399)
  - `distinct distances fcc lattice`: 0 results
- Web search (general web search), `largest subset of three-dimensional lattice points with all pairwise distances distinct face-centered cubic tetrahedral grid Erdos Guy distinct distances`: Erdos and Guy (1970) for the planar grid (counting bound k <= n), distinct-distance subsets of general point sets in the plane and in higher dimensions, distinct distances of the cubic grid; nothing on the face-centred cubic lattice or tetrahedral regions
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no distinct-distance family in the benchmark.

Closest work found, and how this problem differs:
- Our problem tri-distinct: the same question in the triangular grid (two dimensions), where the answers stay below n.
- P. Erdos and R. K. Guy (1970): the n x n square grid, largest sets of order n^(2/3) up to logarithmic factors; a different lattice and dimension.

Verdict: new question for this lattice: Erdos and Guy asked it for the square grid and we for the triangular grid (tri-distinct); no result was found for the face-centred cubic lattice or its tetrahedral pieces.

## First values

| n | grid points | largest set with distinct distances | how |
| --- | --- | --- | --- |
| 1 | 1 | 1 | exact (exhaustive search) |
| 2 | 4 | 2 | exact (exhaustive search) |
| 3 | 10 | 3 | exact (exhaustive search) |
| 4 | 20 | 4 | exact (exhaustive search) |
| 5 | 35 | 5 | exact (exhaustive search) |
| 6 | 56 | 6 | exact (exhaustive search) |
| 7 | 84 | 7 | exact (exhaustive search) |
| 8 | 120 | 8 | exact (exhaustive search) |
| 9 | 165 | 9 | exact (exhaustive search) |
| 10 | 220 | 10 | exact (exhaustive search) |
| 11 | 286 | 10 | best known (ours, local search); at most 14 |
| 12 | 364 | 11 | best known (ours, local search); at most 16 |
| 13 | 455 | 11 | best known (ours, local search); at most 17 |
| 14 | 560 | 12 | best known (ours, local search); at most 18 |
| 15 | 680 | 13 | best known (ours, local search); at most 20 |
| 16 | 816 | 13 | best known (ours, local search); at most 21 |
| 18 | 1140 | 14 | best known (ours, local search); at most 24 |
| 20 | 1540 | 16 | best known (ours, local search); at most 27 |

Exact values from an exhaustive depth-first search (tools/src/tetradist.c, mode exact; n = 10 took 6 minutes). Upper bounds from counting distances. An OEIS search of 1..10 only returns the natural numbers, so the exact terms do not identify a sequence.

## Best known value

16 points, held by Quantavane (Arhan Canli), 9 November 2026: the set in `refs/tetra-distinct.txt`. Upper bound 27 (k(k - 1)/2 <= 19^2 = 361).

Bound on the other side: 27 (upper bound; the k(k - 1)/2 distances are different integers between 1 and 19^2 = 361).

## Submitting and checking

Format: Text file: one line 'a b c' per point (a, b, c >= 0, a + b + c <= 19), all points distinct.

Score: the number of points, an integer (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check tetra-distinct FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_geom.py tetra-distinct 20 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/tetra-distinct.txt`.

## References

- P. Erdos, On sets of distances of n points, Amer. Math. Monthly 53 (1946) 248-250
- P. Erdos, R. K. Guy, Distinct distances between lattice points, Elemente der Mathematik 25 (1970) 121-123
- J. H. Conway, N. J. A. Sloane, Sphere Packings, Lattices and Groups, 3rd ed., Springer (1999) (the face-centred cubic lattice A3)
- Our problem tri-distinct (distinct distances in the triangular grid)
