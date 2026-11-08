# Open Problems Benchmark (v1.1)

Open problems with an exact checker each. A submission scores the exact value its checker proves, and it improves a
problem when that value beats the best known one. Two reference values are kept apart for every problem: the best
value on the source page (with its source) and the best verified value still in review (for instance a pull request
whose certificate we replayed independently). Values are compared exactly; a printed value whose exact original is
unknown counts only when beaten by more than its last printed digit.

    python3 -I obb.py list [FAMILY]
    python3 -I obb.py check 1c-lower submission.json
    python3 -I obb.py verify record.json     # a submission record (SUBMITTING.md) and the leaderboard row it earns
    python3 -I obb.py leaderboard             # the verified results in leaderboard.json
    ./fetch.sh && ./test.sh                   # the reference submissions, red controls and the expected verdicts

v1.1 problems (8 Nov 2026), 373 in all:
- 7 constants from the optimization constants repository (teorth/optimizationproblems): 1a-upper, 1c-lower,
  1d-upper (step-function autocorrelation constants), 68a-lower (Korenblum's constant, moment certificates for two
  known envelopes), 42a-upper (Turán's pure power-sum constant), 59a-upper (Bohr radius of the bidisc) and 16a-lower
  (Brezis-Gallouet-Wainger remainder constant on the torus).
- 133 Ramsey lower bounds R(s,t) from Small Ramsey Numbers (Radziszowski, revision 18): every open cell of its Table
  Ia (s <= 10, t <= 15), 31 cells of its Table IIa (t from 16 to 24), and every cell raised since revision 18, with the best
  known value read on 5 or 8 Nov 2026. Blank cells carry the value the survey's own inequalities give; recursion-
  implied values count like colourings (a submission must beat the larger). Checked by our Bron-Kerbosch program
  (ramsey_check.c, n <= 2048).
- 14 multicolour Ramsey numbers from Tables XIa and XIb of the same survey, among them R(3,3,3,3), R(4,4,4),
  R(5,5,5) and R_7(3).
- 39 cages n(k,g) from the House of Graphs cage table, among them the cubic cages of girth 13 to 20 and cells the
  table leaves blank (their value then comes from monotonicity in the girth).
- 20 cells of the degree-diameter problem (F. Comellas's table), 16 kissing numbers (H. Cohn's table, dimensions 5 to
  21), 21 sorting networks with the fewest comparators (B. Dobbelaere's list, 13 to 33 inputs; Green's 60-comparator
  network for 16 inputs has stood since 1969).
- 10 van der Waerden numbers, 4 Schur and 5 weak Schur numbers, 5 snakes and 5 coils in the box, 2 cap sets, 4
  superpermutations, 2 Golomb rulers and 2 no-three-in-line grids, with the values kept by Leaps in Bounds
  (leapsinbounds.org, D. Munro).
- 4 Hadamard orders with no known matrix (668, the smallest, then 716, 892, 1132), 12 circulant weighing matrices
  open in D. Gordon's La Jolla repository, and independent sets in the fifth strong power of C_7 (Shannon capacity).
- 11 spherical codes, one in each of the dimensions 3, 4, 5, 6, 8, 10, 12, 16, 20, 24 and 32 (Henry Cohn's table),
  scored by the largest cosine in 50-digit decimal arithmetic.
- 10 covering designs from the Covering Repository: five C(v,k,t) and five C(v,k,t,m).
- 14 vehicle routing instances from CVRPLIB: 9 Belgian instances of Arnold, Gendreau and Sörensen (6,000 to 30,000
  customers) and 5 of the XL set, distances rounded exactly in integers.
- 32 constant weight codes A(n,d,w) from Andries Brouwer's table (n from 27 to 60, d = 4 or 6, w = 5 or 6).

Every best known value was read from its source on the date given in the problem file, whose `best_known.provenance`
names the keeper of the table, the revision or commit read, the date and who holds the value. Where the best known
value is ours the file says so (`quantavane_record`): the spherical codes, covering designs, routing instances and
constant weight codes (for A(34,6,6), our code with 10 words added by Brouwer), R(3,18), R(4,18), R(5,15) and
R(8,12), and the cages n(6,9) <= 5600 and n(7,9) <= 17600 (sent to House of Graphs, not listed yet). Our results are
the reference submissions, in `refs/`, with classical constructions built by our code; other authors' certificates,
including 45 from Leaps in Bounds (MIT licence), are fetched into `certs/` by `fetch.sh` at pinned commits.
Changes from version to version are in CHANGELOG.md.

Checkers are Quantavane's own code (MIT, see LICENSE), standard library only (and a C compiler for the Ramsey
checker). Each problem file in `problems/` states its objective, its checker, what the score means, both reference
values and their sources.

## The checkers on their own

Each checker in `checkers/` is one file that can be used without the benchmark: Python standard library only, run
with `python3 -I`, except the Ramsey checker, which is C (`cc -O3 -o ramsey_check checkers/ramsey_check.c`). Each
prints its exact result and exits 0 only for a valid certificate.

- `ramsey_check S T FILE`: a two-colouring of K_n as an n x n 0/1 matrix (1 red, 0 blue) has no red K_S and no blue
  K_T (Bron-Kerbosch with Tomita's pivot and a colouring bound; n <= 2048).
- `sph_check.py FILE D N`: the largest cosine between N points on the sphere in R^D, in 50-digit decimal arithmetic.
- `covering_check.py V K T M FILE`: covering designs C(V,K,T) (M = T) and C(V,K,T,M), by an exact search for an
  uncovered M-subset.
- `cw_check.py N D W FILE`: binary constant weight codes, length N, weight W, distance at least D.
- `cvrp_check.py INSTANCE.vrp SOLUTION.sol`: capacitated vehicle routing in CVRPLIB's formats, distances rounded
  exactly in integers.
- `autocorr_check.py 1a|1c|1d FILE`: step-function certificates for the autocorrelation constants C_1a, C_1c and
  C_1d, in exact rational arithmetic.
- `c68_check.py FILE`: the moment certificates behind lower bounds on Korenblum's constant.
- `c42_check.py FILE`: upper bounds on Turán's pure power-sum constant from a block certificate.
- `c59_check.py FILE`: upper bounds on the Bohr radius of the bidisc.
- `c16_lower.py FILE`: rigorous enclosures of lower bounds on the Brezis-Gallouet-Wainger remainder constant on the
  torus, with `c16_check.py` and `c16_trunc_check.py` for the published certificates.

The checkers added in v1.1 end their output with a line `RESULT v`, the exact value proved (an integer or p/q), and
read the formats of the source tables (graph6 and sparse6 for graphs, as on House of Graphs; the witness formats of
Leaps in Bounds):

- `multiramsey_check.py S_1 ... S_r FILE`: an r-colouring of K_n, colour c without K_(S_c) (branch and bound on bit
  sets).
- `cage_check.py K G FILE`: a K-regular simple graph of girth at least G (breadth-first search from every vertex).
- `degdiam_check.py DELTA D FILE`: maximum degree at most DELTA and diameter at most D (balls kept as bit sets).
- `kissing_check.py D FILE`: integer vectors of one squared norm N, inner products at most N/2, spanning dimension at
  most D (all inner products exactly, by big-integer packing).
- `sortnet_check.py N FILE`: a comparator network that sorts every 0-1 input (the inputs after the first layer run
  bit-sliced).
- `vdw_check.py R K FILE`, `schur_check.py schur|weak K FILE`: colourings without monochromatic K-term progressions,
  or without monochromatic solutions of x + y = z.
- `snake_check.py snake|coil D FILE`, `capset_check.py N FILE`, `superperm_check.py N FILE`, `golomb_check.py M FILE`,
  `no3line_check.py N FILE`, `strongpow_check.py M K FILE`: induced paths and cycles in the hypercube, cap sets in
  F_3^N, superpermutations, Golomb rulers, no-three-in-line sets and independent sets in strong powers of cycles.
- `hadamard_check.py N FILE` and `cwm_check.py N K FILE`: Hadamard matrices (H H^T = N I) and proper circulant
  weighing matrices (W W^T = K I).

## Submitting

Send the certificate in the problem's format with a short record (SUBMITTING.md): who you are, how the object was
found and whether an AI system helped. Open an issue or a pull request, or write to arhan@quantavane.com. We run the
checker, record the exact value, and add the result to `leaderboard.json` with your name or handle. A submission that
improves a problem is also worth sending to the keeper of the source table; we can help with that.

`leaderboard.json` lists the verified results that reach or beat a best known value, each with its holder and the
date we checked it; `python3 -I obb.py leaderboard PROBLEM` shows one problem.

## Quantavane Open Research

Anyone who can program and likes hard problems can work on these problems with us: find a better object, replay a
certificate with your own checker, or make one of our searches faster or better on its own test problems. Every
accepted result carries your name on the results page and in the table it enters, and a paper that uses your result
lists you as a co-author. You choose how your name appears: your name or a handle. To start, open an issue here or
write to arhan@quantavane.com. Details: https://quantavane.com/open-research/
