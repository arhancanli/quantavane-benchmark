# The image of the symmetrization of almost symmetric numerical semigroups

`symmetrization-image` · Number theory · status: **open** · added 15 November 2026 (Quantavane Originals)

Best known value: **1016** (maximize), Quantavane (Arhan Canli), 15 November 2026: 1016 images with Frobenius number 43, one preimage each, from every almost symmetric numerical semigroup with Frobenius number at most 67 (tools/symmetrization_image.py)

## Statement

A numerical semigroup S is a set of non-negative integers that contains 0, is closed under addition and has finite complement; its Frobenius number F(S) is its largest gap, its pseudo-Frobenius numbers PF(S) are the gaps x with x + s in S for every positive s in S, t(S) = |PF(S)| is its type, and S is almost symmetric when every gap x has F(S) - x in S, or x and F(S) - x both in PF(S). A numerical set (a set of non-negative integers containing 0, with finite complement) is symmetric with Frobenius number G when exactly one of a and G - a belongs to it for every a in [0, G]. Write the positions 0, 1, ..., F(S) as a word, E at the elements of S and N at its gaps. The symmetrization Phi(S) of Delgado, Suer and Yesil is the numerical set whose word is obtained by deleting the letters at the pseudo-Frobenius numbers other than F(S) (every integer past the shortened word belongs to it); it is symmetric, with Frobenius number G = F(S) - t(S) + 1. For odd G let I(G) be the number of symmetric numerical sets with Frobenius number G that equal Phi(S) for some almost symmetric numerical semigroup S. Determine I(G). The headline cell is G = 43: find more than 1016 such sets (each with a preimage), or prove that there are no others.

## Why it is interesting

Almost symmetric numerical semigroups were introduced by Barucci and Froberg as the semigroup case of almost Gorenstein rings; Nari showed that S is almost symmetric exactly when 2 g(S) = F(S) + t(S), g(S) the number of gaps, and that the pseudo-Frobenius numbers below F(S) are symmetric about F(S)/2. Numerical sets correspond to Young diagrams through their words, the setting of Yesil's decompositions (2025). Delgado, Suer and Yesil (2026) delete from the Young diagram of S the rows of its pseudo-Frobenius numbers below F(S) and obtain a symmetric numerical set, and they asked whether every symmetric numerical set arises this way. Every symmetric numerical semigroup with Frobenius number G is its own image (type 1), so I(G) is at least the number of symmetric numerical semigroups with Frobenius number G, and at most the 2^((G-1)/2) symmetric numerical sets. The counts below show that Phi is not onto for G >= 3 (1 of 2 sets at G = 3, 770 of 1,048,576 at G = 41) and that the image is a small, irregular part of the symmetric sets: how fast I(G) grows, and which sets of multiplicity 4 or more are images, is open.

## Novelty check

Checked 15 November 2026, before the problem was added. Every search below is in [`novelty/symmetrization-image.json`](../novelty/symmetrization-image.json) with its address, the time it ran and its first results.

- arXiv API, 4 searches:
  - `all:symmetrization AND all:"numerical semigroups"`: 83 results
  - `all:"almost symmetric" AND all:"numerical sets"`: 2 results
  - `all:"symmetric numerical sets"`: 2 results
  - `all:"almost symmetric numerical semigroups" AND all:"Young diagram"`: 2 results
- OEIS, 4 searches:
  - `1,1,2,3,4,7,9,12,18,25,32,50,67,86,124,169,218,311,419,554,770`: 0 results
  - `1,2,3,4,7,9,12,18,25,32,50,67,86`: 0 results
  - `almost symmetric numerical semigroup`: 4 results (A001333, A000110, A000129, A000262)
  - `symmetric numerical set`: 10 results (A164047, A007323, A372341, A164048, A372878)
- Crossref (the journal literature, ranked by relevance), 3 searches:
  - `symmetrization almost symmetric numerical semigroups`: first results "Almost Symmetric and Nearly Symmetric Numerical Semigroups" (2026); "Almost symmetric numerical semigroups with high type" (2019); "Almost Symmetric Numerical Semigroups with Odd Generators" (2020)
  - `symmetric numerical sets image almost symmetric numerical semigroups`: first results "Almost Symmetric and Nearly Symmetric Numerical Semigroups" (2026); "Almost symmetric numerical semigroups with high type" (2019); "Almost Symmetric Numerical Semigroups with Odd Generators" (2020)
  - `numerical sets Young diagrams symmetric almost symmetric`: first results "Young Diagram Decompositions for Almost Symmetric Numerical Semigroups" (2025); "Applying Young diagrams to 2-symmetric fuzzy measures with an application to general fuzzy measures" (2020); "Almost Symmetric and Nearly Symmetric Numerical Semigroups" (2026)
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no numerical-semigroup family.

Closest work found, and how this problem differs:
- Delgado, Suer and Yesil (2026): define Phi and ask whether it is onto (the question above refines theirs; the counts answer it in the negative for G >= 3).
- Yesil (2025): Young diagram decompositions of almost symmetric numerical semigroups, with a symmetric numerical set attached to a semigroup; no image is counted.

Verdict: new. The map Phi was defined in November 2026 (arXiv:2611.14268), whose authors asked only whether it is onto; no count or description of its image was found (arXiv, Crossref, web), and the sequence I(1), I(3), ..., I(41) = 1, 1, 2, 3, 4, 7, 9, 12, 18, 25, 32, 50, ... is not in the OEIS.

## First values

| G | symmetric numerical sets | I(G) | how |
| --- | --- | --- | --- |
| 1 | 1 | 1 | exact (exhaustive) |
| 3 | 2 | 1 | exact (exhaustive) |
| 5 | 4 | 2 | exact (exhaustive) |
| 7 | 8 | 3 | exact (exhaustive) |
| 9 | 16 | 4 | exact (exhaustive) |
| 11 | 32 | 7 | exact (exhaustive) |
| 13 | 64 | 9 | exact (exhaustive) |
| 15 | 128 | 12 | exact (exhaustive) |
| 17 | 256 | 18 | exact (exhaustive) |
| 19 | 512 | 25 | exact (exhaustive) |
| 21 | 1024 | 32 | exact (exhaustive) |
| 23 | 2048 | 50 | exact (exhaustive) |
| 25 | 4096 | 67 | exact (exhaustive) |
| 27 | 8192 | 86 | exact (exhaustive) |
| 29 | 16384 | 124 | exact (exhaustive) |
| 31 | 32768 | 169 | exact (exhaustive) |
| 33 | 65536 | 218 | exact (exhaustive) |
| 35 | 131072 | 311 | exact (exhaustive) |
| 37 | 262144 | 419 | exact (exhaustive) |
| 39 | 524288 | 554 | exact (exhaustive) |
| 41 | 1048576 | 770 | exact (exhaustive) |
| 43 | 2097152 | 1016 | best known (ours) |
| 45 | 4194304 | 1359 | best known (ours) |
| 47 | 8388608 | 1873 | best known (ours) |
| 49 | 16777216 | 2466 | best known (ours) |
| 51 | 33554432 | 3233 | best known (ours) |

Exact for G <= 41: every almost symmetric numerical semigroup with Frobenius number at most 79 was enumerated (tools/src/symmetrization_enum.c, which re-derives the pseudo-Frobenius numbers from the definition at every leaf), and a bound of ours gives every image a preimage with Frobenius number at most max(G, 2G - 5); a separately written Python enumeration agrees for G <= 29, and tools/symmetrization_image.py reproduces every count with preimages of Frobenius number at most 67. For G = 43 to 51 the values are lower bounds from preimages with Frobenius number at most 67 (unchanged from 59 to 67 for G <= 49).

## Best known value

1016 for G = 43, held by Quantavane (Arhan Canli), 15 November 2026: the preimages in `refs/symmetrization-image.txt`. Upper bound: the 2^21 = 2,097,152 symmetric numerical sets with Frobenius number 43, of which those containing 1 are never images; no better bound is stated here.

## Cells

The same question at each value of its parameter (G, an odd Frobenius number): 26 cells, 21 of them exact (an exhaustive search finished) and 5 best known (ours). Each cell has its certificate in `refs/cells/symmetrization-image/` (the headline cell uses `collections/originals/refs/symmetrization-image.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example symmetrization-image-1

| cell | G | value | status |
| --- | --- | --- | --- |
| `symmetrization-image-1` | 1 | 1 | exact |
| `symmetrization-image-3` | 3 | 1 | exact |
| `symmetrization-image-5` | 5 | 2 | exact |
| `symmetrization-image-7` | 7 | 3 | exact |
| `symmetrization-image-9` | 9 | 4 | exact |
| `symmetrization-image-11` | 11 | 7 | exact |
| `symmetrization-image-13` | 13 | 9 | exact |
| `symmetrization-image-15` | 15 | 12 | exact |
| `symmetrization-image-17` | 17 | 18 | exact |
| `symmetrization-image-19` | 19 | 25 | exact |
| `symmetrization-image-21` | 21 | 32 | exact |
| `symmetrization-image-23` | 23 | 50 | exact |
| `symmetrization-image-25` | 25 | 67 | exact |
| `symmetrization-image-27` | 27 | 86 | exact |
| `symmetrization-image-29` | 29 | 124 | exact |
| `symmetrization-image-31` | 31 | 169 | exact |
| `symmetrization-image-33` | 33 | 218 | exact |
| `symmetrization-image-35` | 35 | 311 | exact |
| `symmetrization-image-37` | 37 | 419 | exact |
| `symmetrization-image-39` | 39 | 554 | exact |
| `symmetrization-image-41` | 41 | 770 | exact |
| `symmetrization-image-43` | 43 | 1016 | best known (headline) |
| `symmetrization-image-45` | 45 | 1359 | best known |
| `symmetrization-image-47` | 47 | 1873 | best known |
| `symmetrization-image-49` | 49 | 2466 | best known |
| `symmetrization-image-51` | 51 | 3233 | best known |

Exact cells: every almost symmetric numerical semigroup with Frobenius number at most 79 enumerated (tools/src/symmetrization_enum.c); every image has a preimage with Frobenius number at most max(G, 2G - 5). Best known cells: every almost symmetric numerical semigroup with Frobenius number at most 67 (tools/symmetrization_image.py); a lower bound.

## Submitting and checking

Format: Text file: one almost symmetric numerical semigroup per line, given by generators (positive integers with greatest common divisor 1, separated by spaces); lines starting with # are ignored. Every image Phi(S) must have Frobenius number 43, and no two lines may give the same image.

Score: the number of different images (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check symmetrization-image FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_numth.py symmetrization-image 43 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/symmetrization-image.txt`.

## References

- M. Delgado, M. Suer, M. Yesil, A symmetrization for almost symmetric numerical semigroups, arXiv:2611.14268 (2026)
- V. Barucci, R. Froberg, One-dimensional almost Gorenstein rings, Journal of Algebra 188 (1997) 418-442
- H. Nari, Symmetries on almost symmetric numerical semigroups, Semigroup Forum 86 (2013) 140-154
- M. Yesil, Young diagram decompositions for almost symmetric numerical semigroups, arXiv:2504.20688 (2025)
