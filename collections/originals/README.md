# Quantavane Originals

New open problems, written by Quantavane: <!--count-->39<!--/count--> problems across mathematics, physics,
chemistry, astronomy, computing and biology. Each one is a question that, as far as our searches show, nobody had
asked before, stated precisely, with an exact checker of ours and a first value of ours, so that it starts with a best
known value, a holder and a date. All of them are open.

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
| Problem | Field | Objective | Best known (ours, 9 November 2026) |
| --- | --- | --- | --- |
| [Covering all pairs of Z_p by three-term progressions](problems/ap-cover.md) | Combinatorics and graph theory | minimize | 165 |
| [The autoconvolution constant of the square](problems/autoconv-square.md) | Combinatorics and graph theory | minimize | 5687487427963392/2559015127450681 |
| [The decycling number of the 600-cell](problems/cell600-forest.md) | Combinatorics and graph theory | maximize | 37 |
| [Fewest monochromatic triangles in the E8 root graph](problems/e8-goodman.md) | Combinatorics and graph theory | minimize | 10385 |
| [The metric dimension of the E8 root graph](problems/e8-resolving.md) | Combinatorics and graph theory | minimize | 12 |
| [The minimum overlap constant of the square](problems/overlap-square.md) | Combinatorics and graph theory | minimize | 150615/262144 |
| [The minimum overlap problem for three parts](problems/overlap-three.md) | Combinatorics and graph theory | minimize | 56061/200000 |
| [Densest admissible patterns of primes n^3 + h](problems/cubic-admissible.md) | Number theory | minimize | 255 |
| [Two-colourings with no monochromatic 120-degree triangle](problems/eisenstein-triples.md) | Number theory | maximize | 19200 |
| [Admissible constellations of smallest diameter in the Gaussian integers](problems/gauss-admissible.md) | Number theory | minimize | 218 |
| [Arithmetic progressions of Gaussian primes](problems/gauss-prime-ap.md) | Number theory | maximize | 18 |
| [Largest sum-free set of quadratic residues](problems/qr-sumfree.md) | Number theory | maximize | 174 |
| [Densest admissible patterns of primes n^2 + h](problems/quad-admissible.md) | Number theory | minimize | 247 |
| [Coils in the 120-cell](problems/cell120-coil.md) | Coding theory | maximize | 202 |
| [Identifying codes of the 600-cell](problems/cell600-idcode.md) | Coding theory | minimize | 20 |
| [Identifying codes of the E8 root polytope](problems/e8-idcode.md) | Coding theory | minimize | 15 |
| [Covering the five-digit primes by one-digit changes](problems/prime-cover.md) | Coding theory | minimize | 1219 |
| [Vertices of the 120-cell with no three on a great circle](problems/cell120-great.md) | Discrete geometry | maximize | 57 |
| [Distinct distances in the tetrahedral grid](problems/tetra-distinct.md) | Discrete geometry | maximize | 16 |
| [Distinct triangle areas in the triangular grid](problems/tri-areas.md) | Discrete geometry | maximize | 9 |
| [Distinct distances in the triangular grid](problems/tri-distinct.md) | Discrete geometry | maximize | 14 |
| [Ising antiferromagnet on the grand antiprism](problems/ga-ising.md) | Physics | minimize | -140 |
| [Ground states of the Paley Ising model](problems/paley-ising.md) | Physics | minimize | -480 |
| [Ising antiferromagnet on the 600-cell](problems/polytope-ising.md) | Physics | minimize | -160 |
| [Three-state Potts antiferromagnet on the 600-cell](problems/potts3-600.md) | Physics | minimize | 134 |
| [Ising antiferromagnet on the snub 24-cell](problems/snub24-ising.md) | Physics | minimize | -144 |
| [Benzenoids with the smallest Kemeny constant](problems/benzenoid-kemeny.md) | Chemistry and materials | minimize | 14813904881/113347080 |
| [Catacondensed benzenoids with the smallest Kemeny constant](problems/cata-kemeny.md) | Chemistry and materials | minimize | 59617087737367409/159902997431616 |
| [Lennard-Jones clusters on the face-centred cubic lattice](problems/lj-fcc.md) | Chemistry and materials | minimize | -789723697/1492992 |
| [Non-redundant aperture masks for segmented mirrors](problems/nrm-segments.md) | Astronomy | maximize | 23 |
| [Y-shaped arrays with all baseline lengths different](problems/y-array.md) | Astronomy | minimize | 165 |
| [XOR circuits for the quadratic-residue circulant](problems/qr-xor.md) | Computing and operations research | minimize | 238 |
| [Shortest reset words of the quadratic automaton modulo p](problems/sync-quadratic.md) | Computing and operations research | minimize | 31 |
| [The travelling salesman tour of the Gaussian primes](problems/tsp-gaussian.md) | Computing and operations research | minimize | 11298548 |
| [The travelling salesman tour of a sunflower](problems/tsp-sunflower.md) | Computing and operations research | minimize | 17245349 |
| [The most ambiguous pair of DNA sequences](problems/align-ambiguity.md) | Biology | maximize | 917147 |
| [Fibonacci proteins on the triangular lattice](problems/hp-tri.md) | Biology | minimize | -44 |
| [The most ambiguous RNA under base-pair maximization](problems/nussinov-degeneracy.md) | Biology | maximize | 100603 |
| [DNA open in all six reading frames](problems/six-frame.md) | Biology | minimize | 72 |
<!--/table-->
