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
| 40 | 190 | best known (ours) |
| 50 | 255 | best known (ours) |

Exact values by exhaustive search (tools/cubic_admissible.py exact); the sieve reproduces m(12) = 45 and m(16) = 63 and gives the upper bounds for larger k.

## Best known value

255 for k = 50, held by Quantavane (Arhan Canli), 9 November 2026: the set in `refs/cubic-admissible.txt`. Lower bound m(50) >= m(16) = 63; nothing better is proved.

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
