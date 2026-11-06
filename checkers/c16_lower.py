"""Benchmark checker for lower bounds on C16 (16a page): c16_lower.py FILE, FILE a JSON {"mu": M} or {"mu": M, "R": R}.

The trial function u = sum_k c_k e^{ik.x}, c_k = 1/(|k|^2 (1 + mu |k|^2)), over all k != 0, or over 0 < |k| <= R when R is
given; mu as p/q or a hex float. The bound S0^2/(pi S1) - ln(delta) - ln(1 + ln(delta)), delta = S2/S1, is enclosed by
c16_check.py (untruncated: row sums in closed form) or c16_trunc_check.py (truncated: the disc's sums in integers at
2^256); prints "RESULT C16 >= X" with X the lower end of the enclosure. Standard library only."""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16_check  # noqa: E402
import c16_trunc_check  # noqa: E402


def main():
    d = json.load(open(sys.argv[1]))
    mu = c16_check.hexdec(str(d["mu"])) if str(d["mu"]).startswith("0x") else c16_check.D(Fraction(str(d["mu"])).numerator) / c16_check.D(Fraction(str(d["mu"])).denominator)
    if "R" in d:
        q = Fraction(str(d["mu"]))
        lo = c16_trunc_check.bound(c16_trunc_check.sums(int(d["R"]), q.numerator, q.denominator))[0]
    else:
        lo = c16_check.lower(mu)[0]
    print(f"RESULT C16 >= {lo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
