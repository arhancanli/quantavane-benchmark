# Changes

The version is in `VERSION`; each problem file says in `added` which version first had it. A problem's best known
value can change within a version when its source table changes; the file then says when the value was read.

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
