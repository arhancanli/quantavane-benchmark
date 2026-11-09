/* Domination numbers of Paley graphs (our own code, Quantavane Originals).
   cc -O2 -o paleydom paleydom.c ; ./paleydom P [TIMELIMIT]
   P prime, P = 1 mod 4. Vertices Z_P, x ~ y when x - y is a nonzero square. A dominating set D meets the closed
   neighbourhood N[x] of every vertex x. Exact search: 0 is in some minimum dominating set (vertex-transitivity);
   repeatedly take the least undominated vertex u and branch on the members of N[u]; prune when the dominated count
   plus (slots left) * (largest closed neighbourhood) < P. Iterative deepening on the size. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define MAXP 4096
#define W ((MAXP + 63) / 64)
typedef unsigned long long u64;
static int P, words; static u64 nb[MAXP][W]; static int sel[64], found; static long long nodes; static time_t t0; static int lim, tout;
static int isqr[MAXP];
static int popc(const u64 *a) { int c = 0; for (int i = 0; i < words; i++) c += __builtin_popcountll(a[i]); return c; }
static void rec(int depth, int k, u64 *dom) {
  nodes++;
  if (lim && (nodes & 0xFFFF) == 0 && time(NULL) - t0 > lim) { tout = 1; return; }
  int c = popc(dom);
  if (c == P) { found = depth; return; }
  if (depth == k) return;
  if (c + (long long)(k - depth) * ((P + 1) / 2) < P) return;
  int u = -1; for (int i = 0; i < words && u < 0; i++) { u64 m = ~dom[i]; if (i == words - 1 && P % 64) m &= (1ULL << (P % 64)) - 1; if (m) u = i * 64 + __builtin_ctzll(m); }
  u64 nd[W];
  for (int v = 0; v < P && !found && !tout; v++) {
    if (v != u && !isqr[(v - u + P) % P]) continue;   /* v in N[u] */
    for (int i = 0; i < words; i++) nd[i] = dom[i] | nb[v][i];
    sel[depth] = v; rec(depth + 1, k, nd);
  }
}
int main(int argc, char **argv) {
  P = atoi(argv[1]); lim = argc > 2 ? atoi(argv[2]) : 0; words = (P + 63) / 64;
  for (int x = 1; x < P; x++) isqr[(long long)x * x % P] = 1;
  for (int v = 0; v < P; v++) { memset(nb[v], 0, sizeof(nb[v])); for (int x = 0; x < P; x++) if (x == v || isqr[(x - v + P) % P]) nb[v][x / 64] |= 1ULL << (x % 64); }
  t0 = time(NULL);
  for (int k = 1; k < 64; k++) {
    u64 dom[W]; memcpy(dom, nb[0], sizeof(u64) * W); sel[0] = 0; found = 0; tout = 0;
    rec(1, k, dom);
    if (tout) { printf("%d timeout at size %d: gamma >= %d (nodes %lld)\n", P, k, k, nodes); return 0; }
    if (found) { printf("%d %d  ", P, k); for (int i = 0; i < k; i++) printf("%d ", sel[i]); printf(" (nodes %lld)\n", nodes); return 0; }
  }
  return 0;
}
