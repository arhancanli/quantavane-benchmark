# The smallest knotted ring in the diamond lattice

`diamond-knot` · Chemistry and materials · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **36** (minimize), Quantavane (Arhan Canli), 9 November 2026: a trefoil curve routed through the lattice and shortened by replacing windows of the ring with shorter lattice paths while it stays knotted, with random same-length moves between rounds; runs with five seeds all stopped at 36 atoms (tools/diamond_knot.py)

## Statement

A ring of atoms whose skeleton sits on the diamond lattice is a closed self-avoiding polygon of the lattice: distinct sites (integer points with all coordinates even and x + y + z = 0 mod 4, or all odd and x + y + z = 3 mod 4), each bonded to the next and the last to the first (squared distance 3), so that every bond angle is the tetrahedral angle, as in a cycloalkane in staggered conformations or a ring cut from diamond. How few atoms can a knotted ring have? The checker certifies the knot by its knot determinant |Delta(-1)|, computed from a regular projection, being larger than 1 (3 for the trefoil). The headline cell: find a knotted ring of fewer than 36 atoms (ours: a trefoil, knot determinant 3, with 36 atoms).

## Why it is interesting

Knotted molecules were proposed by Frisch and Wasserman (1961) and first made by Dietrich-Buchecker and Sauvage (1989); how small a knotted ring can be is a basic question of chemical topology, since a tight knot strains every bond. On a lattice the question becomes exact: the minimal knotted polygons of the three cubic lattices are known, 24 edges in the simple cubic lattice (Diao 1993) and 15 and 18 edges in the face-centred and body-centred cubic lattices (Janse van Rensburg and Rechnitzer 2011), all trefoils. The diamond lattice is the lattice of chemistry: the carbon atoms of diamond, the backbone of an alkane or polyethylene chain in its staggered conformations (the rotational-isomeric-state lattice of polymer physics) and the oxygen atoms of cubic ice all sit on it, and every bond angle is tetrahedral. It is also the most open of these lattices, with four neighbours per site and no rings shorter than six, so its knots must be long. A ring is certified knotted when its knot determinant |Delta(-1)| (the determinant of the Fox colouring matrix of a diagram) exceeds 1; the checker computes it exactly from a regular projection. Our shortest ring is a trefoil of 36 atoms; whether a shorter knotted ring exists is open, and no lower bound beyond the trivial one is known to us.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/diamond-knot.json`](../novelty/diamond-knot.json) with its address, the time it ran and its first results.

- arXiv API, 7 searches:
  - `all:"diamond lattice" AND all:knot`: 1 result
  - `all:"diamond lattice" AND all:knotted`: 1 result
  - `all:"minimal knot" AND all:lattice`: 1 result
  - `all:"lattice knots" AND all:"minimal length"`: 3 results
  - `all:"minimal knotted polygons"`: 1 result
  - `all:"knotted" AND all:"cycloalkane"`: 0 results
  - `all:"molecular knot" AND all:smallest`: 0 results
- OEIS, 3 searches:
  - `minimal knot lattice polygon`: 5 results (A122059, A000108, A000975, A000931, A005043)
  - `trefoil lattice minimal number of edges`: 1 result (A122059)
  - `24 15 18 trefoil lattice`: 0 results
- Web search (general web search), `minimal step number trefoil knot diamond lattice self-avoiding polygon minimum length knot "diamond lattice"`: minimal trefoils of 24 edges in the simple cubic lattice (Diao), 15 and 18 edges in the face-centred and body-centred cubic lattices, knots in slabs; nothing for the diamond lattice
- Web search (general web search), `"diamond lattice" knotted ring polymer smallest knot length minimal number of steps trefoil knotting probability`: The compressibility of minimal lattice knots (arXiv:1203.3212), Minimal knotted polygons in cubic lattices (arXiv:1107.2162), relative knot probabilities in confined lattice polygons (arXiv:2501.08835); no minimal knot of the diamond lattice
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no knot or lattice-polygon family in the benchmark.

Closest work found, and how this problem differs:
- Minimal knotted polygons in the cubic lattices (Diao 1993; Janse van Rensburg and Rechnitzer, arXiv:1107.2162; upper bounds for cubic lattice knots, arXiv:1411.1849): the same question on the simple, face-centred and body-centred cubic lattices.
- Knot probabilities of lattice polygons and ring polymers (Frisch-Wasserman-Delbruck conjecture; relative knot probabilities in confined lattice polygons, arXiv:2501.08835): statistics of long rings, not the smallest knot.
- Synthetic molecular knots (Dietrich-Buchecker and Sauvage 1989 and later tight knots): real molecules, not a lattice extremum.

Verdict: new question for the diamond lattice: minimal knotted polygons are known for the simple, face-centred and body-centred cubic lattices, but no minimal knotted ring of the diamond lattice was found, as far as our searches show.

## First values

| lattice | neighbours per site | smallest knotted polygon | knot | source |
| --- | --- | --- | --- | --- |
| face-centred cubic | 12 | 15 | trefoil | Janse van Rensburg and Rechnitzer (2011) |
| body-centred cubic | 8 | 18 | trefoil | Janse van Rensburg and Rechnitzer (2011) |
| simple cubic | 6 | 24 | trefoil | Diao (1993) |
| diamond | 4 | 36 | trefoil (knot determinant 3) | best known (ours, this problem) |

The diamond row is our shortest ring (refs/diamond-knot.txt), certified by the checker; the other rows are the published minima for comparison. The checker's knot determinant gives 3 for a trefoil curve, 5 for a figure-eight knot and 1 for an unknotted ring in our tests.

## Best known value

36 atoms: a knotted ring of the diamond lattice with knot determinant 3, held by Quantavane (Arhan Canli), 9 November 2026 (`refs/diamond-knot.txt`).

## Submitting and checking

Format: Text file: the atoms of the ring in order, one line 'x y z' each: distinct sites of the diamond lattice, consecutive ones (and the last and the first) at squared distance 3.

Score: the number of atoms of the ring (smaller is better), valid only when its knot determinant exceeds 1. A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check diamond-knot FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_chem.py diamond-knot FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/diamond-knot.txt`.

## References

- H. L. Frisch, E. Wasserman, Chemical topology, J. Am. Chem. Soc. 83 (1961) 3789-3795
- C. O. Dietrich-Buchecker, J.-P. Sauvage, A synthetic molecular trefoil knot, Angew. Chem. Int. Ed. Engl. 28 (1989) 189-192
- Y. Diao, Minimal knotted polygons on the cubic lattice, J. Knot Theory Ramifications 2 (1993) 413-425
- E. J. Janse van Rensburg, A. Rechnitzer, Minimal knotted polygons in cubic lattices, arXiv:1107.2162
- R. H. Fox, A quick trip through knot theory, in: Topology of 3-Manifolds and Related Topics, Prentice-Hall, 1962, 120-167 (colourings and the knot determinant)
