"""Exact check of an unrestricted (not necessarily linear) code with minimum distance at least D, over one alphabet or
a mix of alphabets (standard library only; a C compiler makes large codes faster).

  python3 -I ucode_check.py ALPHABETS D FILE

ALPHABETS gives the alphabet size of every coordinate, in order, as factors q^count joined by '.': "2^17" (17 binary
coordinates), "3^9", "2^1.3^6" (one binary coordinate, then six ternary ones). Sizes 2 to 8, at most 64 coordinates.
FILE holds the words, one per line: the symbols of the coordinates (integers below each coordinate's size), separated
by spaces or commas or written as one string of digits. Blank lines and lines starting with '#' are ignored.

The code is valid when every symbol is in its coordinate's alphabet and every two words differ in at least D
coordinates (so no word repeats). Every pair is compared: in this program up to 3,000 words, in the C helper
ucode_scan.c (built with cc -O3 on first use) above that. Prints "words M" and, as its last line, "RESULT M", and
exits 0 for a valid code; prints the reason and exits 1 otherwise."""
import os
import re
import subprocess
import sys


def parse_alphabets(spec):
    sizes = []
    for part in spec.split("."):
        m = re.fullmatch(r"([2-8])\^(\d+)", part)
        if not m:
            raise ValueError(f"bad alphabet part {part!r}")
        sizes += [int(m.group(1))] * int(m.group(2))
    if not 1 <= len(sizes) <= 64:
        raise ValueError("need 1 to 64 coordinates")
    return sizes


def read_words(path, sizes):
    L = len(sizes)
    words = []
    for no, line in enumerate(open(path), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        toks = s.replace(",", " ").split()
        if len(toks) != L and all(t.isdigit() for t in toks) and sum(len(t) for t in toks) == L:
            toks = list("".join(toks))
        if len(toks) != L or not all(t.isdigit() for t in toks):
            raise ValueError(f"line {no}: not {L} symbols")
        w = [int(t) for t in toks]
        for j, (x, q) in enumerate(zip(w, sizes)):
            if x >= q:
                raise ValueError(f"line {no}: symbol {x} at coordinate {j + 1} is not below {q}")
        words.append(w)
    if not words:
        raise ValueError("no words")
    return words


def closest_python(words, D):
    for i in range(len(words)):
        a = words[i]
        for j in range(i + 1, len(words)):
            d = sum(1 for x, y in zip(a, words[j]) if x != y)
            if d < D:
                return i + 1, j + 1, d
    return None


def closest_native(words, D):
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", "ucode_scan"), os.path.join(here, "ucode_scan.c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    text = f"{len(words)} {len(words[0])}\n" + "".join(" ".join(map(str, w)) + "\n" for w in words)
    out = subprocess.run([exe, str(D)], input=text, capture_output=True, text=True, check=True).stdout.split()
    if out[0] == "ok":
        assert int(out[1]) == len(words) * (len(words) - 1) // 2, "ucode_scan: wrong number of pairs"
        return None
    return int(out[1]), int(out[2]), int(out[3])


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    force = None
    for flag in ("--native", "--python"):
        if flag in argv:
            argv.remove(flag)
            force = flag
    if len(argv) != 3:
        print(__doc__)
        return 1
    try:
        sizes = parse_alphabets(argv[0])
        D = int(argv[1])
        if D < 1:
            raise ValueError("D must be at least 1")
        words = read_words(argv[2], sizes)
    except (ValueError, OSError) as err:
        print(f"malformed: {err}")
        return 1
    native = force == "--native" or (force is None and len(words) > 3000)
    bad = closest_native(words, D) if native else closest_python(words, D)
    if bad:
        i, j, d = bad
        print(f"words {i} and {j} differ in {d} coordinates, fewer than {D}")
        return 1
    print(f"{len(words)} words of length {len(sizes)}, every two at distance at least {D}"
          + (" (compared in C)" if native else ""))
    print(f"words {len(words)}")
    print(f"RESULT {len(words)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
