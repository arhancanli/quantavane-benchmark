/* Star-tracker catalogues: fewest stars such that every boresight has at least K chosen stars in its field of view
   (set multicover), by greedy construction and iterated remove-and-repair; also a lower bound (our own code,
   Quantavane Originals).
   cc -O2 -o multicover multicover.c ; ./multicover INSTANCE K SECONDS SEED OUT.txt
   INSTANCE: collections/originals/instances/star-tracker.txt (tools/bsc_instances.py). Writes the chosen HR numbers,
   one per line. Lower bound: boresights whose candidate stars are pairwise disjoint are chosen greedily (fewest
   candidates first); each needs K stars of its own, so K times their number bounds every catalogue from below. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef long long ll;
static int S, B, K, *hr, **sb, *nsb, **bs, *nbs, *cov; static char *in;
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int gain(int s) { int g = 0; for (int j = 0; j < nsb[s]; j++) if (cov[sb[s][j]] < K) g++; return g; }
static void add(int s) { in[s] = 1; for (int j = 0; j < nsb[s]; j++) cov[sb[s][j]]++; }
static void del(int s) { in[s] = 0; for (int j = 0; j < nsb[s]; j++) cov[sb[s][j]]--; }
static int removable(int s) { for (int j = 0; j < nsb[s]; j++) if (cov[sb[s][j]] <= K) return 0; return 1; }
static int deficit(void) { int d = 0; for (int b = 0; b < B; b++) if (cov[b] < K) d += K - cov[b]; return d; }
static void repair(int ban) {
  while (deficit() > 0) { int best = -1, bg = -1, ties = 0;
    for (int s = 0; s < S; s++) { if (in[s] || s == ban) continue; int g = gain(s);
      if (g > bg) { bg = g; best = s; ties = 1; } else if (g == bg && g > 0) { ties++; if (rnd() % ties == 0) best = s; } }
    if (bg <= 0) { if (ban >= 0) { ban = -1; continue; } fprintf(stderr, "infeasible\n"); exit(1); }
    add(best); }
}
static void prune(void) { int *ord = malloc(sizeof(int) * S), n = 0; for (int s = 0; s < S; s++) if (in[s]) ord[n++] = s;
  for (int i = n - 1; i > 0; i--) { int j = rnd() % (i + 1), t = ord[i]; ord[i] = ord[j]; ord[j] = t; }
  for (int i = 0; i < n; i++) if (removable(ord[i])) del(ord[i]); free(ord); }
static int size(void) { int n = 0; for (int s = 0; s < S; s++) n += in[s]; return n; }
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r"); K = atoi(argv[2]); double secs = atof(argv[3]); rs ^= (unsigned long long)atoi(argv[4]) * 2654435761ULL;
  char line[512]; ll T; ll (*sv)[3], (*bv)[3];
  do fgets(line, sizeof line, f); while (line[0] == '#'); sscanf(line, "%lld", &T);
  fgets(line, sizeof line, f); sscanf(line, "%d %d", &S, &B);
  hr = malloc(sizeof(int) * S); sv = malloc(sizeof(*sv) * S); bv = malloc(sizeof(*bv) * B);
  for (int i = 0; i < S; i++) { fgets(line, sizeof line, f); sscanf(line, "%d %lld %lld %lld", &hr[i], &sv[i][0], &sv[i][1], &sv[i][2]); }
  for (int i = 0; i < B; i++) { fgets(line, sizeof line, f); sscanf(line, "%lld %lld %lld", &bv[i][0], &bv[i][1], &bv[i][2]); }
  nsb = calloc(S, sizeof(int)); nbs = calloc(B, sizeof(int)); sb = malloc(sizeof(int *) * S); bs = malloc(sizeof(int *) * B);
  for (int s = 0; s < S; s++) sb[s] = malloc(sizeof(int) * B);
  for (int b = 0; b < B; b++) bs[b] = malloc(sizeof(int) * S);
  for (int s = 0; s < S; s++) for (int b = 0; b < B; b++) {
    __int128 d = (__int128)sv[s][0] * bv[b][0] + (__int128)sv[s][1] * bv[b][1] + (__int128)sv[s][2] * bv[b][2];
    if (d >= T) { sb[s][nsb[s]++] = b; bs[b][nbs[b]++] = s; } }
  /* lower bound: greedy family of boresights with pairwise disjoint candidate lists */
  int *mark = calloc(S, sizeof(int)), *ordb = malloc(sizeof(int) * B), lb = 0;
  for (int b = 0; b < B; b++) ordb[b] = b;
  for (int i = 0; i < B; i++) for (int j = i + 1; j < B; j++) if (nbs[ordb[j]] < nbs[ordb[i]]) { int t = ordb[i]; ordb[i] = ordb[j]; ordb[j] = t; }
  for (int i = 0; i < B; i++) { int b = ordb[i], ok = 1; for (int j = 0; j < nbs[b]; j++) if (mark[bs[b][j]]) { ok = 0; break; }
    if (ok) { lb++; for (int j = 0; j < nbs[b]; j++) mark[bs[b][j]] = 1; } }
  printf("lower bound %d x %d = %d\n", K, lb, K * lb);
  cov = calloc(B, sizeof(int)); in = calloc(S, 1);
  repair(-1); prune(); int best = size(); char *bestin = malloc(S); memcpy(bestin, in, S);
  printf("greedy %d\n", best); fflush(stdout);
  clock_t st = clock(); long it = 0;
  while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) {
    it++; int n = size(), r = 1 + rnd() % 3;
    for (int t = 0; t < r; t++) { int s; do s = rnd() % S; while (!in[s]); del(s); }
    repair(-1); prune();
    int m = size();
    if (m < best) { best = m; memcpy(bestin, in, S); printf("  %d (iteration %ld)\n", best, it); fflush(stdout); }
    else if (m > n + 1 || (m > n && rnd() % 10)) { memcpy(in, bestin, S); memset(cov, 0, sizeof(int) * B);
      for (int s = 0; s < S; s++) if (in[s]) for (int j = 0; j < nsb[s]; j++) cov[sb[s][j]]++; }
  }
  FILE *o = fopen(argv[5], "w"); for (int s = 0; s < S; s++) if (bestin[s]) fprintf(o, "%d\n", hr[s]); fclose(o);
  printf("best %d stars (%ld iterations)\n", best, it); return 0; }
