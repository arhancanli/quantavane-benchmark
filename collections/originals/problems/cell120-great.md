# Vertices of the 120-cell with no three on a great circle

`cell120-great` · Discrete geometry · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **57** (maximize), Quantavane (Arhan Canli), 9 November 2026: random greedy choice followed by exchanges (a vertex whose only obstruction is one chosen vertex replaces it, then free vertices are added), many restarts (tools/greatcircle.py, mode search120)

## Statement

The 120-cell is the regular four-dimensional polytope with 600 vertices on the unit sphere of R^4. Choose as many of its vertices as possible so that no three of them lie on a common great circle, that is, no three of the vertex vectors lie in a plane through the centre (in particular no two chosen vertices are opposite). The vertices come in 300 opposite pairs, which lie on 2,120 great circles through at least three pairs; 60 disjoint great decagons cover all of them, so at most 120 vertices can be chosen. Best known: 57 (ours).

## Why it is interesting

The no-three-in-line problem asks for the most points of a grid with no three on a line (Dudeney 1917; Guy and Kelly 1968), and its projective form, caps, asks for the largest sets with no three collinear points in a projective space; over finite fields caps are a central topic of finite geometry. The 120-cell gives a real projective version with rich structure: its 600 vertices span 300 lines through the centre, and the great circles through three or more of its opposite pairs carry 6, 10 or 12 vertices (1,200, 720 and 200 such circles). A set with no three vertices on a great circle is a cap in this configuration. The Hopf fibration gives the upper bound: left multiplication by a unit quaternion of order 10 of the binary icosahedral group permutes the vertices in 60 orbits, each a great decagon, and a cap meets each decagon in at most two vertices, so at most 120. For the 600-cell (120 vertices, 12 decagons) the same bound is 24. How close a cap can come to the bound is open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/cell120-great.json`](../novelty/cell120-great.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"no three" AND all:"great circle" AND all:polytope`: 0 results
  - `all:"120-cell" AND all:"great circles" AND all:vertices AND all:subset`: 0 results
  - `all:"cap" AND all:"600-cell"`: 0 results
- OEIS, 1 searches:
  - `120-cell no three on a great circle`: 0 results
- Web search (general web search), `largest subset of vertices of the 120-cell OR 600-cell no three on a great circle OR "no three collinear" projective cap regular polytope vertices`: descriptions of the 600-cell and 120-cell (great decagons and pentagons, the 120-cell as five inscribed 600-cells) and a 2026 sphere-packing paper using independent sets among the 600-cell's vertices; nothing on caps or no-three-on-a-great-circle sets
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no cap or no-three-in-line family in the benchmark.

Closest work found, and how this problem differs:
- The no-three-in-line problem in grids (Dudeney; Guy and Kelly) and caps in finite projective spaces (Hirschfeld): the same condition in other spaces.
- Our other problems on the 600-cell (identifying codes, decycling, the Ising and Potts antiferromagnets): other questions on related polytopes.

Verdict: new question: no-three-in-line problems are studied in grids and in finite projective spaces (caps); no result was found on vertices of the 120-cell or the 600-cell with no three on a great circle.

## First values

| polytope | vertices | opposite pairs | great circles through >= 3 pairs | most vertices, no three on a great circle | how | upper bound (Hopf decagons) |
| --- | --- | --- | --- | --- | --- | --- |
| 600-cell | 120 | 60 | 72 decagons, 200 hexagons | 20 | best known (ours; the exhaustive search did not finish) | 24 |
| 120-cell | 600 | 300 | 1,200 through 6 vertices, 720 through 10, 200 through 12 | 57 | best known (ours, local search) | 120 |

Exact arithmetic in Q(sqrt 5) throughout (checkers/orig_geom.py); the decagon partition is computed and verified by tools/greatcircle.py (mode partition).

## Best known value

57 vertices, held by Quantavane (Arhan Canli), 9 November 2026: the set in `refs/cell120-great.txt`. Upper bound 120 (60 disjoint great decagons, at most two chosen vertices on each).

Bound on the other side: 120 (upper bound; the 60 orbits of left multiplication by an element of order 10 of the binary icosahedral group are disjoint great decagons covering all vertices, and each holds at most two chosen vertices).

## Submitting and checking

Format: Text file: one line 'a b c d' per chosen vertex of the 120-cell, written as the tetrahedral cell of the 600-cell whose centre it is (four vertex numbers 0..119 of the 600-cell, numbered as in checkers/orig_codes.py).

Score: the number of chosen vertices (larger is better). A submission improves the problem when its exact value is larger than the best known value.

    python3 -I obb.py check cell120-great FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_geom.py cell120-great FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/cell120-great.txt`.

## References

- H. S. M. Coxeter, Regular Polytopes, 3rd ed., Dover (1973)
- H. E. Dudeney, Amusements in Mathematics, Nelson (1917), problem 317
- R. K. Guy, P. A. Kelly, The no-three-in-line problem, Canad. Math. Bull. 11 (1968) 527-531
- J. W. P. Hirschfeld, Projective Geometries over Finite Fields, 2nd ed., Oxford University Press (1998)
