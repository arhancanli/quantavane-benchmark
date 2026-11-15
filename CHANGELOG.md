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

## Next (in review): the families `circulant-degree-diameter` and `bipartite-degree-diameter` (15 Nov 2026)

- `checkers/circulant_check.py` (new, with the C helper `checkers/circulant_bfs.c`): circulant graphs given by n and
  their jumps; degree and diameter (one breadth-first search from 0, bit-parallel in C above 10^6 vertices).
  `checkers/degdiam_check.py --bipartite`: the graph must also be bipartite. `tests/test_circulant.py` (run by
  `test.sh`): optimal degree-4 circulants pass and fail one diameter lower, in Python and C; the two agree on 150
  random graphs; repeated jumps, too large degrees and disconnected graphs are refused; even and odd cycles.
- `families/circulant-degree-diameter` (170 cells) and `families/bipartite-degree-diameter` (32 cells;
  `tools/combwiki_dd_cells.py`): the Combinatorics Wiki's tables, read 15 Nov 2026, entries not in bold (bipartite: at
  most 20,000 vertices). Sampled cells: C_(2mk+1)(1..m) and even cycles pass; one diameter too many and odd cycles fail.
- index.json: 359,848 problems.

## Next (in review): the family `signed-difference-set` from Gordon's repository (15 Nov 2026)

- `checkers/ds_check.py --signed`: signed difference sets (each element with a sign; for every nonzero g the signed
  count of ordered pairs with difference g must be lambda; the trivial character's condition is checked first).
  `tests/test_ds.py`: three known signed sets pass, and fail with a sign flipped or an element moved.
- `families/signed-difference-set` (22,325 cells; `tools/gordon_cells.py`, which now takes sds.json as well): every
  Open entry of the La Jolla Signed Difference Set Repository, release v2.0 (Zenodo record 24170597, downloaded 15 Nov
  2026), one cell per parameter set and abelian group. All 176 signed sets of the release pass the checker.
- index.json: 359,646 problems.

## Next (in review): the families `difference-set` and `circulant-weighing-matrix` from Gordon's repositories (15 Nov 2026)

- `checkers/ds_check.py` (new): difference sets in abelian groups, every ordered pair's difference counted exactly; in C
  above 10^6 pairs (`checkers/ds_scan.c`: the group rewritten as a product of the fewest cyclic groups; XOR for Z_2^r,
  one subtraction modulo v for cyclic groups, a padded rank with no borrows otherwise, and digit by digit on request).
  `tests/test_ds.py` (run by `test.sh`): ten known sets pass by all three routes and fail with an element moved or
  repeated; the routes agree on 40 random subsets; a Paley set in Z_4999 is counted in C by default.
- `families/difference-set` (102,628 cells; `tools/gordon_cells.py`): every Open entry of the La Jolla Difference Set
  Repository, release 1.3 (Zenodo record 19740740, downloaded 15 Nov 2026), one cell per parameter set and abelian
  group; 91 open entries whose check would take more than ten minutes are left out.
- `families/circulant-weighing-matrix` (2,617 cells; same tool): every Open entry CW(n,s) of the La Jolla Circulant
  Weighing Matrices Repository, release v2.0 (Zenodo record 24170503, downloaded 15 Nov 2026), checked by `cwm_check.py`.
- Removed: seven single problems of v1.1 that release v2.0 settles. cwm-105-36, cwm-120-49 and cwm-140-64 (no such
  matrix: Tan, arXiv:2608.18468, 2026), cwm-155-25, cwm-165-25 and cwm-186-25 (none: Leung and Ma), cwm-96-36 (exists:
  Schmidt and Smith, 2013). They were Open in cwm.json at commit 5b3d729 (24 Apr 2026), read on 8 Nov. `test.sh` now
  refuses the zero row for cwm-112-36 in place of cwm-155-25.
- `tests/sample_cells.py` samples both families (random k-subsets, random rows of weight s^2 and the zero row refused).
- index.json: 337,321 problems (388 single problems).

## Next (in review): the family `strongly-regular-graph` from Brouwer's table (15 Nov 2026)

- `families/strongly-regular-graph` (1,356 cells; `tools/brouwer_srg_cells.py`): every parameter set with v <= 1,300
  that A. E. Brouwer's table of strongly regular graphs marks '?' (existence unknown), read 15 Nov 2026 (26 pages,
  SHA-256 of each in the family file), one cell per set and its complement; srg-88-27-6-9 and srg-99-14-1-2 stay
  single problems. Checked by `srg_check.py` (a valid graph scores 1). `tests/sample_cells.py`: Paley graphs P(13),
  P(29), P(37) and triangular graphs T(6), T(9) pass, the Paley graphs with an edge moved fail, and k-regular circulants
  are refused for sampled cells.
- index.json: 232,083 problems.

## Next (in review): covering designs with m > t searched in C (15 Nov 2026)

- `checkers/covering_check.py`: for m > t with more than 40 blocks (v <= 128) the search for a bad m-subset runs in C
  (`checkers/covering_lotto.c`), the same search step for step, so the same nodes and the same bad set; `--python` and
  `--native` force one way. `tests/test_covering.py`: 200 random block sets (half repaired into valid designs) give the
  same verdict and bad set both ways; our five reference designs pass both ways; all 2,002 5-subsets of 1..14 as a
  C(14,5,3,5) design pass in C and, with the blocks meeting {1..5} in 3 or more points removed, are refused.
- `families/covering-design`: the m > t entries with more than 1,000 blocks enter when a pessimistic estimate of the
  search stays under an hour (`lotto_check_hours`): 4,212 cells, 61,394 in all; 8,891 stay out. Same export (14 Nov
  2026); the 57,182 earlier cells are unchanged. `tests/sample_cells.py` samples the new cells (a greedy t-covering in
  C; red control: the blocks meeting one m-subset in t or more points removed).
- index.json: 230,727 problems.

## Next (in review): the family `golomb-ruler` from Rokicki and Dogon's table (15 Nov 2026)

- `checkers/golomb_check.py`: above 3,000 marks the differences are marked in C (`checkers/golomb_scan.c`, a bit array).
  `tests/test_golomb.py` (run by `test.sh`): Erdos-Turan rulers on both sides of the threshold with red controls.
- `families/golomb-ruler` (39,970 cells, 31 to 40,000 marks without the single problems 29 and 30;
  `tools/golomb_cells.py`): Rokicki and Dogon's 41 metadata files read on 15 Nov 2026. Their explicit rulers for 5 to
  999 marks agree with the metadata; seven of them certify the listed lengths through obb.py. `tests/sample_cells.py`
  samples the family (an Erdos-Turan ruler; a repeated difference as the red control).
- index.json: 226,515 problems.

## Next (in review): the families `job-shop` and `flexible-job-shop` from ScheduleOpt's libraries (15 Nov 2026)

- New exact checker `checkers/jsp_check.py`: job shop schedules (start times) and flexible job shop schedules (machine
  and start time of each operation), precedences and machines checked in integers, the makespan as the value.
  `tests/test_jsp.py` (run by `test.sh`): hand-made schedules with red controls, 30 random job shops with greedy
  schedules and overlapping copies.
- `families/job-shop` (60 cells) and `families/flexible-job-shop` (53 cells; `tools/scheduleopt_cells.py`): open
  instances of ScheduleOpt's bks.json files at commit 8a6e36e, cross-checked with O. Shylo's tables for the job shop;
  fetch.sh downloads the 113 instance files with their SHA-256 (before the CVRPLIB downloads). `tests/sample_cells.py`
  samples both families when the instances are present. Shylo's ta43 schedule reproduces the best known 1846.
- index.json: 186,545 problems.

## Next (in review): the family `degree-diameter` from Comellas's table (15 Nov 2026)

- `families/degree-diameter` (37 cells; `tools/comellas_cells.py`): the entries of F. Comellas's table read on 15 Nov
  2026 that are not optimal, have at most 20,000 vertices and are not among the 20 single problems; checked by the
  existing `degdiam_check.py`. `tests/sample_cells.py` samples the family (a cycle of 2D + 1 vertices; a cycle of
  2D + 3 vertices as the red control).
- index.json: 186,432 problems.

## Next (in review): the family `lj-cluster` from the Cambridge Cluster Database (15 Nov 2026)

- New checker `checkers/cluster_check.py`: the Lennard-Jones energy of a cluster, every coordinate read exactly and
  every pair's term an exact fraction rounded up, printed as a proven upper bound within 10^-12. `tests/test_cluster.py`
  (run by `test.sh`): exact values for two and three atoms, red controls, the bound against Fraction arithmetic.
- `families/lj-cluster` (137 cells, N = 14..150; `tools/ccd_cells.py`): Wales and Doye's table, read 15 Nov 2026
  (unchanged since 1 Nov). `tests/sample_cells.py` samples the family; the database's coordinates for N = 77 give
  "does not improve".
- index.json: 186,395 problems.

## Next (in review): the family `orthogonal-array` (MinT, arrays of any kind) (15 Nov 2026)

- New exact checker `checkers/oa_check.py` with the C helper `checkers/oa_scan.c`: an ordered orthogonal array or net
  given run by run, every choice of depths of weight K tested for uniformity. `tests/test_oa.py` (run by `test.sh`):
  linear objects written out run by run give the verdict of `ooa_check.py` (both ways), a Latin square of order 6 as
  OA(36; 2, 3, 6) with red controls, malformed inputs.
- `families/orthogonal-array` (249 cells; `tools/mint_arb_cells.py`): MinT's cells for arbitrary objects (pages of
  14 Nov 2026) that are open, have at most 2^16 runs, check within 2^33 steps and differ in best known value or bound
  from the linear cell; `tests/sample_cells.py` samples the family.
- index.json: 186,258 problems.

## Next (in review): the family `unrestricted-code` from A. E. Brouwer's tables (15 Nov 2026)

- New exact checker `checkers/ucode_check.py` with the C helper `checkers/ucode_scan.c`: a code over one alphabet or
  mixed alphabets (sizes 2 to 8, up to 64 coordinates) with minimum distance D; every pair of words is compared.
  `tests/test_ucode.py` (run by `test.sh`): the Hamming code and the tetracode both ways with red controls, malformed
  words, 60 random mixed codes with the same verdict both ways, 4,096 words through C.
- `families/unrestricted-code` (352 cells; `tools/brouwer_codes_cells.py`): open entries of A_2(n,d), A_3(n,d),
  A_4(n,d), A_5(n,d) (123) and N(m,n,d) with m, n >= 1 (229), pages read 15 Nov 2026, lower bounds below 2^17.
  `tests/sample_cells.py` samples the family.
- index.json: 186,009 problems.

## Next (in review): the family `ea-quantum-code` from eaqecc.codetables.de (15 Nov 2026)

- `checkers/qcode_check.py --ebits C`: entanglement-assisted codes [[N,K;C]] over GF(Q) (generators need not commute;
  span Q^(N-K+C), form of rank 2C; distance as in Luo, Ezerman, Grassl and Ling, arXiv:2207.05647, Proposition 1).
  `tests/test_qcode.py`: 75 random generator sets against brute force, trivial codes, [[4,1,3;1]] by teleportation,
  red controls (a stabilizer code claimed with an ebit, a non-commuting set claimed as a stabilizer code).
- `families/ea-quantum-code` (3,263 cells: 2,388 qubit, 875 qutrit; `tools/eaqcode_cells.py`): Grassl's tables read on
  15 Nov 2026 (last changed 10 Jul 2025), entries with c >= 1, open, within 2^34 (qubits) or 2^31 (qutrits) steps.
  `tests/sample_cells.py` samples the family.
- index.json: 185,657 problems.

## Next (in review): the depth-vector walk in C for odd bases (15 Nov 2026)

- `checkers/ooa_walk_p.c`: method D of `ooa_check.py` for GF(3), GF(5), GF(7), GF(9), GF(25), GF(27), GF(49), GF(81),
  with each vector kept as e digit planes and every operation done digit-wise modulo p (about 2 x 10^7 steps a second
  for p = 3, 5, 7). `tests/test_ooa.py`: the walk in C against Python on random objects over every base, and
  `--native` against the definition over GF(3), GF(5), GF(7), GF(9) (703 checks).
- `families/ordered-orthogonal-array`: caps of 2^31 steps (b = 3, 5, 7), 2^29 (b = 9, 25, 49) and 2^28 (b = 27, 81)
  for the walk in C: 4,709 cells (552 new: 306 for b = 3, 125 for b = 5, 80 for b = 7, 41 for the extension fields).
- index.json: 182,394 problems.

## Next (in review): Packomania, third part: polygons and radical radii (15 Nov 2026)

- New exact checker `checkers/pack_alg_check.py` (standard library only) for packings whose container or radii are
  irrational: equal circles in the regular n-gons (n = 5..17) and circles of radii i^(1/2), i^(-1/2), i^(-2/3),
  i^(-1/5) (circle) and i^(1/2), (N/i)^(1/2) (square). Every condition is decided exactly: rational enclosures narrowed
  until they decide, and equality by algebra (cyclotomic reduction for polygons; for radicals, equality forces the
  radicals to be rational, and is then computed exactly).
- New families `polygon-circle-packing` (1,106 cells) and `unequal-circle-packing` (578 cells) from the pages read on
  14 Nov 2026 (`tools/packomania_alg_cells.py`), with frames checked on Packomania's coordinate files for 11 sections.
- `tests/test_pack_alg.py` (run by `test.sh`, 48 checks): each polygon's apothem from both sides, exact touching
  (an edge of the hexagon; sqrt 2 + sqrt 8 = sqrt 18; radii 1 and 8^(-2/3) = 1/4), containers from both sides,
  malformed inputs; `tests/sample_cells.py` samples both families.
- index.json: 181,842 problems.

## Next (in review): ordered orthogonal arrays walked in C (15 Nov 2026)

- `checkers/ooa_check.py`: for B = 2, 4, 8, ..., 256 and M <= 64, method D (every choice of depths with a running
  echelon basis) runs in the new C helper `checkers/ooa_walk.c` above 2^20 steps, with each vector kept as e bit planes
  and multiplication by a field element done as a linear map on the planes; `--native` and `--python` force one way.
  About 3 x 10^8 steps a second for B = 2, 7 x 10^7 for B = 4 and 10^7 for B = 256. `tests/test_ooa.py`: method D in C
  against Python on 400 random objects (verdict and number of depth vectors), and `--native` against the definition on
  60 objects (672 checks in all).
- `families/ordered-orthogonal-array` (same MinT pages of 14 Nov 2026; `tools/mint_cells.py`): a cell is kept when one
  more factor can be checked in 2^27 steps in Python or, for B = 2^e, in 2^34 (B = 2), 2^32 (B = 4, 8) or 2^30 (B = 16
  to 256) steps of the walk in C: 4,157 cells (2,600 before; 1,259 new for B = 2).
- index.json: 180,158 problems.

## Next (in review): covering arrays re-read and checked in C (15 Nov 2026)

- `checkers/ca_check.py`: above 5 x 10^7 row visits (C(K,T) x N) the new C helper `checkers/ca_scan.c` (built with
  `cc -O3` on first use) does the check: for each T-set of columns it numbers every row's tuple (sharing the first T-1
  columns' part) and marks it in a bit array of V^T bits. `--python` and `--native` force one way.
  `tests/test_ca.py` (run by `test.sh`): random arrays with the same verdict both ways, the orthogonal arrays
  OA(p^2; 2, p+1, p) for p = 3, 5, 7 with red controls (a row dropped, a symbol changed) both ways, a random
  CA(3000; 4, 60, 3) through C and its red control (a column repeated).
- `families/covering-array` re-read from ca-tools main at commit a2dd39e (15 Nov 2026 00:38 UTC; 15,583 rows) with the
  cap raised from 2 x 10^8 set intersections to 10^11 row visits: 4,731 cells (2,659 before; one cell left the
  staircase because a wider array now has fewer rows; 28 values improved, none got worse). 13 cells hold our own
  arrays (Canli 2026, partly cyclic covering perfect hash families, doi:10.5281/zenodo.23839216), which were above the
  old cap.
- index.json: 178,601 problems.

## Next (in review): covering designs re-read and checked in C (15 Nov 2026)

- `checkers/covering_check.py`: for C(v,k,t), above 2 x 10^7 t-subsets to mark, the new C helper
  `checkers/covering_mark.c` (built with `cc -O3` on first use) marks them, one largest point at a time in a bit array
  of C(v-1,t-1) bits. `--python` and `--native` force one way. `tests/test_covering.py` (run by `test.sh`): 60 random
  block sets with the same verdict and count both ways, greedy coverings and red controls both ways, and a covering of
  46.6 million marks with its red control.
- `families/covering-design` re-read from the Covering Repository's export of 14 Nov 2026 (529 values improved since
  8 Nov, none got worse, no cell closed) with the work cap for t = m raised from 10^8 to 10^10 marks: 57,182 cells
  (1,193 new C(v,k,t) cells, 4 new C(v,k,t,m) cells); 128 hold a value of ours, as before.
- index.json: 176,529 problems.

## Next (in review): Packomania, second part (15 Nov 2026)

- `checkers/pack_check.py`: sections crc100 to crc800 (equal circles in the rectangle [0,1] x [0,h], h = 0.1 to 0.8),
  sspn (balls of radii 1..N in the smallest ball) and csqv (circles of any radii in the unit square; the value is the
  sum of the radii, and pairs are tested by an exact sweep along x).
- `families/circle-packing`: 2,582 rectangle cells (pages read 15 Nov 2026, SHA-256 in the family file); 12,759 cells.
  `families/growing-circle-packing`: 97 sspn cells; 396 cells. New `families/circle-packing-sum`: 3,056 cells.
- Corrected: crt 166, crt 294 and hsp4 300 were each listed twice on their pages and counted twice; each is now one
  cell with the better value (hsp4 300: 0.187824804694, not 0.187648382196). Holders shown on the pages only as an image
  are named by the image's file name. The family files note Packomania's queue of unreviewed candidates.
- Frames checked on Packomania's coordinate files for crc100, crc800, csqv30 and sspn20; `tests/test_pack.py` has 15 new
  checks (touching packings and red controls for the new sections, 10,000 circles through the sweep);
  `tests/sample_cells.py` samples the rectangles, sspn and the new family.
- index.json: 175,332 problems.

## Next (in review): the family `quantum-code` from codetables.de (15 Nov 2026)

- New exact checker `checkers/qcode_check.py` (standard library only) with the C helper `checkers/qcode_enum.c`
  (built with `cc -O3` on first use): an additive quantum code [[N,K]] over GF(Q), Q in 2, 3, 4, 5, 7, 8, given by its
  stabilizer matrix. It checks that the rows commute in the trace-symplectic form and span exactly Q^(N-K) elements
  over the prime field, lists the stabilizer, and gets the weight counts of its trace-symplectic dual from the
  MacWilliams identity in exact integers; the distance is the least weight held by the dual and not by the stabilizer.
- `families/quantum-code` (7,141 cells, maximize the distance): Grassl's range tables read on 15 Nov 2026 (51 pages,
  SHA-256 of each in the family file; `tools/qcode_cells.py`). Kept: open entries whose check takes at most 2^34 steps
  (Q = 2, 4, 8) or 2^31 (Q = 3, 5, 7). Codes published after the tables' last change (`families/quantum-code/outside.json`)
  close 26 qubit cells, which are left out, and raise the best known value of 76 cells, credited to their authors.
- `tests/test_qcode.py` (run by `test.sh`): known codes, 36 random codes against brute force, the C helper against the
  Python lister, red controls (a changed entry, a dropped or repeated generator, an entry out of range, a short line).
  `tests/sample_cells.py` samples the family (single-qudit Z stabilizers; a generator dropped as the red control).
- index.json: 169,600 problems.

## Next (in review): the families `circle-packing` and `growing-circle-packing` from Packomania (14 Nov 2026)

- New exact checker `checkers/pack_check.py` (standard library only): circles or balls in a container, every number read as an exact decimal and every test (containment, and |c_i - c_j|^2 >= (r_i + r_j)^2 for the pairs in neighbouring cells of a grid of side 2 max r, which is exact) in integer arithmetic. Prints the value as an exact fraction.
- `families/circle-packing` (10,180 cells, maximize the radius) and `families/growing-circle-packing` (299 cells, minimize the container), read from the Packomania section pages on 14 Nov 2026 22:3x-22:5x +04 (SHA-256 of each page in the family files; `tools/packomania_cells.py`). A cell is an N whose value is not in bold (proven optimal).
- Frames checked on Packomania's own coordinate files (csq30, cci30, csc30, ccq30, crt30, scu30, ssp30 with its 29 listed centres, ccin10, csqn10): each passes just below the listed value and fails 10^-9 above it (10^-6 for the container size).
- `tests/test_pack.py` (run by `test.sh`): 22 checks, among them touching packings at the edge of validity with red controls one unit in the last decimal away, malformed inputs, and 10,000 touching circles. `tests/sample_cells.py` samples both families (a grid of equal circles in a box inside the container; radii 1..N in a row) with red controls.
- index.json: 162,459 problems.

## Next (in review): the family `ordered-orthogonal-array` from MinT (14 Nov 2026)

- New exact checker `checkers/ooa_check.py` (standard library only) for linear ordered orthogonal arrays over GF(b),
  b = 2, 3, 4, 5, 7, 8, 9, 16, 25, 27, 32, 49, 64, 81, 128, 256 (each extension field by its Conway polynomial; the
  program checks that x is primitive): orthogonal arrays (depth 1), ordered orthogonal arrays of depth 2 to 8 and
  digital nets. It reads a generator matrix and decides strength k by two separate methods: D walks every choice of
  depths of weight k with a running echelon basis and names the first dependent column; E lists the row space once per
  line through the origin, records the leading zeros of every factor, and computes the number of dual words of each
  weight 1..k in the Niederreiter-Rosenbloom-Tsfasman metric by a MacWilliams identity in exact integers.
- `tests/test_ooa.py` (run by `test.sh`): 612 checks. Hamming and extended Hamming arrays, Reed-Solomon arrays over
  GF(5), GF(9) and GF(16), a digital (0,4,2)-net, red controls (a repeated column, one entry changed, the same matrix
  twice), malformed inputs, and 596 random objects over nine fields on which methods D and E and a third program that
  counts every projection of the b^m runs (the definition) give the same verdict (422 with the strength, 174 without).
- New family `families/ordered-orthogonal-array` (2,600 cells, `added` 2.2), built by `tools/mint_fetch.py` (one
  request every six seconds; the pages are not stored here) and `tools/mint_cells.py` from MinT's tables for linear
  objects, read on 14 Nov 2026 11:27-11:39 UTC (MinT's database: 2024-09-05). Open rule, work limit and what is left
  out are in `family.json` and in the README. `tests/sample_cells.py` draws cells of the family, certifies an array of
  unit vectors for each and refuses the same array with a column repeated.
- `index.json` rebuilt: 151,980 problems (395 single problems and 151,585 family cells).

## Next (in review): Quantavane Open Tables, second version (13 Nov 2026): topology optimisation

- QV-Topo 1, `collections/open-tables/checkers/topopt_check.py` (standard library only): plane-stress linear elasticity
  on a fixed grid of square bilinear elements (Young's modulus 1, Poisson's ratio 0.3, void 1e-9), the 88-line code's
  element matrix, our own profile Cholesky solver with correctly rounded sums (the same digits on every machine), our
  own periodic homogenisation (energy method). The checker re-solves from the submitted design alone.
- `topopt-simp` (10 cells): least compliance of density fields in the SIMP model with the 88-line code's density
  filter (MBB beam, cantilever, L-bracket); the elements with density at least 1/2 must form one connected load path.
  Two cells, the 88-line paper's density-filter MBB beam on 60 x 20 and 150 x 50 elements, carry published values
  (233.71 and 235.73 in the paper's preprint, reproduced by our replay of its loop; 233.4878 for 60 x 20 in the
  PINNeAPPle project's results, GitHub, Oct 2026, the lowest found). Our first searches give 232.110 and
  233.714 for these two cells, below every value we found published for those settings; the other cells are first
  entries.
- `topopt-binary` (12 cells): 0/1 designs with a minimum feature size of 2 elements (volume 0.3, 0.4, 0.5) or 3
  (volume 0.5), no point contacts and one connected piece; all first entries.
- `metacell-bulk`, `metacell-shear`, `metacell-poisson` (11 cells): periodic 40 x 40 material cells (0/1, minimum
  feature size 2, connected in both directions): greatest bulk modulus (with the Hashin-Shtrikman bound), greatest shear
  modulus, most negative Poisson's ratio (uniaxial stress along either axis) with Young's moduli at least 0.01; all first
  entries.
- Searches (numpy, our code): optimality criteria and the method of moving asymptotes with the density filter;
  projection, threshold, morphological repair and a local search for 0/1 designs; rotating-square seeds for the Poisson
  cells. Tests: the element matrix, a plate in tension, a uniform cell and two laminates against their exact values,
  red controls, the same output twice, every certificate replayed.
- `obb.py`: an open-table cell may beat a published value (`record`), and a printed, rounded published value is beaten
  only by one unit of its last decimal.

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
