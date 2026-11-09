/* Exact minimal diameter of admissible k-sets in Z[i] (ring 4) or Z[w], w = (-1+sqrt(-3))/2 (ring 3).
   Quantavane Originals, problem gauss-admissible. Our own code.

   cc -O2 -o admissible_exact admissible_exact.c && ./admissible_exact RING KMAX [DSTART]

   A finite set H is admissible when for every prime ideal P of norm at most |H| the residues of H modulo P miss at
   least one class (for larger norms nothing can be covered). The diameter is the largest squared distance between two
   points: x^2 + y^2 for x + yi in Z[i]; x^2 - xy + y^2 for x + yw in Z[w]. For each k the program finds the least D
   for which an admissible k-set of diameter at most D exists, by an exhaustive search: translate so that the
   lexicographically least point is 0; every other point h is then lexicographically above 0 with norm(h) <= D;
   points are added in a fixed order, every pair at squared distance <= D, and a branch stops as soon as the classes of
   some prime ideal are all covered or too few candidates are left. Prints "k D" and one optimal set per k. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXP 4096
#define MAXI 64
static int ring, K;
static int nid; static int inorm[MAXI], ikind[MAXI], ip[MAXI], ir[MAXI];  /* prime ideals */
static int px[MAXP], py[MAXP], np; static unsigned char cls[MAXP][MAXI];
static int sel[64], cnt[MAXI][4096], cov[MAXI];
static long long nodes;

static long long nrm(long long x, long long y) { return ring == 4 ? x * x + y * y : x * x - x * y + y * y; }
static int isprime(int n) { if (n < 2) return 0; for (int d = 2; d * d <= n; d++) if (n % d == 0) return 0; return 1; }
static long long pw(long long b, long long e, long long m) { long long r = 1; b %= m; while (e) { if (e & 1) r = r * b % m; b = b * b % m; e >>= 1; } return r; }
static int sqrtm1(int p) { /* r with r^2 = -1 mod p, p = 1 mod 4 */
  for (int a = 2; a < p; a++) { long long r = pw(a, (p - 1) / 4, p); if (r * r % p == p - 1) return (int)r; } return -1; }
static int cuberoot1(int p) { /* r with r^2 + r + 1 = 0 mod p, p = 1 mod 3 */
  for (int a = 2; a < p; a++) { long long r = pw(a, (p - 1) / 3, p); if (r != 1 && (r * r + r + 1) % p == 0) return (int)r; } return -1; }

static void ideals(int kmax) { /* prime ideals of norm <= kmax: kind 0 ramified/split (residue x + y r mod p), 1 inert */
  nid = 0;
  for (int p = 2; p <= kmax; p++) {
    if (!isprime(p)) continue;
    if (ring == 4) {
      if (p == 2) { inorm[nid] = 2; ikind[nid] = 0; ip[nid] = 2; ir[nid] = 1; nid++; }
      else if (p % 4 == 1) { int r = sqrtm1(p); inorm[nid] = p; ikind[nid] = 0; ip[nid] = p; ir[nid] = r; nid++;
                             inorm[nid] = p; ikind[nid] = 0; ip[nid] = p; ir[nid] = p - r; nid++; }
      else if ((long long)p * p <= kmax) { inorm[nid] = p * p; ikind[nid] = 1; ip[nid] = p; ir[nid] = 0; nid++; }
    } else {
      if (p == 3) { inorm[nid] = 3; ikind[nid] = 0; ip[nid] = 3; ir[nid] = 1; nid++; }   /* w = 1 mod (1 - w) */
      else if (p % 3 == 1) { int r = cuberoot1(p); int s = (int)(((long long)r * r) % p);
                             inorm[nid] = p; ikind[nid] = 0; ip[nid] = p; ir[nid] = r; nid++;
                             inorm[nid] = p; ikind[nid] = 0; ip[nid] = p; ir[nid] = s; nid++; }
      else if ((long long)p * p <= kmax) { inorm[nid] = p * p; ikind[nid] = 1; ip[nid] = p; ir[nid] = 0; nid++; }
    }
  }
}
static int classof(int id, int x, int y) {
  int p = ip[id];
  int a = ((x % p) + p) % p, b = ((y % p) + p) % p;
  if (ikind[id] == 1) return a * p + b;
  return (int)((a + (long long)b * ir[id]) % p);
}

static long long D; static int best[64]; static int found;
static void rec(int depth, int *cand, int nc) {
  nodes++;
  if (depth == K) { found = 1; memcpy(best, sel, sizeof(int) * K); return; }
  if (depth + nc < K) return;
  int *nxt = malloc(sizeof(int) * (nc + 1));
  for (int t = 0; t < nc && !found; t++) {
    if (depth + (nc - t) < K) break;
    int v = cand[t], ok = 1;
    for (int j = 0; j < nid; j++) if (inorm[j] <= K) { if (cnt[j][cls[v][j]] == 0 && cov[j] + 1 == inorm[j]) { ok = 0; break; } }
    if (!ok) continue;
    for (int j = 0; j < nid; j++) if (inorm[j] <= K) { if (cnt[j][cls[v][j]]++ == 0) cov[j]++; }
    sel[depth] = v;
    int m = 0;
    for (int u = t + 1; u < nc; u++) { int w = cand[u]; if (nrm(px[v] - px[w], py[v] - py[w]) <= D) nxt[m++] = w; }
    rec(depth + 1, nxt, m);
    for (int j = 0; j < nid; j++) if (inorm[j] <= K) { if (--cnt[j][cls[v][j]] == 0) cov[j]--; }
  }
  free(nxt);
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: %s RING(4|3) KMAX [DSTART]\n", argv[0]); return 2; }
  ring = atoi(argv[1]); int kmax = atoi(argv[2]); long long d0 = argc > 3 ? atoll(argv[3]) : 0;
  ideals(kmax);
  D = d0;
  for (K = 1; K <= kmax; K++) {
    for (;; D++) {
      /* candidates: 0 first, then points lexicographically above 0 with norm <= D */
      int R = 1; while (nrm(R, 0) <= 4 * D + 4 || nrm(0, R) <= 4 * D + 4) R++; R += 2;
      np = 0;
      for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) {
        if (x < 0 || (x == 0 && y < 0)) continue;
        if (nrm(x, y) > D) continue;
        if (np >= MAXP) { fprintf(stderr, "too many points\n"); return 1; }
        px[np] = x; py[np] = y; np++;
      }
      for (int v = 0; v < np; v++) for (int j = 0; j < nid; j++) cls[v][j] = (unsigned char)0, cls[v][j] = classof(j, px[v], py[v]);
      memset(cnt, 0, sizeof(cnt)); memset(cov, 0, sizeof(cov));
      found = 0; nodes = 0;
      int ok0 = 1;  /* the point 0 is always taken */
      for (int j = 0; j < nid; j++) if (inorm[j] <= K) { if (inorm[j] == 1) ok0 = 0; cnt[j][cls[0][j]]++; cov[j]++; }
      sel[0] = 0;
      if (K == 1) { found = 1; best[0] = 0; }
      else if (ok0) {
        int *cand = malloc(sizeof(int) * np); int nc = 0;
        for (int v = 1; v < np; v++) if (nrm(px[v], py[v]) <= D) cand[nc++] = v;
        rec(1, cand, nc); free(cand);
      }
      if (found) {
        printf("%d %lld  ", K, D);
        for (int i = 0; i < K; i++) printf("%d,%d ", px[best[i]], py[best[i]]);
        printf(" (nodes %lld)\n", nodes); fflush(stdout);
        break;
      }
    }
  }
  return 0;
}
