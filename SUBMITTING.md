# Submitting a result

A submission is a certificate (the object itself, in the problem's format) and a short record that says who sent it
and where it comes from. We check the certificate with the problem's checker, record the exact value it proves and add
a row to `leaderboard.json` with your name or handle.

## 1. Check it yourself

    python3 -I obb.py check PROBLEM CERTIFICATE

The checker prints the exact value it proves and whether it improves the best known value on the source page and the
best verified value still in review. A certificate the checker does not accept scores nothing.

## 2. Write the record

A JSON file next to the certificate:

```json
{
 "problem": "ramsey-5-5",
 "certificate": "r55_k43.txt",
 "sha256": "the SHA-256 of the certificate file, in hex",
 "submitter": "your name or a handle, as it should appear",
 "source": "how the object was found: method, code, paper or earlier result it builds on",
 "ai_assistance": "none, or which AI systems were used and for what",
 "date": "2026-11-08"
}
```

`python3 -I obb.py verify RECORD.json` checks that every field is there, that the certificate matches its SHA-256,
runs the checker, and prints the leaderboard row the submission earns.

## 3. Send it

Open an issue or a pull request with the record and the certificate (large certificates may be compressed with gzip
or xz; say so in the record's source), or write to arhan@quantavane.com. We rerun the check, add the row to
`leaderboard.json` and credit you in the problem's results. A result that improves the source table is worth sending
to its keeper too; we can help with that.

## Rules

- The value is what the checker proves, exactly. A printed value whose exact original is unknown counts only when it
  is beaten by more than its last printed digit.
- Any method is welcome, including computer search and AI systems; say which in the record.
- Certificates are data. Checkers never run code from a submission.
- Each problem file states the version of the benchmark it was added in (`added`); the release notes are in
  `CHANGELOG.md`. A row in `leaderboard.json` names the benchmark version it was verified under.
