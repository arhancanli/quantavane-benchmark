#!/usr/bin/env python3
"""Unknotting sequences on closed braids (Quantavane Open Tables; standard library only).

  python3 -I unknot_check.py BRAID CERTIFICATE

BRAID is the knot's braid word: comma-separated non-zero integers, i for sigma_i and -i for its inverse (KnotInfo's
braid notation without the brackets). The braid has n = max |i| + 1 strands and its closure must be a knot.

CERTIFICATE is a text file of moves, applied in order to the current braid word w on n strands. Positions count from
0; '#' starts a comment. Every move except X keeps the closed braid in its isotopy class (braid relations, conjugation,
stabilization and destabilization: the moves of Markov's theorem). X changes one crossing.

  X p        crossing change: w[p] -> -w[p]                                              (counted)
  I p a      insert the two letters a, -a before position p (1 <= |a| <= n - 1)
  D p        delete w[p] and w[p+1] when w[p+1] = -w[p]
  C p        swap w[p] and w[p+1] when their indices differ by at least 2
  B p        w[p] w[p+1] w[p+2] = a b a -> b a b, when a and b have the same sign and indices differing by 1
  R k        conjugation: move the first k letters to the end (0 <= k <= len(w))
  F          conjugation by the half twist: every letter +-i becomes +-(n - i)
  S e        stabilization: append e * n (e = 1 or -1); n -> n + 1
  U          destabilization: the last letter is +-(n - 1) and no other letter has index n - 1; drop it; n -> n - 1

The certificate is valid when every move is allowed and the final braid is the empty word on one strand, whose closure
is the unknot. Its value is the number of crossing changes (X lines): an upper bound on the unknotting number of the
knot, since crossing changes made between isotopies can all be made at once in a single diagram of the knot.
The output ends with 'RESULT k'; the exit status is 0 only for a valid certificate."""
import sys


def fail(msg):
    print("NOT CERTIFIED: " + msg)
    sys.exit(1)


def parse_braid(text):
    text = text.strip().strip("[]").strip()
    if not text:
        fail("the braid word is empty")
    try:
        w = [int(x) for x in text.replace(" ", "").split(",")]
    except ValueError:
        fail("the braid word is not a list of integers")
    if any(x == 0 for x in w):
        fail("the braid word has a letter 0")
    return w


def closure_components(w, n):
    """The number of components of the closure of the braid w on n strands (cycles of its permutation)."""
    perm = list(range(n))
    for x in w:
        i = abs(x) - 1
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
    seen, cycles = [False] * n, 0
    for s in range(n):
        if not seen[s]:
            cycles += 1
            j = s
            while not seen[j]:
                seen[j] = True
                j = perm[j]
    return cycles


def integer(tok, line_no):
    try:
        return int(tok)
    except ValueError:
        fail(f"line {line_no}: '{tok}' is not an integer")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    w = parse_braid(sys.argv[1])
    n = max(abs(x) for x in w) + 1
    if closure_components(w, n) != 1:
        fail(f"the closure of the braid on {n} strands is not a knot")
    start_len, start_n = len(w), n
    changes = moves = 0
    try:
        lines = open(sys.argv[2]).read().splitlines()
    except (OSError, UnicodeDecodeError) as e:
        fail(f"cannot read the certificate: {e}")
    for line_no, raw in enumerate(lines, 1):
        tok = raw.split("#", 1)[0].split()
        if not tok:
            continue
        op, args = tok[0], [integer(t, line_no) for t in tok[1:]]
        need = {"X": 1, "I": 2, "D": 1, "C": 1, "B": 1, "R": 1, "F": 0, "S": 1, "U": 0}
        if op not in need:
            fail(f"line {line_no}: unknown move '{op}'")
        if len(args) != need[op]:
            fail(f"line {line_no}: move {op} takes {need[op]} number(s)")
        L = len(w)
        if op in ("X", "D", "C", "B"):
            p = args[0]
            width = {"X": 1, "D": 2, "C": 2, "B": 3}[op]
            if not 0 <= p <= L - width:
                fail(f"line {line_no}: position {p} out of range for {op} on a word of length {L}")
        if op == "X":
            w[p] = -w[p]
            changes += 1
        elif op == "I":
            p, a = args
            if not 0 <= p <= L:
                fail(f"line {line_no}: position {p} out of range for I on a word of length {L}")
            if not 1 <= abs(a) <= n - 1:
                fail(f"line {line_no}: letter {a} is not a generator of the braid group on {n} strands")
            w[p:p] = [a, -a]
        elif op == "D":
            if w[p + 1] != -w[p]:
                fail(f"line {line_no}: letters {w[p]}, {w[p + 1]} at {p} do not cancel")
            del w[p:p + 2]
        elif op == "C":
            if abs(abs(w[p]) - abs(w[p + 1])) < 2:
                fail(f"line {line_no}: letters {w[p]}, {w[p + 1]} at {p} do not commute")
            w[p], w[p + 1] = w[p + 1], w[p]
        elif op == "B":
            a, b, c = w[p:p + 3]
            if not (a == c and abs(abs(a) - abs(b)) == 1 and (a > 0) == (b > 0)):
                fail(f"line {line_no}: letters {a}, {b}, {c} at {p} are not a b a with a, b adjacent and of one sign")
            w[p:p + 3] = [b, a, b]
        elif op == "R":
            k = args[0]
            if not 0 <= k <= L:
                fail(f"line {line_no}: cannot move {k} letters of a word of length {L}")
            w = w[k:] + w[:k]
        elif op == "F":
            w = [(n - abs(x)) * (1 if x > 0 else -1) for x in w]
        elif op == "S":
            e = args[0]
            if e not in (1, -1):
                fail(f"line {line_no}: stabilization takes 1 or -1, not {e}")
            w.append(e * n)
            n += 1
        elif op == "U":
            if n < 2 or not w or abs(w[-1]) != n - 1 or any(abs(x) == n - 1 for x in w[:-1]):
                fail(f"line {line_no}: the last letter is not the only letter of index {n - 1}")
            w.pop()
            n -= 1
        moves += 1
    if w or n != 1:
        fail(f"after {moves} moves the braid is not the empty word on one strand ({n} strands, word "
             f"{','.join(map(str, w[:40]))}{'...' if len(w) > 40 else ''})")
    print(f"braid of length {start_len} on {start_n} strands, closure a knot")
    print(f"{moves} moves; the final braid is the empty word on one strand: its closure is the unknot")
    print(f"crossing changes {changes}: the unknotting number is at most {changes}")
    print(f"RESULT {changes}")


if __name__ == "__main__":
    main()
