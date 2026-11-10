# Error-correcting codes made of primes

`prime-code` · Coding theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **299** (maximize), Quantavane (Arhan Canli), 9 November 2026: iterated local search for a maximum independent set of the graph joining two five-digit primes that differ in at most two digits (force a prime in and drop its neighbours, then (1,2)-swaps: one code word out, two in), runs of 60, 300 and 300 seconds with three seeds giving 297, 298 and 299 (tools/src/primecode.c)

## Statement

Choose n-digit primes so that any two of them differ in at least D of their n decimal digits (Hamming distance at least D). With D = 3 the primes form a code that corrects one wrong digit: a five-digit prime read with one digit changed is still closer to it than to any other code word. Let A(n, D) be the largest number of n-digit primes in such a code. The headline cell is n = 5, D = 3, among the 8,363 five-digit primes: find more than 299 five-digit primes, any two differing in at least three digits (ours). Two code words agree in at most two of the five digits, so their (first, second, last) digits are all different: A(5, 3) <= 9 x 10 x 4 = 360.

## Why it is interesting

Error-correcting codes are usually built in a vector space where every word is allowed; here the words must be primes. The primes of a fixed length form the word-ladder graph of our problem prime-cover (two primes adjacent when they differ in one digit), and that problem asks for the smallest covering code of radius one in it; this one asks for the opposite extreme, the largest packing: a set of primes whose balls of radius one are disjoint, so that every single-digit error is corrected. Classical bounds still apply in a restricted form. Two code words of minimum distance D agree in at most n - D digits, so they differ in every set of n - D + 1 positions, and the Singleton bound becomes a count of the allowed digits: 9 first digits, 10 middle digits, and only 1, 3, 7 and 9 as last digits. For four-digit primes this bound, 9 x 4 = 36, is attained; for five-digit primes the bound is 360, and the primes are too sparse to come close as far as we can find. The question joins two well-studied objects, maximum codes and the digit structure of primes (digitally delicate primes, which have no prime at distance one, were studied by Erdos, Tao and others), but codes made of primes are new as far as our searches show.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/prime-code.json`](../novelty/prime-code.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:primes AND all:"error-correcting" AND all:digits`: 3 results
  - `all:"prime numbers" AND all:"Hamming distance"`: 3 results
  - `all:primes AND all:"minimum distance" AND all:"decimal digits"`: 0 results
  - `all:"digitally delicate" AND all:primes`: 4 results
- OEIS, 5 searches:
  - `primes pairwise Hamming distance`: 2 results (A321945, A000166)
  - `largest set of primes differing in at least digits`: 10 results (A163622, A300326, A119892, A001359, A001700)
  - `primes code distance`: 10 results (A164677, A051864, A106169, A110866, A321945)
  - `4,36,299`: 0 results
  - `4,4,36`: 10 results (A046109, A375124, A124859, A253139, A301856)
- Web search (general web search), `largest set of primes with the same number of digits pairwise differing in at least three digits, error-correcting code made of prime numbers, Hamming distance`: prime triplets, prime digit puzzles (primepuzzles.net) and prime curios about concatenations; nothing on codes of primes with a minimum Hamming distance
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark's linear-code and constant-weight-code families are codes over full alphabets; none is restricted to primes.

Closest work found, and how this problem differs:
- Our problem prime-cover: the smallest covering code of radius one inside the five-digit primes, the opposite extreme on the same graph.
- Digitally delicate primes (Erdos; Tao 2011; Hopper and Pollack, arXiv:1510.03401; Filaseta and Juillerat, arXiv:2101.08898): primes with no prime at distance one, a property of single primes, not codes.
- Maximum codes with a minimum distance over a full alphabet (the Singleton and sphere-packing bounds): here the words are restricted to primes.

Verdict: new question: error-correcting codes and the digits of primes are both studied (digitally delicate primes; our own covering problem prime-cover), but no one has asked for the largest set of n-digit primes with a given minimum Hamming distance, as far as our searches show.

## First values

| n (digits) | D | n-digit primes | largest code found | how | upper bound |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | 21 | 4 | exact (bound met: four last digits) | 4 |
| 3 | 3 | 143 | 4 | exact (bound met: four last digits) | 4 |
| 4 | 3 | 1061 | 36 | exact (bound met: 9 first digits x 4 last digits) | 36 |
| 5 | 3 | 8363 | 299 | best known (ours, iterated local search, 300 s) | 360 |

Codes from tools/src/primecode.c; the checker (checkers/orig_codes.py) sieves the n-digit primes and checks every pair. The upper bounds count the possible (first, ..., last) digit tuples on n - D + 1 positions.

## Best known value

299 five-digit primes, any two differing in at least three digits, held by Quantavane (Arhan Canli), 9 November 2026: the code in `refs/prime-code.txt`.

## Cells

The same question at each value of its parameter (n, the number of digits, and D, the minimum number of digits in which two code primes differ): 6 cells, 1 of them exact (an exhaustive search finished) and 5 best known (ours). Each cell has its certificate in `refs/cells/prime-code/` (the headline cell uses `collections/originals/refs/prime-code.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example prime-code-3-2

| cell | n | D | value | status |
| --- | --- | --- | --- | --- |
| `prime-code-3-2` | 3 | 2 | 36 | best known |
| `prime-code-4-2` | 4 | 2 | 322 | best known |
| `prime-code-4-3` | 4 | 3 | 36 | exact |
| `prime-code-5-2` | 5 | 2 | 2569 | best known |
| `prime-code-5-3` | 5 | 3 | 299 | best known (headline) |
| `prime-code-6-3` | 6 | 3 | 2151 | best known |

Exact cells: the construction meets the bound (9 first digits x 4 last digits). Best known cells: iterated local search with (1,2)-swaps for a maximum independent set of the conflict graph (tools/src/primecode.c); a lower bound.

Bound on the other side: 360 (upper bound; two code words agree in at most two of the five digits, so the triples (first digit, second digit, last digit) are all different: at most 9 x 10 x 4, the last digit of a five-digit prime being 1, 3, 7 or 9).

## Submitting and checking

Format: Text file: distinct five-digit primes, separated by spaces or newlines, any two differing in at least three digits.

Score: the number of primes in the code (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check prime-code FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_codes.py prime-code 5 3 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/prime-code.txt`.

## References

- R. C. Singleton, Maximum distance q-nary codes, IEEE Trans. Inform. Theory 10 (1964) 116-118
- T. Tao, A remark on primality testing and decimal expansions, J. Aust. Math. Soc. 91 (2011) 405-413 (digitally delicate primes)
- J. Hopper, P. Pollack, Digitally delicate primes, arXiv:1510.03401
- M. Filaseta, J. Juillerat, Consecutive primes which are widely digitally delicate, arXiv:2101.08898
- D. V. Andrade, M. G. C. Resende, R. F. Werneck, Fast local search for the maximum independent set problem, J. Heuristics 18 (2012) 525-547
