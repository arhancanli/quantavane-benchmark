# Quantavane Originals

New open problems, written by Quantavane: <!--count-->46<!--/count--> problems across mathematics, physics,
chemistry, astronomy, computing and biology. Each one is a question that, as far as our searches show, nobody had
asked before, stated precisely, with an exact checker of ours and a first value of ours, so that it starts with a best
known value, a holder and a date. All of them are open.

Each question is a family of cells: the same question at each value of its natural parameter (the number of antennas,
the side of a grid, the number of digits, ...), each cell with our first value, its certificate in `refs/cells/` and
the family's exact checker, the way the benchmark's table families are counted. There are <!--cells-->1049<!--/cells-->
cells. The questions and the cells are counted apart (`index.json`: `questions`, `cells`, `cells_exact`); each cell says
whether its value is exact (an exhaustive search finished) or the best known (ours), and a family without a cells file
is one cell, its headline. A cell is checked like any problem: `python3 -I obb.py check CELL FILE`.

For every problem the file in `problems/` (and its page `problems/ID.md`) gives:

- the statement, with the headline cell that the checker scores;
- why it is interesting: what it is connected to, with references;
- the novelty check, run before the problem was added: arXiv API searches, OEIS searches of its first values and of
  its words, web searches where useful, and the keeper tables of the Open Problems Benchmark. Every search is kept
  in `novelty/ID.json` with its address, time and first results. A problem whose question had been studied
  before, even if only on other instances, was dropped, not added; each verdict says whether the question is new;
- the first values (exact where an exhaustive search finished, best known otherwise) and how they were computed;
- the best known value, the certificate in `refs/`, and the bound on the other side when there is one.

Checkers are in `checkers/` (one file per field, standard library only; each prints `RESULT v`, the exact value, and
exits 0 only for a valid certificate). The programs that produced the first values and the certificates are in
`tools/` (Python and C, our own code).

    python3 -I obb.py list originals                      # from the benchmark's root
    python3 -I obb.py show paley-ising
    python3 -I obb.py check paley-ising my_configuration.txt
    python3 -I collections/originals/tests/test_originals.py

A result that beats a best known value here is checked like any other submission to the benchmark (SUBMITTING.md)
and is credited by name on the problem's page and in `leaderboard.json`.

<!--table-->
| Problem | Field | Objective | Best known (ours, 9 November 2026) | Cells (exact) |
| --- | --- | --- | --- | --- |
| [Covering all pairs of Z_p by three-term progressions](problems/ap-cover.md) | Combinatorics and graph theory | minimize | 165 | 11 (3) |
| [The autoconvolution constant of the square](problems/autoconv-square.md) | Combinatorics and graph theory | minimize | 5687487427963392/2559015127450681 | 1 (0) |
| [The decycling number of the 600-cell](problems/cell600-forest.md) | Combinatorics and graph theory | maximize | 37 | 1 (0) |
| [Fewest monochromatic triangles in the E8 root graph](problems/e8-goodman.md) | Combinatorics and graph theory | minimize | 10385 | 1 (0) |
| [The metric dimension of the E8 root graph](problems/e8-resolving.md) | Combinatorics and graph theory | minimize | 12 | 1 (0) |
| [The minimum overlap constant of the square](problems/overlap-square.md) | Combinatorics and graph theory | minimize | 150615/262144 | 1 (0) |
| [The minimum overlap problem for three parts](problems/overlap-three.md) | Combinatorics and graph theory | minimize | 268741/960000 | 1 (0) |
| [Densest admissible patterns of primes n^3 + h](problems/cubic-admissible.md) | Number theory | minimize | 255 | 58 (14) |
| [Two-colourings with no monochromatic 120-degree triangle](problems/eisenstein-triples.md) | Number theory | maximize | 19200 | 1 (0) |
| [Admissible constellations of smallest diameter in the Gaussian integers](problems/gauss-admissible.md) | Number theory | minimize | 218 | 122 (47) |
| [The Jacobsthal function of the Gaussian integers](problems/gauss-jacobsthal.md) | Number theory | maximize | 15 | 11 (5) |
| [Arithmetic progressions of Gaussian primes](problems/gauss-prime-ap.md) | Number theory | maximize | 18 | 10 (7) |
| [Largest sum-free set of quadratic residues](problems/qr-sumfree.md) | Number theory | maximize | 174 | 71 (21) |
| [Densest admissible patterns of primes n^2 + h](problems/quad-admissible.md) | Number theory | minimize | 247 | 58 (17) |
| [Coils in the 120-cell](problems/cell120-coil.md) | Coding theory | maximize | 208 | 1 (0) |
| [Identifying codes of the 600-cell](problems/cell600-idcode.md) | Coding theory | minimize | 20 | 1 (0) |
| [Identifying codes of the E8 root polytope](problems/e8-idcode.md) | Coding theory | minimize | 15 | 1 (0) |
| [Error-correcting codes made of primes](problems/prime-code.md) | Coding theory | maximize | 299 | 6 (1) |
| [Covering the five-digit primes by one-digit changes](problems/prime-cover.md) | Coding theory | minimize | 1219 | 5 (1) |
| [Vertices of the 120-cell with no three on a great circle](problems/cell120-great.md) | Discrete geometry | maximize | 57 | 1 (0) |
| [Charges on the roots of E8](problems/e8-coulomb.md) | Discrete geometry | minimize | 304375/1152 | 118 (1) |
| [Distinct distances in the tetrahedral grid](problems/tetra-distinct.md) | Discrete geometry | maximize | 16 | 18 (8) |
| [Distinct triangle areas in the triangular grid](problems/tri-areas.md) | Discrete geometry | maximize | 9 | 27 (11) |
| [Distinct distances in the triangular grid](problems/tri-distinct.md) | Discrete geometry | maximize | 14 | 27 (13) |
| [Ising antiferromagnet on the grand antiprism](problems/ga-ising.md) | Physics | minimize | -140 | 1 (0) |
| [Ising antiferromagnet on the McLaughlin graph](problems/mclaughlin-ising.md) | Physics | minimize | -2968 | 1 (0) |
| [Ground states of the Paley Ising model](problems/paley-ising.md) | Physics | minimize | -492 | 36 (3) |
| [Ising antiferromagnet on the 600-cell](problems/polytope-ising.md) | Physics | minimize | -160 | 1 (0) |
| [Three-state Potts antiferromagnet on the 600-cell](problems/potts3-600.md) | Physics | minimize | 134 | 2 (0) |
| [Ising antiferromagnet on the snub 24-cell](problems/snub24-ising.md) | Physics | minimize | -144 | 1 (0) |
| [Benzenoids with the smallest Kemeny constant](problems/benzenoid-kemeny.md) | Chemistry and materials | minimize | 14813904881/113347080 | 17 (8) |
| [Catacondensed benzenoids with the smallest Kemeny constant](problems/cata-kemeny.md) | Chemistry and materials | minimize | 59617087737367409/159902997431616 | 17 (8) |
| [Pieces of diamond with the fewest dangling bonds](problems/diamond-bonds.md) | Chemistry and materials | minimize | 72 | 95 (12) |
| [The smallest knotted ring in the diamond lattice](problems/diamond-knot.md) | Chemistry and materials | minimize | 36 | 1 (0) |
| [The smallest catenane in the diamond lattice](problems/diamond-link.md) | Chemistry and materials | minimize | 28 | 1 (0) |
| [Lennard-Jones clusters on the face-centred cubic lattice](problems/lj-fcc.md) | Chemistry and materials | minimize | -789723697/1492992 | 147 (0) |
| [Non-redundant aperture masks for segmented mirrors](problems/nrm-segments.md) | Astronomy | maximize | 23 | 9 (3) |
| [Y-shaped arrays with all baseline lengths different](problems/y-array.md) | Astronomy | minimize | 165 | 37 (10) |
| [XOR circuits for the quadratic-residue circulant](problems/qr-xor.md) | Computing and operations research | minimize | 238 | 14 (0) |
| [Shortest reset words of the quadratic automaton modulo p](problems/sync-quadratic.md) | Computing and operations research | minimize | 31 | 51 (18) |
| [The travelling salesman tour of the Gaussian primes](problems/tsp-gaussian.md) | Computing and operations research | minimize | 11298548 | 6 (0) |
| [The travelling salesman tour of a sunflower](problems/tsp-sunflower.md) | Computing and operations research | minimize | 17245349 | 7 (0) |
| [The most ambiguous pair of DNA sequences](problems/align-ambiguity.md) | Biology | maximize | 917147 | 18 (5) |
| [Fibonacci proteins on the triangular lattice](problems/hp-tri.md) | Biology | minimize | -44 | 8 (2) |
| [The most ambiguous RNA under base-pair maximization](problems/nussinov-degeneracy.md) | Biology | maximize | 100603 | 25 (8) |
| [DNA open in all six reading frames](problems/six-frame.md) | Biology | minimize | 72 | 1 (0) |
<!--/table-->
