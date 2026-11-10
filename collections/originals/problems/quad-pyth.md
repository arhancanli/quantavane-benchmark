# Colourings with no monochromatic Pythagorean quadruple

`quad-pyth` · Number theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **473** (maximize), Quantavane (Arhan Canli), 10 November 2026: a 3-colouring of 1..473 with no monochromatic quadruple, found by an incremental SAT search (CaDiCaL through python-sat; tools/colour_sat.py)

## Statement

A Pythagorean quadruple is a solution of x^2 + y^2 + z^2 = w^2 in positive integers (the edges and the space diagonal of a box with integer sides; the smallest is 1^2 + 2^2 + 2^2 = 3^2, and x, y, z may repeat). Colour the integers 1, 2, ..., n with K colours. What is the largest n for which some colouring has no monochromatic quadruple, i.e. no solution with x, y, z and w all of the same colour? For K = 2 the answer is 104 (ours, exact: every 2-colouring of 1..105 has one). The headline cell is K = 3: we have a colouring of 1..473; find a 3-colouring of 1..474 or more, or prove that none exists. We do not know whether the answer for K = 3 is finite.

## Why it is interesting

Erdos and Graham asked whether every finite colouring of the positive integers has a monochromatic Pythagorean triple; for two colours Heule, Kullmann and Marek (2016) found the threshold 7825 with a 200-terabyte proof, and the question for more colours is open. Frantzikinakis, Klurman and Moreira proved that every finite colouring has a monochromatic Pythagorean pair (x and y with x^2 + y^2 or x^2 - y^2 a square), and Chow, Lindqvist and Prendiville settled diagonal quadratic equations in five or more variables (so x1^2 + x2^2 + x3^2 + x4^2 = x5^2 is partition regular). Pythagorean quadruples, with four variables, fall between the two: our exact value for two colours (104) shows that two colours do not suffice, but whether every 3-colouring of a long enough interval contains a monochromatic quadruple is open, and the threshold, if finite, is unknown.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/quad-pyth.json`](../novelty/quad-pyth.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"Pythagorean quadruples" AND all:colouring`: 0 results
  - `all:"Pythagorean quadruples" AND all:coloring`: 0 results
  - `all:"Pythagorean quadruples" AND all:monochromatic`: 1 result
- OEIS, 2 searches:
  - `Pythagorean quadruples coloring`: 1 result (A169580)
  - `monochromatic Pythagorean`: 4 results (A383181, A272709, A401469, A250026)
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `monochromatic Pythagorean quadruples colouring`: first results "Proof Without Words: Pythagorean Quadruples" (2014); "Right tetrahedra, Pythagorean quadruples, and Fibonacci numbers" (2026); "The homothetical-Hopf transformation of Pythagorean quadruples" (2026)
- Web search (general web search), `"partition regular" "x^2+y^2+z^2=w^2" OR "Pythagorean quadruples" monochromatic coloring Ramsey`: Pythagorean triples (Heule-Kullmann-Marek 7825; Erdos-Graham's question open), Frantzikinakis-Klurman-Moreira on Pythagorean pairs, and partition regularity of x1^2 + x2^2 + x3^2 + x4^2 = x5^2 (five variables, arXiv:2501.17203); nothing on x^2 + y^2 + z^2 = w^2 or on colouring thresholds for it
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no colouring family for Diophantine equations other than our eisenstein-triples.

Closest work found, and how this problem differs:
- The Boolean Pythagorean triples problem (Heule, Kullmann and Marek 2016): the same question for x^2 + y^2 = z^2, threshold 7825 for two colours.
- Monochromatic almost-Pythagorean quadruples x^2 + y^2 w^2 = z^2 in multiplicatively dense sets (arXiv:2610.04078): a different equation and a density question.

Verdict: new. Partition regularity is known for five or more squares (Chow, Lindqvist and Prendiville) and studied for Pythagorean triples and pairs; no colouring threshold, finite or infinite, was found for Pythagorean quadruples (arXiv, Crossref and web searches).

## Best known value

473 for K = 3, held by Quantavane (Arhan Canli), 10 November 2026: the colouring in `refs/quad-pyth.txt` (incremental SAT search, tools/colour_sat.py). K = 2: exactly 104 (the SAT solver finds 1..104 colourable and proves 1..105 not; CaDiCaL, Glucose and MiniSat agree, tools/colour_exact.py).

## Cells

The same question at each value of its parameter (K, the number of colours): 2 cells, 1 of them exact (an exhaustive search finished) and 1 best known (ours). Each cell has its certificate in `refs/cells/quad-pyth/` (the headline cell uses `collections/originals/refs/quad-pyth.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example quad-pyth-2

| cell | K | value | status |
| --- | --- | --- | --- |
| `quad-pyth-2` | 2 | 104 | exact |
| `quad-pyth-3` | 3 | 473 | best known (headline) |

Exact cells: an incremental SAT search (CaDiCaL 1.9.5 through python-sat; tools/colour_sat.py) colours 1..n and proves 1..n+1 impossible; three solvers (CaDiCaL, Glucose, MiniSat) agree on the formula built from the checker's list of quadruples (tools/colour_exact.py). Best known cells: the longest colouring an incremental SAT search found in 300 seconds (tools/colour_sat.py).

## Submitting and checking

Format: Text file: the colours of 1, 2, ..., n as digits 0, 1, 2, in order (line breaks and lines starting with # are ignored).

Score: n, the length of the colouring (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check quad-pyth FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_colour.py quad-pyth 3 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/quad-pyth.txt`.

## References

- M. J. H. Heule, O. Kullmann, V. W. Marek, Solving and verifying the Boolean Pythagorean triples problem via cube-and-conquer, SAT 2016, LNCS 9710 (2016) 228-245
- N. Frantzikinakis, O. Klurman, J. Moreira, Partition regularity of Pythagorean pairs, arXiv:2309.10636
- S. Chow, S. Lindqvist, S. Prendiville, Rado's criterion over squares and higher powers, J. Eur. Math. Soc. (2021)
