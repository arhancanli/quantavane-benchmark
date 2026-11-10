# Admissible constellations of smallest diameter in the Gaussian integers

`gauss-admissible` · Number theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **218** (minimize), Quantavane (Arhan Canli), 9 November 2026: an admissible 50-set of diameter 218 found by a greedy sieve in a disc followed by local repair (tools/admissible_sieve.py)

## Statement

A finite set H of Gaussian integers is admissible if, for every prime ideal P of Z[i], the elements of H do not meet every residue class modulo P. Only prime ideals of norm at most |H| can be covered, so admissibility is a finite check: H must avoid one of the 2 classes modulo (1+i) (all its elements x + yi have x + y of the same parity), one of the p classes modulo each of the two prime ideals above a prime p = 1 (mod 4) with p <= |H|, and one of the p^2 classes modulo an inert prime p = 3 (mod 4) with p^2 <= |H|. The diameter of H is the largest squared distance |h - h'|^2 between two of its elements. Let D(k) be the least diameter of an admissible set of k Gaussian integers. Determine D(k); the headline cell is k = 50: find an admissible 50-set of diameter less than 218. The same question in the Eisenstein integers Z[w], w = (-1 + sqrt(-3))/2, with squared distance x^2 - xy + y^2 for x + yw, is part of the problem (second column of the table).

## Why it is interesting

For rational integers the least width H(k) of an admissible k-tuple is the quantity behind bounded gaps between primes: Zhang, Maynard and Polymath8b showed that the Dickson-Hardy-Littlewood statement DHL[k,2] gives infinitely many pairs of primes at distance at most H(k), and Engelsma's exact values (k <= 342) and Sutherland's tables of narrow admissible tuples are the record lists [Maynard, arXiv:1311.4600; Polymath, arXiv:1407.4897]. Maynard's sieve carries over to number fields, giving bounded gaps between prime elements of a fixed number field [Castillo, Hall, Lemke Oliver, Pollack and Thompson, arXiv:1403.5808], and in Z[i] the analogue of H(k) is the smallest diameter D(k) defined here: if the Hardy-Littlewood conjecture for Gaussian primes holds, every admissible set has infinitely many translates made of Gaussian primes. Renze, Wagon and Wick catalogued the 52 maximal admissible connected sets of Gaussian primes (The Gaussian Zoo, Experimental Math. 10 (2001)); smallest diameters for every k had not been computed.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/gauss-admissible.json`](../novelty/gauss-admissible.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:admissible AND all:"Gaussian integers" AND all:tuples`: 0 results
  - `all:"prime constellations" AND all:Gaussian`: 0 results
  - `all:"Gaussian primes" AND all:"k-tuple"`: 0 results
- OEIS, 2 searches:
  - `2,4,4,10,10,16,16,20,20,32,32,40,40,50,52,52,58,58,68,68,74,80,90,90`: 0 results
  - `1,3,4,4,4,12,12,12,16,21,21,28,28,28,36,39,39,39,48,49,49,52,52,63`: 0 results
- Web search (general web search), `admissible k-tuples Gaussian integers minimal diameter prime constellations Z[i]`: only the rational-integer tables (H(k), Engelsma, Sutherland)
- Web search (general web search), `"Gaussian prime" constellations OR "Gaussian prime k-tuples" OR "admissible" "Gaussian integers" Hardy-Littlewood tuples`: The Gaussian Zoo (Renze, Wagon, Wick 2001): maximal admissible connected sets; no smallest-diameter table
- Web search (general web search), `Gaussian primes "admissible" patterns smallest diameter OR "densest" admissible sets Gaussian integers table`: no table of smallest-diameter admissible Gaussian sets
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no entry; the benchmark has no prime-pattern family.

Closest work found, and how this problem differs:
- Renze, Wagon and Wick, The Gaussian Zoo (2001): all 52 maximal admissible connected sets of Gaussian primes. Connectedness bounds the size; here sets need not be connected and the question is the least diameter for every k, the analogue of H(k).
- Engelsma's and Sutherland's tables of H(k) for rational integers: the one-dimensional problem this one extends.

Verdict: new. No paper, OEIS entry or table of smallest-diameter admissible sets of Gaussian or Eisenstein integers was found; the sequences of exact values below are not in the OEIS. The closest work catalogues connected admissible patterns (The Gaussian Zoo), a different question with finitely many answers.

## First values

| k | D(k) in Z[i] | D(k) in Z[w] (norm x^2 - xy + y^2) |
| --- | --- | --- |
| 1 | 0 (exact) | 0 (exact) |
| 2 | 2 (exact) | 1 (exact) |
| 3 | 4 (exact) | 3 (exact) |
| 4 | 4 (exact) | 4 (exact) |
| 5 | 10 (exact) | 4 (exact) |
| 6 | 10 (exact) | 4 (exact) |
| 7 | 16 (exact) | 12 (exact) |
| 8 | 16 (exact) | 12 (exact) |
| 9 | 20 (exact) | 12 (exact) |
| 10 | 20 (exact) | 16 (exact) |
| 11 | 32 (exact) | 21 (exact) |
| 12 | 32 (exact) | 21 (exact) |
| 13 | 40 (exact) | 28 (exact) |
| 14 | 40 (exact) | 28 (exact) |
| 15 | 50 (exact) | 28 (exact) |
| 16 | 52 (exact) | 36 (exact) |
| 17 | 52 (exact) | 39 (exact) |
| 18 | 58 (exact) | 39 (exact) |
| 19 | 58 (exact) | 39 (exact) |
| 20 | 68 (exact) | 48 (exact) |
| 21 | 68 (exact) | 49 (exact) |
| 22 | 74 (exact) | 49 (exact) |
| 23 | 80 (exact) | 52 (exact) |
| 24 | 90 (exact) | 52 (exact) |
| 25 | 90 (exact) | 63 (exact) |
| 26 | 100 | 63 (exact) |
| 27 | 100 | 63 (exact) |
| 28 | 104 | 64 (exact) |
| 29 | 106 | 76 |
| 30 | 106 | 76 |
| 31 | 122 | 76 |
| 32 | 122 | 84 |
| 33 | 130 | 84 |
| 34 | 136 | 91 |
| 35 | 144 | 93 |
| 36 | 144 | 93 |
| 37 | 148 | 93 |
| 38 | 164 | 103 |
| 39 | 164 | 109 |
| 40 | 164 | 111 |
| 42 | 178 | 112 |
| 44 | 180 | 124 |
| 46 | 200 | 133 |
| 48 | 202 | 133 |
| 50 | 218 | 147 |
| 52 | 234 | 156 |
| 56 | 260 | 156 |
| 60 | 290 | 183 |
| 64 | 296 | 196 |

Exact values come from an exhaustive branch and bound (tools/src/admissible_exact.c: translate so that the lexicographically least point is 0, add points in a fixed order, prune when a prime ideal's classes are all covered). The other values are our best known upper bounds (tools/admissible_sieve.py), held by Quantavane (Arhan Canli), 9 November 2026. Exact searches were stopped at k = 26 for Z[i] and k = 29 for Z[w]. Rows improved on 10 November 2026 show the value of the cell (see Cells; tools/src/admsieve.c, the same sieve in C).

## Best known value

218 for k = 50 in Z[i], held by Quantavane (Arhan Canli), 9 November 2026: the set in `refs/gauss-admissible.txt`, found by sieving a disc (for each prime ideal of norm <= 50, smallest norm first, delete the residue class holding the fewest points) and then exchanging points on the diameter (tools/admissible_sieve.py). In Z[w], our best 50-set has diameter 147. Lower bound: D(50) >= D(25) = 90, since removing points keeps a set admissible; nothing better is proved.

## Cells

The same question at each value of its parameter (the ring (4: the Gaussian integers Z[i]; 3: the Eisenstein integers Z[w]) and k, the number of points): 122 cells, 47 of them exact (an exhaustive search finished) and 75 best known (ours). Each cell has its certificate in `refs/cells/gauss-admissible/` (the headline cell uses `collections/originals/refs/gauss-admissible.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example gauss-admissible-3-4

| cell | ring | k | value | status |
| --- | --- | --- | --- | --- |
| `gauss-admissible-3-4` | 3 | 4 | 4 | exact |
| `gauss-admissible-3-5` | 3 | 5 | 4 | exact |
| `gauss-admissible-3-6` | 3 | 6 | 4 | exact |
| `gauss-admissible-3-7` | 3 | 7 | 12 | exact |
| `gauss-admissible-3-8` | 3 | 8 | 12 | exact |
| `gauss-admissible-3-9` | 3 | 9 | 12 | exact |
| `gauss-admissible-3-10` | 3 | 10 | 16 | exact |
| `gauss-admissible-3-11` | 3 | 11 | 21 | exact |
| `gauss-admissible-3-12` | 3 | 12 | 21 | exact |
| `gauss-admissible-3-13` | 3 | 13 | 28 | exact |
| `gauss-admissible-3-14` | 3 | 14 | 28 | exact |
| `gauss-admissible-3-15` | 3 | 15 | 28 | exact |
| `gauss-admissible-3-16` | 3 | 16 | 36 | exact |
| `gauss-admissible-3-17` | 3 | 17 | 39 | exact |
| `gauss-admissible-3-18` | 3 | 18 | 39 | exact |
| `gauss-admissible-3-19` | 3 | 19 | 39 | exact |
| `gauss-admissible-3-20` | 3 | 20 | 48 | exact |
| `gauss-admissible-3-21` | 3 | 21 | 49 | exact |
| `gauss-admissible-3-22` | 3 | 22 | 49 | exact |
| `gauss-admissible-3-23` | 3 | 23 | 52 | exact |
| `gauss-admissible-3-24` | 3 | 24 | 52 | exact |
| `gauss-admissible-3-25` | 3 | 25 | 63 | exact |
| `gauss-admissible-3-26` | 3 | 26 | 63 | exact |
| `gauss-admissible-3-27` | 3 | 27 | 63 | exact |
| `gauss-admissible-3-28` | 3 | 28 | 64 | exact |
| `gauss-admissible-3-29` | 3 | 29 | 76 | best known |
| `gauss-admissible-3-30` | 3 | 30 | 76 | best known |
| `gauss-admissible-3-31` | 3 | 31 | 76 | best known |
| `gauss-admissible-3-32` | 3 | 32 | 84 | best known |
| `gauss-admissible-3-33` | 3 | 33 | 84 | best known |
| `gauss-admissible-3-34` | 3 | 34 | 91 | best known |
| `gauss-admissible-3-35` | 3 | 35 | 93 | best known |
| `gauss-admissible-3-36` | 3 | 36 | 93 | best known |
| `gauss-admissible-3-37` | 3 | 37 | 93 | best known |
| `gauss-admissible-3-38` | 3 | 38 | 103 | best known |
| `gauss-admissible-3-39` | 3 | 39 | 109 | best known |
| `gauss-admissible-3-40` | 3 | 40 | 111 | best known |
| `gauss-admissible-3-41` | 3 | 41 | 112 | best known |
| `gauss-admissible-3-42` | 3 | 42 | 112 | best known |
| `gauss-admissible-3-43` | 3 | 43 | 117 | best known |
| `gauss-admissible-3-44` | 3 | 44 | 124 | best known |
| `gauss-admissible-3-45` | 3 | 45 | 124 | best known |
| `gauss-admissible-3-46` | 3 | 46 | 133 | best known |
| `gauss-admissible-3-47` | 3 | 47 | 133 | best known |
| `gauss-admissible-3-48` | 3 | 48 | 133 | best known |
| `gauss-admissible-3-49` | 3 | 49 | 147 | best known |
| `gauss-admissible-3-50` | 3 | 50 | 147 | best known |
| `gauss-admissible-3-51` | 3 | 51 | 148 | best known |
| `gauss-admissible-3-52` | 3 | 52 | 156 | best known |
| `gauss-admissible-3-53` | 3 | 53 | 156 | best known |
| `gauss-admissible-3-54` | 3 | 54 | 156 | best known |
| `gauss-admissible-3-55` | 3 | 55 | 156 | best known |
| `gauss-admissible-3-56` | 3 | 56 | 156 | best known |
| `gauss-admissible-3-57` | 3 | 57 | 171 | best known |
| `gauss-admissible-3-58` | 3 | 58 | 172 | best known |
| `gauss-admissible-3-59` | 3 | 59 | 172 | best known |
| `gauss-admissible-3-60` | 3 | 60 | 183 | best known |
| `gauss-admissible-3-61` | 3 | 61 | 189 | best known |
| `gauss-admissible-3-62` | 3 | 62 | 196 | best known |
| `gauss-admissible-3-63` | 3 | 63 | 196 | best known |
| `gauss-admissible-3-64` | 3 | 64 | 196 | best known |
| `gauss-admissible-4-4` | 4 | 4 | 4 | exact |
| `gauss-admissible-4-5` | 4 | 5 | 10 | exact |
| `gauss-admissible-4-6` | 4 | 6 | 10 | exact |
| `gauss-admissible-4-7` | 4 | 7 | 16 | exact |
| `gauss-admissible-4-8` | 4 | 8 | 16 | exact |
| `gauss-admissible-4-9` | 4 | 9 | 20 | exact |
| `gauss-admissible-4-10` | 4 | 10 | 20 | exact |
| `gauss-admissible-4-11` | 4 | 11 | 32 | exact |
| `gauss-admissible-4-12` | 4 | 12 | 32 | exact |
| `gauss-admissible-4-13` | 4 | 13 | 40 | exact |
| `gauss-admissible-4-14` | 4 | 14 | 40 | exact |
| `gauss-admissible-4-15` | 4 | 15 | 50 | exact |
| `gauss-admissible-4-16` | 4 | 16 | 52 | exact |
| `gauss-admissible-4-17` | 4 | 17 | 52 | exact |
| `gauss-admissible-4-18` | 4 | 18 | 58 | exact |
| `gauss-admissible-4-19` | 4 | 19 | 58 | exact |
| `gauss-admissible-4-20` | 4 | 20 | 68 | exact |
| `gauss-admissible-4-21` | 4 | 21 | 68 | exact |
| `gauss-admissible-4-22` | 4 | 22 | 74 | exact |
| `gauss-admissible-4-23` | 4 | 23 | 80 | exact |
| `gauss-admissible-4-24` | 4 | 24 | 90 | exact |
| `gauss-admissible-4-25` | 4 | 25 | 90 | exact |
| `gauss-admissible-4-26` | 4 | 26 | 100 | best known |
| `gauss-admissible-4-27` | 4 | 27 | 100 | best known |
| `gauss-admissible-4-28` | 4 | 28 | 104 | best known |
| `gauss-admissible-4-29` | 4 | 29 | 106 | best known |
| `gauss-admissible-4-30` | 4 | 30 | 106 | best known |
| `gauss-admissible-4-31` | 4 | 31 | 122 | best known |
| `gauss-admissible-4-32` | 4 | 32 | 122 | best known |
| `gauss-admissible-4-33` | 4 | 33 | 130 | best known |
| `gauss-admissible-4-34` | 4 | 34 | 136 | best known |
| `gauss-admissible-4-35` | 4 | 35 | 144 | best known |
| `gauss-admissible-4-36` | 4 | 36 | 144 | best known |
| `gauss-admissible-4-37` | 4 | 37 | 148 | best known |
| `gauss-admissible-4-38` | 4 | 38 | 164 | best known |
| `gauss-admissible-4-39` | 4 | 39 | 164 | best known |
| `gauss-admissible-4-40` | 4 | 40 | 164 | best known |
| `gauss-admissible-4-41` | 4 | 41 | 164 | best known |
| `gauss-admissible-4-42` | 4 | 42 | 178 | best known |
| `gauss-admissible-4-43` | 4 | 43 | 180 | best known |
| `gauss-admissible-4-44` | 4 | 44 | 180 | best known |
| `gauss-admissible-4-45` | 4 | 45 | 194 | best known |
| `gauss-admissible-4-46` | 4 | 46 | 200 | best known |
| `gauss-admissible-4-47` | 4 | 47 | 200 | best known |
| `gauss-admissible-4-48` | 4 | 48 | 202 | best known |
| `gauss-admissible-4-49` | 4 | 49 | 208 | best known |
| `gauss-admissible-4-50` | 4 | 50 | 218 | best known (headline) |
| `gauss-admissible-4-51` | 4 | 51 | 218 | best known |
| `gauss-admissible-4-52` | 4 | 52 | 234 | best known |
| `gauss-admissible-4-53` | 4 | 53 | 244 | best known |
| `gauss-admissible-4-54` | 4 | 54 | 244 | best known |
| `gauss-admissible-4-55` | 4 | 55 | 250 | best known |
| `gauss-admissible-4-56` | 4 | 56 | 260 | best known |
| `gauss-admissible-4-57` | 4 | 57 | 260 | best known |
| `gauss-admissible-4-58` | 4 | 58 | 260 | best known |
| `gauss-admissible-4-59` | 4 | 59 | 272 | best known |
| `gauss-admissible-4-60` | 4 | 60 | 290 | best known |
| `gauss-admissible-4-61` | 4 | 61 | 290 | best known |
| `gauss-admissible-4-62` | 4 | 62 | 290 | best known |
| `gauss-admissible-4-63` | 4 | 63 | 292 | best known |
| `gauss-admissible-4-64` | 4 | 64 | 296 | best known |

Exact cells: exhaustive branch and bound (tools/src/admissible_exact.c, 9 November 2026), the certificate a set of that diameter found by the sieve (tools/src/admsieve.c). Best known cells: greedy sieve in a disc with local repair, the method of tools/admissible_sieve.py in C (tools/src/admsieve.c, the best of three runs of 400 trials); an upper bound.

Bound on the other side: 90 (lower bound; D(50) >= D(25) = 90 (exact value by exhaustive search; D is non-decreasing)).

## Submitting and checking

Format: Text file: 50 lines 'x y', one Gaussian integer x + yi per line (lines starting with # are ignored). For the Eisenstein version, run the checker with RING 3 instead of 4.

Score: the diameter, max |h - h'|^2 over the 50 points, an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check gauss-admissible FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_numth.py gauss-admissible 4 50 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/gauss-admissible.txt`.

## References

- J. Maynard, Small gaps between primes, Ann. of Math. 181 (2015) 383-413, arXiv:1311.4600
- D. H. J. Polymath, Variants of the Selberg sieve, and bounded intervals containing many primes, Res. Math. Sci. 1 (2014) 12, arXiv:1407.4897
- A. Castillo, C. Hall, R. J. Lemke Oliver, P. Pollack, L. Thompson, Bounded gaps between primes in number fields and function fields, Proc. AMS 143 (2015) 2841-2856, arXiv:1403.5808
- J. Renze, S. Wagon, B. Wick, The Gaussian zoo, Experimental Mathematics 10 (2001) 161-173
- T. J. Engelsma, k-tuple permissible patterns (tables of H(k) for k <= 342); A. V. Sutherland, narrow admissible tuples (math.mit.edu/~primegaps)
