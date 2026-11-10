# Two-colourings with no monochromatic three squares in arithmetic progression

`squares-ap` · Number theory · status: **open** · added 10 November 2026 (Quantavane Originals)

Best known value: **22948** (maximize), Quantavane (Arhan Canli), 10 November 2026: a 2-colouring of 1..22948 with no monochromatic solution, found by an incremental SAT search (CaDiCaL through python-sat; tools/colour_sat.py)

## Statement

The squares x^2 < z^2 < y^2 are in arithmetic progression when x^2 + y^2 = 2z^2 (the smallest is 1, 25, 49). Colour the integers 1, 2, ..., n with two colours. What is the largest n for which some colouring has no monochromatic progression, i.e. no solution with x, z and y all of the same colour? We have a colouring of 1..22948; the headline cell asks for a 2-colouring of 1..22949 or more, or a proof that none exists. We do not know whether the answer is finite.

## Why it is interesting

Three squares in arithmetic progression are classical (four are impossible, as Fermat claimed and Euler proved; the common differences are congruent numbers times squares), and x^2 + y^2 = 2z^2 is the Pythagorean equation in disguise: u = (y + x)/2, v = (y - x)/2 give u^2 + v^2 = z^2. So this is the Boolean Pythagorean triples question (Heule, Kullmann and Marek 2016: 7825 for two colours) asked for the triples (u - v, z, u + v) instead of (u, v, z); whether every 2-colouring of the integers has a monochromatic one is open, as is the partition regularity of x^2 + y^2 = 2z^2 (Rado-type criteria for squares need five or more variables). Our SAT search slowed sharply near 22948, which suggests, without proving, a finite threshold close by.

## Novelty check

Checked 10 November 2026, before the problem was added. Every search below is in [`novelty/squares-ap.json`](../novelty/squares-ap.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"x^2+y^2=2z^2" AND all:monochromatic`: 0 results
  - `all:"squares in arithmetic progression" AND all:colouring`: 0 results
  - `all:"three squares" AND all:"arithmetic progression" AND all:monochromatic`: 0 results
- OEIS, 2 searches:
  - `squares arithmetic progression coloring`: 10 results (A124882, A306717, A002620, A308776, A401735)
  - `monochromatic x^2+y^2=2z^2`: 0 results
- Crossref (the journal literature, ranked by relevance), 1 search:
  - `partition regularity x^2+y^2=2z^2`: first results "Partition Entropy as a Measure of Regularity of Music Scales" (2024); "15 Partition Regularity of Matrices" (1998); "Chapter 15. Partition Regularity of Matrices" (2011)
- Web search (general web search), `partition regularity "x^2 - xy + y^2 = z^2" OR "x^2+y^2=2z^2" monochromatic solutions two colourings Frantzikinakis Host`: Frantzikinakis-Host: x^2 - xy + y^2 = z^2 is partition regular in x and y (z of any colour); Frantzikinakis-Klurman-Moreira on Pythagorean pairs; nothing on x^2 + y^2 = 2z^2 or on finite colouring thresholds
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no colouring family for Diophantine equations other than our eisenstein-triples.

Closest work found, and how this problem differs:
- The Boolean Pythagorean triples problem (Heule, Kullmann and Marek 2016): colour the triples (u, v, z) of the same Pythagorean triples; here the triples (u - v, z, u + v) are coloured.
- Our eisenstein-triples: the same question for 120-degree triangles x^2 + xy + y^2 = z^2.

Verdict: new. Partition regularity results cover Pythagorean pairs and five or more squares; no colouring threshold for x^2 + y^2 = 2z^2 was found (arXiv, Crossref and web searches).

## Best known value

22948, held by Quantavane (Arhan Canli), 10 November 2026: the colouring in `refs/squares-ap.txt` (incremental SAT search, tools/colour_sat.py). No upper bound is known.

## Submitting and checking

Format: Text file: the colours of 1, 2, ..., n as characters 0 and 1, in order (line breaks and lines starting with # are ignored).

Score: n, the length of the colouring (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check squares-ap FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_colour.py squares-ap 2 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/squares-ap.txt`.

## References

- M. J. H. Heule, O. Kullmann, V. W. Marek, Solving and verifying the Boolean Pythagorean triples problem via cube-and-conquer, SAT 2016, LNCS 9710 (2016) 228-245
- S. Chow, S. Lindqvist, S. Prendiville, Rado's criterion over squares and higher powers, J. Eur. Math. Soc. (2021)
- K. Conrad, Arithmetic progressions of three squares (expository notes)
