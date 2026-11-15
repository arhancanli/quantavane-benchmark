"""Exact check of a difference set in an abelian group (standard library only).

  python3 -I ds_check.py GROUP K L FILE

GROUP is the list of cyclic orders n_1,n_2,...,n_r of G = Z_n1 x ... x Z_nr, as in D. Gordon's La Jolla Difference Set
Repository (for instance 400 for the cyclic group, or 20,20 or 2,10,20). FILE has one element per line: r integers
a_1 ... a_r with 0 <= a_c < n_c, separated by spaces or commas ('#' starts a comment); for a cyclic group one integer.

A (v,k,lambda) difference set is a set D of K distinct elements of G (v = |G|) such that every nonzero element of G is
a difference d - d' of two elements of D in exactly L ways. The checker counts the differences of all K(K-1) ordered
pairs exactly, in Python, or above 10^6 pairs in the C helper ds_scan.c (built with cc -O3 on first use), which
rewrites G by the Chinese remainder theorem as a product of the fewest cyclic groups and counts each difference with
one XOR or subtraction (about a second per 10^9 pairs for cyclic groups); --native or --python forces one way, and
--plain makes the C helper count digit by digit in the given coordinates (a separate route, for the tests). Prints the parameters and "RESULT 1" (a difference set
with these parameters exists in G) and exits 0 for a valid set; exits 1 otherwise.

With --signed it checks a signed difference set (Gordon, 2023): each line starts with a sign + or - before the
coordinates, and for every nonzero element g of G the sum of s s' over the ordered pairs of elements d (sign s) and d'
(sign s') with d - d' = g must be L (which may be negative); then (number of + minus number of -)^2 = (K - L) + L v.
Signed sets are counted in Python."""
import os
import subprocess
import sys

NATIVE_FROM = 10 ** 6


def helper():
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", "ds_scan"), os.path.join(here, "ds_scan.c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    return exe


def count_python(orders, elems, lam, signs=None):
    """(pairs with difference 0, nonzero elements not hit lam times, the first such rank); with signs, each ordered
    pair counts the product of its two signs"""
    v = 1
    for n in orders:
        v *= n
    w, acc = [0] * len(orders), 1
    for c in range(len(orders) - 1, -1, -1):
        w[c] = acc
        acc *= orders[c]
    cnt = [0] * v
    sg = signs or [1] * len(elems)
    for a, sa in zip(elems, sg):
        for b, sb in zip(elems, sg):
            if a is b:
                continue
            cnt[sum((x - y) % n * wc for x, y, n, wc in zip(a, b, orders, w))] += sa * sb
    bad = [x for x in range(1, v) if cnt[x] != lam]
    return cnt[0], len(bad), (bad[0] if bad else -1)


def count_native(orders, elems, lam, plain=False):
    """The same counts in C (checkers/ds_scan.c; plain: digit by digit in the given coordinates, the slowest way)."""
    text = f"{len(orders)}\n{' '.join(map(str, orders))}\n{len(elems)}\n" + "".join(
        " ".join(map(str, e)) + "\n" for e in elems)
    out = subprocess.run([helper(), str(lam)] + (["plain"] if plain else []), input=text, capture_output=True,
                         text=True, check=True).stdout.split()
    vals = dict(zip(out[::2], out[1::2]))
    assert int(vals["pairs"]) == len(elems) * (len(elems) - 1), "ds_scan: unexpected count"
    return int(vals["zero"]), int(vals["bad"]), int(vals["first"])


def element(rank, orders):
    out = []
    for n in reversed(orders):
        out.append(rank % n)
        rank //= n
    return tuple(reversed(out))


def main():
    flags = [a for a in sys.argv[1:] if a in ("--native", "--python", "--plain", "--signed")]
    signed = "--signed" in flags
    args = [a for a in sys.argv[1:] if a not in flags]
    if len(args) != 4:
        print(__doc__)
        return 2
    try:
        orders = [int(x) for x in args[0].split(",")]
        k, lam = int(args[1]), int(args[2])
    except ValueError:
        print("GROUP must be orders separated by commas, K and L integers")
        return 2
    if not orders or min(orders) < 1 or k < 1 or (lam < 0 and not signed):
        print("bad parameters")
        return 2
    v = 1
    for n in orders:
        v *= n
    elems, signs = [], []
    for line in open(args[3]):
        line = line.split("#")[0].replace(",", " ").strip()
        if not line:
            continue
        if signed:
            sign, _, line = line.partition(" ")
            if sign not in ("+", "-", "+1", "-1", "1"):
                print(f"a signed element starts with + or -: {sign[:20]!r}")
                return 1
            signs.append(-1 if sign.startswith("-") else 1)
            line = line.strip()
        try:
            e = tuple(int(x) for x in line.split())
        except ValueError:
            print(f"not a list of integers: {line[:80]!r}")
            return 1
        if len(e) != len(orders) or not all(0 <= x < n for x, n in zip(e, orders)):
            print(f"element {line[:80]!r} is not in Z_{' x Z_'.join(map(str, orders))} (coordinates 0 <= a_c < n_c)")
            return 1
        elems.append(e)
    print(f"group Z_{' x Z_'.join(map(str, orders))} of order {v}; {len(elems)} elements; lambda {lam}")
    if len(elems) != k:
        print(f"{len(elems)} elements, not {k}")
        return 1
    if len(set(elems)) != k:
        print("an element is repeated")
        return 1
    if signed:
        plus = signs.count(1)
        if (2 * plus - k) ** 2 != (k - lam) + lam * v:
            print(f"no signed ({v},{k},{lam}) difference set with {plus} signs +: (#+ - #-)^2 = {(2 * plus - k) ** 2} "
                  f"differs from (k - lambda) + lambda v = {(k - lam) + lam * v}")
            return 1
        zero, bad, first = count_python(orders, elems, lam, signs)
        if zero or bad:
            print(f"{bad} nonzero elements have signed difference count other than {lam}"
                  + (f", the first {element(first, orders)}" if first >= 0 else ""))
            return 1
        print(f"every nonzero element has signed difference count {lam}")
        print("RESULT 1")
        return 0
    if lam * (v - 1) != k * (k - 1):
        print(f"no ({v},{k},{lam}) difference set: lambda (v - 1) = {lam * (v - 1)} differs from k (k - 1) = "
              f"{k * (k - 1)}")
        return 1
    native = "--native" in flags or "--plain" in flags or ("--python" not in flags and k * (k - 1) > NATIVE_FROM)
    if native:
        zero, bad, first = count_native(orders, elems, lam, plain="--plain" in flags)
    else:
        zero, bad, first = count_python(orders, elems, lam)
    if zero or bad:
        what = f"{bad} nonzero elements are not differences exactly {lam} times"
        if first >= 0:
            what += f", the first {element(first, orders)}"
        print(what + (" (counted in C)" if native else ""))
        return 1
    print(f"every nonzero element is a difference exactly {lam} times" + (" (counted in C)" if native else ""))
    print("RESULT 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
