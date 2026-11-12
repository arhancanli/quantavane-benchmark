# Changes

The version is in `VERSION`; each problem file says in `added` which version first had it. A problem's best known
value can change within a version when its source table changes; the file then says when the value was read.

## v2.1, 12 Nov 2026: five cage cells re-read

- The House of Graphs cage table, re-read on 12 Nov 2026, now lists S. Taghiyev's graphs [T26] (Zenodo 10.5281/zenodo.24060986,
  records 24114698 and 24121626) in five of our cage cells: n(6,9) <= 3422, n(7,9) <= 9324, n(6,10) <= 6250, n(5,11) <= 2656
  and n(16,7) <= 7920. Those five problems now give these values as their best known (`kind: table entry`, read 12 Nov).
- cage-6-9 and cage-7-9 no longer call our graphs (5600 and 17600 vertices, 8 Nov 2026) the smallest known, and no longer
  list them as verified in review: they were the first graphs for those cells, and Taghiyev's smaller graphs (9 and 10 Nov)
  are now the table's values. Their entries in `leaderboard.json` stay as dated records of the check of 8 Nov.
  `test.sh` expects "does not improve" for both reference graphs.
- Not changed: the five cage problems whose best known value is implied by a (k,11)-graph the table showed on 8 Nov
  (cage-7-10, cage-8-9, cage-8-10, cage-9-9, cage-9-10). The table no longer shows those cells or their (k,11) bases (since
  autumn 2026 it lists a first value for an empty cell only for a graph of at most 10,000 vertices); smaller graphs for
  some of them are public on Zenodo. Their values stay as read on 8 Nov until a rule for cells the table does not list is
  chosen.

## Next (in review): Quantavane Open Tables, first version (12 Nov 2026)

- `collections/open-tables/`: benchmark tables for fields with no keeper of records, each cell with its best known
  value marked as published (with its source and the date read) or as a first entry (nothing comparable published);
  the two are counted apart and only beating a published value can be a record. Not counted in the totals.
- Topology, `unknotting` (67 cells): every prime knot of at most 11 crossings whose unknotting number KnotInfo gives as
  an interval (file of 2 Nov 2026, fetched by `fetch.sh` at a pinned commit with its SHA-256), less the 8 settled by
  McCoy and Park (arXiv:2603.10732, March 2026). Checker `checkers/unknot_check.py`: an unknotting sequence as Markov
  moves and crossing changes on KnotInfo's braid word, ending at the trivial braid; the value is the number of changes.
  Our certificates replay KnotInfo's upper bound for 66 cells (11n_138 not yet).
- Aerodynamics in a numerical model, `airfoil-ld` (20 cells: largest Cl/Cd by Reynolds number and thickness) and
  `airfoil-cd` (18 cells: least Cd at a required lift): checker `checkers/airfoil_check.py`, QV-Foil 1 (Hess-Smith
  panels, Thwaites, Michel, Head, Squire-Young; our own log, exp and arctangent, so the same result on every machine).
  A numerical model, not a wind tunnel. Every cell is a first entry with a NACA baseline.
- `obb.py`: a collection cell may carry a published value or a first entry (`open_table_cell`); `fetch.sh` fetches the
  KnotInfo file; `test.sh` runs `collections/open-tables/tests/test_open_tables.py`.

## Next (in review): Quantavane Originals

- `collections/originals/`: new open problems of ours, each with a novelty check written down before it was added, an
  exact checker of ours and a first value of ours (best known value, certificate, holder and date), in nine fields
  (astronomy added: `checkers/orig_astro.py`). A problem qualifies only when its question is new, not only its
  instance; candidates whose question had been studied are in `dropped.json` with the evidence.
  `dropped.json` lists the candidates dropped because they were already studied or settled. Not counted in the
  totals; `index.json` lists the folder as its own shard.
- `obb.py`: problems of a collection (`collections/NAME/problems/ID.json`) are found by `show`, `check` and `verify`
  and listed by `list NAME`; a checker may live in the collection (`collections/NAME/checkers/`), and arguments that
  start with `collections/` are read from the benchmark's folder.
- `test.sh` runs `collections/originals/tests/test_originals.py`.
- `collections/originals/cells/`: cells, counted the way the table families are: each question at every value of its
  natural parameter, one line per cell with its value, whether it is exact (an exhaustive search finished) or the best
  known, how it was found and its certificate (`refs/cells/ID/`). `tools/cells.py` writes them by running every
  certificate through the family's checker, so every value is one the checker proves. `index.json` counts the
  questions and the cells apart (`questions`, `cells`, `cells_exact`). `obb.py check` and `show` take a cell id (for
  example `y-array-20`), and `obb.py list originals` gives the number of cells.
- 10 Nov 2026, audit of every value the Originals publish: each headline value, each cell and each row of the
  first-values tables now has a certificate in the repository that passes its checker. A row is backed by its cell,
  by the headline certificate, or by a table certificate (`refs/table/ID/`, listed under `first_values.certified`).
  Rows that report someone else's value or no value say why (`first_values.context`). `tests/test_originals.py`
  (`tables()`) checks all of it. New checker modes, so that the context rows can be certified: the 5-, 8-, 16- and
  24-cells and the Gosset polytope 3_21 (`polytope-ising`), two subgraphs of the McLaughlin graph (`mclaughlin-sub`),
  the 600-cell's great circles (`cell600-great`) and induced paths in the 120-cell (`cell120-snake`). Corrections,
  each now showing the best value we can certify:
  - hp-tri, N = 3: the table said 0 (exact); the minimum is -1, since HPH folds into a triangle with one contact.
  - hp-tri, N = 34: -29 had no saved certificate and could not be reproduced (three runs of 300 and 600 seconds);
    the row now says -28.
  - overlap-square, the 8 x 8 grid: 0.5803 was a floating-point value before rounding, never certified; the certified
    value is 2459/4096 = 0.600342.
  - autoconv-square, the 8 x 8 grid: 2.34383 had no saved certificate and could not be reproduced (runs of 20,000 and
    60,000 steps); the row now says 351221187259904/149842105482001 = 2.343942.
  - Two columns of values without certificates were removed (the product functions of autoconv-square and the planar
    chains of cata-kemeny), with two such numbers from the cata-kemeny context.
  Values the audit runs improved: the coil in the 120-cell, 202 to 208 (the headline), and its longest snake (an
  induced path), 214 to 226; the three-part overlap,
  56061/200000 = 0.280305 to 268741/960000 = 0.279938 with 120 cells (the headline); the covering of the four-digit
  primes, 157 to 154; the autoconvolution ratio on the 16 x 16 grid, 2.26079 to 2.235115, and the three-part overlap
  with 24 cells, 0.28199 to 0.280310 (both had been floats without certificates). The values of align-ambiguity at
  n = 12 (4334, the pair printed in the table), nrm-segments at s = 8 (20) and tetra-distinct at n = 15 (13) were
  reproduced.
- 10 Nov 2026 (evening), new families, first batch: 24 new questions, each with its novelty check (arXiv API, OEIS,
  Crossref and web searches, kept in novelty/ID.json), an exact checker with red controls, and certified cells (exact
  where CP-SAT or an exhaustive search proved the optimum, every small exact cell also checked by brute force in the
  tests). Lattice point sets (checkers/orig_lattice.py, tools/lattice_sets.py): isosceles-free and right-angle-free
  sets in the triangular, honeycomb, kagome, tetrahedral (face-centred cubic) and body-centred cubic grids, and
  distinct distances in the honeycomb, kagome and body-centred cubic grids (13 questions). Invariants of the graphs of
  the six regular 4-polytopes and of the E8 polytopes 3_21 and 4_21 (checkers/orig_graphs.py, tools/polytope_sets.py):
  zero forcing, power domination, locating-dominating sets, induced matchings, L(2,1)-labellings, bandwidth, bisection
  width, total domination and 2-domination (9 questions). Colourings with no monochromatic solution
  (checkers/orig_colour.py, tools/colour_sat.py, tools/colour_exact.py): Pythagorean quadruples (two colours: exactly
  104, three SAT solvers agree; three colours: at least 473) and three squares in arithmetic progression (two colours:
  at least 22,948). Ten candidates dropped with the evidence (no three in line in the triangular and honeycomb grids,
  equilateral-free sets, distinct distances in the cubic grid, distinct areas in the square grid, the cubic-grid
  isosceles and right-angle questions, 1/x + 1/y = 1/z, 60-degree triangles, the maximum cut of Kneser graphs, the
  metric dimension of the 4-polytopes). tools/novelty.py also searches Crossref; the pages list those searches. 70
  questions, 1,251 cells (360 exact).

## 2.1 (9 Nov 2026): 149,372 problems and the Prestige 100 collection

- `collections/prestige100/`: Quantavane Prestige 100, one hundred famous open problems in which one checked object
  settles the score, chosen by fame and checkability: 20 two-colour and 4 multicolour Ramsey numbers, 10 Schur, weak
  Schur and van der Waerden numbers, the kissing numbers in the 25 open dimensions from 5 to 31, 3 x 3 and 4 x 4 matrix
  multiplication, Hadamard orders 668, 716 and 892, the Moore graph of degree 57, Conway's 99-graph, srg(88,27,6,9), a
  projective plane of order 12, three MOLS of order 10, Costas arrays of orders 32 and 33, 6 cages, 6 degree-diameter
  cells, sorting networks for 13 to 17 inputs, Golomb rulers with 29 and 30 marks, cap sets in dimensions 7 and 8, the
  snake in the 9-cube, the superpermutation on 6 symbols, Erdos problems #107 and #993, the constant C_1a, independent
  sets in the fifth power of C_7, no-three-in-line on the 75 x 75 grid and the Mona Lisa TSP. Every keeper read on
  9 Nov 2026; histories from the keepers (Small Ramsey Numbers revision 18, Leaps in Bounds at a5bbf82, H. Cohn's
  table, A. Kravatskiy's table, B. Dobbelaere, F. Comellas, A. E. Brouwer, T. Tao et al., A. Sedoglavic, W. Cook,
  erdosproblems.com, OEIS, K. Drakakis). `tools/build_prestige100.py` builds the pages, `index.json` and
  `leaderboard.json` from `curation.json` and the problem files, and checks them.
- 21 new single problems (Costas 32 and 33, Moore 57, srg(99,14,1,2), srg(88,27,6,9), projective plane 12, MOLS 10,
  matmul 3x3x3 and 4x4x4, Mona Lisa TSP, Erdos #107 and #993, kissing numbers in dimensions 22, 23, 25-31) and eight
  checkers (`costas_check.py`, `srg_check.py`, `projplane_check.py`, `mols_check.py`, `matmul_check.py`,
  `tsp_check.py`, `convex_check.py`, `tree_unimodal_check.py`), unit-tested in `tests/units_prestige.py`.
- Record certificates replayed by our checkers on 9 Nov 2026 and in `test.sh`: Nagata's Mona Lisa tour (5,757,191),
  Laderman's <3x3x3:23> and the catalogue's <4x4x4:48> (rational coefficients), Dobbelaere's networks for 13 to 17
  inputs (45, 51, 56, 60, 71), Kalbfleisch's, Mathon's and Burling and Reyner's colourings for R(6,6) >= 102,
  R(7,7) >= 205 and R(8,8) >= 282 (from Leaps in Bounds), McKenna's S(6) >= 538, our WS(7) >= 2154, WS(8) >= 7002 and
  WS(9) >= 22620, and our C_1a <= 1.5027427375 (pull request #346, in review).
- Values read again on 9 Nov 2026: `schur-6` 537 -> 538 (McKenna); `weak-schur-7`, `-8`, `-9` now ours (2154, 7002,
  22620; certificates merged by Leaps in Bounds, pull request #50); `1a-upper` gains our value in review.
- `fetch.sh` fetches the record certificates and the Mona Lisa instance before the CVRPLIB instances.

## 2.0 (9 Nov 2026): 149,351 problems

- Families: one statement and one checker applied to a whole table kept by someone else, one cell per entry of the
  table (`families/NAME/family.json` and `families/NAME/cells.jsonl`). A cell holds its parameters, the best known
  value read from the table, the bound on the other side, and who holds the value when the table names them; the
  family holds the keeper, the address, the date read, the revision read, how open cells were chosen and what was left
  out. 148,977 cells in six families: `project-scheduling` 59,170 (RCPSP, Solutions Update, Ghent University),
  `covering-design` 55,985 (Covering Repository), `linear-code` 15,255 (codetables.de), `spherical-code` 14,782 (H.
  Cohn's table), `covering-array` 2,651 (ca-tools) and `constant-weight-code` 1,134 (A. E. Brouwer's table). 2,655
  cells hold a value of ours (`quantavane_record`). Cells that are already single problems stay single problems.
- `index.json`: the folder of single problems and the six cell files, each with its count and SHA-256.
- `obb.py`: new commands `families`, `show`, `sample` and `index`; `list FAMILY`, `check` and `verify` take family
  cells; `list` without a family prints the single problems and the size of each family.
- New checkers: `ca_check.py` (covering arrays), `lincode_check.py` (exact minimum distance of linear codes over
  GF(q), q <= 9) and `rcpsp_check.py` (project schedules in Patterson, PSPLIB and NetRes formats).
- `covering_check.py`: same command and output (and a last line `RESULT B`); for t = m a bit array of ranks instead of
  a set of tuples, for m > t an exact branch-and-bound search that finishes on designs where the v1 search did not.
- Tests: `tests/units.py` (known objects with their exact values, red controls, cross-checks against brute force) and
  `tests/sample_cells.py` (a few random cells of every family: an object of ours that must be certified and must not
  improve, and a red control that must be refused); `test.sh` runs both and checks `index.json`.
- `tools/import_families.py` rebuilds every family from the saved table files.

## 1.1 (8 Nov 2026): 374 problems

- 257 new problems, each with an exact checker of ours:
  - 90 Ramsey lower bounds R(s,t) from Small Ramsey Numbers (revision 18): every open cell of Table Ia (s <= 10,
    t <= 15) not already here, blank cells included with the value the survey's inequalities imply, and 31 cells of
    Table IIa (t from 16 to 24); R(3,18) >= 101 is ours.
  - 14 multicolour Ramsey numbers (Tables XIa and XIb of the same survey), 40 cages (House of Graphs), 20
    degree-diameter cells (F. Comellas's table), 16 kissing numbers (H. Cohn's table, dimensions 5 to 21), 21
    sorting networks (B. Dobbelaere's list, 13 to 33 inputs), 10 van der Waerden numbers, 4 Schur and 5 weak Schur
    numbers, 5 snakes and 5 coils in the box, 2 cap sets, 4 superpermutations, 2 Golomb rulers, 2 no-three-in-line
    grids, 4 Hadamard orders (668, 716, 892, 1132), 12 circulant weighing matrices open in D. Gordon's repository and
    independent sets in the fifth strong power of C_7.
- 15 new checkers (`cage_check.py`, `degdiam_check.py`, `kissing_check.py`, `sortnet_check.py`, `vdw_check.py`,
  `schur_check.py`, `snake_check.py`, `capset_check.py`, `superperm_check.py`, `golomb_check.py`,
  `no3line_check.py`, `hadamard_check.py`, `cwm_check.py`, `strongpow_check.py`, `multiramsey_check.py`), all
  standard-library Python. Each ends its output with `RESULT v` (an integer or p/q) and exits 0 only for a valid
  certificate: the value kind `result` in `obb.py`, which every later checker will use too.
- R(4,18): best known now 210 (R(4,18) >= 211, ours, 8 Nov 2026).
- Every problem file now has `family`, `score` (what the value means), `added`, and `best_known.provenance`: the
  keeper of the source table, its address, the date the value was read, the revision or commit read, and who holds
  the value. Cells where the best known value is ours carry `quantavane_record`.
- `SUBMITTING.md` (the submission record), `obb.py verify` (checks a record and prints its leaderboard row),
  `leaderboard.json` and `obb.py leaderboard` (verified results, with credit).
- `fetch.sh` also downloads 45 certificates from Leaps in Bounds (MIT licence) at a pinned commit; `test.sh` replays
  them, checks our references and classical constructions, and runs red controls for every new checker.

## 1 (6 Nov 2026): 117 problems

7 constants from the optimization constants repository, 43 Ramsey lower bounds, 11 spherical codes, 10 covering
designs, 14 CVRPLIB routing instances and 32 constant weight codes. Later: R(5,15) and R(8,12) values updated (6 Nov);
`ramsey_check.c` rejects rows wider than 2048 characters before copying them (8 Nov).

## 0 (5 Nov 2026): 47 problems

4 constants (1a, 1c, 1d, 68a) and 43 Ramsey lower bounds (every cell raised since revision 18 of Small Ramsey
Numbers).
