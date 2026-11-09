# An optimal strategy for Primel

`primel` · Computing and operations research · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **29016** (minimize), Quantavane (Arhan Canli), 9 November 2026: a strategy tree built top down; at each node the 12, 6 and 3 best guesses (by the sum of |C| log |C| over the mark classes C) are tried at depths 0, 1 and 2, each with its whole subtree, and sets of at most 3 answers are solved exactly (tools/src/primel.c)

## Statement

Primel is Wordle played with five-digit primes: the hidden answer is one of the 8,363 primes from 10007 to 99991, every guess must be one of these primes too, and after each guess every digit is marked green (the right digit in the right place), yellow (the digit occurs elsewhere in the answer) or grey, with Wordle's rule for repeated digits (greens first, then yellows for the answer's unmatched digits, left to right). A strategy chooses each guess from the marks seen so far. Find a strategy that solves every answer within six guesses and uses the fewest guesses in total over all 8,363 answers (the smallest average number of guesses). Best known: 29,016 guesses, an average of 3.469568 (ours); every strategy needs at least 24,866.

## Why it is interesting

Wordle and Mastermind are the standard small cases of adaptive search with structured feedback: Knuth (1976) found a Mastermind strategy that always wins in five guesses, Koyama and Lai (1993) the one with the smallest average, and the best Wordle strategy was found by exhaustive search (A. Selby, 2022; Bertsimas and Paskov, Operations Research), with an average of 3.421 guesses over its 2,315 answers. Primel replaces the words by the 8,363 five-digit primes and allows only primes as guesses. Its answer set is more than three times larger, and its structure comes from arithmetic: the last digit is 1, 3, 7 or 9, the digit sum is never a multiple of 3, and how often each digit occurs in each place follows the distribution of primes. The best first guesses split the primes into at most 221 mark classes, which gives the lower bound 24,866 (one answer can be found at the first guess, at most 221 at the second, all others need at least three); the best strategy found needs 29,016. Closing the gap needs the exact methods used for Wordle on an answer set more than three times larger.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/primel.json`](../novelty/primel.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:Primel AND all:Wordle`: 0 results
  - `all:Wordle AND all:"prime numbers"`: 0 results
- Web search (general web search), `Primel prime number wordle optimal strategy solver decision tree average guesses`: an entropy-based Primel solver project (8,363 answers, no average given), a filtering script, and the exact Wordle solution (Bertsimas and Paskov; average 3.421 with SALET); no optimal or published Primel strategy value
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no Wordle- or Mastermind-type family in the benchmark.

Closest work found, and how this problem differs:
- Wordle: the optimal strategy (average 3.421 over 2,315 answers) found by exhaustive search (Selby; Bertsimas and Paskov). Same feedback rules, different answer set (words), and the dictionary of allowed guesses differs.
- An entropy-based Primel solver (a student project found by our web search) and a filtering script: no strategy value published.

Verdict: new question for this game: exact strategies are known for Wordle and Mastermind, games with other answer sets; for Primel only heuristic solvers without published values were found.

## Best known value

29,016 guesses (average 3.469568; 1 answer in one guess, 58 in two, 4,347 in three, 3,927 in four, 30 in five), held by Quantavane (Arhan Canli), 9 November 2026: the strategy in `refs/primel.txt`. Lower bound 24,866 (average 2.9733): no first guess splits the primes into more than 221 mark classes besides the all-green one.

Bound on the other side: 24866 (lower bound; 1 + 2 x 221 + 3 x (8,362 - 221): the most mark classes of any first guess is 221 (computed over all 8,363 primes), and each class can solve at most one answer at the second guess).

## Submitting and checking

Format: Text file: one line per answer, the five-digit primes guessed for it in order, the last being the answer itself; the lines must form one strategy (the same marks so far always lead to the same next guess).

Score: the total number of guesses over the 8,363 answers, an integer (smaller is better; divide by 8,363 for the average). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check primel FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comp.py primel FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/primel.txt`.

## References

- D. E. Knuth, The computer as master mind, J. Recreational Math. 9 (1976-77) 1-6
- K. Koyama, T. W. Lai, An optimal Mastermind strategy, J. Recreational Math. 25 (1993) 251-256
- D. Bertsimas, A. Paskov, An exact and interpretable solution to Wordle, Operations Research (2024), doi:10.1287/opre.2022.0434
- A. Selby, The best strategies for Wordle (2022), https://sonorouschocolate.com/notes/index.php/The_best_strategies_for_Wordle
