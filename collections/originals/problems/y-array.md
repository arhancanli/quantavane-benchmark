# Y-shaped arrays with all baseline lengths different

`y-array` · Astronomy · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **165** (minimize), Quantavane (Arhan Canli), 9 November 2026: local search that moves one antenna at a time to the place creating the fewest repeated lengths, with a tabu list, shortening the arms while it succeeds (tools/src/yarray.c, mode ls)

## Statement

A Y-shaped interferometer, like the Very Large Array, places its antennas on three straight arms that meet at 120 degrees. Put antennas at whole-number distances 1, 2, 3, ... from the centre (the centre itself unused). Two antennas on one arm at distances a and a' are |a - a'| apart; two on different arms are sqrt(a^2 + ab + b^2) apart. Each baseline length gives one sample of the visibility of a circularly symmetric source, so we ask that all N(N - 1)/2 baseline lengths be different. Let L(N) be the shortest arm length for which N antennas fit. We find L(N) exactly for N <= 12. The headline cell is N = 27, the number of antennas of the VLA: find a Y array of 27 antennas with all 351 baseline lengths different and arms shorter than 165 (ours).

## Why it is interesting

Radio and optical interferometers sample the Fourier transform of the sky at the baselines between their telescopes, and many are Y-shaped: the VLA has 27 antennas on three arms at 120 degrees, CHARA six telescopes, MROI up to ten. Non-redundant designs avoid repeated baseline vectors, which on a Y is easy (baselines between different arms never repeat; each arm only needs a Golomb ruler). For a circularly symmetric source, such as a star's disc, the visibility depends only on the baseline length, and then repeated lengths waste samples: the question becomes one of distinct distances on three rays of the triangular lattice. It couples three structures: the differences within the arms must all be different (one Golomb-type condition shared by the three arms), the cross lengths a^2 + ab + b^2 are Loschian numbers that must be represented only once, and a cross length equals a within-arm length exactly when (a, b, |a' - a''|) is a triangle with a 120-degree angle, an Eisenstein triple (problem eisenstein-triples). Counting gives L(27) >= 109: the 108 or more within-arm differences are different integers below L. The exact values for small N, the growth of L(N), and how close the VLA-sized case can come to 109 are open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/y-array.json`](../novelty/y-array.json) with its address, the time it ran and its first results.

- arXiv API, 5 searches:
  - `all:"Y-shaped" AND all:array AND all:baselines AND all:"non-redundant"`: 0 results
  - `all:"Y-shaped array" AND all:"baseline lengths"`: 0 results
  - `all:"minimum redundancy" AND all:"Y-shaped"`: 0 results
  - `all:Golomb AND all:"Y-shaped"`: 0 results
  - `all:"baseline lengths" AND all:distinct AND all:array AND all:interferometer`: 0 results
- OEIS, 4 searches:
  - `Y-shaped array distinct baselines`: 0 results
  - `1,2,3,5,6,7,9,11,14,17,21`: 0 results
  - `2,3,5,6,7,9,11,14,17,21`: 0 results
  - `1,2,3,5,6,7,9,11,14,17`: 0 results
- Web search (general web search), `Y-shaped interferometer array antenna positions all baseline lengths distinct Golomb VLA arms 120 degrees non-redundant baseline lengths`: the VLA's 120-degree arms, CHARA as a non-redundant Y of six telescopes (15 baselines, not all of different length), MROI's non-redundant Y; no array with all baseline lengths different
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no array-design family in the benchmark.

Closest work found, and how this problem differs:
- Non-redundant Y arrays in practice (CHARA, MROI): baseline vectors different, lengths not; on a Y that only asks for a Golomb ruler on each arm.
- Golomb rulers (one arm) and distinct distances in grids (Erdos and Guy; our tri-distinct): related distinctness questions on other point sets.
- Y-array design for the VLA (power-law antenna spacing for uv-coverage): a different objective.

Verdict: new question: non-redundant Y arrays are built with different baseline vectors (CHARA, MROI) and Golomb rulers solve the one-armed case; no result was found on Y arrays whose baseline lengths are all different.

## First values

| antennas N | shortest arm length L(N) | an array (the three arms) | how |
| --- | --- | --- | --- |
| 2 | 1 | 1 / 1 / - | exact (exhaustive search) |
| 3 | 2 | 1,2 / 1 / - | exact (exhaustive search) |
| 4 | 3 | 1,2 / 1,3 / - | exact (exhaustive search) |
| 5 | 5 | 1,2,4 / 1,5 / - | exact (exhaustive search) |
| 6 | 6 | 1,2,5 / 3 / 4,6 | exact (exhaustive search) |
| 7 | 7 | 1,2,6 / 3,5 / 4,7 | exact (exhaustive search) |
| 8 | 9 | 1,2,7,9 / 3,6 / 4,8 | exact (exhaustive search) |
| 9 | 11 | 1,7,11 / 2,3,10 / 4,6,9 | exact (exhaustive search) |
| 10 | 14 | 1,2,10,13 / 4,8,14 / 5,7,12 | exact (exhaustive search) |
| 11 | 17 | 1,2,7,15,17 / 3,10,14 / 4,13,16 | exact (exhaustive search) |
| 12 | 21 | 1,2,9,21 / 3,8,12,18 / 4,6,17,20 | exact (exhaustive search) |
| 15 | 35 | 4,7,11,27,33,35 / 1,12,22,31 / 2,16,17,29,34 | best known (ours, local search) |
| 20 | 73 | 14,15,18,42,60,68 / 1,6,26,40,61,63,73 / 5,12,21,34,53,64,70 | best known (ours, local search) |
| 27 | 165 | 2,13,15,36,117,139,143,153,158 / 1,4,33,51,71,78,113,156,164,165 / 10,47,75,100,106,130,146,163 | best known (ours, local search) |

Exact values from tools/src/yarray.c (mode exact: depth-first search over arms and distances, increasing L). OEIS has no sequence with the exact terms 1, 2, 3, 5, 6, 7, 9, 11, 14, 17, 21.

## Best known value

arm length 165, held by Quantavane (Arhan Canli), 9 November 2026: the array in `refs/y-array.txt` (arms of 9, 10, 8 antennas). Lower bound 109.

Bound on the other side: 109 (lower bound; the arms carry at least 108 pairs of antennas (sizes 9, 9, 9 minimise the count), whose differences are different integers between 1 and L - 1).

## Submitting and checking

Format: Text file: three lines, the distances (positive integers) of the antennas on each arm ('-' for an empty arm), 27 antennas in all.

Score: the arm length, the largest distance used (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check y-array FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_astro.py y-array 27 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/y-array.txt`.

## References

- A. R. Thompson, J. M. Moran, G. W. Swenson Jr., Interferometry and Synthesis in Radio Astronomy, 3rd ed., Springer (2017)
- P. J. Napier, A. R. Thompson, R. D. Ekers, The Very Large Array: design and performance of a modern synthesis radio telescope, Proc. IEEE 71 (1983) 1295-1320
- T. A. ten Brummelaar et al., First results from the CHARA Array. II. A description of the instrument, Astrophys. J. 628 (2005) 453-465 (arXiv:astro-ph/0504082)
- G. S. Bloom, S. W. Golomb, Applications of numbered undirected graphs, Proc. IEEE 65 (1977) 562-570
- P. Erdos, R. K. Guy, Distinct distances between lattice points, Elemente der Mathematik 25 (1970) 121-123
