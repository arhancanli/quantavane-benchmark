"""Energy of a Lennard-Jones cluster, with a proven bound (standard library only).

  python3 -I cluster_check.py lj N FILE

FILE: N lines, each the position of one atom, three decimal numbers (reduced units: sigma = epsilon = 1). Blank lines
and lines starting with '#' are ignored. The energy is E = sum over pairs of 4 (r^-12 - r^-6). Every coordinate is read
exactly; each pair's term is the exact fraction 4 S^6 (S^6 - D^3) / D^6 (D = the squared distance times S^2, an
integer, for the common scale S), rounded up at the 30th decimal, and the sum is rounded up at the 12th decimal: the
printed value is a proven upper bound for E, at most 10^-12 above it. Two atoms at the same place are refused.

Prints "energy_upper X" and, as its last line, "RESULT p/q" (X as a fraction), and exits 0; exits 1 for malformed
input."""
import sys
from math import gcd


def parse_dec(s):
    s = s.strip()
    neg = s.startswith("-")
    body = s[1:] if s[:1] in "+-" else s
    if not body or "e" in body.lower() or body.count(".") > 1 or not body.replace(".", "").isdigit():
        raise ValueError("not a decimal number: " + s)
    whole, _, frac = body.partition(".")
    v = int((whole or "0") + frac)
    return (-v if neg else v), len(frac)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3 or argv[0] != "lj":
        print(__doc__)
        return 1
    try:
        n = int(argv[1])
        lines = [l.strip() for l in open(argv[2]) if l.strip() and not l.strip().startswith("#")]
        if len(lines) != n:
            raise ValueError(f"expected {n} lines, found {len(lines)}")
        raw = []
        for i, l in enumerate(lines):
            parts = l.replace(",", " ").split()
            if len(parts) != 3:
                raise ValueError(f"line {i + 1}: expected 3 coordinates")
            raw.append([parse_dec(p) for p in parts])
    except (ValueError, OSError) as err:
        print("malformed:", err)
        return 1
    scale = max(d for p in raw for _, d in p)
    S = 10 ** scale
    pts = [[v * 10 ** (scale - d) for v, d in p] for p in raw]
    S6 = S ** 6
    K = 10 ** 30
    total = 0                                  # sum of the terms times 10^30, each rounded up
    for i in range(n):
        xi, yi, zi = pts[i]
        for j in range(i + 1, n):
            xj, yj, zj = pts[j]
            D = (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2
            if D == 0:
                print(f"atoms {i + 1} and {j + 1} are at the same place")
                return 1
            D3 = D ** 3
            num = 4 * S6 * (S6 - D3) * K
            den = D3 * D3
            total += -((-num) // den)          # ceiling
    unit = 10 ** 18                            # from 10^-30 to 10^-12
    up = -((-total) // unit)                   # rounded up at the 12th decimal
    g = gcd(up, 10 ** 12)
    p, q = up // g, 10 ** 12 // g
    sign = "-" if up < 0 else ""
    a = abs(up)
    print(f"energy_upper {sign}{a // 10 ** 12}.{a % 10 ** 12:012d}")
    print(f"{n} atoms, {n * (n - 1) // 2} pairs, no two at the same place")
    print("RESULT", p if q == 1 else f"{p}/{q}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
