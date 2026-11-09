# XOR circuits for the quadratic-residue circulant

`qr-xor` · Computing and operations research · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **238** (minimize), Quantavane (Arhan Canli), 9 November 2026: Paar's greedy common-pair elimination, best of 60 randomized runs (tools/qr_xor.py)

## Statement

For a prime p let Q_p be the p x p circulant matrix over GF(2) with Q[i][j] = 1 exactly when j - i is a nonzero square modulo p (its rows span the quadratic-residue codes of length p). An XOR circuit (linear straight-line program) for Q_p starts from the inputs x_0, ..., x_(p-1), adds gates s = a XOR b of earlier signals, and must produce every output y_i = sum over j of Q[i][j] x_j as one of its signals. What is the smallest number of gates? The headline cell is p = 31: find a circuit with fewer than 238 gates.

## Why it is interesting

The smallest XOR circuit for a fixed GF(2)-linear map is the shortest linear program problem, NP-hard in general and attacked with heuristics and SAT solvers (Boyar, Matthews and Peralta, J. Cryptology 26 (2013)); it is studied intensively for the diffusion matrices of block ciphers, where every saved gate makes a smaller implementation (Kranz, Leander, Stoffelen and Wiemer, ToSC 2017). The quadratic-residue circulants encode the classical quadratic-residue codes (MacWilliams and Sloane, chapter 16) and have a large symmetry group (x -> ax + b with a a nonzero square), so they test whether symmetry can be turned into sharing: for p = 7 the residues {1, 2, 4} form a perfect difference set, every pair of inputs lies in exactly one row, and no cancellation-free sharing is possible (14 gates); for p = 31 the greedy method already saves 45 percent (238 gates against 434).

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/qr-xor.json`](../novelty/qr-xor.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"XOR count" AND all:circulant AND all:"quadratic residue"`: 0 results
  - `all:"shortest linear program" AND all:circulant`: 0 results
- Web search (general web search), `XOR count OR "straight-line program" quadratic residue circulant matrix GF(2) encoder quadratic residue code XOR gates minimum`: general shortest-linear-program work and XOR counts of MDS circulants; nothing on quadratic-residue circulants or QR-code encoders
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no circuit-complexity family.

Closest work found, and how this problem differs:
- Straight-line programs for MDS diffusion matrices and block circulant MDS matrices (Kranz et al. 2017 and later work): the same question for different matrices.

Verdict: new. No XOR count or straight-line program for quadratic-residue circulants was found on arXiv or by web search; published XOR-count work concerns MDS diffusion matrices and general heuristics.

## First values

| p | row weight | naive gates p((p-1)/2 - 1) | best found (ours, Paar greedy) |
| --- | --- | --- | --- |
| 7 | 3 | 14 | 14 |
| 11 | 5 | 44 | 34 |
| 13 | 6 | 65 | 46 |
| 17 | 8 | 119 | 76 |
| 19 | 9 | 152 | 98 |
| 23 | 11 | 230 | 136 |
| 29 | 14 | 377 | 209 |
| 31 | 15 | 434 | 238 |
| 37 | 18 | 629 | 323 |
| 41 | 20 | 779 | 396 |
| 43 | 21 | 860 | 430 |
| 47 | 23 | 1034 | 508 |

Upper bounds from 60 randomized runs of Paar's greedy method (cancellation-free). Circuits that use cancellation (as in the Boyar-Peralta heuristic) may do better; no lower bound beyond the trivial p is proved.

## Best known value

238 gates for p = 31, held by Quantavane (Arhan Canli), 9 November 2026: the circuit in `refs/qr-xor.txt` (Paar's greedy method, tools/qr_xor.py). Lower bound: 31 (the 31 outputs are distinct and none is an input, so each is a different gate); nothing better is proved.

Bound on the other side: 31 (lower bound (trivial); the 31 outputs are distinct non-input signals).

## Submitting and checking

Format: Text file: a first line '31 G', then G lines 'a b' (gate k is signal 30 + k, the XOR of signals a and b, which must be inputs 0..30 or earlier gates), then one line of 31 signal numbers giving outputs y_0, ..., y_30 in order.

Score: G, the number of XOR gates (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check qr-xor FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_comp.py qr-xor 31 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/qr-xor.txt`.

## References

- C. Paar, Optimized arithmetic for Reed-Solomon encoders, IEEE ISIT 1997 (the greedy common-pair method)
- J. Boyar, P. Matthews, R. Peralta, Logic minimization techniques with applications to cryptology, J. Cryptology 26 (2013) 280-312
- T. Kranz, G. Leander, K. Stoffelen, F. Wiemer, Shorter linear straight-line programs for MDS matrices, IACR Trans. Symmetric Cryptology 2017(4) 188-211
- F. J. MacWilliams, N. J. A. Sloane, The Theory of Error-Correcting Codes (North-Holland, 1977), chapter 16 (quadratic-residue codes)
