/* Exact searches on the triangular grid T_n = {(a,b): a,b >= 0, a+b <= n-1} (our own code, Quantavane Originals).
   The point (a,b) is a + b*e^{i pi/3}; squared distance da^2 + da*db + db^2; three points are collinear when
   det = da1*db2 - da2*db1 = 0, and |det| is the area of the triangle in units of the unit triangle's area sqrt(3)/4.
   cc -O2 -o trigrid trigrid.c
   ./trigrid no3 NMAX            largest subset of T_n with no three collinear, n = 1..NMAX
   ./trigrid dist NMAX           largest subset of T_n with all pairwise distances distinct
   ./trigrid areas NMAX          largest subset of T_n whose triangles have distinct nonzero areas
   ./trigrid heil NMAX [NMIN]    largest t such that n points of T_n have every triangle of area >= t (no three
                                 collinear): the discrete Heilbronn value h(n) in units of sqrt(3)/4
   Each prints n, the value and one optimal set. Exhaustive branch and bound with the symmetry of T_n left alone
   (the bounds are simple: the number of points still available). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int N, np, pa[400], pb[400];
static int best, bestset[400], cur[400], ncur;
static long long nodes;
static int mode, target, need;

static int det(int i, int j, int k) {
  int da1 = pa[j] - pa[i], db1 = pb[j] - pb[i], da2 = pa[k] - pa[i], db2 = pb[k] - pb[i];
  int d = da1 * db2 - da2 * db1; return d < 0 ? -d : d;
}
static int dist2(int i, int j) { int da = pa[i] - pa[j], db = pb[i] - pb[j]; return da * da + da * db + db * db; }
static unsigned char used[100000];

static int ok_add(int v) {
  if (mode == 0) { for (int x = 0; x < ncur; x++) for (int y = x + 1; y < ncur; y++) if (det(cur[x], cur[y], v) == 0) return 0; return 1; }
  if (mode == 2) { for (int x = 0; x < ncur; x++) for (int y = x + 1; y < ncur; y++) if (det(cur[x], cur[y], v) < target) return 0; return 1; }
  if (mode == 3) {   /* areas of the new triangles (v with each pair) must be nonzero, new, distinct among themselves */
    int tmp[8000], nt = 0;
    for (int x = 0; x < ncur; x++) for (int y = x + 1; y < ncur; y++) { int d = det(cur[x], cur[y], v); if (d == 0 || used[d]) return 0;
      for (int t = 0; t < nt; t++) if (tmp[t] == d) return 0; tmp[nt++] = d; }
    return 1;
  }
  /* mode 1: distances from v to current points must be new and distinct among themselves */
  int tmp[400], nt = 0;
  for (int x = 0; x < ncur; x++) { int d = dist2(cur[x], v); if (used[d]) return 0; for (int t = 0; t < nt; t++) if (tmp[t] == d) return 0; tmp[nt++] = d; }
  return 1;
}
static void add(int v, int sign) { if (mode == 1) for (int x = 0; x < ncur; x++) used[dist2(cur[x], v)] += sign;
  if (mode == 3) for (int x = 0; x < ncur; x++) for (int y = x + 1; y < ncur; y++) used[det(cur[x], cur[y], v)] += sign; }

static int done;
static void rec(int start) {
  nodes++;
  if (ncur > best) { best = ncur; memcpy(bestset, cur, sizeof(int) * ncur); if (mode == 2 && best >= need) { done = 1; return; } }
  if (ncur + (np - start) <= best) return;
  for (int v = start; v < np && !done; v++) {
    if (ncur + (np - v) <= best) return;
    if (!ok_add(v)) continue;
    add(v, 1); cur[ncur++] = v;
    rec(v + 1);
    ncur--; add(v, -1);
  }
}

int main(int argc, char **argv) {
  if (argc < 3) return 2;
  mode = !strcmp(argv[1], "no3") ? 0 : !strcmp(argv[1], "dist") ? 1 : !strcmp(argv[1], "areas") ? 3 : 2;
  int nmax = atoi(argv[2]);
  for (N = (mode == 2 ? (argc > 3 ? atoi(argv[3]) : 3) : 1); N <= nmax; N++) {
    np = 0; for (int a = 0; a < N; a++) for (int b = 0; a + b < N; b++) { pa[np] = a; pb[np] = b; np++; }
    if (mode != 2) {
      best = 0; ncur = 0; nodes = 0; done = 0; memset(used, 0, sizeof(used)); rec(0);
      printf("%d %d  ", N, best); for (int i = 0; i < best; i++) printf("%d,%d ", pa[bestset[i]], pb[bestset[i]]);
      printf(" (nodes %lld)\n", nodes); fflush(stdout);
    } else {
      need = N; int lastok = -1, lastset[400];
      for (target = 1;; target++) {
        best = 0; ncur = 0; nodes = 0; done = 0; rec(0);
        if (best >= need) { lastok = target; memcpy(lastset, bestset, sizeof(int) * need); } else break;
      }
      printf("%d %d  ", N, lastok); if (lastok > 0) for (int i = 0; i < need; i++) printf("%d,%d ", pa[lastset[i]], pb[lastset[i]]);
      printf("\n"); fflush(stdout);
    }
  }
  return 0;
}
