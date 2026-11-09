# The smallest catenane in the diamond lattice

`diamond-link` · Chemistry and materials · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **28** (minimize), Quantavane (Arhan Canli), 9 November 2026: two linked circles routed through the lattice and shortened ring by ring, replacing windows with shorter lattice paths while the rings stay disjoint and linked, with random same-length moves between rounds; runs with several seeds stopped at two rings of 14 atoms (tools/diamond_link.py)

## Statement

Two rings of atoms on the diamond lattice, each a closed self-avoiding polygon of the lattice (distinct sites, each bonded to the next and the last to the first, at squared distance 3; sites with all coordinates even and x + y + z = 0 mod 4, or all odd and x + y + z = 3 mod 4), with no site in common, form a [2]catenane when they are linked and cannot be pulled apart. How few atoms in total can such a pair have? The checker certifies the link by the linking number of the two rings (half the sum of the signs of their crossings in a regular projection) being different from 0. The headline cell: find a catenane with fewer than 28 atoms (ours: two rings of 14 atoms, linking number 1 up to sign).

## Why it is interesting

Catenanes, molecules made of interlocked rings, were imagined by Frisch and Wasserman (1961) and made efficiently by Sauvage's templated synthesis (1983); with rotaxanes they became the first molecular machines (Nobel Prize in Chemistry 2016, Sauvage, Stoddart and Feringa). How small the interlocked rings can be is a basic question of chemical topology: each ring must be wide enough for the other to pass through. On a lattice the question is exact. Minimal links and their lattice stick numbers have been studied in the simple cubic lattice (for example Hong, No and Oh 2014), but the diamond lattice, the lattice of saturated carbon chains in their staggered conformations and of diamond itself, is more constrained: its rings of six atoms (all chairs) are the faces of the natural tiling of the diamond net by adamantane cages, so no other ring of the lattice, which runs along the edges of the tiles, can pass through one; every catenane needs larger rings. Our smallest catenane uses two rings of 14 atoms. The companion problem diamond-knot asks for the smallest knotted single ring.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/diamond-link.json`](../novelty/diamond-link.json) with its address, the time it ran and its first results.

- arXiv API, 6 searches:
  - `all:"lattice stick number" AND all:links`: 2 results
  - `all:"Hopf link" AND all:lattice AND all:minimal`: 1 result
  - `all:catenane AND all:lattice AND all:polygons`: 0 results
  - `all:"diamond lattice" AND all:linked`: 6 results
  - `all:"linked polygons" AND all:"cubic lattice"`: 0 results
  - `all:"minimal links" AND all:lattice`: 0 results
- OEIS, 2 searches:
  - `minimal lattice link Hopf`: 5 results (A000108, A001700, A001003, A001190, A060854)
  - `catenane lattice minimal`: 0 results
- Web search (general web search), `minimal links cubic lattice Hopf link minimum number of edges two lattice polygons linked catenane lattice "minimal links"`: minimal edge numbers of several links in the simple cubic lattice (a 2005 thesis), lattice stick numbers of links with small stick numbers (Hong, No and Oh), Diao's minimal trefoil of 24 edges; nothing on the diamond lattice
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no knot, link or lattice-polygon family in the benchmark.

Closest work found, and how this problem differs:
- Links with small lattice stick numbers in the cubic lattice (Hong, No and Oh, arXiv:1402.1642) and minimal edge counts of links in the simple cubic lattice: the same kind of question on another lattice.
- Minimal knotted polygons in the cubic lattices (Diao 1993; Janse van Rensburg and Rechnitzer, arXiv:1107.2162) and our diamond-knot: one ring, not two.
- Synthetic catenanes (Frisch and Wasserman 1961; Sauvage 1983 and later): real molecules, not a lattice extremum.

Verdict: new question for the diamond lattice: minimal links (lattice stick numbers, minimal edge counts) are studied in the simple cubic lattice, but no smallest pair of linked rings of the diamond lattice was found, as far as our searches show.

## First values

| rings | atoms | linking number | how |
| --- | --- | --- | --- |
| a ring of 6 atoms (a chair) with any other ring | - | 0 always | proved: the six-membered rings are faces of the tiling of the lattice by adamantane cages, so another ring of the lattice cannot cross them |
| two rings of 14 atoms | 28 | 1 (up to sign) | best known (ours, tools/diamond_link.py) |

The checker computes the linking number exactly from a regular projection (crossing signs between the two rings, counted both ways and checked equal); our tests also check it on a Hopf link of two circles (1 up to sign), on two separate circles (0) and with one ring reversed (the sign flips).

## Best known value

28 atoms: two rings of 14 atoms of the diamond lattice with linking number 1 up to sign, held by Quantavane (Arhan Canli), 9 November 2026 (`refs/diamond-link.txt`).

## Submitting and checking

Format: Text file: the atoms of the first ring in order (lines 'x y z'), a line holding only '-', then the atoms of the second ring in order.

Score: the total number of atoms of the two rings (smaller is better), valid only when they share no site and their linking number is not 0. A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check diamond-link FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_chem.py diamond-link FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/diamond-link.txt`.

## References

- H. L. Frisch, E. Wasserman, Chemical topology, J. Am. Chem. Soc. 83 (1961) 3789-3795
- C. O. Dietrich-Buchecker, J.-P. Sauvage, J. P. Kintzinger, Une nouvelle famille de molecules: les metallo-catenanes, Tetrahedron Lett. 24 (1983) 5095-5098
- K. Hong, S. No, S. Oh, Links with small lattice stick numbers, arXiv:1402.1642
- Our problem diamond-knot (the smallest knotted ring of the diamond lattice)
