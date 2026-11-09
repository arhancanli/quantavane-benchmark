/* Most degenerate RNA sequences under base-pair maximization (our own code, Quantavane Originals).
   Model: letters A C G U; pairs AU, UA, GC, CG, GU, UG; a pair (i, j) needs j - i >= 4 (hairpin of >= 3); structures
   are non-crossing sets of pairs. N(s) = number of structures with the most pairs. D(n) = max over sequences of N(s).
   cc -O2 -o nussdeg nussdeg.c ; ./nussdeg exhaustive NMAX    every sequence of length n (n <= 14), sequence and its
                                                              reversal counted once
                                 ./nussdeg anneal N SECONDS SEED      local search on sequences (single-letter changes)
   N(s) by dynamic programming over intervals, splitting on the partner of the first base (each structure once). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
static int ok[4][4];
static int best[64][64]; static unsigned long long cnt[64][64];
static unsigned long long degen(const int *s, int n, int *pairs) {
  for (int len = 0; len <= n; len++) for (int i = 0; i + len <= n; i++) {
    int j = i + len - 1;   /* interval [i, j], empty when len = 0 */
    if (len == 0) { best[i][i] = 0; cnt[i][i] = 1; continue; }   /* stored at [i][i] for empty [i, i-1] */
  }
  /* use b(i, j) for interval [i, j] with j >= i - 1; store at index [i][j+1] */
  for (int i = 0; i <= n; i++) { best[i][i] = 0; cnt[i][i] = 1; }
  for (int len = 1; len <= n; len++) for (int i = 0; i + len <= n; i++) {
    int e = i + len;  /* interval [i, e) */
    int bb = best[i + 1][e]; unsigned long long cc = cnt[i + 1][e];
    for (int k = i + 4; k < e; k++) if (ok[s[i]][s[k]]) {
      int v = 1 + best[i + 1][k] + best[k + 1][e]; unsigned long long c = cnt[i + 1][k] * cnt[k + 1][e];
      if (v > bb) { bb = v; cc = c; } else if (v == bb) cc += c;
    }
    best[i][e] = bb; cnt[i][e] = cc;
  }
  *pairs = best[0][n]; return cnt[0][n];
}
static unsigned long long rs = 88172645463325252ULL; static unsigned long long xr(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static const char L[] = "ACGU";
int main(int argc, char **argv) {
  /* A0 C1 G2 U3 */
  ok[0][3] = ok[3][0] = ok[1][2] = ok[2][1] = ok[2][3] = ok[3][2] = 1;
  if (!strcmp(argv[1], "exhaustive")) {
    int nmax = atoi(argv[2]);
    for (int n = 1; n <= nmax; n++) {
      int s[64]; unsigned long long bestc = 0; int bestp = 0; long long arg = 0;
      for (long long code = 0; code < (1LL << (2 * n)); code++) {
        for (int i = 0; i < n; i++) s[i] = (code >> (2 * i)) & 3;
        int p; unsigned long long c = degen(s, n, &p);
        if (c > bestc) { bestc = c; bestp = p; arg = code; }
      }
      printf("%d %llu ", n, bestc); for (int i = 0; i < n; i++) putchar(L[(arg >> (2 * i)) & 3]); printf(" (pairs %d)\n", bestp); fflush(stdout);
    }
    return 0;
  }
  int n = atoi(argv[2]); double secs = atof(argv[3]); rs ^= (unsigned long long)atoll(argv[4]) * 2654435761ULL;
  int s[64], bs[64]; unsigned long long bc = 0; time_t t0 = time(NULL);
  while (difftime(time(NULL), t0) < secs) {
    for (int i = 0; i < n; i++) s[i] = xr() & 3;
    int p; unsigned long long c = degen(s, n, &p); double T = 1.0;
    for (int it = 0; it < 200000; it++) {
      int i = xr() % n, old = s[i]; s[i] = (old + 1 + xr() % 3) & 3;
      unsigned long long c2 = degen(s, n, &p);
      double d = log((double)c2 + 1) - log((double)c + 1);
      if (d >= 0 || exp(d / T) > (xr() >> 11) * (1.0 / 9007199254740992.0)) { c = c2; if (c > bc) { bc = c; memcpy(bs, s, sizeof(int) * n); } }
      else s[i] = old;
      T *= 0.99997; if (T < 0.01) T = 0.01;
    }
  }
  int p; degen(bs, n, &p);
  printf("%d %llu ", n, bc); for (int i = 0; i < n; i++) putchar(L[bs[i]]); printf(" (pairs %d)\n", p);
  return 0;
}
