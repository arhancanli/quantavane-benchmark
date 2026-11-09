/* Lennard-Jones clusters on the face-centred cubic lattice (our own code, Quantavane Originals, problem lj-fcc).
   Sites: integer points (x, y, z) with x + y + z even; nearest neighbours at squared distance q = 2 sit at the
   minimum of the pair potential, so the pair energy is 64/q^6 - 16/q^3 (in units of the well depth; -1 for nearest
   neighbours), summed over the pairs with q <= 8 (the usual cutoff at 2.5 sigma keeps the first four shells).
   cc -O2 -o ljfcc ljfcc.c -lm ; ./ljfcc N SECONDS SEED OUT.txt
   Start: the N sites nearest to a random centre; moves: an occupied site with the highest energy goes to the empty
   site (adjacent to the cluster) with the lowest energy, with Metropolis acceptance at a slowly falling temperature
   and restarts; the best cluster is written as lines "x y z". Floating point here; the checker sums exactly. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define L 24
#define IDX(x, y, z) ((((x) + L) * (2 * L + 1) + ((y) + L)) * (2 * L + 1) + ((z) + L))
static double pe(int q) { if (q > 8) return 0; double q3 = (double)q * q * q; return 64.0 / (q3 * q3) - 16.0 / q3; }
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double ur(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static int N, cx[512], cy[512], cz[512]; static unsigned char *occ;
static double site_e(int x, int y, int z, int skip) { double e = 0; for (int i = 0; i < N; i++) { if (i == skip) continue; int dx = x - cx[i], dy = y - cy[i], dz = z - cz[i]; int q = dx * dx + dy * dy + dz * dz; if (q) e += pe(q); } return e; }
static double total(void) { double e = 0; for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) { int dx = cx[i] - cx[j], dy = cy[i] - cy[j], dz = cz[i] - cz[j]; e += pe(dx * dx + dy * dy + dz * dz); } return e; }
static const int nb[12][3] = {{1,1,0},{1,-1,0},{-1,1,0},{-1,-1,0},{1,0,1},{1,0,-1},{-1,0,1},{-1,0,-1},{0,1,1},{0,1,-1},{0,-1,1},{0,-1,-1}};
int main(int argc, char **argv) {
  N = atoi(argv[1]); double secs = atof(argv[2]); rs ^= (unsigned long long)atoi(argv[3]) * 2654435761ULL;
  occ = calloc((size_t)(2 * L + 1) * (2 * L + 1) * (2 * L + 1), 1);
  double bestE = 1e300; int bx[512], by[512], bz[512]; clock_t st = clock(); int restarts = 0;
  while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) { restarts++;
    memset(occ, 0, (size_t)(2 * L + 1) * (2 * L + 1) * (2 * L + 1));
    double ox = ur(), oy = ur(), oz = ur(); /* N sites nearest to a random centre */
    int R = 8, cnt = 0; static int px[40000], py[40000], pz[40000]; static double pd[40000];
    for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) for (int z = -R; z <= R; z++) if (((x + y + z) & 1) == 0) { px[cnt] = x; py[cnt] = y; pz[cnt] = z; pd[cnt] = (x - ox) * (x - ox) + (y - oy) * (y - oy) + (z - oz) * (z - oz); cnt++; }
    for (int i = 0; i < N; i++) { int b = i; for (int j = i + 1; j < cnt; j++) if (pd[j] < pd[b]) b = j;
      double t = pd[i]; pd[i] = pd[b]; pd[b] = t; int s = px[i]; px[i] = px[b]; px[b] = s; s = py[i]; py[i] = py[b]; py[b] = s; s = pz[i]; pz[i] = pz[b]; pz[b] = s;
      cx[i] = px[i]; cy[i] = py[i]; cz[i] = pz[i]; occ[IDX(cx[i], cy[i], cz[i])] = 1; }
    double E = total(), T = 0.6; int steps = 4000 + 40 * N;
    for (int s = 0; s < steps; s++, T *= 0.999) {
      int i = rnd() % N; double ei = site_e(cx[i], cy[i], cz[i], i);
      /* candidate: empty neighbour of a random occupied atom */
      int j = rnd() % N, k = rnd() % 12; int x = cx[j] + nb[k][0], y = cy[j] + nb[k][1], z = cz[j] + nb[k][2];
      if (abs(x) >= L - 1 || abs(y) >= L - 1 || abs(z) >= L - 1 || occ[IDX(x, y, z)]) continue;
      double en = site_e(x, y, z, i); double d = en - ei;
      if (d < 0 || ur() < exp(-d / (T + 1e-9))) { occ[IDX(cx[i], cy[i], cz[i])] = 0; cx[i] = x; cy[i] = y; cz[i] = z; occ[IDX(x, y, z)] = 1; E += d; }
      if (E < bestE - 1e-9) { bestE = E; memcpy(bx, cx, sizeof(int) * N); memcpy(by, cy, sizeof(int) * N); memcpy(bz, cz, sizeof(int) * N); } } }
  FILE *o = fopen(argv[4], "w"); for (int i = 0; i < N; i++) fprintf(o, "%d %d %d\n", bx[i], by[i], bz[i]); fclose(o);
  printf("N=%d best %.6f (%d restarts)\n", N, bestE, restarts); return 0; }
