# DNA open in all six reading frames

`six-frame` · Biology · status: **open** · added 9 November 2026 (Quantavane Originals)

Best known value: **72** (minimize), Quantavane (Arhan Canli), 9 November 2026: simulated annealing over sequences of each length (single-base changes), minimising the stop codons and missing amino acids over the six frames (tools/src/sixframe.c)

## Statement

A DNA sequence has six reading frames: three on the strand itself, starting at its first, second or third base, and the same three on its reverse complement, each read as consecutive codons with the standard genetic code (an incomplete codon at the end is ignored). What is the shortest sequence in which all six frames are open, with no stop codon (TAA, TAG, TGA), and each frame contains all 20 amino acids? Every frame needs at least 20 codons, so at least 62 bases are needed. Best known: 72 bases (ours).

## Why it is interesting

Overlapping genes, where one stretch of DNA encodes proteins in two or more frames, are common in viruses (the first were found in the bacteriophage phiX174, Barrell, Air and Hutchison 1976) and occur in bacteria and animals; they show how much information a sequence can carry at once under the constraints of the genetic code, since a codon in one frame fixes parts of the codons in the others. The extreme case asks for a sequence that is an open reading frame in all six frames at once and uses the whole amino-acid alphabet in every one of them. The genetic code makes this tight: methionine (ATG) and tryptophan (TGG) have a single codon each, and the stops TAA, TAG and TGA must be avoided in all six frames, so their reverse complements TTA, CTA and TCA cannot appear in any forward frame either. Counting codons gives at least 62 bases; our search finds 72. The exact minimum, and its value when only the three forward frames are required, are open.

## Novelty check

Checked 9 November 2026, before the problem was added. Every search below is in [`novelty/six-frame.json`](../novelty/six-frame.json) with its address, the time it ran and its first results.

- arXiv API, 3 searches:
  - `all:"six reading frames" AND all:"amino acids"`: 0 results
  - `all:"overlapping genes" AND all:"reading frames" AND all:"all six"`: 0 results
  - `all:"open reading frames" AND all:"six frames" AND all:shortest`: 0 results
- OEIS, 1 searches:
  - `DNA sequence all six reading frames`: 0 results
- Web search (general web search), `shortest DNA sequence that encodes all 20 amino acids in every reading frame six frames overlapping codons all amino acids`: textbook material on reading frames and the genetic code, a 1990s piece on overlapping codes; no extremal result on sequences open in all six frames
- Open Problems Benchmark v2.0 (its 26 families and the keeper tables they come from): no sequence-design family in the benchmark.

Closest work found, and how this problem differs:
- Overlapping genes in viruses and other genomes (phiX174 and later): natural sequences coding in two or three frames, studied for their constraints and evolution, not this extremal question.
- Six-frame translation in genome annotation: every frame is read, with no extremal question.

Verdict: new question: overlapping genes and the coding capacity of overlapping frames are studied, but no result was found on the shortest sequence that is open in all six frames and uses all 20 amino acids in each.

## First values

| length | result | how |
| --- | --- | --- |
| lower bound | 62 | each of the six frames needs 20 codons |
| length 62 | not found | annealing, 60 s: at best 6 stop codons or missing amino acids left |
| length 63 | not found | annealing, 60 s: at best 5 stop codons or missing amino acids left |
| length 64 | not found | annealing, 60 s: at best 4 stop codons or missing amino acids left |
| length 65 | not found | annealing, 60 s: at best 4 stop codons or missing amino acids left |
| length 66 | not found | annealing, 60 s: at best 3 stop codons or missing amino acids left |
| length 67 | not found | annealing, 60 s: at best 3 stop codons or missing amino acids left |
| length 68 | not found | annealing, 60 s: at best 2 stop codons or missing amino acids left |
| length 69 | not found | annealing, 60 s: at best 2 stop codons or missing amino acids left |
| length 70 | not found | annealing, 60 s: at best 1 stop codons or missing amino acids left |
| length 71 | not found | annealing, 60 s: at best 1 stop codons or missing amino acids left |
| shortest found | 72 | ours (tools/src/sixframe.c) |

A length with no sequence found is not proved impossible; only 62 is a proved lower bound.

## Best known value

72 bases, held by Quantavane (Arhan Canli), 9 November 2026: the sequence in `refs/six-frame.txt`. Lower bound 62.

Bound on the other side: 62 (lower bound; each frame must contain 20 codons, so a frame starting at the third base needs 2 + 60 bases).

## Submitting and checking

Format: Text file: the DNA sequence (letters A, C, G, T; line breaks ignored).

Score: the length of the sequence (smaller is better). A submission improves the problem when its exact value is smaller than the best known value.

    python3 -I obb.py check six-frame FILE               # from the benchmark's root
    python3 -I collections/originals/checkers/orig_bio.py six-frame FILE

The checker is ours (standard library only); it prints the exact value as its last line `RESULT v` and exits 0 only for a valid certificate. Our certificate: `collections/originals/refs/six-frame.txt`.

## References

- B. G. Barrell, G. M. Air, C. A. Hutchison III, Overlapping genes in bacteriophage phiX174, Nature 264 (1976) 34-41
- The standard genetic code (NCBI translation table 1)
