"""Low-weight codewords of the binary code spanned by a graph's adjacency matrix (our own code, Quantavane Originals).

  python3 -I lowweight.py EDGES SECONDS SEED OUT.txt

The code is the row space over GF(2) of the adjacency matrix. Randomized information-set search (Lee-Brickell): put
the generator matrix in systematic form on a random set of columns and try every row and every sum of two rows,
keeping the lightest nonzero codeword. Writes its support (positions of the ones), one per line."""
import random
import sys
import time


def main():
    path, secs, seed, out = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    f = open(path)
    n, m = map(int, f.readline().split())
    rows = [0] * n
    for line in f:
        a, b = map(int, line.split())
        rows[a] |= 1 << b
        rows[b] |= 1 << a
    rng = random.Random(seed)
    best = min(rows, key=lambda r: bin(r).count("1"))
    t0 = time.time()
    while time.time() - t0 < secs:
        perm = list(range(n))
        rng.shuffle(perm)
        basis = []          # (pivot column, row) in systematic form over the permuted columns
        for r in rows:
            for c, b in basis:
                if r >> c & 1:
                    r ^= b
            if r:
                c = next(c for c in perm if r >> c & 1)
                basis = [(c2, b2 ^ r if b2 >> c & 1 else b2) for c2, b2 in basis]
                basis.append((c, r))
        bs = [b for _, b in basis]
        for i, x in enumerate(bs):
            if bin(x).count("1") < bin(best).count("1"):
                best = x
            for y in bs[i + 1:]:
                z = x ^ y
                if z and bin(z).count("1") < bin(best).count("1"):
                    best = z
    with open(out, "w") as fh:
        fh.write(f"# nonzero codeword of weight {bin(best).count('1')} (support: positions of the ones)\n")
        fh.write("".join(f"{i}\n" for i in range(n) if best >> i & 1))
    print(bin(best).count("1"))


if __name__ == "__main__":
    main()
