/* Short reset words for Q_p (x -> x + 1, x -> x^2 mod p, p <= 127) by beam search over subsets (our own code).
   cc -O2 -o syncbeam syncbeam.c ; ./syncbeam P BEAM
   Level by level from the full set, apply both letters, drop repeated subsets within a level, and keep the BEAM
   subsets of smallest size; stop at a single state and print the word (an upper bound, not a proof of optimality). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
static int P, sq[128];
typedef struct { u128 s; int cnt; long long parent; char letter; } Node;
static int pc(u128 s) { return __builtin_popcountll((unsigned long long)s) + __builtin_popcountll((unsigned long long)(s >> 64)); }
static u128 apply(u128 s, int l) { u128 t = 0; for (int x = 0; x < P; x++) if ((s >> x) & 1) t |= ((u128)1) << (l == 0 ? (x + 1) % P : sq[x]); return t; }
static int cmp(const void *a, const void *b) { const Node *x = a, *y = b; if (x->cnt != y->cnt) return x->cnt - y->cnt; return (x->s < y->s) ? -1 : (x->s > y->s); }
int main(int argc, char **argv) {
  P = atoi(argv[1]); long long B = atoll(argv[2]);
  for (int x = 0; x < P; x++) sq[x] = x * x % P;
  long long cap = B * 2 * 64 + 16; Node *all = malloc(sizeof(Node) * cap); long long nall = 0;
  Node *lvl = malloc(sizeof(Node) * 2 * B + 16), *nx = malloc(sizeof(Node) * 2 * B + 16);
  long long nl = 1; lvl[0].s = (((u128)1) << P) - 1; lvl[0].cnt = P; lvl[0].parent = -1; lvl[0].letter = 0;
  all[nall++] = lvl[0]; long long *idx = malloc(sizeof(long long) * (2 * B + 16)); idx[0] = 0;
  for (int depth = 1; depth < 64; depth++) {
    long long nn = 0;
    for (long long i = 0; i < nl; i++) for (int l = 0; l < 2; l++) {
      nx[nn].s = apply(lvl[i].s, l); nx[nn].cnt = pc(nx[nn].s); nx[nn].parent = idx[i]; nx[nn].letter = l ? 'b' : 'a'; nn++; }
    qsort(nx, nn, sizeof(Node), cmp);
    long long m = 0; for (long long i = 0; i < nn; i++) if (m == 0 || nx[i].s != nx[m - 1].s) nx[m++] = nx[i];
    if (m > B) m = B;
    for (long long i = 0; i < m; i++) { lvl[i] = nx[i]; if (nall >= cap) { fprintf(stderr, "cap\n"); return 1; } all[nall] = nx[i]; idx[i] = nall++; }
    nl = m;
    if (lvl[0].cnt == 1) {
      char w[200]; int L = 0; long long c = idx[0]; while (all[c].parent >= 0) { w[L++] = all[c].letter; c = all[c].parent; }
      printf("%d %d ", P, L); for (int i = L - 1; i >= 0; i--) putchar(w[i]); printf("\n"); return 0;
    }
  }
  printf("%d no reset word found within depth 63\n", P); return 0;
}
