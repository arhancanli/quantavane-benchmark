"""Exact check of a Golomb ruler (standard library only).

  python3 -I golomb_check.py M FILE

FILE holds the M marks, distinct integers separated by whitespace or commas (the format of Leaps in Bounds). A Golomb
ruler has all M(M-1)/2 differences between its marks distinct. The ruler is moved to start at 0; its length is the
largest mark. A ruler of length L shows G(M) <= L. Prints the length and "RESULT L"; exits 0 for a valid ruler, 1
otherwise."""
import sys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    m = int(sys.argv[1])
    try:
        marks = sorted(int(x) for x in "\n".join(line.split("#")[0] for line in open(sys.argv[2], encoding="ascii", errors="replace")).replace(",", " ").split())
    except ValueError:
        print("the marks must be integers")
        return 1
    if len(marks) != m or len(set(marks)) != m:
        print(f"{len(marks)} marks ({len(set(marks))} distinct), expected {m} distinct marks")
        return 1
    marks = [x - marks[0] for x in marks]
    seen = {}
    for i in range(m):
        for j in range(i + 1, m):
            d = marks[j] - marks[i]
            if d in seen:
                print(f"the difference {d} occurs twice: {seen[d]} and {(marks[i], marks[j])}")
                return 1
            seen[d] = (marks[i], marks[j])
    print(f"marks {m} length {marks[-1]}: all {len(seen)} differences distinct")
    print(f"RESULT {marks[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
