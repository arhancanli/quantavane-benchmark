# The minimum overlap constant of the square

`overlap-square` · Combinatorics and graph theory · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **150615/262144** (minimize), Quantavane (Arhan Canli), 9 November 2026: a 16 x 16 step function with values in multiples of 1/64, found by projected gradient descent on a smoothed maximum from an 8 x 8 start (tools/overlap2d.py)

## Statement

For a measurable f: [0,2]^2 -> [0,1] with integral 2 (half the area of the square), let g = 1 - f on the square and g = 0 outside, and let M(f) = sup over x in R^2 of the integral of f(t) g(t - x) dt, the largest overlap between the 'first half' f and a translate of the 'second half' g. Determine mu_sq = inf over f of M(f). This is the square version of Erdos's minimum overlap problem (split {1, ..., 2n} into two halves A and B of equal size and minimise the largest number of solutions of a - b = k); its one-dimensional constant mu = 0.380... is constant 1b of the optimization-constants repository. Known bounds: 1/4 <= mu_sq <= 150615/262144 = 0.574550...; find a step function with a smaller overlap.

## Why it is interesting

Erdos's minimum overlap problem asks how evenly {1, ..., 2n} can be split so that no difference is realised too often between the halves; it reduces to a continuous constant mu, with White's lower bound 0.379005 (arXiv:2201.05704) and upper bounds by Haugland (0.380927, arXiv:1609.08000) and later computer searches (repository constant 1b: 0.379005 <= mu <= 0.38085856). In the square the same question measures how well a region of half the area can avoid its complement under every translation. Two elementary bounds frame it: averaging over translations gives mu_sq >= (int f)(int g) / 16 = 1/4, and cylinders f(t_1, t_2) = F(t_1) give mu_sq <= 2 mu < 0.7618; our 16 x 16 step function already gives 0.5746, so genuinely two-dimensional sets do much better than cylinders.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/overlap-square.json`](../novelty/overlap-square.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"minimum overlap" AND all:"two-dimensional"`: 1 result
  - `all:"Erdos minimum overlap" AND all:dimension`: 0 results
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): the benchmark has the one-dimensional constants 1a, 1c and 1d, not 1b, and nothing two-dimensional of this kind.

Closest work found, and how this problem differs:
- The one-dimensional minimum overlap constant mu (Erdos; Haugland; repository constant 1b). The square constant mu_sq is a different quantity, between 1/4 and 2 mu.

Verdict: new. No paper or table on a two-dimensional (or square) version of Erdos's minimum overlap problem was found; the one-dimensional constant (repository constant 1b) is the closest.

## First values

| grid | best overlap found (ours) |
| --- | --- |
| 8 x 8 (values in 1/64) | 0.5803 (float, before rounding) |
| 16 x 16 (values in 1/64) | 150615/262144 = 0.574551 |

For comparison: cylinder functions built from the best known one-dimensional functions give 2 mu, about 0.7617.

## Best known value

150615/262144 = 0.574550... (16 x 16 step function with values in multiples of 1/64, `refs/overlap-square.txt`), held by Quantavane (Arhan Canli), 9 November 2026. Lower bound 1/4 from averaging the overlap over all translations (the translations x with nonzero overlap fill [-2,2]^2, of area 16, and the overlaps integrate to (int f)(int g) = 4).

Bound on the other side: 1/4 (lower bound; averaging over translations: integral over x of the overlap is 4, supported on [-2,2]^2 of area 16).

## Submitting and checking

Format: Text file: a 16 x 16 array of integers between 0 and 64 summing to 64 * 16^2 / 2 = 8192 (16 lines of 16 numbers): the step function f = entry/64 on the cells of side 1/8 of [0,2]^2. Other grids and denominators can be checked with the checker's M and DEN arguments.

Score: the overlap M(f) of the step function, an exact rational number (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check overlap-square FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comb.py overlap-square 16 64 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/overlap-square.txt`.

## References

- P. Erdos, Some remarks on number theory, Riveon Lematematika 9 (1955) 45-48 (the minimum overlap problem)
- J. K. Haugland, The minimum overlap problem revisited, arXiv:1609.08000
- E. P. White, Erdos' minimum overlap problem, arXiv:2201.05704 (the lower bound 0.379005)
- Optimization constants in mathematics, constant 1b (github.com/teorth/optimizationproblems), read 9 November 2026
