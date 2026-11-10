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

## Cells

The same question at each value of its parameter (N, the number of atoms): 147 cells, 0 of them exact (an exhaustive search finished) and 147 best known (ours). Each cell has its certificate in `refs/cells/lj-fcc/` (the headline cell uses `collections/originals/refs/lj-fcc.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example lj-fcc-4

| cell | N | value | status |
| --- | --- | --- | --- |
| `lj-fcc-4` | 4 | -6 | best known |
| `lj-fcc-5` | 5 | -271/32 | best known |
| `lj-fcc-6` | 6 | -813/64 | best known |
| `lj-fcc-7` | 7 | -247607/15552 | best known |
| `lj-fcc-8` | 8 | -75325/3888 | best known |
| `lj-fcc-9` | 9 | -7583471/331776 | best known |
| `lj-fcc-10` | 10 | -40602343/1492992 | best known |
| `lj-fcc-11` | 11 | -30680167/995328 | best known |
| `lj-fcc-12` | 12 | -2928559/82944 | best known |
| `lj-fcc-13` | 13 | -20276519/497664 | best known |
| `lj-fcc-14` | 14 | -67585621/1492992 | best known |
| `lj-fcc-15` | 15 | -148775953/2985984 | best known |
| `lj-fcc-16` | 16 | -18052583/331776 | best known |
| `lj-fcc-17` | 17 | -176170541/2985984 | best known |
| `lj-fcc-18` | 18 | -94980209/1492992 | best known |
| `lj-fcc-19` | 19 | -68072131/995328 | best known |
| `lj-fcc-20` | 20 | -217913687/2985984 | best known |
| `lj-fcc-21` | 21 | -57925891/746496 | best known |
| `lj-fcc-22` | 22 | -20663873/248832 | best known |
| `lj-fcc-23` | 23 | -14560997/165888 | best known |
| `lj-fcc-24` | 24 | -11633975/124416 | best known |
| `lj-fcc-25` | 25 | -293005277/2985984 | best known |
| `lj-fcc-26` | 26 | -306887737/2985984 | best known |
| `lj-fcc-27` | 27 | -107716883/995328 | best known |
| `lj-fcc-28` | 28 | -18743039/165888 | best known |
| `lj-fcc-29` | 29 | -29541013/248832 | best known |
| `lj-fcc-30` | 30 | -122905403/995328 | best known |
| `lj-fcc-31` | 31 | -21440347/165888 | best known |
| `lj-fcc-32` | 32 | -399995597/2985984 | best known |
| `lj-fcc-33` | 33 | -417812891/2985984 | best known |
| `lj-fcc-34` | 34 | -27232673/186624 | best known |
| `lj-fcc-35` | 35 | -50042333/331776 | best known |
| `lj-fcc-36` | 36 | -234012605/1492992 | best known |
| `lj-fcc-37` | 37 | -486369263/2985984 | best known |
| `lj-fcc-38` | 38 | -42308275/248832 | best known |
| `lj-fcc-39` | 39 | -8149715/46656 | best known |
| `lj-fcc-40` | 40 | -133866055/746496 | best known |
| `lj-fcc-41` | 41 | -183939905/995328 | best known |
| `lj-fcc-42` | 42 | -20968013/110592 | best known |
| `lj-fcc-43` | 43 | -194417935/995328 | best known |
| `lj-fcc-44` | 44 | -199190147/995328 | best known |
| `lj-fcc-45` | 45 | -34154471/165888 | best known |
| `lj-fcc-46` | 46 | -104849519/497664 | best known |
| `lj-fcc-47` | 47 | -323379853/1492992 | best known |
| `lj-fcc-48` | 48 | -664669583/2985984 | best known |
| `lj-fcc-49` | 49 | -75491155/331776 | best known |
| `lj-fcc-50` | 50 | -21783269/93312 | best known |
| `lj-fcc-51` | 51 | -715408661/2985984 | best known |
| `lj-fcc-52` | 52 | -122789783/497664 | best known |
| `lj-fcc-53` | 53 | -125175889/497664 | best known |
| `lj-fcc-54` | 54 | -14228851/55296 | best known |
| `lj-fcc-55` | 55 | -130445765/497664 | best known |
| `lj-fcc-56` | 56 | -400168591/1492992 | best known |
| `lj-fcc-57` | 57 | -409169821/1492992 | best known |
| `lj-fcc-58` | 58 | -15427601/55296 | best known |
| `lj-fcc-59` | 59 | -425413625/1492992 | best known |
| `lj-fcc-60` | 60 | -869171303/2985984 | best known |
| `lj-fcc-61` | 61 | -74208445/248832 | best known |
| `lj-fcc-62` | 62 | -37700749/124416 | best known |
| `lj-fcc-63` | 63 | -25614461/82944 | best known |
| `lj-fcc-64` | 64 | -104224867/331776 | best known |
| `lj-fcc-65` | 65 | -19915285/62208 | best known |
| `lj-fcc-66` | 66 | -81161345/248832 | best known |
| `lj-fcc-67` | 67 | -110225687/331776 | best known |
| `lj-fcc-68` | 68 | -84402491/248832 | best known |
| `lj-fcc-69` | 69 | -1188827/3456 | best known |
| `lj-fcc-70` | 70 | -523048919/1492992 | best known |
| `lj-fcc-71` | 71 | -1064192881/2985984 | best known |
| `lj-fcc-72` | 72 | -1078943693/2985984 | best known |
| `lj-fcc-73` | 73 | -365560163/995328 | best known |
| `lj-fcc-74` | 74 | -1115117125/2985984 | best known |
| `lj-fcc-75` | 75 | -568223581/1492992 | best known |
| `lj-fcc-76` | 76 | -21318481/55296 | best known |
| `lj-fcc-77` | 77 | -584467385/1492992 | best known |
| `lj-fcc-78` | 78 | -593685703/1492992 | best known |
| `lj-fcc-79` | 79 | -201465671/497664 | best known |
| `lj-fcc-80` | 80 | -611338243/1492992 | best known |
| `lj-fcc-81` | 81 | -1237445677/2985984 | best known |
| `lj-fcc-82` | 82 | -629387857/1492992 | best known |
| `lj-fcc-83` | 83 | -212254421/497664 | best known |
| `lj-fcc-84` | 84 | -646294399/1492992 | best known |
| `lj-fcc-85` | 85 | -1310683841/2985984 | best known |
| `lj-fcc-86` | 86 | -221853763/497664 | best known |
| `lj-fcc-87` | 87 | -24915541/55296 | best known |
| `lj-fcc-88` | 88 | -227123639/497664 | best known |
| `lj-fcc-89` | 89 | -230489687/497664 | best known |
| `lj-fcc-90` | 90 | -467011055/995328 | best known |
| `lj-fcc-91` | 91 | -1415783977/2985984 | best known |
| `lj-fcc-92` | 92 | -238977061/497664 | best known |
| `lj-fcc-93` | 93 | -727642493/1492992 | best known |
| `lj-fcc-94` | 94 | -1473380029/2985984 | best known |
| `lj-fcc-95` | 95 | -1488130841/2985984 | best known |
| `lj-fcc-96` | 96 | -753550265/1492992 | best known |
| `lj-fcc-97` | 97 | -1525195573/2985984 | best known |
| `lj-fcc-98` | 98 | -772817155/1492992 | best known |
| `lj-fcc-99` | 99 | -260064187/497664 | best known |
| `lj-fcc-100` | 100 | -789723697/1492992 | best known (headline) |
| `lj-fcc-101` | 101 | -799050559/1492992 | best known |
| `lj-fcc-102` | 102 | -1616413249/2985984 | best known |
| `lj-fcc-103` | 103 | -408735617/746496 | best known |
| `lj-fcc-104` | 104 | -17253803/31104 | best known |
| `lj-fcc-105` | 105 | -417778975/746496 | best known |
| `lj-fcc-106` | 106 | -211106587/373248 | best known |
| `lj-fcc-107` | 107 | -142274111/248832 | best known |
| `lj-fcc-108` | 108 | -108044497/186624 | best known |
| `lj-fcc-109` | 109 | -435865691/746496 | best known |
| `lj-fcc-110` | 110 | -587533169/995328 | best known |
| `lj-fcc-111` | 111 | -222903713/373248 | best known |
| `lj-fcc-112` | 112 | -1802458763/2985984 | best known |
| `lj-fcc-113` | 113 | -101165999/165888 | best known |
| `lj-fcc-114` | 114 | -921205301/1492992 | best known |
| `lj-fcc-115` | 115 | -1860939821/2985984 | best known |
| `lj-fcc-116` | 116 | -39217813/62208 | best known |
| `lj-fcc-117` | 117 | -474301459/746496 | best known |
| `lj-fcc-118` | 118 | -239367829/373248 | best known |
| `lj-fcc-119` | 119 | -161114939/248832 | best known |
| `lj-fcc-120` | 120 | -61087559/93312 | best known |
| `lj-fcc-121` | 121 | -492388175/746496 | best known |
| `lj-fcc-122` | 122 | -27601243/41472 | best known |
| `lj-fcc-123` | 123 | -501431533/746496 | best known |
| `lj-fcc-124` | 124 | -126696797/186624 | best known |
| `lj-fcc-125` | 125 | -170158297/248832 | best known |
| `lj-fcc-126` | 126 | -257454545/373248 | best known |
| `lj-fcc-127` | 127 | -259870537/373248 | best known |
| `lj-fcc-128` | 128 | -10934873/15552 | best known |
| `lj-fcc-129` | 129 | -528561607/746496 | best known |
| `lj-fcc-130` | 130 | -266497903/373248 | best known |
| `lj-fcc-131` | 131 | -9962789/13824 | best known |
| `lj-fcc-132` | 132 | -2170274555/2985984 | best known |
| `lj-fcc-133` | 133 | -364800629/497664 | best known |
| `lj-fcc-134` | 134 | -1105113197/1492992 | best known |
| `lj-fcc-135` | 135 | -370901897/497664 | best known |
| `lj-fcc-136` | 136 | -2243489771/2985984 | best known |
| `lj-fcc-137` | 137 | -377003165/497664 | best known |
| `lj-fcc-138` | 138 | -1141720805/1492992 | best known |
| `lj-fcc-139` | 139 | -1149096211/1492992 | best known |
| `lj-fcc-140` | 140 | -48405959/62208 | best known |
| `lj-fcc-141` | 141 | -1168545505/1492992 | best known |
| `lj-fcc-142` | 142 | -261813341/331776 | best known |
| `lj-fcc-143` | 143 | -296856161/373248 | best known |
| `lj-fcc-144` | 144 | -599067977/746496 | best known |
| `lj-fcc-145` | 145 | -804933709/995328 | best known |
| `lj-fcc-146` | 146 | -1218158165/1492992 | best known |
| `lj-fcc-147` | 147 | -408583553/497664 | best known |
| `lj-fcc-148` | 148 | -1234836145/1492992 | best known |
| `lj-fcc-149` | 149 | -414684821/497664 | best known |
| `lj-fcc-150` | 150 | -1254765773/1492992 | best known |

Exact cells: none. Best known cells: simulated annealing over lattice clusters with restarts (tools/src/ljfcc.c); an upper bound.

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
