/* Two-colourings of 1..N with no monochromatic triple x^2 + xy + y^2 = z^2 (our own code, Quantavane Originals,
   problem eisenstein-triples). Focused random walk on the triples (WalkSAT-style): pick a monochromatic triple, flip
   the member whose flip makes the fewest other triples monochromatic (or, with probability 0.4, a random member).
   cc -O2 -o eiswalk eiswalk.c -lm
   ./eiswalk NMAX STEP SECONDS SEED OUT [START]   grows N by STEP from STEP (or from the colouring in START, a file
                                                 "N" then the string) while a valid colouring is found within SECONDS
                                                 per value of N; OUT always holds the last valid colouring. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
typedef struct { int a, b, c; } T;
static T *t; static int nt, **occ, *nocc; static char *col;
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int mono(int i) { return col[t[i].a] == col[t[i].b] && col[t[i].b] == col[t[i].c]; }
int main(int argc, char **argv) {
  int NMAX = atoi(argv[1]), STEP = atoi(argv[2]); double secs = atof(argv[3]); rs ^= (unsigned long long)atoi(argv[4]) * 2654435761ULL;
  int cap = 1 << 20; t = malloc(sizeof(T) * cap); nt = 0;
  for (long x = 1; x <= NMAX; x++) for (long y = x + 1; y <= NMAX; y++) { long z2 = x * x + x * y + y * y; if (z2 > (long)NMAX * NMAX) break;
    long z = (long)sqrt((double)z2); while (z * z > z2) z--; while ((z + 1) * (z + 1) <= z2) z++;
    if (z * z == z2) { if (nt == cap) { cap *= 2; t = realloc(t, sizeof(T) * cap); } t[nt].a = x; t[nt].b = y; t[nt].c = z; nt++; } }
  int *cnt = calloc(NMAX + 2, sizeof(int)), *pos = calloc(NMAX + 2, sizeof(int)); T *s2 = malloc(sizeof(T) * nt);
  for (int i = 0; i < nt; i++) cnt[t[i].c]++; for (int z = 1; z <= NMAX; z++) pos[z] = pos[z - 1] + cnt[z - 1];
  for (int i = 0; i < nt; i++) s2[pos[t[i].c]++] = t[i]; t = s2;
  nocc = calloc(NMAX + 1, sizeof(int)); for (int i = 0; i < nt; i++) { nocc[t[i].a]++; nocc[t[i].b]++; nocc[t[i].c]++; }
  occ = malloc(sizeof(int *) * (NMAX + 1)); for (int v = 0; v <= NMAX; v++) { occ[v] = malloc(sizeof(int) * (nocc[v] + 1)); nocc[v] = 0; }
  col = calloc(NMAX + 1, 1); for (int v = 1; v <= NMAX; v++) col[v] = rnd() & 1;
  int N = STEP;
  if (argc > 6) { FILE *f = fopen(argv[6], "r"); int n0; char *buf = malloc(NMAX + 16);
    if (fscanf(f, "%d %s", &n0, buf) == 2) { for (int v = 1; v <= n0; v++) col[v] = buf[v - 1] - '0'; N = n0 + STEP; } fclose(f); }
  int active = 0, *bad = malloc(sizeof(int) * nt), *where = malloc(sizeof(int) * nt), nb = 0, lastgood = 0;
  while (N <= NMAX) {
    while (active < nt && t[active].c <= N) { int i = active++; occ[t[i].a][nocc[t[i].a]++] = i; occ[t[i].b][nocc[t[i].b]++] = i; occ[t[i].c][nocc[t[i].c]++] = i; }
    nb = 0; for (int i = 0; i < active; i++) { where[i] = -1; if (mono(i)) { where[i] = nb; bad[nb++] = i; } }
    clock_t st = clock(); long steps = 0;
    while (nb > 0 && (double)(clock() - st) / CLOCKS_PER_SEC < secs) {
      int i = bad[rnd() % nb], vs[3] = {t[i].a, t[i].b, t[i].c}, pick = -1, bestbr = 1 << 30;
      for (int k = 0; k < 3; k++) { int v = vs[k], br = 0; col[v] ^= 1; for (int j = 0; j < nocc[v]; j++) if (mono(occ[v][j])) br++; col[v] ^= 1; if (br < bestbr) { bestbr = br; pick = v; } }
      if (bestbr > 0 && rnd() % 100 < 40) pick = vs[rnd() % 3];
      int v = pick; col[v] ^= 1; steps++;
      for (int j = 0; j < nocc[v]; j++) { int q = occ[v][j], m = mono(q);
        if (m && where[q] < 0) { where[q] = nb; bad[nb++] = q; }
        else if (!m && where[q] >= 0) { int w = where[q], last = bad[--nb]; bad[w] = last; where[last] = w; where[q] = -1; } } }
    if (nb > 0) { printf("N=%d: %d monochromatic triples left; last valid N=%d\n", N, nb, lastgood); break; }
    lastgood = N; printf("N=%d valid (%d triples, %ld flips)\n", N, active, steps); fflush(stdout);
    FILE *o = fopen(argv[5], "w"); fprintf(o, "%d\n", N); for (int v = 1; v <= N; v++) fputc('0' + col[v], o); fputc('\n', o); fclose(o);
    N += STEP; }
  return 0; }
