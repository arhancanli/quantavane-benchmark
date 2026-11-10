# Densest admissible patterns of primes n^3 + h

`cubic-admissible` · Number theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **255** (minimize), Quantavane (Arhan Canli), 9 November 2026: an admissible 50-set with largest element 255 found by a randomized greedy sieve (tools/cubic_admissible.py sieve)

## Statement

Call a set H of positive integers admissible for n^3 + h if for every prime p there is an integer n with n^3 + h not divisible by p for all h in H; equivalently the residues -h (mod p) miss one of the values of n^3 (mod p), 0 included (all p residues when p = 3 or p = 2 mod 3, and (p+2)/3 of them when p = 1 mod 3). Only primes p <= 3|H| - 2 need checking. Let m(k) be the least m such that an admissible k-set lies in [1, m]. Determine m(k); the headline cell is k = 50: find an admissible 50-set with largest element below 255.

## Why it is interesting

Admissible patterns govern the Hardy-Littlewood and Bateman-Horn predictions for prime constellations: for linear shifts n + h the least width H(k) is the classical table behind bounded gaps between primes, and for n^2 + h the analogous least sets are the problem quad-admissible. The cubic family is the next case and mixes two behaviours: at primes p = 2 (mod 3) cubing is a bijection, so the condition is the linear one, while at primes p = 1 (mod 3) only (p+2)/3 cube classes need to be missed, so covering them is easier and admissibility harder. The values differ from both neighbours already at k = 5 (14, against 13 for n^2 + h and 13 for shifted linear tuples).

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/cubic-admissible.json`](../novelty/cubic-admissible.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:admissible AND all:"n^3" AND all:primes AND all:tuples`: 0 results
  - `all:"Bateman-Horn" AND all:cubic AND all:admissible`: 0 results
- OEIS, 2 searches:
  - `1,3,7,9,14,19,23,28,31,35,37,45,49,52,58,63`: 0 results
  - `n^3+h admissible`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no prime-pattern family.

Closest work found, and how this problem differs:
- The linear admissible tuples H(k) and our quadratic problem quad-admissible: the same question for other polynomial families.

Verdict: new. No table of least admissible shift sets for n^3 + h was found (arXiv), and the sequence m(k) is not in the OEIS.

## First values

| k | m(k) | how |
| --- | --- | --- |
| 1 | 1 | exact (exhaustive) |
| 2 | 3 | exact (exhaustive) |
| 3 | 7 | exact (exhaustive) |
| 4 | 9 | exact (exhaustive) |
| 5 | 14 | exact (exhaustive) |
| 6 | 19 | exact (exhaustive) |
| 7 | 23 | exact (exhaustive) |
| 8 | 28 | exact (exhaustive) |
| 9 | 31 | exact (exhaustive) |
| 10 | 35 | exact (exhaustive) |
| 11 | 37 | exact (exhaustive) |
| 12 | 45 | exact (exhaustive) |
| 13 | 49 | exact (exhaustive) |
| 14 | 52 | exact (exhaustive) |
| 15 | 58 | exact (exhaustive) |
| 16 | 63 | exact (exhaustive) |
| 20 | 82 | best known (ours) |
| 30 | 141 | best known (ours) |
| 40 | 189 | best known (ours) |
| 50 | 255 | best known (ours) |

Exact values by exhaustive search (tools/cubic_admissible.py exact); the sieve reproduces m(12) = 45 and m(16) = 63 and gives the upper bounds for larger k. Rows improved on 10 November 2026 show the value of the cell (see Cells).

## Best known value

255 for k = 50, held by Quantavane (Arhan Canli), 9 November 2026: the set in `refs/cubic-admissible.txt`. Lower bound m(50) >= m(16) = 63; nothing better is proved.

## Cells

The same question at each value of its parameter (k, the number of shifts): 58 cells, 14 of them exact (an exhaustive search finished) and 44 best known (ours). Each cell has its certificate in `refs/cells/cubic-admissible/` (the headline cell uses `collections/originals/refs/cubic-admissible.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example cubic-admissible-3

| cell | k | value | status |
| --- | --- | --- | --- |
| `cubic-admissible-3` | 3 | 7 | exact |
| `cubic-admissible-4` | 4 | 9 | exact |
| `cubic-admissible-5` | 5 | 14 | exact |
| `cubic-admissible-6` | 6 | 19 | exact |
| `cubic-admissible-7` | 7 | 23 | exact |
| `cubic-admissible-8` | 8 | 28 | exact |
| `cubic-admissible-9` | 9 | 31 | exact |
| `cubic-admissible-10` | 10 | 35 | exact |
| `cubic-admissible-11` | 11 | 37 | exact |
| `cubic-admissible-12` | 12 | 45 | exact |
| `cubic-admissible-13` | 13 | 49 | exact |
| `cubic-admissible-14` | 14 | 52 | exact |
| `cubic-admissible-15` | 15 | 58 | exact |
| `cubic-admissible-16` | 16 | 63 | exact |
| `cubic-admissible-17` | 17 | 68 | best known |
| `cubic-admissible-18` | 18 | 72 | best known |
| `cubic-admissible-19` | 19 | 77 | best known |
| `cubic-admissible-20` | 20 | 82 | best known |
| `cubic-admissible-21` | 21 | 86 | best known |
| `cubic-admissible-22` | 22 | 94 | best known |
| `cubic-admissible-23` | 23 | 98 | best known |
| `cubic-admissible-24` | 24 | 105 | best known |
| `cubic-admissible-25` | 25 | 112 | best known |
| `cubic-admissible-26` | 26 | 120 | best known |
| `cubic-admissible-27` | 27 | 123 | best known |
| `cubic-admissible-28` | 28 | 128 | best known |
| `cubic-admissible-29` | 29 | 134 | best known |
| `cubic-admissible-30` | 30 | 141 | best known |
| `cubic-admissible-31` | 31 | 144 | best known |
| `cubic-admissible-32` | 32 | 149 | best known |
| `cubic-admissible-33` | 33 | 154 | best known |
| `cubic-admissible-34` | 34 | 159 | best known |
| `cubic-admissible-35` | 35 | 164 | best known |
| `cubic-admissible-36` | 36 | 170 | best known |
| `cubic-admissible-37` | 37 | 177 | best known |
| `cubic-admissible-38` | 38 | 184 | best known |
| `cubic-admissible-39` | 39 | 185 | best known |
| `cubic-admissible-40` | 40 | 189 | best known |
| `cubic-admissible-41` | 41 | 192 | best known |
| `cubic-admissible-42` | 42 | 202 | best known |
| `cubic-admissible-43` | 43 | 204 | best known |
| `cubic-admissible-44` | 44 | 214 | best known |
| `cubic-admissible-45` | 45 | 214 | best known |
| `cubic-admissible-46` | 46 | 222 | best known |
| `cubic-admissible-47` | 47 | 234 | best known |
| `cubic-admissible-48` | 48 | 241 | best known |
| `cubic-admissible-49` | 49 | 246 | best known |
| `cubic-admissible-50` | 50 | 255 | best known (headline) |
| `cubic-admissible-51` | 51 | 259 | best known |
| `cubic-admissible-52` | 52 | 269 | best known |
| `cubic-admissible-53` | 53 | 271 | best known |
| `cubic-admissible-54` | 54 | 275 | best known |
| `cubic-admissible-55` | 55 | 287 | best known |
| `cubic-admissible-56` | 56 | 289 | best known |
| `cubic-admissible-57` | 57 | 300 | best known |
| `cubic-admissible-58` | 58 | 305 | best known |
| `cubic-admissible-59` | 59 | 306 | best known |
| `cubic-admissible-60` | 60 | 319 | best known |

Exact cells: exhaustive search over the sets with largest element m, m increasing (tools/cubic_admissible.py, mode exact). Best known cells: randomized greedy sieve deleting one cube class per prime, the best of 300 trials (tools/cubic_admissible.py, mode sieve); an upper bound.

Bound on the other side: 63 (lower bound; m(k) is non-decreasing and m(16) = 63 exactly).

## Submitting and checking

Format: Text file: 50 distinct positive integers h, separated by spaces or newlines.

Score: the largest element of the set (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check cubic-admissible FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_numth.py cubic-admissible 50 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/cubic-admissible.txt`.

## References

- P. T. Bateman, R. A. Horn, A heuristic asymptotic formula concerning the distribution of prime numbers, Math. Comp. 16 (1962) 363-367
- D. H. J. Polymath, Variants of the Selberg sieve, and bounded intervals containing many primes, arXiv:1407.4897
- W. Banks, K. Ford, Sets of integers satisfying Bateman-Horn statistics, arXiv:2605.01155
