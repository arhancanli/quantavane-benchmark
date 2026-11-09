"""Exact checkers for the computing and operations research problems of the Quantavane Originals (standard library).

  python3 -I orig_comp.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved); it exits 0 only for a
valid certificate and 1 otherwise. Problems:

  sync-quadratic P FILE   FILE: a word over the letters a and b (whitespace ignored). The automaton Q_P has states
                          0, ..., P-1 (P prime), the letter a maps x to x + 1 and b maps x to x^2 (mod P); a word is
                          applied letter by letter from the left. Valid when the word sends every state to the same
                          state (a reset word). Value: its length.
  tsp INSTANCE FILE (also tsp-sunflower)
                          INSTANCE: collections/originals/instances/sunflower-N.txt (N, then lines "k x y" with
                          integer coordinates). FILE: a tour, the point numbers 1..N in visiting order (one per line
                          or separated by spaces), each exactly once. Value: the tour length, the sum over consecutive
                          points (and back to the start) of the Euclidean distance rounded to the nearest integer
                          (computed exactly: round(sqrt(n)) is r or r + 1 with r = isqrt(n), r + 1 when
                          4n >= (2r + 1)^2).
  qr-xor P FILE           FILE: "P G", then G gates "a b" (signal numbers: 0..P-1 are the inputs x_0..x_(P-1), and
                          gate k, k = 1..G, is signal P+k-1 = (signal a) XOR (signal b), with a, b < P+k-1), then a
                          line of P signal numbers, the outputs. Valid when output i computes the XOR of the inputs
                          x_j with j - i a nonzero square modulo P (row i of the quadratic-residue circulant over
                          GF(2)). Value: G, the number of XOR gates."""
import math
import sys


def isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def sync_quadratic(args, path):
    p = int(args[0])
    if not isprime(p):
        print("P must be prime")
        return 1
    text = "".join(line.split("#")[0] for line in open(path, encoding="ascii", errors="replace"))
    w = "".join(text.split())
    if set(w) - set("ab"):
        print("the word must use only the letters a and b")
        return 1
    states = set(range(p))
    for c in w:
        states = {(x + 1) % p for x in states} if c == "a" else {x * x % p for x in states}
    if len(states) != 1:
        print(f"not a reset word: {len(states)} states remain")
        return 1
    print(f"reset word of length {len(w)} for Q_{p}: every state goes to {states.pop()}")
    print(f"RESULT {len(w)}")
    return 0


def nint_dist(a, b):
    n = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    r = math.isqrt(n)
    return r + 1 if 4 * n >= (2 * r + 1) ** 2 else r


def tsp_sunflower(args, path):
    pts = {}
    count = None
    for line in open(args[0], encoding="ascii"):
        line = line.split("#")[0].split()
        if len(line) == 1 and count is None:
            count = int(line[0])
        elif len(line) == 3:
            pts[int(line[0])] = (int(line[1]), int(line[2]))
    if count is None or len(pts) != count or set(pts) != set(range(1, count + 1)):
        print("unreadable instance")
        return 1
    toks = " ".join(line.split("#")[0] for line in open(path, encoding="ascii", errors="replace")).split()
    tour = [int(t) for t in toks]
    if sorted(tour) != list(range(1, count + 1)):
        print(f"not a tour: {len(tour)} entries, {len(set(tour))} distinct, expected each of 1..{count} once")
        return 1
    L = sum(nint_dist(pts[tour[i]], pts[tour[(i + 1) % count]]) for i in range(count))
    print(f"tour through all {count} points: length {L}")
    print(f"RESULT {L}")
    return 0


def qr_xor(args, path):
    p = int(args[0])
    if not isprime(p):
        print("P must be prime")
        return 1
    lines = [line.split("#")[0].split() for line in open(path, encoding="ascii", errors="replace")]
    lines = [l for l in lines if l]
    pp, g = int(lines[0][0]), int(lines[0][1])
    if pp != p or len(lines) != g + 2:
        print(f"expected 'P G', G gate lines and one output line (P = {p})")
        return 1
    form = [1 << j for j in range(p)]
    for k in range(g):
        a, b = (int(t) for t in lines[1 + k])
        if not (0 <= a < len(form) and 0 <= b < len(form)) or a == b:
            print(f"gate {k + 1} uses unknown or equal signals {a}, {b}")
            return 1
        form.append(form[a] ^ form[b])
    outs = [int(t) for t in lines[-1]]
    if len(outs) != p or any(not 0 <= o < len(form) for o in outs):
        print(f"expected {p} output signal numbers")
        return 1
    qr = {x * x % p for x in range(1, p)}
    for i, o in enumerate(outs):
        want = sum(1 << ((i + d) % p) for d in qr)
        if form[o] != want:
            print(f"output {i} (signal {o}) does not compute row {i} of the circulant")
            return 1
    print(f"XOR circuit with {g} gates computes the quadratic-residue circulant Q_{p} over GF(2)")
    print(f"RESULT {g}")
    return 0


PROBLEMS = {"sync-quadratic": (1, sync_quadratic), "tsp": (1, tsp_sunflower), "tsp-sunflower": (1, tsp_sunflower),
            "qr-xor": (1, qr_xor)}


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in PROBLEMS:
        print(__doc__)
        return 2
    nargs, fn = PROBLEMS[sys.argv[1]]
    if len(sys.argv) != 3 + nargs:
        print(__doc__)
        return 2
    try:
        return fn(sys.argv[2:-1], sys.argv[-1])
    except (ValueError, OSError) as e:
        print(f"unreadable certificate: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
