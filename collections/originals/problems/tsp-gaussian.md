# The travelling salesman tour of the Gaussian primes

`tsp-gaussian` · Computing and operations research · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **11298548** (minimize), Quantavane (Arhan Canli), 9 November 2026: nearest-neighbour start, 2-opt and Or-opt with 10-nearest-neighbour lists, then segment perturbation for 240 seconds (tools/src/tsp2opt.c)

## Statement

Take the Gaussian primes a + bi with a > 0, b >= 0 (one associate of each prime element) and norm a^2 + b^2 <= 50,000: 5,125 points, placed at (1000a, 1000b) and listed in collections/originals/instances/gaussian-primes-50000.txt. With distances the Euclidean distances rounded to the nearest integer (TSPLIB EUC_2D), find the shortest closed tour through all of them. Best known: 11,298,548 (ours); no lower bound has been computed.

## Why it is interesting

The Gaussian primes are a classical picture of arithmetic randomness in the plane (the 'Gaussian moat' question asks whether one can walk to infinity on them with bounded steps), and the travelling salesman tour through them is an exactly defined instance whose local structure comes from the distribution of primes of the form a^2 + b^2: there are no points with a + b even except 1 + i, rows and columns thin out like the primes, and the density falls slowly with the norm. Standard benchmark sets for the travelling salesman problem are random, clustered or geographic; this one is arithmetic, and how its optimal tour length compares with the Beardwood-Halton-Hammersley asymptotics for random points of the same density is open. The sunflower problem (tsp-sunflower) is its quasi-uniform counterpart.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/tsp-gaussian.json`](../novelty/tsp-gaussian.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"traveling salesman" AND all:"Gaussian primes"`: 0 results
  - `all:"travelling salesman" AND all:primes AND all:points`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark has vehicle routing instances and the Mona Lisa TSP (Prestige 100), not this point set.

Closest work found, and how this problem differs:
- TSPLIB and the DIMACS challenge instances (random, clustered and geographic point sets), and our sunflower instance; none is a set of primes.

Verdict: new. No travelling salesman instance on the Gaussian primes was found on arXiv or among the standard benchmark sets; the instance is defined here.

## Best known value

11,298,548, held by Quantavane (Arhan Canli), 9 November 2026: the tour in `refs/tsp-gaussian.txt` (tools/src/tsp2opt.c, 240 s). A quick local-search tour; Lin-Kernighan-type heuristics should improve it, and an exact solver could settle the optimum.

## Submitting and checking

Format: Text file: the point numbers 1..5125 in the order of the tour, each exactly once.

Score: the tour length in rounded Euclidean distances, an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check tsp-gaussian FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comp.py tsp collections/originals/instances/gaussian-primes-50000.txt FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/tsp-gaussian.txt`.

## References

- E. Gethner, S. Wagon, B. Wick, A stroll through the Gaussian primes, Amer. Math. Monthly 105 (1998) 327-337
- G. Reinelt, TSPLIB - a traveling salesman problem library, ORSA J. Computing 3 (1991) 376-384
- J. Beardwood, J. H. Halton, J. M. Hammersley, The shortest path through many points, Proc. Cambridge Philos. Soc. 55 (1959) 299-327
