# Covering all pairs of Z_p by three-term progressions

`ap-cover` · Combinatorics and graph theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **165** (minimize), Quantavane (Arhan Canli), 9 November 2026: greedy covering followed by local search (remove blocks, repair greedily; tools/ap_cover.py)

## Statement

For a prime p, call a three-term arithmetic progression {a, a + d, a + 2d} (mod p, d not 0) a block. Each pair of elements of Z_p lies in exactly three blocks, so the blocks form a 2-(p, 3, 3) design. Let A(p) be the least number of blocks that together contain every pair of Z_p. Determine A(p). The Schonheim bound gives A(p) >= ceil(p ceil((p-1)/2) / 3), and A(p) equals it exactly when the progressions contain a Steiner triple system (a subsystem in which every pair lies in exactly one block). The headline cell is p = 31: find fewer than 165 progressions covering all pairs of Z_31 (the bound is 155).

## Why it is interesting

Covering designs C(v, k, 2), the fewest k-sets covering all pairs of a v-set, are among the most studied tables in design theory (La Jolla Covering Repository), and their cyclic and structured versions model sampling and testing schedules. Restricting the blocks to arithmetic progressions asks how much is lost when every block must be equally spaced, as in periodic schedules on a ring. For p = 7 and 13, where Steiner triple systems exist, no system consists of progressions only: the exact minima 9 and 27 exceed the Steiner values 7 and 26. Whether the progression design of Z_p ever contains a Steiner triple system (p = 19, 31, 37, 43, ... are the candidates) is open, and so is the growth of A(p) beyond the bound.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/ap-cover.json`](../novelty/ap-cover.json) with its address, the time it ran and its first results.

- arXiv API, 1 searches:
  - `all:"arithmetic progressions" AND all:covering AND all:pairs AND all:"cyclic group"`: 0 results
- Web search (general web search), `covering all pairs of Z_n by arithmetic progressions of length k minimum number "arithmetic progressions" covering design pairs cyclic group blocks progressions`: rainbow progressions covering k-subsets (arXiv:1802.03285), covering sets by progressions (NP-hardness); nothing on pair coverings by progressions
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark's covering-design family uses arbitrary blocks; no progression-block entry.

Closest work found, and how this problem differs:
- Covering designs C(v, 3, 2) (Covering Repository): the same covering problem with arbitrary triples; the progression constraint changes the answers (9 versus 7 at p = 7).
- Rainbow progressions covering k-subsets (arXiv:1802.03285) and coverings of sets by progressions: different problems.

Verdict: new. No study of pair coverings (or Steiner triple systems) made of arithmetic progressions in Z_p was found on arXiv or by web search; covering by progressions is studied in other senses (covering sets of integers, rainbow progressions), which are different problems.

## First values

| p | A(p) | Schonheim bound | status |
| --- | --- | --- | --- |
| 5 | 4 | 4 | exact |
| 7 | 9 | 7 | exact |
| 11 | 20 | 19 | exact |
| 13 | 27 | 26 | exact |
| 17 | 46 to 48 | 46 | open (search proved 46 lower bound; ours 48) |
| 19 | <= 59 (ours) | 57 | open |
| 31 | <= 165 (ours) | 155 | open |
| 37 | <= 229 (ours) | 222 | open |

Exact values by depth-first search with iterative deepening (tools/ap_cover.py exact); for p = 17 the search ruled out 45 or fewer before its node limit. Upper bounds for larger p from our local search.

## Best known value

165 for p = 31, held by Quantavane (Arhan Canli), 9 November 2026: the progressions in `refs/ap-cover.txt`. Lower bound 155 (Schonheim); an answer of 155 would be a Steiner triple system made of progressions.

Bound on the other side: 155 (lower bound; Schonheim bound ceil(31 ceil(30/2) / 3)).

## Submitting and checking

Format: Text file: one progression per line, 'a d' (the block {a, a+d, a+2d} mod 31, d not 0).

Score: the number of progressions (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check ap-cover FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comb.py ap-cover 31 3 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/ap-cover.txt`.

## References

- J. Schonheim, On coverings, Pacific J. Math. 14 (1964) 1405-1411
- D. M. Gordon, La Jolla Covering Repository (now the Covering Repository): tables of C(v, k, t)
- C. J. Colbourn, J. H. Dinitz (eds.), Handbook of Combinatorial Designs (2nd ed., CRC 2007): Steiner triple systems and coverings
