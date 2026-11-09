"""Instances from the Yale Bright Star Catalogue, 5th revised edition (our own code, Quantavane Originals).

  python3 -I bsc_instances.py heasarc_bsc5p.tdat.gz OUTDIR [VLIM RADIUS_DEG NSIDE]

Reads the catalogue as distributed by NASA HEASARC (table heasarc_bsc5p: D. Hoffleit and W. H. Warren Jr., The Bright
Star Catalogue, 5th revised ed., Yale University Observatory, 1991) and keeps every star with a J2000 position.

  OUTDIR/bsc-sky.txt       one line per star, sorted by HR number: "HR RA DEC V" with RA in tenths of a second of
                           time (0..863999), DEC in arcseconds (-324000..324000), V in hundredths of a magnitude, all
                           copied exactly from the catalogue's sexagesimal J2000 fields.
  OUTDIR/star-tracker.txt  (with VLIM, RADIUS_DEG, NSIDE) the stars with V <= VLIM and the HEALPix ring-scheme pixel
                           centres for NSIDE (Gorski et al. 2005) as boresight directions, every direction a unit vector
                           rounded to integers (times 10^9); a star lies in the field of view of a boresight when the
                           dot product of their integer vectors is at least T = round(10^18 cos RADIUS). Format: line
                           "T", line "S B" (numbers of stars and boresights), S lines "HR x y z", B lines "x y z".
The rounding is done once here; the checker uses only the integers in the file."""
import gzip
import math
import os
import sys

SCALE = 10 ** 9


def stars(path):
    lines = gzip.open(path, "rt", errors="replace").read().splitlines()
    fields = next(l for l in lines if l.startswith("line[1]")).split("=", 1)[1].split()
    start = next(k for k, l in enumerate(lines) if l.startswith("<DATA>")) + 1
    out = []
    for l in lines[start:]:
        if l.startswith("<END>") or "|" not in l:
            continue
        rec = dict(zip(fields, l.split("|")))
        cra, cdec, v, hr = rec["cra"].strip(), rec["cdec"].strip(), rec["vmag"].strip(), rec["hr"].strip()
        if not cra or not cdec or not v or not hr:
            continue
        h, m, s = int(cra[0:2]), int(cra[2:4]), cra[4:]
        sec, tenth = s.split(".")
        ra = ((h * 60 + m) * 60 + int(sec)) * 10 + int(tenth)
        sign = -1 if cdec[0] == "-" else 1
        d, mi, se = int(cdec[1:3]), int(cdec[3:5]), int(cdec[5:7])
        dec = sign * ((d * 60 + mi) * 60 + se)
        vv = round(float(v) * 100)
        out.append((int(hr), ra, dec, vv))
    out.sort()
    return out


def unit(ra_rad, dec_rad):
    return (round(SCALE * math.cos(dec_rad) * math.cos(ra_rad)), round(SCALE * math.cos(dec_rad) * math.sin(ra_rad)),
            round(SCALE * math.sin(dec_rad)))


def healpix_centres(N):
    """Pixel centres of the HEALPix ring scheme (Gorski et al. 2005, ApJ 622, 759, eqs. 4-9) as (z, phi)."""
    out = []
    for i in range(1, 4 * N):
        if i < N:
            z = 1 - i * i / (3 * N * N)
            out += [(z, math.pi / (2 * i) * (j - 0.5)) for j in range(1, 4 * i + 1)]
        elif i <= 3 * N:
            z = 4 / 3 - 2 * i / (3 * N)
            s = (i - N + 1) % 2
            out += [(z, math.pi / (2 * N) * (j - s / 2)) for j in range(1, 4 * N + 1)]
        else:
            k = 4 * N - i
            z = -(1 - k * k / (3 * N * N))
            out += [(z, math.pi / (2 * k) * (j - 0.5)) for j in range(1, 4 * k + 1)]
    assert len(out) == 12 * N * N
    return out


def main():
    if len(sys.argv) not in (3, 6):
        print(__doc__)
        return 2
    S = stars(sys.argv[1])
    os.makedirs(sys.argv[2], exist_ok=True)
    with open(os.path.join(sys.argv[2], "bsc-sky.txt"), "w") as f:
        f.write(f"# Yale Bright Star Catalogue, 5th revised ed. (Hoffleit and Warren 1991; NASA HEASARC table "
                f"heasarc_bsc5p): {len(S)} stars with a J2000 position\n# HR, RA (tenths of a second of time), "
                f"Dec (arcseconds), V (hundredths of a magnitude)\n")
        for r in S:
            f.write("%d %d %d %d\n" % r)
    print(len(S), "stars with positions")
    if len(sys.argv) == 6:
        vlim, rad, N = float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
        sel = [r for r in S if r[3] <= round(vlim * 100)]
        T = round(SCALE * SCALE * math.cos(math.radians(rad)))
        B = [(round(SCALE * math.sqrt(1 - z * z) * math.cos(p)), round(SCALE * math.sqrt(1 - z * z) * math.sin(p)),
              round(SCALE * z)) for z, p in healpix_centres(N)]
        with open(os.path.join(sys.argv[2], "star-tracker.txt"), "w") as f:
            f.write(f"# stars of the Yale Bright Star Catalogue (5th rev. ed.) with V <= {vlim}; boresights: HEALPix "
                    f"Nside = {N} pixel centres; field of view radius {rad} degrees\n{T}\n{len(sel)} {len(B)}\n")
            for hr, ra, dec, v in sel:
                x, y, z = unit(ra * math.pi / 432000, dec * math.pi / 648000)
                f.write(f"{hr} {x} {y} {z}\n")
            for x, y, z in B:
                f.write(f"{x} {y} {z}\n")
        print(len(sel), "stars with V <=", vlim, ";", len(B), "boresights")
    return 0


if __name__ == "__main__":
    sys.exit(main())
