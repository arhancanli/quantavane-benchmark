"""Exact checkers for the biology problems of the Quantavane Originals (standard library only).

  python3 -I orig_bio.py PROBLEM ARGS... FILE

Each check prints what it verified and ends with a line "RESULT v" (the exact value proved); it exits 0 only for a
valid certificate and 1 otherwise. Problems:

  nussinov-degeneracy N FILE   FILE: an RNA sequence of length N over A, C, G, U (whitespace and lines starting with
                               # ignored). Model (base-pair maximization, Nussinov): allowed pairs AU, UA, GC, CG, GU,
                               UG; a pair (i, j) needs j - i >= 4 (a hairpin loop of at least 3 bases); a secondary
                               structure is a set of pairs, each base in at most one pair, with no two pairs crossing
                               (i < k < j < l). Value: the number of structures with the largest possible number of
                               pairs, computed exactly by dynamic programming over intervals that splits on the
                               partner of the first base (each structure counted once).
  hp-tri N FILE                FILE: N lattice sites "a b" (one per line), the conformation of the HP chain of
                               length N given by the Fibonacci word (S_1 = P, S_2 = H, S_k = S_(k-1) S_(k-2); N a
                               Fibonacci number) on the triangular lattice (site a + b e^(i pi/3)). Valid when the
                               sites are distinct and consecutive sites are lattice neighbours (differences (1,0),
                               (0,1), (-1,1), (-1,0), (0,-1), (1,-1)). Value: the energy, minus the number of pairs of
                               H monomers on neighbouring sites that are not consecutive in the chain.
  align-ambiguity N FILE       FILE: two lines, DNA sequences x and y of length N over A, C, G, T. Value: the number
                               of optimal global alignments of x and y with unit costs (mismatch 1, gap 1, match 0):
                               paths in the edit graph from (0, 0) to (N, N) with diagonal, horizontal and vertical
                               steps and the least total cost, counted exactly by dynamic programming.
  six-frame FILE               FILE: a DNA sequence over A, C, G, T (line breaks and lines starting with # ignored).
                               Its six reading frames: the forward frames starting at the first, second and third
                               base, and the same three frames of the reverse complement, each read as consecutive
                               codons (an incomplete codon at the end is ignored) with the standard genetic code.
                               Valid when no frame contains a stop codon (TAA, TAG, TGA) and every frame contains all
                               20 amino acids. Value: the length of the sequence."""
import sys

PAIRS = {("A", "U"), ("U", "A"), ("G", "C"), ("C", "G"), ("G", "U"), ("U", "G")}


def sequence(path, n):
    text = "".join(line.split("#")[0] for line in open(path, encoding="ascii", errors="replace"))
    s = "".join(text.split()).upper()
    if len(s) != n or set(s) - set("ACGU"):
        raise ValueError(f"expected an RNA sequence of length {n} over A, C, G, U")
    return s


def nussinov_count(s):
    n = len(s)
    best = [[0] * (n + 1) for _ in range(n + 2)]
    cnt = [[1] * (n + 1) for _ in range(n + 2)]
    for length in range(1, n + 1):
        for i in range(0, n - length + 1):
            e = i + length                 # interval [i, e)
            b, c = best[i + 1][e], cnt[i + 1][e]
            for k in range(i + 4, e):
                if (s[i], s[k]) in PAIRS:
                    v = 1 + best[i + 1][k] + best[k + 1][e]
                    w = cnt[i + 1][k] * cnt[k + 1][e]
                    if v > b:
                        b, c = v, w
                    elif v == b:
                        c += w
            best[i][e], cnt[i][e] = b, c
    return best[0][n], cnt[0][n]


def nussinov_degeneracy(args, path):
    n = int(args[0])
    s = sequence(path, n)
    pairs, count = nussinov_count(s)
    print(f"{s}: at most {pairs} base pairs, {count} structures with {pairs} pairs")
    print(f"RESULT {count}")
    return 0


TRI = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]


def fib_word(n):
    a, b = "P", "H"
    while len(b) < n:
        a, b = b, b + a
    if len(b) != n:
        raise ValueError(f"{n} is not a Fibonacci number")
    return b


def hp_tri(args, path):
    n = int(args[0])
    seq = fib_word(n)
    pos = []
    for line in open(path, encoding="ascii", errors="replace"):
        line = line.split("#")[0].split()
        if line:
            pos.append((int(line[0]), int(line[1])))
    if len(pos) != n:
        print(f"{len(pos)} sites, expected {n}")
        return 1
    if len(set(pos)) != n:
        print("two monomers share a site")
        return 1
    for i in range(n - 1):
        if (pos[i + 1][0] - pos[i][0], pos[i + 1][1] - pos[i][1]) not in TRI:
            print(f"monomers {i} and {i + 1} are not on neighbouring sites")
            return 1
    where = {p: i for i, p in enumerate(pos)}
    contacts = 0
    for i, p in enumerate(pos):
        if seq[i] == "H":
            for dx, dy in TRI:
                j = where.get((p[0] + dx, p[1] + dy))
                if j is not None and j > i + 1 and seq[j] == "H":
                    contacts += 1
    print(f"Fibonacci HP chain {seq} on the triangular lattice: {contacts} H-H contacts, energy {-contacts}")
    print(f"RESULT {-contacts}")
    return 0


def align_ambiguity(args, path):
    n = int(args[0])
    seqs = [l.strip().upper() for l in open(path, encoding="ascii", errors="replace") if l.strip() and not l.startswith("#")]
    if len(seqs) != 2 or any(len(t) != n or set(t) - set("ACGT") for t in seqs):
        print(f"expected two DNA sequences of length {n}")
        return 1
    x, y = seqs
    INF = 10 ** 9
    D = [[INF] * (n + 1) for _ in range(n + 1)]
    C = [[0] * (n + 1) for _ in range(n + 1)]
    D[0][0], C[0][0] = 0, 1
    for i in range(n + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                continue
            cands = []
            if i and j:
                cands.append((D[i - 1][j - 1] + (x[i - 1] != y[j - 1]), C[i - 1][j - 1]))
            if i:
                cands.append((D[i - 1][j] + 1, C[i - 1][j]))
            if j:
                cands.append((D[i][j - 1] + 1, C[i][j - 1]))
            best = min(c for c, _ in cands)
            D[i][j] = best
            C[i][j] = sum(k for c, k in cands if c == best)
    print(f"{x} / {y}: edit distance {D[n][n]}, {C[n][n]} optimal alignments")
    print(f"RESULT {C[n][n]}")
    return 0


STANDARD_CODE = {}
for _aa, _codons in (("F", "TTT TTC"), ("L", "TTA TTG CTT CTC CTA CTG"), ("I", "ATT ATC ATA"), ("M", "ATG"),
                     ("V", "GTT GTC GTA GTG"), ("S", "TCT TCC TCA TCG AGT AGC"), ("P", "CCT CCC CCA CCG"),
                     ("T", "ACT ACC ACA ACG"), ("A", "GCT GCC GCA GCG"), ("Y", "TAT TAC"), ("*", "TAA TAG TGA"),
                     ("H", "CAT CAC"), ("Q", "CAA CAG"), ("N", "AAT AAC"), ("K", "AAA AAG"), ("D", "GAT GAC"),
                     ("E", "GAA GAG"), ("C", "TGT TGC"), ("W", "TGG"), ("R", "CGT CGC CGA CGG AGA AGG"),
                     ("G", "GGT GGC GGA GGG")):
    for _c in _codons.split():
        STANDARD_CODE[_c] = _aa


def six_frame(args, path):
    seq = "".join("".join(l.split()) for l in open(path, encoding="ascii", errors="replace") if not l.startswith("#")).upper()
    if not seq or set(seq) - set("ACGT"):
        print("the sequence must consist of the letters A, C, G, T")
        return 1
    rc = seq[::-1].translate(str.maketrans("ACGT", "TGCA"))
    for name, strand in (("forward", seq), ("reverse", rc)):
        for f in range(3):
            prot = "".join(STANDARD_CODE[strand[i:i + 3]] for i in range(f, len(strand) - 2, 3))
            if "*" in prot:
                print(f"{name} frame {f + 1} contains a stop codon")
                return 1
            missing = set("ACDEFGHIKLMNPQRSTVWY") - set(prot)
            if missing:
                print(f"{name} frame {f + 1} lacks {''.join(sorted(missing))}")
                return 1
    print(f"a sequence of {len(seq)} bases: all six frames are open and contain all 20 amino acids")
    print(f"RESULT {len(seq)}")
    return 0


PROBLEMS = {"align-ambiguity": (1, align_ambiguity), "six-frame": (0, six_frame), "nussinov-degeneracy": (1, nussinov_degeneracy), "hp-tri": (1, hp_tri)}


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
