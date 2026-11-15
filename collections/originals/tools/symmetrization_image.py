"""Certificates for the problem symmetrization-image (standard library only).

  python3 -I tools/symmetrization_image.py FMAX OUTDIR     (run from collections/originals)

Enumerates every almost symmetric numerical semigroup S with Frobenius number F <= FMAX, pair by pair: for
x = 1, 2, ... the pair {x, F - x} is decided (x in S, F - x in S, or both pseudo-Frobenius numbers), and closure
under addition and the pseudo-Frobenius condition are tested on every new element (description (b) of almost
symmetric semigroups: every gap x has F - x in S or x and F - x both pseudo-Frobenius). For each S it forms Phi(S),
the lattice path of S with the letters at its pseudo-Frobenius numbers below F deleted, a symmetric numerical set
with Frobenius number G = F - t + 1. For every odd G it keeps, for each image, the preimage with the smallest F, and
writes OUTDIR/G.txt: one line per image, the minimal generators of that preimage. The image is complete for
2G - 3 <= FMAX (a bound of ours: for G >= 3 every image has a preimage with F <= 2G - 5, or F = G when the
image is its own preimage); for larger G it is a lower bound.
The certificate is checked by checkers/orig_numth.py symmetrization-image G FILE, which shares no code with this."""
import os
import sys


def as_semigroups(F):
    """(A, P) bitmasks over 0..F of every almost symmetric numerical semigroup with Frobenius number F:
    A the elements in 1..F-1, P the pseudo-Frobenius numbers below F."""
    out = []
    bitF = 1 << F

    def ok(Am, Pm, Bm, newA, newP, newNon):
        AP = Am | Pm
        nonA = Bm | Pm | bitF
        for a in newA:
            if (AP << a) & nonA:
                return False
        for y in newP:
            if (Am << y) & nonA:
                return False
        for z in newNon:
            m = Am
            while m:
                low = m & -m
                a = low.bit_length() - 1
                m ^= low
                if a >= z:
                    break
                if (AP >> (z - a)) & 1:
                    return False
        return True

    def rec(x, Am, Bm, Pm):
        y = F - x
        if x > y:
            out.append((Am, Pm))
            return
        if x == y:
            P2 = Pm | (1 << x)
            if ok(Am, P2, Bm, [], [x], [x]):
                rec(x + 1, Am, Bm, P2)
            return
        bx, by = 1 << x, 1 << y
        if ok(Am | bx, Pm, Bm | by, [x], [], [y]):
            rec(x + 1, Am | bx, Bm | by, Pm)
        if ok(Am | by, Pm, Bm | bx, [y], [], [x]):
            rec(x + 1, Am | by, Bm | bx, Pm)
        P2 = Pm | bx | by
        if ok(Am, P2, Bm, [], [x, y], [x, y]):
            rec(x + 1, Am, Bm, P2)

    rec(1, 0, 0, 0)
    return out


def image_word(F, Am, Pm):
    return "".join("E" if (v == 0 or (Am >> v) & 1) else "N" for v in range(F + 1) if not (Pm >> v) & 1)


def minimal_generators(F, Am):
    """the positive elements that are not a sum of two positive elements; all lie in [m, F + m]."""
    m = next(v for v in range(1, F + 2) if v == F + 1 or (Am >> v) & 1)
    inS = [v == 0 or v > F or bool((Am >> v) & 1) for v in range(F + m + 1)]
    return [v for v in range(1, F + m + 1) if inS[v] and not any(inS[a] and inS[v - a] for a in range(1, v))]


def main():
    fmax, outdir = int(sys.argv[1]), sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    best = {}                                        # G -> {word: (F, generators)}
    for F in range(1, fmax + 1):
        for Am, Pm in as_semigroups(F):
            w = image_word(F, Am, Pm)
            G = len(w) - 1
            d = best.setdefault(G, {})
            if w not in d:
                d[w] = (F, minimal_generators(F, Am))
        print(f"F = {F} done", flush=True)
    for G in sorted(best):
        if G % 2 == 0:
            continue
        rows = sorted(best[G].items())
        complete = G <= 1 or 2 * G - 3 <= fmax
        with open(os.path.join(outdir, f"{G}.txt"), "w") as f:
            f.write(f"# symmetrization-image G = {G}: {len(rows)} symmetric numerical sets with Frobenius number {G} in the image"
                    f" of Phi, one preimage each (minimal generators; preimages with F <= {fmax}"
                    f"{', complete' if complete else ', a lower bound'})\n")
            for w, (F, gens) in rows:
                f.write(" ".join(map(str, gens)) + "\n")
        print(f"G = {G}: {len(rows)} images{' (complete)' if complete else ''}, largest F of a chosen preimage "
              f"{max(F for F, _ in best[G].values())}")


if __name__ == "__main__":
    main()
