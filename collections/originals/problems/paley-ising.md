# Ground states of the Paley Ising model

`paley-ising` · Physics · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **-492** (minimize), Quantavane (Arhan Canli), 10 November 2026: a configuration of energy -492 found by simulated annealing with single-flip descent (tools/src/ising.c; -480 on 9 November 2026)

## Statement

Let p be a prime with p = 1 (mod 4) and let chi be the Legendre symbol modulo p. The Paley Ising model on p spins s_0, ..., s_(p-1) in {+1, -1} has energy E_p(s) = sum over 0 <= i < j <= p-1 of chi(j - i) s_i s_j: the couplings are +1 (antiferromagnetic) on the edges of the Paley graph P_p and -1 (ferromagnetic) on its non-edges. Determine the ground-state energy E_p = min over s of E_p(s). The headline cell is p = 101: find a configuration with E_101(s) < -492. Every E_p(s) is divisible by 4, and E_p >= -p^(3/2)/2 because the coupling matrix has eigenvalues +sqrt(p), -sqrt(p) and 0.

## Why it is interesting

Deterministic spin models whose couplings are explicit arithmetic functions can be as glassy as random ones: Bernasconi's low-autocorrelation model and the sine model of Marinari, Parisi and Ritort (J_ij = sin(2 pi i j / p)), whose ground states for p = 3 mod 4 are built from Legendre symbols, are the standard examples [MPR 1994, hep-th/9405148 and cond-mat/9406074; Borsari, Graffi and Unguendoli, cond-mat/9511019]. The Paley model is the Fourier dual of that picture: its coupling matrix is the circulant Legendre (Paley conference) matrix, whose eigenvectors are the additive characters with eigenvalues chi(k) sqrt(p), so a ground state is a +-1 vector as close as possible to the span of the non-residue frequencies. It is also a signed maximum cut of K_p with the Paley signs, linking it to the pseudo-randomness of Paley graphs; the ratio E_p / (-p^(3/2)/2) measures how well +-1 vectors can follow that eigenspace (0.92 at p = 29, 0.95 at p = 101 for our best states).

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/paley-ising.json`](../novelty/paley-ising.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:Paley AND all:Ising`: 0 results
  - `all:"Legendre symbol" AND all:"spin glass"`: 0 results
  - `all:"quadratic residue" AND all:Ising`: 1 result
- OEIS, 2 searches:
  - `4,20,32,72,108,124`: 0 results
  - `-4,-20,-32,-72`: 0 results
- Web search (general web search), `Ising spin glass couplings Legendre symbol quadratic residues "Paley" ground state energy deterministic spin model`: the sine-model papers (cond-mat/9511019, cond-mat/0006476) with Legendre-symbol ground states; nothing with Legendre-symbol couplings
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no Ising or max-cut family; the benchmark's Paley-related entries are Ramsey colourings, a different quantity.

Closest work found, and how this problem differs:
- Marinari, Parisi and Ritort's sine model and Borsari, Graffi and Unguendoli (cond-mat/9511019): couplings sin(2 pi i j/p), Legendre-symbol ground states for p = 3 mod 4. Here the Legendre symbol is the coupling, the matrix is circulant, and the ground states are unknown.

Verdict: new. No paper, OEIS entry or keeper table found for the Ising model with Legendre-symbol (Paley) couplings or for its ground-state energies. The closest work is the sine model of Marinari, Parisi and Ritort, where Legendre symbols appear as ground states rather than as couplings.

## First values

| p | E_p | how | ground states with s_0 = +1 | lower bound 4*ceil(-p^(3/2)/8) |
| --- | --- | --- | --- | --- |
| 5 | -4 | exact (all 2^(p-1) states) | 5 | -4 |
| 13 | -20 | exact (all 2^(p-1) states) | 39 | -20 |
| 17 | -32 | exact (all 2^(p-1) states) | 34 | -32 |
| 29 | -72 | exact (all 2^(p-1) states) | 203 | -76 |
| 37 | -108 | best known (ours) |  | -112 |
| 41 | -124 | best known (ours) |  | -128 |
| 53 | -184 | best known (ours) |  | -192 |
| 61 | -228 | best known (ours) |  | -236 |
| 73 | -296 | best known (ours) |  | -308 |
| 89 | -400 | best known (ours) |  | -416 |
| 97 | -456 | best known (ours) |  | -476 |
| 101 | -492 | best known (ours) |  | -504 |
| 109 | -548 | best known (ours) |  | -568 |
| 113 | -580 | best known (ours) |  | -600 |
| 137 | -760 | best known (ours) |  | -800 |
| 149 | -860 | best known (ours) |  | -908 |
| 157 | -928 | best known (ours) |  | -980 |
| 173 | -1072 | best known (ours) |  | -1136 |
| 181 | -1144 | best known (ours) |  | -1216 |
| 193 | -1268 | best known (ours) |  | -1340 |
| 197 | -1300 | best known (ours) |  | -1380 |

Exact values come from enumerating all 2^(p-1) configurations with s_0 = +1 (the energy is invariant under s -> -s). Best known values for p >= 37 are ours (simulated annealing, 30 restarts of 20,000 sweeps, then single-flip descent); they are upper bounds. Rows improved on 10 November 2026 show the value of the cell (see Cells).

## Best known value

-492 for p = 101, held by Quantavane (Arhan Canli), 10 November 2026 (our first value, 9 November, was -480): the configuration in `refs/paley-ising.txt`, found by simulated annealing (tools/src/ising.c, `ising anneal`). The exact values for p <= 29 come from `ising exact` (all configurations, Gray code). Lower bound for p = 101: -504 (spectral bound -p^(3/2)/2 = -507.5..., rounded up to a multiple of 4).

## Cells

The same question at each value of its parameter (p, a prime with p = 1 (mod 4)): 36 cells, 3 of them exact (an exhaustive search finished) and 33 best known (ours). Each cell has its certificate in `refs/cells/paley-ising/` (the headline cell uses `collections/originals/refs/paley-ising.txt`) and is checked with the family's checker:

    python3 -I obb.py check CELL FILE                  # for example paley-ising-13

| cell | p | value | status |
| --- | --- | --- | --- |
| `paley-ising-13` | 13 | -20 | exact |
| `paley-ising-17` | 17 | -32 | exact |
| `paley-ising-29` | 29 | -72 | exact |
| `paley-ising-37` | 37 | -108 | best known |
| `paley-ising-41` | 41 | -124 | best known |
| `paley-ising-53` | 53 | -184 | best known |
| `paley-ising-61` | 61 | -228 | best known |
| `paley-ising-73` | 73 | -296 | best known |
| `paley-ising-89` | 89 | -400 | best known |
| `paley-ising-97` | 97 | -456 | best known |
| `paley-ising-101` | 101 | -492 | best known (headline) |
| `paley-ising-109` | 109 | -548 | best known |
| `paley-ising-113` | 113 | -580 | best known |
| `paley-ising-137` | 137 | -760 | best known |
| `paley-ising-149` | 149 | -860 | best known |
| `paley-ising-157` | 157 | -928 | best known |
| `paley-ising-173` | 173 | -1072 | best known |
| `paley-ising-181` | 181 | -1144 | best known |
| `paley-ising-193` | 193 | -1268 | best known |
| `paley-ising-197` | 197 | -1300 | best known |
| `paley-ising-229` | 229 | -1628 | best known |
| `paley-ising-233` | 233 | -1668 | best known |
| `paley-ising-241` | 241 | -1760 | best known |
| `paley-ising-257` | 257 | -1940 | best known |
| `paley-ising-269` | 269 | -2068 | best known |
| `paley-ising-277` | 277 | -2172 | best known |
| `paley-ising-281` | 281 | -2212 | best known |
| `paley-ising-293` | 293 | -2352 | best known |
| `paley-ising-313` | 313 | -2600 | best known |
| `paley-ising-317` | 317 | -2644 | best known |
| `paley-ising-337` | 337 | -2912 | best known |
| `paley-ising-349` | 349 | -3056 | best known |
| `paley-ising-353` | 353 | -3108 | best known |
| `paley-ising-373` | 373 | -3376 | best known |
| `paley-ising-389` | 389 | -3600 | best known |
| `paley-ising-397` | 397 | -3704 | best known |

Exact cells: all 2^(p-1) configurations with s_0 = +1 (tools/src/ising.c, mode exact). Best known cells: simulated annealing, 40 restarts of 20,000 sweeps, then single-flip descent (tools/src/ising.c, mode anneal).

Bound on the other side: -504 (lower bound; E_p >= -p^(3/2)/2 (eigenvalues of the Paley conference matrix) and E_p = 0 mod 4).

## Submitting and checking

Format: Text file: the 101 spins s_0, ..., s_100 as a string of + and - (whitespace and lines starting with # are ignored), or as 101 integers 1 and -1.

Score: the energy E_101(s), an integer (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check paley-ising FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_phys.py paley-ising 101 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/paley-ising.txt`.

## References

- E. Marinari, G. Parisi, F. Ritort, Replica field theory for deterministic models: binary sequences with low autocorrelation, J. Phys. A 27 (1994) 7615, arXiv:hep-th/9405148
- E. Marinari, G. Parisi, F. Ritort, Replica field theory for deterministic models (II): a non-random spin glass with glassy behaviour, J. Phys. A 27 (1994) 7647, arXiv:cond-mat/9406074
- I. Borsari, S. Graffi, F. Unguendoli, Ground states for a class of deterministic spin models with glassy behaviour, arXiv:cond-mat/9511019
- J. Bernasconi, Low autocorrelation binary sequences: statistical mechanics and configuration space analysis, J. Physique 48 (1987) 559
- R. E. A. C. Paley, On orthogonal matrices, J. Math. Phys. 12 (1933) 311
