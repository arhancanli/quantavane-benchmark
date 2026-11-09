"""The Jacobsthal function of the Gaussian integers: from residue classes to a square (our own code, Quantavane
Originals, problem gauss-jacobsthal).

  python3 -I gauss_jacobsthal.py "cover S: a,b,c a,b,c ..." OUT.txt

The search program (tools/src/gjacob.c) prints a cover of the S x S square {j + ki : 0 <= j, k < S} by one residue
class per Gaussian prime: "a,b,c" for the prime a + bi (b = 0: the inert prime a = 3 mod 4; a = b = 1: 1 + i) and the
class c of the points it covers (c = (j + k r) mod p for a + bi of norm p, where r = -a/b mod p, so that a + bi
divides x + yi exactly when x + y r = 0 mod p; c = (j mod q) q + (k mod q) for an inert q; c = (j + k) mod 2 for 1 + i).
By the Chinese remainder theorem there is a corner x0 + y0 i whose translate of the square has every point divisible by
its chosen prime; this program finds it and writes "x0 y0 S"."""
import sys


def crt(pairs):
    x, m = 0, 1
    for r, q in pairs:
        t = ((r - x) * pow(m, -1, q)) % q
        x, m = x + m * t, m * q
    return x % m, m


def main():
    line, out = sys.argv[1], sys.argv[2]
    head, body = line.split(":", 1)
    side = int(head.split()[1])
    by_p = {}
    xs, ys = [], []
    for item in body.split():
        a, b, c = (int(t) for t in item.split(","))
        if a == 1 and b == 1:
            xs.append((c % 2, 2))
            ys.append((0, 2))
        elif b == 0:
            q = a
            xs.append(((-(c // q)) % q, q))
            ys.append(((-(c % q)) % q, q))
        else:
            p = a * a + b * b
            r = (-a * pow(b % p, -1, p)) % p
            by_p.setdefault(p, []).append((r, (-c) % p))
    for p, eqs in by_p.items():
        if len(eqs) == 1:
            (r, t), = eqs
            xs.append((t, p))
            ys.append((0, p))
        else:
            (r1, t1), (r2, t2) = eqs        # x + r1 y = t1, x + r2 y = t2 (mod p)
            y = ((t1 - t2) * pow((r1 - r2) % p, -1, p)) % p
            xs.append(((t1 - r1 * y) % p, p))
            ys.append((y, p))
    x0, m = crt(xs)
    y0, m2 = crt(ys)
    with open(out, "w") as f:
        f.write(f"{x0} {y0} {side}\n")
    print(f"corner {x0} + {y0}i (moduli {m}), side {side}")


if __name__ == "__main__":
    main()
