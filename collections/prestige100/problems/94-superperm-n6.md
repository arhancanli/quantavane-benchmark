# 94. Shortest superpermutation on 6 symbols

Family: Superpermutations. Benchmark problem: `superperm-n6`.

**Best known:** length ≤ 872, R. Houston (2014). Also known: length ≥ 867 (an anonymous 4chan poster, R. Houston, J. Pantone and V. Vatter, 2018).

**To beat it:** a string on 6 symbols of length 871 or less containing all 720 permutations as substrings.

**Keeper:** [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04 (source data at commit a5bbf82 (9 Nov 2026, 05:15 UTC)).

## The problem

Find a string over 1..6 that contains every permutation of 1..6 as 6 consecutive characters, as short as possible. The shortest known, by Houston (2014), has length 872; a shorter one improves it.

## Why it matters

The minimal superpermutation is known for n ≤ 5 (153 for n = 5); for n = 6 Houston's 872 (2014) broke the conjectured formula, and the lower bound 867 came from an argument first posted anonymously on 4chan and then written up by Houston, Pantone and Vatter. Closing the gap between 867 and 872 is a well-known open problem.

Sources: [Houston, Tackling the minimal superpermutation problem, arXiv:1408.5108](https://arxiv.org/abs/1408.5108); [Leaps in Bounds, minimal-superpermutation](https://github.com/daniel-munro/leaps-in-bounds).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| undated | upper | 873 | not named | Leaps in Bounds table entry (via Leaps in Bounds) |
| 2014-08-21 | upper | 872 | R. Houston | Houston, R. (2014). Tackling the minimal superpermutation problem. arXiv preprint arXiv:1408.5108. (via Leaps in Bounds) |
| 2018-10-25 | lower | 867 | an anonymous 4chan poster, R. Houston, J. Pantone and V. Vatter | Anonymous 4chan poster, R. Houston, J. Pantone and V. Vatter. A lower bound on the length of the shortest superpattern (2018). (via Leaps in Bounds) |

## Check a certificate

Certificate format: Text file: the string, digits 1..6 (whitespace ignored).

Score: the length of the string (smaller is better).

```
python3 -I obb.py check superperm-n6 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/superperm_check.py 6 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
