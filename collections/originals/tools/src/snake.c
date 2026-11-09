/* Longest induced paths (snakes) and induced cycles (coils) in Fibonacci and Lucas cubes (our own code).
   Fibonacci cube F_n: binary words of length n with no two adjacent 1s; Lucas cube L_n: the same with the first and
   last letters not both 1 (cyclic). Edges join words at Hamming distance 1.
   cc -O2 -o snake snake.c ; ./snake fib|luc N [snake|coil] [SECONDS]
   Exhaustive depth-first search over induced paths started at every vertex (a vertex may join the path only when its
   one path neighbour is the current end); bound: path length + vertices still free <= best. Prints the longest found
   (exact if the search finishes before the time limit) as words, one per line. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n, V, word[2048], adj[2048][32], deg[2048], cyc;
static int path[2048], len, best, bestpath[2048];
static int cnt[2048];  /* number of path vertices adjacent to v */
static unsigned char onp[2048];
static long long nodes; static time_t t0; static int limit, timedout, coil;
static int popc(int x) { return __builtin_popcount(x); }
static void rec(void) {
  nodes++;
  if ((nodes & 0xFFFFF) == 0 && limit && time(NULL) - t0 > limit) { timedout = 1; return; }
  int end = path[len - 1];
  if (!coil) { if (len - 1 > best) { best = len - 1; memcpy(bestpath, path, sizeof(int) * len); } }
  int freec = 0; for (int v = 0; v < V; v++) if (!onp[v] && cnt[v] == 0) freec++;
  if (!coil && len - 1 + freec + 1 <= best) return;
  if (coil && len + freec + 1 <= best) return;
  for (int t = 0; t < deg[end] && !timedout; t++) {
    int v = adj[end][t];
    if (onp[v]) continue;
    if (coil && len >= 3 && cnt[v] == 2) {
      /* v adjacent to end and to path[0] only: closes an induced cycle */
      int ok = 1; for (int s = 0; s < deg[v]; s++) { int u = adj[v][s]; if (onp[u] && u != end && u != path[0]) ok = 0; }
      int a0 = 0; for (int s = 0; s < deg[v]; s++) if (adj[v][s] == path[0]) a0 = 1;
      if (ok && a0 && len + 1 > best && v > path[0]) { best = len + 1; memcpy(bestpath, path, sizeof(int) * len); bestpath[len] = v; }
      continue;
    }
    if (cnt[v] != 1) continue;
    if (coil && v < path[0]) continue;   /* the start is the least vertex of the cycle */
    onp[v] = 1; path[len++] = v; for (int s = 0; s < deg[v]; s++) cnt[adj[v][s]]++;
    rec();
    for (int s = 0; s < deg[v]; s++) cnt[adj[v][s]]--; len--; onp[v] = 0;
  }
}
int main(int argc, char **argv) {
  int luc = !strcmp(argv[1], "luc"); n = atoi(argv[2]); coil = argc > 3 && !strcmp(argv[3], "coil");
  limit = argc > 4 ? atoi(argv[4]) : 0;
  V = 0;
  for (int w = 0; w < (1 << n); w++) { if (w & (w >> 1)) continue; if (luc && n > 1 && (w & 1) && (w >> (n - 1) & 1)) continue; word[V++] = w; }
  for (int a = 0; a < V; a++) { deg[a] = 0; for (int b = 0; b < V; b++) if (popc(word[a] ^ word[b]) == 1) adj[a][deg[a]++] = b; }
  best = coil ? 0 : 0; t0 = time(NULL);
  for (int s = 0; s < V && !timedout; s++) {
    memset(cnt, 0, sizeof(cnt)); memset(onp, 0, sizeof(onp));
    path[0] = s; len = 1; onp[s] = 1; for (int t = 0; t < deg[s]; t++) cnt[adj[s][t]]++;
    rec();
  }
  int L = coil ? best : best + 1;
  printf("# %s cube n=%d %s: %d %s%s (nodes %lld)\n", luc ? "Lucas" : "Fibonacci", n, coil ? "coil" : "snake", best, coil ? "vertices" : "edges", timedout ? " (time limit: best found, not proved)" : " (exhaustive)", nodes);
  for (int i = 0; i < L; i++) { for (int b = n - 1; b >= 0; b--) putchar((word[bestpath[i]] >> b & 1) ? '1' : '0'); putchar('\n'); }
  return 0;
}
