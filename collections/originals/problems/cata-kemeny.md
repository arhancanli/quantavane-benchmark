# Catacondensed benzenoids with the smallest Kemeny constant

`cata-kemeny` · Chemistry and materials · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **59617087737367409/159902997431616** (minimize), Quantavane (Arhan Canli), 9 November 2026: a branched catacondensed system found by a beam search (width 80) that grows the best systems of each size by one hexagon (perimeter-only growth)

## Statement

A catacondensed benzenoid is a benzenoid system in which no carbon atom is internal: every vertex of its molecular graph lies on the perimeter (equivalently, no three hexagons share a vertex, and a system with h hexagons has 4h + 2 atoms). Unbranched ones are the hexagonal chains; branched ones contain a hexagon with three neighbouring hexagons (triphenylene is the smallest). For each h, which catacondensed benzenoid with h hexagons has the smallest Kemeny constant K = (1/(2m)) sum over vertex pairs of d_i d_j R_ij? The headline cell is h = 19: find a catacondensed benzenoid with 19 hexagons and Kemeny constant below 59617087737367409/159902997431616 = 372.8328342...

## Why it is interesting

Among hexagonal chains (unbranched catacondensed benzenoids) the extremes of Kemeny's constant are known: the linear chain maximises it and the helicene chain minimises it (Y. Yang and W. Li, MATCH 2026). Branching changes the picture. Our exhaustive computation over all catacondensed benzenoids (the counts 1, 2, 5, 12, 36, 118, 411, 1489, 5572 of OEIS A038142 for h = 2..10) shows that from h = 4 on the minimum is always attained by a branched system (triphenylene at h = 4), well below every chain (at h = 10: 137.90, against 176.39 for the best planar chain and 172.18 for the helicene, which is a planar benzenoid only up to h = 5). Which branched architectures minimise the random-walk mixing time as h grows, and whether the minimisers are the most branched systems, is open; the problem is the catacondensed counterpart of benzenoid-kemeny, where pericondensed systems are allowed and compact ones win.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/cata-kemeny.json`](../novelty/cata-kemeny.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:Kemeny AND all:catacondensed`: 0 results
  - `all:Kemeny AND all:"hexagonal chains"`: 0 results
  - `all:"degree-Kirchhoff" AND all:catacondensed`: 0 results
- OEIS, 1 searches:
  - `1,1,2,5,12,36,118,411,1489,5572`: 1 result (A038142)
- Web search (general web search), `degree-Kirchhoff index catacondensed hexagonal systems extremal minimum`: extremal catacondensed systems for degree-based indices (Rada and Gutman 2013; Rada 2017; ABC index); nothing on the degree-Kirchhoff index or Kemeny's constant over catacondensed systems
- Web search (general web search), `Kemeny's constant hexagonal chains helicene linear chain MATCH 2026`: Y. Yang and W. Li, MATCH 96 (2026) 625-646: among hexagonal chains the linear chain is the unique maximiser and the helicene the unique minimiser; Liao, Chen and Li, polygonal chains (DAM 2026); nothing on branched systems
- Web search (general web search), `"Kemeny" constant catacondensed OR "hexagonal systems" OR benzenoid branched minimum resistance random walk`: the same chain results and hexagonal ring networks (Zaman et al. 2022); nothing on branched systems
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no chemical-graph family.

Closest work found, and how this problem differs:
- Y. Yang and W. Li, Kemeny's constant of hexagonal chains (MATCH, 2026): the unbranched subclass, whose minimiser (the helicene) is beaten by branched systems from h = 4 on.
- Our problem benzenoid-kemeny: the same index over all benzenoids (pericondensed allowed).

Verdict: new as stated. Kemeny's constant is known on hexagonal chains (unbranched); no result was found on its minimum over all catacondensed benzenoids, where our computation shows branched systems win.

## First values

| h | catacondensed benzenoids | smallest Kemeny constant | minimiser | smallest among planar chains | how |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | 2157/154 = 14.006494 | unbranched | 14.006494 | exact (all) |
| 3 | 2 | 40643/1632 = 24.903799 | unbranched | 24.903799 | exact (all) |
| 4 | 5 | 50521/1386 = 36.450938 | branched | 38.384897 | exact (all) |
| 5 | 12 | 4642381/90012 = 51.575134 | branched | 54.403918 | exact (all) |
| 6 | 36 | 341945/5208 = 65.657642 | branched | 73.632526 | exact (all) |
| 7 | 118 | 354425627/4229928 = 83.789991 | branched | 95.265507 | exact (all) |
| 8 | 411 | 18090949/179826 = 100.602521 | branched | 119.275691 | exact (all) |
| 9 | 1489 | 76472594/636939 = 120.062665 | branched | 146.647331 | exact (all) |
| 10 | 5572 | 436031/3162 = 137.897217 | branched | 176.388147 | exact (all) |
| 11 |  | 353290036/2193051 = 161.095221 |  |  | best known (ours, beam search) |
| 12 |  | 736859064061/4009799010 = 183.764588 |  |  | best known (ours, beam search) |
| 13 |  | 63351576841933/303429537180 = 208.785135 |  |  | best known (ours, beam search) |
| 14 |  | 88031905628/377469015 = 233.216243 |  |  | best known (ours, beam search) |
| 15 |  | 21315415985969/82350709188 = 258.837066 |  |  | best known (ours, beam search) |
| 16 |  | 2138411927/7505190 = 284.924423 |  |  | best known (ours, beam search) |
| 17 |  | 2572810144859/8172722244 = 314.804550 |  |  | best known (ours, beam search) |
| 18 |  | 40030782928281217/117027590999592 = 342.062778 |  |  | best known (ours, beam search) |
| 19 |  | 59617087737367409/159902997431616 = 372.832834 |  |  | best known (ours, beam search) |

Exact for h <= 10 (every catacondensed benzenoid enumerated; the minimum recomputed in exact arithmetic); for h >= 11 the values are the best found by our beam search (upper bounds), which reproduces the exact value at h = 10.

## Best known value

59617087737367409/159902997431616 = 372.8328342... for h = 19, held by Quantavane (Arhan Canli), 9 November 2026: the system in `refs/cata-kemeny.txt` (78 atoms, 96 bonds). No lower bound beyond the trivial one is proved.

## Submitting and checking

Format: Text file: 19 lines 'q r', the axial coordinates of the hexagons, forming a catacondensed benzenoid.

Score: Kemeny's constant of the molecular graph, an exact rational number (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check cata-kemeny FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_chem.py cata-kemeny 19 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/cata-kemeny.txt`.

## References

- Y. Yang, W. Li, Extremal hexagonal chains with respect to the Kemeny's constant, MATCH Commun. Math. Comput. Chem. 96 (2026) 625-646 (linear chain maximal, helicene minimal among hexagonal chains; read as data)
- H. Chen, F. Zhang, Resistance distance and the normalized Laplacian spectrum, Discrete Applied Math. 155 (2007) 654-661
- OEIS A038142 (number of planar cata-polyhexes with n cells; our enumeration reproduces it)
- I. Gutman, S. J. Cyvin, Introduction to the Theory of Benzenoid Hydrocarbons (Springer, 1989)
