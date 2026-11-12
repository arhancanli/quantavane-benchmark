# Periodic material cells of most negative Poisson's ratio with a stiffness floor (QV-Topo 1)

`metacell-poisson` · Metamaterials (numerical model) · status: **open** · added 13 November 2026 (Quantavane Open Tables)

Headline cell `metacell-poisson-n40-v0.5-k2-f0.01`: **-0.851727** (minimize), first entry (no published value): Quantavane (Arhan Canli), 2026-11-13: seed: rotating squares (angle 18 degrees, shrunk by 3.0, hinges of radius 2.0); local search of 2-element strip moves

## Statement

A periodic cell of 40 x 40 square elements describes a two-dimensional material: every element is solid (Young's modulus 1, Poisson's ratio 0.3, plane stress) or void (Young's modulus 1e-9). The cell must have at most the cell's volume fraction of solid elements, a minimum feature size of 2 (every solid element in a 2 x 2 solid square and every void one in a 2 x 2 void square, wrapping around the cell), no point contacts, and its solid elements must form one connected piece that wraps around the cell in both directions (a connected material). QV-Topo 1 (checkers/topopt_check.py, standard library only) computes the homogenised stiffness tensor C (Voigt notation, engineering shear strain) by the energy method with periodic boundary conditions: for each unit average strain the periodic displacement that minimises the energy, solved by our own direct solver, the same digits on every machine. THIS IS A NUMERICAL MODEL of an idealised material. The score is the larger of the two Poisson's ratios of a uniaxial stress along the cell's axes, nu12 = -S12/S11 and nu21 = -S12/S22 with S the inverse of C, rounded up to 0.000001; a cell is refused when either Young's modulus 1/S11 or 1/S22 is below the floor 0.01 (one per cent of the solid's), so that a mechanism with no stiffness cannot score. Two-dimensional stability bounds Poisson's ratio below by -1. The headline cell: volume fraction 0.5.

## Why it is interesting

Materials that widen when stretched (auxetics, negative Poisson's ratio) absorb energy and resist indentation; their microstructures are a classic target of inverse homogenisation (Sigmund 1994; Larsen, Sigmund and Bouwstra 1997). Without a stiffness requirement the problem degenerates into mechanisms, so each cell has a stiffness floor; Poisson's ratio is measured as in a tensile test (uniaxial stress), so no symmetry of the cell is needed. No published value applies under these settings: every cell is a first entry. Our first entries start from Grima and Evans' rotating squares (squares turned alternately, joined at the corners), drawn on the grid and then improved by a local search.

## Cells

3 cells: 0 with a published best value, 3 first entries (no published value); 3 with a certificate here that the checker replays.

| Cell | Parameters | Best | Status | Holder | Baseline (ours) | Published value |
| --- | --- | ---: | --- | --- | ---: | ---: |
| `metacell-poisson-n40-v0.4-k2-f0.01` | volume 0.4, stiffness floor 0.01 | -0.741009 | first entry | Quantavane (Arhan Canli) | - | - |
| `metacell-poisson-n40-v0.5-k2-f0.01` | volume 0.5, stiffness floor 0.01 | -0.851727 | first entry | Quantavane (Arhan Canli) | - | - |
| `metacell-poisson-n40-v0.6-k2-f0.01` | volume 0.6, stiffness floor 0.01 | -0.912989 | first entry | Quantavane (Arhan Canli) | - | - |

## References

- O. Sigmund, Materials with prescribed constitutive parameters: an inverse homogenization problem, Int. J. Solids Struct. 31 (1994) 2313-2329
- O. Sigmund, A new class of extremal composites, J. Mech. Phys. Solids 48 (2000) 397-428
- E. Andreassen, C. S. Andreasen, How to determine composite material properties using numerical homogenization, Comput. Mater. Sci. 83 (2014) 488-495: the energy method used here
- L. Xia, P. Breitkopf, Design of materials using topology optimization and energy-based homogenization approach in Matlab, Struct. Multidisc. Optim. 52 (2015) 1229-1241
- Z. Hashin, S. Shtrikman, A variational approach to the theory of the elastic behaviour of multiphase materials, J. Mech. Phys. Solids 11 (1963) 127-140; Z. Hashin, On elastic behaviour of fibre reinforced materials of arbitrary transverse phase geometry, J. Mech. Phys. Solids 13 (1965) 119-134: the two-dimensional bounds
- G. W. Milton, The Theory of Composites, Cambridge University Press (2002)
- R. Lakes, Foam structures with a negative Poisson's ratio, Science 235 (1987) 1038-1040
- J. N. Grima, K. E. Evans, Auxetic behavior from rotating squares, J. Mater. Sci. Lett. 19 (2000) 1563-1565
- U. D. Larsen, O. Sigmund, S. Bouwstra, Design and fabrication of compliant micromechanisms and structures with negative Poisson's ratio, J. Microelectromech. Syst. 6 (1997) 99-106

## Submitting and checking

Format: Text file: 40 lines of 40 characters 0 or 1 (the top row first). See checkers/topopt_check.py.

```sh
python3 -I obb.py show metacell-poisson-n40-v0.4-k2-f0.01
python3 -I obb.py check metacell-poisson-n40-v0.4-k2-f0.01 my_submission.txt
python3 -I collections/open-tables/checkers/topopt_check.py cell poisson 40 0.5 2 0.01 my_submission.txt
```
