# The most ambiguous RNA under base-pair maximization

`nussinov-degeneracy` · Biology · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **100603** (maximize), Quantavane (Arhan Canli), 9 November 2026: the sequence UUUUUUGGCAUCGGGAAAAAAAAAGGGAGA (7 pairs, 100,603 optimal structures), found by simulated annealing over sequences (tools/src/nussdeg.c)

## Statement

In the base-pair maximization (Nussinov) model an RNA sequence over A, C, G, U folds into a secondary structure: a set of base pairs from {AU, UA, GC, CG, GU, UG}, each base in at most one pair, every pair (i, j) with j - i >= 4 (a hairpin loop of at least three bases), and no two pairs crossing (i < k < j < l). The predicted structures are those with the largest number of pairs. Let N(s) be the number of such optimal structures of the sequence s and D(n) the largest N(s) over sequences of length n. Determine D(n); the headline cell is n = 30: find a sequence of length 30 with more than 100,603 optimal structures.

## Why it is interesting

Base-pair maximization (Nussinov and Jacobson, PNAS 1980) is the simplest RNA folding model and the core of the dynamic programs behind energy-based prediction; its optimum is often far from unique, and the number of co-optimal and suboptimal structures is how prediction ambiguity is measured (Wuchty, Fontana, Hofacker and Schuster, Biopolymers 1999). The total number of secondary structures of a length-n chain grows exponentially (Stein and Waterman 1979); D(n) asks how much of that can be concentrated on the optimum by one sequence, a worst case for structure prediction. The exact first values below grow quickly (D(13) = 63) and the best sequences found mix G-U wobble stretches with A-U and G-C blocks, but neither the growth rate of D(n) nor the shape of the extremal sequences is known.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/nussinov-degeneracy.json`](../novelty/nussinov-degeneracy.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:Nussinov AND all:degeneracy`: 9 results
  - `all:"base pair maximization" AND all:"optimal structures"`: 0 results
  - `all:"number of optimal" AND all:"secondary structures" AND all:"base pairs"`: 0 results
  - `all:"maximum number" AND all:"optimal secondary structures"`: 0 results
- OEIS, 1 searches:
  - `1,1,1,1,1,3,5,7,13,22,27,48,63`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no RNA family.

Closest work found, and how this problem differs:
- Counting of all secondary structures (Stein-Waterman numbers) and suboptimal-structure enumeration for given sequences; neither maximizes the number of optimal structures over sequences.

Verdict: new. No paper, table or OEIS entry was found for the largest number of co-optimal structures under base-pair maximization; the exact sequence D(1), ..., D(13) is not in the OEIS.

## First values

| n | D(n) | how |
| --- | --- | --- |
| 1 | 1 | exact (all 4^n sequences) |
| 2 | 1 | exact (all 4^n sequences) |
| 3 | 1 | exact (all 4^n sequences) |
| 4 | 1 | exact (all 4^n sequences) |
| 5 | 1 | exact (all 4^n sequences) |
| 6 | 3 | exact (all 4^n sequences) |
| 7 | 5 | exact (all 4^n sequences) |
| 8 | 7 | exact (all 4^n sequences) |
| 9 | 13 | exact (all 4^n sequences) |
| 10 | 22 | exact (all 4^n sequences) |
| 11 | 27 | exact (all 4^n sequences) |
| 12 | 48 | exact (all 4^n sequences) |
| 13 | 63 | exact (all 4^n sequences) |
| 16 | 247 | best known (ours) |
| 20 | 1368 | best known (ours) |
| 25 | 10310 | best known (ours) |
| 30 | 100603 | best known (ours) |

Exact values: every sequence of length n (tools/src/nussdeg.c exhaustive). Best known values: simulated annealing over sequences, 60 s each. Trivial upper bound: the number of all secondary structures on n bases (568 for n = 13, 240,944,076 for n = 30).

## Best known value

100,603 for n = 30, held by Quantavane (Arhan Canli), 9 November 2026: the sequence in `refs/nussinov-degeneracy.txt`. Upper bound 240,944,076, the number of all secondary structures of a 30-base chain with hairpins of at least 3 bases.

Bound on the other side: 240944076 (upper bound (trivial); all secondary structures on 30 bases with hairpin loops of at least 3).

## Submitting and checking

Format: Text file: an RNA sequence of length 30 over A, C, G, U (whitespace and lines starting with # are ignored).

Score: the number N(s) of structures with the maximum number of base pairs, computed exactly by the checker (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check nussinov-degeneracy FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_bio.py nussinov-degeneracy 30 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/nussinov-degeneracy.txt`.

## References

- R. Nussinov, A. B. Jacobson, Fast algorithm for predicting the secondary structure of single-stranded RNA, PNAS 77 (1980) 6309-6313
- P. R. Stein, M. S. Waterman, On some new sequences generalizing the Catalan and Motzkin numbers, Discrete Math. 26 (1979) 261-272
- S. Wuchty, W. Fontana, I. L. Hofacker, P. Schuster, Complete suboptimal folding of RNA and the stability of secondary structures, Biopolymers 49 (1999) 145-165
