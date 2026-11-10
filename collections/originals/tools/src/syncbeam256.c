/* Short reset words for Q_p (x -> x + 1, x -> x^2 mod p) for primes p <= 256, by beam search over subsets (our own code,
   Quantavane Originals, problem sync-quadratic): tools/src/syncbeam.c with 256-bit subsets.
   cc -O2 -o syncbeam256 syncbeam256.c ; ./syncbeam256 P BEAM
   Level by level from the full set, apply both letters, drop repeated subsets within a level, and keep the BEAM
   subsets of smallest size; stop at a single state and print "P L word" (an upper bound, not a proof of optimality). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXD 400
typedef struct { uint64_t w[4]; } Set;
typedef struct { Set s; int cnt; int parent; char letter; } Node;
static int P, sq[256];
static int pc(const Set *s) { int c = 0; for (int i = 0; i < 4; i++) c += __builtin_popcountll(s->w[i]); return c; }
static Set apply(const Set *s, int l) {
  Set t = {{0, 0, 0, 0}};
  for (int x = 0; x < P; x++) if (s->w[x >> 6] >> (x & 63) & 1) { int y = l == 0 ? (x + 1) % P : sq[x]; t.w[y >> 6] |= 1ULL << (y & 63); }
  return t; }
static int scmp(const Set *a, const Set *b) { for (int i = 3; i >= 0; i--) if (a->w[i] != b->w[i]) return a->w[i] < b->w[i] ? -1 : 1; return 0; }
static int cmp(const void *a, const void *b) { const Node *x = a, *y = b; if (x->cnt != y->cnt) return x->cnt - y->cnt; return scmp(&x->s, &y->s); }
int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: syncbeam256 P BEAM\n"); return 2; }
  P = atoi(argv[1]); int B = atoi(argv[2]);
  if (P < 3 || P > 256) return 2;
  for (int x = 0; x < P; x++) sq[x] = (int)((long)x * x % P);

  Node *all = malloc(sizeof(Node) * ((size_t)B * MAXD + 16)); int nall = 0;
  Node *lvl = malloc(sizeof(Node) * (2 * (size_t)B + 16)), *nx = malloc(sizeof(Node) * (2 * (size_t)B + 16));
  int *idx = malloc(sizeof(int) * (2 * (size_t)B + 16));
  if (!all || !lvl || !nx || !idx) { fprintf(stderr, "memory\n"); return 1; }
  memset(&lvl[0].s, 0, sizeof(Set)); for (int x = 0; x < P; x++) lvl[0].s.w[x >> 6] |= 1ULL << (x & 63);
  lvl[0].cnt = P; lvl[0].parent = -1; lvl[0].letter = 0; all[nall] = lvl[0]; idx[0] = nall++; int nl = 1;
  for (int depth = 1; depth < MAXD; depth++) {
    int nn = 0;
    for (int i = 0; i < nl; i++) for (int l = 0; l < 2; l++) {
      nx[nn].s = apply(&lvl[i].s, l); nx[nn].cnt = pc(&nx[nn].s); nx[nn].parent = idx[i]; nx[nn].letter = l ? 'b' : 'a'; nn++; }
    qsort(nx, nn, sizeof(Node), cmp);
    int m = 0; for (int i = 0; i < nn; i++) if (m == 0 || scmp(&nx[i].s, &nx[m - 1].s)) nx[m++] = nx[i];
    if (m > B) m = B;
    for (int i = 0; i < m; i++) { lvl[i] = nx[i]; all[nall] = nx[i]; idx[i] = nall++; }
    nl = m;
    if (lvl[0].cnt == 1) {
      static char w[MAXD + 8]; int L = 0, c = idx[0]; while (all[c].parent >= 0) { w[L++] = all[c].letter; c = all[c].parent; }
      printf("%d %d ", P, L); for (int i = L - 1; i >= 0; i--) putchar(w[i]); printf("\n"); return 0; } }
  printf("%d no reset word found within depth %d\n", P, MAXD - 1); return 0; }
