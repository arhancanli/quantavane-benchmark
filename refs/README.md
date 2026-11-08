# Reference submissions kept in the repository

Our own results, each the best known entry of its source table when the problem file was written (the problem file
gives the source and the date it was read). They are also public in our records repositories and on the source
tables.

- `ours_sphere_d*_n*.txt`: spherical codes, from arhancanli/quantavane-spherical-codes (`codes/`), listed on
  spherical-codes.org.
- `ours_covering_*.txt`: covering designs, from arhancanli/quantavane-covering-records (`coverings/`), listed in the
  Covering Repository.
- `ours_cvrp_*.sol`: vehicle routing solutions in CVRPLIB's format, listed on CVRPLIB as the best known solutions.
- `ours_cw_*.txt`: constant weight codes, one word per line as the positions of its ones; the same codes as the
  files listed in Andries Brouwer's table (A(34,6,6): the table lists our 2,046 words with 10 words he added).
- `ours_ramsey_*.txt`: our Ramsey colourings R(3,18) >= 101 (K_100), R(4,18) >= 211 (K_210) and R(5,15) >= 283
  (K_282), from arhancanli/quantavane-ramsey-records (CC BY 4.0). Our K_522 for R(8,12) >= 523 is there too; it is
  not repeated here because its exact check takes longer than this test suite should.
- `ours_cage_6_9_n5600.s6` and `ours_cage_7_9_n17600.s6`: a 6-regular graph of girth 9 on 5600 vertices and a
  7-regular graph of girth 9 on 17600 vertices (cyclic lifts of K_7 and K_8), sent to House of Graphs on 8 Nov 2026;
  the cage table lists no graph for these cells yet.

Classical constructions built by our own code, credited in their first line and in the problem files. Some equal
the best known value (the root systems D5, E6, E7, the Barnes-Wall vectors, the cubic-residue colouring of K_127);
the others only show the format and exercise the checker:

- `classic_kissing_d5_D5_n40.txt`, `classic_kissing_d6_E6_n72.txt`, `classic_kissing_d7_E7_n126.txt`,
  `classic_kissing_d16_BW16_n4320.txt`: kissing configurations (Korkine and Zolotareff 1873; Barnes and Wall 1959);
  E6 and E7 are given in 8 coordinates as E8 roots orthogonal to one or two fixed roots.
- `classic_sortnet_batcher_n*.txt`: Batcher's odd-even merge sorting networks.
- `classic_golomb_erdos_turan_m29.txt`, `classic_golomb_erdos_turan_m30.txt`: Golomb rulers from the Erdos-Turan
  construction 2pk + (k^2 mod p) with p = 31.
- `classic_superperm_n8.txt`, `classic_superperm_n9.txt`: superpermutations of length 1! + 2! + ... + n! from the
  classical recursive construction.
- `classic_shannon_c7_k5_n243.txt`: the independent set {0,2,4}^5 in the fifth strong power of C_7.
- `classic_multiramsey_3333_n32.txt`: the Greenwood-Gleason 3-colouring of K_16 (cubic classes of GF(16)) with every
  vertex doubled, the doubled pairs in a fourth colour; `classic_multiramsey_444_n127.txt`: the edge {i,j} of K_127
  coloured by the cubic class of i - j modulo 127, which has no monochromatic K_4 (R(4,4,4) >= 128, the value of
  Hill and Irving).

Two small parameter files describe other authors' C16 constructions for the 16a-lower checker:
`maxr_c16_lower.json` (R and mu of maximusrufus's truncated trial function, the best value on the 16a page) and
`vid_c16_lower.json` (the mu of vidigoat's construction in pull request #270, in review). Their sources are in
`problems/16a-lower.json`.

Other authors' certificates are not kept here: `fetch.sh` downloads them into `certs/` at pinned commits and checks
each SHA-256 (among them the Leaps in Bounds certificates, MIT licence, for the snake, coil, cap set, superpermutation,
Schur, weak Schur, van der Waerden, no-three-in-line and degree-diameter problems).
