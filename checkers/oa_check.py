"""Exact strength check of an ordered orthogonal array given run by run (any array, linear or not): orthogonal
arrays (depth 1), ordered orthogonal arrays of depth 2 to 8, and nets (depth K), in base B (standard library only;
a C compiler makes large arrays faster).

  python3 -I oa_check.py B T M K FILE [--python | --native]

FILE holds the B^M runs, one per line: S * D symbols 0..B-1 (D = T, or D = K for T = net), factor after factor, the D
coordinates of a factor in order of depth (written separated by spaces or commas, or for B <= 10 as one string of
digits). Blank lines and lines starting with '#' are ignored. The symbols are just labels: any B-symbol alphabet.

The array has strength K when, for every choice of depths d_1 + ... + d_S = K with 0 <= d_i <= min(D, K), the runs'
symbols in the first d_i coordinates of each factor take each of the B^K possible values exactly B^(M-K) times. Every
such choice is checked (the number of choices times B^M steps; in C, oa_scan.c, above 2^20 steps). For T = net the
array is a (M - K, M, S)-net in base B written by the first K base-B digits of each coordinate of each point.

Prints "RESULT S" (the number of factors) as its last line and exits 0 when the strength is at least K; prints the
reason and exits 1 otherwise."""
import os
import subprocess
import sys


def depth_vectors(s, t, k, cap):
    row = [1] + [0] * k
    for _ in range(s):
        new, run = [0] * (k + 1), 0
        for j in range(k + 1):
            run += row[j]
            if j - t - 1 >= 0:
                run -= row[j - t - 1]
            new[j] = run
        row = new
        if row[k] > cap:
            break
    return row[k]


def read_runs(path, b):
    runs = []
    for no, line in enumerate(open(path), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        toks = s.replace(",", " ").split()
        if len(toks) == 1 and b <= 10 and len(toks[0]) > 1 and toks[0].isdigit():
            toks = list(toks[0])
        if not all(x.isdigit() for x in toks):
            raise ValueError(f"line {no}: not a list of symbols")
        run = [int(x) for x in toks]
        if any(x >= b for x in run):
            raise ValueError(f"line {no}: a symbol is not below {b}")
        runs.append(run)
    if not runs or len({len(r) for r in runs}) != 1:
        raise ValueError("the runs do not all have the same positive length")
    return runs


def skewed_python(runs, b, s, D, t, k):
    """None when every depth vector is uniform, else the chosen (factor, depth) pairs of a non-uniform one."""
    N = len(runs)
    want = N // b ** k

    def rec(start, r, part, chosen):
        for f in range(start, s):
            if (s - f) * t < r:
                return None
            cur = part
            for d in range(1, min(t, r) + 1):
                cur = [x * b + run[f * D + d - 1] for x, run in zip(cur, runs)]
                if r - d == 0:
                    counts = {}
                    for x in cur:
                        counts[x] = counts.get(x, 0) + 1
                    if len(counts) != b ** k or any(v != want for v in counts.values()):
                        return chosen + [(f + 1, d)]
                else:
                    bad = rec(f + 1, r - d, cur, chosen + [(f + 1, d)])
                    if bad:
                        return bad
        return None
    return rec(0, k, [0] * N, [])


def skewed_native(runs, b, s, D, t, k):
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", "oa_scan"), os.path.join(here, "oa_scan.c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    text = f"{b} {len(runs)} {s} {D} {t} {k}\n" + "".join(" ".join(map(str, r)) + "\n" for r in runs)
    out = subprocess.run([exe], input=text, capture_output=True, text=True, check=True).stdout.split("\n")[0]
    if out.startswith("uniform"):
        return None
    return out[len("skewed "):]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    force = None
    for flag in ("--native", "--python"):
        if flag in argv:
            argv.remove(flag)
            force = flag
    if len(argv) != 5:
        print(__doc__)
        return 1
    try:
        b, m, k = int(argv[0]), int(argv[2]), int(argv[3])
        T = None if argv[1] == "net" else int(argv[1])
        if b < 2 or b > 256 or m < 1 or not 1 <= k <= m or (T is not None and T < 1):
            raise ValueError("need 2 <= B <= 256, M >= 1, 1 <= K <= M, T >= 1 or net")
        runs = read_runs(argv[4], b)
    except (ValueError, OSError) as err:
        print(f"malformed: {err}")
        return 1
    D = k if T is None else T
    if len(runs) != b ** m:
        print(f"malformed: {len(runs)} runs, expected {b}^{m} = {b ** m}")
        return 1
    if len(runs[0]) % D:
        print(f"malformed: {len(runs[0])} symbols per run is not a multiple of the depth {D}")
        return 1
    s = len(runs[0]) // D
    t = min(D, k)
    if s * t < k:
        print(f"malformed: {s} factors of depth {t} cannot carry strength {k}")
        return 1
    n = depth_vectors(s, t, k, 10 ** 18)
    work = n * b ** m
    print(f"array with {b}^{m} runs, {s} factors of depth {'net (' + str(k) + ')' if T is None else T}; {n} choices "
          f"of depths of weight {k}, {work} steps")
    native = force == "--native" or (force is None and work > 2 ** 20)
    bad = skewed_native(runs, b, s, D, t, k) if native else skewed_python(runs, b, s, D, t, k)
    if bad:
        print(f"NOT strength {k}: the choice of depths (factor, depth) = {bad if isinstance(bad, str) else ', '.join(map(str, bad))} is not uniform")
        return 1
    print(f"strength at least {k}: every choice of depths of weight {k} is uniform" + (" (checked in C)" if native else ""))
    print(f"RESULT {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
