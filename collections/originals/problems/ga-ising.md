# Ising antiferromagnet on the grand antiprism

`ga-ising` · Physics · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **-140** (minimize), Quantavane (Arhan Canli), 9 November 2026: a configuration with 180 frustrated edges found by simulated annealing (tools/src/ising.c; three seeds of 30 restarts each reach -140)

## Statement

The grand antiprism, the uniform 4-polytope found by Conway and Guy in 1965 (100 vertices, 500 edges, 10 edges at each vertex), is the 600-cell with the 20 vertices of two great decagons in orthogonal planes removed. Put an Ising spin s_v = +1 or -1 on each vertex and couple the ends of every edge antiferromagnetically: E(s) = sum over the 500 edges uv of s_u s_v. Determine the ground-state energy min E(s) (equivalently the maximum cut). Known: -166 <= min E <= -140; find a configuration with energy below -140, or prove -140 optimal.

## Why it is interesting

The grand antiprism is the one convex uniform 4-polytope that is not obtained by Wythoff's construction (Conway and Guy, 1965); its 300 tetrahedral cells and 20 pentagonal antiprisms make it a frustrated cousin of the 600-cell, from which it is cut by removing two orthogonal rings of ten vertices. Like the 600-cell (problem polytope-ising) and the snub 24-cell (snub24-ising), its Ising antiferromagnet is a maximum-cut problem on a symmetric graph with many triangles, and the eigenvalue bound (smallest eigenvalue -3.3216..., so at most 333 cut edges) is far from the best configuration we found (320 cut edges, 180 frustrated): the three polytopes test how much of the frustration the spectrum sees.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/ga-ising.json`](../novelty/ga-ising.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"grand antiprism"`: 3 results
  - `all:"grand antiprism" AND all:Ising`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no Ising or maximum-cut family.

Closest work found, and how this problem differs:
- Papers on the grand antiprism's construction (e.g. Clifford spinors and root system induction: H4 and the Grand Antiprism, arXiv:2103.07817): geometry, not spin systems.

Verdict: new. On arXiv the grand antiprism appears only in papers on its symmetry and construction; no spin model, maximum cut or Ising ground state on it was found.

## Best known value

-140 (180 frustrated edges), held by Quantavane (Arhan Canli), 9 November 2026: the configuration in `refs/ga-ising.txt`. Lower bound -166 from the eigenvalue bound: max cut <= 100 (10 + 3.3216...) / 4 < 334.

Bound on the other side: -166 (lower bound; eigenvalue bound for the maximum cut, n (k - lambda_min) / 4 = 100 (10 + 3.3216...) / 4 < 334).

## Submitting and checking

Format: Text file: the 100 spins as a string of + and - (or 100 integers 1 and -1) in the checker's vertex order (the 600-cell's vertices in sorted order without the two removed decagons; see polytope_graph in checkers/orig_phys.py).

Score: the energy E(s), an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check ga-ising FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_phys.py polytope-ising ga FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/ga-ising.txt`.

## References

- J. H. Conway, M. J. T. Guy, Four-dimensional Archimedean polytopes, Proc. Colloquium on Convexity, Copenhagen (1965) 38-39
- H. S. M. Coxeter, Regular Polytopes (Dover, 1973)
- B. Mohar, S. Poljak, Eigenvalues and the max-cut problem, Czechoslovak Math. J. 40 (1990) 343-352
