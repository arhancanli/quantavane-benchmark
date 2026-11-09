# Non-redundant aperture masks for segmented mirrors

`nrm-segments` · Astronomy · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **23** (maximize), Quantavane (Arhan Canli), 9 November 2026: local search that moves one hole at a time to the segment creating the fewest repeated baselines, with a tabu list (tools/src/nrm.c, mode ls)

## Statement

A segmented telescope mirror with s rings of hexagonal segments around a missing central segment has 3s(s + 1) segments, centred at the points a + b*w of the triangular lattice (w = e^(i pi/3)) with hexagonal norm max(|a|, |b|, |a + b|) from 1 to s. An aperture mask that puts one hole on each of some segments is non-redundant when no baseline repeats: the vectors joining two holes are all different, a vector and its negative counting as the same baseline. Let h(s) be the largest number of holes of a non-redundant mask on the s-ring mirror. The headline cell is s = 10 (330 segments): find a non-redundant mask with more than 23 holes.

## Why it is interesting

Aperture masking turns a single telescope into an interferometer: a mask with a few small holes in the pupil plane makes every pair of holes a baseline, and when no baseline repeats (a non-redundant mask) each Fourier component of the image is measured by one pair only, so closure phases are free of redundancy noise (Haniff et al. 1987; Tuthill et al. 2000). On a segmented mirror the holes must avoid the gaps between segments, which in practice puts at most one hole on each segment, at its centre. The mask of the NIRISS instrument on the James Webb Space Telescope has 7 holes on 7 of the mirror's 18 segments (Sivaramakrishnan et al. 2023); our exhaustive search shows that 7 is the most possible on that layout (s = 2). Keck's and GTC's mirrors have the 36-segment layout s = 3, where the most is 9; HET and SALT have 91 segments, TMT 492 and ELT 798, and the question grows with them. Mathematically h(s) is the largest Sidon set (all differences distinct) inside a hexagon of the triangular lattice with its centre removed. Golay (1971) designed compact non-redundant arrays for radio and optical astronomy, Blackburn, Etzion, Martin and Paterson (2010) found the largest hexagonal-grid configurations with distinct differences whose points are at most a given distance apart (diameter up to 10), and Blackburn, Panoui, Paterson and Stinson (2010) classified honeycomb arrays; none of these fixes the region to a mirror's segment layout with the centre removed, and we found no table of h(s). Counting baselines gives h(10) <= 36; the gap between 23 and 36 is open, as is the growth of h(s).

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/nrm-segments.json`](../novelty/nrm-segments.json) with its address, the time it ran and its first results.

- arXiv API, 8 searches:
  - `all:"non-redundant" AND all:"aperture mask" AND all:segmented`: 2 results
  - `all:"non-redundant mask" AND all:holes AND all:maximum`: 0 results
  - `all:"distinct difference" AND all:hexagonal`: 5 results
  - `all:"Sidon set" AND all:hexagonal`: 0 results
  - `all:Golomb AND all:hexagonal AND all:lattice`: 0 results
  - `all:"honeycomb arrays"`: 43 results
  - `all:"aperture masking" AND all:"non-redundant" AND all:design`: 7 results
  - `all:"sparse aperture masking" AND all:segments AND all:"non-redundant"`: 1 result
- OEIS, 5 searches:
  - `non-redundant mask`: 0 results
  - `Sidon hexagon`: 2 results (A000217, A001107)
  - `distinct differences hexagonal`: 10 results (A390739, A205128, A390738, A205129, A066931)
  - `4,7,9,12`: 10 results (A003136, A003151, A301692, A047211, A185256)
  - `4,7,9,12,14`: 10 results (A003151, A047211, A022840, A007064, A246514)
- Web search (general web search), `maximum number of holes non-redundant aperture mask segmented mirror hexagonal segments one hole per segment JWST AMI Keck design`: the JWST NIRISS documentation and Sivaramakrishnan et al. (2023): a 7-hole non-redundant mask with one hole per primary segment; the Keck segment-tilting experiment; no maximum hole count for masks with one hole per segment
- Web search (arXiv full text (read)), `arXiv:0811.3832 (Blackburn, Etzion, Martin, Paterson)`: hexagonal-grid distinct-difference configurations with diameter at most r, the best ones found by backtracking for 2 <= r <= 10 (given in a figure); the constraint is the diameter, not a fixed region with its centre removed
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark's families (covering designs, codes, covering arrays, schedules) have no aperture or Sidon-set family.

Closest work found, and how this problem differs:
- S. R. Blackburn, T. Etzion, K. M. Martin and M. B. Paterson (2010): the largest hexagonal-grid configurations with distinct differences and diameter at most r (r <= 10, by backtracking). Their region is any set of that diameter; here the region is fixed (the segment layout) and the centre is missing, as on real telescopes.
- The JWST NIRISS mask (7 holes on 18 segments) and other masks designed instrument by instrument; none asks for the maximum on a given layout.
- Golay arrays (1971) and honeycomb arrays (Blackburn, Panoui, Paterson, Stinson 2010): non-redundant arrays with other constraints (compactness; one dot in every row in three directions).

Verdict: new question: nobody asked for the largest non-redundant set of segments of a hexagonal segmented mirror with its centre removed. Masks are designed instrument by instrument, and distinct-difference configurations in the hexagonal grid were studied with a bound on their diameter, which is a different question.

## First values

| s | segments | most holes h(s) | telescopes with this layout | how |
| --- | --- | --- | --- | --- |
| 1 | 6 | 4 |  | exact (exhaustive search) |
| 2 | 18 | 7 | JWST | exact (exhaustive search) |
| 3 | 36 | 9 | Keck, GTC | exact (exhaustive search) |
| 4 | 60 | 12 |  | exact (exhaustive search, 49 million nodes) |
| 5 | 90 | 14 | HET and SALT (91, centre included) | best known (ours, local search) |
| 6 | 126 | 16 |  | best known (ours, local search) |
| 7 | 168 | 18 |  | best known (ours, local search) |
| 8 | 216 | 20 |  | best known (ours, local search) |
| 9 | 270 | 21 |  | best known (ours, local search) |
| 10 | 330 | 23 |  | best known (ours, local search) |

Exact values from tools/src/nrm.c (mode max: depth-first search over segments with the baselines used so far marked); the local search (mode ls) reproduces them. Larger values are lower bounds.

## Best known value

23 holes, held by Quantavane (Arhan Canli), 9 November 2026: the mask in `refs/nrm-segments.txt` (253 baselines, all different). Counting baselines (the 630 baseline vectors of hexagonal norm at most 20, up to sign) gives h(10) <= 36.

Bound on the other side: 36 (upper bound; counting: the h(h - 1)/2 baselines of a mask with h holes are distinct vectors of hexagonal norm at most 20, of which there are 630 up to sign, so h(h - 1)/2 <= 630).

## Submitting and checking

Format: Text file: one line 'a b' per hole, the segment a + b*w (hexagonal norm 1..10), each segment at most once.

Score: the number of holes, an integer (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check nrm-segments FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_astro.py nrm-segments 10 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/nrm-segments.txt`.

## References

- C. A. Haniff, C. D. Mackay, D. J. Titterington, D. Sivia, J. E. Baldwin, The first images from optical aperture synthesis, Nature 328 (1987) 694-696
- P. G. Tuthill, J. D. Monnier, W. C. Danchi, E. H. Wishnow, C. A. Haniff, Michelson interferometry with the Keck I telescope, Publ. Astron. Soc. Pacific 112 (2000) 555-565
- A. Sivaramakrishnan et al., The James Webb Space Telescope Aperture Masking Interferometer, Publ. Astron. Soc. Pacific 135 (2023) 015003 (arXiv:2201.01524)
- M. J. E. Golay, Point arrays having compact, nonredundant autocorrelations, J. Opt. Soc. Am. 61 (1971) 272-273
- S. R. Blackburn, T. Etzion, K. M. Martin, M. B. Paterson, Two-dimensional patterns with distinct differences: constructions, bounds, and maximal anticodes, IEEE Trans. Inform. Theory 56 (2010) 1216-1229 (arXiv:0811.3832)
- S. R. Blackburn, A. Panoui, M. B. Paterson, D. R. Stinson, Honeycomb arrays, Electron. J. Combin. 17 (2010) R172
