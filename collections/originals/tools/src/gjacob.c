/* The Jacobsthal function of the Gaussian integers (our own code, Quantavane Originals, problem gauss-jacobsthal).
   Gaussian primes up to units with norm <= X: 1+i; a+bi and a-bi for each p = a^2 + b^2 = 1 (mod 4), p <= X; q for
   q = 3 (mod 4), q^2 <= X. Choose one residue class modulo each prime; the s x s square {x + yi : 0 <= x, y < s} is
   covered when every point lies in a chosen class (by the Chinese remainder theorem some translate of the square then
   consists of Gaussian integers each divisible by a prime of norm <= X; tools/gauss_jacobsthal.py finds it).
     gjacob exact X SMAX [S0]          for s = S0, S0 + 1, ...: is the s x s square coverable? Exhaustive search: the
                                       first uncovered point must be covered by some unused prime; pruned when the
                                       unused primes, each counted with its fullest class among the uncovered points,
                                       cannot cover what is left. Prints a cover "a,b,c ..." for each coverable s.
     gjacob search X S SECONDS SEED    weighted local search for a cover of the S x S square (move one prime's class
                                       onto a random uncovered point, the best such move by weights that grow on points
                                       left uncovered; a short tabu list) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define MP 300
#define MS 48
static int np, kind[MP], P[MP], A[MP], B[MP], R[MP], nclass[MP];
static int S, NPT, cls[MP][MS * MS], cov[MS * MS], chosen[MP], used[MP];
static long long nodes;
static int isprime(int n) { if (n < 2) return 0; for (int d = 2; d * d <= n; d++) if (n % d == 0) return 0; return 1; }
static int pmod(long long a, int m) { a %= m; return a < 0 ? (int)(a + m) : (int)a; }
static int inv(int a, int m) { for (int x = 1; x < m; x++) if ((long long)a * x % m == 1) return x; return -1; }
static void primes(int X) {
  np = 0; kind[np] = 0; P[np] = 2; A[np] = 1; B[np] = 1; nclass[np] = 2; np++;
  for (int p = 3; p <= X; p++) if (isprime(p)) {
    if (p % 4 == 1) { int a, b = 0; for (a = 1; a * a < p; a++) { int bb = p - a * a, r = 0; while (r * r < bb) r++; if (r * r == bb && a > r) { b = r; break; } }
      for (int sg = 1; sg >= -1; sg -= 2) { kind[np] = 1; P[np] = p; A[np] = a; B[np] = sg * b; nclass[np] = p; R[np] = pmod(-(long long)a * inv(pmod(sg * b, p), p), p); np++; } }
    else if ((long long)p * p <= X) { kind[np] = 2; P[np] = p; nclass[np] = p * p; np++; } }
}
static int classof(int k, int x, int y) { if (kind[k] == 0) return (x + y) & 1; if (kind[k] == 1) return pmod(x + (long long)y * R[k], P[k]); return pmod(x, P[k]) * P[k] + pmod(y, P[k]); }
static void setup(int s) { S = s; NPT = s * s; for (int k = 0; k < np; k++) for (int y = 0; y < s; y++) for (int x = 0; x < s; x++) cls[k][y * s + x] = classof(k, x, y); }
static int tmpc[MP][4096];
static int bestclass(int k) { /* most uncovered points in one class of prime k */
  int m = 0, *c = tmpc[k], nc = nclass[k] < 4096 ? nclass[k] : 4096; memset(c, 0, sizeof(int) * nc);
  for (int t = 0; t < NPT; t++) if (!cov[t]) { int v = cls[k][t]; if (v < 4096 && ++c[v] > m) m = c[v]; } return m; }
static int rec(int uncovered) {
  nodes++;
  if (uncovered == 0) return 1;
  int bound = 0; for (int k = 0; k < np; k++) if (!used[k]) bound += bestclass(k);
  if (bound < uncovered) return 0;
  /* branch on the uncovered point with the fewest primes able to cover it usefully: here simply the first uncovered */
  int z = 0; while (cov[z]) z++;
  for (int k = 0; k < np; k++) if (!used[k]) {
    int c = cls[k][z], gain = 0; used[k] = 1; chosen[k] = c;
    for (int t = 0; t < NPT; t++) if (cls[k][t] == c) { if (cov[t]++ == 0) gain++; }
    if (rec(uncovered - gain)) return 1;
    for (int t = 0; t < NPT; t++) if (cls[k][t] == c) cov[t]--;
    used[k] = 0; }
  return 0;
}
static void show(int s, int all) { printf("cover %d:", s); for (int k = 0; k < np; k++) if (all || used[k]) printf(" %d,%d,%d", kind[k] == 2 ? P[k] : A[k], kind[k] == 2 ? 0 : B[k], chosen[k]); printf("\n"); fflush(stdout); }
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int main(int argc, char **argv) {
  if (argc >= 4 && !strcmp(argv[1], "exact")) {
    int X = atoi(argv[2]), smax = atoi(argv[3]); int s0 = argc > 4 ? atoi(argv[4]) : 1; primes(X); printf("X %d: %d primes\n", X, np);
    for (int s = s0; s <= smax; s++) { setup(s); memset(cov, 0, sizeof cov); memset(used, 0, sizeof used); nodes = 0; clock_t st = clock();
      int ok = rec(NPT); printf("X %d s %d %s nodes %lld (%.1f s)\n", X, s, ok ? "coverable" : "NOT coverable", nodes, (double)(clock() - st) / CLOCKS_PER_SEC); fflush(stdout); if (ok) show(s, 0); else break; }
    return 0; }
  if (argc >= 6 && !strcmp(argv[1], "search")) {
    int X = atoi(argv[2]), s = atoi(argv[3]); double secs = atof(argv[4]); rs ^= (unsigned long long)atoll(argv[5]) * 2654435761ULL;
    primes(X); setup(s); static int cnt[MS * MS]; static double w[MS * MS]; clock_t st = clock(); long it = 0;
    for (int k = 0; k < np; k++) chosen[k] = cls[k][rnd() % NPT];
    for (int t = 0; t < NPT; t++) { cnt[t] = 0; w[t] = 1; } for (int k = 0; k < np; k++) for (int t = 0; t < NPT; t++) if (cls[k][t] == chosen[k]) cnt[t]++;
    int unc = 0; for (int t = 0; t < NPT; t++) unc += cnt[t] == 0; int best = unc; static int tabu[MP];
    static double gainc[4096];
    while (unc > 0 && (double)(clock() - st) / CLOCKS_PER_SEC < secs) { it++;
      /* best weighted move over all primes and classes that cover at least one uncovered point */
      int bk = -1, bc = -1; double bd = -1e300;
      int z; do z = rnd() % NPT; while (cnt[z]);
      for (int k = 0; k < np; k++) { if (tabu[k] > it) continue; int c = cls[k][z], old = chosen[k]; if (c == old) continue;
        double d = 0; for (int t = 0; t < NPT; t++) { if (cls[k][t] == old && cnt[t] == 1) d -= w[t]; if (cls[k][t] == c && cnt[t] == 0) d += w[t]; }
        d += 1e-9 * (rnd() % 1000); if (d > bd) { bd = d; bk = k; bc = c; } }
      if (bk < 0) continue;
      int old = chosen[bk]; for (int t = 0; t < NPT; t++) { if (cls[bk][t] == old) { if (--cnt[t] == 0) unc++; } if (cls[bk][t] == bc) { if (cnt[t]++ == 0) unc--; } }
      chosen[bk] = bc; tabu[bk] = it + 2 + rnd() % 4;
      for (int t = 0; t < NPT; t++) if (!cnt[t]) w[t] += 1;
      if (unc < best) best = unc; }
    printf("X %d s %d uncovered %d (best %d) after %ld moves %.1f s\n", X, s, unc, best, it, (double)(clock() - st) / CLOCKS_PER_SEC);
    if (unc == 0) show(s, 1);
    return unc == 0 ? 0 : 1; }
  return 2; }
