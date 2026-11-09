# Changes

The version is in `VERSION`; each problem file says in `added` which version first had it. A problem's best known
value can change within a version when its source table changes; the file then says when the value was read.

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
