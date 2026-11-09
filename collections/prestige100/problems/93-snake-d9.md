# 93. Longest snake in the 9-dimensional hypercube

Family: Snake-in-the-box. Benchmark problem: `snake-d9`.

**Best known:** 191 edges, M. Orland, B. Fagan et al. (2026).

**To beat it:** an induced path of 192 or more edges in the 9-dimensional hypercube.

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find an induced path in the hypercube Q_9 (two of its vertices adjacent only when consecutive) with as many edges as possible. The longest known, by Orland, Fagan et al. (2026), has 191 edges; a longer one improves it.

## Why it matters

The snake-in-the-box problem (Kautz 1958) asks for the longest induced path in a hypercube, a model for error-detecting codes; it is solved up to dimension 8 (98, Östergård and Pettersson 2014). Dimension 9 is the first open case, and its record moved from 190 (2012) to 191 in 2026.

Sources: [Leaps in Bounds, snake-in-the-box](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2005-05 | lower | 186 | D. A. Casella and W. D. Potter | D.A. Casella and W.D. Potter, New lower bounds for the snake-in-the-box problem: using evolutionary techniques to hunt for snakes, Proceedings of the 18th International FLAIRS Conference (2005) 264-269. (via Leaps in Bounds) |
| 2007-06 | lower | 188 | D. R. Tuohy, W. D. Potter and D. A. Casella | D.R. Tuohy, W.D. Potter and D.A. Casella, Searching for snake-in-the-box codes with evolved pruning models, Proceedings of the 2007 International Conference on Genetic and Evolutionary Methods (GEM'07) 3-9. (via Leaps in Bounds) |
| 2012-01-08 | lower | 190 | E. Wynn | E. Wynn, Constructing circuit codes by permuting initial sequences, arXiv:1201.1647. (via Leaps in Bounds) |
| 2026-07-16 | lower | 191 | M. Orland, B. Fagan et al. | M. Orland, B. Fagan, et al., A census of new snake-in-the-box records, arXiv:2607.15270v1. (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the transition sequence from the vertex 0, one character per edge for the coordinate that changes (0-9, then a-z; whitespace ignored).

Score: the number of edges (larger is better).

```
python3 -I obb.py check snake-d9 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/snake_check.py snake 9 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 191 | Orland, Fagan et al. (2026) (certificate from Leaps in Bounds, MIT) | record | 2026-11-08 | certs/lib_snake-in-the-box-9-lower-191.txt (a9b63ff19ff4...) |
