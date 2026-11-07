# Open Problems Benchmark (v1)

Open problems with an exact checker each. A submission scores the exact value its checker proves, and it improves a
problem when that value beats the best known one. Two reference values are kept apart for every problem: the best
value on the source page (with its source) and the best verified value still in review (a pull request whose
certificate we replayed independently). Values are compared exactly; a printed value whose exact original is unknown
counts only when beaten by more than its last printed digit.

    python3 -I obb.py list
    python3 -I obb.py check 1c-lower submission.json
    ./fetch.sh && ./test.sh        # the reference submissions and the expected verdicts

v1 problems (6 Nov 2026), 117 in all:
- 7 constants from the optimization constants repository (teorth/optimizationproblems): 1a-upper, 1c-lower,
  1d-upper (step-function autocorrelation constants), 68a-lower (Korenblum's constant, moment certificates for two
  known envelopes), 42a-upper (Turán's pure power-sum constant), 59a-upper (Bohr radius of the bidisc) and 16a-lower
  (Brezis-Gallouet-Wainger remainder constant on the torus).
- 43 Ramsey lower bounds R(s,t): every cell raised since revision 18 of Small Ramsey Numbers (Radziszowski), with
  its best known value read on 5 Nov 2026, direct colourings and recursion-implied values alike (a submission must
  beat the larger), checked by our Bron-Kerbosch program (ramsey_check.c, n <= 2048).
- 11 spherical codes, one in each of the dimensions 3, 4, 5, 6, 8, 10, 12, 16, 20, 24 and 32 (Henry Cohn's table),
  scored by the largest cosine in 50-digit decimal arithmetic.
- 10 covering designs from the Covering Repository: five C(v,k,t) and five C(v,k,t,m).
- 14 vehicle routing instances from CVRPLIB: 9 Belgian instances of Arnold, Gendreau and Sörensen (6,000 to 30,000
  customers) and 5 of the XL set, distances rounded exactly in integers.
- 32 constant weight codes A(n,d,w) from Andries Brouwer's table (n from 27 to 60, d = 4 or 6, w = 5 or 6).
Every best known value was read from its source on the date given in the problem file. For the spherical codes,
covering designs, routing instances and constant weight codes the best known entry is currently ours (for A(34,6,6),
our code with 10 words added by Brouwer), and our result is the reference submission, in `refs/`.
Next: more constants (C82, C86, C44, C70, C49), prime gaps, linear codes, scheduling instances.

Checkers are Quantavane's own code (MIT, see LICENSE), standard library only (and a C compiler for the Ramsey
checker). Each problem file in `problems/` states its objective, its checker, both reference values and their sources.

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

## Submitting

Open an issue or a pull request with your certificate in the problem's format (the reference submissions show each
format: ours in `refs/`, the others fetched into `certs/` by `fetch.sh`, which also fetches the CVRPLIB instances
into `instances/`) and say where the construction comes from. We run the checker, record the exact value, and list
the result with your name and source. A submission that improves a problem is also worth sending to
the keeper of the source table; we can help with that.

## Quantavane Open Research

Anyone who can program and likes hard problems can work on these problems with us: find a better object, replay a
certificate with your own checker, or make one of our searches faster or better on its own test problems. Every
accepted result carries your name on the results page and in the table it enters, and a paper that uses your result
lists you as a co-author. You choose how your name appears: your name or a handle. To start, open an issue here or
write to arhan@quantavane.com. Details: https://quantavane.com/open-research/
