/* Non-redundant aperture masks on the hexagonal segment array of s rings with the centre segment removed (our own
   code, Quantavane Originals; problem nrm-segments).
   Segments: points (a, b) of the triangular lattice with hexagonal norm max(|a|, |b|, |a + b|) from 1 to s. A set is
   non-redundant when the difference vectors of its pairs are all different up to sign.
   cc -O2 -o nrm nrm.c
   ./nrm max S            exhaustive search: the largest non-redundant set (prints one)
   ./nrm ls S K0 SECS SEED   local search for k = K0, K0+1, ...: move one hole at a time to the position creating the
                          fewest repeated baselines (tabu list); prints every k reached */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int s, n, R, W, pa[2000], pb[2000];
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int hn(int a, int b) { int c = -(a + b), m = abs(a); if (abs(b) > m) m = abs(b); if (abs(c) > m) m = abs(c); return m; }
static int key(int i, int j) { int da = pa[i] - pa[j], db = pb[i] - pb[j]; if (da < 0 || (da == 0 && db < 0)) { da = -da; db = -db; } return (da + R) * W + (db + R); }
static void setup(int S) { s = S; R = 2 * s; W = 4 * s + 1; n = 0;
  for (int a = -s; a <= s; a++) for (int b = -s; b <= s; b++) { int h = hn(a, b); if (h >= 1 && h <= s) { pa[n] = a; pb[n] = b; n++; } } }

/* exhaustive search (max) */
static unsigned char *used; static int chosen[64], bestset[64], best; static long long nodes;
static void dfs(int k, int *cand, int nc) {
  nodes++;
  if (k > best) { best = k; memcpy(bestset, chosen, sizeof(int) * k); }
  for (int i = 0; i < nc; i++) {
    if (k + (nc - i) <= best) return;
    int p = cand[i], keys[64], ok = 1;
    for (int j = 0; j < k; j++) { int kk = key(p, chosen[j]); if (used[kk]) { ok = 0; break; } for (int t = 0; t < j; t++) if (keys[t] == kk) { ok = 0; break; } if (!ok) break; keys[j] = kk; }
    if (!ok) continue;
    chosen[k] = p; for (int j = 0; j < k; j++) used[keys[j]] = 1;
    int *nc2 = malloc(sizeof(int) * nc), m = 0;
    for (int t = i + 1; t < nc; t++) { int q = cand[t], good = 1, kq[64];
      for (int j = 0; j <= k; j++) { int kk = key(q, chosen[j]); if (used[kk]) { good = 0; break; } for (int u = 0; u < j; u++) if (kq[u] == kk) { good = 0; break; } if (!good) break; kq[j] = kk; }
      if (good) nc2[m++] = q; }
    dfs(k + 1, nc2, m); free(nc2);
    for (int j = 0; j < k; j++) used[keys[j]] = 0; }
}

/* local search for one large set */
static int ls(int K0, double secs) {
  int *cnt = calloc(W * W, sizeof(int)), in[2000], sel[200], *tabu = calloc(n, sizeof(int)), bestk = 0; long it = 0; clock_t st = clock();
  for (int k = K0;; k++) {
    memset(in, 0, sizeof in); memset(cnt, 0, sizeof(int) * W * W);
    for (int i = 0; i < k;) { int p = rnd() % n; if (!in[p]) { in[p] = 1; sel[i++] = p; } }
    for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) cnt[key(sel[i], sel[j])]++;
    int conf = 0; for (int i = 0; i < W * W; i++) if (cnt[i] > 1) conf += cnt[i] - 1;
    while (conf > 0 && (double)(clock() - st) / CLOCKS_PER_SEC < secs) { it++;
      int cand[200], nc = 0; for (int i = 0; i < k; i++) { int bad = 0; for (int j = 0; j < k && !bad; j++) if (j != i && cnt[key(sel[i], sel[j])] > 1) bad = 1; if (bad) cand[nc++] = i; }
      int i = cand[rnd() % nc], p = sel[i];
      for (int j = 0; j < k; j++) if (j != i) cnt[key(p, sel[j])]--;
      in[p] = 0;
      int bq = -1, bd = 1 << 30, ties = 0;
      for (int q = 0; q < n; q++) { if (in[q] || q == p || tabu[q] > it) continue; int d = 0;
        for (int j = 0; j < k; j++) if (j != i && cnt[key(q, sel[j])] >= 1) d++;
        if (d < bd) { bd = d; bq = q; ties = 1; } else if (d == bd) { ties++; if (rnd() % ties == 0) bq = q; } }
      if (bq < 0) bq = p;
      sel[i] = bq; in[bq] = 1; for (int j = 0; j < k; j++) if (j != i) cnt[key(bq, sel[j])]++;
      tabu[p] = it + 5 + rnd() % 10;
      conf = 0; for (int t = 0; t < W * W; t++) if (cnt[t] > 1) conf += cnt[t] - 1; }
    if (conf > 0) break;
    bestk = k; printf("k=%d:", k); for (int i = 0; i < k; i++) printf(" %d %d", pa[sel[i]], pb[sel[i]]); printf("\n"); fflush(stdout); }
  return bestk;
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: nrm max|ls S ...\n"); return 2; }
  setup(atoi(argv[2])); used = calloc(W * W, 1);
  if (!strcmp(argv[1], "max")) {
    int *cand = malloc(sizeof(int) * n); for (int i = 0; i < n; i++) cand[i] = i;
    dfs(0, cand, n);
    printf("s=%d: maximum %d (%lld nodes):", s, best, nodes); for (int i = 0; i < best; i++) printf(" %d %d", pa[bestset[i]], pb[bestset[i]]); printf("\n");
  } else if (!strcmp(argv[1], "ls")) { rs ^= (unsigned long long)atoi(argv[5]) * 2654435761ULL; ls(atoi(argv[3]), atof(argv[4])); }
  return 0;
}
