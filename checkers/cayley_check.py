"""Exact check of a Cayley graph for the degree-diameter problem (standard library only; C helpers for large
groups).

  python3 -I cayley_check.py DEGREE DIAMETER FILE [--python | --native]

FILE gives a group G and a generating set S in one of two forms ('#' starts a comment):

- Permutations: a first line "points m", then one permutation per line, the images of 0, 1, ..., m - 1.
- A semidirect product of cyclic groups: a first line "semidirect m n a", the group Z_m x|_a Z_n of the pairs
  [x, y] (0 <= x < m, 0 <= y < n) with [x, y][u, v] = [x + u mod m, y a^u + v mod n], the convention of the
  Combinatorics Wiki's and F. Comellas's tables (after M. J. Dinneen and P. Hafner); a must be a unit mod n with
  a^m = 1 mod n (otherwise the product is not a group). Then one generator per line, "x y". Most record Cayley graphs
  of the table are of this kind, and this form needs one byte per element where permutations would need gigabytes.

S must not contain the identity, its elements must be distinct, and S must be closed under inverses (an involution
counts once); |S| <= DEGREE. The Cayley graph Cay(G, S) has the elements of <S> as vertices and g ~ g s for s in S:
it is |S|-regular and vertex-transitive, so its diameter is the eccentricity of the identity. The checker builds <S>
by breadth-first search from the identity (every element multiplied by every generator; in C above 10^5 elements:
cayley_bfs.c for permutations, elements kept in a hash table, and cayley_sdp.c for semidirect products, a byte of
distance per element), which gives both the order |<S>| and the diameter, and requires the diameter to be at most
DIAMETER. Prints the order, the degree and the diameter, and "RESULT |<S>|" (larger is better); exits 0 for a valid
graph, 1 otherwise."""
import math
import os
import subprocess
import sys

NATIVE_FROM = 10 ** 5
MAX_ORDER = 2 * 10 ** 8          # permutations: the hash table keeps every element
MAX_SDP = 5 * 10 ** 8            # semidirect products: m n bytes


def helper(name):
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", name), os.path.join(here, name + ".c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    return exe


def bfs_python(m, gens, limit):
    ident = tuple(range(m))
    dist = {ident: 0}
    frontier, d = [ident], 0
    while frontier:
        nxt = []
        for g in frontier:
            for s in gens:
                h = tuple(s[x] for x in g)          # g then s
                if h not in dist:
                    dist[h] = d + 1
                    nxt.append(h)
        if nxt:
            d += 1
        frontier = nxt
        if len(dist) > limit:
            return None, None
    return len(dist), d


def sdp_mul(g, h, m, n, a):
    return ((g[0] + h[0]) % m, (g[1] * pow(a, h[0], n) + h[1]) % n)


def sdp_inv(g, m, n, a):
    """[x, y]^-1 = [-x, -y a^(-x)]"""
    u = (-g[0]) % m
    return (u, (-g[1] * pow(a, u, n)) % n)


def bfs_sdp_python(m, n, a, gens, limit):
    dist = {(0, 0): 0}
    frontier, d = [(0, 0)], 0
    while frontier:
        nxt = []
        for g in frontier:
            for s in gens:
                h = sdp_mul(g, s, m, n, a)
                if h not in dist:
                    dist[h] = d + 1
                    nxt.append(h)
        if nxt:
            d += 1
        frontier = nxt
        if len(dist) > limit:
            return None, None
    return len(dist), d


def read_file(path):
    """(kind, header, generators) or an error text"""
    head, gens = None, []
    for ln, line in enumerate(open(path, encoding="ascii", errors="replace"), 1):
        tok = line.split("#")[0].replace(",", " ").split()
        if not tok:
            continue
        if head is None:
            if tok[0] == "points" and len(tok) == 2 and tok[1].isdigit() and int(tok[1]) >= 1:
                head = ("points", int(tok[1]))
            elif tok[0] == "semidirect" and len(tok) == 4 and all(t.isdigit() for t in tok[1:]) \
                    and int(tok[1]) >= 1 and int(tok[2]) >= 1:
                head = ("semidirect", int(tok[1]), int(tok[2]), int(tok[3]))
            else:
                return f"line {ln}: the first line must be 'points m' or 'semidirect m n a'"
            continue
        if not all(t.isdigit() for t in tok):
            return f"line {ln}: a generator is a list of non-negative integers"
        g = tuple(int(x) for x in tok)
        if head[0] == "points":
            m = head[1]
            if len(g) != m or sorted(g) != list(range(m)):
                return f"line {ln}: not a permutation of 0..{m - 1}"
        else:
            m, n = head[1], head[2]
            if len(g) != 2 or not (g[0] < m and g[1] < n):
                return f"line {ln}: a generator of Z_{m} x| Z_{n} is a pair x y with 0 <= x < {m}, 0 <= y < {n}"
        gens.append(g)
    if head is None or not gens:
        return "no generators"
    return head, gens


def main():
    flags = [a for a in sys.argv[1:] if a in ("--python", "--native")]
    args = [a for a in sys.argv[1:] if a not in flags]
    if len(args) != 3:
        print(__doc__)
        return 2
    degree, diameter = int(args[0]), int(args[1])
    got = read_file(args[2])
    if isinstance(got, str):
        print(got)
        return 1
    head, gens = got
    if len(set(gens)) != len(gens):
        print("a generator is repeated")
        return 1
    S = set(gens)
    if head[0] == "points":
        m = head[1]
        if tuple(range(m)) in S:
            print("the identity is not allowed in S")
            return 1
        for g in gens:
            inv = [0] * m
            for i, x in enumerate(g):
                inv[x] = i
            if tuple(inv) not in S:
                print("S is not closed under inverses")
                return 1
    else:
        _, m, n, a = head
        if n == 1:
            a = 0
        if a >= n:
            print(f"a = {a} must be below n = {n}")
            return 1
        if math.gcd(a, n) != 1 or pow(a, m, n) != 1 % n:
            print(f"Z_{m} x|_{a} Z_{n} is not a group: a must be a unit mod n with a^m = 1 mod n")
            return 1
        if (0, 0) in S:
            print("the identity is not allowed in S")
            return 1
        if any(sdp_inv(g, m, n, a) not in S for g in gens):
            print("S is not closed under inverses")
            return 1
        if m * n > MAX_SDP:
            print(f"the group has more than {MAX_SDP} elements")
            return 1
    if len(gens) > degree:
        print(f"{len(gens)} generators: the degree is above {degree}")
        return 1
    if head[0] == "points":
        native = "--native" in flags or ("--python" not in flags and not small_group(m, gens))
        if native:
            text = f"{m} {len(gens)} {MAX_ORDER}\n" + "".join(" ".join(map(str, g)) + "\n" for g in gens)
            res = run_helper("cayley_bfs", text)
        else:
            res = bfs_python(m, gens, MAX_ORDER)
    else:
        native = "--native" in flags or ("--python" not in flags and m * n > NATIVE_FROM)
        if native:
            text = f"{m} {n} {a} {len(gens)} {MAX_SDP}\n" + "".join(f"{x} {y}\n" for x, y in gens)
            res = run_helper("cayley_sdp", text)
        else:
            res = bfs_sdp_python(m, n, a, gens, MAX_SDP)
    if isinstance(res, str):
        print(res)
        return 1
    order, diam = res
    if order is None:
        print("the group has more elements than the checker keeps")
        return 1
    print(f"Cayley graph of order {order}, degree {len(gens)}, diameter {diam}")
    if diam > diameter:
        print(f"the diameter {diam} is above {diameter}")
        return 1
    print(f"RESULT {order}")
    return 0


def run_helper(name, text):
    r = subprocess.run([helper(name)], input=text, capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or [f"FAIL no output from {name}"])[-1]
    if r.returncode or not last.startswith("OK "):
        return last[5:] if last.startswith("FAIL ") else last
    return int(last.split()[1]), int(last.split()[2])


def small_group(m, gens):
    """True when breadth-first search in Python stays below NATIVE_FROM elements (stopped early otherwise)."""
    return bfs_python(m, gens, NATIVE_FROM)[0] is not None


if __name__ == "__main__":
    sys.exit(main())
