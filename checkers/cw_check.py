"""Exact check of a binary constant weight code (standard library only).

  python3 -I cw_check.py N D W FILE

FILE has one code word per line, given by the W positions of its ones: W distinct integers from 1..N separated by
spaces. Two words of weight W are at Hamming distance 2(W - c), where c is the number of positions they share, so
the distance is at least D exactly when no two words share S = W - ceil(D/2) + 1 positions. The check lists every
S-subset of every word and fails on the first one seen twice; this decides the same thing as comparing all pairs.
Prints "words M" and exits 0 when the code is valid, exits 1 otherwise."""
import itertools
import sys


def main():
    n, d, w = (int(x) for x in sys.argv[1:4])
    words = []
    for line in open(sys.argv[4]):
        line = line.split("#")[0].strip()
        if line:
            words.append(sorted(int(x) for x in line.split()))
    for x in words:
        if len(x) != w or len(set(x)) != w or not all(1 <= p <= n for p in x):
            print(f"invalid word {x}: need {w} distinct positions from 1..{n}")
            return 1
    s = w - (d + 1) // 2 + 1
    if s <= 0 and len(words) > 1:
        print(f"two words of weight {w} differ in at most {2 * w} < {d} positions")
        return 1
    seen = {}
    for i, x in enumerate(words):
        for sub in itertools.combinations(x, max(s, 0)):
            if sub in seen:
                print(f"words {seen[sub] + 1} and {i + 1} share the positions {list(sub)}: distance below {d}")
                return 1
            seen[sub] = i
    print(f"every word has weight {w}; any two differ in at least {d} positions ({len(seen)} {s}-subsets, all distinct)")
    print(f"words {len(words)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
