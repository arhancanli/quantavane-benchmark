/* Slew tours of a star catalogue for an equatorial mount (our own code, Quantavane Originals).
   cc -O2 -o tspmount tspmount.c ; ./tspmount bsc-sky.txt SECONDS SEED OUT.txt
   Distance between stars: max(dRA, dDec) in half arcseconds, dRA the hour-angle turn the right-ascension axis makes
   (the shorter way round, |RA difference| or 2,592,000 minus it) and dDec the declination turn, both axes turning at
   the same rate (bsc-sky.txt: RA in tenths of a second of time = 3 half arcseconds, Dec in arcseconds = 2 half
   arcseconds). Nearest-neighbour start, then 2-opt and Or-opt with 12-nearest-neighbour lists, then iterated local
   search with random double-bridge kicks kept when the tour gets shorter. Writes the tour (HR numbers, one per line)
   and prints its length. Upper bounds only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define K 12
#define FULL 2592000LL
static int n, *hr, *tour, *pos, (*nb)[K]; static long long *ra, *de;
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static long long dist(int a, int b) { long long d = ra[a] - ra[b]; if (d < 0) d = -d; if (FULL - d < d) d = FULL - d;
  long long e = de[a] - de[b]; if (e < 0) e = -e; return d > e ? d : e; }
static long long length(void) { long long L = 0; for (int i = 0; i < n; i++) L += dist(tour[i], tour[(i + 1) % n]); return L; }
static void reverse(int i, int j) { /* reverse tour[i..j] (cyclic indices, i to j forward) */
  int len = j - i; if (len < 0) len += n; len++;
  for (int k = 0; k < len / 2; k++) { int a = (i + k) % n, b = (j - k + n) % n; int t = tour[a]; tour[a] = tour[b]; tour[b] = t; pos[tour[a]] = a; pos[tour[b]] = b; } }
static int localopt(void) { int any = 0, imp = 1;
  while (imp) { imp = 0;
    for (int a = 0; a < n; a++) { int pa = pos[a], sa = tour[(pa + 1) % n];
      for (int k = 0; k < K; k++) { int c = nb[a][k]; int pc = pos[c], sc = tour[(pc + 1) % n]; if (c == sa || sc == a) continue;
        long long delta = dist(a, c) + dist(sa, sc) - dist(a, sa) - dist(c, sc);
        if (delta < 0) { reverse((pa + 1) % n, pc); imp = any = 1; break; } } }
    for (int a = 0; a < n; a++) for (int seg = 1; seg <= 3; seg++) { int pa = pos[a]; int s0 = a, s1 = tour[(pa + seg - 1) % n];
        int pr = tour[(pa - 1 + n) % n], nx = tour[(pa + seg) % n]; if (nx == s0 || pr == s1) continue;
        long long rem = dist(pr, s0) + dist(s1, nx) - dist(pr, nx);
        for (int k = 0; k < K; k++) { int c = nb[a][k]; int pc = pos[c]; int inside = 0; for (int t = 0; t < seg; t++) if (tour[(pa + t) % n] == c) inside = 1;
          if (inside || c == pr) continue; int d = tour[(pc + 1) % n]; int insd = 0; for (int t = 0; t < seg; t++) if (tour[(pa + t) % n] == d) insd = 1; if (insd) continue;
          long long add1 = dist(c, s1) + dist(s0, d) - dist(c, d), add2 = dist(c, s0) + dist(s1, d) - dist(c, d);
          if (add1 < rem || add2 < rem) { int seglist[3]; for (int t = 0; t < seg; t++) seglist[t] = tour[(pa + t) % n];
            int *nt = malloc(sizeof(int) * n), m = 0; for (int t = 0; t < n; t++) { int v = tour[t]; int skip = 0; for (int u = 0; u < seg; u++) if (v == seglist[u]) skip = 1; if (skip) continue;
              nt[m++] = v; if (v == c) { if (add1 < add2) for (int u = seg - 1; u >= 0; u--) nt[m++] = seglist[u]; else for (int u = 0; u < seg; u++) nt[m++] = seglist[u]; } }
            memcpy(tour, nt, sizeof(int) * n); free(nt); for (int t = 0; t < n; t++) pos[tour[t]] = t; imp = any = 1; break; } } } }
  return any; }
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r"); double secs = atof(argv[2]); rs ^= (unsigned long long)atoi(argv[3]) * 2654435761ULL;
  char line[256]; int cap = 10000; hr = malloc(sizeof(int) * cap); ra = malloc(sizeof(long long) * cap); de = malloc(sizeof(long long) * cap); n = 0;
  while (fgets(line, sizeof line, f)) { if (line[0] == '#') continue; long long r, d; int h, v; if (sscanf(line, "%d %lld %lld %d", &h, &r, &d, &v) == 4) { hr[n] = h; ra[n] = 3 * r; de[n] = 2 * d; n++; } }
  tour = malloc(sizeof(int) * n); pos = malloc(sizeof(int) * n); nb = malloc(sizeof(*nb) * n);
  long long *bd = malloc(sizeof(long long) * K);
  for (int a = 0; a < n; a++) { int cnt = 0; for (int b = 0; b < n; b++) { if (b == a) continue; long long d = dist(a, b);
      if (cnt < K) { int i = cnt++; while (i > 0 && bd[i - 1] > d) { bd[i] = bd[i - 1]; nb[a][i] = nb[a][i - 1]; i--; } bd[i] = d; nb[a][i] = b; }
      else if (d < bd[K - 1]) { int i = K - 1; while (i > 0 && bd[i - 1] > d) { bd[i] = bd[i - 1]; nb[a][i] = nb[a][i - 1]; i--; } bd[i] = d; nb[a][i] = b; } } }
  char *used = calloc(n, 1); int cur = 0; used[0] = 1; tour[0] = 0;
  for (int i = 1; i < n; i++) { int best = -1; for (int k = 0; k < K; k++) if (!used[nb[cur][k]]) { best = nb[cur][k]; break; }
    if (best < 0) { long long b2 = -1; for (int c = 0; c < n; c++) if (!used[c]) { long long d = dist(cur, c); if (b2 < 0 || d < b2) { b2 = d; best = c; } } }
    tour[i] = best; used[best] = 1; cur = best; }
  for (int i = 0; i < n; i++) pos[tour[i]] = i;
  localopt(); long long L = length(); printf("local optimum %lld\n", L); fflush(stdout);
  int *bestt = malloc(sizeof(int) * n); memcpy(bestt, tour, sizeof(int) * n); long long bestL = L;
  clock_t st = clock(); long kicks = 0;
  while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) { kicks++;
    int i = rnd() % n, len = 30 + rnd() % 200; /* double bridge inside a window */
    int p1 = i, p2 = (i + 1 + rnd() % (len / 3)) % n, p3 = (p2 + 1 + rnd() % (len / 3)) % n, p4 = (p3 + 1 + rnd() % (len / 3)) % n;
    int *nt = malloc(sizeof(int) * n), m = 0; int idx[4] = {p1, p2, p3, p4}; (void)idx;
    /* segments A = (p4+1 .. p1), B = (p1+1 .. p2), C = (p2+1 .. p3), D = (p3+1 .. p4); new order A C B D */
    for (int t = (p4 + 1) % n;; t = (t + 1) % n) { nt[m++] = tour[t]; if (t == p1) break; }
    for (int t = (p2 + 1) % n;; t = (t + 1) % n) { nt[m++] = tour[t]; if (t == p3) break; }
    for (int t = (p1 + 1) % n;; t = (t + 1) % n) { nt[m++] = tour[t]; if (t == p2) break; }
    for (int t = (p3 + 1) % n;; t = (t + 1) % n) { nt[m++] = tour[t]; if (t == p4) break; }
    if (m != n) { free(nt); continue; }
    memcpy(tour, nt, sizeof(int) * n); free(nt); for (int t = 0; t < n; t++) pos[tour[t]] = t;
    localopt(); L = length();
    if (L < bestL) { bestL = L; memcpy(bestt, tour, sizeof(int) * n); printf("  %lld after %ld kicks\n", bestL, kicks); fflush(stdout); }
    else { memcpy(tour, bestt, sizeof(int) * n); for (int t = 0; t < n; t++) pos[tour[t]] = t; } }
  FILE *o = fopen(argv[4], "w"); for (int i = 0; i < n; i++) fprintf(o, "%d\n", hr[bestt[i]]); fclose(o);
  printf("best %lld (%ld kicks)\n", bestL, kicks); return 0; }
