# Arithmetic progressions of Gaussian primes

`gauss-prime-ap` · Number theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **18** (maximize), Quantavane (Arhan Canli), 9 November 2026: exhaustive search over common differences d in 1105(1 + i)Z[i] and all first terms with bit tables of the Gaussian primes of norm up to 1.2 x 10^9 (tools/src/gaussap.c, mode big)

## Statement

A Gaussian prime is a prime element of Z[i]: a + bi with a^2 + b^2 a prime (a, b nonzero), or an associate of a prime p = 3 (mod 4). A k-term progression is a, a + d, ..., a + (k - 1)d with d a nonzero Gaussian integer; Tao (2006) proved that the Gaussian primes contain progressions (and constellations of every shape) of every length. Let M(k) be the least possible largest norm of a k-term progression of Gaussian primes. We find M(k) exactly for k <= 18 (table). The headline cell asks for the longest progression of Gaussian primes all of whose norms are at most 10^11: the best known has 18 terms (ours, all norms at most 557,124,937).

## Why it is interesting

Green and Tao proved that the primes contain arbitrarily long arithmetic progressions, and Tao (2006) that the Gaussian primes contain every finite constellation; both proofs are existence proofs. For the rational primes the least progressions of each length are tabulated and the longest known has 27 terms (PrimeGrid, 2019). For the Gaussian primes we found no computation of explicit long progressions. The arithmetic of Z[i] shapes them: if k >= 10 the common difference must be divisible by 5(1 + i), because otherwise two terms would be divisible by 2 + i (or by 1 + i) and both would have to be the same small prime; a prime ideal P of norm k or less either divides d or contains one term of norm N(P). Inert primes such as 3 and 7 never force anything, since the progression meets only p of the p^2 residue classes modulo p. These facts reduce each length to a few exhaustive searches: M(k) is known exactly for k <= 18 here, and it jumps irregularly (M(12) = 122,033, M(13) = 7,114,409, M(14) = 8,565,209). The least 17-term progression extends to 18 terms with the same largest norm, and no 19-term progression has d in 1105(1 + i)Z[i] and norms up to 1.4 x 10^9. How long a progression fits under 10^11, and how M(k) grows, are open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/gauss-prime-ap.json`](../novelty/gauss-prime-ap.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"Gaussian primes" AND all:"arithmetic progression"`: 6 results
  - `all:"Gaussian primes" AND all:constellations AND all:computation`: 1 result
  - `all:"Gaussian primes" AND all:"arithmetic progressions" AND all:longest`: 0 results
- OEIS, 4 searches:
  - `Gaussian primes arithmetic progression`: 7 results (A000043, A034693, A000984, A004018, A060294)
  - `9,9,17,17,29,29,173,1013,14489`: 0 results
  - `17,29,173,1013,14489,122033`: 0 results
  - `Gaussian primes in arithmetic progression`: 7 results (A000043, A034693, A000984, A004018, A060294)
- Web search (general web search), `longest arithmetic progression of Gaussian primes computational search record smallest norm`: Tao's existence theorem for constellations in the Gaussian primes, expositions of Green-Tao and records for rational primes (Andersen's table, 26 and 27 terms); no computation for Gaussian primes
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no prime-progression family in the benchmark.

Closest work found, and how this problem differs:
- T. Tao (2006): existence of every constellation in the Gaussian primes, with no explicit examples or bounds usable for computation.
- Records for rational primes (minimal and longest progressions, PrimeGrid and others): the same questions in Z.
- Our problem gauss-admissible: admissible constellations (no primality) of smallest diameter in Z[i].

Verdict: new question: long progressions in the Gaussian primes are known to exist (Tao 2006); no computation of explicit progressions, of least norms or of the longest progression in a disc was found.

## First values

| k | least largest norm M(k) | a progression (first term, d) | how |
| --- | --- | --- | --- |
| 3 | 9 | -3, d = 2 - i | exhaustive |
| 4 | 9 | -3, d = 1 - i | exhaustive |
| 5 | 17 | -4 - i, d = 1 + i | exhaustive |
| 6 | 17 | -4 - i, d = 1 + i | exhaustive |
| 7 | 29 | -5 - 2i, d = 1 + i | exhaustive |
| 8 | 29 | -5 - 2i, d = 1 + i | exhaustive |
| 9 | 173 | -13 - 2i, d = 3 + i | exhaustive |
| 10 | 1,013 | -23 - 22i, d = 5 + 5i | exhaustive |
| 11 | 14,489 | -100 - 67i, d = 20 | exhaustive |
| 12 | 122,033 | -268 - 73i, d = 55 + 15i | exhaustive over d in 5(1 + i)Z[i] |
| 13 | 7,114,409 | -460 - 197i, d = 260 | exhaustive over d in 5(1 + i)Z[i] |
| 14 | 8,565,209 | -2920 - 197i, d = 260 | d in 65(1 + i)Z[i], plus every progression through a prime of norm 13 |
| 15 | 82,467,349 | -8985 - 1318i, d = 1040 + 260i | the same case split |
| 16 | 140,768,753 | -9592 - 6983i, d = 1105 + 1105i | the same case split |
| 17 | 557,124,937 | -23189 + 4404i, d = 1105 + 1105i | d in 1105(1 + i)Z[i], plus every progression through a prime of norm 13 or 17 |
| 18 | 557,124,937 | -23189 + 4404i, d = 1105 + 1105i | the 17-term progression extends; M(18) >= M(17) |
| 19 | > 1.4 x 10^9 if d is in 1105(1 + i)Z[i] | none found | search up to norm 1.4 x 10^9 |

Exact values from tools/src/gaussap.c: mode exact (every pair of terms) for k <= 11; for larger k the necessary divisibility of d and the case split by small prime ideals (modes fast, big and through), each search complete up to a norm bound above the value found. M(k) never decreases with k, so M(18) = M(17).

## Best known value

18 terms, held by Quantavane (Arhan Canli), 9 November 2026: the progression in `refs/gauss-prime-ap.txt` (a = -23189 + 4404i, d = 1105 + 1105i, largest norm 557,124,937). No progression of 19 Gaussian primes is known to us.

## Submitting and checking

Format: Text file: one line 'x y' per term x + yi of the progression, in order; every term a Gaussian prime of norm at most 10^11.

Score: the number of terms, an integer (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check gauss-prime-ap FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_numth.py gauss-prime-ap 100000000000 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/gauss-prime-ap.txt`.

## References

- T. Tao, The Gaussian primes contain arbitrarily shaped constellations, J. Anal. Math. 99 (2006) 109-176 (arXiv:math/0501314)
- B. Green, T. Tao, The primes contain arbitrarily long arithmetic progressions, Ann. of Math. 167 (2008) 481-547
- E. Gethner, S. Wagon, B. Wick, A stroll through the Gaussian primes, Amer. Math. Monthly 105 (1998) 327-337
- J. K. Andersen, Primes in arithmetic progression records (web page)
