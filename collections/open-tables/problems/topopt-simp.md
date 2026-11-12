# Least-compliance structures in the SIMP model with a density filter (QV-Topo 1)

`topopt-simp` · Structural topology optimisation (numerical model) · status: **open** · added 13 November 2026 (Quantavane Open Tables)

Headline cell `topopt-simp-mbb-60x20-v0.5-r2.4`: **232.110** (minimize), beats the published value: Quantavane (Arhan Canli), 2026-11-13: OC from the design converged with a filter radius 6.00, then with the cell's radius to a change < 1e-5; below the published value 233.4878 (PINNeAPPle-Labs/PINNeAPPle on GitHub (Apache-2.0), examples/topology_optimization/results/mbb_summary.json at commit a3a93b7c (12 Oct 2026): 'MBB, MMA, filter', compliance 233.4878134 after 58 iterations of MMA (its script 01_mbb_beam.py: MBB 60 x 20, volume 0.5, density filter r_min = 2.4, the setup of the 88-line paper), read 2026-11-13. Other published values for the same setup: 233.71 (E. Andreassen, A. Clausen, M. Schevenels, B. S. Lazarov, O. Sigmund, Efficient topology optimization in MATLAB using 88 lines of code, preprint of 27 Oct 2010 (Lirias, KU Leuven, lirias.kuleuven.be/retrieve/225946), Fig. 3, bottom row (density filter), read 2026-11-13; the journal version (Struct. Multidisc. Optim. 43 (2011) 1-16) shows the same designs without the values. Section 3.4: MBB beam, volume fraction 0.5, penalty 3, filter radius 0.04 times the width (2.4 and 6). A number cited with attribution; no text or code copied); 233.6004 (UdvardiPeter/topokit on GitHub, MIT, benchmarks/tests/data/mbb_60x20_mma.npz, MMA capped at 100 iterations, commit 4f867d2c of 9 Aug 2026); 233.7146 (reproductions of the 88-line loop: qBraid/open-simulation-examples, Apache-2.0, 6 Oct 2026; lambdaclass/stabileo; tysunseven/topopt-hw))

## Statement

Distribute a limited amount of material in a fixed grid of square elements so that the structure is as stiff as possible under one unit load, that is, with the least compliance (the work done by the load). QV-Topo 1, a pinned finite-element model (checkers/topopt_check.py, standard library only): linear elasticity in plane stress with Young's modulus 1 and Poisson's ratio 0.3, void modelled as the same material with Young's modulus 1e-9, square bilinear elements of side 1, and a direct solver of our own whose sums are all correctly rounded, so every machine prints the same digits. THIS IS A NUMERICAL MODEL: a score is what the model computes for the submitted design, and the checker computes it from the design alone. In this table the design is a density field x in [0, 1], as in the 88-line code: the physical densities are x averaged by the linear density filter of the cell's radius (weights max(0, r - distance between element centres), design elements only), an element's Young's modulus is 1e-9 + xPhys^3 (1 - 1e-9) (penalty 3), and the filtered densities may add up to at most the cell's volume fraction of the design elements. The elements with xPhys >= 1/2 must form one edge-connected piece that reaches the load and the supports, so a checkerboard or a broken load path cannot score. Three load cases. MBB: the half MBB beam of the 88-line code (left edge free to slide vertically only, the bottom-right corner held vertically, a unit downward load at the top-left corner). Cantilever: the left edge clamped, a unit downward load at the bottom-right corner (the cantilever of the 99- and 88-line papers). L-bracket: an L-shaped domain with legs 2/5 of the side wide, clamped along the top of the vertical leg, a unit downward load at the middle of the end of the horizontal leg. The score is the compliance rounded up to 0.001. The headline cell is the MBB beam on 60 x 20 elements with volume fraction 0.5 and filter radius 2.4: exactly the density-filter example of the 88-line paper.

## Why it is interesting

Least-compliance design is the classic test problem of topology optimisation: every new method since Bendsoe and Kikuchi (1988) is shown on the MBB beam or the cantilever. Results are published paper by paper, each with its own mesh, filter, penalty, void stiffness and stopping rule, and most papers give the compliance only in a figure, so values are seldom comparable and nobody keeps records. This table fixes one model, that of the widely used 88-line code, so that values compare. Two cells have a published value under exactly these settings: the preprint of the 88-line paper prints the compliance of its density-filter MBB designs, 233.71 on 60 x 20 elements and 235.73 on 150 x 50, and the lowest value published for the 60 x 20 cell that we found is 233.4878 (a results file of the PINNeAPPle project on GitHub, October 2026, by the method of moving asymptotes). Our replay of that paper's optimality-criteria loop (our code, written from the paper, with its stopping rule: the largest change below 0.01) gives 233.7146 and 235.7337 at the last printed iteration, which confirms that the settings are the same. The other cells (volume fractions 0.3 and 0.4, the cantilever on 80 x 50 elements, the L-bracket on 50 x 50) have no published value under these settings and start as first entries. Each cell also keeps a baseline: our replay of the 88-line loop, scaled to the volume limit.

## Cells

10 cells: 2 with a published best value, 8 first entries (no published value); 10 with a certificate here that the checker replays.

| Cell | Parameters | Best | Status | Holder | Baseline (ours) | Published value |
| --- | --- | ---: | --- | --- | ---: | ---: |
| `topopt-simp-mbb-60x20-v0.5-r2.4` | mbb, 60 x 20, volume 0.5, filter radius 2.4 | 232.110 | beats the published value | Quantavane (Arhan Canli) | 233.725 | 233.4878 |
| `topopt-simp-mbb-150x50-v0.5-r6` | mbb, 150 x 50, volume 0.5, filter radius 6 | 233.714 | beats the published value | Quantavane (Arhan Canli) | 235.740 | 235.73 |
| `topopt-simp-mbb-60x20-v0.3-r2.4` | mbb, 60 x 20, volume 0.3, filter radius 2.4 | 526.494 | first entry | Quantavane (Arhan Canli) | 526.834 | - |
| `topopt-simp-mbb-60x20-v0.4-r2.4` | mbb, 60 x 20, volume 0.4, filter radius 2.4 | 315.536 | first entry | Quantavane (Arhan Canli) | 320.498 | - |
| `topopt-simp-cantilever-80x50-v0.3-r3` | cantilever, 80 x 50, volume 0.3, filter radius 3 | 88.660 | first entry | Quantavane (Arhan Canli) | 90.454 | - |
| `topopt-simp-cantilever-80x50-v0.4-r3` | cantilever, 80 x 50, volume 0.4, filter radius 3 | 62.668 | first entry | Quantavane (Arhan Canli) | 63.031 | - |
| `topopt-simp-cantilever-80x50-v0.5-r3` | cantilever, 80 x 50, volume 0.5, filter radius 3 | 49.445 | first entry | Quantavane (Arhan Canli) | 50.016 | - |
| `topopt-simp-lbracket-50x50-v0.3-r2` | lbracket, 50 x 50, volume 0.3, filter radius 2 | 371.579 | first entry | Quantavane (Arhan Canli) | 373.270 | - |
| `topopt-simp-lbracket-50x50-v0.4-r2` | lbracket, 50 x 50, volume 0.4, filter radius 2 | 247.854 | first entry | Quantavane (Arhan Canli) | 249.802 | - |
| `topopt-simp-lbracket-50x50-v0.5-r2` | lbracket, 50 x 50, volume 0.5, filter radius 2 | 192.028 | first entry | Quantavane (Arhan Canli) | 193.944 | - |

## Published values and licences

- Compliance 233.71 (MBB beam, 60 x 20 elements, volume fraction 0.5, penalty 3, density filter of radius 2.4) and 235.73 (150 x 50 elements, radius 6), the 88-line code's density-filter designs. Source: E. Andreassen, A. Clausen, M. Schevenels, B. S. Lazarov, O. Sigmund, Efficient topology optimization in MATLAB using 88 lines of code, preprint of 27 Oct 2010 (lirias.kuleuven.be/retrieve/225946), Fig. 3, bottom row, and section 3.4 (the settings); the journal version (Struct. Multidisc. Optim. 43 (2011) 1-16) shows the same designs without the values. Read 13 Nov 2026. Numbers cited as facts with attribution; no text, figure or code of the paper is copied or run. The code that wrote our baselines is ours, written from the paper's equations.
- Compliance 233.4878 for the same 60 x 20 cell, by the method of moving asymptotes (the lowest published value we found for this setup). Source: PINNeAPPle-Labs/PINNeAPPle on GitHub, examples/topology_optimization/results/mbb_summary.json, commit a3a93b7c of 12 Oct 2026 (script 01_mbb_beam.py: MBB 60 x 20, volume 0.5, density filter r_min = 2.4). Read 13 Nov 2026. Apache-2.0; the number is cited with attribution, nothing is copied or run.
- Other values for the same two cells: 233.6004 (60 x 20, MMA capped at 100 iterations) and 233.7146 or 235.7337 (reproductions of the 88-line loop with its stopping rule). Source: UdvardiPeter/topokit on GitHub (benchmarks/tests/data/mbb_60x20_mma.npz, 9 Aug 2026; MIT); qBraid/open-simulation-examples (topology-optimization/README.md, 6 Oct 2026; Apache-2.0); SOPTX (L. He, H. Wei, T. Tian), arXiv:2505.02438 (May 2025), the density-filter MBB figure at 150 x 50. Read 13 Nov 2026. Numbers cited with attribution; nothing is copied or run.

## References

- M. P. Bendsoe, N. Kikuchi, Generating optimal topologies in structural design using a homogenization method, Comput. Methods Appl. Mech. Eng. 71 (1988) 197-224
- M. P. Bendsoe, Optimal shape design as a material distribution problem, Struct. Optim. 1 (1989) 193-202: the SIMP model
- O. Sigmund, A 99 line topology optimization code written in Matlab, Struct. Multidisc. Optim. 21 (2001) 120-127: the MBB beam and the cantilever
- E. Andreassen, A. Clausen, M. Schevenels, B. S. Lazarov, O. Sigmund, Efficient topology optimization in MATLAB using 88 lines of code, Struct. Multidisc. Optim. 43 (2011) 1-16; the authors' preprint of 27 Oct 2010 (lirias.kuleuven.be/retrieve/225946) prints the compliance of each design in its Figs. 3, 4 and 8
- B. Bourdin, Filters in topology optimization, Int. J. Numer. Meth. Eng. 50 (2001) 2143-2158; T. E. Bruns, D. A. Tortorelli, Topology optimization of non-linear elastic structures and compliant mechanisms, Comput. Methods Appl. Mech. Eng. 190 (2001) 3443-3459: the density filter
- M. P. Bendsoe, O. Sigmund, Topology Optimization: Theory, Methods and Applications, Springer (2003)
- F. Ferrari, O. Sigmund, A new generation 99 line Matlab code for compliance topology optimization and its extension to 3D, Struct. Multidisc. Optim. 62 (2020) 2211-2228
- S. Rojas-Labanda, M. Stolpe, Benchmarking optimization solvers for structural topology optimization, Struct. Multidisc. Optim. 52 (2015) 527-547: a set of problem instances for comparing solvers (performance profiles, not a table of values under these settings)
- E. Biyikli, A. C. To, Proportional topology optimization, PLoS ONE 10 (2015) e0145041 (CC BY 4.0): MBB beam, cantilever and L-bracket against the 88-line code with filter radius 1.5, compliances shown in figures only

## Submitting and checking

Format: Text file: NELY lines of NELX numbers in [0, 1] (the design x; the top row first; passive L-bracket elements 0). See checkers/topopt_check.py.

```sh
python3 -I obb.py show topopt-simp-mbb-60x20-v0.5-r2.4
python3 -I obb.py check topopt-simp-mbb-60x20-v0.5-r2.4 my_submission.txt
python3 -I collections/open-tables/checkers/topopt_check.py compliance mbb 60 20 0.5 simp 2.4 my_submission.txt
```
