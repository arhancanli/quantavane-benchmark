# Ising antiferromagnet on the 600-cell

`polytope-ising` · Physics · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **-160** (minimize), Quantavane (Arhan Canli), 9 November 2026: a configuration with 280 frustrated edges found by simulated annealing (tools/src/ising.c; three independent seeds of 30 restarts each reach -160)

## Statement

Place an Ising spin s_v = +1 or -1 on each of the 120 vertices of the 600-cell {3,3,5} and couple nearest neighbours antiferromagnetically: E(s) = sum over the 720 edges uv of s_u s_v. Determine the ground-state energy E_0 = min E(s), equivalently the maximum cut of the 600-cell graph (E_0 = 720 - 2 maxcut). The graph is 12-regular, every vertex figure is an icosahedron and the 1200 triangles make the system frustrated. Known bounds: -222 <= E_0 <= -160; find a configuration with E(s) < -160, or prove that -160 is the ground-state energy.

## Why it is interesting

The 600-cell is the curved-space template of icosahedral order in Nelson's theory of frustration in dense liquids and metallic glasses (Order, frustration, and defects in liquids and glasses, Phys. Rev. B 28 (1983) 5515), and classical XX and Heisenberg antiferromagnets on its 120 vertices were analysed by Konstantinidis (arXiv:2207.11077). The Ising antiferromagnet on the same graph is a maximum-cut problem on a highly symmetric 12-regular graph: the triangle bound (each of the 1200 triangles has a frustrated edge, each edge lies in 5 triangles) gives at least 240 frustrated edges and the eigenvalue bound of Mohar and Poljak gives at least 249, while the best configuration we found has 280. For the 120-cell and the E8 root polytope 4_21 our configurations meet the pentagon bound and the eigenvalue bound exactly, so the 600-cell is the open case among these polytopes.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/polytope-ising.json`](../novelty/polytope-ising.json) with its address, the time it ran and its first results.

- arXiv API, 6 searches:
  - `all:"600-cell" AND all:Ising`: 1 result
  - `all:"600-cell" AND all:antiferromagnet`: 1 result
  - `all:"120-cell" AND all:Ising`: 0 results
  - `all:"max-cut" AND all:"600-cell"`: 0 results
  - `all:"Gosset" AND all:"max-cut"`: 4 results
  - `all:E8 AND all:"root system" AND all:"maximum cut"`: 0 results
- Web search (general web search), `600-cell graph maximum cut OR "Ising antiferromagnet" 600-cell ground state frustrated edges icosahedral polytope {3,3,5} Ising`: nothing on the 600-cell's maximum cut or Ising ground state
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no Ising or maximum-cut family.

Closest work found, and how this problem differs:
- Konstantinidis, arXiv:2207.11077: classical XX and Heisenberg antiferromagnets on the 600-cell in a field. Here the spins are Ising spins and the question is the exact zero-field ground-state energy (a maximum cut).

Verdict: new. No paper, table or OEIS entry was found for the Ising antiferromagnet (or maximum cut) of the 600-cell, the 120-cell or the E8 root polytope; the classical XX and Heisenberg models on the 600-cell (Konstantinidis 2022) are continuous-spin models with different ground states.

## First values

| polytope | spins | edges | E_0 | status |
| --- | --- | --- | --- | --- |
| 5-cell (K5) | 5 | 10 | -2 | exact |
| 8-cell (tesseract) | 16 | 32 | -32 | exact (bipartite) |
| 16-cell | 8 | 24 | -8 | exact |
| 24-cell | 24 | 96 | -32 | exact (all 2^23 states; 1461 ground states with s_0 = +1) |
| 120-cell | 600 | 1200 | -720 | exact: our configuration has 240 frustrated edges, the pentagon bound (720 pentagons, 3 per edge) |
| 4_21 (240 roots of E8) | 240 | 6720 | -480 | exact: our configuration meets the eigenvalue bound (smallest eigenvalue -4: max cut <= 240 * 60 / 4 = 3600) |
| 600-cell | 120 | 720 | -160 (ours) | open; lower bound -222 (smallest eigenvalue 6 - 6 phi = -3.708...: max cut <= 471) |

Graph spectra computed numerically (Jacobi rotations) and checked against the multiplicities: 600-cell 12, 9.708 (4), 6.472 (9), 3 (16), 0 (25), -2 (36), -2.472 (9), -3 (16), -3.708 (4); 4_21: 56, 28 (8), 8 (35), -2 (112), -4 (84). The checker can score the 120-cell and 4_21 too (KIND 120 or e8).

## Best known value

-160 (280 frustrated edges), held by Quantavane (Arhan Canli), 9 November 2026: the configuration in `refs/polytope-ising.txt`, found by simulated annealing (tools/src/ising.c). Lower bound -222 from the eigenvalue bound. Exact values for the 120-cell (-720) and 4_21 (-480) are attained by our configurations and proved optimal by the bounds named in the table.

Bound on the other side: -222 (lower bound; eigenvalue bound for the maximum cut, n (k - lambda_min) / 4 = 120 (12 + 3.708...) / 4 < 472).

## Submitting and checking

Format: Text file: the 120 spins as a string of + and - in the checker's vertex order (the 600-cell's vertices as exact coordinates in Q(sqrt 5), sorted; see polytope_graph in checkers/orig_phys.py), or 120 integers 1 and -1.

Score: the energy E(s) = sum over edges of s_u s_v, an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check polytope-ising FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_phys.py polytope-ising 600 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/polytope-ising.txt`.

## References

- D. R. Nelson, Order, frustration, and defects in liquids and glasses, Phys. Rev. B 28 (1983) 5515
- N. P. Konstantinidis, Classical magnetization of a four-dimensional Platonic solid, arXiv:2207.11077
- B. Mohar, S. Poljak, Eigenvalues and the max-cut problem, Czechoslovak Math. J. 40 (1990) 343-352
- H. S. M. Coxeter, Regular Polytopes (3rd ed., Dover 1973): coordinates of the 600-cell, the 120-cell and 4_21
