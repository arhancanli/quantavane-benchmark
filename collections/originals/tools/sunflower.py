"""The sunflower (golden-angle spiral) point sets of the tsp-sunflower problem (our own code, Quantavane Originals).

  python3 -I sunflower.py N OUT.txt

Point k (k = 1, ..., N) is (round(S sqrt(k) cos(k a)), round(S sqrt(k) sin(k a))) with the golden angle
a = pi (3 - sqrt 5) and S = 1000, Vogel's model of a sunflower head. The file written here is the instance: the
checker reads the coordinates from it, so the instance does not depend on floating-point details elsewhere."""
import math
import sys


def main():
    n, out = int(sys.argv[1]), sys.argv[2]
    a = math.pi * (3 - math.sqrt(5))
    with open(out, "w") as f:
        f.write(f"# sunflower {n}: point k = (round(1000 sqrt(k) cos(k a)), round(1000 sqrt(k) sin(k a))), a = pi (3 - sqrt 5)\n")
        f.write(f"{n}\n")
        for k in range(1, n + 1):
            r = 1000 * math.sqrt(k)
            f.write(f"{k} {round(r * math.cos(k * a))} {round(r * math.sin(k * a))}\n")


if __name__ == "__main__":
    main()
