# Pieces of diamond with the fewest dangling bonds

`diamond-bonds` · Chemistry and materials · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **72** (minimize), Quantavane (Arhan Canli), 9 November 2026: simulated annealing over 100-atom clusters started from the sites nearest a random centre, moving one atom at a time to an empty site next to the cluster, many restarts in 30 seconds (tools/src/diamond.c, mode anneal)

## Statement

Cut N atoms out of the diamond crystal: N distinct sites of the diamond lattice (integer points with all three coordinates even and x + y + z = 0 mod 4, or all three odd and x + y + z = 3 mod 4), connected through bonds, the pairs of sites at squared distance 3. In the crystal every atom has four bonds; the bonds to missing neighbours are dangling bonds, 4N - 2B of them when B bonds join the chosen atoms, and capping each with a hydrogen atom gives the hydrocarbon C_N H_(4N-2B) (adamantane, C10H16, for N = 10). Which N-atom pieces of diamond have the fewest dangling bonds, that is, the most bonds among N sites of the diamond lattice (its edge-isoperimetric problem)? The headline cell is N = 100: find a connected piece of 100 atoms with fewer than 72 dangling bonds (ours: C100H72, with 164 bonds).

## Why it is interesting

Diamond, silicon and germanium crystallise on the diamond lattice, each atom bonded to four neighbours at the corners of a tetrahedron. A finite piece of the crystal leaves dangling bonds on its surface; in hydrocarbons they are capped by hydrogen atoms, giving the diamondoids (adamantane C10H16, diamantane C14H20, triamantane C18H24 and the higher polymantanes found in petroleum) and hydrogen-terminated nanodiamonds, and in silicon they are the surface states of hydrogen-passivated nanocrystals. The oxygen atoms of cubic ice Ic sit on the same lattice, so the most hydrogen-bonded clusters of N water molecules cut from cubic ice are the same pieces. Counting dangling bonds turns the question into the edge-isoperimetric problem of the diamond lattice: which N vertices of this 4-regular graph span the most edges? The problem is solved exactly for the square, triangular and hexagonal lattices (Harary and Harborth 1976) and for the integer grid Z^d (Bollobas and Leader 1991; Ahlswede and Bezrukov 1995), and asymptotically for Cayley graphs on Z^d (Barber and Erde 2018), but the diamond lattice, which is not a lattice in the group sense (its two sublattices point their bonds in opposite directions), is not covered. Chemists have enumerated the diamondoids built from whole adamantane cages (Balaban and Schleyer 1978) and computed the stabilities of those with up to 41 carbon atoms, but the fewest dangling bonds over all pieces of the crystal, cages or not, has not been asked as far as our searches show. The exact values below come from an exhaustive enumeration of every connected cluster with up to 17 atoms (our counts of clusters agree with OEIS A039740); beyond that our values come from annealing.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/diamond-bonds.json`](../novelty/diamond-bonds.json) with its address, the time it ran and its first results.

- arXiv API, 7 searches:
  - `all:"diamond lattice" AND all:"edge-isoperimetric"`: 0 results
  - `all:"diamond lattice" AND all:isoperimetric`: 0 results
  - `all:"diamond lattice" AND all:clusters AND all:"dangling bonds"`: 0 results
  - `all:diamondoids AND all:enumeration`: 0 results
  - `all:"diamond lattice" AND all:"lattice animals"`: 0 results
  - `all:"silicon nanocrystals" AND all:hydrogen AND all:"magic" AND all:clusters`: 0 results
  - `all:"maximum number of bonds" AND all:lattice AND all:clusters`: 1 result
- OEIS, 6 searches:
  - `diamond lattice bonds cluster`: 1 result (A003211)
  - `diamondoid hydrogen`: 0 results
  - `diamond lattice maximal number of edges`: 6 results (A010683, A001147, A001263, A394840, A006125)
  - `0,1,2,3,4,6,7,8,10,12,13,14,16,18,19,20,22`: 0 results
  - `4,6,8,10,12,12,14,16,16,16,18,20,20,20,22,24,24`: 0 results
  - `1,2,6,22,91,398,1806,8393,39713,190625`: 0 results
- Web search (general web search), `maximum number of bonds among n atoms in the diamond lattice, cluster with fewest dangling bonds, edge-isoperimetric problem diamond lattice`: edge-isoperimetric results for Z^d (Bollobas and Leader), the triangular, square, hexagonal and cubic lattices (N^(3/4) laws for the minimisers), Barber and Erde for Cayley graphs on Z^d, and Strachan and Swanepoel, Edge isoperimetry of lattices (arXiv:2503.09591: Cayley graphs on Z^d and the triangular lattice); nothing on the diamond lattice
- Web search (general web search), `diamondoid C_nH_m fewest hydrogen atoms for a given number of carbon atoms, diamond lattice, most compact hydrocarbon fragment, nanodiamond minimum hydrogens`: the catamantane formula C(4n+6)H(4n+12) (Balaban and Rucker), an enumeration of the diamondoids CnHm with 10 to 41 carbon atoms (nomenclature, stabilities, gaps; 2018), CH and CH2 counts of truncated tetrahedral nanodiamonds (arXiv:2111.04490); no fewest-hydrogen values over all fragments of the diamond lattice
- Web search (general web search), `hydrogenated silicon nanocrystal Si_nH_m minimum number of hydrogen atoms for given n, optimal shape, diamond lattice cluster, dangling bonds, minimal surface`: structures of SinH2m clusters with n <= 21 (Nanoscale 2021) and work on amorphous and nanocrystalline silicon; no extremal dangling-bond counts
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no cluster or isoperimetric family in the benchmark.

Closest work found, and how this problem differs:
- Edge-isoperimetric problems on lattices (Harary and Harborth 1976 for the planar lattices; Bollobas and Leader 1991 and Ahlswede and Bezrukov 1995 for Z^d; Barber and Erde 2018 asymptotically for Cayley graphs on Z^d; Strachan and Swanepoel, arXiv:2503.09591): the same question on other lattices; the diamond lattice is not among them.
- Diamondoid enumerations (Balaban and Schleyer 1978; a 2018 study of the diamondoids CnHm with 10 to 41 carbons): only pieces made of whole adamantane cages, ranked by stability, not the extremal count over all pieces.
- Hydrogen-passivated silicon nanocrystals and nanodiamond shapes (closed-form CH counts for truncated tetrahedra, arXiv:2111.04490): particular shapes, not the minimum for each N.

Verdict: new question for the diamond lattice: the edge-isoperimetric problem (most bonds among N sites) is solved or studied for Z^d and the planar lattices, and diamondoids made of whole adamantane cages are enumerated, but no one has asked for the fewest dangling bonds over all N-atom pieces of the diamond lattice, as far as our searches show.

## First values

| N (atoms) | most bonds B | fewest dangling bonds 4N - 2B | hydrocarbon | how |
| --- | --- | --- | --- | --- |
| 1 | 0 | 4 | C1H4 | exact: all 2 clusters |
| 2 | 1 | 6 | C2H6 | exact: all 4 clusters |
| 3 | 2 | 8 | C3H8 | exact: all 12 clusters |
| 4 | 3 | 10 | C4H10 | exact: all 44 clusters |
| 5 | 4 | 12 | C5H12 | exact: all 182 clusters |
| 6 | 6 | 12 | C6H12 (cyclohexane) | exact: all 796 clusters |
| 7 | 7 | 14 | C7H14 | exact: all 3,612 clusters |
| 8 | 8 | 16 | C8H16 | exact: all 16,786 clusters |
| 9 | 10 | 16 | C9H16 | exact: all 79,426 clusters |
| 10 | 12 | 16 | C10H16 (adamantane) | exact: all 381,250 clusters |
| 11 | 13 | 18 | C11H18 | exact: all 1,851,832 clusters |
| 12 | 14 | 20 | C12H20 | exact: all 9,086,022 clusters |
| 13 | 16 | 20 | C13H20 | exact: all 44,970,688 clusters |
| 14 | 18 | 20 | C14H20 (diamantane) | exact: all 224,279,188 clusters |
| 15 | 19 | 22 | C15H22 | exact: all 1,126,038,472 clusters |
| 16 | 20 | 24 | C16H24 | exact: all 5,687,027,204 clusters |
| 17 | 22 | 24 | C17H24 | exact: all 28,873,452,032 clusters |
| 18 | 24 | 24 | C18H24 (as triamantane) | best known (ours, simulated annealing) |
| 20 | 26 | 28 | C20H28 | best known (ours, simulated annealing) |
| 22 | 30 | 28 | C22H28 (as tetramantane) | best known (ours, simulated annealing) |
| 26 | 37 | 30 | C26H30 | best known (ours, simulated annealing) |
| 30 | 43 | 34 | C30H34 | best known (ours, simulated annealing) |
| 35 | 52 | 36 | C35H36 | best known (ours, simulated annealing) |
| 40 | 59 | 42 | C40H42 | best known (ours, simulated annealing) |
| 50 | 76 | 48 | C50H48 | best known (ours, simulated annealing) |
| 70 | 110 | 60 | C70H60 | best known (ours, simulated annealing) |
| 100 | 164 | 72 | C100H72 | best known (ours, simulated annealing) |
| 147 | 246 | 96 | C147H96 | best known (ours, simulated annealing) |
| 200 | 341 | 118 | C200H118 | best known (ours, simulated annealing) |

Exact values: every connected cluster of the diamond lattice with N <= 17 atoms, enumerated by Redelmeier's method from an A and from a B origin (tools/src/diamond.c, mode exact; the counts are those of OEIS A039740, with the one-atom cluster counted once from each origin). Best known values: tools/src/diamond.c, mode anneal, 30 s and two seeds for each N (both seeds agree). The checker counts bonds and checks connectivity exactly.

## Best known value

72 dangling bonds (C100H72: 100 atoms, 164 bonds), held by Quantavane (Arhan Canli), 9 November 2026: the cluster in `refs/diamond-bonds.txt`.

## Cells

The same question at each value of its parameter (N, the number of atoms): 95 cells, 12 of them exact (an exhaustive search finished) and 83 best known (ours). Each cell has its certificate in `refs/cells/diamond-bonds/` (the headline cell uses `collections/originals/refs/diamond-bonds.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example diamond-bonds-6

| cell | N | value | status |
| --- | --- | --- | --- |
| `diamond-bonds-6` | 6 | 12 | exact |
| `diamond-bonds-7` | 7 | 14 | exact |
| `diamond-bonds-8` | 8 | 16 | exact |
| `diamond-bonds-9` | 9 | 16 | exact |
| `diamond-bonds-10` | 10 | 16 | exact |
| `diamond-bonds-11` | 11 | 18 | exact |
| `diamond-bonds-12` | 12 | 20 | exact |
| `diamond-bonds-13` | 13 | 20 | exact |
| `diamond-bonds-14` | 14 | 20 | exact |
| `diamond-bonds-15` | 15 | 22 | exact |
| `diamond-bonds-16` | 16 | 24 | exact |
| `diamond-bonds-17` | 17 | 24 | exact |
| `diamond-bonds-18` | 18 | 24 | best known |
| `diamond-bonds-19` | 19 | 26 | best known |
| `diamond-bonds-20` | 20 | 28 | best known |
| `diamond-bonds-21` | 21 | 28 | best known |
| `diamond-bonds-22` | 22 | 28 | best known |
| `diamond-bonds-23` | 23 | 30 | best known |
| `diamond-bonds-24` | 24 | 30 | best known |
| `diamond-bonds-25` | 25 | 30 | best known |
| `diamond-bonds-26` | 26 | 30 | best known |
| `diamond-bonds-27` | 27 | 32 | best known |
| `diamond-bonds-28` | 28 | 34 | best known |
| `diamond-bonds-29` | 29 | 34 | best known |
| `diamond-bonds-30` | 30 | 34 | best known |
| `diamond-bonds-31` | 31 | 36 | best known |
| `diamond-bonds-32` | 32 | 36 | best known |
| `diamond-bonds-33` | 33 | 36 | best known |
| `diamond-bonds-34` | 34 | 36 | best known |
| `diamond-bonds-35` | 35 | 36 | best known |
| `diamond-bonds-36` | 36 | 38 | best known |
| `diamond-bonds-37` | 37 | 40 | best known |
| `diamond-bonds-38` | 38 | 40 | best known |
| `diamond-bonds-39` | 39 | 40 | best known |
| `diamond-bonds-40` | 40 | 42 | best known |
| `diamond-bonds-41` | 41 | 42 | best known |
| `diamond-bonds-42` | 42 | 42 | best known |
| `diamond-bonds-43` | 43 | 42 | best known |
| `diamond-bonds-44` | 44 | 42 | best known |
| `diamond-bonds-45` | 45 | 44 | best known |
| `diamond-bonds-46` | 46 | 46 | best known |
| `diamond-bonds-47` | 47 | 46 | best known |
| `diamond-bonds-48` | 48 | 46 | best known |
| `diamond-bonds-49` | 49 | 48 | best known |
| `diamond-bonds-50` | 50 | 48 | best known |
| `diamond-bonds-51` | 51 | 48 | best known |
| `diamond-bonds-52` | 52 | 48 | best known |
| `diamond-bonds-53` | 53 | 48 | best known |
| `diamond-bonds-54` | 54 | 50 | best known |
| `diamond-bonds-55` | 55 | 52 | best known |
| `diamond-bonds-56` | 56 | 52 | best known |
| `diamond-bonds-57` | 57 | 52 | best known |
| `diamond-bonds-58` | 58 | 54 | best known |
| `diamond-bonds-59` | 59 | 54 | best known |
| `diamond-bonds-60` | 60 | 54 | best known |
| `diamond-bonds-61` | 61 | 54 | best known |
| `diamond-bonds-62` | 62 | 54 | best known |
| `diamond-bonds-63` | 63 | 56 | best known |
| `diamond-bonds-64` | 64 | 56 | best known |
| `diamond-bonds-65` | 65 | 56 | best known |
| `diamond-bonds-66` | 66 | 56 | best known |
| `diamond-bonds-67` | 67 | 56 | best known |
| `diamond-bonds-68` | 68 | 56 | best known |
| `diamond-bonds-69` | 69 | 58 | best known |
| `diamond-bonds-70` | 70 | 60 | best known |
| `diamond-bonds-71` | 71 | 60 | best known |
| `diamond-bonds-72` | 72 | 60 | best known |
| `diamond-bonds-73` | 73 | 62 | best known |
| `diamond-bonds-74` | 74 | 62 | best known |
| `diamond-bonds-75` | 75 | 62 | best known |
| `diamond-bonds-76` | 76 | 62 | best known |
| `diamond-bonds-77` | 77 | 62 | best known |
| `diamond-bonds-78` | 78 | 64 | best known |
| `diamond-bonds-79` | 79 | 64 | best known |
| `diamond-bonds-80` | 80 | 64 | best known |
| `diamond-bonds-81` | 81 | 64 | best known |
| `diamond-bonds-82` | 82 | 64 | best known |
| `diamond-bonds-83` | 83 | 64 | best known |
| `diamond-bonds-84` | 84 | 64 | best known |
| `diamond-bonds-85` | 85 | 66 | best known |
| `diamond-bonds-86` | 86 | 68 | best known |
| `diamond-bonds-87` | 87 | 68 | best known |
| `diamond-bonds-88` | 88 | 68 | best known |
| `diamond-bonds-89` | 89 | 70 | best known |
| `diamond-bonds-90` | 90 | 70 | best known |
| `diamond-bonds-91` | 91 | 70 | best known |
| `diamond-bonds-92` | 92 | 70 | best known |
| `diamond-bonds-93` | 93 | 70 | best known |
| `diamond-bonds-94` | 94 | 72 | best known |
| `diamond-bonds-95` | 95 | 72 | best known |
| `diamond-bonds-96` | 96 | 72 | best known |
| `diamond-bonds-97` | 97 | 72 | best known |
| `diamond-bonds-98` | 98 | 72 | best known |
| `diamond-bonds-99` | 99 | 72 | best known |
| `diamond-bonds-100` | 100 | 72 | best known (headline) |

Exact cells: the value of the enumeration of every connected cluster with at most 17 sites (Redelmeier's method, tools/src/diamond.c, mode exact); the certificate is a cluster of that value. Best known cells: simulated annealing over connected clusters (tools/src/diamond.c, mode anneal).

## Submitting and checking

Format: Text file: 100 lines 'x y z', distinct sites of the diamond lattice (all coordinates even with x + y + z = 0 mod 4, or all odd with x + y + z = 3 mod 4), connected through bonds (pairs at squared distance 3).

Score: the number of dangling bonds 4N - 2B, the number of hydrogen atoms of the hydrocarbon (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check diamond-bonds FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_chem.py diamond-bonds 100 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/diamond-bonds.txt`.

## References

- F. Harary, H. Harborth, Extremal animals, J. Combin. Inform. System Sci. 1 (1976) 1-8
- B. Bollobas, I. Leader, Edge-isoperimetric inequalities in the grid, Combinatorica 11 (1991) 299-314
- R. Ahlswede, S. L. Bezrukov, Edge isoperimetric theorems for integer point arrays, Appl. Math. Lett. 8 (1995) 75-80
- B. Barber, J. Erde, Isoperimetry in integer lattices, Discrete Analysis 2018:7
- A. T. Balaban, P. von R. Schleyer, Systematic classification and nomenclature of diamond hydrocarbons I: graph-theoretical enumeration of polymantanes, Tetrahedron 34 (1978) 3599-3609
- OEIS A039740: lattice animals in the cubic diamond lattice (the cluster counts of our enumeration)
