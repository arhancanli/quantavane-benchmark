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

Two small parameter files describe other authors' C16 constructions for the 16a-lower checker:
`maxr_c16_lower.json` (R and mu of maximusrufus's truncated trial function, the best value on the 16a page) and
`vid_c16_lower.json` (the mu of vidigoat's construction in pull request #270, in review). Their sources are in
`problems/16a-lower.json`.
