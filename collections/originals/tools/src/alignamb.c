/* Pairs of DNA sequences with the most optimal alignments (our own code, Quantavane Originals, problem
   align-ambiguity). Global alignment with unit costs (mismatch 1, gap 1, match 0); an alignment is a path in the
   edit graph from (0,0) to (n,n) with diagonal, horizontal and vertical steps; N(x, y) = number of minimum-cost paths.
   cc -O2 -o alignamb alignamb.c ; ./alignamb exact N      every pair (x canonical: letters in order of first
                                                            appearance; pairs and their reversals and swaps counted once)
                                     ./alignamb ls N SECONDS SEED   local search on pairs (change one letter) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef unsigned __int128 u128;
static int n; static char X[64], Y[64];
static u128 count(void) { static int D[64][64]; static u128 C[64][64];
  for (int i = 0; i <= n; i++) for (int j = 0; j <= n; j++) {
    if (!i && !j) { D[0][0] = 0; C[0][0] = 1; continue; }
    int best = 1 << 30; u128 c = 0;
    if (i && j) { int d = D[i - 1][j - 1] + (X[i - 1] != Y[j - 1]); if (d < best) { best = d; c = C[i - 1][j - 1]; } else if (d == best) c += C[i - 1][j - 1]; }
    if (i) { int d = D[i - 1][j] + 1; if (d < best) { best = d; c = C[i - 1][j]; } else if (d == best) c += C[i - 1][j]; }
    if (j) { int d = D[i][j - 1] + 1; if (d < best) { best = d; c = C[i][j - 1]; } else if (d == best) c += C[i][j - 1]; }
    D[i][j] = best; C[i][j] = c; }
  return C[n][n]; }
static void pr(u128 v) { char b[64]; int k = 0; if (!v) b[k++] = '0'; while (v) { b[k++] = '0' + (int)(v % 10); v /= 10; } while (k) putchar(b[--k]); }
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int main(int argc, char **argv) { n = atoi(argv[2]); const char *A = "ACGT";
  if (!strcmp(argv[1], "exact")) { u128 best = 0; char bx[64], by[64]; long total = 1; for (int i = 0; i < 2 * n; i++) total *= 4;
    for (long code = 0; code < total; code++) { long c = code; for (int i = 0; i < n; i++) { X[i] = A[c & 3]; c >>= 2; } for (int i = 0; i < n; i++) { Y[i] = A[c & 3]; c >>= 2; }
      /* x canonical: first letters appear in the order A, C, G, T */
      int seen = 0, ok = 1; for (int i = 0; i < n && ok; i++) { int l = (int)(strchr(A, X[i]) - A); if (l > seen) ok = 0; else if (l == seen) seen++; } if (!ok) continue;
      u128 v = count(); if (v > best) { best = v; memcpy(bx, X, n); memcpy(by, Y, n); } }
    printf("n=%d most optimal alignments: ", n); pr(best); printf("  %.*s / %.*s\n", n, bx, n, by); }
  else { double secs = atof(argv[3]); rs ^= (unsigned long long)atoi(argv[4]) * 2654435761ULL; u128 best = 0; char bx[64], by[64]; clock_t st = clock();
    while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) { for (int i = 0; i < n; i++) { X[i] = A[rnd() & 3]; Y[i] = A[rnd() & 3]; } u128 cur = count();
      for (int it = 0; it < 20000; it++) { char *s = (rnd() & 1) ? X : Y; int p = rnd() % n; char old = s[p]; s[p] = A[rnd() & 3]; u128 v = count();
        if (v >= cur || (rnd() % 100) < 2) cur = v; else s[p] = old;
        if (cur > best) { best = cur; memcpy(bx, X, n); memcpy(by, Y, n); } } }
    printf("n=%d best ", n); pr(best); printf("  %.*s / %.*s\n", n, bx, n, by); }
  return 0; }
