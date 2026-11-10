/* Small-diameter admissible k-sets in Z[i] (RING 4) or Z[w] (RING 3): the method of tools/admissible_sieve.py in C
   (our own code, Quantavane Originals, problem gauss-admissible), fast enough for every k up to 64 in both rings.
   cc -O2 -o admsieve admsieve.c ; ./admsieve RING K TRIALS SEED
   For a centre c (in quarter units) and a squared radius R (in sixteenths), take the lattice points z with
   norm(z - c) <= R; for each prime ideal P of norm <= K (smallest norm first) delete the residue class modulo P holding
   the fewest remaining points (ties at random); if K points remain, the K nearest to c form an admissible set. The
   least R that works is found by bisection; then local repair: take a point on the diameter out and put in any
   admissible point that does not raise the diameter. Prints "# ring R k K diameter D" and the set, one "x y" per line.
   An upper bound only; the checker (checkers/orig_numth.py gauss-admissible) proves the value. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static int RING, K, NI, In[64], Ik[64], Ip[64], Ir[64];
static unsigned long long rs;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static long nrm(long x, long y) { return RING == 4 ? x * x + y * y : x * x - x * y + y * y; }
static int isprime(int n) { if (n < 2) return 0; for (int d = 2; d * d <= n; d++) if (n % d == 0) return 0; return 1; }
static int md(long a, int p) { long r = a % p; return (int)(r < 0 ? r + p : r); }
static int res(int i, long x, long y) { return Ik[i] ? md(x, Ip[i]) * Ip[i] + md(y, Ip[i]) : md(x + y * Ir[i], Ip[i]); }
static void ideals(void) {  /* sorted by norm (then by order of discovery, as the Python sort on tuples) */
  int n[64], k[64], p[64], r[64], m = 0;
  for (int q = 2; q <= K; q++) { if (!isprime(q)) continue;
    if (RING == 4) {
      if (q == 2) { n[m] = 2; k[m] = 0; p[m] = 2; r[m++] = 1; }
      else if (q % 4 == 1) { int a = 2; while ((a * a + 1) % q) a++; n[m] = q; k[m] = 0; p[m] = q; r[m++] = a; n[m] = q; k[m] = 0; p[m] = q; r[m++] = q - a; }
      else if (q * q <= K) { n[m] = q * q; k[m] = 1; p[m] = q; r[m++] = 0; }
    } else {
      if (q == 3) { n[m] = 3; k[m] = 0; p[m] = 3; r[m++] = 1; }
      else if (q % 3 == 1) { int a = 2; while ((a * a + a + 1) % q) a++; n[m] = q; k[m] = 0; p[m] = q; r[m++] = a; n[m] = q; k[m] = 0; p[m] = q; r[m++] = (a * a) % q; }
      else if (q * q <= K) { n[m] = q * q; k[m] = 1; p[m] = q; r[m++] = 0; }
    } }
  int used[64] = {0}; NI = 0;   /* order by (norm, kind, p, r) like Python's sorted() of tuples */
  for (int t = 0; t < m; t++) { int b = -1;
    for (int j = 0; j < m; j++) if (!used[j] && (b < 0 || n[j] < n[b] || (n[j] == n[b] && (k[j] < k[b] || (k[j] == k[b] && (p[j] < p[b] || (p[j] == p[b] && r[j] < r[b]))))))) b = j;
    used[b] = 1; In[NI] = n[b]; Ik[NI] = k[b]; Ip[NI] = p[b]; Ir[NI] = r[b]; NI++; } }
static int admissible(long *X, long *Y, int k) {
  static char seen[4096];
  for (int i = 0; i < NI; i++) { if (In[i] > k) continue; memset(seen, 0, In[i]); int c = 0;
    for (int j = 0; j < k; j++) { int v = res(i, X[j], Y[j]); if (!seen[v]) { seen[v] = 1; c++; } }
    if (c == In[i]) return 0; }
  return 1; }
static long diam(long *X, long *Y, int k) { long D = 0; for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) { long d = nrm(X[i] - X[j], Y[i] - Y[j]); if (d > D) D = d; } return D; }
typedef struct { long d, x, y; } P3;
static int cmp3(const void *a, const void *b) { const P3 *p = a, *q = b;
  if (p->d != q->d) return p->d < q->d ? -1 : 1; if (p->x != q->x) return p->x < q->x ? -1 : 1; return p->y < q->y ? -1 : (p->y > q->y); }
static P3 *buf; static int bufcap;
/* returns 1 and fills X, Y with k points when the sieve keeps at least k */
static int sieve(int cx, int cy, long R, unsigned long long seed, long *X, long *Y) {
  long m = (long)(sqrt((double)R) / 4) + 3, ox = cx / 4, oy = cy / 4; int n = 0;
  for (long x = ox - m - 2; x <= ox + m + 2; x++) for (long y = oy - m - 2; y <= oy + m + 2; y++) {
    long d = nrm(4 * x - cx, 4 * y - cy);
    if (d <= R) { if (n == bufcap) { bufcap = bufcap ? 2 * bufcap : 4096; buf = realloc(buf, sizeof(P3) * bufcap); } buf[n].d = d; buf[n].x = x; buf[n].y = y; n++; } }
  if (n < K) return 0;
  unsigned long long save = rs; rs = seed * 0x9E3779B97F4A7C15ULL + 12345; if (!rs) rs = 1;
  static int cnt[4096];
  for (int i = 0; i < NI; i++) { memset(cnt, 0, sizeof(int) * In[i]);
    for (int j = 0; j < n; j++) cnt[res(i, buf[j].x, buf[j].y)]++;
    int lo = 1 << 30, nz = 1; for (int c = 0; c < In[i]; c++) { if (!cnt[c]) { nz = 0; break; } if (cnt[c] < lo) lo = cnt[c]; }
    if (!nz) continue;
    int ties = 0; for (int c = 0; c < In[i]; c++) if (cnt[c] == lo) ties++;
    int pick = (int)(rnd() % ties), drop = -1; for (int c = 0; c < In[i]; c++) if (cnt[c] == lo && pick-- == 0) { drop = c; break; }
    int w = 0; for (int j = 0; j < n; j++) if (res(i, buf[j].x, buf[j].y) != drop) buf[w++] = buf[j];
    n = w; if (n < K) { rs = save; return 0; } }
  rs = save;
  qsort(buf, n, sizeof(P3), cmp3);
  for (int j = 0; j < K; j++) { X[j] = buf[j].x; Y[j] = buf[j].y; }
  return 1; }
static long improve(long *X, long *Y, int rounds) {
  long D = diam(X, Y, K); long RX[128], RY[128], TX[128], TY[128];
  static long CX[200000], CY[200000];
  for (int t = 0; t < rounds; t++) {
    int pa[4096], pb[4096], np = 0;
    for (int i = 0; i < K; i++) for (int j = i + 1; j < K; j++) if (nrm(X[i] - X[j], Y[i] - Y[j]) == D && np < 4096) { pa[np] = i; pb[np] = j; np++; }
    int e = (int)(rnd() % np), out = (rnd() & 1) ? pa[e] : pb[e], r = 0;
    for (int i = 0; i < K; i++) if (i != out) { RX[r] = X[i]; RY[r] = Y[i]; r++; }
    long x0 = RX[0], x1 = RX[0], y0 = RY[0], y1 = RY[0];
    for (int i = 1; i < r; i++) { if (RX[i] < x0) x0 = RX[i]; if (RX[i] > x1) x1 = RX[i]; if (RY[i] < y0) y0 = RY[i]; if (RY[i] > y1) y1 = RY[i]; }
    int nc = 0;
    for (long x = x0 - 2; x <= x1 + 2; x++) for (long y = y0 - 2; y <= y1 + 2; y++) { int ok = 1;
      for (int i = 0; i < r && ok; i++) { if (RX[i] == x && RY[i] == y) ok = 0; else if (nrm(x - RX[i], y - RY[i]) >= D) ok = 0; }
      if (ok && nc < 200000) { CX[nc] = x; CY[nc] = y; nc++; } }
    for (int i = nc - 1; i > 0; i--) { int j = (int)(rnd() % (i + 1)); long a = CX[i]; CX[i] = CX[j]; CX[j] = a; a = CY[i]; CY[i] = CY[j]; CY[j] = a; }
    for (int c = 0; c < nc; c++) {
      memcpy(TX, RX, sizeof(long) * r); memcpy(TY, RY, sizeof(long) * r); TX[r] = CX[c]; TY[r] = CY[c];
      if (admissible(TX, TY, K)) { long d2 = diam(TX, TY, K);
        if (d2 < D || (d2 == D && (rnd() % 1000) < 300)) { memcpy(X, TX, sizeof(long) * K); memcpy(Y, TY, sizeof(long) * K); D = d2; break; } } } }
  return D; }
int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: admsieve RING K TRIALS SEED\n"); return 2; }
  RING = atoi(argv[1]); K = atoi(argv[2]); int trials = atoi(argv[3]); rs = 88172645463325252ULL ^ (unsigned long long)atoll(argv[4]) * 2654435761ULL;
  if ((RING != 3 && RING != 4) || K < 2 || K > 120) return 2;
  ideals();
  long BX[128], BY[128], X[128], Y[128], bestD = -1;
  for (int t = 0; t < trials; t++) {
    int cx = (int)(rnd() % 4), cy = (int)(rnd() % 4); long lo = 1, hi = 64L * K * 16; int found = 0;
    while (lo < hi) { long mid = (lo + hi) / 2;
      if (sieve(cx, cy, mid, (unsigned long long)t * 7919 + (unsigned long long)atoll(argv[4]), X, Y)) { hi = mid; found = 1; } else lo = mid + 1; }
    if (!found || !sieve(cx, cy, hi, (unsigned long long)t * 7919 + (unsigned long long)atoll(argv[4]), X, Y)) continue;
    if (!admissible(X, Y, K)) continue;
    long D = improve(X, Y, 60);
    if (bestD < 0 || D < bestD) { bestD = D; memcpy(BX, X, sizeof(long) * K); memcpy(BY, Y, sizeof(long) * K); } }
  if (bestD < 0) { printf("# none found\n"); return 1; }
  bestD = improve(BX, BY, 2000);
  if (!admissible(BX, BY, K)) { printf("# internal error\n"); return 1; }
  printf("# ring %d k %d diameter %ld\n", RING, K, bestD);
  for (int i = 0; i < K; i++) printf("%ld %ld\n", BX[i], BY[i]);
  return 0; }
