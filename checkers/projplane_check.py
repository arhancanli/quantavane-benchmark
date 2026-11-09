"""Exact check of a finite projective plane of order N (standard library only).

  python3 -I projplane_check.py N FILE

FILE holds the lines of the plane, one per text line: N + 1 point labels separated by spaces or commas, with the
points numbered 0..N^2+N or 1..N^2+N+1. A projective plane of order N has N^2+N+1 points and N^2+N+1 lines, each line
holding N+1 points, and every two points lie on exactly one line (then every two lines meet in exactly one point).
The checker marks every pair of points on every line and refuses a pair met twice; since the plane has exactly
(N^2+N+1) N(N+1)/2 = C(N^2+N+1, 2) such pairs, no repetition means that every pair is covered exactly once. Prints the
order and "RESULT 1" (a projective plane of order N exists); exits 0 for a valid plane, 1 otherwise."""
import sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    q = int(sys.argv[1])
    v = q * q + q + 1
    lines = []
    for text in open(sys.argv[2], encoding="ascii", errors="replace"):
        s = text.split("#")[0].replace(",", " ").split()
        if not s:
            continue
        try:
            lines.append([int(x) for x in s])
        except ValueError:
            print(f"not a line of integers: {text.strip()[:60]!r}")
            return 1
    if len(lines) != v:
        print(f"{len(lines)} lines, expected {v}")
        return 1
    labels = {x for ln in lines for x in ln}
    if labels == set(range(1, v + 1)):
        lines = [[x - 1 for x in ln] for ln in lines]
    elif labels != set(range(v)):
        print(f"the points must be numbered 0..{v - 1} or 1..{v}, each used at least once")
        return 1
    seen = bytearray(v * v)
    for idx, ln in enumerate(lines):
        if len(ln) != q + 1 or len(set(ln)) != q + 1:
            print(f"line {idx + 1} does not hold {q + 1} distinct points")
            return 1
        for a in range(q + 1):
            for b in range(a + 1, q + 1):
                x, y = ln[a], ln[b]
                if x > y:
                    x, y = y, x
                if seen[x * v + y]:
                    print(f"points {x} and {y} lie on two lines (line {idx + 1} and an earlier one)")
                    return 1
                seen[x * v + y] = 1
    print(f"order {q}: {v} points, {v} lines of {q + 1} points, every pair of points on exactly one line")
    print("RESULT 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
