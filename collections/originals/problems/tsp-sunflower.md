# The travelling salesman tour of a sunflower

`tsp-sunflower` · Computing and operations research · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **17245349** (minimize), Quantavane (Arhan Canli), 9 November 2026: nearest-neighbour start, 2-opt and Or-opt with 10-nearest-neighbour lists, then 5 minutes of segment perturbation (tools/src/tsp2opt.c)

## Statement

The sunflower point set S_N consists of the points k = 1, ..., N at (round(1000 sqrt(k) cos(k a)), round(1000 sqrt(k) sin(k a))), with the golden angle a = pi (3 - sqrt 5) (Vogel's model of the florets of a sunflower head); the coordinates are fixed in collections/originals/instances/sunflower-N.txt. The distance between two points is their Euclidean distance rounded to the nearest integer (TSPLIB EUC_2D). Find the shortest closed tour through all points of S_10000. Best known: 17,245,349 (ours); no lower bound has been computed.

## Why it is interesting

Benchmark sets for the travelling salesman problem are mostly random uniform points, clustered points or real cities (TSPLIB, the DIMACS challenge, the national instances), and the best solvers (Concorde for proofs, LKH for tours) are tuned on them. The sunflower is a deterministic, quasi-uniform point set with a different geometry: points lie on families of crossing spirals (parastichies whose counts are Fibonacci numbers), the density is uniform on average but the local structure changes slowly with the radius. How the optimal tour follows these spirals, and how its length compares with the Beardwood-Halton-Hammersley asymptotics for random points (constant 12 of the optimization-constants repository), are open; the instance is defined exactly and every tour is checked in integer arithmetic.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/tsp-sunflower.json`](../novelty/tsp-sunflower.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"traveling salesman" AND all:sunflower`: 0 results
  - `all:"traveling salesman" AND all:"Fibonacci lattice"`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark has vehicle routing (CVRPLIB) instances, not the travelling salesman problem on this point set.

Closest work found, and how this problem differs:
- TSPLIB and the DIMACS TSP challenge instances (random, clustered and geographic point sets); none is a phyllotactic spiral.

Verdict: new. The sunflower (golden-angle spiral) point set does not appear among the TSP benchmark sets or in any paper found on arXiv or the web, and the instance here is defined by us.

## First values

| N | best tour length (ours) |
| --- | --- |
| 1000 | 1734027 |
| 10000 | 17245349 |

Both found with tools/src/tsp2opt.c (10 s for N = 1000, 300 s for N = 10000); upper bounds only. The N = 1000 instance is in instances/sunflower-1000.txt and can be checked with the same checker.

## Best known value

17,245,349 for N = 10000, held by Quantavane (Arhan Canli), 9 November 2026: the tour in `refs/tsp-sunflower.txt`. This is a quick local-search tour; a stronger heuristic (Lin-Kernighan type) should improve it, and an exact solver could settle the optimum.

## Submitting and checking

Format: Text file: the point numbers 1..10000 in the order of the tour, each exactly once (one per line or separated by spaces).

Score: the tour length in rounded Euclidean distances, an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check tsp-sunflower FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comp.py tsp collections/originals/instances/sunflower-10000.txt FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/tsp-sunflower.txt`.

## References

- H. Vogel, A better way to construct the sunflower head, Mathematical Biosciences 44 (1979) 179-189
- G. Reinelt, TSPLIB - a traveling salesman problem library, ORSA J. Computing 3 (1991) 376-384 (EUC_2D distances)
- D. Applegate, R. Bixby, V. Chvatal, W. Cook, The Traveling Salesman Problem: A Computational Study (Princeton, 2006)
