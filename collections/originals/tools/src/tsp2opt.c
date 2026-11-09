/* Tours for the sunflower instances: greedy-edge start, then 2-opt and Or-opt with neighbour lists (our own code).
   cc -O2 -o tsp2opt tsp2opt.c -lm ; ./tsp2opt INSTANCE.txt SECONDS SEED OUT.txt
   Distances are the Euclidean distances rounded to the nearest integer (as TSPLIB EUC_2D). Writes the tour (1-based
   point numbers, one per line) and prints its length. Our own implementation; upper bounds only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define K 10
static int n; static double *X, *Y; static int *nb; static int *tour, *pos;
static long long dist(int a, int b) { double dx = X[a] - X[b], dy = Y[a] - Y[b]; return (long long)floor(sqrt(dx * dx + dy * dy) + 0.5); }
static unsigned long long rs = 88172645463325252ULL; static unsigned long long xr(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static void reverse(int i, int j) { /* reverse tour[i..j] (indices mod n, i before j going forward) */
  int len = (j - i + n) % n + 1;
  for (int s = 0; s < len / 2; s++) { int a = (i + s) % n, b = (j - s + n) % n; int t = tour[a]; tour[a] = tour[b]; tour[b] = t; pos[tour[a]] = a; pos[tour[b]] = b; }
}
static long long length(void) { long long L = 0; for (int i = 0; i < n; i++) L += dist(tour[i], tour[(i + 1) % n]); return L; }
static int cmpd_base; static int cmpd(const void *a, const void *b) { long long x = dist(cmpd_base, *(int *)a), y = dist(cmpd_base, *(int *)b); return (x > y) - (x < y); }
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r"); char line[256];
  while (fgets(line, sizeof line, f) && line[0] == '#') ;
  n = atoi(line); X = malloc(sizeof(double) * n); Y = malloc(sizeof(double) * n);
  for (int i = 0; i < n; i++) { int k; long xx, yy; if (fscanf(f, "%d %ld %ld", &k, &xx, &yy) != 3) return 2; X[i] = xx; Y[i] = yy; }
  fclose(f);
  double secs = atof(argv[2]); rs ^= (unsigned long long)atoll(argv[3]) * 2654435761ULL;
  /* neighbour lists: K nearest by a grid */
  nb = malloc(sizeof(int) * n * K);
  { int G = (int)sqrt(n / 2.0) + 1; double mnx = 1e18, mny = 1e18, mxx = -1e18, mxy = -1e18;
    for (int i = 0; i < n; i++) { if (X[i] < mnx) mnx = X[i]; if (Y[i] < mny) mny = Y[i]; if (X[i] > mxx) mxx = X[i]; if (Y[i] > mxy) mxy = Y[i]; }
    int *head = malloc(sizeof(int) * G * G), *nxt = malloc(sizeof(int) * n); for (int c = 0; c < G * G; c++) head[c] = -1;
    double cw = (mxx - mnx) / G + 1e-9, ch = (mxy - mny) / G + 1e-9;
    for (int i = 0; i < n; i++) { int cx = (int)((X[i] - mnx) / cw), cy = (int)((Y[i] - mny) / ch); if (cx >= G) cx = G - 1; if (cy >= G) cy = G - 1; nxt[i] = head[cy * G + cx]; head[cy * G + cx] = i; }
    int *cand = malloc(sizeof(int) * n);
    for (int i = 0; i < n; i++) {
      int cx = (int)((X[i] - mnx) / cw), cy = (int)((Y[i] - mny) / ch); if (cx >= G) cx = G - 1; if (cy >= G) cy = G - 1;
      int nc = 0;
      for (int r = 1; nc < 4 * K && r < G + 2; r++) { nc = 0;
        for (int yy = cy - r; yy <= cy + r; yy++) for (int xx = cx - r; xx <= cx + r; xx++) { if (xx < 0 || yy < 0 || xx >= G || yy >= G) continue;
          for (int j = head[yy * G + xx]; j >= 0; j = nxt[j]) if (j != i) cand[nc++] = j; } }
      cmpd_base = i; qsort(cand, nc, sizeof(int), cmpd);
      for (int t = 0; t < K; t++) nb[i * K + t] = cand[t < nc ? t : nc - 1];
    }
  }
  /* nearest-neighbour start */
  tour = malloc(sizeof(int) * n); pos = malloc(sizeof(int) * n); char *used = calloc(n, 1);
  int cur = 0; used[0] = 1; tour[0] = 0;
  for (int i = 1; i < n; i++) { int best = -1; for (int t = 0; t < K; t++) { int c = nb[cur * K + t]; if (!used[c]) { best = c; break; } }
    if (best < 0) { long long bd = -1; for (int c = 0; c < n; c++) if (!used[c]) { long long d = dist(cur, c); if (bd < 0 || d < bd) { bd = d; best = c; } } }
    tour[i] = best; used[best] = 1; cur = best; }
  for (int i = 0; i < n; i++) pos[tour[i]] = i;
  time_t t0 = time(NULL); long long L = length();
  int improved = 1;
  while (improved && difftime(time(NULL), t0) < secs) {
    improved = 0;
    for (int a = 0; a < n; a++) {   /* 2-opt: edge (a, succ a) with (c, succ c), c a neighbour of a */
      int pa = pos[a], sa = tour[(pa + 1) % n];
      for (int t = 0; t < K; t++) { int c = nb[a * K + t]; int pc = pos[c], sc = tour[(pc + 1) % n];
        if (c == sa || sc == a) continue;
        long long delta = dist(a, c) + dist(sa, sc) - dist(a, sa) - dist(c, sc);
        if (delta < 0) { reverse((pa + 1) % n, pc); L += delta; improved = 1; break; } }
    }
    for (int a = 0; a < n; a++) {   /* Or-opt: move a segment of 1-3 points next to a neighbour */
      for (int seg = 1; seg <= 3; seg++) {
        int pa = pos[a]; int s0 = a, s1 = tour[(pa + seg - 1) % n]; int pr = tour[(pa - 1 + n) % n], nx = tour[(pa + seg) % n];
        long long rem = dist(pr, s0) + dist(s1, nx) - dist(pr, nx);
        for (int t = 0; t < K; t++) { int c = nb[a * K + t]; int pc = pos[c]; int off = (pc - pa + n) % n; if (off < seg + 1 && off != seg) continue; if (off == seg) continue;
          int d = tour[(pc + 1) % n]; if (d == s0) continue;
          long long add1 = dist(c, s1) + dist(s0, d) - dist(c, d);   /* insert reversed: c s1 ... s0 d */
          long long add2 = dist(c, s0) + dist(s1, d) - dist(c, d);   /* insert forward: c s0 ... s1 d */
          long long best = add1 < add2 ? add1 : add2;
          if (best - rem < 0) {
            /* rebuild by extracting the segment (simple O(n) move) */
            int *nt = malloc(sizeof(int) * n), k = 0; int segv[3]; for (int q = 0; q < seg; q++) segv[q] = tour[(pa + q) % n];
            for (int q = 0; q < n; q++) { int v = tour[(pa + seg + q) % n]; if (q >= n - seg) break; nt[k++] = v;
              if (v == c) { if (add1 <= add2) for (int z = seg - 1; z >= 0; z--) nt[k++] = segv[z]; else for (int z = 0; z < seg; z++) nt[k++] = segv[z]; } }
            memcpy(tour, nt, sizeof(int) * n); free(nt); for (int q = 0; q < n; q++) pos[tour[q]] = q;
            L += best - rem; improved = 1; break; }
        }
      }
    }
  }
  /* random restarts of segment perturbation (double bridge) with 2-opt repair until time runs out */
  long long bestL = length(); int *bestT = malloc(sizeof(int) * n); memcpy(bestT, tour, sizeof(int) * n);
  while (difftime(time(NULL), t0) < secs) {
    int i = (int)(xr() % n), len = 30 + (int)(xr() % 50); if (len >= n) break;
    int j = (i + len) % n; reverse(i, j);   /* local scramble */
    for (int rep = 0, imp = 1; imp && rep < 50; rep++) { imp = 0;
      for (int q = 0; q < len + 20; q++) { int a = tour[(i - 10 + q + n) % n]; int pa = pos[a], sa = tour[(pa + 1) % n];
        for (int t = 0; t < K; t++) { int c = nb[a * K + t]; int pc = pos[c], sc = tour[(pc + 1) % n]; if (c == sa || sc == a) continue;
          long long delta = dist(a, c) + dist(sa, sc) - dist(a, sa) - dist(c, sc); if (delta < 0) { reverse((pa + 1) % n, pc); imp = 1; break; } } } }
    long long L2 = length();
    if (L2 < bestL) { bestL = L2; memcpy(bestT, tour, sizeof(int) * n); } else { memcpy(tour, bestT, sizeof(int) * n); for (int q = 0; q < n; q++) pos[tour[q]] = q; }
  }
  FILE *o = fopen(argv[4], "w"); fprintf(o, "# tour of length %lld\n", bestL); for (int i = 0; i < n; i++) fprintf(o, "%d\n", bestT[i] + 1); fclose(o);
  printf("%d %lld\n", n, bestL); return 0;
}
