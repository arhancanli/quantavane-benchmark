# Periodic material cells of greatest shear modulus (QV-Topo 1)

`metacell-shear` · Metamaterials (numerical model) · status: **open** · added 13 November 2026 (Quantavane Open Tables)

Headline cell `metacell-shear-n40-v0.5-k2`: **0.137341** (maximize), first entry (no published value): Quantavane (Arhan Canli), 2026-11-13: SIMP on the periodic cell (symmetric designs, density filter 2.0, projection), threshold, repair, local search of symmetric strip moves

## Statement

A periodic cell of 40 x 40 square elements describes a two-dimensional material: every element is solid (Young's modulus 1, Poisson's ratio 0.3, plane stress) or void (Young's modulus 1e-9). The cell must have at most the cell's volume fraction of solid elements, a minimum feature size of 2 (every solid element in a 2 x 2 solid square and every void one in a 2 x 2 void square, wrapping around the cell), no point contacts, and its solid elements must form one connected piece that wraps around the cell in both directions (a connected material). QV-Topo 1 (checkers/topopt_check.py, standard library only) computes the homogenised stiffness tensor C (Voigt notation, engineering shear strain) by the energy method with periodic boundary conditions: for each unit average strain the periodic displacement that minimises the energy, solved by our own direct solver, the same digits on every machine. THIS IS A NUMERICAL MODEL of an idealised material. The score is the shear modulus C33 (shear along the cell's axes), rounded down to 0.000001. The Voigt bound (the volume fraction times the solid's shear modulus) bounds it; the Hashin-Shtrikman shear bound holds only for isotropic materials and is not a bound here (a grid of diagonal bars exceeds it). The headline cell: volume fraction 0.5.

## Why it is interesting

The stiffest material in shear along given axes: the companion of the bulk-modulus table. Because the cells need not be isotropic, the bound to compare with is the Voigt bound, not the Hashin-Shtrikman one. No published value applies under these settings: every cell is a first entry. Each cell also keeps a baseline: a plain grid of diagonal bars.

## Cells

4 cells: 0 with a published best value, 4 first entries (no published value); 4 with a certificate here that the checker replays.

| Cell | Parameters | Best | Status | Holder | Baseline (ours) | Published value |
| --- | --- | ---: | --- | --- | ---: | ---: |
| `metacell-shear-n40-v0.3-k2` | volume 0.3 | 0.076536 | first entry | Quantavane (Arhan Canli) | 0.061023 | - |
| `metacell-shear-n40-v0.4-k2` | volume 0.4 | 0.107366 | first entry | Quantavane (Arhan Canli) | 0.107366 | - |
| `metacell-shear-n40-v0.5-k2` | volume 0.5 | 0.137341 | first entry | Quantavane (Arhan Canli) | 0.129834 | - |
| `metacell-shear-n40-v0.6-k2` | volume 0.6 | 0.168393 | first entry | Quantavane (Arhan Canli) | 0.151849 | - |

## References

- O. Sigmund, Materials with prescribed constitutive parameters: an inverse homogenization problem, Int. J. Solids Struct. 31 (1994) 2313-2329
- O. Sigmund, A new class of extremal composites, J. Mech. Phys. Solids 48 (2000) 397-428
- E. Andreassen, C. S. Andreasen, How to determine composite material properties using numerical homogenization, Comput. Mater. Sci. 83 (2014) 488-495: the energy method used here
- L. Xia, P. Breitkopf, Design of materials using topology optimization and energy-based homogenization approach in Matlab, Struct. Multidisc. Optim. 52 (2015) 1229-1241
- Z. Hashin, S. Shtrikman, A variational approach to the theory of the elastic behaviour of multiphase materials, J. Mech. Phys. Solids 11 (1963) 127-140; Z. Hashin, On elastic behaviour of fibre reinforced materials of arbitrary transverse phase geometry, J. Mech. Phys. Solids 13 (1965) 119-134: the two-dimensional bounds
- G. W. Milton, The Theory of Composites, Cambridge University Press (2002)

## Submitting and checking

Format: Text file: 40 lines of 40 characters 0 or 1 (the top row first). See checkers/topopt_check.py.

```sh
python3 -I obb.py show metacell-shear-n40-v0.3-k2
python3 -I obb.py check metacell-shear-n40-v0.3-k2 my_submission.txt
python3 -I collections/open-tables/checkers/topopt_check.py cell shear 40 0.5 2 0 my_submission.txt
```
