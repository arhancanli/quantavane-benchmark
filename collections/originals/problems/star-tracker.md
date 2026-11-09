# The smallest star-tracker catalogue of the bright sky

`star-tracker` · Astronomy · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **456** (minimize), Quantavane (Arhan Canli), 9 November 2026: greedy construction, then iterated removal of one to three random stars, greedy repair and pruning of redundant stars for 600 seconds (tools/src/multicover.c)

## Statement

A star tracker finds a spacecraft's attitude from the catalogued stars in its field of view and needs at least three of them wherever it points. Take the 2,887 stars of the Yale Bright Star Catalogue (5th revised edition) with V <= 5.5 and, as pointing directions, the 3,072 pixel centres of the HEALPix grid with Nside = 16; both are given as integer unit vectors (rounded to 10^-9) in collections/originals/instances/star-tracker.txt, and a star is in the field of view of a pointing when the dot product of their vectors is at least the threshold T in the file (a field of radius 10 degrees). Choose the fewest stars so that every pointing has at least k = 3 chosen stars in its field of view. Best known: 456 stars (ours); every such catalogue has at least 288.

## Why it is interesting

On-board star catalogues are thinned so that identification searches fewer stars while every pointing still sees enough of them; 'at least three stars in every field of view' is the usual design rule (Liebe 2002), and guide-star selection methods in the star-tracker literature (thinning, entropy and probability criteria, genetic algorithms) build near-uniform catalogues for particular sensors. Exactly stated, the task is a set multicover problem on the sky, and the real sky makes it uneven: stars crowd along the Milky Way and thin out towards the galactic poles, so a catalogue must keep faint stars in sparse regions and can drop many in dense ones. The instance fixes everything (catalogue, magnitude limit, field radius, pointing grid, rounding) so that values can be compared exactly. A simple lower bound: 96 pointings have pairwise disjoint sets of stars in view, and each needs three of its own, so at least 288 stars are needed; the gap to 456 is open. The table gives the best values for other k as well; k = 3 is the headline cell.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/star-tracker.json`](../novelty/star-tracker.json) with its address, the time it ran and its first results.

- arXiv API, 6 searches:
  - `all:"star catalog" AND all:"star tracker" AND all:thinning`: 0 results
  - `all:"navigation star" AND all:catalog AND all:uniform`: 0 results
  - `all:"star tracker" AND all:"set cover"`: 0 results
  - `all:"guide star" AND all:"minimum number" AND all:"field of view"`: 0 results
  - `all:"star tracker" AND all:"star catalog" AND all:"uniform"`: 0 results
  - `all:"guide star catalog" AND all:"star sensor" AND all:selection`: 0 results
- Web search (general web search), `star tracker navigation star catalog selection minimum number of stars every field of view at least three stars set cover optimization`: guide-star catalogue generation for star trackers: the design rule of more than two stars in every field of view, catalogue decimation, a genetic algorithm with Latinized stratified sampling, a minimum Boltzmann entropy criterion and a probability model (IEEE Sensors J. 2018); heuristics for particular sensors, no exact instance or set-cover benchmark
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark's covering-design family covers sets combinatorially; no geometric multicover instance.

Closest work found, and how this problem differs:
- Guide-star catalogue generation for star trackers (methods found by our web search: genetic algorithms with stratified sampling, minimum-entropy and probability criteria, IEEE Sensors Journal 2018): the same requirement of more than two stars per field, for particular sensors, with heuristic catalogues and no benchmark value.
- Covering the sphere by equal caps (covering problems on the sphere): there the caps can be placed anywhere and must cover once; here the caps are centred at given stars and every pointing must be covered three times.

Verdict: new as an instance. Thinning star catalogues so that every field of view keeps at least three stars is a design step of star trackers, solved there by heuristics for particular sensors and catalogues; no exactly specified instance or best known value was found. The instance is defined here.

## First values

| k (stars needed in every field) | fewest stars found | lower bound (96 k) | how |
| --- | --- | --- | --- |
| 1 | 166 | 96 | best known (ours, 150 s) |
| 2 | 314 | 192 | best known (ours, 150 s) |
| 3 | 456 | 288 | best known (ours, 600 s) |
| 4 | 599 | 384 | best known (ours, 150 s) |
| 5 | 735 | 480 | best known (ours, 150 s) |

The whole catalogue (2,887 stars) puts at least 7 stars in every field. Lower bound: 96 pointings with pairwise disjoint sets of stars in view (chosen greedily, fewest stars first) each need k stars of their own.

## Best known value

456 stars, held by Quantavane (Arhan Canli), 9 November 2026: the catalogue in `refs/star-tracker.txt` (tools/src/multicover.c, 600 s); every pointing sees at least 3 of its stars. Lower bound 288 (96 pointings with disjoint fields).

Bound on the other side: 288 (lower bound; 96 pointings have pairwise disjoint sets of stars in view (tools/src/multicover.c), and each needs 3 chosen stars of its own).

## Submitting and checking

Format: Text file: the HR numbers of the chosen stars (whitespace-separated), each at most once, all stars of the instance.

Score: the number of chosen stars, an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check star-tracker FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_astro.py star-tracker collections/originals/instances/star-tracker.txt 3 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/star-tracker.txt`.

## References

- D. Hoffleit, W. H. Warren Jr., The Bright Star Catalogue, 5th revised ed., Yale University Observatory (1991); NASA HEASARC table heasarc_bsc5p
- K. M. Gorski et al., HEALPix: a framework for high-resolution discretization and fast analysis of data distributed on the sphere, Astrophys. J. 622 (2005) 759-771
- C. C. Liebe, Accuracy performance of star trackers - a tutorial, IEEE Trans. Aerosp. Electron. Syst. 38 (2002) 587-599
- Generation of guide star catalog for star trackers, IEEE Sensors Journal (2018) (found by our web search; selection by a probability model of the stars in the field of view)
- U. Feige, A threshold of ln n for approximating set cover, J. ACM 45 (1998) 634-652
