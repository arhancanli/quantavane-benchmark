/* Strategies for Primel (Wordle on the 8,363 five-digit primes), our own code, Quantavane Originals, problem primel.
   cc -O2 -o primel primel.c -lm ; ./primel OUT.txt [DEPTHCAP] [EXACT_LIMIT] [BEAM]   (BEAM e.g. 12,6,3: candidates per depth)
   Feedback: greens first, then yellows for the remaining digits of the answer, left to right (Wordle's rule for
   repeated digits); encoded in base 3 (grey 0, yellow 1, green 2), 242 = solved. The strategy tree is built top
   down: at a node with answer set S (all consistent with the marks so far), every prime is a candidate guess; the
   guesses with the smallest sum over mark classes C of |C| * log|C| (ties: a guess in S) are tried, BEAM[depth] of
   them, each with its whole subtree, and the one with the fewest total guesses is kept; sets with at most EXACT_LIMIT
   answers are solved exactly among guesses from the set (fewest total guesses within the remaining depth). Writes one line per answer: the guesses in order (the last is the answer). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define NP 8363
static int P[NP], np; static unsigned char *F; /* F[g*np + a] */
static int dig[NP][5];
static int fb(int g, int a) { int G[5], A[5], m[5] = {0}, used[5] = {0}; for (int i = 0; i < 5; i++) { G[i] = dig[g][i]; A[i] = dig[a][i]; }
  for (int i = 0; i < 5; i++) if (G[i] == A[i]) { m[i] = 2; used[i] = 1; }
  for (int i = 0; i < 5; i++) if (m[i] != 2) for (int j = 0; j < 5; j++) if (!used[j] && A[j] == G[i]) { m[i] = 1; used[j] = 1; break; }
  return m[0] * 81 + m[1] * 27 + m[2] * 9 + m[3] * 3 + m[4]; }
static int exact_limit = 3, depthcap = 6;
static int **seq; static int *slen; /* per answer: guesses */
/* exact: minimal total guesses for set S (n answers) with at most `left` guesses remaining; returns large if impossible.
   Only guesses from S are tried for n <= exact_limit (enough for the small sets where it is used). */
static int best_small(int *S, int n, int left, int *bestg) {
  if (n == 1) { *bestg = S[0]; return left >= 1 ? 1 : 1000000; }
  if (left <= 1) return 1000000;
  int best = 1000000;
  for (int t = 0; t < n; t++) { int g = S[t]; int cls[243], cnt[243] = {0}; int tot = 1; /* this guess */
    for (int u = 0; u < n; u++) cnt[F[(long)g * np + S[u]]]++;
    int ok = 1; for (int c = 0; c < 243 && ok; c++) if (cnt[c] && c != 242) { int sub[16], m = 0; for (int u = 0; u < n; u++) if (F[(long)g * np + S[u]] == c) sub[m++] = S[u];
        int bg; int r = best_small(sub, m, left - 1, &bg); if (r >= 1000000) ok = 0; else tot += r + m; } /* each answer in C pays this guess (counted in m) */
    /* tot counts: the guess itself for the answer equal to g (1), and for the others 1 (this guess) + their subtree */
    if (ok) { int total = 0; total = 1; for (int c = 0; c < 243; c++) if (cnt[c] && c != 242) { int sub[16], m = 0; for (int u = 0; u < n; u++) if (F[(long)g * np + S[u]] == c) sub[m++] = S[u]; int bg; total += m + best_small(sub, m, left - 1, &bg); }
      if (total < best) { best = total; *bestg = g; } }
    (void)cls; (void)tot; }
  return best;
}
static int beam[16] = {12, 6, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
static int topk(int *S, int n, int k, int *out) {   /* the k guesses with the smallest sum |C| log |C| */
  static double sc[NP]; static int cnt[243]; char *inS = calloc(np, 1); for (int u = 0; u < n; u++) inS[S[u]] = 1;
  for (int c = 0; c < np; c++) { memset(cnt, 0, sizeof cnt); for (int u = 0; u < n; u++) cnt[F[(long)c * np + S[u]]]++;
    double v = 0; for (int q = 0; q < 243; q++) if (cnt[q] > 1) v += cnt[q] * log((double)cnt[q]); sc[c] = v - (inS[c] ? 1e-6 : 0); }
  free(inS);
  int m = 0; for (int c = 0; c < np; c++) { int pos = m < k ? m++ : k; if (pos == k) { if (sc[c] >= sc[out[k - 1]]) continue; pos = k - 1; }
    while (pos > 0 && sc[out[pos - 1]] > sc[c]) { out[pos] = out[pos - 1]; pos--; } out[pos] = c; }
  return m; }
static long cost(int *S, int n, int depth, int *choice);
static long cost_with(int *S, int n, int depth, int g) {  /* total guesses over S if g is guessed now */
  long tot = n; int *sub = malloc(sizeof(int) * n);
  for (int c = 0; c < 242; c++) { int m = 0; for (int u = 0; u < n; u++) if (F[(long)g * np + S[u]] == c) sub[m++] = S[u];
    if (m) { int ch; long r = cost(sub, m, depth + 1, &ch); if (r >= 1000000) { free(sub); return 1000000; } tot += r; } }
  free(sub); return tot; }
static long cost(int *S, int n, int depth, int *choice) {
  if (n == 1) { *choice = S[0]; return depth < depthcap ? 1 : 1000000; }
  if (depth >= depthcap - 1) return 1000000;
  if (n <= exact_limit) { int g; int r = best_small(S, n, depthcap - depth, &g); *choice = g; return r; }
  int k = beam[depth < 16 ? depth : 15], cand[64]; int m = topk(S, n, k, cand); long best = 1000000; *choice = cand[0];
  for (int t = 0; t < m; t++) { long r = cost_with(S, n, depth, cand[t]); if (r < best) { best = r; *choice = cand[t]; } }
  return best; }
static void build(int *S, int n, int depth) {
  int g; cost(S, n, depth, &g);
  for (int u = 0; u < n; u++) seq[S[u]][slen[S[u]]++] = g;
  int *sub = malloc(sizeof(int) * n);
  for (int c = 0; c < 242; c++) { int m = 0; for (int u = 0; u < n; u++) if (F[(long)g * np + S[u]] == c) sub[m++] = S[u]; if (m) build(sub, m, depth + 1); }
  free(sub);
}
int main(int argc, char **argv) {
  if (argc > 2) depthcap = atoi(argv[2]); if (argc > 3) exact_limit = atoi(argv[3]);
  if (argc > 4) { int k = 0; char *tok = strtok(argv[4], ","); while (tok && k < 16) { beam[k++] = atoi(tok); tok = strtok(NULL, ","); } while (k < 16) beam[k++] = 1; }
  char *comp = calloc(100000, 1); for (int i = 2; i < 100000; i++) if (!comp[i]) for (long j = (long)i * i; j < 100000; j += i) comp[j] = 1;
  for (int i = 10000; i < 100000; i++) if (!comp[i]) { P[np] = i; int x = i; for (int k = 4; k >= 0; k--) { dig[np][k] = x % 10; x /= 10; } np++; }
  F = malloc((size_t)np * np); for (int g = 0; g < np; g++) for (int a = 0; a < np; a++) F[(long)g * np + a] = (unsigned char)fb(g, a);
  seq = malloc(sizeof(int *) * np); slen = calloc(np, sizeof(int)); for (int a = 0; a < np; a++) seq[a] = malloc(sizeof(int) * 16);
  int *S = malloc(sizeof(int) * np); for (int a = 0; a < np; a++) S[a] = a;
  build(S, np, 0);
  long tot = 0; int mx = 0, hist[17] = {0}; for (int a = 0; a < np; a++) { tot += slen[a]; if (slen[a] > mx) mx = slen[a]; hist[slen[a]]++; }
  printf("%d primes; total guesses %ld (average %.6f), worst %d; histogram:", np, tot, (double)tot / np, mx); for (int k = 1; k <= mx; k++) printf(" %d", hist[k]); printf("\n");
  FILE *o = fopen(argv[1], "w"); for (int a = 0; a < np; a++) { for (int k = 0; k < slen[a]; k++) fprintf(o, k ? " %d" : "%d", P[seq[a][k]]); fprintf(o, "\n"); } fclose(o);
  return 0; }
