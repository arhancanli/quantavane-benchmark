/* Small resolving sets (metric dimension) of a graph by local search (our own code, Quantavane Originals,
   problem e8-resolving).
   cc -O2 -o resolve resolve.c ; ./resolve EDGES K SECONDS SEED
   EDGES: "n m" then m lines "u v". For a set W of K vertices, the cost is the number of vertices minus the number of
   distinct distance vectors (d(v, w))_{w in W}; W resolves the graph when the cost is 0. Moves replace one vertex of
   W by the vertex outside W that gives the lowest cost (ties at random, a tabu list on recently removed vertices);
   restarts from random sets. Prints every resolving set found. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n, m, *adj[4096], deg[4096]; static unsigned char D[1200][1200];
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int cmpu(const void *a, const void *b) { unsigned long long x = *(unsigned long long *)a, y = *(unsigned long long *)b; return (x > y) - (x < y); }
static int cost(int *W, int k) { static unsigned long long key[1200];
  for (int v = 0; v < n; v++) { unsigned long long h = 0; for (int i = 0; i < k; i++) h = h * 8 + D[v][W[i]]; key[v] = h; }
  qsort(key, n, sizeof key[0], cmpu); int distinct = 1; for (int v = 1; v < n; v++) if (key[v] != key[v - 1]) distinct++; return n - distinct; }
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r"); int K = atoi(argv[2]); double secs = atof(argv[3]); rs ^= (unsigned long long)atoi(argv[4]) * 2654435761ULL;
  if (fscanf(f, "%d %d", &n, &m) != 2) return 2; int *ea = malloc(sizeof(int) * m), *eb = malloc(sizeof(int) * m);
  for (int i = 0; i < m; i++) { if (fscanf(f, "%d %d", &ea[i], &eb[i]) != 2) return 2; deg[ea[i]]++; deg[eb[i]]++; }
  for (int v = 0; v < n; v++) { adj[v] = malloc(sizeof(int) * deg[v]); deg[v] = 0; }
  for (int i = 0; i < m; i++) { adj[ea[i]][deg[ea[i]]++] = eb[i]; adj[eb[i]][deg[eb[i]]++] = ea[i]; }
  for (int s = 0; s < n; s++) { int q[1200], h = 0, t = 0; memset(D[s], 255, n); D[s][s] = 0; q[t++] = s;
    while (h < t) { int u = q[h++]; for (int j = 0; j < deg[u]; j++) { int w = adj[u][j]; if (D[s][w] == 255) { D[s][w] = D[s][u] + 1; q[t++] = w; } } } }
  int W[64], inW[1200], tabu[1200]; clock_t st = clock(); long it = 0; int found = 0;
  while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) {
    memset(inW, 0, sizeof inW); memset(tabu, 0, sizeof tabu);
    for (int i = 0; i < K;) { int v = rnd() % n; if (!inW[v]) { inW[v] = 1; W[i++] = v; } }
    int c = cost(W, K), bestc = c, stall = 0;
    while (c > 0 && stall < 2000 && (double)(clock() - st) / CLOCKS_PER_SEC < secs) { it++;
      int i = rnd() % K, old = W[i], bv = -1, bcst = 1 << 30, ties = 0;
      for (int v = 0; v < n; v++) { if (inW[v] || tabu[v] > it) continue; W[i] = v; int cc = cost(W, K);
        if (cc < bcst) { bcst = cc; bv = v; ties = 1; } else if (cc == bcst && rnd() % (++ties) == 0) bv = v; }
      W[i] = bv; inW[old] = 0; inW[bv] = 1; tabu[old] = it + 10 + rnd() % 20; c = bcst;
      if (c < bestc) { bestc = c; stall = 0; } else stall++; }
    if (c == 0) { found++; printf("resolving set of size %d:", K); for (int i = 0; i < K; i++) printf(" %d", W[i]); printf("\n"); fflush(stdout); break; }
  }
  if (!found) printf("no resolving set of size %d found (%ld moves)\n", K, it);
  return 0; }
