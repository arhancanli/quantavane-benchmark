# Fibonacci proteins on the triangular lattice

`hp-tri` · Biology · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **-44** (minimize), Quantavane (Arhan Canli), 9 November 2026: simulated annealing with pivot moves over self-avoiding conformations (tools/hp_tri.py, two runs of 60 s)

## Statement

In the HP model of protein folding a chain of hydrophobic (H) and polar (P) monomers occupies distinct sites of a lattice, consecutive monomers on neighbouring sites, and its energy is minus the number of pairs of H monomers that are lattice neighbours without being consecutive. Take the Fibonacci words S_1 = P, S_2 = H, S_k = S_(k-1) S_(k-2) (S_3 = HP, S_4 = HPH, S_5 = HPHHP, ...; S_k has length F_k) as sequences and the triangular lattice (each site has 6 neighbours) as the lattice. Determine the ground-state energy E_k of S_k. The headline cell is S_10, of length 55: find a conformation with energy below -44.

## Why it is interesting

The HP model (Dill 1985; Lau and Dill 1989) is the standard minimal model of protein folding and a standard hard benchmark for optimisation (finding HP ground states is NP-hard on the square and cubic lattices); its benchmark sequences are mostly random or designed. Fibonacci sequences are the canonical quasiperiodic chains: Stillinger, Head-Gordon and Hirshfeld introduced them for the off-lattice AB model, where they remain test cases for folding algorithms (e.g. cond-mat/0302545), but they have not been posed as HP chains on a lattice. On the triangular lattice the model is less constrained by parity than on the square lattice (odd cycles exist, so any two monomers can touch), and the question is how a quasiperiodic hydrophobic pattern packs: the H fraction of S_k tends to 1/phi = 0.618..., and the best folds found put the H monomers into a compact core.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/hp-tri.json`](../novelty/hp-tri.json) with its address, the time it ran and its first results.

- arXiv API, 2 searches:
  - `all:"HP model" AND all:"triangular lattice"`: 2 results
  - `all:"HP model" AND all:Fibonacci`: 0 results
- Web search (general web search), `HP lattice protein model Fibonacci sequences ground state energy square lattice OR triangular lattice "Fibonacci" HP sequence benchmark`: Fibonacci sequences only in the off-lattice AB model (cond-mat/0302545); HP benchmark sequences on lattices are other sequences
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no protein-folding family.

Closest work found, and how this problem differs:
- Fibonacci sequences in the off-lattice AB model (Stillinger et al. 1993; Hsu et al., cond-mat/0302545): the same sequences in a different, continuous model.
- HP folding on the triangular lattice (e.g. cond-mat/9708049): the same lattice with other sequences.

Verdict: new. No ground-state energies of Fibonacci HP chains on any lattice were found (arXiv, web search); Fibonacci sequences have been folded only in the off-lattice AB model, and triangular-lattice HP studies use other sequences.

## First values

| length F_k | sequence | ground-state energy E_k | how |
| --- | --- | --- | --- |
| 1 | H | 0 | exact |
| 2 | HP | 0 | exact |
| 3 | HPH | 0 | exact |
| 5 | HPHHP | -2 | exact (all conformations) |
| 8 | HPHHPHPH | -6 | exact (all conformations) |
| 13 | HPHHPHPHHPHHP | -10 | exact (all conformations) |
| 21 | S_8 | -19 | best known (ours) |
| 34 | S_9 | -29 | best known (ours) |
| 55 | S_10 | -44 | best known (ours) |

Exact values: every self-avoiding conformation enumerated (tools/hp_tri.py exact); larger chains: our best annealed folds (upper bounds). S_10 has 34 H and 21 P monomers.

## Best known value

-44 for S_10 (length 55), held by Quantavane (Arhan Canli), 9 November 2026: the fold in `refs/hp-tri.txt`. Lower bound -69: each H monomer has at most 4 neighbouring sites besides its chain neighbours (5 at a chain end), so 34 H monomers make at most 69 contacts.

Bound on the other side: -69 (lower bound (trivial); at most 4 free neighbours per H monomer (5 at an end); 34 H monomers).

## Submitting and checking

Format: Text file: 55 lines 'a b', the lattice site a + b e^(i pi/3) of each monomer in chain order (neighbouring sites differ by (1,0), (0,1), (-1,1), (-1,0), (0,-1) or (1,-1)).

Score: the energy, minus the number of non-consecutive H-H neighbour pairs (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check hp-tri FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_bio.py hp-tri 55 FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/hp-tri.txt`.

## References

- K. A. Dill, Theory for the folding and stability of globular proteins, Biochemistry 24 (1985) 1501-1509
- K. F. Lau, K. A. Dill, A lattice statistical mechanics model of the conformational and sequence spaces of proteins, Macromolecules 22 (1989) 3986-3997
- F. H. Stillinger, T. Head-Gordon, C. L. Hirshfeld, Toy model for protein folding, Phys. Rev. E 48 (1993) 1469-1477 (Fibonacci sequences in the AB model)
- Structure optimization in an off-lattice protein model, arXiv:cond-mat/0302545 (Fibonacci AB chains, off-lattice)
