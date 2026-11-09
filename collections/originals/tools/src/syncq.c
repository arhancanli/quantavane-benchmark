/* Shortest reset words of the automaton Q_p on Z_p with letters a: x -> x + 1 and b: x -> x^2 (mod p), our own code.
   cc -O2 -o syncq syncq.c ; ./syncq P [MAXSTATES]
   Breadth-first search over the subsets reached from Z_p (bit masks, p <= 127), applying a and b, until a single
   state is reached: the depth is the length of a shortest reset word (exact). A word of that length is printed. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u64;   /* subsets of Z_p, p <= 127 */
static int P; static int sq[128];
static u64 apply(u64 s, int letter) {
  u64 t = 0;
  for (int x = 0; x < P; x++) if (s >> x & 1) t |= ((u64)1) << (letter == 0 ? (x + 1) % P : sq[x]);
  return t;
}
/* hash set of visited subsets with parent pointers */
static u64 *key; static int *par; static char *let; static long long cap, used;
static long long find(u64 k) { unsigned long long lo = (unsigned long long)k ^ (unsigned long long)(k >> 64) * 0xC2B2AE3D27D4EB4FULL; long long h = (long long)((lo * 0x9E3779B97F4A7C15ULL) >> 1) % cap; while (key[h] && key[h] != k) h = (h + 1) % cap; return h; }
int main(int argc, char **argv) {
  P = atoi(argv[1]); cap = argc > 2 ? atoll(argv[2]) : 50000000;
  for (int x = 0; x < P; x++) sq[x] = x * x % P;
  key = calloc(cap, sizeof(u64)); par = malloc(sizeof(int) * cap); let = malloc(cap);
  long long *queue = malloc(sizeof(long long) * cap); long long qh = 0, qt = 0;
  u64 full = (((u64)1) << P) - 1;
  long long h0 = find(full); key[h0] = full; par[h0] = -1; queue[qt++] = h0; used = 1;
  int depth = 0; long long levelend = qt;
  while (qh < qt) {
    long long cur = queue[qh++];
    u64 s = key[cur];
    if ((s & (s - 1)) == 0) {
      char w[100000]; int L = 0; long long c = cur; while (par[c] >= 0) { w[L++] = let[c]; c = par[c]; }
      printf("%d %d ", P, L); for (int i = L - 1; i >= 0; i--) putchar(w[i]); printf("  (subsets visited %lld)\n", used); return 0;
    }
    for (int l = 0; l < 2; l++) {
      u64 t = apply(s, l); long long h = find(t);
      if (!key[h]) { if (used * 10 > cap * 7) { printf("%d too many subsets (> %lld) at depth %d\n", P, used, depth); return 0; }
        key[h] = t; par[h] = (int)cur; let[h] = l ? 'b' : 'a'; queue[qt++] = h; used++; }
    }
    if (qh == levelend) { depth++; levelend = qt; }
  }
  printf("%d not synchronizing (subsets visited %lld)\n", P, used);
  return 0;
}
