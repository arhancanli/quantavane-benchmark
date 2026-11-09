# Lennard-Jones clusters on the face-centred cubic lattice

`lj-fcc` · Chemistry and materials · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **-789723697/1492992** (minimize), Quantavane (Arhan Canli), 9 November 2026: simulated annealing over clusters started from the sites nearest a random centre, moving one atom at a time to a site next to the cluster, many restarts in 60 seconds (tools/src/ljfcc.c)

## Statement

Place N atoms on distinct sites of the face-centred cubic lattice: integer points (x, y, z) with x + y + z even, nearest neighbours at squared distance 2. Every pair of atoms interacts by the Lennard-Jones potential with the nearest-neighbour distance at the potential's minimum, so a pair at squared distance q contributes 64/q^6 - 16/q^3 in units of the well depth (exactly -1 for nearest neighbours), with the usual cutoff at 2.5 sigma: only pairs with q <= 8 (the first four shells) count. Energies are exact rational numbers. Which N-atom clusters have the lowest energy? The headline cell is N = 100: find a cluster of 100 atoms with energy below -789723697/1492992 = -528.953737 (ours).

## Why it is interesting

Clusters of rare-gas atoms bound by the Lennard-Jones potential are the standard test of global optimisation: the best known minima are tabulated up to 1,610 atoms (the Cambridge Cluster Database), and their structure changes with size, icosahedral for most small clusters, decahedral or face-centred cubic for some, and face-centred cubic in the bulk crystal. Lattice searches build candidates on icosahedral, decahedral or fcc lattices before relaxing them (Northby 1987; Shao, Cheng and Cai 2004). Keeping the atoms on fcc sites, with the bond length at the potential minimum and no relaxation, gives a purely combinatorial problem with exact rational energies: the most stable N-atom piece of an fcc crystal under the Lennard-Jones interaction with the standard cutoff at 2.5 sigma (four shells of neighbours). Nearest-neighbour bonds dominate (the 13-atom cuboctahedron has 36 of them), but the second, third and fourth shells reward compact shapes beyond counting bonds, and clusters with the same number of bonds are separated by those pairs. Exact minima are not known to us for any N beyond the smallest; the table gives our best clusters.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/lj-fcc.json`](../novelty/lj-fcc.json) with its address, the time it ran and its first results.

- arXiv API, 7 searches:
  - `all:"Lennard-Jones" AND all:"fcc lattice" AND all:clusters AND all:"global minimum"`: 0 results
  - `all:"lattice search" AND all:"Lennard-Jones clusters"`: 0 results
  - `all:"lattice" AND all:"Lennard-Jones clusters" AND all:restricted`: 0 results
  - `all:"Lennard-Jones" AND all:fcc AND all:cluster AND all:"lattice-based"`: 0 results
  - `all:"Lennard-Jones" AND all:"fcc" AND all:"lattice gas" AND all:cluster`: 0 results
  - `all:"discrete" AND all:"Lennard-Jones" AND all:"lattice" AND all:"global optimization"`: 1 result
  - `all:"Lennard-Jones" AND all:"face-centred cubic" AND all:clusters AND all:"magic numbers"`: 1 result
- Web search (general web search), `Lennard-Jones clusters restricted to fcc lattice sites global minimum energy N atoms lattice optimization table exact`: the Cambridge Cluster Database and basin-hopping minima (relaxed), the fcc truncated octahedron as LJ38's global minimum, Northby's icosahedral lattice search; no table of fcc-restricted minima
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no cluster or lattice-gas family in the benchmark.

Closest work found, and how this problem differs:
- The Cambridge Cluster Database and basin-hopping minima (Wales and Doye 1997): relaxed clusters in continuous space; here the atoms stay on lattice sites and energies are exact.
- Lattice searching methods (Northby 1987: icosahedral lattice; Shao, Cheng and Cai 2004 and later: fcc and decahedral lattices): use lattice clusters as starting points and relax them; the unrelaxed fcc minima are not reported as a problem of their own.

Verdict: new question: Lennard-Jones minima are tabulated for relaxed clusters, and lattices serve only to generate candidates; no one posed the minima restricted to fcc sites (2.5 sigma cutoff, exact energies) as a question of their own.

## First values

| N | lowest energy found | exact value | nearest-neighbour pairs | how |
| --- | --- | --- | --- | --- |
| 13 | -40.743391 | -20276519/497664 | 36 | best known (ours, local search) |
| 19 | -68.391657 | -68072131/995328 | 60 | best known (ours, local search) |
| 38 | -170.027468 | -42308275/248832 | 144 | best known (ours, local search) |
| 55 | -262.116137 | -130445765/497664 | 220 | best known (ours, local search) |
| 79 | -404.822674 | -201465671/497664 | 336 | best known (ours, local search) |
| 100 | -528.953737 | -789723697/1492992 | 435 | best known (ours, local search) |
| 147 | -821.002831 | -408583553/497664 | 669 | best known (ours, local search) |

Energies from the exact checker (checkers/orig_chem.py, cutoff q <= 8); clusters from tools/src/ljfcc.c, 60 s for each N. No lower bound beyond the trivial one is known to us.

## Best known value

-789723697/1492992 = -528.953736524 (435 nearest-neighbour pairs), held by Quantavane (Arhan Canli), 9 November 2026: the cluster in `refs/lj-fcc.txt`.

## Submitting and checking

Format: Text file: 100 lines 'x y z', distinct integer points with x + y + z even.

Score: the energy, an exact rational number (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check lj-fcc FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_chem.py lj-fcc 100 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/lj-fcc.txt`.

## References

- J. A. Northby, Structure and binding of Lennard-Jones clusters: 13 <= N <= 147, J. Chem. Phys. 87 (1987) 6166-6177
- D. J. Wales, J. P. K. Doye, Global optimization by basin-hopping and the lowest energy structures of Lennard-Jones clusters containing up to 110 atoms, J. Phys. Chem. A 101 (1997) 5111-5116
- X. Shao, L. Cheng, W. Cai, A dynamic lattice searching method for fast optimization of Lennard-Jones clusters, J. Comput. Chem. 25 (2004) 1693-1698
- The Cambridge Cluster Database (D. J. Wales et al.), https://www-wales.ch.cam.ac.uk/CCD.html
