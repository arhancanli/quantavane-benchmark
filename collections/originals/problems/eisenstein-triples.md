# Two-colourings with no monochromatic 120-degree triangle

`eisenstein-triples` · Number theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **19200** (maximize), Quantavane (Arhan Canli), 9 November 2026: a focused random walk on the triples (pick a monochromatic triple, flip the member that breaks the fewest others, or a random member with probability 0.4), extending n by 100 while a valid colouring is found within 240 seconds (tools/src/eiswalk.c)

## Statement

An Eisenstein triple is a triple of positive integers x < y, z with x^2 + xy + y^2 = z^2: the side lengths of a triangle with an angle of 120 degrees opposite z (the smallest are (3, 5, 7), (7, 8, 13) and (5, 16, 19)). Colour the integers 1, 2, ..., n with two colours. What is the largest n for which some colouring has no monochromatic Eisenstein triple, that is, no triple with x, y and z all of the same colour? We do not know whether this n is finite. For Pythagorean triples x^2 + y^2 = z^2 the answer is 7824 (Heule, Kullmann and Marek 2016). The headline cell: give a valid colouring of 1..n for some n > 19,200.

## Why it is interesting

The Boolean Pythagorean triples problem asked whether the positive integers can be split into two parts with no Pythagorean triple inside a part; Heule, Kullmann and Marek (2016) proved with a SAT solver that 1..7824 can be split and 1..7825 cannot, and Leng (2026) gave a new proof, without an explicit bound, that every two-colouring of the natural numbers has a monochromatic Pythagorean triple. Eisenstein triples play the same role for the norm form x^2 + xy + y^2 of the Eisenstein integers that Pythagorean triples play for the Gaussian norm x^2 + y^2: they are the integer triangles with a 120-degree angle, and they are about as dense (7,839 triples with z <= 7825, against 9,472 Pythagorean triples with c <= 7825). Yet the two problems behave differently. Our local search finds two-colourings of 1..19,200 avoiding monochromatic Eisenstein triples (21,624 triples) and stalls only above that, while the same program run on Pythagorean triples stops at 6,800, below the true answer 7,824 there (it had 60 s per step instead of 240 s; earlier computer searches had reached 7664 before the SAT proof). So the 120-degree threshold, if there is one, is more than twice the Pythagorean one. Whether the threshold is finite (two-colour partition regularity of x^2 + xy + y^2 = z^2) is not settled in anything we found; the exact threshold would need a SAT computation of the cube-and-conquer kind, and a two-colouring of all positive integers would settle the problem the other way.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/eisenstein-triples.json`](../novelty/eisenstein-triples.json) with its address, the time it ran and its first results.

- arXiv API, 8 searches:
  - `all:"Pythagorean triples" AND all:coloring AND all:Eisenstein`: 0 results
  - `all:"Boolean Pythagorean triples"`: 3 results
  - `all:"Eisenstein triples"`: 0 results
  - `all:monochromatic AND all:"Pythagorean" AND all:"120 degrees"`: 0 results
  - `all:"x^2+xy+y^2" AND all:coloring`: 0 results
  - `all:"partition regular" AND all:"quadratic" AND all:"Pythagorean"`: 1 result
  - `all:"120 degree" AND all:triangles AND all:integer AND all:coloring`: 0 results
  - `all:"Pythagorean triples" AND all:"two colors" AND all:monochromatic`: 2 results
- OEIS, 4 searches:
  - `Eisenstein triples`: 10 results (A121992, A201223, A264826, A242039, A335893)
  - `Pythagorean triples 2-coloring`: 6 results (A383181, A272709, A250026, A000984, A004526)
  - `triangles 120 degrees 2-coloring`: 6 results (A000295, A000031, A001700, A011782, A004526)
  - `x^2+xy+y^2=z^2 coloring`: 0 results
- Web search (general web search), `2-coloring monochromatic "x^2+xy+y^2=z^2" OR "Eisenstein triples" Ramsey OR "Rado number" OR "Boolean"`: the Boolean Pythagorean triples results (7825), monochromatic solutions of x + y = z^2 (Green and Lindqvist), generalized Schur triples; nothing on x^2 + xy + y^2 = z^2
- Web search (general web search), `"partition regular" OR "monochromatic" "x^2 + xy + y^2 = z^2" triangles 120 degrees integer sides coloring`: morphic colourings and Pythagorean triples (Eliahou et al.), x + y = z^2; nothing on the 120-degree equation
- Web search (arXiv abstract and full text (read)), `arXiv:2609.34676 (J. Leng)`: a new proof of two-colour partition regularity of Pythagorean triples; no explicit bound, no other equation treated (Frantzikinakis-Host and Frantzikinakis-Mountakis cited for other quadratic equations)
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no Ramsey-type colouring family in the benchmark.

Closest work found, and how this problem differs:
- M. J. H. Heule, O. Kullmann and V. W. Marek (2016): the same question for x^2 + y^2 = z^2 (answer 7824); J. Leng (2026): a new proof that the Pythagorean version is finite, with no bound and no other equation.
- Partition-regularity results for homogeneous quadratic equations (Frantzikinakis and Host, as cited by Leng) concern other equations and infinite colourings; no explicit thresholds.
- OEIS A121992, A264826: lists of Eisenstein triples, without any colouring question.

Verdict: new question: the Pythagorean version is solved (7824); no result was found on two-colourings avoiding monochromatic triples x^2 + xy + y^2 = z^2, finite or infinite.

## First values

| n | Eisenstein triples with z <= n | Pythagorean triples with c <= n | two-colouring of 1..n with no monochromatic Eisenstein triple |
| --- | --- | --- | --- |
| 1000 | 719 | 881 | found (ours) |
| 5000 | 4703 | 5681 | found (ours) |
| 7825 | 7839 | 9472 | found (ours); none exists for Pythagorean triples |
| 10000 | 10374 | 12471 | found (ours) |
| 15000 | 16386 |  | found (ours) |
| 17500 | 19489 |  | found (ours) |
| 19200 | 21624 |  | found (ours), the best known |

Triples counted by the checker's exact enumeration (factorisations of 3x^2) and cross-checked against a direct search; colourings found by tools/src/eiswalk.c. At n = 19,300 the search stopped with 5 monochromatic triples after 240 s. Control: the same program on Pythagorean triples (x^2 + y^2 = z^2, 60 s per step) reaches 6,800 and stops at 6,900.

## Best known value

n = 19,200, held by Quantavane (Arhan Canli), 9 November 2026: the colouring in `refs/eisenstein-triples.txt` (no monochromatic triple among the 21,624 Eisenstein triples with z <= 19,200). No upper bound is known.

## Submitting and checking

Format: Text file: the colours of 1, 2, ..., n as characters 0 and 1, in order (line breaks and lines starting with # are ignored).

Score: n, the length of the colouring (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check eisenstein-triples FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_numth.py eisenstein-triples FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/eisenstein-triples.txt`.

## References

- M. J. H. Heule, O. Kullmann, V. W. Marek, Solving and verifying the Boolean Pythagorean triples problem via cube-and-conquer, SAT 2016, Lecture Notes in Comput. Sci. 9710 (2016) 228-245 (arXiv:1605.00723)
- J. Leng, A new proof of two-color partition regularity of Pythagorean triples, arXiv:2609.34676 (2026)
- S. Eliahou, J. Fromentin, V. Marion-Poty, D. Robilliard, Are monochromatic Pythagorean triples unavoidable under morphic colorings?, arXiv:1605.00859 (2016)
- N. Frantzikinakis, B. Host, Higher order Fourier analysis of multiplicative functions and applications, J. Amer. Math. Soc. 30 (2017) 67-157
- OEIS A121992 and A264826: lists of Eisenstein triples
