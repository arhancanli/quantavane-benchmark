# Ising antiferromagnet on the snub 24-cell

`snub24-ising` · Physics · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **-144** (minimize), Quantavane (Arhan Canli), 9 November 2026: a configuration with 144 frustrated edges found by simulated annealing (tools/src/ising.c; three seeds of 30 restarts each reach -144)

## Statement

The snub 24-cell (a uniform 4-polytope found by Gosset, with 96 vertices, 432 edges, 480 triangles and 9 edges at each vertex) is obtained from the 600-cell by removing the 24 vertices of an inscribed 24-cell. Put an Ising spin s_v = +1 or -1 on each vertex and couple the ends of every edge antiferromagnetically: E(s) = sum over the 432 edges uv of s_u s_v. Determine the ground-state energy min E(s) (equivalently the maximum cut of the graph). Known: -158 <= min E <= -144; find a configuration with energy below -144, or prove that -144 is optimal.

## Why it is interesting

Frustrated antiferromagnets on polyhedral clusters (the icosahedron, the dodecahedron, the icosidodecahedron and the fullerenes) are a standard testing ground for geometric frustration in magnetic molecules, and the 4-dimensional polytopes are their curved-space relatives (Nelson's icosahedral order lives on the 600-cell; see the problems polytope-ising and potts3-600). The snub 24-cell sits between the 600-cell and the 24-cell: removing an inscribed 24-cell leaves 24 icosahedral and 120 tetrahedral cells, edges lying in 3 or 4 triangles, and a spectrum (smallest eigenvalue 3.29... below zero) that bounds the maximum cut at 295. The best configuration we found has 144 frustrated edges against the eigenvalue bound of 137; the 120-cell, the E8 polytope 4_21 and the Gosset polytope 3_21 are solved exactly by their bounds, so the snub 24-cell and the 600-cell are the open cases we know.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/snub24-ising.json`](../novelty/snub24-ising.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"snub 24-cell"`: 5 results
  - `all:"snub 24-cell" AND all:antiferromagnet`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no Ising or maximum-cut family.

Closest work found, and how this problem differs:
- Papers on the snub 24-cell's construction from W(D4) and the E8 root system (arXiv:1106.3433, arXiv:0906.2109): geometry, not spin systems.

Verdict: new. The snub 24-cell appears on arXiv only in papers on its symmetry and construction (arXiv:1106.3433, 0906.2109); no spin model, maximum cut or Ising ground state on it was found.

## First values

| system | spins | edges | ground-state energy | status |
| --- | --- | --- | --- | --- |
| snub 24-cell | 96 | 432 | -144 (ours) | open; lower bound -158 (eigenvalue bound) |
| Gosset polytope 3_21 | 56 | 756 | -84 | exact: our configuration meets the eigenvalue bound (smallest eigenvalue -3) |
| 600-cell | 120 | 720 | -160 (ours) | open (problem polytope-ising) |

Spectrum of the snub 24-cell graph (numerical): 9, 7.29 (4), 4.92 (9), 3 (8), 1 (8), 0 (14), -1.20 (9), -2 (24), -2.72 (9), -3 (6), -3.29 (4). Edges: 288 in 3 triangles, 144 in 4.

## Best known value

-144 (144 frustrated edges), held by Quantavane (Arhan Canli), 9 November 2026: the configuration in `refs/snub24-ising.txt`. Lower bound -158 from the eigenvalue bound: max cut <= 96 (9 + 3.2915...) / 4 < 295.

Bound on the other side: -158 (lower bound; eigenvalue bound for the maximum cut, n (k - lambda_min) / 4 = 96 (9 + 3.2915...) / 4 < 295).

## Submitting and checking

Format: Text file: the 96 spins as a string of + and - (or 96 integers 1 and -1) in the checker's vertex order: the 600-cell's vertices with irrational coordinates, in sorted order (see polytope_graph in checkers/orig_phys.py).

Score: the energy E(s), an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check snub24-ising FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_phys.py polytope-ising snub FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/snub24-ising.txt`.

## References

- T. Gosset, On the regular and semi-regular figures in space of n dimensions, Messenger of Mathematics 29 (1900) 43-48
- H. S. M. Coxeter, Regular Polytopes (Dover, 1973)
- Snub 24-cell derived from the Coxeter-Weyl group W(D4), arXiv:1106.3433
- B. Mohar, S. Poljak, Eigenvalues and the max-cut problem, Czechoslovak Math. J. 40 (1990) 343-352
