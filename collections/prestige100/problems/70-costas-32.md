# 70. A Costas array of order 32

Family: Costas arrays. Benchmark problem: `costas-32`.

**Best known:** none known, none.

**To beat it:** a permutation of 1..32 whose dots have pairwise distinct displacement vectors.

**Keeper:** [K. Drakakis, Open problems in Costas arrays (arXiv:1102.5727)](https://arxiv.org/abs/1102.5727), read 2026-11-09 16:05 +04 (section 3.2 and Table 1).

## The problem

Find a permutation p of 1..32 such that the 496 vectors (j - i, p(j) - p(i)), i < j, are pairwise distinct: a Costas array of order 32. Costas arrays are known for every order up to 31, but none is known for the orders 32 and 33. A valid array scores 1 and settles the order.

## Why it matters

Costas arrays, introduced for sonar and radar waveforms, are known in every order up to 31 from the Welch and Golomb constructions and exhaustive searches; 32 and 33 are the smallest orders with none known (Drakakis, section 3.2). No known construction reaches order 32, so an array would have to be sporadic (the largest sporadic array known has order 27) or come from a new construction.

Sources: [Drakakis, Open problems in Costas arrays, arXiv:1102.5727](https://arxiv.org/abs/1102.5727).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1984 | - | - | J. P. Costas | A study of detection waveforms having nearly ideal range-Doppler ambiguity properties, Proc. IEEE 72 (1984) |
| 1984 | - | - | S. W. Golomb | Algebraic constructions for Costas arrays, J. Combin. Theory A 37 (1984): the Welch and Lempel-Golomb constructions |
| 2011 | - | orders 32 and 33 open | K. Drakakis | Open problems in Costas arrays, arXiv:1102.5727: all orders up to 29 enumerated; no array known for orders 32 and 33 (via K. Drakakis) |

## Check a certificate

Certificate format: Text file: 32 integers, a permutation of 1..32 (or of 0..31), separated by spaces, commas or newlines; the i-th number is the row of the dot in column i.

Score: 1 for a Costas array of order 32; none is known, so the best known value is 0.

```
python3 -I obb.py check costas-32 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/costas_check.py 32 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
