# Charges on the roots of E8

`e8-coulomb` · Discrete geometry · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **304375/1152** (minimize), Quantavane (Arhan Canli), 9 November 2026: simulated annealing over 120-subsets of the roots, swapping a chosen root for an unchosen one, restarts for 8 seconds; two seeds and a 10-second run gave the same energy (tools/src/e8coulomb.c)

## Statement

Place N unit charges on N distinct roots of E8, the 240 shortest vectors of the E8 lattice (norm 2), and let them repel with the Coulomb potential of eight-dimensional space, 1/r^6 (the Newtonian potential r^(2-d) in dimension d = 8). Two roots are at squared distance 2, 4, 6 or 8 (inner product 1, 0, -1 or -2), so a pair costs 1/8, 1/64, 1/216 or 1/512 and every energy is an exact rational number. Which N roots have the lowest energy? This is the Thomson problem restricted to the best 240-point configuration in eight dimensions. The headline cell is N = 120, half of the roots: find 120 roots with energy below 304375/1152 = 264.214410 (ours).

## Why it is interesting

The Thomson problem asks how N equal charges arrange themselves on a sphere to minimise their Coulomb energy; it is solved for only a handful of N in three dimensions. In eight dimensions the E8 root system is the answer for N = 240: Cohn and Kumar (2007) proved it universally optimal, minimising every completely monotonic potential, the Coulomb potential 1/r^6 included. Restricting the charges to the roots themselves turns the problem for smaller N into an exact discrete one: which N-subsets of the best configuration are best? The energy depends only on how many pairs meet at 60, 90, 120 and 180 degrees, so it is a rational number, and the question becomes a weighted extremal problem on the root system. Our best subsets are structured: for N = 16 the cross-polytope (8 orthogonal pairs of opposite roots); for N = 112 and N = 128 sets with exactly the angle counts of the 112 roots of D8 and of the 128 roots (+-1/2)^8; for most even N from 16 on, centrally symmetric sets (N = 60 and N = 100 are exceptions in the table); the best N = 120 subset we found consists of 60 pairs of opposite roots. Minimum-energy subset selection is studied as an algorithmic problem for points on a line or in the plane, and the energies of the whole root systems are classical, but the subsets of the E8 roots have not been asked about as far as our searches show. No lower bound beyond the trivial one is known to us for N = 120.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/e8-coulomb.json`](../novelty/e8-coulomb.json) with its address, the time it ran and its first results.

- arXiv API, 6 searches:
  - `all:E8 AND all:"root system" AND all:subsets AND all:energy`: 0 results
  - `all:"Riesz energy" AND all:E8`: 0 results
  - `all:"discrete energy" AND all:"root system"`: 0 results
  - `all:"Thomson problem" AND all:dimensions AND all:lattice`: 0 results
  - `all:"E8 lattice" AND all:Coulomb AND all:configurations`: 0 results
  - `all:"universally optimal" AND all:subsets AND all:"E8"`: 0 results
- OEIS, 2 searches:
  - `E8 roots energy subsets`: 0 results
  - `E8 root system subsets minimal energy`: 0 results
- Web search (general web search), `minimal energy subsets of the E8 root system, N points, Coulomb Riesz energy, E8 subsets of roots, optimal configurations, discrete energy`: the complexity of minimum Riesz s-energy subset selection in Euclidean and ultrametric spaces (arXiv:2605.04715), dynamic programming for subsets of points on a line (Emmerich, arXiv:2502.01163), local optimality of D4, E8 and the Leech lattice for Riesz energies (Cohn, Kumar, Miller and others); nothing on energy-minimising subsets of the E8 roots
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark's spherical-code and kissing families ask for the largest minimum distance, not for energy.

Closest work found, and how this problem differs:
- Universal optimality of the E8 roots and lattice (Cohn and Kumar 2007; Cohn, Kumar, Miller, Radchenko and Viazovska): the whole configuration, not its subsets.
- Minimum Riesz s-energy subset selection (Emmerich, arXiv:2502.01163; complexity results, arXiv:2605.04715): algorithms for subsets of points on a line or in the plane.
- Our problems on E8 (e8-goodman, e8-idcode, e8-resolving): other questions on the same configuration.

Verdict: new question for the E8 root system: the whole configuration is universally optimal (Cohn and Kumar) and minimum-energy subset selection is studied for points on a line or in the plane, but no one has asked which N-subsets of the E8 roots minimise the Coulomb energy, as far as our searches show.

## First values

| N | lowest energy found | decimal | pairs at 60, 90, 120, 180 degrees | how |
| --- | --- | --- | --- | --- |
| 3 | 1/72 | 0.013889 | 0, 0, 3, 0 | exact (brute force over all triples through one root) |
| 8 | 151/432 | 0.349537 | 0, 20, 8, 0 | best known (ours, simulated annealing) |
| 16 | 113/64 | 1.765625 | 0, 112, 0, 8 | best known (ours); a cross-polytope: 8 orthogonal pairs of opposite roots |
| 24 | 7499/1152 | 6.509549 | 24, 216, 24, 12 | best known (ours, simulated annealing) |
| 32 | 11947/864 | 13.827546 | 64, 352, 64, 16 | best known (ours, simulated annealing) |
| 40 | 27325/1152 | 23.719618 | 120, 520, 120, 20 | best known (ours, simulated annealing) |
| 56 | 177037/3456 | 51.225984 | 280, 952, 280, 28 | best known (ours, simulated annealing) |
| 60 | 34705/576 | 60.251736 | 336, 1062, 348, 24 | best known (ours, simulated annealing) |
| 72 | 34187/384 | 89.028646 | 504, 1512, 504, 36 | best known (ours, simulated annealing) |
| 80 | 193175/1728 | 111.791088 | 640, 1840, 640, 40 | best known (ours, simulated annealing) |
| 100 | 207935/1152 | 180.499132 | 1056, 2782, 1068, 44 | best known (ours, simulated annealing) |
| 112 | 131663/576 | 228.581597 | 1344, 3472, 1344, 56 | best known (ours); the same angle counts as the 112 roots of D8 |
| 120 | 304375/1152 | 264.214410 | 1560, 3960, 1560, 60 | best known (ours, simulated annealing) |
| 126 | 4050053/13824 | 292.972584 | 1736, 4340, 1736, 63 | best known (ours, simulated annealing) |
| 128 | 65323/216 | 302.421296 | 1792, 4480, 1792, 64 | best known (ours); the same angle counts as the 128 roots (+-1/2)^8 |
| 160 | 46175/96 | 480.989583 | 2880, 6880, 2880, 80 | best known (ours, simulated annealing) |
| 200 | 2633875/3456 | 762.116609 | 4600, 10600, 4600, 100 | best known (ours, simulated annealing) |
| 240 | 637975/576 | 1107.595486 | 6720, 15120, 6720, 120 | all roots |

Energies from the exact checker (checkers/orig_geom.py); subsets from tools/src/e8coulomb.c, 8 s and two seeds for each N (the seeds agree for every N). Our tests check N = 3 by brute force and N = 240 against the counts 56, 126, 56, 1 of the root system.

## Best known value

304375/1152 = 264.214410 (1560, 3960, 1560 and 60 pairs at 60, 90, 120 and 180 degrees), held by Quantavane (Arhan Canli), 9 November 2026: the 120 roots in `refs/e8-coulomb.txt`.

## Cells

The same question at each value of its parameter (N, the number of charges, up to 120; N charges and the 240 - N on the other roots have the same minimisers, since E(240 - N) = E(240) - N c + E(N) with c the energy of one root against all others): 118 cells, 1 of them exact (an exhaustive search finished) and 117 best known (ours). Each cell has its certificate in `refs/cells/e8-coulomb/` (the headline cell uses `collections/originals/refs/e8-coulomb.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example e8-coulomb-3

| cell | N | value | status |
| --- | --- | --- | --- |
| `e8-coulomb-3` | 3 | 1/72 | exact |
| `e8-coulomb-4` | 4 | 43/864 | best known |
| `e8-coulomb-5` | 5 | 175/1728 | best known |
| `e8-coulomb-6` | 6 | 97/576 | best known |
| `e8-coulomb-7` | 7 | 217/864 | best known |
| `e8-coulomb-8` | 8 | 151/432 | best known |
| `e8-coulomb-9` | 9 | 89/192 | best known |
| `e8-coulomb-10` | 10 | 1025/1728 | best known |
| `e8-coulomb-11` | 11 | 1147/1536 | best known |
| `e8-coulomb-12` | 12 | 259/288 | best known |
| `e8-coulomb-13` | 13 | 3871/3456 | best known |
| `e8-coulomb-14` | 14 | 679/512 | best known |
| `e8-coulomb-15` | 15 | 791/512 | best known |
| `e8-coulomb-16` | 16 | 113/64 | best known |
| `e8-coulomb-17` | 17 | 4163/1728 | best known |
| `e8-coulomb-18` | 18 | 42227/13824 | best known |
| `e8-coulomb-19` | 19 | 2137/576 | best known |
| `e8-coulomb-20` | 20 | 10075/2304 | best known |
| `e8-coulomb-21` | 21 | 22561/4608 | best known |
| `e8-coulomb-22` | 22 | 75017/13824 | best known |
| `e8-coulomb-23` | 23 | 82489/13824 | best known |
| `e8-coulomb-24` | 24 | 7499/1152 | best known |
| `e8-coulomb-25` | 25 | 8611/1152 | best known |
| `e8-coulomb-26` | 26 | 12967/1536 | best known |
| `e8-coulomb-27` | 27 | 3617/384 | best known |
| `e8-coulomb-28` | 28 | 5983/576 | best known |
| `e8-coulomb-29` | 29 | 155503/13824 | best known |
| `e8-coulomb-30` | 30 | 167285/13824 | best known |
| `e8-coulomb-31` | 31 | 59735/4608 | best known |
| `e8-coulomb-32` | 32 | 11947/864 | best known |
| `e8-coulomb-33` | 33 | 1451/96 | best known |
| `e8-coulomb-34` | 34 | 226763/13824 | best known |
| `e8-coulomb-35` | 35 | 15295/864 | best known |
| `e8-coulomb-36` | 36 | 2431/128 | best known |
| `e8-coulomb-37` | 37 | 92969/4608 | best known |
| `e8-coulomb-38` | 38 | 10931/512 | best known |
| `e8-coulomb-39` | 39 | 103835/4608 | best known |
| `e8-coulomb-40` | 40 | 27325/1152 | best known |
| `e8-coulomb-41` | 41 | 87535/3456 | best known |
| `e8-coulomb-42` | 42 | 372407/13824 | best known |
| `e8-coulomb-43` | 43 | 10967/384 | best known |
| `e8-coulomb-44` | 44 | 6517/216 | best known |
| `e8-coulomb-45` | 45 | 48655/1536 | best known |
| `e8-coulomb-46` | 46 | 458573/13824 | best known |
| `e8-coulomb-47` | 47 | 479389/13824 | best known |
| `e8-coulomb-48` | 48 | 20843/576 | best known |
| `e8-coulomb-49` | 49 | 21955/576 | best known |
| `e8-coulomb-50` | 50 | 20505/512 | best known |
| `e8-coulomb-51` | 51 | 24187/576 | best known |
| `e8-coulomb-52` | 52 | 16867/384 | best known |
| `e8-coulomb-53` | 53 | 632467/13824 | best known |
| `e8-coulomb-54` | 54 | 657593/13824 | best known |
| `e8-coulomb-55` | 55 | 25291/512 | best known |
| `e8-coulomb-56` | 56 | 177037/3456 | best known |
| `e8-coulomb-57` | 57 | 61607/1152 | best known |
| `e8-coulomb-58` | 58 | 770447/13824 | best known |
| `e8-coulomb-59` | 59 | 200437/3456 | best known |
| `e8-coulomb-60` | 60 | 34705/576 | best known |
| `e8-coulomb-61` | 61 | 31949/512 | best known |
| `e8-coulomb-62` | 62 | 99133/1536 | best known |
| `e8-coulomb-63` | 63 | 307303/4608 | best known |
| `e8-coulomb-64` | 64 | 9913/144 | best known |
| `e8-coulomb-65` | 65 | 30851/432 | best known |
| `e8-coulomb-66` | 66 | 1022843/13824 | best known |
| `e8-coulomb-67` | 67 | 11027/144 | best known |
| `e8-coulomb-68` | 68 | 273553/3456 | best known |
| `e8-coulomb-69` | 69 | 376121/4608 | best known |
| `e8-coulomb-70` | 70 | 1162385/13824 | best known |
| `e8-coulomb-71` | 71 | 1196545/13824 | best known |
| `e8-coulomb-72` | 72 | 34187/384 | best known |
| `e8-coulomb-73` | 73 | 35299/384 | best known |
| `e8-coulomb-74` | 74 | 48549/512 | best known |
| `e8-coulomb-75` | 75 | 112585/1152 | best known |
| `e8-coulomb-76` | 76 | 28981/288 | best known |
| `e8-coulomb-77` | 77 | 1429687/13824 | best known |
| `e8-coulomb-78` | 78 | 1468157/13824 | best known |
| `e8-coulomb-79` | 79 | 502255/4608 | best known |
| `e8-coulomb-80` | 80 | 193175/1728 | best known |
| `e8-coulomb-81` | 81 | 66245/576 | best known |
| `e8-coulomb-82` | 82 | 1634387/13824 | best known |
| `e8-coulomb-83` | 83 | 209879/1728 | best known |
| `e8-coulomb-84` | 84 | 143629/1152 | best known |
| `e8-coulomb-85` | 85 | 588865/4608 | best known |
| `e8-coulomb-86` | 86 | 67019/512 | best known |
| `e8-coulomb-87` | 87 | 205841/1536 | best known |
| `e8-coulomb-88` | 88 | 52657/384 | best known |
| `e8-coulomb-89` | 89 | 486145/3456 | best known |
| `e8-coulomb-90` | 90 | 1993535/13824 | best known |
| `e8-coulomb-91` | 91 | 170219/1152 | best known |
| `e8-coulomb-92` | 92 | 261449/1728 | best known |
| `e8-coulomb-93` | 93 | 713029/4608 | best known |
| `e8-coulomb-94` | 94 | 2186453/13824 | best known |
| `e8-coulomb-95` | 95 | 2233957/13824 | best known |
| `e8-coulomb-96` | 96 | 47531/288 | best known |
| `e8-coulomb-97` | 97 | 48643/288 | best known |
| `e8-coulomb-98` | 98 | 265363/1536 | best known |
| `e8-coulomb-99` | 99 | 16957/96 | best known |
| `e8-coulomb-100` | 100 | 207935/1152 | best known |
| `e8-coulomb-101` | 101 | 2547163/13824 | best known |
| `e8-coulomb-102` | 102 | 2598977/13824 | best known |
| `e8-coulomb-103` | 103 | 883643/4608 | best known |
| `e8-coulomb-104` | 104 | 675727/3456 | best known |
| `e8-coulomb-105` | 105 | 76687/384 | best known |
| `e8-coulomb-106` | 106 | 2818583/13824 | best known |
| `e8-coulomb-107` | 107 | 719143/3456 | best known |
| `e8-coulomb-108` | 108 | 10189/48 | best known |
| `e8-coulomb-109` | 109 | 996941/4608 | best known |
| `e8-coulomb-110` | 110 | 112855/512 | best known |
| `e8-coulomb-111` | 111 | 1034495/4608 | best known |
| `e8-coulomb-112` | 112 | 131663/576 | best known |
| `e8-coulomb-113` | 113 | 402773/1728 | best known |
| `e8-coulomb-114` | 114 | 3284483/13824 | best known |
| `e8-coulomb-115` | 115 | 15495/64 | best known |
| `e8-coulomb-116` | 116 | 852307/3456 | best known |
| `e8-coulomb-117` | 117 | 128521/512 | best known |
| `e8-coulomb-118` | 118 | 3530777/13824 | best known |
| `e8-coulomb-119` | 119 | 3591625/13824 | best known |
| `e8-coulomb-120` | 120 | 304375/1152 | best known (headline) |

Exact cells: brute force over the pairs of roots added to a fixed root (the Weyl group is transitive on roots). Best known cells: simulated annealing over N-subsets with restarts (tools/src/e8coulomb.c); an upper bound.

## Submitting and checking

Format: Text file: 120 lines of 8 integers, distinct roots of E8 written doubled: a permutation of (+-2, +-2, 0, 0, 0, 0, 0, 0), or eight entries +-1 with an even number of minus signs.

Score: the Coulomb energy, an exact rational number (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check e8-coulomb FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_geom.py e8-coulomb 120 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/e8-coulomb.txt`.

## References

- J. J. Thomson, On the structure of the atom, Philos. Mag. (6) 7 (1904) 237-265
- H. Cohn, A. Kumar, Universally optimal distribution of points on spheres, J. Amer. Math. Soc. 20 (2007) 99-148
- J. H. Conway, N. J. A. Sloane, Sphere Packings, Lattices and Groups, 3rd ed., Springer, 1999 (the E8 root system)
- M. Emmerich, Minimum Riesz s-energy subset selection in ordered point sets via dynamic programming, arXiv:2502.01163
