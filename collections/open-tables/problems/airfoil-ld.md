# Airfoil sections of greatest lift-to-drag ratio in the QV-Foil 1 model

`airfoil-ld` · Aerodynamics (numerical model) · status: **open** · added 12 November 2026 (Quantavane Open Tables)

Headline cell `airfoil-ld-re3m-t12`: **207.93** (maximize), first entry (no published value): Quantavane (Arhan Canli), 2026-11-12: CST design, CMA-ES from the CST fit of NACA 35015 (2500 evaluations, order 7, tools/airfoil_search.py); found for airfoil-ld-re3m-t15

## Statement

Design a two-dimensional airfoil section, given as a NACA 4- or 5-digit section or by class-shape coefficients of its two surfaces, and an angle of attack between -5 and 15 degrees, with the largest lift-to-drag ratio Cl/Cd at a given chord Reynolds number, subject to a smallest allowed largest thickness. QV-Foil 1, a pinned numerical model (checkers/airfoil_check.py): incompressible potential flow by the Hess-Smith panel method on 160 panels, Thwaites' laminar boundary layer, Michel's transition criterion, Head's turbulent boundary layer with the Ludwieg-Tillmann skin friction and the Squire-Young drag formula, with no viscous feedback on the pressures. THIS IS A NUMERICAL MODEL, NOT A WIND TUNNEL: a score is what the model computes and says nothing more about a real wing. Designs are refused when the outline is not simple, the trailing-edge wedge is below 4 degrees, the pitching moment about the quarter chord is below -0.10, the pitching moment about the quarter chord is below -0.10, or the turbulent boundary layer separates (H >= 2.4) before x = 0.99. The score is Cl/Cd rounded down to 0.01. The headline cell: Re = 3,000,000, thickness at least 12 % of the chord.

## Why it is interesting

Airfoil design has no keeper of records: results are published per paper, each with its own solver, mesh and settings, so no two values are comparable. These tables fix one classical model and its settings once, in code anyone can run (standard library only, the same result on every machine), so that values become comparable and an improvement is a fact about the model. Every cell starts as a first entry: no value has been published for this model. Each cell records the best of the classical NACA 4- and 5-digit sections scored by the model (the baseline: published shapes, our evaluation) and the best design found so far.

## Cells

20 cells: 0 with a published best value, 20 first entries (no published value); 20 with a certificate here that the checker replays.

| Cell | Parameters | Best | Holder | NACA baseline (published shape, our evaluation) |
| --- | --- | ---: | --- | --- |
| `airfoil-ld-re500k-t06` | re 500000, tmin 0.06 | 135.46 | Quantavane (Arhan Canli) | 98.64 (NACA 4307, alpha 5.5) |
| `airfoil-ld-re500k-t09` | re 500000, tmin 0.09 | 134.05 | Quantavane (Arhan Canli) | 88.65 (NACA 3409, alpha 4.0) |
| `airfoil-ld-re500k-t12` | re 500000, tmin 0.12 | 127.82 | Quantavane (Arhan Canli) | 69.40 (NACA 3512, alpha 1.5) |
| `airfoil-ld-re500k-t15` | re 500000, tmin 0.15 | 110.21 | Quantavane (Arhan Canli) | 29.66 (NACA 2715, alpha -1.0) |
| `airfoil-ld-re1m-t06` | re 1000000, tmin 0.06 | 172.53 | Quantavane (Arhan Canli) | 117.74 (NACA 5207, alpha 6.0) |
| `airfoil-ld-re1m-t09` | re 1000000, tmin 0.09 | 153.19 | Quantavane (Arhan Canli) | 113.44 (NACA 45009, alpha 6.5) |
| `airfoil-ld-re1m-t12` | re 1000000, tmin 0.12 | 144.83 | Quantavane (Arhan Canli) | 93.34 (NACA 3412, alpha 3.0) |
| `airfoil-ld-re1m-t15` | re 1000000, tmin 0.15 | 144.83 | Quantavane (Arhan Canli) | 51.13 (NACA 23015, alpha 2.25) |
| `airfoil-ld-re3m-t06` | re 3000000, tmin 0.06 | 243.14 | Quantavane (Arhan Canli) | 156.78 (NACA 5207, alpha 7.0) |
| `airfoil-ld-re3m-t09` | re 3000000, tmin 0.09 | 207.93 | Quantavane (Arhan Canli) | 147.36 (NACA 5210, alpha 5.75) |
| `airfoil-ld-re3m-t12` | re 3000000, tmin 0.12 | 207.93 | Quantavane (Arhan Canli) | 143.12 (NACA 45012, alpha 5.75) |
| `airfoil-ld-re3m-t15` | re 3000000, tmin 0.15 | 207.93 | Quantavane (Arhan Canli) | 111.94 (NACA 35015, alpha 3.75) |
| `airfoil-ld-re6m-t06` | re 6000000, tmin 0.06 | 260.78 | Quantavane (Arhan Canli) | 183.08 (NACA 5208, alpha 6.25) |
| `airfoil-ld-re6m-t09` | re 6000000, tmin 0.09 | 259.82 | Quantavane (Arhan Canli) | 179.22 (NACA 5210, alpha 6.5) |
| `airfoil-ld-re6m-t12` | re 6000000, tmin 0.12 | 259.82 | Quantavane (Arhan Canli) | 164.14 (NACA 45013, alpha 6.0) |
| `airfoil-ld-re6m-t15` | re 6000000, tmin 0.15 | 259.82 | Quantavane (Arhan Canli) | 155.86 (NACA 45015, alpha 4.75) |
| `airfoil-ld-re9m-t06` | re 9000000, tmin 0.06 | 287.30 | Quantavane (Arhan Canli) | 197.65 (NACA 5209, alpha 6.25) |
| `airfoil-ld-re9m-t09` | re 9000000, tmin 0.09 | 287.30 | Quantavane (Arhan Canli) | 196.55 (NACA 5210, alpha 6.5) |
| `airfoil-ld-re9m-t12` | re 9000000, tmin 0.12 | 287.30 | Quantavane (Arhan Canli) | 181.26 (NACA 4213, alpha 6.25) |
| `airfoil-ld-re9m-t15` | re 9000000, tmin 0.15 | 251.59 | Quantavane (Arhan Canli) | 171.70 (NACA 45015, alpha 5.25) |

## References

- J. L. Hess, A. M. O. Smith, Calculation of potential flow about arbitrary bodies, Prog. Aerospace Sci. 8 (1967) 1-138
- B. Thwaites, Approximate calculation of the laminar boundary layer, Aeronaut. Q. 1 (1949) 245-280; T. Cebeci, P. Bradshaw, Momentum Transfer in Boundary Layers, Hemisphere (1977): the fits for H and l
- R. Michel, Etude de la transition sur les profils d'aile, ONERA Rep. 1/1578A (1951)
- M. R. Head, Entrainment in the turbulent boundary layer, ARC R&M 3152 (1958); H. Ludwieg, W. Tillmann, Ing.-Arch. 17 (1949) 288-299
- H. B. Squire, A. D. Young, The calculation of the profile drag of aerofoils, ARC R&M 1838 (1938)
- B. M. Kulfan, Universal parametric geometry representation method, J. Aircraft 45 (2008) 142-158: the class-shape (CST) form
- E. N. Jacobs, K. E. Ward, R. M. Pinkerton, NACA Report 460 (1933); I. H. Abbott, A. E. von Doenhoff, L. S. Stivers, NACA Report 824 (1945): the NACA 4- and 5-digit sections (US government works, public domain)
- J. L. Moran, An Introduction to Theoretical and Computational Aerodynamics, Wiley (1984): the same combination of methods in a textbook
- S. Fazliani et al., ShapeBench, arXiv:2605.20763 (May 2026): an open shape-optimisation benchmark whose airfoil tasks are scored by the NeuralFoil surrogate, not by a model of this kind

## Submitting and checking

Format: Text file: 'alpha A' (degrees), then either 'naca DDDD' or 'naca DDDDD', or two lines 'upper a0 ... aN' and 'lower b0 ... bM' (class-shape coefficients, 1 <= N, M <= 15, |a| <= 1). See checkers/airfoil_check.py.

```sh
python3 -I obb.py show airfoil-ld-re500k-t06
python3 -I obb.py check airfoil-ld-re500k-t06 my_submission.txt
python3 -I collections/open-tables/checkers/airfoil_check.py ld 3000000 0.12 0 my_submission.txt
```
