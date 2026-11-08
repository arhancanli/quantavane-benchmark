"""Exact check of a snake or a coil in the hypercube Q_D (standard library only).

  python3 -I snake_check.py snake|coil D FILE

FILE holds the transition sequence: the coordinates (0 to D-1, one base-36 character each: 0-9 then a-z) that change
along the edges in order, starting from the vertex 0 (whitespace ignored; the format of Leaps in Bounds). A snake is
an induced path (two of its vertices are adjacent in Q_D only when consecutive) and a coil an induced cycle, whose
transitions lead back to 0. The length is the number of edges. For every vertex the checker looks up its D
neighbours among the vertices of the path. Prints the length and "RESULT L"; exits 0 when valid, 1 otherwise."""
import sys

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("snake", "coil"):
        print(__doc__)
        return 2
    coil, d = sys.argv[1] == "coil", int(sys.argv[2])
    if not 1 <= d <= 36:
        print("D must be 1..36")
        return 2
    text = "".join("\n".join(line.split("#")[0] for line in open(sys.argv[3], encoding="ascii", errors="replace")).split()).lower()
    if not text or any(c not in DIGITS[:d] for c in text):
        print(f"the transitions must be base-36 digits below {d}")
        return 1
    verts = [0]
    for c in text:
        verts.append(verts[-1] ^ (1 << DIGITS.index(c)))
    length = len(text)
    if coil:
        if verts[-1] != 0:
            print("the transitions of a coil must lead back to the vertex 0")
            return 1
        if length < 4:
            print("a coil has at least 4 edges")
            return 1
        verts.pop()
    where = {}
    for i, v in enumerate(verts):
        if v in where:
            print(f"vertex {v:0{d}b} is visited twice (steps {where[v]} and {i})")
            return 1
        where[v] = i
    m = len(verts)
    for i, v in enumerate(verts):
        for b in range(d):
            j = where.get(v ^ (1 << b))
            if j is None:
                continue
            gap = abs(i - j)
            if gap == 1 or (coil and gap == m - 1):
                continue
            print(f"vertices {i} and {j} of the {'coil' if coil else 'snake'} are adjacent but not consecutive")
            return 1
    print(f"{'coil' if coil else 'snake'} in Q_{d}: {length} edges, induced")
    print(f"RESULT {length}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
