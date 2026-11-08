"""Exact check of a sorting network (standard library only).

  python3 -I sortnet_check.py N FILE

FILE lists the comparators in order, each as a pair of channel numbers from 0 to N-1: every two integers in the file
form one comparator, so Bert Dobbelaere's format "[(0,13),(1,12),...],[(0,5),...]" and one "i j" per line both work
(text after # on a line is ignored). A comparator on channels i and j puts the smaller value on the lower-numbered
channel. The network sorts every input exactly when it sorts every input of 0s and 1s (Knuth's 0-1 principle).

The checker runs all 0-1 inputs at once, bit-sliced: channel c is held as a bit set with one bit per input, and a
comparator maps the pair (a, b) to (a and b, a or b). Inputs that agree after the first layer of comparators (the
longest opening run on disjoint channels) are run once: each first-layer comparator leaves 3 of its 4 input pairs and
each other channel 2 values, so the inputs to the rest of the network form a product set, enumerated in blocks of at
most 2^24 inputs. The network sorts when, on every input, channel c is at most channel c+1. Prints the size (number of
comparators) and the depth (number of layers when each comparator runs as early as it can), then "RESULT size";
exits 0 for a sorting network, 1 otherwise."""
import itertools
import re
import sys

INNER_BITS = 24


def repeat(block, period, total):
    """The bit pattern `block` (period bits) repeated to fill `total` bits."""
    x, length = block, period
    while length < total:
        x |= x << length
        length <<= 1
    return x & ((1 << total) - 1)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    n = int(sys.argv[1])
    text = "\n".join(line.split("#")[0] for line in open(sys.argv[2], encoding="ascii", errors="replace"))
    nums = [int(x) for x in re.findall(r"-?\d+", text)]
    if len(nums) % 2:
        print("an odd number of channel numbers: comparators come in pairs")
        return 1
    comps = []
    for a, b in zip(nums[0::2], nums[1::2]):
        if a == b or not (0 <= a < n and 0 <= b < n):
            print(f"comparator ({a},{b}) is not two different channels from 0 to {n - 1}")
            return 1
        comps.append((min(a, b), max(a, b)))
    level = [0] * n
    depth = 0
    for a, b in comps:
        level[a] = level[b] = max(level[a], level[b]) + 1
        depth = max(depth, level[a])
    used, first = set(), []
    for a, b in comps:
        if a in used or b in used:
            break
        used.update((a, b))
        first.append((a, b))
    rest = comps[len(first):]
    # factors of the input set after the first layer: a first-layer pair takes 00, 01, 11; another channel 0 or 1
    factors = [("pair", a, b) for a, b in first] + [("free", c, None) for c in range(n) if c not in used]
    inner, outer, total = [], [], 1
    for f in factors:
        r = 3 if f[0] == "pair" else 2
        if total * r <= (1 << INNER_BITS) and not outer:
            inner.append(f)
            total *= r
        else:
            outer.append(f)
    patterns = {}
    period = 1
    for kind, a, b in inner:
        r = 3 if kind == "pair" else 2
        if kind == "pair":                     # digit 0: (0,0), 1: (0,1), 2: (1,1)
            patterns[a] = repeat((1 << (3 * period)) - (1 << (2 * period)), 3 * period, total)
            patterns[b] = repeat((1 << (3 * period)) - (1 << period), 3 * period, total)
        else:
            patterns[a] = repeat((1 << (2 * period)) - (1 << period), 2 * period, total)
        period *= r
    full = (1 << total) - 1
    radices = [range(3) if kind == "pair" else range(2) for kind, _, _ in outer]
    blocks = 0
    for values in itertools.product(*radices):
        blocks += 1
        ch = [0] * n
        for c, pat in patterns.items():
            ch[c] = pat
        for (kind, a, b), v in zip(outer, values):
            if kind == "pair":
                ch[a] = full if v == 2 else 0
                ch[b] = full if v >= 1 else 0
            else:
                ch[a] = full if v else 0
        for a, b in rest:
            x, y = ch[a], ch[b]
            ch[a], ch[b] = x & y, x | y
        for c in range(n - 1):
            if ch[c] | ch[c + 1] != ch[c + 1]:
                print(f"not a sorting network: some 0-1 input leaves a 1 on channel {c} above a 0 on channel {c + 1}")
                return 1
    print(f"sorting network on {n} channels: size {len(comps)} depth {depth} (first layer {len(first)} comparators, "
          f"{blocks} block(s) of {total} inputs)")
    print(f"RESULT {len(comps)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
