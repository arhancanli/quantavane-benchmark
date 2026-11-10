# Largest sum-free set of quadratic residues

`qr-sumfree` · Number theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **174** (maximize), Quantavane (Arhan Canli), 9 November 2026: a sum-free set of 174 quadratic residues found by randomized greedy construction with local search (tools/qr_sumfree_search.py)

## Statement

For a prime p let QR_p be the set of the (p-1)/2 nonzero squares modulo p. Let s(p) be the largest size of a subset A of QR_p that is sum-free: a + b = c (mod p) has no solution with a, b, c in A (a = b allowed). Determine s(p), and the behaviour of s(p) / |QR_p| as p grows. The headline cell is p = 1009: find a sum-free set of more than 174 quadratic residues modulo 1009.

## Why it is interesting

Erdos showed that every set of n nonzero integers contains a sum-free subset of more than n/3 elements, Alon and Kleitman extended this to finite groups, and Eberhard, Green and Manners proved that the constant 1/3 cannot be improved; for subsets A of F_p* the largest sum-free subset sf(A) is at least |A|/3 + O(|A|/p), and sets for which sf(A) is close to |A|/3 must be evenly spread over the cosets of large multiplicative subgroups (arXiv:2004.01884). The quadratic residues, the most studied pseudo-random subset of F_p, are themselves a multiplicative subgroup, so s(p) asks where they sit between the general bound |QR_p|/3 and the trivial |QR_p|. The exact values below fluctuate (s(61) = 16 of 30, s(97) = 18 of 48, s(101) = 22 of 50), and our best set for p = 1009 is 174 of 504, close to one third; whether s(p)/|QR_p| tends to 1/3 is open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/qr-sumfree.json`](../novelty/qr-sumfree.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"sum-free" AND all:"quadratic residues"`: 0 results
  - `all:"sum-free" AND all:"multiplicative subgroup"`: 1 result
- OEIS, 3 searches:
  - `1,2,1,3,4,4,4,4,8,5,10,10,9,8,14,12,16,13`: 0 results
  - `2,4,4,8,10,10,14,16`: 0 results
  - `sum-free quadratic residues`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no entry.

Closest work found, and how this problem differs:
- The general sum-free subset problem sf(A) (Erdos 1965, Alon-Kleitman 1990, Eberhard-Green-Manners 2014) and its multiplicative-subgroup refinement (arXiv:2004.01884): this problem is the case A = QR_p, which no source evaluates.

Verdict: new as stated. The largest sum-free subset of a general set A is a classical function (Erdos; Alon and Kleitman); its value for A = the quadratic residues modulo p is not tabulated anywhere we found (OEIS, arXiv), and the sequence s(p) is not in the OEIS.

## First values

| p | |QR_p| | s(p) | how |
| --- | --- | --- | --- |
| 3 | 1 | 1 | exact (exhaustive) |
| 5 | 2 | 2 | exact (exhaustive) |
| 7 | 3 | 1 | exact (exhaustive) |
| 11 | 5 | 3 | exact (exhaustive) |
| 13 | 6 | 4 | exact (exhaustive) |
| 17 | 8 | 4 | exact (exhaustive) |
| 19 | 9 | 4 | exact (exhaustive) |
| 23 | 11 | 4 | exact (exhaustive) |
| 29 | 14 | 8 | exact (exhaustive) |
| 31 | 15 | 5 | exact (exhaustive) |
| 37 | 18 | 10 | exact (exhaustive) |
| 41 | 20 | 10 | exact (exhaustive) |
| 43 | 21 | 9 | exact (exhaustive) |
| 47 | 23 | 8 | exact (exhaustive) |
| 53 | 26 | 14 | exact (exhaustive) |
| 59 | 29 | 12 | exact (exhaustive) |
| 61 | 30 | 16 | exact (exhaustive) |
| 67 | 33 | 13 | exact (exhaustive) |
| 71 | 35 | 12 | exact (exhaustive) |
| 73 | 36 | 16 | exact (exhaustive) |
| 79 | 39 | 13 | exact (exhaustive) |
| 83 | 41 | 16 | exact (exhaustive) |
| 89 | 44 | 16 | exact (exhaustive) |
| 97 | 48 | 18 | exact (exhaustive) |
| 101 | 50 | 22 | exact (exhaustive) |
| 103 | 51 | 17 | exact (exhaustive) |
| 107 | 53 | 20 | exact (exhaustive) |
| 109 | 54 | 24 | exact (exhaustive) |
| 113 | 56 | 22 | exact (exhaustive) |
| 1009 | 504 | 174 | best known (ours) |

Exact values for every prime p <= 113 by exhaustive branch and bound (each candidate residue checked against all sums of chosen ones); the p = 1009 value is our best known lower bound. Our heuristic reproduces every exact value it was tried on (p = 61, 101).

## Best known value

174 for p = 1009, held by Quantavane (Arhan Canli), 9 November 2026: the set in `refs/qr-sumfree.txt`. Lower bound from the general theory: at least |QR_p|/3 + O(|QR_p|/p), about 168; upper bound: trivially at most 504, and no better bound is proved here.

## Cells

The same question at each value of its parameter (p, a prime): 71 cells, 21 of them exact (an exhaustive search finished) and 50 best known (ours). Each cell has its certificate in `refs/cells/qr-sumfree/` (the headline cell uses `collections/originals/refs/qr-sumfree.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example qr-sumfree-29

| cell | p | value | status |
| --- | --- | --- | --- |
| `qr-sumfree-29` | 29 | 8 | exact |
| `qr-sumfree-31` | 31 | 5 | exact |
| `qr-sumfree-37` | 37 | 10 | exact |
| `qr-sumfree-41` | 41 | 10 | exact |
| `qr-sumfree-43` | 43 | 9 | exact |
| `qr-sumfree-47` | 47 | 8 | exact |
| `qr-sumfree-53` | 53 | 14 | exact |
| `qr-sumfree-59` | 59 | 12 | exact |
| `qr-sumfree-61` | 61 | 16 | exact |
| `qr-sumfree-67` | 67 | 13 | exact |
| `qr-sumfree-71` | 71 | 12 | exact |
| `qr-sumfree-73` | 73 | 16 | exact |
| `qr-sumfree-79` | 79 | 13 | exact |
| `qr-sumfree-83` | 83 | 16 | exact |
| `qr-sumfree-89` | 89 | 16 | exact |
| `qr-sumfree-97` | 97 | 18 | exact |
| `qr-sumfree-101` | 101 | 22 | exact |
| `qr-sumfree-103` | 103 | 17 | exact |
| `qr-sumfree-107` | 107 | 20 | exact |
| `qr-sumfree-109` | 109 | 24 | exact |
| `qr-sumfree-113` | 113 | 22 | exact |
| `qr-sumfree-127` | 127 | 21 | best known |
| `qr-sumfree-131` | 131 | 24 | best known |
| `qr-sumfree-137` | 137 | 26 | best known |
| `qr-sumfree-139` | 139 | 25 | best known |
| `qr-sumfree-149` | 149 | 32 | best known |
| `qr-sumfree-151` | 151 | 25 | best known |
| `qr-sumfree-157` | 157 | 34 | best known |
| `qr-sumfree-163` | 163 | 29 | best known |
| `qr-sumfree-167` | 167 | 28 | best known |
| `qr-sumfree-173` | 173 | 38 | best known |
| `qr-sumfree-179` | 179 | 31 | best known |
| `qr-sumfree-181` | 181 | 40 | best known |
| `qr-sumfree-191` | 191 | 32 | best known |
| `qr-sumfree-193` | 193 | 36 | best known |
| `qr-sumfree-197` | 197 | 44 | best known |
| `qr-sumfree-199` | 199 | 33 | best known |
| `qr-sumfree-211` | 211 | 36 | best known |
| `qr-sumfree-223` | 223 | 37 | best known |
| `qr-sumfree-227` | 227 | 41 | best known |
| `qr-sumfree-229` | 229 | 46 | best known |
| `qr-sumfree-233` | 233 | 44 | best known |
| `qr-sumfree-239` | 239 | 40 | best known |
| `qr-sumfree-241` | 241 | 42 | best known |
| `qr-sumfree-251` | 251 | 44 | best known |
| `qr-sumfree-257` | 257 | 46 | best known |
| `qr-sumfree-263` | 263 | 44 | best known |
| `qr-sumfree-269` | 269 | 52 | best known |
| `qr-sumfree-271` | 271 | 45 | best known |
| `qr-sumfree-277` | 277 | 60 | best known |
| `qr-sumfree-281` | 281 | 50 | best known |
| `qr-sumfree-283` | 283 | 50 | best known |
| `qr-sumfree-293` | 293 | 60 | best known |
| `qr-sumfree-307` | 307 | 54 | best known |
| `qr-sumfree-311` | 311 | 52 | best known |
| `qr-sumfree-313` | 313 | 56 | best known |
| `qr-sumfree-317` | 317 | 66 | best known |
| `qr-sumfree-331` | 331 | 56 | best known |
| `qr-sumfree-337` | 337 | 62 | best known |
| `qr-sumfree-347` | 347 | 60 | best known |
| `qr-sumfree-349` | 349 | 68 | best known |
| `qr-sumfree-353` | 353 | 56 | best known |
| `qr-sumfree-359` | 359 | 60 | best known |
| `qr-sumfree-367` | 367 | 61 | best known |
| `qr-sumfree-373` | 373 | 78 | best known |
| `qr-sumfree-379` | 379 | 64 | best known |
| `qr-sumfree-383` | 383 | 64 | best known |
| `qr-sumfree-389` | 389 | 76 | best known |
| `qr-sumfree-397` | 397 | 80 | best known |
| `qr-sumfree-401` | 401 | 70 | best known |
| `qr-sumfree-1009` | 1009 | 174 | best known (headline) |

Exact cells: the value of the exhaustive branch and bound over subsets of the squares (9 November 2026); the certificate is a set of that size found by our local search. Best known cells: randomized greedy construction and local search (tools/qr_sumfree_search.py); a lower bound.

## Submitting and checking

Format: Text file: the elements of A, distinct nonzero squares modulo 1009 written as integers in 1..1008, separated by spaces or newlines.

Score: the number of elements (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check qr-sumfree FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_numth.py qr-sumfree 1009 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/qr-sumfree.txt`.

## References

- P. Erdos, Extremal problems in number theory, Proc. Sympos. Pure Math. 8 (1965) 181-189
- N. Alon, D. J. Kleitman, Sum-free subsets, in A Tribute to Paul Erdos (Cambridge University Press, 1990) 13-26
- S. Eberhard, B. Green, F. Manners, Sets of integers with no large sum-free subset, Annals of Math. 180 (2014) 621-652
- L-functions and sum-free sets, arXiv:2004.01884
