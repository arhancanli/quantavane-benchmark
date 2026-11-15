"""Exact check of a Golomb ruler (standard library only).

  python3 -I golomb_check.py M FILE

FILE holds the M marks, distinct integers separated by whitespace or commas (the format of Leaps in Bounds). A Golomb
ruler has all M(M-1)/2 differences between its marks distinct. The ruler is moved to start at 0; its length is the
largest mark. A ruler of length L shows G(M) <= L. Above 3,000 marks the differences are marked in a bit array of L + 1
bits by the C helper golomb_scan.c (built with cc -O3 on first use). Prints the length and "RESULT L"; exits 0 for a
valid ruler, 1 otherwise."""
import sys


NATIVE_FROM = 3000          # above this many marks the differences are marked in C (golomb_scan.c, a bit array)


def check_native(marks):
    import os
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", "golomb_scan"), os.path.join(here, "golomb_scan.c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    out = subprocess.run([exe], input=f"{len(marks)}\n" + " ".join(map(str, marks)) + "\n", capture_output=True,
                         text=True, check=True).stdout.split()
    m = len(marks)
    if out[0] == "repeat":
        d, i, j = int(out[1]), int(out[2]), int(out[3])
        print(f"the difference {d} occurs twice (once between marks {marks[i - 1]} and {marks[j - 1]})")
        return 1
    assert int(out[1]) == m * (m - 1) // 2, "golomb_scan: wrong number of differences"
    print(f"marks {m} length {marks[-1]}: all {out[1]} differences distinct (marked in C)")
    print(f"RESULT {marks[-1]}")
    return 0


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
    if m > NATIVE_FROM:
        return check_native(marks)
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
