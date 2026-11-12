# Airfoil sections of least drag at a required lift in the QV-Foil 1 model

`airfoil-cd` · Aerodynamics (numerical model) · status: **open** · added 12 November 2026 (Quantavane Open Tables)

Headline cell `airfoil-cd-re3m-cl0.6-t12`: **0.003995** (minimize), first entry (no published value): Quantavane (Arhan Canli), 2026-11-12: CST design, CMA-ES from the CST fit of NACA 35012 (2500 evaluations, order 7, tools/airfoil_search.py)

## Statement

Design a two-dimensional airfoil section and an angle of attack with the least drag coefficient Cd at a given chord Reynolds number, subject to a smallest required lift coefficient and a smallest allowed largest thickness. QV-Foil 1, a pinned numerical model (checkers/airfoil_check.py): incompressible potential flow by the Hess-Smith panel method on 160 panels, Thwaites' laminar boundary layer, Michel's transition criterion, Head's turbulent boundary layer with the Ludwieg-Tillmann skin friction and the Squire-Young drag formula, with no viscous feedback on the pressures. THIS IS A NUMERICAL MODEL, NOT A WIND TUNNEL: a score is what the model computes and says nothing more about a real wing. Designs are refused when the outline is not simple, the trailing-edge wedge is below 4 degrees, the pitching moment about the quarter chord is below -0.10, the pitching moment about the quarter chord is below -0.10, the turbulent boundary layer separates (H >= 2.4) before x = 0.99, or Cl is below the required value. The score is Cd rounded up to 0.000001. The headline cell: Re = 3,000,000, Cl at least 0.6, thickness at least 12 %.

## Why it is interesting

Airfoil design has no keeper of records: results are published per paper, each with its own solver, mesh and settings, so no two values are comparable. These tables fix one classical model and its settings once, in code anyone can run (standard library only, the same result on every machine), so that values become comparable and an improvement is a fact about the model. Every cell starts as a first entry: no value has been published for this model. Each cell records the best of the classical NACA 4- and 5-digit sections scored by the model (the baseline: published shapes, our evaluation) and the best design found so far.

## Cells

18 cells: 0 with a published best value, 18 first entries (no published value); 18 with a certificate here that the checker replays.

| Cell | Parameters | Best | Holder | NACA baseline (published shape, our evaluation) |
| --- | --- | ---: | --- | --- |
| `airfoil-cd-re1m-cl0.3-t09` | re 1000000, clmin 0.3, tmin 0.09 | 0.004340 | Quantavane (Arhan Canli) | 0.006702 (NACA 2709, alpha -0.25) |
| `airfoil-cd-re1m-cl0.3-t12` | re 1000000, clmin 0.3, tmin 0.12 | 0.005405 | Quantavane (Arhan Canli) | 0.007355 (NACA 3512, alpha -0.75) |
| `airfoil-cd-re1m-cl0.6-t09` | re 1000000, clmin 0.6, tmin 0.09 | 0.004891 | Quantavane (Arhan Canli) | 0.006788 (NACA 3409, alpha 2.0) |
| `airfoil-cd-re1m-cl0.6-t12` | re 1000000, clmin 0.6, tmin 0.12 | 0.005480 | Quantavane (Arhan Canli) | 0.007756 (NACA 3412, alpha 2.5) |
| `airfoil-cd-re1m-cl0.9-t09` | re 1000000, clmin 0.9, tmin 0.09 | 0.006437 | Quantavane (Arhan Canli) | 0.008597 (NACA 4310, alpha 3.75) |
| `airfoil-cd-re1m-cl0.9-t12` | re 1000000, clmin 0.9, tmin 0.12 | 0.006437 | Quantavane (Arhan Canli) | none |
| `airfoil-cd-re3m-cl0.3-t09` | re 3000000, clmin 0.3, tmin 0.09 | 0.003115 | Quantavane (Arhan Canli) | 0.005404 (NACA 35009, alpha 1.75) |
| `airfoil-cd-re3m-cl0.3-t12` | re 3000000, clmin 0.3, tmin 0.12 | 0.003598 | Quantavane (Arhan Canli) | 0.005986 (NACA 35012, alpha 2.0) |
| `airfoil-cd-re3m-cl0.6-t09` | re 3000000, clmin 0.6, tmin 0.09 | 0.003671 | Quantavane (Arhan Canli) | 0.005650 (NACA 35009, alpha 3.0) |
| `airfoil-cd-re3m-cl0.6-t12` | re 3000000, clmin 0.6, tmin 0.12 | 0.003995 | Quantavane (Arhan Canli) | 0.006029 (NACA 35012, alpha 2.75) |
| `airfoil-cd-re3m-cl0.9-t09` | re 3000000, clmin 0.9, tmin 0.09 | 0.004167 | Quantavane (Arhan Canli) | 0.006585 (NACA 4311, alpha 3.75) |
| `airfoil-cd-re3m-cl0.9-t12` | re 3000000, clmin 0.9, tmin 0.12 | 0.004799 | Quantavane (Arhan Canli) | 0.006881 (NACA 45012, alpha 4.5) |
| `airfoil-cd-re9m-cl0.3-t09` | re 9000000, clmin 0.3, tmin 0.09 | 0.002271 | Quantavane (Arhan Canli) | 0.004723 (NACA 35009, alpha 2.75) |
| `airfoil-cd-re9m-cl0.3-t12` | re 9000000, clmin 0.3, tmin 0.12 | 0.002496 | Quantavane (Arhan Canli) | 0.005116 (NACA 35012, alpha 2.25) |
| `airfoil-cd-re9m-cl0.6-t09` | re 9000000, clmin 0.6, tmin 0.09 | 0.002849 | Quantavane (Arhan Canli) | 0.004792 (NACA 35009, alpha 3.25) |
| `airfoil-cd-re9m-cl0.6-t12` | re 9000000, clmin 0.6, tmin 0.12 | 0.002849 | Quantavane (Arhan Canli) | 0.005162 (NACA 45012, alpha 3.25) |
| `airfoil-cd-re9m-cl0.9-t09` | re 9000000, clmin 0.9, tmin 0.09 | 0.003230 | Quantavane (Arhan Canli) | 0.005405 (NACA 45010, alpha 4.75) |
| `airfoil-cd-re9m-cl0.9-t12` | re 9000000, clmin 0.9, tmin 0.12 | 0.003981 | Quantavane (Arhan Canli) | 0.005465 (NACA 45012, alpha 4.5) |

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

Format: Text file: 'alpha A' (degrees), then either 'naca DDDD' or 'naca DDDDD', or two lines 'upper a0 ... aN' and 'lower b0 ... bM'. See checkers/airfoil_check.py.

```sh
python3 -I obb.py show airfoil-cd-re1m-cl0.3-t09
python3 -I obb.py check airfoil-cd-re1m-cl0.3-t09 my_submission.txt
python3 -I collections/open-tables/checkers/airfoil_check.py cd 3000000 0.12 0.6 my_submission.txt
```
