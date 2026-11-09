/* Small dominating sets (covering codes of radius 1) of a graph, and a packing lower bound (our own code, Quantavane
   Originals, problem prime-cover).
   cc -O2 -o dominate dominate.c ; ./dominate EDGES SECONDS SEED OUT.txt
   EDGES: "n m" then m lines "u v". Greedy construction (the vertex whose closed neighbourhood covers the most
   uncovered vertices), then iterated local search: remove one to three random code vertices, repair greedily, prune
   redundant vertices; keep the smallest code. Lower bound: vertices pairwise at distance >= 3 (chosen greedily, the
   smallest closed neighbourhoods first) need different code vertices. Writes the code, one vertex number per line. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n, m, **adj, *deg, *cov; static char *in;
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int gain(int v) { int g = !cov[v]; for (int j = 0; j < deg[v]; j++) g += !cov[adj[v][j]]; return g; }
static void add(int v) { in[v] = 1; cov[v]++; for (int j = 0; j < deg[v]; j++) cov[adj[v][j]]++; }
static void del(int v) { in[v] = 0; cov[v]--; for (int j = 0; j < deg[v]; j++) cov[adj[v][j]]--; }
static int removable(int v) { if (cov[v] < 2) return 0; for (int j = 0; j < deg[v]; j++) if (cov[adj[v][j]] < 2) return 0; return 1; }
static void repair(void) { while (1) { int best = -1, bg = 0, ties = 0;
    for (int v = 0; v < n; v++) { if (in[v]) continue; int g = gain(v); if (g > bg) { bg = g; best = v; ties = 1; } else if (g == bg && g > 0 && rnd() % (++ties) == 0) best = v; }
    if (bg == 0) break; add(best); } }
static void prune(void) { int *o = malloc(sizeof(int) * n), k = 0; for (int v = 0; v < n; v++) if (in[v]) o[k++] = v;
  for (int i = k - 1; i > 0; i--) { int j = rnd() % (i + 1), t = o[i]; o[i] = o[j]; o[j] = t; }
  for (int i = 0; i < k; i++) if (removable(o[i])) del(o[i]); free(o); }
static int size(void) { int k = 0; for (int v = 0; v < n; v++) k += in[v]; return k; }
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r"); double secs = atof(argv[2]); rs ^= (unsigned long long)atoi(argv[3]) * 2654435761ULL;
  if (fscanf(f, "%d %d", &n, &m) != 2) return 2; int *ea = malloc(sizeof(int) * m), *eb = malloc(sizeof(int) * m); deg = calloc(n, sizeof(int));
  for (int i = 0; i < m; i++) { if (fscanf(f, "%d %d", &ea[i], &eb[i]) != 2) return 2; deg[ea[i]]++; deg[eb[i]]++; }
  adj = malloc(sizeof(int *) * n); for (int v = 0; v < n; v++) { adj[v] = malloc(sizeof(int) * (deg[v] + 1)); deg[v] = 0; }
  for (int i = 0; i < m; i++) { adj[ea[i]][deg[ea[i]]++] = eb[i]; adj[eb[i]][deg[eb[i]]++] = ea[i]; }
  /* lower bound: greedy 2-packing */
  int *ord = malloc(sizeof(int) * n); char *blk = calloc(n, 1); for (int v = 0; v < n; v++) ord[v] = v;
  for (int i = 1; i < n; i++) { int v = ord[i], j = i; while (j > 0 && deg[ord[j - 1]] > deg[v]) { ord[j] = ord[j - 1]; j--; } ord[j] = v; }
  int lb = 0; for (int i = 0; i < n; i++) { int v = ord[i], ok = !blk[v]; for (int j = 0; j < deg[v] && ok; j++) if (blk[adj[v][j]]) ok = 0;
    if (!ok) continue; lb++; blk[v] = 1; for (int j = 0; j < deg[v]; j++) { int u = adj[v][j]; blk[u] = 1; for (int t = 0; t < deg[u]; t++) blk[adj[u][t]] = 1; } }
  printf("packing lower bound %d\n", lb);
  cov = calloc(n, sizeof(int)); in = calloc(n, 1); repair(); prune(); int best = size(); char *bin = malloc(n); memcpy(bin, in, n);
  printf("greedy %d\n", best); fflush(stdout);
  clock_t st = clock(); long it = 0;
  while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) { it++; int k = size(), r = 1 + rnd() % 3;
    for (int t = 0; t < r; t++) { int v; do v = rnd() % n; while (!in[v]); del(v); }
    repair(); prune(); int s = size();
    if (s < best) { best = s; memcpy(bin, in, n); printf("  %d (iteration %ld)\n", best, it); fflush(stdout); }
    else if (s > k + 1 || (s > k && rnd() % 10)) { memcpy(in, bin, n); memset(cov, 0, sizeof(int) * n);
      for (int v = 0; v < n; v++) if (in[v]) { cov[v]++; for (int j = 0; j < deg[v]; j++) cov[adj[v][j]]++; } } }
  FILE *o = fopen(argv[4], "w"); for (int v = 0; v < n; v++) if (bin[v]) fprintf(o, "%d\n", v); fclose(o);
  printf("best %d (%ld iterations)\n", best, it); return 0; }
