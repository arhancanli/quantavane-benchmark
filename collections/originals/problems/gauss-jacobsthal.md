# The Jacobsthal function of the Gaussian integers

`gauss-jacobsthal` · Number theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **15** (maximize), Quantavane (Arhan Canli), 9 November 2026: weighted local search for one residue class per prime covering the 15 x 15 square (tools/src/gjacob.c, mode search), turned into a square of Gaussian integers by the Chinese remainder theorem (tools/gauss_jacobsthal.py); searches of 20 seconds with two seeds did not cover the 16 x 16 square

## Statement

For a bound X, let s(X) be the side of the largest square block of Gaussian integers {x + yi : x0 <= x < x0 + s, y0 <= y < y0 + s} in which every element is divisible by some Gaussian prime of norm at most X, that is, no element is coprime to the product of those primes. This is the two-dimensional analogue, for the Gaussian integers, of Jacobsthal's function j(m) at a primorial (the longest run of consecutive integers each sharing a factor with m). By the Chinese remainder theorem s(X) is also the largest s for which one residue class modulo each Gaussian prime of norm at most X covers an s x s square. The headline cell is X = 100, with the 25 Gaussian primes of norm at most 100 (up to units): find a square of side 16 or more in which every Gaussian integer has a prime factor of norm at most 100 (ours: side 15).

## Why it is interesting

Jacobsthal's function j(m) is the smallest j such that every run of j consecutive integers contains one coprime to m. Its values at the primorials measure how long a run of integers can be sieved out by the small primes, which is the engine of every construction of long gaps between primes, from Westzynthius and Rankin to the work of Ford, Green, Konyagin, Maynard and Tao (2018), and it is computed exactly to large primorials (Hagedorn 2009; Ziller and Morack). Generalisations replace the run of integers by paired progressions (Ziller and Morack) or by the values of a polynomial (Kalmynin and Konyagin). In the Gaussian integers the natural run is a square block, and the same sieve gives squares of Gaussian integers with no prime among them far from the origin, the two-dimensional counterpart of long prime gaps (compare the Gaussian moat problem of Gethner, Wagon and Wick on walking through Gaussian primes). The sieve is richer than for the integers: a split prime p = 1 mod 4 contributes two prime ideals, each removing a different lattice line pattern of density 1/p, an inert prime q = 3 mod 4 removes only a sublattice of density 1/q^2, and 1 + i removes a checkerboard. The values below are exact up to X = 41 by an exhaustive search (the first uncovered point must be covered by some unused prime; branches are cut when the unused primes cannot cover what is left), and best known beyond.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/gauss-jacobsthal.json`](../novelty/gauss-jacobsthal.json) with its address, the time it ran and its first results.

- arXiv API, 6 searches:
  - `all:Jacobsthal AND all:Gaussian`: 2 results
  - `all:"Jacobsthal function" AND all:"number field"`: 0 results
  - `all:"Jacobsthal function" AND all:"imaginary quadratic"`: 1 result
  - `all:"Jacobsthal function" AND all:"two-dimensional"`: 0 results
  - `all:"Gaussian integers" AND all:coprime AND all:primorial`: 0 results
  - `all:"Jacobsthal" AND all:"lattice points"`: 0 results
- OEIS, 5 searches:
  - `Jacobsthal Gaussian`: 9 results (A001045, A014551, A015331, A000225, A002275)
  - `Gaussian integers Jacobsthal function`: 5 results (A001045, A014551, A000225, A000129, A341091)
  - `Jacobsthal function Gaussian primes`: 3 results (A001045, A000225, A000129)
  - `1,2,2,4,5,7,9`: 10 results (A000726, A211861, A137200, A240215, A094362)
  - `1,2,2,4,5,7,9,9`: 0 results
- Web search (general web search), `"Jacobsthal function" Gaussian integers OR "number fields" OR "imaginary quadratic" generalization maximal gap coprime`: the generalised Jacobsthal function for paired progressions (arXiv:1706.03668), the polynomial analogue of Kalmynin and Konyagin (runs of integers i with N sharing a factor with x + f(i)), and papers on Gaussian or complex Jacobsthal numbers (an unrelated sequence); no Jacobsthal function of the Gaussian integers or of other rings of integers
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no sieve or Jacobsthal family in the benchmark.

Closest work found, and how this problem differs:
- Jacobsthal's function of the integers at primorials (Jacobsthal 1960; Hagedorn 2009; Ziller and Morack): runs of integers, not squares of Gaussian integers.
- Generalised Jacobsthal functions for paired progressions (Ziller and Morack, arXiv:1706.03668) and for polynomial values (Kalmynin and Konyagin, arXiv:2302.00459): other generalisations, still over the integers.
- The Gaussian moat problem (Gethner, Wagon and Wick 1998): gaps between Gaussian primes for a walk to infinity, a different question.

Verdict: new question for the Gaussian integers: Jacobsthal's function is studied for the integers and generalised to paired progressions and to polynomial values, but no Jacobsthal function of the Gaussian integers (or of another ring of integers) was found, as far as our searches show.

## First values

| X (norm bound) | Gaussian primes of norm <= X (up to units) | s(X) | how |
| --- | --- | --- | --- |
| 2 | 1 | 1 | exact |
| 5 | 3 | 2 | exact |
| 9 | 4 | 2 | exact |
| 13 | 6 | 4 | exact |
| 17 | 8 | 5 | exact |
| 29 | 10 | 7 | exact |
| 37 | 12 | 9 | exact |
| 41 | 14 | 9 | exact |
| 49 | 15 | 9 or 10 | 9 by exhaustive search; 10 not decided in 900 s |
| 53 | 17 | 11 | best known (ours; 12 not reached) |
| 61 | 19 | 11 | best known (ours; 12 not reached) |
| 73 | 21 | 13 | best known (ours; 14 not reached) |
| 89 | 23 | 15 | best known (ours; 16 not reached) |
| 100 | 25 | 15 | best known (ours; 16 not reached) |

Exact values: tools/src/gjacob.c, mode exact (s + 1 proved impossible: X = 37 in 4 s, X = 41 in 520 s); exhaustive searches over all residue classes for X = 5 and X = 13 in the tests agree. For X = 49 the exhaustive search covered the 9 x 9 square but did not settle 10 x 10 within 900 s. Best known values: mode search (weighted local search, 20 s for each attempt, two seeds); the gaps above them are open. The X = 100 square is in refs/gauss-jacobsthal.txt.

## Best known value

15: the 15 x 15 square with corner 326020023537680738 + 705589564511901608 i, every element divisible by a Gaussian prime of norm at most 100, held by Quantavane (Arhan Canli), 9 November 2026 (`refs/gauss-jacobsthal.txt`).

## Submitting and checking

Format: Text file: one line 'x0 y0 s', the corner x0 + y0 i and the side s of the square (x0 and y0 may be large integers).

Score: the side s of the square (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check gauss-jacobsthal FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_numth.py gauss-jacobsthal 100 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/gauss-jacobsthal.txt`.

## References

- E. Jacobsthal, Uber Sequenzen ganzer Zahlen, von denen keine zu n teilerfremd ist, I-III, Norske Vid. Selsk. Forh. (Trondheim) 33 (1960)
- T. R. Hagedorn, Computation of Jacobsthal's function h(n) for n < 50, Math. Comp. 78 (2009) 1073-1087
- M. Ziller, J. F. Morack, A short note on the computation of the generalised Jacobsthal function for paired progressions, arXiv:1706.03668
- A. Kalmynin, S. Konyagin, A polynomial analogue of Jacobsthal function, arXiv:2302.00459
- K. Ford, B. Green, S. Konyagin, J. Maynard, T. Tao, Long gaps between primes, J. Amer. Math. Soc. 31 (2018) 65-105
- E. Gethner, S. Wagon, B. Wick, A stroll through the Gaussian primes, Amer. Math. Monthly 105 (1998) 327-337
