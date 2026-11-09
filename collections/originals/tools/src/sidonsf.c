/* Largest sum-free Sidon subsets of {1,...,n} (our own code, Quantavane Originals, problem sidon-sumfree).
   A is Sidon when all differences a - b (a > b in A) are distinct, equivalently all sums a + b (a <= b) are distinct;
   A is sum-free when a + b = c has no solution with a, b, c in A (a = b allowed).
   cc -O2 -o sidonsf sidonsf.c ; ./sidonsf NMAX
   For each n, f(n) = max(f(n-1), largest such set containing n): a depth-first search adds elements below n in
   decreasing order and stops when the elements left cannot reach f(n-1) + 1. Prints "n f(n) set". */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, want, a[64], k, found, sol[64];
static unsigned char diff[4096], in[4096];
static long long nodes;
static int ok(int x) {
  if (in[2 * x]) return 0;                     /* x + x = c */
  for (int i = 0; i < k; i++) {
    int d = a[i] - x; if (diff[d]) return 0;   /* differences new and distinct among themselves */
    for (int j = 0; j < i; j++) if (a[j] - x == d) return 0;
    if (in[a[i] + x]) return 0;                /* x + a = c */
    if (a[i] - x != x && in[a[i] - x]) return 0; /* x + c = a  (c = a - x) */
    if (a[i] == 2 * x) return 0;               /* x + x = a */
  }
  return 1;
}
static void rec(int below) {
  nodes++;
  if (k == want) { found = 1; memcpy(sol, a, sizeof(int) * k); return; }
  for (int x = below - 1; x >= 1 && !found; x--) {
    if (k + x < want) return;                  /* at most x more elements fit below */
    if (!ok(x)) continue;
    for (int i = 0; i < k; i++) diff[a[i] - x] = 1;
    a[k++] = x; in[x] = 1;
    rec(x);
    in[x] = 0; k--;
    for (int i = 0; i < k; i++) diff[a[i] - x] = 0;
  }
}
int main(int argc, char **argv) {
  int nmax = atoi(argv[1]); int f = 0; int best[64]; int bk = 0;
  for (n = 1; n <= nmax; n++) {
    want = f + 1; found = 0; k = 0; memset(diff, 0, sizeof(diff)); memset(in, 0, sizeof(in)); nodes = 0;
    a[k++] = n; in[n] = 1;
    if (!(in[2 * n])) rec(n);
    if (found) { f = want; memcpy(best, sol, sizeof(int) * f); bk = f; }
    printf("%d %d  ", n, f); for (int i = bk - 1; i >= 0; i--) printf("%d ", best[i]); printf(" (nodes %lld)\n", nodes); fflush(stdout);
  }
  return 0;
}
