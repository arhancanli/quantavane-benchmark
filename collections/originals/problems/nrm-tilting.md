# Splitting a segmented mirror into non-redundant groups

`nrm-tilting` · Astronomy · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **11** (minimize), Quantavane (Arhan Canli), 9 November 2026: min-conflicts local search that moves one segment between groups, with a tabu list (tools/src/nrm.c, mode part)

## Statement

On the segmented mirror with s rings of hexagonal segments around a missing centre (the 3s(s + 1) segments a + b*w of problem nrm-segments, w = e^(i pi/3), hexagonal norm 1 to s), split all the segments into groups so that no baseline repeats inside a group: within each group the vectors joining two segments are all different, a vector and its negative counting as one. Let g(s) be the fewest groups. Tilting the segments of each group so that its light forms its own interferogram turns the whole mirror into several non-redundant interferometers at once. The headline cell is s = 6 (126 segments): split them into fewer than 11 non-redundant groups.

## Why it is interesting

A non-redundant aperture mask uses only a few segments of a mirror and throws most of the light away (problem nrm-segments). Pupil remapping recovers it: on Keck, the primary-mirror segments were tilted so that four non-redundant groups of six segments formed separate interferograms on the detector at the same time, and the other 12 segments, which 'could not all fit into four non-redundant patterns', made a fifth image (Monnier et al. 2009). Jewel Optics (Taras, Piroscia and Tuthill 2025) does the same with phase wedges on a hexagonal grid of sub-apertures inside a circular pupil, choosing 'as few sets as possible' by a local search, with no proof of a minimum. Using every segment needs a partition of the whole mirror into non-redundant groups, and the fewest groups means the fewest interferograms to fit on the detector. For Keck's 36-segment layout (s = 3) we find that five groups suffice and four do not, confirming the experiment's observation: a split into four groups would need four disjoint largest masks of 9 segments, and an exhaustive search of all 5,190 such masks finds no four that partition the mirror. For s = 4 five groups are impossible in the same way (178 largest masks of 12 segments, no five disjoint), seven are enough, and six is open. Mathematically, g(s) is the least number of Sidon sets that partition a hexagon of the triangular lattice with its centre removed; partitions of sets of integers into Sidon sets have been studied, but we found nothing on hexagonal regions or on segmented mirrors.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/nrm-tilting.json`](../novelty/nrm-tilting.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"pupil remapping" AND all:segments AND all:tilting`: 0 results
  - `all:"segment tilting" AND all:interferometry`: 3 results
  - `all:"Sidon sets" AND all:partition AND all:"minimum number"`: 0 results
- OEIS, 2 searches:
  - `2,3,5`: 10 results (A000040, A000045, A000041, A005117, A001620)
  - `partition into Sidon sets`: 2 results (A000217, A398238)
- Web search (general web search), `Keck segment tilting experiment Monnier 2009 24 of 36 segments four interferograms non-redundant pupil remapping`: Monnier et al. (2009, arXiv:0905.3495): four non-redundant arrays of tilted segments, 24 of the 36 segments used for science, the rest in a fifth image because they could not all fit into four non-redundant patterns; Tuthill's review of masking (arXiv:1302.2722); Jewel Optics (arXiv:2501.01570)
- Web search (arXiv full text (read)), `arXiv:2501.01570 (Taras, Piroscia, Tuthill, Jewel Optics I)`: sub-apertures on a hexagonal close-packed grid in a circular pupil, split into non-redundant sets by a binary local search from random starts; 'the number of sets is selected empirically such that the final design has as few sets as possible'; 4 to 9 interferograms in their designs; no proven minimum, no segment layouts
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no Sidon-set or partition family in the benchmark.

Closest work found, and how this problem differs:
- The Keck segment-tilting experiment (Monnier et al. 2009): 24 of 36 segments in four interferograms; here every segment is used and the number of groups is minimised.
- Jewel Optics (A. K. Taras, G. Piroscia, P. Tuthill 2025): the same design question (tile a pupil by few non-redundant sets) on hexagonal grids inside circular pupils with obstructions removed, solved by local search for particular designs (4 to 9 interferograms), without a proven minimum and not on the segment layout of a segmented mirror. The problem type is studied there; this region, its exact small values and the bounds are not.
- Our problem nrm-segments (the largest single non-redundant group), whose exact values give the lower bounds for s <= 4 here.
- Partitions of {1, ..., n} into Sidon sets (one-dimensional, from the Sidon-set literature collected by O'Bryant): a different region and dimension.

Verdict: new as stated, close to a studied design question. Tiling a pupil by few non-redundant sets was done on Keck (segment tilting) and in Jewel Optics (hexagonal grids in circular pupils, by local search); no result was found on the fewest groups for the segment layout of a hexagonal segmented mirror, and no proven minimum for any layout.

## First values

| s | segments | fewest groups g(s) | how |
| --- | --- | --- | --- |
| 1 | 6 | 2 | exact (largest non-redundant set: 4 segments) |
| 2 | 18 | 3 | exact (largest set: 7) |
| 3 | 36 | 5 | exact: 4 groups would need 4 disjoint largest masks; none among the 5,190 masks of 9 segments |
| 4 | 60 | 6 or 7 | 7 found; 5 impossible (no 5 disjoint among the 178 masks of 12 segments) |
| 5 | 90 | 9 | best known (ours, local search); at least 5 |
| 6 | 126 | 11 | best known (ours, local search); at least 6 |

Lower bounds: the number of segments divided by the largest non-redundant set (exact for s <= 4; the counting bound h(5) <= 18, h(6) <= 22 otherwise), and exact covers by all largest sets (tools/src/nrm.c mode all, tools/nrm_cover.py).

## Best known value

11 groups, held by Quantavane (Arhan Canli), 9 November 2026: the partition in `refs/nrm-tilting.txt`. Lower bound 6: a non-redundant set on the 6-ring mirror has at most 22 segments (its baselines are distinct vectors of hexagonal norm at most 12, 234 of them up to sign), and 126/22 > 5.

Bound on the other side: 6 (lower bound; a non-redundant group has at most 22 of the 126 segments (counting baselines: 234 vectors of hexagonal norm at most 12 up to sign)).

## Submitting and checking

Format: Text file: one line per group, its segments written 'a,b' and separated by spaces; every segment of the 6-ring mirror exactly once.

Score: the number of groups, an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check nrm-tilting FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_astro.py nrm-tilting 6 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/nrm-tilting.txt`.

## References

- A. K. Taras, G. Piroscia, P. Tuthill, Jewel Optics I: non-redundant Fizeau beam combination without the guilt, arXiv:2501.01570 (2025)
- J. D. Monnier et al., Mid-infrared size survey of young stellar objects: description of Keck segment-tilting experiment and basic results, Astrophys. J. 700 (2009) 491-505 (arXiv:0905.3495)
- P. G. Tuthill, J. D. Monnier, W. C. Danchi, E. H. Wishnow, C. A. Haniff, Michelson interferometry with the Keck I telescope, Publ. Astron. Soc. Pacific 112 (2000) 555-565
- S. R. Blackburn, T. Etzion, K. M. Martin, M. B. Paterson, Two-dimensional patterns with distinct differences: constructions, bounds, and maximal anticodes, IEEE Trans. Inform. Theory 56 (2010) 1216-1229
- K. O'Bryant, A complete annotated bibliography of work related to Sidon sequences, Electron. J. Combin. DS11 (2004)
