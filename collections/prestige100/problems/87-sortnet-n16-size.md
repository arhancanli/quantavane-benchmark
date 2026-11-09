# 87. Sorting network on 16 inputs with the fewest comparators

Family: Sorting networks. Benchmark problem: `sortnet-n16-size`.

**Best known:** 60 comparators, M. W. Green (1969), in TAOCP vol. 3. Also known: at least 57 comparators (Dobbelaere's table).

**To beat it:** a sorting network on 16 channels with 59 comparators or fewer.

**Keeper:** [Smallest and fastest sorting networks (B. Dobbelaere)](https://bertdobbelaere.github.io/sorting_networks.html), read 2026-11-09 15:51 +04 (page updated 10 Oct 2026 (commit 6bb0bd2)).

## The problem

Find a sorting network on 16 channels (a fixed sequence of comparators, each putting the smaller of two values on the lower-numbered channel, that sorts every input) with as few comparators as possible. The smallest known network on Bert Dobbelaere's list has 60 comparators (Green's network of 1969 for 16 inputs has stood since then); a network with fewer comparators improves it. Its depth is reported but not scored.

## Why it matters

Green's 60-comparator network for 16 inputs has stood since 1969, and the lower bound is 57. Optimal sizes are proved only up to 12 inputs (Harder 2019 for 11 and 12), so these are the smallest open cases of a problem in Knuth's The Art of Computer Programming.

Sources: [B. Dobbelaere, Smallest and fastest sorting networks](https://bertdobbelaere.github.io/sorting_networks.html); [Knuth, TAOCP vol. 3, section 5.3.4](https://www-cs-faculty.stanford.edu/~knuth/taocp.html).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1969 | upper | 60 | M. W. Green (1969), in TAOCP vol. 3 | D. E. Knuth, The Art of Computer Programming, vol. 3, 2nd ed. (1998), as cited by Dobbelaere [TAOCPv3] (via B. Dobbelaere) |
| 2025-04-21 | lower | 57 | B. Dobbelaere, on a suggestion of J. Firet | tighter lower bounds based on Van Voorhis (1972) [VVoorh72] (via B. Dobbelaere) |

## Check a certificate

Certificate format: Text file: the comparators in order, each as a pair of channel numbers 0..15; every two integers form one comparator (Dobbelaere's "[(0,13),(1,12),...]" format and one "i j" per line both work; text after # is ignored).

Score: the number of comparators (smaller is better).

```
python3 -I obb.py check sortnet-n16-size CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/sortnet_check.py 16 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

| Value | Holder | Standing | Verified | Certificate (SHA-256) |
| --- | --- | --- | --- | --- |
| 60 | M. W. Green (1969) | record | 2026-11-09 | certs/dobb_n16_s60.txt (d5095642a544...) |
