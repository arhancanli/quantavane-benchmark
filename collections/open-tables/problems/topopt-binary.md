# Least-compliance 0/1 structures with a minimum feature size (QV-Topo 1)

`topopt-binary` · Structural topology optimisation (numerical model) · status: **open** · added 13 November 2026 (Quantavane Open Tables)

Headline cell `topopt-binary-mbb-60x20-v0.5-k2`: **189.894** (minimize), first entry (no published value): Quantavane (Arhan Canli), 2026-11-13: SIMP with a density filter of radius 3.0 and a projection (beta to 32); threshold, morphological repair, local search of 2-element strip moves

## Statement

Distribute a limited amount of material in a fixed grid of square elements so that the structure is as stiff as possible under one unit load (the least compliance). QV-Topo 1, a pinned finite-element model (checkers/topopt_check.py, standard library only): linear elasticity in plane stress with Young's modulus 1 and Poisson's ratio 0.3, void modelled as the same material with Young's modulus 1e-9, square bilinear elements of side 1, and a direct solver of our own whose sums are all correctly rounded, so every machine prints the same digits. THIS IS A NUMERICAL MODEL: a score is what the model computes for the submitted design, and the checker computes it from the design alone. In this table every element is solid (Young's modulus 1) or void (1e-9): at most the cell's volume fraction of the design elements may be solid; every solid element must lie in a k x k square of solid elements and every void element in a k x k square of void elements (a minimum feature size of k elements for both material and holes; outside the domain counts as void); no two solid elements may touch at a corner only; and the solid elements must form one edge-connected piece that reaches the load and the supports. Checkerboards, one-node hinges, thin struts and floating pieces therefore cannot score. Three load cases. MBB: the half MBB beam of the 88-line code (left edge free to slide vertically only, the bottom-right corner held vertically, a unit downward load at the top-left corner). Cantilever: the left edge clamped, a unit downward load at the bottom-right corner (the cantilever of the 99- and 88-line papers). L-bracket: an L-shaped domain with legs 2/5 of the side wide, clamped along the top of the vertical leg, a unit downward load at the middle of the end of the horizontal leg. The score is the compliance rounded up to 0.001. The headline cell is the MBB beam on 60 x 20 elements, volume fraction 0.5, minimum feature size 2.

## Why it is interesting

A part that can be made is solid or empty, with no struts or holes thinner than the process allows. Papers that report black-and-white designs reach them with projection filters or robust formulations and keep some grey, each under its own settings, so no published value applies to these cells: every cell is a first entry. The cells: each load case at volume fractions 0.3, 0.4 and 0.5 with minimum feature size 2, and at 0.5 with minimum feature size 3 (at lower volumes our first search found no sensible design with feature size 3; those cells can come later). The rules here are exact and checkable (a minimum feature size by squares of k elements, no point contacts, one connected piece), the same model as the SIMP table, so a 0/1 design can also be compared with the grey optimum of the same mesh. For scale only (different rules): the 88-line paper's preprint gives 189.14 for a projected, almost black-and-white MBB design on 60 x 20 elements with volume fraction 0.5 (its Fig. 8).

## Cells

12 cells: 0 with a published best value, 12 first entries (no published value); 12 with a certificate here that the checker replays.

| Cell | Parameters | Best | Status | Holder | Baseline (ours) | Published value |
| --- | --- | ---: | --- | --- | ---: | ---: |
| `topopt-binary-mbb-60x20-v0.3-k2` | mbb, 60 x 20, volume 0.3, feature size 2 | 330.685 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-mbb-60x20-v0.4-k2` | mbb, 60 x 20, volume 0.4, feature size 2 | 229.120 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-mbb-60x20-v0.5-k2` | mbb, 60 x 20, volume 0.5, feature size 2 | 189.894 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-mbb-60x20-v0.5-k3` | mbb, 60 x 20, volume 0.5, feature size 3 | 197.128 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-cantilever-80x50-v0.3-k2` | cantilever, 80 x 50, volume 0.3, feature size 2 | 69.707 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-cantilever-80x50-v0.4-k2` | cantilever, 80 x 50, volume 0.4, feature size 2 | 53.829 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-cantilever-80x50-v0.5-k2` | cantilever, 80 x 50, volume 0.5, feature size 2 | 44.247 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-cantilever-80x50-v0.5-k3` | cantilever, 80 x 50, volume 0.5, feature size 3 | 45.151 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-lbracket-50x50-v0.3-k2` | lbracket, 50 x 50, volume 0.3, feature size 2 | 268.575 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-lbracket-50x50-v0.4-k2` | lbracket, 50 x 50, volume 0.4, feature size 2 | 201.794 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-lbracket-50x50-v0.5-k2` | lbracket, 50 x 50, volume 0.5, feature size 2 | 167.593 | first entry | Quantavane (Arhan Canli) | - | - |
| `topopt-binary-lbracket-50x50-v0.5-k3` | lbracket, 50 x 50, volume 0.5, feature size 3 | 172.719 | first entry | Quantavane (Arhan Canli) | - | - |

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
- O. Sigmund, Morphology-based black and white filters for topology optimization, Struct. Multidisc. Optim. 33 (2007) 401-424: minimum length scales by morphology (open and close)
- J. K. Guest, J. H. Prevost, T. Belytschko, Achieving minimum length scale in topology optimization using nodal design variables and projection functions, Int. J. Numer. Meth. Eng. 61 (2004) 238-254

## Submitting and checking

Format: Text file: NELY lines of NELX characters 0 or 1 (the top row first; passive L-bracket elements 0). See checkers/topopt_check.py.

```sh
python3 -I obb.py show topopt-binary-mbb-60x20-v0.3-k2
python3 -I obb.py check topopt-binary-mbb-60x20-v0.3-k2 my_submission.txt
python3 -I collections/open-tables/checkers/topopt_check.py compliance mbb 60 20 0.5 binary 2 my_submission.txt
```
