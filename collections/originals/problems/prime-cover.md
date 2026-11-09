# Covering the five-digit primes by one-digit changes

`prime-cover` · Coding theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **1219** (minimize), Quantavane (Arhan Canli), 9 November 2026: greedy construction, then iterated removal of one to three random code primes, greedy repair and pruning, 300 seconds (tools/src/dominate.c)

## Statement

Two n-digit primes are neighbours when they differ in exactly one digit (the leading digit stays nonzero), as in a word ladder: 10007 and 10009, or 10007 and 10607. A covering code of radius 1 inside the n-digit primes is a set C of n-digit primes such that every n-digit prime is in C or is a neighbour of a prime in C. Let c(n) be the smallest size of such a code. The headline cell is n = 5, the 8,363 five-digit primes: find a covering code with fewer than 1,219 primes.

## Why it is interesting

Covering codes ask for the fewest words such that every word of a space is within a given distance of one of them; in the Hamming spaces they are the football-pool problem and its relatives (Cohen, Honkala, Litsyn and Lobstein 1997). Restricting the space to the primes makes the neighbourhoods irregular: a five-digit prime has between 1 and 16 prime neighbours, and primes that agree except in one place form cliques, which makes packing arguments weak. Primes with no prime neighbour at all, the digitally delicate primes, would have to belong to every code; Tao (2011) proved that a positive proportion of primes are digitally delicate, and the smallest one is 294001, so the five-digit primes have none. A fractional count gives c(5) >= 686 (every prime needs a code prime among its neighbours, and a code prime covers at most 17 primes); the best code found has 1,219 primes, and the gap is open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/prime-cover.json`](../novelty/prime-cover.json) with its address, the time it ran and its first results.

- arXiv API, 5 searches:
  - `all:primes AND all:"Hamming distance" AND all:"covering code"`: 0 results
  - `all:"digitally delicate primes"`: 3 results
  - `all:primes AND all:"one digit" AND all:graph AND all:domination`: 0 results
  - `all:"covering code" AND all:primes`: 8 results
  - `all:"dominating set" AND all:"prime numbers" AND all:digits`: 0 results
- OEIS, 4 searches:
  - `primes differ in one digit`: 10 results (A090910, A100369, A103900, A048853, A235154)
  - `dominating set primes digits`: 9 results (A372309, A370612, A000110, A000045, A000108)
  - `4,22`: 10 results (A002293, A181819, A057163, A116608, A360005)
  - `domination number primes one digit`: 10 results (A014499, A000045, A000108, A000110, A000225)
- Web search (general web search), `smallest set of primes such that every five-digit prime differs from one of them in at most one digit dominating set "prime graph" digits change one digit`: sum-dominant sets of primes, OEIS entries on primes differing in every digit and on five-digit primes with distinct digits; nothing on covering or dominating the primes by one-digit changes
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark's covering-design and code families concern whole Hamming or Johnson spaces, not primes.

Closest work found, and how this problem differs:
- Covering codes and the football-pool problem in Hamming spaces (Cohen, Honkala, Litsyn and Lobstein): the whole space, regular neighbourhoods; here only primes.
- Digitally delicate primes (Tao 2011; Filaseta and others): primes with no prime neighbour, which would be forced into any code; none has five digits.

Verdict: new question: covering codes of Hamming spaces and digitally delicate primes are studied; no result was found on covering codes inside the primes with the digit (Hamming) distance.

## First values

| n (digits) | n-digit primes | smallest code found | how | fractional lower bound |
| --- | --- | --- | --- | --- |
| 2 | 21 | 4 | exact (every set of 3 fails) | 3 |
| 3 | 143 | 22 | best known (ours) | 14 |
| 4 | 1061 | 157 | best known (ours, local search, 15 s) | 93 |
| 5 | 8363 | 1219 | best known (ours, local search, 300 s) | 686 |

Lower bound: the sum over all n-digit primes u of 1/(largest closed neighbourhood among u and its neighbours), rounded up. Codes from tools/src/dominate.c.

## Best known value

1,219 primes, held by Quantavane (Arhan Canli), 9 November 2026: the code in `refs/prime-cover.txt`. Lower bound 686 (fractional count).

Bound on the other side: 686 (lower bound; the sum over the five-digit primes u of 1/(largest closed neighbourhood among u and its neighbours) is 685.95).

## Submitting and checking

Format: Text file: the five-digit primes of the code, separated by spaces or newlines.

Score: the number of primes in the code (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check prime-cover FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_codes.py prime-cover 5 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/prime-cover.txt`.

## References

- G. Cohen, I. Honkala, S. Litsyn, A. Lobstein, Covering Codes, North-Holland (1997)
- T. Tao, A remark on primality testing and decimal expansions, J. Aust. Math. Soc. 91 (2011) 405-413
- OEIS A050249 (weakly primes, or digitally delicate primes: 294001, 505447, ...)
