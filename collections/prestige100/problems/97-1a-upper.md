# 97. The autocorrelation constant C_1a (upper bound)

Family: Optimization constants. Benchmark problem: `1a-upper`.

**Best known:** C_1a ≤ 1.5027434868, Atris (2026), on the constant's page. Also known: C_1a ≥ 1.2802 (constant 1a page).

**To beat it:** a non-negative step function f whose autoconvolution max (f*f) / (∫f)^2 is below the best value, certified exactly.

**Keeper:** [Optimization constants in mathematics, constant 1a (T. Tao et al.)](https://teorth.github.io/optimizationproblems/constants/1a.html), read 2026-11-09 15:58 +04 (page source at main (README at 87b4ebb)).

**Quantavane value in review.** Quantavane's step function with 262,144 cells certifies C_1a ≤ 1.5027427375 (exact fraction in the leaderboard), the best value we have verified; it is in review as pull request #346 and is not yet on the page, so the page value stays the record here.

## The problem

C_1a is the largest constant with max_{|t|<=1/2} (f*f)(t) >= C_1a (int f)^2 for every non-negative f. Any non-negative f on [-1/4, 1/4] gives C_1a <= max(f*f) / (int f)^2. Find f making this smaller.

## Why it matters

C_1a measures how small the autoconvolution of a function can be, and it controls the size of Sidon sets (Cloninger-Steinerberger, Matolcsi-Vinuesa). Since 2025 it has become a proving ground for AI search systems, with seven improvements on Tao's page since May 2025.

Sources: [Tao et al., constant 1a](https://teorth.github.io/optimizationproblems/constants/1a.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2002 | upper | π/2 | [SS2002] | constant 1a page |
| 2009 | upper | 1.50992 | M. Matolcsi and C. Vinuesa [MV2009] | constant 1a page |
| 2025-05 | upper | 1.5053 | AlphaEvolve [GGSWT2025] | constant 1a page |
| 2025-12 | upper | 1.503164 | AlphaEvolve [GGSWT2025] | constant 1a page |
| 2025 | upper | 1.503133 | ThetaEvolve [WSZXRYHHMPCHCWDS2025] | constant 1a page |
| 2026 | upper | 1.502870 | TTT-Discover [YKLBMWKCZGS2026] | constant 1a page |
| 2026 | upper | 1.502862 | TogetherAI [T2026] | constant 1a page |
| 2026-10-03 | upper | 1.5027435320 | AgentDiscover, EinsteinArena [EA2026] | constant 1a page |
| 2026 | upper | 1.5027434868 | Atris [A2026] | constant 1a page |
| 2026-11-05 | upper | 1.5027433522 | vidigoat (pull request #270, in review) | teorth/optimizationproblems#270, replayed by Quantavane on 5 Nov 2026 |
| 2026-11-08 | upper | 1.5027427375 | A. Canli (Quantavane) (pull request #346, in review) | teorth/optimizationproblems#346; certificate in github.com/arhancanli/quantavane-replays (improvements/c1a) |

## Check a certificate

Certificate format: JSON {"values": [...]}: the non-negative heights of a step function with n equal cells on [-1/4, 1/4] (integers, JSON numbers read as binary64, or decimal strings read exactly).

Score: a certified upper bound on the constant (exact; smaller is better).

```
python3 -I obb.py check 1a-upper CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/autocorr_check.py 1a CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 29134478977604335569142246661390387511296/19387536037290895570476550697799766901521 | A. Canli (Quantavane), pull request #346, in review | above the listed record (in review) | 2026-11-09 | certs/ours_c1a_upper_n262144.json (a5eba0bf6142...) |
