# Densest admissible patterns of primes n^2 + h

`quad-admissible` · Number theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **247** (minimize), Quantavane (Arhan Canli), 9 November 2026: an admissible 50-set with largest element 247 found by a randomized greedy sieve (tools/quad_sieve.py: for each prime p <= 99 delete the h whose -h falls in the least used square class)

## Statement

Call a set H of positive integers admissible for n^2 + h if for every prime p there is an integer n with n^2 + h not divisible by p for all h in H; equivalently, the residues -h (mod p) miss at least one of the (p+1)/2 values of n^2 (mod p), 0 included. Only primes p <= 2|H| - 1 need checking. Admissibility is necessary for n^2 + h to be prime for all h in H at once for infinitely many n, and by the Bateman-Horn conjecture it is sufficient. Let m(k) be the least m such that some admissible k-set lies in [1, m]. Determine m(k); the headline cell is k = 50: find an admissible 50-set with largest element below 247.

## Why it is interesting

For linear shifts n + h, the least width of an admissible k-tuple, H(k), is the classical quantity behind bounded gaps between primes (Engelsma's and Sutherland's tables; Polymath8b). Quadratic families are the next case of the Bateman-Horn conjecture: whether n^2 + 1 is prime infinitely often is one of Landau's problems, and Hardy and Littlewood's Conjecture F gives the predicted density. The dense patterns here are the quadratic analogue of prime k-tuples: {1, 3, 7, 9} gives 5, 7, 11, 13 at n = 2, and the question is how tightly k such polynomials can be packed without a fixed prime divisor. Admissibility for n^2 + h is a covering condition on the square classes modulo each prime (a class is blocked by every h with -h in it), so it differs from the linear case already at p = 3, where only the classes 0 and 1 need covering.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/quad-admissible.json`](../novelty/quad-admissible.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:admissible AND all:"n^2+1" AND all:tuples`: 0 results
  - `all:"Bateman-Horn" AND all:admissible AND all:quadratic AND all:"k-tuples"`: 0 results
  - `all:"prime constellations" AND all:quadratic AND all:polynomials`: 0 results
- OEIS, 2 searches:
  - `1,3,7,9,13,20,22,27,31,34,38,44,50,52`: 0 results
  - `n^2+h admissible`: 0 results
- Web search (general web search), `admissible set of shifts for n^2 + h prime constellations quadratic "n^2+1" "n^2+3" "n^2+7" "n^2+9" all prime densest patterns Bateman-Horn`: admissibility definitions for polynomial tuples (arXiv:2605.01155) and densest linear patterns (arXiv:1901.03785); nothing on least shift sets for n^2 + h
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no prime-pattern family.

Closest work found, and how this problem differs:
- Linear admissible k-tuples and their least width H(k) (Engelsma, Sutherland, Polymath8b; Kourbatov and Wolf on densest patterns, arXiv:1901.03785): the linear case of this problem.

Verdict: new. No table or study of least admissible shift sets for the family n^2 + h was found (arXiv, web search); the sequence m(k) is not in the OEIS. Densest admissible tuples are studied only for linear shifts.

## First values

| k | m(k) | how |
| --- | --- | --- |
| 1 | 1 | exact (exhaustive) |
| 2 | 3 | exact (exhaustive) |
| 3 | 7 | exact (exhaustive) |
| 4 | 9 | exact (exhaustive) |
| 5 | 13 | exact (exhaustive) |
| 6 | 20 | exact (exhaustive) |
| 7 | 22 | exact (exhaustive) |
| 8 | 27 | exact (exhaustive) |
| 9 | 31 | exact (exhaustive) |
| 10 | 34 | exact (exhaustive) |
| 11 | 38 | exact (exhaustive) |
| 12 | 44 | exact (exhaustive) |
| 13 | 50 | exact (exhaustive) |
| 14 | 52 | exact (exhaustive) |
| 15 | 57 | exact (exhaustive) |
| 16 | 63 | exact (exhaustive) |
| 17 | 67 | exact (exhaustive) |
| 18 | 73 | exact (exhaustive) |
| 19 | 77 | exact (exhaustive) |
| 20 | 84 | best known (ours) |
| 25 | 112 | best known (ours) |
| 30 | 140 | best known (ours) |
| 40 | 190 | best known (ours) |
| 50 | 247 | best known (ours) |

Exact values by exhaustive search (tools/quad_admissible.py, sets with largest element m for increasing m); the sieve (tools/quad_sieve.py) reproduces every exact value and gives the upper bounds for larger k.

## Best known value

247 for k = 50, held by Quantavane (Arhan Canli), 9 November 2026: the set in `refs/quad-admissible.txt`. Lower bound: m(50) >= m(19) = 77 (removing elements keeps a set admissible); nothing better is proved.

Bound on the other side: 77 (lower bound; m(k) is non-decreasing and m(19) = 77 exactly).

## Submitting and checking

Format: Text file: 50 distinct positive integers h, separated by spaces or newlines (lines starting with # are ignored).

Score: the largest element of the set (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check quad-admissible FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_numth.py quad-admissible 50 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/quad-admissible.txt`.

## References

- P. T. Bateman, R. A. Horn, A heuristic asymptotic formula concerning the distribution of prime numbers, Math. Comp. 16 (1962) 363-367
- G. H. Hardy, J. E. Littlewood, Some problems of 'Partitio numerorum' III, Acta Math. 44 (1923) 1-70 (Conjecture F on n^2 + 1)
- D. H. J. Polymath, Variants of the Selberg sieve, and bounded intervals containing many primes, arXiv:1407.4897 (H(k) for linear tuples)
- W. Banks, K. Ford, Sets of integers satisfying Bateman-Horn statistics, arXiv:2605.01155
- A. Kourbatov, M. Wolf, Predicting maximal gaps in sets of primes, arXiv:1901.03785 (densest linear patterns)
