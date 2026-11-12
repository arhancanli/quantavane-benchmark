# Quantavane Open Tables

Benchmark tables for fields that have no keeper of records. Each table is one question with an exact checker of ours
(standard library only, last line `RESULT v`, exit status 0 only for a valid submission); each cell is one instance of
the question. Every cell says where its best known value comes from, and the two kinds are counted apart:

- **published value**: read from a paper or a public table, with its source and the date it was read. A submission
  that beats it is a new result against the literature, once a prior-art search (papers, GitHub and Zenodo, the last
  six months at least) finds nothing better.
- **first entry**: nothing comparable has been published, so the cell starts with a value of ours (or a baseline we
  computed). Beating it is a new best in this table, not a record against the literature.

This first version (12 November 2026) has two fields:

- **Topology**: the unknotting numbers of the knots with at most 11 crossings that are still open. Each cell is a knot
  with KnotInfo's interval [a, a + 1]; a submission is an unknotting sequence on a closed braid (Markov moves and
  crossing changes), replayed exactly by `checkers/unknot_check.py`. A sequence with a crossing changes, if anyone finds
  one, settles that knot's unknotting number. Our certificates replay KnotInfo's upper bound for 66 of the 67 knots.
- **Aerodynamics, in a numerical model**: two-dimensional airfoil sections scored by QV-Foil 1
  (`checkers/airfoil_check.py`), a classical model fixed in code: the Hess-Smith panel method, Thwaites' laminar
  boundary layer, Michel's transition criterion, Head's turbulent boundary layer and the Squire-Young drag formula.
  **It is a numerical model, not a wind tunnel**: a score says what the model computes, nothing more. It runs on the
  standard library with our own logarithm, exponential and arctangent, so every machine gives the same number. No value
  has been published for this model, so every cell is a first entry; each also records the best NACA 4- or 5-digit
  section (published shapes, scored by us) as its baseline.

<!--table-->
| Table | Field | Objective | Cells | Published values | First entries | Certified here |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| [Unknotting numbers of the knots with at most 11 crossings](problems/unknotting.md) | Topology | minimize | 67 | 67 | 0 | 66 |
| [Airfoil sections of greatest lift-to-drag ratio in the QV-Foil 1 model](problems/airfoil-ld.md) | Aerodynamics (numerical model) | maximize | 20 | 0 | 20 | 20 |
| [Airfoil sections of least drag at a required lift in the QV-Foil 1 model](problems/airfoil-cd.md) | Aerodynamics (numerical model) | minimize | 18 | 0 | 18 | 18 |
<!--/table-->

    python3 -I obb.py list open-tables                              # from the benchmark's root
    python3 -I obb.py show unknotting-10-6
    python3 -I obb.py check unknotting-10-6 my_sequence.txt
    python3 -I obb.py check airfoil-ld-re3m-t12 my_airfoil.txt
    python3 -I collections/open-tables/tests/test_open_tables.py

Layout: `problems/ID.json` and `problems/ID.md` (one per table: statement, context, references, sources, the cells
block), `cells/ID.jsonl` (one line per cell), `checkers/`, `refs/cells/` (our certificates: unknotting sequences that
replay the published bounds, NACA baselines and our airfoil designs), `tools/` (the programs that built the cells and
ran the searches), `tests/`. `tools/build.py` writes the pages, `index.json` and the table above from the problem files
and the cells. Every program uses the standard library only, except `tools/airfoil_search.py`, which uses numpy to
speed up the search (run it as `python3 tools/airfoil_search.py ...`); its designs count only through the checker.

Data and licences. Our code, cells and certificates: MIT (the benchmark's LICENSE). KnotInfo (C. Livingston and A. H.
Moore) states no licence and asks to be cited; the spreadsheet is redistributed under GPL-3.0 by the database_knotinfo
package. It is not copied here: `fetch.sh` downloads it at a pinned commit with its SHA-256, and the cells keep only the
values read from it (each knot's name, braid word, the two bounds, Alexander polynomial and signature), with the
source. The NACA sections are generated from their published formulas (NACA Reports 460, 610 and 824, US government
works in the public domain).
