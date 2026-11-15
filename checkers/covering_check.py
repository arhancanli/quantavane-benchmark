"""Exact check of a covering design (standard library only).

  python3 -I covering_check.py V K T M FILE

FILE has one block per line, K distinct points from 1..V separated by spaces ('#' starts a comment).

With M = T this is a (V,K,T) covering: every T-subset of {1..V} must lie in some block. Every T-subset of every block
is marked in a bit array indexed by its rank (colex order), and all C(V,T) bits must be set; a design whose blocks hold
fewer than C(V,T) T-subsets in all is refused at once, so the array is never larger than the work done to fill it.

With M > T it is a (V,K,T,M) covering: every M-subset must meet some block in at least T points, that is, no M-subset
meets every block in at most T-1 points. An exact branch-and-bound search looks for such an M-subset: points are added
one at a time (the others stay candidates until some block holding them already has T-1 chosen points), and a branch
is cut when even the candidates cannot complete it: split along blocks, the candidates inside a block can add at most
that block's remaining room T-1-(chosen points in it). The search is complete, so "no bad M-subset" is a proof.

Above 2 x 10^7 subsets to mark (M = T) the marking is done by the C helper covering_mark.c (built with cc -O3 on first
use; the bit array then holds up to 2^36 bits). For M > T with more than 40 blocks (and V <= 128) the search runs in
the C helper covering_lotto.c, the same search step for step (it visits the same nodes and finds the same bad set),
about 2.5 ns per block per node. --native or --python forces one way.

Prints "blocks B" and, as its last line, "RESULT B", and exits 0 when the design is valid; exits 1 otherwise."""
import itertools
import math
import sys

try:
    popcount = int.bit_count        # Python 3.10+
except AttributeError:              # Python 3.9
    def popcount(x):
        return bin(x).count("1")


NATIVE_FROM = 2 * 10 ** 7                 # above this many t-subsets to mark, the C helper covering_mark.c marks them
NATIVE_LOTTO_FROM = 40                    # above this many blocks (m > t, v <= 128), covering_lotto.c searches


def helper(name):
    """The C helper checkers/NAME.c, built with cc -O3 into checkers/bin/ on first use (and again when it changes)."""
    import os
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    exe, src = os.path.join(here, "bin", name), os.path.join(here, name + ".c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        subprocess.run(["cc", "-O3", "-o", exe, src], check=True)
    return exe


def find_bad_set_native(blocks, v, k, t, m):
    """find_bad_set in C (checkers/covering_lotto.c): the same search, so the same answer."""
    import subprocess
    text = f"{len(blocks)}\n" + "".join(" ".join(str(p - 1) for p in sorted(b)) + "\n" for b in blocks)
    out = subprocess.run([helper("covering_lotto"), str(v), str(k), str(t), str(m)], input=text,
                         capture_output=True, text=True, check=True).stdout.split("\n")
    if out[0] == "none":
        return None
    bad = [int(x) + 1 for x in out[0].split()[1:]]
    assert out[0].startswith("bad ") and len(set(bad)) == m and all(1 <= p <= v for p in bad), "covering_lotto: output"
    assert all(len(set(bad) & set(b)) < t for b in blocks), "covering_lotto: the set it found is not bad"
    return bad


def covers_native(blocks, v, k, t):
    """The same marking in C (checkers/covering_mark.c, built with cc -O3 on first use); returns (covered, total)."""
    import subprocess
    exe = helper("covering_mark")
    text = f"{len(blocks)}\n" + "".join(" ".join(str(p - 1) for p in sorted(b)) + "\n" for b in blocks)
    out = subprocess.run([exe, str(v), str(k), str(t)], input=text, capture_output=True, text=True, check=True).stdout
    covered, total = (int(x) for x in out.split()[1:4:2])
    marks = int(out.split()[-1])
    assert total == math.comb(v, t) and marks == len(blocks) * math.comb(k, t), "covering_mark: unexpected counts"
    return covered, total


def covers_everything(blocks, v, k, t, native=None):
    total = math.comb(v, t)
    if len(blocks) * math.comb(k, t) < total:
        return False, (f"{len(blocks)} blocks hold at most {len(blocks) * math.comb(k, t)} {t}-subsets, "
                       f"fewer than the {total} to cover")
    if native if native is not None else len(blocks) * math.comb(k, t) > NATIVE_FROM:
        covered, total = covers_native(blocks, v, k, t)
        if covered == total:
            return True, f"every one of the {total} {t}-subsets lies in a block (marked in C)"
        return False, f"{total - covered} of {total} {t}-subsets uncovered (marked in C)"
    bits = bytearray((total + 7) // 8)
    for b in blocks:
        pts = sorted(p - 1 for p in b)
        # the colex rank of {x_1 < ... < x_t} is the sum of C(x_i, i); build all ranks of the block level by level
        level = [(j, math.comb(x, 1)) for j, x in enumerate(pts)]
        for i in range(2, t + 1):
            level = [(j2, s + math.comb(pts[j2], i)) for j, s in level for j2 in range(j + 1, k)]
        for _, r in level:
            bits[r >> 3] |= 1 << (r & 7)
    full, rest = divmod(total, 8)
    ok = bits[:full] == b"\xff" * full and (rest == 0 or bits[full] == (1 << rest) - 1)
    if ok:
        return True, f"every one of the {total} {t}-subsets lies in a block"
    missing = total - popcount(int.from_bytes(bytes(bits), "little"))
    return False, f"{missing} of {total} {t}-subsets uncovered"


def find_bad_set(blocks, v, t, m):
    """An m-subset of 1..v meeting every block in at most t-1 points, or None when there is none."""
    nb = len(blocks)
    bmask = [0] * nb
    of = [[] for _ in range(v)]
    for j, b in enumerate(blocks):
        for p in b:
            bmask[j] |= 1 << (p - 1)
            of[p - 1].append(j)
    sig = {}
    kind = [sig.setdefault(tuple(of[p]), len(sig)) for p in range(v)]   # points in the same blocks are interchangeable
    same = [0] * len(sig)
    for p in range(v):
        same[kind[p]] |= 1 << p
    cnt = [0] * nb
    chosen = []

    def parts(cand):
        """Split the candidates: the part inside block j can add at most room t-1-cnt[j] (blocks whose overlap
        exceeds their room, fullest first); the rest, in no such part, can all be added. Returns [(mask, cap)]."""
        over = []
        for j in range(nb):
            ov = popcount(bmask[j] & cand)
            room = t - 1 - cnt[j]
            if ov > room:
                over.append((room - ov, j))
        over.sort()
        rem, out = cand, []
        for _, j in over:
            part = bmask[j] & rem
            if part:
                room = t - 1 - cnt[j]
                if popcount(part) > room:
                    out.append((part, room))
                    rem &= ~part
        return [(rem, popcount(rem))] + out

    def rec(cand, s):
        if s >= m:
            return True
        if s + popcount(cand) < m:
            return False
        order, cum = [], 0
        for mask, cap in parts(cand):
            cum += cap
            order.append((mask, cum))
        for mask, cum in reversed(order):        # at most cum points can still come from this part and those before it
            c = mask & cand
            while c:
                if s + cum < m:
                    return False
                low = c & -c
                p = low.bit_length() - 1
                c ^= low
                if not cand >> p & 1:
                    continue
                cand &= ~low
                forbid = 0
                for j in of[p]:
                    cnt[j] += 1
                    if cnt[j] >= t - 1:
                        forbid |= bmask[j]
                chosen.append(p)
                if rec(cand & ~forbid, s + 1):
                    return True
                chosen.pop()
                for j in of[p]:
                    cnt[j] -= 1
                # no bad set holds p, so none holds a point of the same kind in place of p
                cand &= ~same[kind[p]]
                c &= cand
        return False

    start = (1 << v) - 1
    if t == 1:                       # room 0 from the start: no point of any block can be chosen
        for x in bmask:
            start &= ~x
    return [p + 1 for p in chosen] if rec(start, 0) else None


def main():
    flags = [a for a in sys.argv[1:] if a in ("--native", "--python")]
    args = [a for a in sys.argv[1:] if a not in flags]
    if len(args) != 5:
        print(__doc__)
        return 1
    v, k, t, m = (int(x) for x in args[:4])
    if not (1 <= t <= k <= v and t <= m <= v):
        print(f"need 1 <= T <= K <= V and T <= M <= V, got V={v} K={k} T={t} M={m}")
        return 1
    blocks = []
    for line in open(args[4]):
        line = line.split("#")[0].strip()
        if line:
            try:
                blocks.append([int(x) for x in line.split()])
            except ValueError:
                print(f"not a list of integers: {line[:80]!r}")
                return 1
    if not blocks:
        print("no blocks")
        return 1
    for b in blocks:
        if len(b) != k or len(set(b)) != k or not all(1 <= p <= v for p in b):
            print(f"invalid block {b}: need {k} distinct points from 1..{v}")
            return 1
    native = True if "--native" in flags else False if "--python" in flags else None
    if m == t:
        ok, why = covers_everything(blocks, v, k, t, native)
    else:
        if native is None:
            native = len(blocks) > NATIVE_LOTTO_FROM and v <= 128
        bad = find_bad_set_native(blocks, v, k, t, m) if native else find_bad_set(blocks, v, t, m)
        ok = bad is None
        why = ("no bad m-subset exists" + (" (searched in C)" if native else "") if ok else
               f"the {m}-subset {sorted(bad)} meets every block in fewer than {t} points")
    print(why)
    if not ok:
        return 1
    print(f"blocks {len(blocks)}")
    print(f"RESULT {len(blocks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
