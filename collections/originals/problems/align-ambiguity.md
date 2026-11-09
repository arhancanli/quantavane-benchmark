# The most ambiguous pair of DNA sequences

`align-ambiguity` · Biology · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **917147** (maximize), Quantavane (Arhan Canli), 9 November 2026: local search on pairs (change one letter, keep the change when the count does not fall, with a small chance of accepting a worse pair), 60 seconds (tools/src/alignamb.c)

## Statement

Two DNA sequences x and y of length n over A, C, G, T are aligned globally with unit costs: a mismatch costs 1, a gap (one letter inserted or deleted) costs 1, a match costs 0. An alignment is a path from (0, 0) to (n, n) in the edit graph with diagonal, horizontal and vertical steps, and the optimal alignments are the paths of least total cost (the edit distance). Let A(n) be the largest number of optimal alignments of a pair of sequences of length n. We find A(n) exactly for n <= 7 (1, 3, 5, 12, 24, 53, 114). The headline cell is n = 20: find a pair of DNA sequences of length 20 with more than 917,147 optimal alignments (ours).

## Why it is interesting

Alignments underlie almost every comparison of biological sequences, and when several alignments have the same optimal score the one a program reports is an arbitrary choice: the positions of gaps, and the mutations and indels read off them, can change from one co-optimal alignment to another. Counting the co-optimal alignments of two given sequences is a textbook dynamic program (Gusfield 1997; the Rosalind exercise 'Counting optimal alignments'). How ambiguous can it get? For the longest common subsequence, Greenberg (2003) bounded the number of optimal embeddings and of distinct common subsequences, and for parametric alignment the number of distinct optimal alignment summaries is of order n^(2/3) (Gusfield et al.; Vinzant). Here the scoring is fixed (unit edit costs), the alphabet is DNA, and the question is the pair with the most optimal alignments. The exact values grow roughly by a factor of two per letter: A(7) = 114. The first six values 1, 3, 5, 12, 24, 53 coincide with OEIS A026786 (the middle column of a path-counting triangle of Kimberling), but the next term there is 117, not 114, so the coincidence ends. The growth rate of A(n) and the shape of the extremal pairs are open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/align-ambiguity.json`](../novelty/align-ambiguity.json) with its address, the time it ran and its first results.

- arXiv API, 8 searches:
  - `all:"number of optimal alignments"`: 0 results
  - `all:"co-optimal alignments"`: 0 results
  - `all:"optimal alignments" AND all:"edit distance" AND all:number AND all:maximum`: 1 result
  - `all:"co-optimal" AND all:alignment AND all:number`: 3 results
  - `all:"number of optimal alignments" AND all:sequences`: 0 results
  - `all:"optimal alignments" AND all:"maximum number"`: 2 results
  - `all:"optimal alignments" AND all:"number of" AND all:"edit distance"`: 1 result
  - `all:"longest common subsequences" AND all:"number of" AND all:bounds`: 16 results
- OEIS, 4 searches:
  - `number of optimal alignments`: 10 results (A124484, A374505, A000629, A227133, A225227)
  - `1,3,5,12,24,53`: 2 results (A026786, A027246)
  - `3,5,12,24,53`: 2 results (A026786, A027246)
  - `number of optimal alignments maximum`: 6 results (A124484, A374505, A227133, A371154, A000292)
- Web search (general web search), `maximum number of co-optimal alignments two sequences length n edit distance worst case number of optimal alignment paths`: Vinzant's lower bounds for parametric alignment summaries, Greenberg's bounds on the number of LCS, the Rosalind exercise on counting optimal alignments; no maximum over pairs for unit edit costs
- Web search (OEIS entry (read)), `A026786`: a(n) = T(n, floor(n/2)) for Kimberling's triangle A026780 (T(n,k) = T(n-1,k-1) + T(n-2,k-1) + T(n-1,k) for k <= n/2): 1, 1, 3, 5, 12, 24, 53, 117, 246, ...; no alignments; differs from A(7) = 114
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no alignment family in the benchmark.

Closest work found, and how this problem differs:
- R. I. Greenberg (2003): the largest number of longest-common-subsequence embeddings and of distinct LCS strings (indels only, no substitutions); here substitutions cost 1 as well.
- Parametric alignment (Gusfield et al.; Vinzant): the number of distinct optimal alignment summaries as the scores vary, not the number of optimal paths for one scoring.
- OEIS A026786 and A027246 (Kimberling's triangle A026780): agree with our values 1, 3, 5, 12, 24, 53 and then give 117, where A(7) = 114.

Verdict: new question: counting the optimal alignments of given sequences is standard, but no result was found on the pair of sequences of a given length with the most optimal alignments under unit costs. Our first values match an unrelated OEIS sequence for six terms and differ at the seventh.

## First values

| n | most optimal alignments A(n) | an extremal pair x / y | how |
| --- | --- | --- | --- |
| 1 | 1 | A / A | exact (every pair) |
| 2 | 3 | AC / CA | exact (every pair) |
| 3 | 5 | ACC / CAA | exact (every pair) |
| 4 | 12 | ACGA / GAAC | exact (every pair) |
| 5 | 24 | ACCGG / CGACA | exact (every pair) |
| 6 | 53 | ACCGGT / CGTACG | exact (every pair) |
| 7 | 114 | ACCGGTT / CGTACGA | exact (every pair) |
| 8 | 249 | ACTAGCTG / GGCCTTAA | best known (ours, local search) |
| 10 | 1081 | AAGGGCCCTT / TGCCTAGGCA | best known (ours, local search) |
| 12 | 4334 | TTGGGCCCCAAA / CGCCAATGGCCG | best known (ours, local search) |
| 16 | 50253 | AAGCCCCCCTTGGTTG / TTCTTTGGGGCCACCT | best known (ours, local search) |
| 20 | 917147 | TCGCTTCCAGAAAAACAGCG / AAAGGGGTTTTCCCTGGTTT | best known (ours, local search) |

Exact values by trying every pair (x with its letters in order of first appearance; tools/src/alignamb.c, mode exact). Larger n: local search, lower bounds only.

## Best known value

917,147 optimal alignments, held by Quantavane (Arhan Canli), 9 November 2026: the pair in `refs/align-ambiguity.txt` (TCGCTTCCAGAAAAACAGCG / AAAGGGGTTTTCCCTGGTTT).

## Submitting and checking

Format: Text file: two lines, the DNA sequences x and y, each of 20 letters A, C, G, T.

Score: the number of optimal alignments, an integer (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check align-ambiguity FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_bio.py align-ambiguity 20 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/align-ambiguity.txt`.

## References

- S. B. Needleman, C. D. Wunsch, A general method applicable to the search for similarities in the amino acid sequence of two proteins, J. Mol. Biol. 48 (1970) 443-453
- D. Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press (1997)
- R. I. Greenberg, Bounds on the number of longest common subsequences, arXiv:cs/0301030 (2003)
- C. Vinzant, Lower bounds for optimal alignments of binary sequences, arXiv:0807.0051
- Rosalind, Counting optimal alignments (problem CTEA), https://rosalind.info/problems/ctea/
