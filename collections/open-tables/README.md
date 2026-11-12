# Quantavane Open Tables

Benchmark tables for fields that have no keeper of records. Each table is one question with an exact checker of ours
(standard library only, last line `RESULT v`, exit status 0 only for a valid submission); each cell is one instance of
the question. Every cell says where its best known value comes from, and the two kinds are counted apart:

- **published value**: read from a paper or a public table, with its source and the date it was read. A submission
  that beats it is a new result against the literature, once a prior-art search (papers, GitHub and Zenodo, the last
  six months at least) finds nothing better.
- **first entry**: nothing comparable has been published, so the cell starts with a value of ours (or a baseline we
  computed). Beating it is a new best in this table, not a record against the literature.

The first version (12 November 2026) had two fields; the second (13 November 2026) adds a third, topology
optimisation of structures and metamaterials:

- **Topology**: the unknotting numbers of the knots with at most 11 crossings that are still open. Each cell is a knot
  with KnotInfo's interval [a, a + 1]; a submission is an unknotting sequence on a closed braid (Markov moves and
  crossing changes), replayed exactly by `checkers/unknot_check.py`. A sequence with a crossing changes, if anyone finds
  one, settles that knot's unknotting number. Our certificates replay KnotInfo's upper bound for 66 of the 67 knots.
- **Aerodynamics, in a numerical model**: two-dimensional airfoil sections scored by QV-Foil 1
  (`checkers/airfoil_check.py`), a classical model fixed in code: the Hess-Smith panel method, Thwaites' laminar
  boundary layer, Michel's transition criterion, Head's turbulent boundary layer and the Squire-Young drag formula.
  **It is a numerical model, not a wind tunnel**: a score says what the model computes, nothing more. It runs on the
  standard library with our own logarithm, exponential and arctangent, so every machine gives the same number. No value
  has been published for this model, so every cell is a first entry; each also records the best NACA 4- or 5-digit
  section (published shapes, scored by us) as its baseline.
- **Topology optimisation, in a numerical model**: QV-Topo 1 (`checkers/topopt_check.py`), plane-stress linear
  elasticity on a fixed grid of square bilinear elements (Young's modulus 1, Poisson's ratio 0.3, void 1e-9), solved by
  our own banded Cholesky factorisation whose sums are all correctly rounded, so every machine prints the same digits.
  Five tables, 33 cells. Least compliance (the MBB beam and the cantilever of the 99- and 88-line papers, and an
  L-bracket) in two forms: `topopt-simp`, density fields in the SIMP model with the 88-line code's density filter, and
  `topopt-binary`, 0/1 designs with a minimum feature size, no point contacts and one connected piece. Periodic
  material cells (40 x 40, 0/1, a minimum feature size, connected in both directions) whose homogenised stiffness, by
  our own code, has the greatest bulk modulus (`metacell-bulk`, shown against the Hashin-Shtrikman bound), the greatest
  shear modulus (`metacell-shear`) or the most negative Poisson's ratio above a stiffness floor (`metacell-poisson`).
  The checker re-solves from the design alone. Two SIMP cells, the MBB beam of the 88-line paper on 60 x 20 and
  150 x 50 elements, have published values under exactly these settings (our replay of that paper's loop gives its
  printed values, 233.71 and 235.73; the lowest published value we found for 60 x 20 is 233.4878, from the PINNeAPPle
  project). Our first searches give 232.110 and 233.714 for these two cells; every other cell is a first entry.

<!--table-->
| Table | Field | Objective | Cells | Published values | First entries | Certified here |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| [Unknotting numbers of the knots with at most 11 crossings](problems/unknotting.md) | Topology | minimize | 67 | 67 | 0 | 66 |
| [Airfoil sections of greatest lift-to-drag ratio in the QV-Foil 1 model](problems/airfoil-ld.md) | Aerodynamics (numerical model) | maximize | 20 | 0 | 20 | 20 |
| [Airfoil sections of least drag at a required lift in the QV-Foil 1 model](problems/airfoil-cd.md) | Aerodynamics (numerical model) | minimize | 18 | 0 | 18 | 18 |
| [Least-compliance structures in the SIMP model with a density filter (QV-Topo 1)](problems/topopt-simp.md) | Structural topology optimisation (numerical model) | minimize | 10 | 2 | 8 | 10 |
| [Least-compliance 0/1 structures with a minimum feature size (QV-Topo 1)](problems/topopt-binary.md) | Structural topology optimisation (numerical model) | minimize | 12 | 0 | 12 | 12 |
| [Periodic material cells of greatest bulk modulus (QV-Topo 1)](problems/metacell-bulk.md) | Metamaterials (numerical model) | maximize | 4 | 0 | 4 | 4 |
| [Periodic material cells of greatest shear modulus (QV-Topo 1)](problems/metacell-shear.md) | Metamaterials (numerical model) | maximize | 4 | 0 | 4 | 4 |
| [Periodic material cells of most negative Poisson's ratio with a stiffness floor (QV-Topo 1)](problems/metacell-poisson.md) | Metamaterials (numerical model) | minimize | 3 | 0 | 3 | 3 |
<!--/table-->

    python3 -I obb.py list open-tables                              # from the benchmark's root
    python3 -I obb.py show unknotting-10-6
    python3 -I obb.py check unknotting-10-6 my_sequence.txt
    python3 -I obb.py check airfoil-ld-re3m-t12 my_airfoil.txt
    python3 -I obb.py check topopt-simp-mbb-60x20-v0.5-r2.4 my_density_field.txt
    python3 -I obb.py check metacell-bulk-n40-v0.5-k2 my_cell.txt
    python3 -I collections/open-tables/tests/test_open_tables.py

Layout: `problems/ID.json` and `problems/ID.md` (one per table: statement, context, references, sources, the cells
block), `cells/ID.jsonl` (one line per cell), `checkers/`, `refs/cells/` (our certificates: unknotting sequences that
replay the published bounds, NACA baselines and our airfoil designs, our designs and baselines for the topology
optimisation cells), `tools/` (the programs that built the cells and ran the searches), `tests/`. `tools/build.py`
writes the pages, `index.json` and the table above from the problem files and the cells. Every program uses the
standard library only, except `tools/airfoil_search.py`, `tools/topopt_fe.py` and `tools/topopt_search.py`, which use
numpy to speed up the searches (run them as `python3 tools/NAME.py ...`); their designs count only through the
checker. No program of anyone else was run: the searches (optimality criteria, the method of moving asymptotes,
projection and a local search) are our own code, written from the published equations.

Data and licences. Our code, cells and certificates: MIT (the benchmark's LICENSE). KnotInfo (C. Livingston and A. H.
Moore) states no licence and asks to be cited; the spreadsheet is redistributed under GPL-3.0 by the database_knotinfo
package. It is not copied here: `fetch.sh` downloads it at a pinned commit with its SHA-256, and the cells keep only the
values read from it (each knot's name, braid word, the two bounds, Alexander polynomial and signature), with the
source. The NACA sections are generated from their published formulas (NACA Reports 460, 610 and 824, US government
works in the public domain). The published compliance values of the topology optimisation cells are cited as facts with
their sources: the 88-line paper's preprint (Andreassen et al., 27 Oct 2010, Lirias, KU Leuven), the PINNeAPPle project
(GitHub, Apache-2.0), topokit (GitHub, MIT), qBraid's examples (GitHub, Apache-2.0) and SOPTX (arXiv:2505.02438);
nothing of theirs is copied or run.
