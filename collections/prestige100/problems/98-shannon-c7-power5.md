# 98. Shannon capacity of the 7-cycle: an independent set of 368 in the fifth strong power

Family: Optimization constants. Benchmark problem: `shannon-c7-power5`.

**Best known:** 367 vertices, S. C. Polak and A. Schrijver (2018).

**To beat it:** an independent set of 368 vertices in the fifth strong power of the 7-cycle (it would give Θ(C7) ≥ 368^(1/5) ≈ 3.25958, above the best known 3.25883262).

**Keeper:** [Optimization constants in mathematics, constant 9 (T. Tao et al.)](https://teorth.github.io/optimizationproblems/constants/9a.html), read 2026-11-09 15:58 +04 (page source at main (README at 87b4ebb)).

## The problem

Find as large an independent set as possible in C_7^5, the fifth strong power of the 7-cycle (two distinct 5-tuples over Z_7 are adjacent when every coordinate is equal or differs by 1 mod 7). An independent set of size a gives the Shannon capacity bound Theta(C_7) >= a^(1/5). The largest known has 367 vertices (Polak and Schrijver, 2018); a larger one improves it. Tao's page 9a lists better capacity bounds from much higher powers.

## Why it matters

Shannon's zero-error capacity of the 7-cycle is one of the oldest open problems in information theory (Shannon 1956; Lovász settled the 5-cycle in 1979). The best known independent set in the fifth power has 367 vertices (Polak and Schrijver 2018), and one of 368 would by itself beat every recursive bound on Tao's page.

Sources: [Tao et al., constant 9](https://teorth.github.io/optimizationproblems/constants/9a.html); Polak and Schrijver, New lower bound on the Shannon capacity of C7, Inform. Process. Lett. 143 (2019).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1971 | lower | 343 | L. D. Baumert et al. [BMRRST1971] | constant 9 page: 343^(1/5) |
| 2017 | lower | 350 | K. A. Mathew and P. R. J. Östergård [MO2017] | constant 9 page: 350^(1/5) |
| 2018 | lower | 367 | S. C. Polak and A. Schrijver [PS2018] | constant 9 page: 367^(1/5) ≈ 3.2578 |
| 2026 | - | 3.25883262 (capacity) | [Tan2026] | constant 9 page: heterogeneous recursion in the 500th power, the best capacity bound; the 367-set is its gadget |

## Check a certificate

Certificate format: Text file: the vertices, one per line, each as 5 digits 0-6 with nothing between them.

Score: the size of the independent set (larger is better).

```
python3 -I obb.py check shannon-c7-power5 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/strongpow_check.py 7 5 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
