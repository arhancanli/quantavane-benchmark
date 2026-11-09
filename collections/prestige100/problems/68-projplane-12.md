# 68. A projective plane of order 12

Family: Projective planes and Latin squares. Benchmark problem: `projplane-12`.

**Best known:** none known, none.

**To beat it:** 157 lines of 13 points on 157 points such that every two points lie on exactly one line.

**Keeper:** [The On-Line Encyclopedia of Integer Sequences](https://oeis.org), read 2026-11-09 16:14 +04 (A001231 (revision 35) and A001438 (revision 96)).

## The problem

Find a projective plane of order 12: 157 points and 157 lines, each line holding 13 points, such that every two points lie on exactly one line. Planes are known for every prime-power order; order 6 is impossible (Bruck and Ryser 1949) and order 10 was ruled out by computer (Lam, Thiel and Swiercz 1989), so 12 is the smallest open order. A valid plane scores 1.

## Why it matters

Projective planes exist for every prime-power order; order 6 is impossible (Bruck-Ryser 1949) and order 10 was ruled out by Lam's computer search in 1989, so 12 is the smallest order whose existence is open. Every known plane has prime-power order, and a plane of order 12 would refute the prime power conjecture.

Sources: [OEIS A001231](https://oeis.org/A001231); Lam, The search for a finite projective plane of order 10, Amer. Math. Monthly 98 (1991).

## History

As recorded by the keepers and the sources named, oldest first; Bound says which side of the value a row improves.

| Date | Bound | Value | By | Source |
| --- | --- | --- | --- | --- |
| 1949 | - | 6, 14, 21, 22, ... excluded | R. H. Bruck and H. J. Ryser | The nonexistence of certain finite projective planes, Canad. J. Math. 1 (1949) 88-93 |
| 1989 | - | 10 excluded | C. W. H. Lam, L. Thiel and S. Swiercz | The non-existence of finite projective planes of order 10, Canad. J. Math. 41 (1989) 1117-1123 |
| 2026-11-09 | - | 12 open | OEIS A001231 | number of projective planes of order n, known through n = 10 (via OEIS) |

## Check a certificate

Certificate format: Text file: 157 lines of text, each with the 13 points (numbered 0..156 or 1..157) of one line of the plane, separated by spaces or commas.

Score: 1 for a projective plane of order 12; none is known, so the best known value is 0.

```
python3 -I obb.py check projplane-12 CERTIFICATE        # the checker, and the comparison with the best known value
python3 -I checkers/projplane_check.py 12 CERTIFICATE        # the checker on its own
```

To submit, see [SUBMITTING.md](../../../SUBMITTING.md): the certificate and a short record (who, how, whether AI helped).

## Leaderboard

No certificate has been checked here yet; the record above is as its keeper lists it.
