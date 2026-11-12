# Unknotting numbers of the knots with at most 11 crossings

`unknotting` · Topology · status: **open** · added 12 November 2026 (Quantavane Open Tables)

Headline cell `unknotting-10-6`: **3** (minimize), published value: KnotInfo, unknotting number [2,3] (upper bound 3, lower bound 2); database_knotinfo 2026.11.2 (commit 219c2d9, 2 Nov 2026), the KnotInfo spreadsheet of that date, read 2026-11-12

## Statement

The unknotting number u(K) of a knot K is the least number of crossing changes that turn K into the unknot, where isotopies are allowed before, between and after the changes (equivalently: the least number of crossings to change in a single diagram of K, minimised over all diagrams). KnotInfo gives u(K) only as an interval for 75 of the 801 prime knots with at most 11 crossings; 8 of them were settled in March 2026 (McCoy and Park), leaving 67 open cells, one per knot. A submission for a knot is an unknotting sequence written as moves on a closed braid, starting from KnotInfo's braid word for the knot: braid relations, conjugations, stabilizations and destabilizations (the moves of Markov's theorem, which keep the knot), and crossing changes, ending at the trivial braid on one strand, whose closure is the unknot. The score is the number of crossing changes, an upper bound on u(K). A score below KnotInfo's upper bound improves the cell, and a score equal to its lower bound settles u(K). The headline cell: 10_6, u in {2, 3}.

## Why it is interesting

The unknotting number is the oldest measure of how knotted a knot is and among the hardest to compute: lower bounds come from invariants (the signature, Rasmussen's s, Ozsvath-Szabo's tau and the obstructions of Heegaard Floer theory, the linking form), upper bounds only from explicit sequences of crossing changes, and some knots need a non-minimal diagram (10_8, Bleiler and Nakanishi). The ten 10-crossing knots in the table (10_6, 10_11, 10_47, 10_51, 10_54, 10_61, 10_76, 10_77, 10_79, 10_100) have resisted every method; 10_6 joined them in January 2026, when its database value 3 turned out to be unproven (arXiv:2601.18757). A reinforcement-learning search over millions of diagrams (Applebaum et al., arXiv:2409.09032) found no shorter sequence for any open knot with at most 12 crossings, and Brittenham and Hermiller showed in 2025 that the unknotting number is not additive under connected sum. A shorter sequence for any cell here would be new: it lowers KnotInfo's upper bound and, since every cell's interval has length 1, settles the unknotting number of that knot.

## Cells

67 cells: 67 with a published best value, 0 first entries (no published value); 66 with a certificate here that the checker replays.

| Cell | Knot | Upper bound (best known) | Lower bound | Our certificate | Source |
| --- | --- | ---: | ---: | --- | --- |
| `unknotting-10-6` | 10_6 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_6.txt) | KnotInfo |
| `unknotting-10-11` | 10_11 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_11.txt) | KnotInfo |
| `unknotting-10-47` | 10_47 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_47.txt) | KnotInfo |
| `unknotting-10-51` | 10_51 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_51.txt) | KnotInfo |
| `unknotting-10-54` | 10_54 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_54.txt) | KnotInfo |
| `unknotting-10-61` | 10_61 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_61.txt) | KnotInfo |
| `unknotting-10-76` | 10_76 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_76.txt) | KnotInfo |
| `unknotting-10-77` | 10_77 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_77.txt) | KnotInfo |
| `unknotting-10-79` | 10_79 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_79.txt) | KnotInfo |
| `unknotting-10-100` | 10_100 | 3 | 2 | [3 changes](../refs/cells/unknotting/10_100.txt) | KnotInfo |
| `unknotting-11a-14` | 11a_14 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_14.txt) | KnotInfo |
| `unknotting-11a-18` | 11a_18 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_18.txt) | KnotInfo |
| `unknotting-11a-20` | 11a_20 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_20.txt) | KnotInfo |
| `unknotting-11a-45` | 11a_45 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_45.txt) | KnotInfo |
| `unknotting-11a-49` | 11a_49 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_49.txt) | KnotInfo |
| `unknotting-11a-53` | 11a_53 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_53.txt) | KnotInfo |
| `unknotting-11a-60` | 11a_60 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_60.txt) | KnotInfo |
| `unknotting-11a-83` | 11a_83 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_83.txt) | KnotInfo |
| `unknotting-11a-105` | 11a_105 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_105.txt) | KnotInfo |
| `unknotting-11a-126` | 11a_126 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_126.txt) | KnotInfo |
| `unknotting-11a-137` | 11a_137 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_137.txt) | KnotInfo |
| `unknotting-11a-161` | 11a_161 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_161.txt) | KnotInfo |
| `unknotting-11a-197` | 11a_197 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_197.txt) | KnotInfo |
| `unknotting-11a-202` | 11a_202 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_202.txt) | KnotInfo |
| `unknotting-11a-293` | 11a_293 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_293.txt) | KnotInfo |
| `unknotting-11a-304` | 11a_304 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_304.txt) | KnotInfo |
| `unknotting-11a-346` | 11a_346 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_346.txt) | KnotInfo |
| `unknotting-11a-354` | 11a_354 | 4 | 3 | [4 changes](../refs/cells/unknotting/11a_354.txt) | KnotInfo |
| `unknotting-11a-361` | 11a_361 | 4 | 3 | [4 changes](../refs/cells/unknotting/11a_361.txt) | KnotInfo |
| `unknotting-11a-362` | 11a_362 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_362.txt) | KnotInfo |
| `unknotting-11a-363` | 11a_363 | 3 | 2 | [3 changes](../refs/cells/unknotting/11a_363.txt) | KnotInfo |
| `unknotting-11a-366` | 11a_366 | 4 | 3 | [4 changes](../refs/cells/unknotting/11a_366.txt) | KnotInfo |
| `unknotting-11n-3` | 11n_3 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_3.txt) | KnotInfo |
| `unknotting-11n-17` | 11n_17 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_17.txt) | KnotInfo |
| `unknotting-11n-23` | 11n_23 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_23.txt) | KnotInfo |
| `unknotting-11n-30` | 11n_30 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_30.txt) | KnotInfo |
| `unknotting-11n-51` | 11n_51 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_51.txt) | KnotInfo |
| `unknotting-11n-54` | 11n_54 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_54.txt) | KnotInfo |
| `unknotting-11n-60` | 11n_60 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_60.txt) | KnotInfo |
| `unknotting-11n-65` | 11n_65 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_65.txt) | KnotInfo |
| `unknotting-11n-78` | 11n_78 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_78.txt) | KnotInfo |
| `unknotting-11n-94` | 11n_94 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_94.txt) | KnotInfo |
| `unknotting-11n-99` | 11n_99 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_99.txt) | KnotInfo |
| `unknotting-11n-112` | 11n_112 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_112.txt) | KnotInfo |
| `unknotting-11n-115` | 11n_115 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_115.txt) | KnotInfo |
| `unknotting-11n-116` | 11n_116 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_116.txt) | KnotInfo |
| `unknotting-11n-119` | 11n_119 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_119.txt) | KnotInfo |
| `unknotting-11n-120` | 11n_120 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_120.txt) | KnotInfo |
| `unknotting-11n-122` | 11n_122 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_122.txt) | KnotInfo |
| `unknotting-11n-128` | 11n_128 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_128.txt) | KnotInfo |
| `unknotting-11n-129` | 11n_129 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_129.txt) | KnotInfo |
| `unknotting-11n-137` | 11n_137 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_137.txt) | KnotInfo |
| `unknotting-11n-138` | 11n_138 | 2 | 1 | none yet | KnotInfo |
| `unknotting-11n-141` | 11n_141 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_141.txt) | KnotInfo |
| `unknotting-11n-142` | 11n_142 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_142.txt) | KnotInfo |
| `unknotting-11n-160` | 11n_160 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_160.txt) | KnotInfo |
| `unknotting-11n-161` | 11n_161 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_161.txt) | KnotInfo |
| `unknotting-11n-166` | 11n_166 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_166.txt) | KnotInfo |
| `unknotting-11n-169` | 11n_169 | 4 | 3 | [4 changes](../refs/cells/unknotting/11n_169.txt) | KnotInfo |
| `unknotting-11n-171` | 11n_171 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_171.txt) | KnotInfo |
| `unknotting-11n-172` | 11n_172 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_172.txt) | KnotInfo |
| `unknotting-11n-173` | 11n_173 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_173.txt) | KnotInfo |
| `unknotting-11n-177` | 11n_177 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_177.txt) | KnotInfo |
| `unknotting-11n-179` | 11n_179 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_179.txt) | KnotInfo |
| `unknotting-11n-180` | 11n_180 | 4 | 3 | [4 changes](../refs/cells/unknotting/11n_180.txt) | KnotInfo |
| `unknotting-11n-181` | 11n_181 | 3 | 2 | [3 changes](../refs/cells/unknotting/11n_181.txt) | KnotInfo |
| `unknotting-11n-182` | 11n_182 | 2 | 1 | [2 changes](../refs/cells/unknotting/11n_182.txt) | KnotInfo |

## Sources and licences

- KnotInfo (C. Livingston, A. H. Moore), the spreadsheet of 2 Nov 2026 as packaged by database_knotinfo 2026.11.2 (S. Oehms): `instances/knotinfo/knotinfo_data_complete.csv`, fetched by `fetch.sh` from https://raw.githubusercontent.com/soehms/database_knotinfo/219c2d982b89fb92b6ab0c556f28cdd766a18734/database_knotinfo/csv_data/knotinfo_data_complete.csv (SHA-256 `ed4447ff81dc50e2561764760d631356186c34e2dd35f89cc84e0a4d8fedd3d0`). knotinfo.org states no licence and asks users to cite KnotInfo; the database_knotinfo package that redistributes the spreadsheet is GPL-3.0. Not copied here: fetch.sh downloads it at the pinned commit and checks its SHA-256; the cells store only values read from it (knot names, braid words, the two bounds, Alexander polynomials, signatures), with the source.

## References

- C. Livingston, A. H. Moore, KnotInfo: Table of Knot Invariants, knotinfo.org, November 12, 2026 (the spreadsheet of 2 Nov 2026 as packaged by database_knotinfo 2026.11.2)
- A. A. Markov, Uber die freie Aquivalenz der geschlossenen Zopfe, Rec. Math. Moscou 1 (1936) 73-78; J. S. Birman, Braids, Links, and Mapping Class Groups, Princeton (1974): Markov's theorem
- T. Gittings, Minimum braids: a complete invariant of knots and links, arXiv:math/0401051 (2004): the minimal braid words behind KnotInfo's braid notation
- S. A. Bleiler, A note on unknotting number, Math. Proc. Cambridge Philos. Soc. 96 (1984) 469-471; Y. Nakanishi, Unknotting numbers and knot diagrams with the minimum crossings, Math. Sem. Notes Kobe Univ. 11 (1983) 257-258
- T. Applebaum, S. Blackwell, A. Davies, T. Edlich, A. Juhasz, M. Lackenby, N. Tomasev, D. Zheng, The unknotting number, hard unknot diagrams, and reinforcement learning, arXiv:2409.09032 (v2, 19 Jul 2025), to appear in Experimental Mathematics
- M. Brittenham, S. Hermiller, Unknotting number is not additive under connected sum, arXiv:2506.24088 (2025)
- Unknotting number and connected sums: the knots 4_1 and 5_1, arXiv:2601.18757 (January 2026): u(10_6) is 2 or 3
- D. McCoy, J. Park, Special alternating links of minimal unlinking number, arXiv:2603.10732 (v2, 24 Mar 2026): u = 4 for 11a291, 11a298, 11a319, 11a336, 11a340, 11a353, 11a356, 11a357
- A. Dranowski, Y. Kabkov, D. Tubbenhauer, RL unknotter, hard unknots and unknotting number, arXiv:2603.07955 (v4, Sep 2026): new upper bounds at 12 and 13 crossings only
- M. Jablonowski, Integer knot invariants: inequalities, computations, and open problems, arXiv:2605.22652 (v5, Sep 2026): new values at 13 crossings only

## Submitting and checking

Format: Text file: one move per line, applied in order to the knot's braid word (positions from 0): X p (crossing change at p, counted), I p a (insert a, -a before p), D p (delete a cancelling pair at p, p+1), C p (swap commuting letters at p, p+1), B p (a b a -> b a b at p), R k (move the first k letters to the end), F (every letter +-i -> +-(n-i)), S e (append e*n, n -> n+1), U (drop the last letter, the only one of index n-1; n -> n-1). See checkers/unknot_check.py.

```sh
python3 -I obb.py show unknotting-10-6
python3 -I obb.py check unknotting-10-6 my_submission.txt
python3 -I collections/open-tables/checkers/unknot_check.py 1,1,1,1,1,1,2,-1,-3,2,-3 my_submission.txt
```
