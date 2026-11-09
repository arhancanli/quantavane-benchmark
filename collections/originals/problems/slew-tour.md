# The slewing tour of the Bright Star Catalogue

`slew-tour` · Astronomy · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **103836804** (minimize), Quantavane (Arhan Canli), 9 November 2026: nearest-neighbour start, 2-opt and Or-opt with 12-nearest-neighbour lists, then iterated local search with double-bridge kicks for 900 seconds (tools/src/tspmount.c)

## Statement

Take the 9,096 stars of the Yale Bright Star Catalogue (5th revised edition) that have a J2000 position, listed in collections/originals/instances/bsc-sky.txt with their right ascension in tenths of a second of time and their declination in arcseconds, exactly as in the catalogue. An equatorial telescope mount turns its two axes at the same rate, so going from one star to the next costs max(dRA, dDec): dRA is the turn of the polar axis, the shorter way round (the difference of right ascensions or the full circle minus it), dDec the turn of the declination axis, both in half arcseconds (a tenth of a second of time is 3 half arcseconds; the full circle is 2,592,000). Find the shortest closed tour through all the stars. Best known: 103,836,804 half arcseconds (ours); every tour is at least 88,725,989.

## Why it is interesting

Observing programmes that visit a fixed list of targets lose telescope time to slewing, and ordering the targets is a travelling salesman problem in the mount's own metric. An equatorial mount that drives both axes at the same rate needs the larger of the two turns, so the metric is the maximum (Chebyshev) distance on the cylinder of right ascension and declination, not the angle on the sky: near the celestial poles a short step on the sky can need a long turn of the polar axis, and along the equator a diagonal step costs no more than a straight one. The best tour therefore differs from the great-circle tour of the same stars. The instance is the classical naked-eye catalogue (Hoffleit and Warren 1991), the target list of programmes that observe every bright star. Target ordering by slew time is solved as a travelling salesman problem in survey schedulers (Bellm et al. 2019) and was studied as the Traveling Telescope Problem (Handley, Petigura and Misic 2023); tours through whole star catalogues have been computed with straight-line distances in space (W. Cook's star tours of the Hipparcos and Gaia stars). We found no tour of a catalogue in a mount's metric and no exact solution of this instance. A simple lower bound (each star's two tour steps are at least its two shortest steps) gives 88,725,989; better tours and better bounds (the Held-Karp bound, exact solvers such as Concorde) are open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/slew-tour.json`](../novelty/slew-tour.json) with its address, the time it ran and its first results.

- arXiv API, 7 searches:
  - `all:"traveling salesman" AND all:"bright star"`: 0 results
  - `all:"travelling salesman" AND all:telescope AND all:slew`: 1 result
  - `all:"star tours" AND all:"traveling salesman"`: 0 results
  - `all:"telescope scheduling" AND all:"traveling salesman"`: 0 results
  - `all:"slew time" AND all:"traveling salesman"`: 1 result
  - `all:"equatorial mount" AND all:slew`: 0 results
  - `all:"Bright Star Catalogue" AND all:tour`: 0 results
- Web search (general web search), `travelling salesman tour telescope slew equatorial mount star catalogue Bright Star Catalogue`: the Traveling Telescope Problem (Handley, Petigura and Misic, arXiv:2310.18497: a travelling salesman variant with time-dependent slew times, solved by integer programming), the Zwicky Transient Facility scheduler (arXiv:1905.02209: a travelling salesman problem inside each observing block, equatorial mount with independent axes), a pulsar timing programme ordering sources with 2-opt (arXiv:1812.04038) and amateur forum threads; none uses the Bright Star Catalogue or poses a benchmark instance
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark has vehicle routing instances, the Mona Lisa tour (Prestige 100) and our Euclidean tours, not this metric.

Closest work found, and how this problem differs:
- W. Cook's star tours: travelling salesman tours through the positions of Hipparcos and Gaia stars in three-dimensional space (Euclidean distances), not slewing tours on the sky.
- The Traveling Telescope Problem (Handley, Petigura and Misic 2023) and the Zwicky Transient Facility scheduler (Bellm et al. 2019): target ordering as a travelling salesman problem with mount slew times, for particular target lists under observing constraints. The problem type is studied; this instance (the whole Bright Star Catalogue, the idealised equal-rate equatorial metric) and its values are not.
- Our problems tsp-gaussian and tsp-sunflower: Euclidean instances in the plane.

Verdict: new as an instance. Ordering telescope targets as a travelling salesman problem in slew time is studied (the Traveling Telescope Problem; survey schedulers); no tour of a whole star catalogue in a mount's metric, and no benchmark value, was found. The instance is defined here from the Bright Star Catalogue.

## Best known value

103,836,804 half arcseconds (14,421.78 degrees of slewing), held by Quantavane (Arhan Canli), 9 November 2026: the tour in `refs/slew-tour.txt` (tools/src/tspmount.c, 900 s). Lower bound 88,725,989: half the sum over the stars of their two shortest steps.

Bound on the other side: 88725989 (lower bound; half the sum over all stars of the lengths of their two shortest steps (each star has two tour steps)).

## Submitting and checking

Format: Text file: the HR numbers of all 9,096 stars of the instance in the order of the tour, each exactly once.

Score: the length of the tour in half arcseconds, an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check slew-tour FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_astro.py slew-tour collections/originals/instances/bsc-sky.txt FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/slew-tour.txt`.

## References

- D. Hoffleit, W. H. Warren Jr., The Bright Star Catalogue, 5th revised ed., Yale University Observatory (1991); distributed by NASA HEASARC (table heasarc_bsc5p) and CDS (V/50)
- D. L. Applegate, R. E. Bixby, V. Chvatal, W. J. Cook, The Traveling Salesman Problem: A Computational Study, Princeton University Press (2006)
- W. Cook, Star tours (travelling salesman tours through the Hipparcos and Gaia stars), https://www.math.uwaterloo.ca/tsp/star/
- L. Handley, E. A. Petigura, V. V. Misic, Solving the Traveling Telescope Problem with mixed-integer linear programming, arXiv:2310.18497 (2023)
- E. C. Bellm et al., The Zwicky Transient Facility: surveys and scheduler, Publ. Astron. Soc. Pacific 131 (2019) 068003 (arXiv:1905.02209)
- M. Held, R. M. Karp, The traveling-salesman problem and minimum spanning trees, Oper. Res. 18 (1970) 1138-1162
