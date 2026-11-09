# 100. The Mona Lisa TSP: a tour shorter than 5,757,191 ($1,000 prize)

Family: Travelling salesman. Benchmark problem: `tsp-mona-lisa`.

**Best known:** tour length 5,757,191, Y. Nagata (17 Mar 2009). Also known: no tour shorter than 5,757,084 (Concorde bound, 27 Jul 2012).

**To beat it:** a tour of the 100,000 cities of mona-lisa100K.tsp of length 5,757,190 or less.

**Keeper:** [Mona Lisa TSP Challenge (W. Cook)](https://www.math.uwaterloo.ca/tsp/data/ml/monalisa.html), read 2026-11-09 15:58 +04 (status and computation log).

## The problem

Find a shortest closed tour through the 100,000 cities of R. Bosch's Mona Lisa instance (mona-lisa100K.tsp, TSPLIB EUC_2D distances). The best known tour has length 5,757,191 (Y. Nagata, 17 Mar 2009) and no tour is shorter than 5,757,084 (Concorde, 27 Jul 2012); W. Cook offers $1,000 for the first tour shorter than 5,757,191.

## Why it matters

Robert Bosch's 100,000-city Mona Lisa instance (2009) is a famous TSP challenge, and William Cook offers $1,000 for the first tour shorter than 5,757,191. Nagata's record tour has stood since 17 March 2009, 107 units above the best lower bound.

Sources: [W. Cook, Mona Lisa TSP Challenge](https://www.math.uwaterloo.ca/tsp/data/ml/monalisa.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2009-02-23 | upper | 5758831 | K. Helsgaun (LKH) | Cook's computation log |
| 2009-02-26 | upper | 5757795 | K. Helsgaun (LKH-2, 8-opt) | Cook's computation log |
| 2009-02-26 | upper | 5757245 | K. Helsgaun (parallel LKH) | Cook's computation log |
| 2009-03-02 | upper | 5757241 | C. Dong, C. Ernst, G. Jäger, D. Richter and P. Molitor | Cook's computation log |
| 2009-03-02 | upper | 5757205 | K. Helsgaun | Cook's computation log |
| 2009-03-06 | upper | 5757204 | C. Dong, C. Ernst, G. Jäger, D. Richter and P. Molitor | Cook's computation log |
| 2009-03-07 | upper | 5757203 | K. Helsgaun | Cook's computation log |
| 2009-03-08 | upper | 5757200 | K. Helsgaun | Cook's computation log |
| 2009-03-16 | upper | 5757199 | K. Helsgaun | Cook's computation log |
| 2009-03-17 | upper | 5757191 | Y. Nagata (genetic algorithm) | Cook's computation log |
| 2012-07-27 | lower | 5757084 | W. Cook (Concorde) | Cook's computation log: gap 107 (0.0019%) |

## Check a certificate

Certificate format: Text file: a TSPLIB tour file (TOUR_SECTION ending with -1) or the 100,000 city numbers 1..100000 in the order visited, one per line.

Score: L, the tour length with EUC_2D distances rounded to the nearest integer (smaller is better).

```
python3 -I obb.py check tsp-mona-lisa CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/tsp_check.py instances/tsp/mona-lisa100K.tsp CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 5757191 | Y. Nagata (17 Mar 2009) | record | 2026-11-09 | certs/cook_monalisa_5757191.tour (d8a98a936d01...) |
