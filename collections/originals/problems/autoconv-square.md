# The autoconvolution constant of the square

`autoconv-square` · Combinatorics and graph theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **5687487427963392/2559015127450681** (minimize), Quantavane (Arhan Canli), 9 November 2026: a 24 x 24 step function found by exponentiated-gradient descent on a smoothed maximum, started from an 8 x 8 solution refined at 16 x 16 and three times at 24 x 24 (tools/autoconv2d.py)

## Statement

Let C_sq be the infimum, over nonnegative integrable functions f on the plane that vanish outside the square Q = [-1/4, 1/4]^2 and are not almost everywhere zero, of ||f*f||_inf / (integral of f)^2, where f*f(x) = integral of f(y) f(x - y) dy. Determine C_sq. Bounds: C_1a <= C_sq <= C_1a^2, where C_1a is the one-dimensional constant of the same kind (functions on [-1/4, 1/4]; constant 1a of the optimization-constants repository, 1.2802 <= C_1a <= 1.5027435). A step function constant on the M x M cells of side 1/(2M) gives an exact rational upper bound 4 M^2 max (a*a) / (sum a)^2 (a*a: the discrete autoconvolution of its array of values). The headline task is to beat our 24 x 24 step function: find a nonnegative f supported in Q with ||f*f||_inf / (int f)^2 < 5687487427963392/2559015127450681 = 2.2225298190...

## Why it is interesting

In one dimension the constant C_1a = inf ||f*f||_inf / (int f)^2 over f >= 0 on [-1/4, 1/4] controls how large a set of integers can be when every sum a + b is represented at most g times (generalized Sidon or B_2[g] sets; Cilleruelo, Ruzsa and Vinuesa, arXiv:0909.5024), and its bounds have been pushed by Matolcsi and Vinuesa (arXiv:0807.5121) and Cloninger and Steinerberger (arXiv:1403.7988). The square version asks the same question for sums in the plane; a projection argument gives C_sq >= C_1a (integrate f*f along one coordinate) and product functions g(x)g(y) give C_sq <= C_1a^2. Our 24 x 24 step function gives 2.22253, below 2.25823 = 1.5027435^2, the square of the best known one-dimensional bound, so functions that are not products already do better than the best known products.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/autoconv-square.json`](../novelty/autoconv-square.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:autoconvolution AND all:"two-dimensional"`: 3 results
  - `all:Sidon AND all:"two-dimensional" AND all:"B_2[g]"`: 0 results
  - `all:"Sidon sets" AND all:"higher dimensions" AND all:autoconvolution`: 0 results
- Web search (general web search), `two-dimensional autoconvolution inequality sup norm f*f nonnegative function supported on square constant Sidon sets in Z^2 g-Sidon "B_2[g]" two dimensions`: only the one-dimensional work (Matolcsi-Vinuesa, Cloninger-Steinerberger, Cilleruelo-Ruzsa-Vinuesa)
- Web search (general web search), `"generalized Sidon" OR "B_2[g]" sets in "N^d" OR "Z^d" OR "dimension d" maximal size constant autoconvolution Cilleruelo`: one-dimensional and cyclic-group results only (Cilleruelo-Ruzsa-Vinuesa; Martin-O'Bryant; Kravitz)
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark's constants 1a, 1c and 1d are one-dimensional; there is no two-dimensional autoconvolution entry.

Closest work found, and how this problem differs:
- The one-dimensional constant C_1a (repository constant 1a; Matolcsi-Vinuesa, Cloninger-Steinerberger, Cilleruelo-Ruzsa-Vinuesa). The square constant is a different quantity, between C_1a and C_1a^2.
- Kravitz (arXiv:2004.06611): correspondences between discrete additive problems and autocorrelation integrals, in one dimension.

Verdict: new. No paper, table or repository entry was found for the autoconvolution constant of a two-dimensional domain; the one-dimensional constant (1a in the optimization-constants repository) is the closest, and the bounds relating the two are elementary.

## First values

| grid M x M | best ratio found (ours) | same grid, best product g(x)g(y) found (ours) |
| --- | --- | --- |
| 8 x 8 | 2.34383 | 2.49946 (= 1.58097^2) |
| 16 x 16 | 2.26079 | 2.41038 (= 1.55254^2) |
| 24 x 24 | 2.22253 |  |

Upper bounds by step functions on finer grids. The product column uses our own one-dimensional optimizer at the same number of steps; the best known one-dimensional bound, 1.5027435, gives the product bound 2.25823. Exact values of our certificates are rational numbers recomputed by the checker.

## Best known value

5687487427963392/2559015127450681 = 2.2225298190... (24 x 24 step function in `refs/autoconv-square.txt`), held by Quantavane (Arhan Canli), 9 November 2026. Lower bound: C_sq >= C_1a >= 1.2802 (the projection f -> its marginal g(x) = integral f(x, y) dy has ||g*g||_inf <= ||f*f||_inf, since f*f vanishes outside [-1/2, 1/2]^2; 1.2802 is the best known lower bound for C_1a in the optimization-constants repository, read 9 November 2026).

Bound on the other side: 1.2802 (lower bound; C_sq >= C_1a >= 1.2802 (projection argument; repository constant 1a)).

## Submitting and checking

Format: Text file: a 24 x 24 array of nonnegative integers (24 lines of 24 numbers), the values of a step function on the cells of side 1/48 of the square. Step functions on other grids can be checked with the checker's M argument (python3 -I collections/originals/checkers/orig_comb.py autoconv-square M FILE).

Score: ||f*f||_inf / (int f)^2 for the step function, an exact rational number (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check autoconv-square FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comb.py autoconv-square 24 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/autoconv-square.txt`.

## References

- J. Cilleruelo, I. Ruzsa, C. Vinuesa, Generalized Sidon sets, arXiv:0909.5024
- M. Matolcsi, C. Vinuesa, The supremum of autoconvolutions, with applications to additive number theory, arXiv:0807.5121
- A. Cloninger, S. Steinerberger, On suprema of autoconvolutions with an application to Sidon sets, arXiv:1403.7988
- Optimization constants in mathematics, constant 1a (github.com/teorth/optimizationproblems), read 9 November 2026
- Z. Kravitz, Generalized difference sets and autocorrelation integrals, arXiv:2004.06611
