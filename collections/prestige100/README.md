# Quantavane Prestige 100

One hundred famous open problems in which a single object, checked exactly by a program, settles the score: a better Ramsey colouring, a Hadamard matrix of order 668, a Costas array of order 32, a 3 × 3 matrix multiplication with 22 multiplications, a shorter Mona Lisa tour. Each problem has its statement, why it matters, the best known value with its holders and history as recorded by the table that keeps it, the checker, the certificate format and a leaderboard.

Version 1.0, 2026-11-09. Every keeper was read on 9 November 2026; the date and time of each reading are on the problem's page. Values change when the keepers' tables change: check the keeper before claiming a record.

Choice. Fame first, then checkability: each problem has an exact checker in this benchmark and a certificate small enough to send. The list covers the smallest open Ramsey numbers and the diagonal ones, multicolour Ramsey numbers, Schur, weak Schur and van der Waerden numbers, the kissing numbers in every open dimension from 5 to 31, the smallest open cases of matrix multiplication, Hadamard matrices, Moore and strongly regular graphs, projective planes, Latin squares and Costas arrays, cages and the degree-diameter problem, sorting networks, Golomb rulers, cap sets, snake-in-the-box and superpermutations, two falsifiable Erdős problems, two optimization constants, the no-three-in-line problem and the Mona Lisa TSP. Quantavane holds the best known value in 7 of them, marked below: R(5,15), R(8,12) and WS(7) to WS(9) are in Leaps in Bounds' records, and R(3,18) and R(4,18) are published with a checker for the survey's next revision. They are in the list because they are cells of the famous tables, not the other way round.

Submitting: run `python3 -I obb.py check ID CERTIFICATE`, then send the certificate and a short record as in [SUBMITTING.md](../../SUBMITTING.md) (open an issue or write to arhan@quantavane.com). We rerun the check, add the result to `leaderboard.json` with your name or handle, and help you send it to the keeper of the table, who decides the listing. Machine-readable: `index.json` (everything) and `leaderboard.json`.

## Ramsey numbers

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 1 | [R(5,5)](problems/01-ramsey-5-5.md) | R(5,5) ≥ 43 | G. Exoo (1989) | `ramsey_check` |
| 2 | [R(6,6)](problems/02-ramsey-6-6.md) | R(6,6) ≥ 102 | J. G. Kalbfleisch (1966) | `ramsey_check` |
| 3 | [R(7,7)](problems/03-ramsey-7-7.md) | R(7,7) ≥ 205 | R. Mathon (1987) | `ramsey_check` |
| 4 | [R(8,8)](problems/04-ramsey-8-8.md) | R(8,8) ≥ 282 | J. P. Burling and S. W. Reyner (1972) | `ramsey_check` |
| 5 | [R(9,9)](problems/05-ramsey-9-9.md) | R(9,9) ≥ 565 | R. Mathon (1987) | `ramsey_check` |
| 6 | [R(10,10)](problems/06-ramsey-10-10.md) | R(10,10) ≥ 798 | R. Mathon (1987) | `ramsey_check` |
| 7 | [R(4,6)](problems/07-ramsey-4-6.md) | R(4,6) ≥ 36 | G. Exoo (2012) | `ramsey_check` |
| 8 | [R(3,10)](problems/08-ramsey-3-10.md) | R(3,10) ≥ 40 | G. Exoo (1989) | `ramsey_check` |
| 9 | [R(3,11)](problems/09-ramsey-3-11.md) | R(3,11) ≥ 47 | G. Exoo (2013) | `ramsey_check` |
| 10 | [R(3,12)](problems/10-ramsey-3-12.md) | R(3,12) ≥ 53 | M. Kolodyazhny (2015) | `ramsey_check` |
| 11 | [R(3,13)](problems/11-ramsey-3-13.md) | R(3,13) ≥ 61 | Google Research, ramsey_number_bounds (2026) | `ramsey_check` |
| 12 | [R(3,14)](problems/12-ramsey-3-14.md) | R(3,14) ≥ 67 | M. Kolodyazhny (2016) | `ramsey_check` |
| 13 | [R(4,7)](problems/13-ramsey-4-7.md) | R(4,7) ≥ 49 | G. Exoo (1989) | `ramsey_check` |
| 14 | [R(4,8)](problems/14-ramsey-4-8.md) | R(4,8) ≥ 59 | G. Exoo and M. Tatarevic (2015) | `ramsey_check` |
| 15 | [R(5,6)](problems/15-ramsey-5-6.md) | R(5,6) ≥ 59 | G. Exoo (2023) | `ramsey_check` |
| 16 | [R(5,7)](problems/16-ramsey-5-7.md) | R(5,7) ≥ 80 | N. J. Calkin, P. Erdős and C. A. Tovey (1997) | `ramsey_check` |
| 17 | [R(5,15)](problems/17-ramsey-5-15.md) | R(5,15) ≥ 283 (Quantavane) | A. Canli (Quantavane), 5 Nov 2026 | `ramsey_check` |
| 18 | [R(8,12)](problems/18-ramsey-8-12.md) | R(8,12) ≥ 523 (Quantavane) | A. Canli (Quantavane), 6 Nov 2026 | `ramsey_check` |
| 19 | [R(3,18)](problems/19-ramsey-3-18.md) | R(3,18) ≥ 101 (Quantavane) | A. Canli (Quantavane), 8 Nov 2026 | `ramsey_check` |
| 20 | [R(4,18)](problems/20-ramsey-4-18.md) | R(4,18) ≥ 211 (Quantavane) | A. Canli (Quantavane), 8 Nov 2026 | `ramsey_check` |

## Multicolour Ramsey numbers

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 21 | [R(3,3,3,3)](problems/21-multiramsey-3-3-3-3.md) | R(3,3,3,3) ≥ 51 | F. R. K. Chung (1973) | `multiramsey_check.py` |
| 22 | [R(4,4,4)](problems/22-multiramsey-4-4-4.md) | R(4,4,4) ≥ 128 | R. Hill and R. W. Irving (1982) | `multiramsey_check.py` |
| 23 | [R(3,3,5)](problems/23-multiramsey-3-3-5.md) | R(3,3,5) ≥ 45 | G. Exoo (1989) | `multiramsey_check.py` |
| 24 | [R(3,3,3,3,3)](problems/24-multiramsey-3-3-3-3-3.md) | R(3,3,3,3,3) ≥ 162 | G. Exoo (1994) | `multiramsey_check.py` |

## Schur and van der Waerden numbers

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 25 | [S(6)](problems/25-schur-6.md) | S(6) ≥ 538 | A. McKenna (4 Nov 2026) | `schur_check.py` |
| 26 | [S(7)](problems/26-schur-7.md) | S(7) ≥ 1696 | F. Rowley (2021) | `schur_check.py` |
| 27 | [WS(5)](problems/27-weak-schur-5.md) | WS(5) ≥ 207 | F. Rowley (2025) | `schur_check.py` |
| 28 | [WS(6)](problems/28-weak-schur-6.md) | WS(6) ≥ 650 | S. E. Rodrigo (2026) | `schur_check.py` |
| 29 | [WS(7)](problems/29-weak-schur-7.md) | WS(7) ≥ 2154 (Quantavane) | A. Canli (Quantavane), 8 Nov 2026 | `schur_check.py` |
| 30 | [WS(8)](problems/30-weak-schur-8.md) | WS(8) ≥ 7002 (Quantavane) | A. Canli (Quantavane), 8 Nov 2026 | `schur_check.py` |
| 31 | [WS(9)](problems/31-weak-schur-9.md) | WS(9) ≥ 22620 (Quantavane) | A. Canli (Quantavane), 8 Nov 2026 | `schur_check.py` |
| 32 | [W(2,7)](problems/32-vdw-2-7.md) | W(2,7) ≥ 3704 | J. Rabung and M. Lotts (2012) | `vdw_check.py` |
| 33 | [W(4,4)](problems/33-vdw-4-4.md) | W(4,4) ≥ 1049 | J. Rabung and M. Lotts (2012) | `vdw_check.py` |
| 34 | [W(5,3)](problems/34-vdw-5-3.md) | W(5,3) ≥ 171 | J. Rabung and M. Lotts (2012) | `vdw_check.py` |

## Kissing numbers

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 35 | [Kissing number, dimension 5](problems/35-kissing-d5.md) | κ(5) ≥ 40 | A. Korkine and G. Zolotareff (1873) | `kissing_check.py` |
| 36 | [Kissing number, dimension 6](problems/36-kissing-d6.md) | κ(6) ≥ 72 | A. Korkine and G. Zolotareff (1873) | `kissing_check.py` |
| 37 | [Kissing number, dimension 7](problems/37-kissing-d7.md) | κ(7) ≥ 126 | A. Korkine and G. Zolotareff (1873) | `kissing_check.py` |
| 38 | [Kissing number, dimension 9](problems/38-kissing-d9.md) | κ(9) ≥ 306 | J. Leech and N. J. A. Sloane (1971) | `kissing_check.py` |
| 39 | [Kissing number, dimension 10](problems/39-kissing-d10.md) | κ(10) ≥ 510 | M. Ganzhinov (2022) | `kissing_check.py` |
| 40 | [Kissing number, dimension 11](problems/40-kissing-d11.md) | κ(11) ≥ 604 | F. Bianchi, Y. Kwon, A. Pappu and J. Zou (2026) | `kissing_check.py` |
| 41 | [Kissing number, dimension 12](problems/41-kissing-d12.md) | κ(12) ≥ 841 | R. Takhanov, Z. Assylbekov and S. Yun (2026) | `kissing_check.py` |
| 42 | [Kissing number, dimension 13](problems/42-kissing-d13.md) | κ(13) ≥ 1154 | V. A. Zinoviev and T. Ericson (1999) | `kissing_check.py` |
| 43 | [Kissing number, dimension 14](problems/43-kissing-d14.md) | κ(14) ≥ 1932 | M. Ganzhinov (2022) | `kissing_check.py` |
| 44 | [Kissing number, dimension 15](problems/44-kissing-d15.md) | κ(15) ≥ 2564 | J. Leech and N. J. A. Sloane (1971) | `kissing_check.py` |
| 45 | [Kissing number, dimension 16](problems/45-kissing-d16.md) | κ(16) ≥ 4320 | E. S. Barnes and G. E. Wall (1959) | `kissing_check.py` |
| 46 | [Kissing number, dimension 17](problems/46-kissing-d17.md) | κ(17) ≥ 5730 | H. Cohn and A. Li (2024) | `kissing_check.py` |
| 47 | [Kissing number, dimension 18](problems/47-kissing-d18.md) | κ(18) ≥ 8358 | A. Kravatskiy (2026) | `kissing_check.py` |
| 48 | [Kissing number, dimension 19](problems/48-kissing-d19.md) | κ(19) ≥ 12460 | K. Li (2026) | `kissing_check.py` |
| 49 | [Kissing number, dimension 20](problems/49-kissing-d20.md) | κ(20) ≥ 19448 | H. Cohn and A. Li (2024) | `kissing_check.py` |
| 50 | [Kissing number, dimension 21](problems/50-kissing-d21.md) | κ(21) ≥ 31560 | K. Li (2026) | `kissing_check.py` |
| 51 | [Kissing number, dimension 22](problems/51-kissing-d22.md) | κ(22) ≥ 49896 | J. Leech (1967) | `kissing_check.py` |
| 52 | [Kissing number, dimension 23](problems/52-kissing-d23.md) | κ(23) ≥ 93150 | J. Leech (1967) | `kissing_check.py` |
| 53 | [Kissing number, dimension 25](problems/53-kissing-d25.md) | κ(25) ≥ 197584 | A. Kravatskiy (2026) | `kissing_check.py` |
| 54 | [Kissing number, dimension 26](problems/54-kissing-d26.md) | κ(26) ≥ 201136 | A. Kravatskiy (2026) | `kissing_check.py` |
| 55 | [Kissing number, dimension 27](problems/55-kissing-d27.md) | κ(27) ≥ 209825 | A. Kravatskiy (2026) | `kissing_check.py` |
| 56 | [Kissing number, dimension 28](problems/56-kissing-d28.md) | κ(28) ≥ 221988 | A. Kravatskiy (2026) | `kissing_check.py` |
| 57 | [Kissing number, dimension 29](problems/57-kissing-d29.md) | κ(29) ≥ 231697 | A. Kravatskiy (2026) | `kissing_check.py` |
| 58 | [Kissing number, dimension 30](problems/58-kissing-d30.md) | κ(30) ≥ 247972 | A. Kravatskiy (2026) | `kissing_check.py` |
| 59 | [Kissing number, dimension 31](problems/59-kissing-d31.md) | κ(31) ≥ 251200 | A. Kravatskiy (2026) | `kissing_check.py` |

## Matrix multiplication

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 60 | [3 × 3 matrix multiplication](problems/60-matmul-3x3x3.md) | rank ≤ 23 | J. D. Laderman (1976) | `matmul_check.py` |
| 61 | [4 × 4 matrix multiplication](problems/61-matmul-4x4x4.md) | rank ≤ 48 over the rationals | A. Novikov et al. (AlphaEvolve, 2025), as credited by the catalogue | `matmul_check.py` |

## Hadamard matrices

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 62 | [Hadamard matrix of order 668](problems/62-hadamard-668.md) | none known | none | `hadamard_check.py` |
| 63 | [Hadamard matrix of order 716](problems/63-hadamard-716.md) | none known | none | `hadamard_check.py` |
| 64 | [Hadamard matrix of order 892](problems/64-hadamard-892.md) | none known | none | `hadamard_check.py` |

## Moore graph and strongly regular graphs

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 65 | [Moore graph of degree 57](problems/65-moore-57.md) | none known | none | `srg_check.py` |
| 66 | [Conway's 99-graph](problems/66-srg-99-14-1-2.md) | none known | none | `srg_check.py` |
| 67 | [srg(88, 27, 6, 9)](problems/67-srg-88-27-6-9.md) | none known | none | `srg_check.py` |

## Projective planes and Latin squares

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 68 | [Projective plane of order 12](problems/68-projplane-12.md) | none known | none | `projplane_check.py` |
| 69 | [Three MOLS of order 10](problems/69-mols-10.md) | 2 | E. T. Parker (1959) | `mols_check.py` |

## Costas arrays

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 70 | [Costas array of order 32](problems/70-costas-32.md) | none known | none | `costas_check.py` |
| 71 | [Costas array of order 33](problems/71-costas-33.md) | none known | none | `costas_check.py` |

## Cages

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 72 | [Cage n(3,13)](problems/72-cage-3-13.md) | n(3,13) ≤ 272 | Hoare, reported by Biggs ([Bi89]) | `cage_check.py` |
| 73 | [Cage n(3,14)](problems/73-cage-3-14.md) | n(3,14) ≤ 372 | [EK26] in the House of Graphs table | `cage_check.py` |
| 74 | [Cage n(3,15)](problems/74-cage-3-15.md) | n(3,15) ≤ 620 | N. Biggs and M. J. Hoare (1983) | `cage_check.py` |
| 75 | [Cage n(3,16)](problems/75-cage-3-16.md) | n(3,16) ≤ 702 | [P26] in the House of Graphs table | `cage_check.py` |
| 76 | [Cage n(4,9)](problems/76-cage-4-9.md) | n(4,9) ≤ 270 | G. Exoo, J. Goedgebeur, J. Jooken, T. Stubbe and G. Van den Eede (2026) | `cage_check.py` |
| 77 | [Cage n(5,7)](problems/77-cage-5-7.md) | n(5,7) ≤ 152 | [MY] in the House of Graphs table | `cage_check.py` |

## Degree-diameter problem

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 78 | [(3,5)-graph](problems/78-degdiam-3-5.md) | 70 vertices | C. von Conta (1983); I. Alegre, M. A. Fiol and J. L. A. Yebra (1986) | `degdiam_check.py` |
| 79 | [(3,6)-graph](problems/79-degdiam-3-6.md) | 132 vertices | G. Exoo (1998) | `degdiam_check.py` |
| 80 | [(4,3)-graph](problems/80-degdiam-4-3.md) | 41 vertices | J. Allwright (1992) | `degdiam_check.py` |
| 81 | [(4,4)-graph](problems/81-degdiam-4-4.md) | 104 vertices | N. Bhakar (Aug 2026) | `degdiam_check.py` |
| 82 | [(5,3)-graph](problems/82-degdiam-5-3.md) | 72 vertices | G. Exoo (2001) | `degdiam_check.py` |
| 83 | [(8,2)-graph](problems/83-degdiam-8-2.md) | 57 vertices | R. M. Storwick (1970) | `degdiam_check.py` |

## Sorting networks

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 84 | [Sorting network, 13 inputs](problems/84-sortnet-n13-size.md) | 45 comparators | as listed in D. E. Knuth's TAOCP vol. 3 | `sortnet_check.py` |
| 85 | [Sorting network, 14 inputs](problems/85-sortnet-n14-size.md) | 51 comparators | as listed in D. E. Knuth's TAOCP vol. 3 | `sortnet_check.py` |
| 86 | [Sorting network, 15 inputs](problems/86-sortnet-n15-size.md) | 56 comparators | as listed in D. E. Knuth's TAOCP vol. 3 | `sortnet_check.py` |
| 87 | [Sorting network, 16 inputs](problems/87-sortnet-n16-size.md) | 60 comparators | M. W. Green (1969), in TAOCP vol. 3 | `sortnet_check.py` |
| 88 | [Sorting network, 17 inputs](problems/88-sortnet-n17-size.md) | 71 comparators | S. W. Al-Haj Baddar (2009) | `sortnet_check.py` |

## Golomb rulers

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 89 | [Golomb ruler, 29 marks](problems/89-golomb-29.md) | length ≤ 623 | M. D. Atkinson and A. Hassenklover (1984) | `golomb_check.py` |
| 90 | [Golomb ruler, 30 marks](problems/90-golomb-30.md) | length ≤ 680 | M. D. Atkinson and A. Hassenklover (1984) | `golomb_check.py` |

## Cap sets

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 91 | [Cap set in F_3^7](problems/91-capset-n7.md) | 236 points | A. R. Calderbank and P. C. Fishburn (1994) | `capset_check.py` |
| 92 | [Cap set in F_3^8](problems/92-capset-n8.md) | 512 points | B. Romera-Paredes et al. (FunSearch, 2023) | `capset_check.py` |

## Snake-in-the-box

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 93 | [Snake in the 9-cube](problems/93-snake-d9.md) | 191 edges | M. Orland, B. Fagan et al. (2026) | `snake_check.py` |

## Superpermutations

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 94 | [Minimal superpermutation, n = 6](problems/94-superperm-n6.md) | length ≤ 872 | R. Houston (2014) | `superperm_check.py` |

## Erdős problems

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 95 | [Erdős #107 (happy ending)](problems/95-erdos-107.md) | no counterexample known | none | `convex_check.py` |
| 96 | [Erdős #993 (trees)](problems/96-erdos-993.md) | no counterexample known | none | `tree_unimodal_check.py` |

## Optimization constants

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 97 | [Sidon autocorrelation constant C_1a](problems/97-1a-upper.md) | C_1a ≤ 1.5027434868 | Atris (2026), on the constant's page | `autocorr_check.py` |
| 98 | [Independent sets in C7^5](problems/98-shannon-c7-power5.md) | 367 vertices | S. C. Polak and A. Schrijver (2018) | `strongpow_check.py` |

## No-three-in-line

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 99 | [No-three-in-line, 75 × 75](problems/99-no3line-75.md) | 148 points | the 74 × 74 solution (T. Prellberg, 2026) placed in the 75 × 75 grid | `no3line_check.py` |

## Travelling salesman

| # | Problem | Best known | Holder | Checker |
| --- | --- | --- | --- | --- |
| 100 | [Mona Lisa TSP](problems/100-tsp-mona-lisa.md) | tour length 5,757,191 | Y. Nagata (17 Mar 2009) | `tsp_check.py` |

## The keepers

The records belong to the people who found them, and the tables to the people who keep them. This collection only gathers them, with credit:

- [Small Ramsey Numbers (S. P. Radziszowski), Electronic Journal of Combinatorics, Dynamic Survey DS1](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1), read 2026-11-09 16:02 +04.
- [Leaps in Bounds (D. Munro)](https://github.com/daniel-munro/leaps-in-bounds), read 2026-11-09 15:49 +04.
- [Kissing numbers (H. Cohn)](https://cohn.mit.edu/kissing-numbers/), read 2026-11-09 15:51 +04.
- [A. Kravatskiy, KissingNumbers (GitHub)](https://github.com/alexlegeartis/KissingNumbers), read 2026-11-09 15:56 +04.
- [Yet another catalogue of fast matrix multiplication algorithms (A. Sedoglavic)](https://fmm.univ-lille.fr/), read 2026-11-09 15:58 +04.
- [Optimization constants in mathematics, constant 23a (T. Tao et al.)](https://teorth.github.io/optimizationproblems/constants/23a.html), read 2026-11-09 15:58 +04.
- [The (Degree, Diameter) Problem for Graphs (F. Comellas)](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), read 2026-11-09 15:51 +04.
- [Parameters of strongly regular graphs (A. E. Brouwer)](https://www.win.tue.nl/~aeb/graphs/srg/srgtab.html), read 2026-11-09 15:52 +04.
- [The On-Line Encyclopedia of Integer Sequences](https://oeis.org), read 2026-11-09 16:14 +04.
- [K. Drakakis, Open problems in Costas arrays (arXiv:1102.5727)](https://arxiv.org/abs/1102.5727), read 2026-11-09 16:05 +04.
- [House of Graphs cage table (J. Goedgebeur, J. Jooken, T. Van den Eede)](https://houseofgraphs.org/meta-directory/cages), read 2026-11-09 07:4x +04.
- [Smallest and fastest sorting networks (B. Dobbelaere)](https://bertdobbelaere.github.io/sorting_networks.html), read 2026-11-09 15:51 +04.
- [Erdős Problems (T. F. Bloom)](https://www.erdosproblems.com), read 2026-11-09 15:58 +04.
- [Optimization constants in mathematics, constant 1a (T. Tao et al.)](https://teorth.github.io/optimizationproblems/constants/1a.html), read 2026-11-09 15:58 +04.
- [Optimization constants in mathematics, constant 9 (T. Tao et al.)](https://teorth.github.io/optimizationproblems/constants/9a.html), read 2026-11-09 15:58 +04.
- [No-three-in-line records (A. Flammenkamp), via Leaps in Bounds](http://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html), read 2026-11-09 15:49 +04.
- [Mona Lisa TSP Challenge (W. Cook)](https://www.math.uwaterloo.ca/tsp/data/ml/monalisa.html), read 2026-11-09 15:58 +04.

Checkers are Quantavane's own code (MIT); the statements and data credit their sources. Corrections are welcome: open an issue.
