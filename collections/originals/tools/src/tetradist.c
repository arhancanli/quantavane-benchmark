/* Subsets of the tetrahedral grid with all pairwise distances distinct (our own code, Quantavane Originals, problem
   tetra-distinct). Points (a, b, c) with a, b, c >= 0 and a + b + c <= n - 1 stand for a e1 + b e2 + c e3, the unit
   vectors e1, e2, e3 at 60 degrees to each other (a tetrahedral piece of the face-centred cubic lattice); squared
   distance q = da^2 + db^2 + dc^2 + da db + db dc + da dc.
   cc -O2 -o tetradist tetradist.c
   ./tetradist exact NMAX            largest such subset for n = 1..NMAX (exhaustive depth-first search)
   ./tetradist ls N K0 SECONDS SEED  local search for k = K0, K0+1, ...: move one point at a time to the position that
                                     creates the fewest repeated distances (tabu list); prints every k reached */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n, np, P[4000][3], best, bestset[64], chosen[64]; static unsigned char *used; static int QM;
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int q(int i, int j) { int a = P[i][0] - P[j][0], b = P[i][1] - P[j][1], c = P[i][2] - P[j][2]; return a * a + b * b + c * c + a * b + b * c + a * c; }
static void setup(int N) { n = N; np = 0; for (int a = 0; a < n; a++) for (int b = 0; a + b < n; b++) for (int c = 0; a + b + c < n; c++) { P[np][0] = a; P[np][1] = b; P[np][2] = c; np++; } QM = (n - 1) * (n - 1) + 1; }
static void dfs(int k, int *cand, int nc) {
  if (k > best) { best = k; memcpy(bestset, chosen, sizeof(int) * k); }
  for (int i = 0; i < nc; i++) { if (k + (nc - i) <= best) return; int p = cand[i], ks[64], ok = 1;
    for (int j = 0; j < k; j++) { int d = q(p, chosen[j]); if (used[d]) { ok = 0; break; } for (int t = 0; t < j; t++) if (ks[t] == d) { ok = 0; break; } if (!ok) break; ks[j] = d; }
    if (!ok) continue; chosen[k] = p; for (int j = 0; j < k; j++) used[ks[j]] = 1;
    int *nc2 = malloc(sizeof(int) * nc), m = 0;
    for (int t = i + 1; t < nc; t++) { int r = cand[t], good = 1, kr[64]; for (int j = 0; j <= k; j++) { int d = q(r, chosen[j]); if (used[d]) { good = 0; break; } for (int u = 0; u < j; u++) if (kr[u] == d) { good = 0; break; } if (!good) break; kr[j] = d; } if (good) nc2[m++] = r; }
    dfs(k + 1, nc2, m); free(nc2); for (int j = 0; j < k; j++) used[ks[j]] = 0; } }
static void ls(int K0, double secs) { int *cnt = calloc(QM, sizeof(int)), sel[64], in[4000], *tabu = calloc(np, sizeof(int)); long it = 0; clock_t st = clock();
  for (int k = K0;; k++) { memset(in, 0, sizeof in); memset(cnt, 0, sizeof(int) * QM);
    for (int i = 0; i < k;) { int p = rnd() % np; if (!in[p]) { in[p] = 1; sel[i++] = p; } }
    for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) cnt[q(sel[i], sel[j])]++;
    int conf = 0; for (int t = 0; t < QM; t++) if (cnt[t] > 1) conf += cnt[t] - 1;
    while (conf > 0 && (double)(clock() - st) / CLOCKS_PER_SEC < secs) { it++;
      int cand[64], nc = 0; for (int i = 0; i < k; i++) { int bad = 0; for (int j = 0; j < k && !bad; j++) if (j != i && cnt[q(sel[i], sel[j])] > 1) bad = 1; if (bad) cand[nc++] = i; }
      int i = cand[rnd() % nc], p = sel[i]; for (int j = 0; j < k; j++) if (j != i) cnt[q(p, sel[j])]--; in[p] = 0;
      int bq = -1, bd = 1 << 30, ties = 0;
      for (int r = 0; r < np; r++) { if (in[r] || r == p || tabu[r] > it) continue; int d = 0; for (int j = 0; j < k; j++) if (j != i && cnt[q(r, sel[j])] >= 1) d++;
        if (d < bd) { bd = d; bq = r; ties = 1; } else if (d == bd && rnd() % (++ties) == 0) bq = r; }
      if (bq < 0) bq = p; sel[i] = bq; in[bq] = 1; for (int j = 0; j < k; j++) if (j != i) cnt[q(bq, sel[j])]++; tabu[p] = it + 5 + rnd() % 10;
      conf = 0; for (int t = 0; t < QM; t++) if (cnt[t] > 1) conf += cnt[t] - 1; }
    if (conf) break;
    printf("n=%d k=%d:", n, k); for (int i = 0; i < k; i++) printf(" %d,%d,%d", P[sel[i]][0], P[sel[i]][1], P[sel[i]][2]); printf("\n"); fflush(stdout); } }
int main(int argc, char **argv) {
  if (!strcmp(argv[1], "exact")) { int NM = atoi(argv[2]); for (int N = 1; N <= NM; N++) { setup(N); used = calloc(QM + 1, 1); best = 0;
      int *cand = malloc(sizeof(int) * np); for (int i = 0; i < np; i++) cand[i] = i; clock_t st = clock(); dfs(0, cand, np);
      printf("n=%d points=%d max=%d (%.1f s):", N, np, best, (double)(clock() - st) / CLOCKS_PER_SEC); for (int i = 0; i < best; i++) printf(" %d,%d,%d", P[bestset[i]][0], P[bestset[i]][1], P[bestset[i]][2]); printf("\n"); fflush(stdout); free(used); free(cand); } }
  else { setup(atoi(argv[2])); rs ^= (unsigned long long)atoi(argv[5]) * 2654435761ULL; ls(atoi(argv[3]), atof(argv[4])); }
  return 0; }
