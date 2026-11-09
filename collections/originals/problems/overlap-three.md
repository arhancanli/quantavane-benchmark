# The minimum overlap problem for three parts

`overlap-three` · Combinatorics and graph theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **56061/200000** (minimize), Quantavane (Arhan Canli), 9 November 2026: a 60-cell step splitting found by multiplicative gradient steps on a smoothed maximum with Sinkhorn rebalancing (tools/overlap3.py), rounded to multiples of 1/600

## Statement

Split [0,3] into three parts of equal measure, allowing fractional membership: measurable f_1, f_2, f_3: [0,3] -> [0,1] with f_1 + f_2 + f_3 = 1 and the integral of each f_a equal to 1. The overlap of parts a != b at shift x is the integral of f_a(t) f_b(t - x) dt (the continuous count of differences x between part a and part b). Let mu_3 be the infimum, over all such splittings, of the largest overlap over all pairs a != b and shifts x. Determine mu_3. This is the three-part version of Erdos's minimum overlap problem (two parts of {1, ..., 2n}, constant mu = 0.380...). Known: 1/6 <= mu_3 <= 56061/200000 = 0.280305; find a splitting with a smaller largest overlap.

## Why it is interesting

Erdos's minimum overlap problem (1955) asks how evenly {1, ..., 2n} can be split into two halves so that no difference occurs too often between them; the limiting constant mu lies between White's lower bound 0.379005 (arXiv:2201.05704) and the best constructions near 0.38086, and it is constant 1b of the optimization-constants repository. With three parts every pair of parts must avoid every shift at once. Two elementary bounds frame mu_3: averaging over shifts gives at least 1/6 for each pair (the overlaps of a pair integrate to 1 over shifts in [-3, 3]), and the uniform splitting f_a = 1/3 gives 1/3; our step functions reach 0.2803, so non-uniform splittings help, but how far is open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/overlap-three.json`](../novelty/overlap-three.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"minimum overlap" AND all:partition AND all:sets`: 0 results
  - `all:"minimum overlap" AND all:"three sets"`: 0 results
  - `all:"minimum overlap" AND all:"k sets"`: 0 results
- Web search (general web search), `Erdős minimum overlap problem generalization three sets OR "k parts" OR "several sets" partition {1,...,kn} differences between parts`: only the two-part problem (MathWorld, Wikipedia, arXiv:2201.05704, arXiv:1609.08000, OEIS A393584)
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no entry; the benchmark's one-dimensional constants are 1a, 1c and 1d.

Closest work found, and how this problem differs:
- Erdos's two-part minimum overlap problem (constant mu, repository constant 1b); the three-part constant is a different quantity.

Verdict: new. No version of Erdos's minimum overlap problem with three or more parts was found (arXiv, web search); the two-part problem and its continuous form are the closest.

## First values

| cells | best largest overlap found (ours) |
| --- | --- |
| 24 | 0.28199 (float) |
| 60 | 56061/200000 = 0.280305 |
| 120 | 0.28062 (float; the optimizer did not improve on 60 cells) |

Upper bounds; the uniform splitting gives 1/3 and the averaging bound is 1/6.

## Best known value

56061/200000 = 0.280305 (60-cell splitting in `refs/overlap-three.txt`), held by Quantavane (Arhan Canli), 9 November 2026. Lower bound 1/6 by averaging the overlaps of one pair over all shifts.

Bound on the other side: 1/6 (lower bound; the overlaps of a pair integrate to 1 over shifts in [-3, 3]).

## Submitting and checking

Format: Text file: 60 lines of three integers between 0 and 600, the values of f_1, f_2, f_3 (times 600) on the 60 cells of width 1/20 of [0,3]; each line must sum to 600 and each column to 12000. Other grids and denominators can be checked with the checker's M and DEN arguments.

Score: the largest overlap of the step functions, an exact rational number (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check overlap-three FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comb.py overlap-three 60 600 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/overlap-three.txt`.

## References

- P. Erdos, Some remarks on number theory, Riveon Lematematika 9 (1955) 45-48
- J. K. Haugland, The minimum overlap problem revisited, arXiv:1609.08000
- E. P. White, Erdos' minimum overlap problem, arXiv:2201.05704
- Optimization constants in mathematics, constant 1b (github.com/teorth/optimizationproblems), read 9 November 2026
