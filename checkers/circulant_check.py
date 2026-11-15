"""Exact check of a circulant graph for the degree-diameter problem (standard library only).

  python3 -I circulant_check.py DELTA DIAMETER FILE

FILE gives the circulant graph C_n(S): the order n on the first line, then the jumps s (integers, any number per line,
'#' starts a comment). Vertices are 0..n-1 and x is joined to x + s and x - s modulo n for every jump s. The jumps
must be nonzero modulo n and give distinct edges: no jump may repeat another or its negative. The degree is the number
of distinct values +-s modulo n (s = n/2 counts once) and must be at most DELTA. A circulant graph is
vertex-transitive (x -> x + 1 is an automorphism), so its diameter is the eccentricity of vertex 0, found by
breadth-first search; it must be at most DIAMETER. Above 10^6 vertices the search runs in the C helper
circulant_bfs.c (built with cc -O3 on first use); --native or --python forces one way. Prints the order and
"RESULT n"; exits 0 for a valid graph, 1 otherwise."""
import os
import subprocess
import sys

NATIVE_FROM = 10 ** 6


def ecc_python(n, steps, limit):
    """The eccentricity of 0 in the Cayley graph of Z_n with these steps, or -1 if some vertex is farther than
    limit."""
    seen = bytearray(n)
    seen[0] = 1
    frontier, reached, r = [0], 1, 0
    while reached < n:
        if r == limit:
            return -1
        nxt = []
        for x in frontier:
            for s in steps:
                y = x + s
                if y >= n:
                    y -= n
                if not seen[y]:
                    seen[y] = 1
                    nxt.append(y)
        if not nxt:
            return -1
        reached += len(nxt)
        frontier = nxt
        r += 1
    return r


def ecc_native(n, steps, limit):
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", "circulant_bfs"), os.path.join(here, "circulant_bfs.c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    out = subprocess.run([exe, str(n), str(limit)], input=" ".join(map(str, steps)) + "\n", capture_output=True,
                         text=True, check=True).stdout.split()
    assert out[0] == "ecc", "circulant_bfs: output"
    return int(out[1])


def main():
    flags = [a for a in sys.argv[1:] if a in ("--native", "--python")]
    args = [a for a in sys.argv[1:] if a not in flags]
    if len(args) != 3:
        print(__doc__)
        return 2
    delta, diam = int(args[0]), int(args[1])
    nums = []
    for line in open(args[2]):
        line = line.split("#")[0].replace(",", " ").strip()
        try:
            nums += [int(x) for x in line.split()]
        except ValueError:
            print(f"not a list of integers: {line[:80]!r}")
            return 1
    if not nums or nums[0] < 2:
        print("the first number must be the order n >= 2")
        return 1
    n, jumps = nums[0], nums[1:]
    steps = set()
    for s in jumps:
        a = s % n
        if a == 0:
            print(f"jump {s} is 0 modulo {n}")
            return 1
        pair = {a, (n - a) % n}
        if pair & steps:
            print(f"jump {s} repeats an edge of an earlier jump")
            return 1
        steps |= pair
    print(f"circulant graph on {n} vertices, {len(jumps)} jumps, degree {len(steps)}")
    if len(steps) > delta:
        print(f"degree {len(steps)} > {delta}")
        return 1
    native = "--native" in flags or ("--python" not in flags and n > NATIVE_FROM)
    e = (ecc_native if native else ecc_python)(n, sorted(steps), diam)
    if e < 0:
        print(f"some vertex is farther than {diam} from vertex 0 (or the graph is disconnected)")
        return 1
    print(f"diameter {e} <= {diam}" + (" (searched in C)" if native else ""))
    print(f"RESULT {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
