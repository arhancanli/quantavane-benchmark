/* Y-shaped arrays with all baseline lengths distinct (our own code, Quantavane Originals, problem y-array).
   Three arms at 120 degrees; an antenna at distance a >= 1 on an arm. Squared baseline lengths: (a - a')^2 on one arm,
   a^2 + ab + b^2 between two arms. All N(N-1)/2 squared lengths must be different; minimise the arm length L (the
   largest distance used).
   cc -O2 -o yarray yarray.c
   ./yarray exact NMAX           least L for N = 2..NMAX (depth-first search over arms and positions, L increasing)
   ./yarray ls N L0 SECONDS SEED local search for L = L0, L0 - 1, ...: move one antenna at a time to the place that
                                 makes the fewest repeated lengths (tabu list); prints every L reached */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int N, L, arm[64], pos[64], *cnt, best[64][2];
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int len2(int a1, int p1, int a2, int p2) { if (a1 == a2) return (p1 - p2) * (p1 - p2); return p1 * p1 + p1 * p2 + p2 * p2; }
/* exact: place antennas in canonical order (arm, position increasing), with arm sizes nonincreasing up to symmetry */
static int k; static int found;
static void dfs(int start_arm, int start_pos) {
  if (found) return;
  if (k == N) { found = 1; for (int i = 0; i < N; i++) { best[i][0] = arm[i]; best[i][1] = pos[i]; } return; }
  for (int a = start_arm; a < 3; a++) {
    for (int p = (a == start_arm ? start_pos : 1); p <= L; p++) {
      int ok = 1, keys[64]; for (int j = 0; j < k; j++) { int v = len2(a, p, arm[j], pos[j]); if (cnt[v]) { ok = 0; break; } for (int t = 0; t < j; t++) if (keys[t] == v) { ok = 0; break; } if (!ok) break; keys[j] = v; }
      if (!ok) continue;
      for (int j = 0; j < k; j++) cnt[keys[j]] = 1; arm[k] = a; pos[k] = p; k++;
      dfs(a, p + 1); k--; for (int j = 0; j < k; j++) cnt[keys[j]] = 0;
      if (found) return; } } }
int main(int argc, char **argv) {
  if (!strcmp(argv[1], "exact")) { int NM = atoi(argv[2]);
    for (N = 2; N <= NM; N++) { for (L = 1;; L++) { cnt = calloc(3 * L * L + 1, sizeof(int)); k = 0; found = 0; dfs(0, 1); free(cnt); if (found) break; }
      printf("N=%d least L=%d:", N, L); for (int a = 0; a < 3; a++) { printf(" arm%d {", a); int f = 1; for (int i = 0; i < N; i++) if (best[i][0] == a) { printf(f ? "%d" : ",%d", best[i][1]); f = 0; } printf("}"); } printf("\n"); fflush(stdout); }
    return 0; }
  N = atoi(argv[2]); int L0 = atoi(argv[3]); double secs = atof(argv[4]); rs ^= (unsigned long long)atoi(argv[5]) * 2654435761ULL;
  for (L = L0; L >= 1; L--) { cnt = calloc(3 * L * L + 1, sizeof(int)); static char occ[3][2000]; memset(occ, 0, sizeof occ);
    for (int i = 0; i < N; i++) { int a, p; do { a = rnd() % 3; p = 1 + rnd() % L; } while (occ[a][p]); occ[a][p] = 1; arm[i] = a; pos[i] = p; }
    for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) cnt[len2(arm[i], pos[i], arm[j], pos[j])]++;
    int conf = 0; for (int v = 0; v <= 3 * L * L; v++) if (cnt[v] > 1) conf += cnt[v] - 1;
    static int tabu[3][2000]; memset(tabu, 0, sizeof tabu); long it = 0; clock_t st = clock();
    while (conf > 0 && (double)(clock() - st) / CLOCKS_PER_SEC < secs) { it++;
      int i; do i = rnd() % N; while (0); /* pick an antenna in conflict */
      for (int tries = 0; tries < 50; tries++) { i = rnd() % N; int bad = 0; for (int j = 0; j < N && !bad; j++) if (j != i && cnt[len2(arm[i], pos[i], arm[j], pos[j])] > 1) bad = 1; if (bad) break; }
      for (int j = 0; j < N; j++) if (j != i) { int v = len2(arm[i], pos[i], arm[j], pos[j]); if (cnt[v] > 1) conf--; cnt[v]--; }
      occ[arm[i]][pos[i]] = 0;
      int ba = arm[i], bp = pos[i], bd = 1 << 30, ties = 0;
      for (int a = 0; a < 3; a++) for (int p = 1; p <= L; p++) { if (occ[a][p] || tabu[a][p] > it) continue; int d = 0;
          for (int j = 0; j < N; j++) if (j != i && cnt[len2(a, p, arm[j], pos[j])] >= 1) d++;
          if (d < bd) { bd = d; ba = a; bp = p; ties = 1; } else if (d == bd && rnd() % (++ties) == 0) { ba = a; bp = p; } }
      tabu[arm[i]][pos[i]] = it + 7 + rnd() % 10; arm[i] = ba; pos[i] = bp; occ[ba][bp] = 1;
      for (int j = 0; j < N; j++) if (j != i) { int v = len2(arm[i], pos[i], arm[j], pos[j]); if (cnt[v] >= 1) conf++; cnt[v]++; } }
    free(cnt);
    if (conf) { printf("N=%d: none found with L=%d\n", N, L); break; }
    int mx = 0; for (int i = 0; i < N; i++) if (pos[i] > mx) mx = pos[i]; if (mx < L) L = mx;
    printf("N=%d L=%d:", N, L); for (int a = 0; a < 3; a++) { printf(" arm%d {", a); int f = 1; for (int p = 1; p <= L; p++) for (int i = 0; i < N; i++) if (arm[i] == a && pos[i] == p) { printf(f ? "%d" : ",%d", p); f = 0; } printf("}"); } printf("\n"); fflush(stdout); }
  return 0; }
