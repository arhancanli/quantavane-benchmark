/* Long induced cycles (coils, snake-in-the-box codes) and induced paths (snakes) of a graph by randomised greedy
   growth with restarts (our own code, Quantavane Originals, problem cell120-coil).
   cc -O2 -o coil coil.c ; ./coil EDGES SECONDS SEED OUT.txt
   A path v0 v1 ... vk grows at its tail: the next vertex u is a neighbour of vk outside the path with no neighbour
   among v0 .. v(k-1) (so the path stays induced); among the allowed u the one that blocks the fewest still-free
   vertices is preferred (random ties, and with probability 0.2 a random allowed u). When a neighbour u of vk is
   adjacent to v0 and to no other path vertex but vk, the cycle v0 .. vk u is induced (a coil) and is recorded.
   Writes the longest coil found, one vertex per line, and prints its length and the longest snake. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n, m, *adj[4096], deg[4096];
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r"); double secs = atof(argv[2]); rs ^= (unsigned long long)atoi(argv[3]) * 2654435761ULL;
  if (fscanf(f, "%d %d", &n, &m) != 2) return 2; int *ea = malloc(sizeof(int) * m), *eb = malloc(sizeof(int) * m);
  for (int i = 0; i < m; i++) { if (fscanf(f, "%d %d", &ea[i], &eb[i]) != 2) return 2; deg[ea[i]]++; deg[eb[i]]++; }
  for (int v = 0; v < n; v++) { adj[v] = malloc(sizeof(int) * deg[v]); deg[v] = 0; }
  for (int i = 0; i < m; i++) { adj[ea[i]][deg[ea[i]]++] = eb[i]; adj[eb[i]][deg[eb[i]]++] = ea[i]; }
  int *path = malloc(sizeof(int) * n), *cnt = malloc(sizeof(int) * n), *best = malloc(sizeof(int) * n); char *inP = malloc(n);
  int bestc = 0, bests = 0; clock_t st = clock(); long runs = 0;
  while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) { runs++;
    memset(inP, 0, n); memset(cnt, 0, sizeof(int) * n);   /* cnt[u] = number of path vertices adjacent to u */
    int k = 0, v0 = rnd() % n; path[k++] = v0; inP[v0] = 1; for (int j = 0; j < deg[v0]; j++) cnt[adj[v0][j]]++;
    while (1) { int t = path[k - 1], cand[64], nc = 0, cost[64];
      for (int j = 0; j < deg[t]; j++) { int u = adj[t][j]; if (inP[u]) continue;
        /* u is adjacent to t; allowed if adjacent to no other path vertex */
        int other = cnt[u] - 1; int adj0 = 0; for (int q = 0; q < deg[u]; q++) if (adj[u][q] == v0) adj0 = 1;
        if (k >= 3 && adj0 && other == 1) { /* closes an induced cycle of length k + 1 */
          if (k + 1 > bestc) { bestc = k + 1; memcpy(best, path, sizeof(int) * k); best[k] = u; printf("  coil %d\n", bestc); fflush(stdout); } }
        if (other > 0) continue;
        int c = 0; for (int q = 0; q < deg[u]; q++) { int w = adj[u][q]; if (!inP[w] && cnt[w] == 0) c++; }
        cand[nc] = u; cost[nc++] = c; }
      if (!nc) break;
      int pick; if (rnd() % 100 < 20) pick = rnd() % nc; else { int bc = 1 << 30, ties = 0; pick = 0;
        for (int i = 0; i < nc; i++) { if (cost[i] < bc) { bc = cost[i]; pick = i; ties = 1; } else if (cost[i] == bc && rnd() % (++ties) == 0) pick = i; } }
      int u = cand[pick]; path[k++] = u; inP[u] = 1; for (int q = 0; q < deg[u]; q++) cnt[adj[u][q]]++; }
    if (k > bests) bests = k; }
  FILE *o = fopen(argv[4], "w"); for (int i = 0; i < bestc; i++) fprintf(o, "%d\n", best[i]); fclose(o);
  printf("longest coil %d, longest snake %d vertices (%ld runs)\n", bestc, bests, runs); return 0; }
