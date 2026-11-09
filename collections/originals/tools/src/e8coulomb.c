/* Charges on the roots of E8 with the eight-dimensional Coulomb potential 1/r^6 (our own code, Quantavane Originals, problem e8-coulomb).
   Roots doubled to integers: (+-2,+-2,0^6) and (+-1)^8 with an even number of minus signs; for roots of norm 2 the
   squared distance is 4 - 2<x,y> in {2,4,6,8}, so a pair costs 1/8, 1/64, 1/216 or 1/512 (scaled by 13824: 1728, 216,
   64, 27).
   cc -O2 -o e8coulomb e8coulomb.c -lm; ./e8coulomb N SECONDS SEED OUT
   simulated annealing over N-subsets (swap a chosen root for an unchosen one, energy changes from per-root fields),
   restarts until the time is up; the best subset goes to OUT as N lines of eight doubled coordinates. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
static int R[240][8], ip[240][240], W[240][240];
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double ur(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
int main(int argc, char **argv) {
  int n = 0;
  for (int i = 0; i < 8; i++) for (int j = i + 1; j < 8; j++) for (int a = -1; a <= 1; a += 2) for (int b = -1; b <= 1; b += 2) { memset(R[n], 0, sizeof R[n]); R[n][i] = 2 * a; R[n][j] = 2 * b; n++; }
  for (int m = 0; m < 256; m++) if (__builtin_popcount(m) % 2 == 0) { for (int k = 0; k < 8; k++) R[n][k] = (m >> k & 1) ? -1 : 1; n++; }
  for (int i = 0; i < 240; i++) for (int j = 0; j < 240; j++) { int s = 0; for (int k = 0; k < 8; k++) s += R[i][k] * R[j][k]; ip[i][j] = s / 4;
    W[i][j] = i == j ? 0 : (s / 4 == 1 ? 1728 : s / 4 == 0 ? 216 : s / 4 == -1 ? 64 : 27); }
  int N = atoi(argv[1]); double secs = atof(argv[2]); rs ^= (unsigned long long)atoll(argv[3]) * 2654435761ULL;
  static int in[240], mem[240], non[240], pos[240], best[240]; static long f[240]; long bestE = 1L << 60; clock_t st = clock(); int restarts = 0;
  while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) { restarts++;
    int perm[240]; for (int i = 0; i < 240; i++) perm[i] = i; for (int i = 239; i > 0; i--) { int j = rnd() % (i + 1); int t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
    for (int i = 0; i < 240; i++) in[perm[i]] = i < N;
    int nm = 0, nn = 0; for (int i = 0; i < 240; i++) { if (in[i]) { pos[i] = nm; mem[nm++] = i; } else { pos[i] = nn; non[nn++] = i; } }
    for (int v = 0; v < 240; v++) { f[v] = 0; for (int k = 0; k < nm; k++) f[v] += W[v][mem[k]]; }
    long E = 0; for (int k = 0; k < nm; k++) E += f[mem[k]]; E /= 2;
    double T = 400; long steps = 200000;
    for (long s = 0; s < steps; s++, T *= 0.99996) {
      int a = mem[rnd() % nm], b = non[rnd() % nn]; long d = f[b] - W[a][b] - f[a];
      if (d <= 0 || ur() < exp(-d / T)) { E += d; for (int v = 0; v < 240; v++) f[v] += W[v][b] - W[v][a];
        int pa = pos[a], pb = pos[b]; mem[pa] = b; pos[b] = pa; non[pb] = a; pos[a] = pb; in[a] = 0; in[b] = 1;
        if (E < bestE) { bestE = E; memcpy(best, in, sizeof in); } } } }
  int c[5] = {0}; for (int i = 0; i < 240; i++) if (best[i]) for (int j = i + 1; j < 240; j++) if (best[j]) c[ip[i][j] + 2]++;
  printf("N %d E*13824 %ld = %.9f  pairs ip1 %d ip0 %d ip-1 %d ip-2 %d (%d restarts)\n", N, bestE, bestE / 13824.0, c[3], c[2], c[1], c[0], restarts);
  if (argc > 4) { FILE *o = fopen(argv[4], "w"); for (int i = 0; i < 240; i++) if (best[i]) { for (int k = 0; k < 8; k++) fprintf(o, "%d%c", R[i][k], k < 7 ? ' ' : '\n'); } fclose(o); }
  return 0; }
