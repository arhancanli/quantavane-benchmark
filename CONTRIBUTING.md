# Contributing to the Open Problems Benchmark

Draft for the benchmark repository (9 Nov 2026, 09:2x +04). Nothing here is public until the owner approves it and
adds it to the repository.

Anyone can contribute: a better object for one of the problems, an independent check of a certificate, a checker of
your own, a new table, or a correction. You do not need to be at a university.

## Submitting a result

1. Find a problem. `python3 -I obb.py families` lists the families and their tables, `python3 -I obb.py list FAMILY`
   lists the cells of one family, and `python3 -I obb.py show PROBLEM` prints a problem in full: its statement, the
   format of a certificate, the best known value, where and when we read it, and who holds it.
2. Check your object yourself: `python3 -I obb.py check PROBLEM FILE`. The checker prints the exact value it proves
   and whether it beats the best known value. A certificate the checker does not accept scores nothing.
3. Write the short record described in SUBMITTING.md: the problem, the file and its SHA-256, the name or handle you
   want shown, how the object was found, whether an AI system helped, and the date.
   `python3 -I obb.py verify RECORD.json` checks the record and prints the leaderboard row it earns.
4. Send it: open an issue or a pull request with the record and the certificate, or write to arhan@quantavane.com.
   Large certificates may be compressed with gzip or xz.
5. We run the checker again on our side and add your row to `leaderboard.json`, usually the same day.

If your result beats the value in the keeper's table, it belongs in that table too. Each family names its keeper and
page. You can send it yourself, or we can help you send it, always under your name.

## How credit works

- The leaderboard row carries your name or handle, exactly as you choose, with the date we checked it and the
  benchmark version.
- A result you send to a keeper is credited to you in that table; we never send someone else's result as ours.
- A paper of ours that uses your result lists you as a co-author, or cites you if you prefer (Quantavane Open
  Research: https://quantavane.com/open-research/).
- Corrections (a value we read wrongly, a holder we missed, a broken statement) are credited by name in CHANGELOG.md.

## Using AI systems

Any method is welcome, including computer search and AI systems. We ask one thing: say which systems you used and for
what, in the record's `ai_assistance` field. For example: "none"; "a language model wrote the search program, the
object came from running it"; "the construction was suggested by a language model and checked by hand". The field is
published with your row. Results are judged only by the checker, and saying that you used AI never lowers the credit.

Some keepers and journals have their own rules on AI use. Read them before you send a result there.

## The leaderboard

`leaderboard.json` lists every verified result that reaches or beats a best known value: the problem, the exact value,
the submitter, the source, the AI-use statement, the certificate's SHA-256, the dates submitted and verified, the
benchmark version and the checker. `python3 -I obb.py leaderboard` shows them, best first;
`python3 -I obb.py leaderboard PROBLEM` shows one problem. Family cells appear by their id, like any other problem.

## Other ways to help

- An independent checker. Write your own checker for a family; we compare it with ours on the reference objects and
  on random cases, and list it as a second check.
- A new table. Propose a table kept by someone else, with an exact checker: who keeps it, where the values come from,
  how open cells are told apart from solved ones, and whether the values may be quoted with credit.
- A correction. If a cell is wrong or out of date, open an issue with a link to the keeper's page.

## Rules

- Certificates are data. Checkers never run code from a submission.
- Values are compared exactly. A printed value whose exact original is unknown counts only when it is beaten by more
  than its last printed digit.
- Only values are stored here, with their sources; keepers' files are never copied.
- The keepers maintain these tables for everyone, mostly unpaid. Follow their rules when you send them results.
