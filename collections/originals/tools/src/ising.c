/* Ising ground states for the Quantavane Originals (our own code).
   cc -O2 -o ising ising.c
   ./ising exact FILE           every configuration with s_0 = +1 (Gray code), n <= 40: the minimum and its count
   ./ising anneal FILE SWEEPS RESTARTS SEED     simulated annealing, then single-flip descent; best found
   FILE: n, then the n x n integer coupling matrix J (symmetric, zero diagonal), then optionally n integer fields h.
   Energy E(s) = sum_{i<j} J_ij s_i s_j + sum_i h_i s_i, s_i = +1 or -1 (fields break the global flip; with fields the
   exact mode runs over all 2^n configurations). Prints "E <min>" and the configuration as a string of + and -. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static int n; static long long *J; static long long *h; static int hasfield;
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long xr(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double ur(void) { return (xr() >> 11) * (1.0 / 9007199254740992.0); }

static long long energy(const int *s) {
  long long e = 0;
  for (int i = 0; i < n; i++) { for (int j = i + 1; j < n; j++) e += J[i * n + j] * s[i] * s[j]; if (hasfield) e += h[i] * s[i]; }
  return e;
}
static void show(long long e, const int *s) { printf("E %lld\n", e); for (int i = 0; i < n; i++) putchar(s[i] > 0 ? '+' : '-'); putchar('\n'); }

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage\n"); return 2; }
  FILE *f = fopen(argv[2], "r"); if (!f) return 2;
  if (fscanf(f, "%d", &n) != 1) return 2;
  J = calloc((size_t)n * n, sizeof(long long)); h = calloc(n, sizeof(long long));
  for (int i = 0; i < n * n; i++) if (fscanf(f, "%lld", &J[i]) != 1) return 2;
  hasfield = 1; for (int i = 0; i < n; i++) if (fscanf(f, "%lld", &h[i]) != 1) { hasfield = 0; break; }
  if (!hasfield) memset(h, 0, sizeof(long long) * n);
  fclose(f);
  int *s = malloc(sizeof(int) * n), *best = malloc(sizeof(int) * n);
  long long *loc = malloc(sizeof(long long) * n);
  if (!strcmp(argv[1], "exact")) {
    int m = hasfield ? n : n - 1;   /* spins varied: all, or all but s_0 */
    for (int i = 0; i < n; i++) s[i] = 1;
    long long e = energy(s), be = e; unsigned long long cnt = 1; memcpy(best, s, sizeof(int) * n);
    for (int i = 0; i < n; i++) { loc[i] = hasfield ? h[i] : 0; for (int j = 0; j < n; j++) if (j != i) loc[i] += J[i * n + j] * s[j]; }
    for (unsigned long long g = 1; g < (1ULL << m); g++) {
      int k = __builtin_ctzll(g) + (hasfield ? 0 : 1);
      e -= 2 * s[k] * loc[k];
      s[k] = -s[k];
      for (int j = 0; j < n; j++) if (j != k) loc[j] += 2 * J[j * n + k] * s[k];
      if (e < be) { be = e; cnt = 1; memcpy(best, s, sizeof(int) * n); } else if (e == be) cnt++;
    }
    show(be, best); printf("ground states with s_0 = +1 (or all, with fields): %llu\n", cnt);
    return 0;
  }
  long long sweeps = atoll(argv[3]); int restarts = atoi(argv[4]); rs ^= (unsigned long long)atoll(argv[5]) * 2654435761ULL;
  long long maxabs = 1; for (int i = 0; i < n * n; i++) if (llabs(J[i]) > maxabs) maxabs = llabs(J[i]);
  long long be = 0; int have = 0;
  for (int r = 0; r < restarts; r++) {
    for (int i = 0; i < n; i++) s[i] = (xr() & 1) ? 1 : -1;
    for (int i = 0; i < n; i++) { loc[i] = h[i]; for (int j = 0; j < n; j++) if (j != i) loc[i] += J[i * n + j] * s[j]; }
    long long e = energy(s), le = e; int *ls = malloc(sizeof(int) * n); memcpy(ls, s, sizeof(int) * n);
    double T0 = 2.0 * maxabs * sqrt((double)n), T1 = 0.05 * maxabs;
    for (long long t = 0; t < sweeps; t++) {
      double T = T0 * pow(T1 / T0, (double)t / (sweeps > 1 ? sweeps - 1 : 1));
      for (int q = 0; q < n; q++) {
        int k = (int)(xr() % n); long long d = -2 * s[k] * loc[k];
        if (d <= 0 || ur() < exp(-d / T)) {
          s[k] = -s[k]; e += d;
          for (int j = 0; j < n; j++) if (j != k) loc[j] += 2 * J[j * n + k] * s[k];
          if (e < le) { le = e; memcpy(ls, s, sizeof(int) * n); }
        }
      }
    }
    memcpy(s, ls, sizeof(int) * n); e = le;     /* descent from the best state */
    for (int i = 0; i < n; i++) { loc[i] = h[i]; for (int j = 0; j < n; j++) if (j != i) loc[i] += J[i * n + j] * s[j]; }
    for (int improved = 1; improved;) { improved = 0;
      for (int k = 0; k < n; k++) { long long d = -2 * s[k] * loc[k]; if (d < 0) { s[k] = -s[k]; e += d; improved = 1;
        for (int j = 0; j < n; j++) if (j != k) loc[j] += 2 * J[j * n + k] * s[k]; } } }
    if (!have || e < be) { be = e; memcpy(best, s, sizeof(int) * n); have = 1; }
    free(ls);
  }
  if (energy(best) != be) { fprintf(stderr, "energy mismatch\n"); return 1; }
  show(be, best);
  return 0;
}
