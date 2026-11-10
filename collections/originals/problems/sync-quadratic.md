# Shortest reset words of the quadratic automaton modulo p

`sync-quadratic` · Computing and operations research · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **31** (minimize), Quantavane (Arhan Canli), 9 November 2026: a reset word of length 31 found by beam search over subsets (tools/src/syncbeam.c, beam width 50,000)

## Statement

For a prime p let Q_p be the automaton with states 0, 1, ..., p-1 and two letters, a: x -> x + 1 and b: x -> x^2 (mod p). A reset word is a word that sends every state to one and the same state; let r(p) be the length of a shortest reset word. Determine r(p). The headline cell is p = 101, where 25 <= r(101) <= 31: find a reset word of length at most 30, or prove that 31 is optimal.

## Why it is interesting

The Cerny conjecture says that an n-state synchronizing automaton has a reset word of length at most (n-1)^2; it is open in general and proved for several classes, among them circular automata, where one letter permutes the states in a single cycle (Dubuc, RAIRO Theor. Inform. Appl. 32 (1998) 21-34). Q_p is circular (the letter a), so r(p) <= (p-1)^2, but its second letter is the squaring map, whose functional graph modulo p carries the arithmetic of quadratic residues; the exact values below are tiny by comparison (r(101) <= 31 against the bound 10,000) and depend on p in an irregular way (r(17) = 8 and r(97) = 14, while r(47) = 28), so the problem asks how arithmetic controls synchronization. No formula, bound or table for r(p) was found.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/sync-quadratic.json`](../novelty/sync-quadratic.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:synchronizing AND all:automata AND all:quadratic`: 24 results
  - `all:"synchronizing word" AND all:prime AND all:automaton`: 0 results
  - `all:"reset word" AND all:"quadratic map"`: 0 results
  - `all:synchronizing AND all:automaton AND all:"x^2"`: 1 result
- OEIS, 2 searches:
  - `synchronizing quadratic automaton`: 3 results (A141105, A141106, A141107)
  - `3,5,9,12,10,8,16,17,16,21,19,14,24,28,23`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no automaton or reset-word family.

Closest work found, and how this problem differs:
- Dubuc (1998): circular automata satisfy the Cerny bound. That bound applies to Q_p but is far from the values here.

Verdict: new. The automaton x -> x + 1, x -> x^2 (mod p) and its reset thresholds appear in no paper, table or OEIS entry found; the sequence r(3), r(5), ..., r(53) is not in the OEIS.

## First values

| p | r(p) | how |
| --- | --- | --- |
| 3 | 3 | exact (breadth-first search over subsets) |
| 5 | 5 | exact (breadth-first search over subsets) |
| 7 | 9 | exact (breadth-first search over subsets) |
| 11 | 12 | exact (breadth-first search over subsets) |
| 13 | 10 | exact (breadth-first search over subsets) |
| 17 | 8 | exact (breadth-first search over subsets) |
| 19 | 16 | exact (breadth-first search over subsets) |
| 23 | 17 | exact (breadth-first search over subsets) |
| 29 | 16 | exact (breadth-first search over subsets) |
| 31 | 21 | exact (breadth-first search over subsets) |
| 37 | 19 | exact (breadth-first search over subsets) |
| 41 | 14 | exact (breadth-first search over subsets) |
| 43 | 24 | exact (breadth-first search over subsets) |
| 47 | 28 | exact (breadth-first search over subsets) |
| 53 | 23 | exact (breadth-first search over subsets) |
| 59 | <= 34 (ours), >= 26 | open |
| 61 | 21 | exact (breadth-first search over subsets) |
| 67 | <= 38 (ours), >= 25 | open |
| 71 | <= 33 (ours), >= 25 | open |
| 73 | 19 | exact (breadth-first search over subsets) |
| 79 | <= 39 (ours), >= 25 | open |
| 83 | <= 37 (ours), >= 25 | open |
| 89 | 23 | exact (breadth-first search over subsets) |
| 97 | 14 | exact (breadth-first search over subsets) |
| 101 | <= 31 (ours), >= 25 | open |
| 103 | <= 46 (ours), >= 24 | open |
| 107 | <= 47 (ours), >= 24 | open |
| 109 | <= 33 (ours), >= 25 | open |
| 113 | 19 | exact (breadth-first search over subsets) |
| 127 | <= 49 (ours), >= 24 | open |

Exact values: breadth-first search over the subsets of states reached from the full set (tools/src/syncq.c); where that search exceeded 14 million subsets, the depth it completed is a lower bound and our beam search gives the upper bound. Rows improved on 10 November 2026 show the value of the cell (see Cells).

## Best known value

31 for p = 101, held by Quantavane (Arhan Canli), 9 November 2026: the word in `refs/sync-quadratic.txt`. Lower bound 25: the breadth-first search finished every word of length at most 24 without reaching a single state (tools/src/syncq.c).

## Cells

The same question at each value of its parameter (p, a prime): 51 cells, 18 of them exact (an exhaustive search finished) and 33 best known (ours). Each cell has its certificate in `refs/cells/sync-quadratic/` (the headline cell uses `collections/originals/refs/sync-quadratic.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example sync-quadratic-7

| cell | p | value | status |
| --- | --- | --- | --- |
| `sync-quadratic-7` | 7 | 9 | exact |
| `sync-quadratic-11` | 11 | 12 | exact |
| `sync-quadratic-13` | 13 | 10 | exact |
| `sync-quadratic-17` | 17 | 8 | exact |
| `sync-quadratic-19` | 19 | 16 | exact |
| `sync-quadratic-23` | 23 | 17 | exact |
| `sync-quadratic-29` | 29 | 16 | exact |
| `sync-quadratic-31` | 31 | 21 | exact |
| `sync-quadratic-37` | 37 | 19 | exact |
| `sync-quadratic-41` | 41 | 14 | exact |
| `sync-quadratic-43` | 43 | 24 | exact |
| `sync-quadratic-47` | 47 | 28 | exact |
| `sync-quadratic-53` | 53 | 23 | exact |
| `sync-quadratic-59` | 59 | 34 | best known |
| `sync-quadratic-61` | 61 | 21 | exact |
| `sync-quadratic-67` | 67 | 38 | best known |
| `sync-quadratic-71` | 71 | 33 | best known |
| `sync-quadratic-73` | 73 | 19 | exact |
| `sync-quadratic-79` | 79 | 39 | best known |
| `sync-quadratic-83` | 83 | 37 | best known |
| `sync-quadratic-89` | 89 | 23 | exact |
| `sync-quadratic-97` | 97 | 14 | exact |
| `sync-quadratic-101` | 101 | 31 | best known (headline) |
| `sync-quadratic-103` | 103 | 46 | best known |
| `sync-quadratic-107` | 107 | 47 | best known |
| `sync-quadratic-109` | 109 | 33 | best known |
| `sync-quadratic-113` | 113 | 19 | exact |
| `sync-quadratic-127` | 127 | 49 | best known |
| `sync-quadratic-131` | 131 | 48 | best known |
| `sync-quadratic-137` | 137 | 29 | best known |
| `sync-quadratic-139` | 139 | 51 | best known |
| `sync-quadratic-149` | 149 | 42 | best known |
| `sync-quadratic-151` | 151 | 53 | best known |
| `sync-quadratic-157` | 157 | 39 | best known |
| `sync-quadratic-163` | 163 | 59 | best known |
| `sync-quadratic-167` | 167 | 59 | best known |
| `sync-quadratic-173` | 173 | 33 | best known |
| `sync-quadratic-179` | 179 | 62 | best known |
| `sync-quadratic-181` | 181 | 44 | best known |
| `sync-quadratic-191` | 191 | 61 | best known |
| `sync-quadratic-193` | 193 | 20 | best known |
| `sync-quadratic-197` | 197 | 42 | best known |
| `sync-quadratic-199` | 199 | 62 | best known |
| `sync-quadratic-211` | 211 | 68 | best known |
| `sync-quadratic-223` | 223 | 68 | best known |
| `sync-quadratic-227` | 227 | 71 | best known |
| `sync-quadratic-229` | 229 | 50 | best known |
| `sync-quadratic-233` | 233 | 37 | best known |
| `sync-quadratic-239` | 239 | 71 | best known |
| `sync-quadratic-241` | 241 | 32 | best known |
| `sync-quadratic-251` | 251 | 75 | best known |

Exact cells: breadth-first search over the subsets of Z_p reached from Z_p, finished (tools/src/syncq.c). Best known cells: beam search over subsets keeping the 300,000 smallest per level (tools/src/syncbeam.c); an upper bound.

Bound on the other side: 25 (lower bound; exhaustive breadth-first search over all subsets reachable by words of length <= 24).

## Submitting and checking

Format: Text file: a word over the letters a and b (whitespace and lines starting with # are ignored), applied letter by letter from the left.

Score: the length of the word (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check sync-quadratic FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comp.py sync-quadratic 101 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/sync-quadratic.txt`.

## References

- J. Cerny, Poznamka k homogennym experimentom s konecnymi automatmi, Matematicko-fyzikalny casopis 14 (1964) 208-216
- L. Dubuc, Sur les automates circulaires et la conjecture de Cerny, RAIRO Theoretical Informatics and Applications 32 (1998) 21-34
