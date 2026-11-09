# 88. Sorting network on 17 inputs with the fewest comparators

Family: Sorting networks. Benchmark problem: `sortnet-n17-size`.

**Best known:** 71 comparators, S. W. Al-Haj Baddar (2009). Also known: at least 63 comparators (Dobbelaere's table).

**To beat it:** a sorting network on 17 channels with 70 comparators or fewer.

**Keeper:** [Smallest and fastest sorting networks (B. Dobbelaere)](https://bertdobbelaere.github.io/sorting_networks.html), read 2026-11-09 15:51 +04 (page updated 10 Oct 2026 (commit 6bb0bd2)).

## The problem

Find a sorting network on 17 channels (a fixed sequence of comparators, each putting the smaller of two values on the lower-numbered channel, that sorts every input) with as few comparators as possible. The smallest known network on Bert Dobbelaere's list has 71 comparators; a network with fewer comparators improves it. Its depth is reported but not scored.

## Why it matters

For 17 inputs the best network has 71 comparators (Baddar 2009) and the lower bound is 63. Optimal sizes are proved only up to 12 inputs (Harder 2019 for 11 and 12), so these are the smallest open cases of a problem in Knuth's The Art of Computer Programming.

Sources: [B. Dobbelaere, Smallest and fastest sorting networks](https://bertdobbelaere.github.io/sorting_networks.html); [Knuth, TAOCP vol. 3, section 5.3.4](https://www-cs-faculty.stanford.edu/~knuth/taocp.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 2009 | upper | 71 | S. W. Al-Haj Baddar (2009) | S. W. Al-Haj Baddar, Finding Better Sorting Networks, PhD thesis, Kent State University (2009) [Baddar09] (via B. Dobbelaere) |
| 2025-04-21 | lower | 63 | B. Dobbelaere, on a suggestion of J. Firet | tighter lower bounds based on Van Voorhis (1972) [VVoorh72] (via B. Dobbelaere) |

## Check a certificate

Certificate format: Text file: the comparators in order, each as a pair of channel numbers 0..16; every two integers form one comparator (Dobbelaere's "[(0,13),(1,12),...]" format and one "i j" per line both work; text after # is ignored).

Score: the number of comparators (smaller is better).

```
python3 -I obb.py check sortnet-n17-size CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/sortnet_check.py 17 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 71 | S. W. Al-Haj Baddar (2009) | record | 2026-11-09 | certs/dobb_n17_s71.txt (01e04d83789d...) |
