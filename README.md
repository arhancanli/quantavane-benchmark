# Open Problems Benchmark (v0, private draft)

Open problems with an exact checker each. A submission scores the exact value its checker proves, and it improves a
problem when that value beats the best known one. Two reference values are kept apart for every problem: the best
value on the source page (with its source) and the best verified value still in review (a pull request whose
certificate we replayed independently). Values are compared exactly; a printed value whose exact original is unknown
counts only when beaten by more than its last printed digit.

    python3 -I obb.py list
    python3 -I obb.py check 1c-lower submission.json
    ./fetch.sh && ./test.sh        # the reference submissions and the expected verdicts

v0 problems (5 Nov 2026), 47 in all:
- 4 constants from the optimization constants repository (teorth/optimizationproblems): 1a-upper, 1c-lower,
  1d-upper (step-function autocorrelation constants) and 68a-lower (Korenblum's constant, moment certificates for
  two known envelopes).
- 43 Ramsey lower bounds R(s,t): every cell raised since revision 18 of Small Ramsey Numbers (Radziszowski), with
  its best known value read on 5 Nov 2026, direct colourings and recursion-implied values alike (a submission must
  beat the larger), checked by our Bron-Kerbosch program (ramsey_check.c, n <= 2048).
Next: C82, C86, C44, C70, C49; covering arrays, spherical codes, covering designs, prime gaps, codes.

Checkers are Quantavane's own code (MIT), standard library only. Draft: nothing here is public yet.
