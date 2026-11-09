"""The Gaussian-prime point sets of the tsp-gaussian problem (our own code, Quantavane Originals).

  python3 -I gaussian_primes_instance.py X OUT.txt

The points are the Gaussian primes a + bi with a > 0, b >= 0 (one of the four associates of each prime element) and
norm a^2 + b^2 <= X, at the integer coordinates (1000 a, 1000 b), numbered in order of norm, then a. A Gaussian
integer a + bi with a, b > 0 is prime when a^2 + b^2 is prime; a + 0i is prime when a is a prime = 3 (mod 4); and
1 + i (norm 2) is prime. The file written is the instance."""
import sys


def isprime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def main():
    X, out = int(sys.argv[1]), sys.argv[2]
    pts = []
    a = 1
    while a * a <= X:
        b = 0
        while a * a + b * b <= X:
            n = a * a + b * b
            if (b == 0 and isprime(a) and a % 4 == 3) or (b > 0 and isprime(n)):
                pts.append((n, a, b))
            b += 1
        a += 1
    pts.sort()
    with open(out, "w") as f:
        f.write(f"# Gaussian primes a + bi, a > 0, b >= 0, norm <= {X}, at (1000a, 1000b), in order of norm then a\n{len(pts)}\n")
        for k, (n, a, b) in enumerate(pts, 1):
            f.write(f"{k} {1000 * a} {1000 * b}\n")
    print(len(pts))


if __name__ == "__main__":
    main()
