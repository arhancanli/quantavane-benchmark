/* Clusters of the diamond lattice with the most bonds (our own code, Quantavane Originals, problem diamond-bonds).
   Sites: A = integer points with all coordinates even and x + y + z = 0 (mod 4); B = A + (1, 1, 1). Bonds join an
   A site a to a + (1,1,1), a + (1,-1,-1), a + (-1,1,-1), a + (-1,-1,1) (squared length 3).
     diamond exact NMAX            every connected cluster with at most NMAX sites (Redelmeier's method, from an A and
                                   from a B origin, the origin the lexicographically smallest site): most bonds for each size
     diamond anneal N SECONDS SEED OUT   simulated annealing for N sites, best connected cluster to OUT */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define R 40
#define W (2 * R + 1)
#define ID(x, y, z) ((((x) + R) * W + ((y) + R)) * W + ((z) + R))
static const int D[4][3] = {{1,1,1},{1,-1,-1},{-1,1,-1},{-1,-1,1}};
static int isA(int x, int y, int z) { return ((x & 1) == 0); }
static int nbr(int x, int y, int z, int k, int *o) { int s = isA(x, y, z) ? 1 : -1; o[0] = x + s * D[k][0]; o[1] = y + s * D[k][1]; o[2] = z + s * D[k][2]; return 0; }
static unsigned char *in, *seen;
static int NMAX, ax[64], ay[64], az[64], na, bonds, best[64], bx[64][64][3];
static long long cnt[64];
static int gt(int x, int y, int z, int ox, int oy, int oz) { if (x != ox) return x > ox; if (y != oy) return y > oy; return z > oz; }
static int OX, OY, OZ;
static void rec(int *U, int nu) {
  while (nu > 0) {
    int s = U[--nu]; int x = s / (W * W) - R, y = (s / W) % W - R, z = s % W - R;
    int add = 0, o[3];
    for (int k = 0; k < 4; k++) { nbr(x, y, z, k, o); if (in[ID(o[0], o[1], o[2])]) add++; }
    in[s] = 1; ax[na] = x; ay[na] = y; az[na] = z; na++; bonds += add; cnt[na]++;
    if (bonds > best[na]) { best[na] = bonds; for (int i = 0; i < na; i++) { bx[na][i][0] = ax[i]; bx[na][i][1] = ay[i]; bx[na][i][2] = az[i]; } }
    if (na < NMAX) {
      int V[256], nv = nu; memcpy(V, U, sizeof(int) * nu); int newl[4], nn = 0;
      for (int k = 0; k < 4; k++) { nbr(x, y, z, k, o); int t = ID(o[0], o[1], o[2]);
        if (gt(o[0], o[1], o[2], OX, OY, OZ) && !in[t] && !seen[t]) { seen[t] = 1; newl[nn++] = t; V[nv++] = t; } }
      rec(V, nv);
      for (int i = 0; i < nn; i++) seen[newl[i]] = 0;
    }
    in[s] = 0; na--; bonds -= add;
  }
}
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double ur(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static int deg(int x, int y, int z) { int c = 0, o[3]; for (int k = 0; k < 4; k++) { nbr(x, y, z, k, o); c += in[ID(o[0], o[1], o[2])]; } return c; }
static int connected(int n, int *cx, int *cy, int *cz) {
  int st[4096], sp = 0, c = 1; unsigned char *v = seen; v[ID(cx[0], cy[0], cz[0])] = 1; st[sp++] = ID(cx[0], cy[0], cz[0]);
  while (sp) { int s = st[--sp]; int x = s / (W * W) - R, y = (s / W) % W - R, z = s % W - R, o[3];
    for (int k = 0; k < 4; k++) { nbr(x, y, z, k, o); int t = ID(o[0], o[1], o[2]); if (in[t] && !v[t]) { v[t] = 1; c++; st[sp++] = t; } } }
  for (int i = 0; i < n; i++) v[ID(cx[i], cy[i], cz[i])] = 0;
  return c == n;
}
int main(int argc, char **argv) {
  in = calloc((size_t)W * W * W, 1); seen = calloc((size_t)W * W * W, 1);
  if (argc >= 3 && !strcmp(argv[1], "exact")) {
    NMAX = atoi(argv[2]);
    int origins[2][3] = {{0,0,0},{1,1,1}};
    for (int t = 0; t < 2; t++) { OX = origins[t][0]; OY = origins[t][1]; OZ = origins[t][2];
      int U[1] = {ID(OX, OY, OZ)}; seen[U[0]] = 1; rec(U, 1); seen[U[0]] = 0; }
    for (int n = 1; n <= NMAX; n++) { printf("n %d animals %lld maxbonds %d dangling %d :", n, cnt[n], best[n], 4 * n - 2 * best[n]);
      for (int i = 0; i < n; i++) printf(" %d,%d,%d", bx[n][i][0], bx[n][i][1], bx[n][i][2]); printf("\n"); }
    return 0; }
  if (argc >= 6 && !strcmp(argv[1], "anneal")) {
    int N = atoi(argv[2]); double secs = atof(argv[3]); rs ^= (unsigned long long)atoi(argv[4]) * 2654435761ULL;
    static int cx[4096], cy[4096], cz[4096], bxx[4096], byy[4096], bzz[4096]; int bestB = -1; clock_t st = clock(); int restarts = 0;
    while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) { restarts++;
      /* start: the N sites nearest a random centre */
      for (int i = 0; i < N; i++) in[ID(cx[i], cy[i], cz[i])] = 0;
      double ox = 4 * ur(), oy = 4 * ur(), oz = 4 * ur(); int rr = (int)ceil(cbrt(N) * 1.6) + 3; static int px[200000], py[200000], pz[200000]; static double pd[200000]; int m = 0;
      for (int x = -rr; x <= rr; x++) for (int y = -rr; y <= rr; y++) for (int z = -rr; z <= rr; z++) {
        int ok = ((x & 1) == 0 && (y & 1) == 0 && (z & 1) == 0 && (((x + y + z) % 4) + 4) % 4 == 0) || ((x & 1) && (y & 1) && (z & 1) && (((x + y + z) % 4) + 4) % 4 == 3);
        if (ok) { px[m] = x; py[m] = y; pz[m] = z; pd[m] = (x - ox) * (x - ox) + (y - oy) * (y - oy) + (z - oz) * (z - oz) + 1e-9 * ur(); m++; } }
      for (int i = 0; i < N; i++) { int b = i; for (int j = i + 1; j < m; j++) if (pd[j] < pd[b]) b = j;
        double t = pd[i]; pd[i] = pd[b]; pd[b] = t; int s = px[i]; px[i] = px[b]; px[b] = s; s = py[i]; py[i] = py[b]; py[b] = s; s = pz[i]; pz[i] = pz[b]; pz[b] = s;
        cx[i] = px[i]; cy[i] = py[i]; cz[i] = pz[i]; in[ID(cx[i], cy[i], cz[i])] = 1; }
      int B = 0; for (int i = 0; i < N; i++) B += deg(cx[i], cy[i], cz[i]); B /= 2;
      double T = 1.2; long steps = 20000 + 400L * N;
      for (long s = 0; s < steps; s++, T *= 0.99985) {
        int i = rnd() % N, j = rnd() % N, k = rnd() % 4, o[3]; nbr(cx[j], cy[j], cz[j], k, o);
        if (abs(o[0]) >= R - 2 || abs(o[1]) >= R - 2 || abs(o[2]) >= R - 2 || in[ID(o[0], o[1], o[2])]) continue;
        int di = deg(cx[i], cy[i], cz[i]); in[ID(cx[i], cy[i], cz[i])] = 0; int dn = deg(o[0], o[1], o[2]);
        int d = dn - di;
        if (d >= 0 || ur() < exp(d / (T + 1e-9))) { cx[i] = o[0]; cy[i] = o[1]; cz[i] = o[2]; in[ID(o[0], o[1], o[2])] = 1; B += d; }
        else in[ID(cx[i], cy[i], cz[i])] = 1;
        if (B > bestB && connected(N, cx, cy, cz)) { bestB = B; memcpy(bxx, cx, sizeof(int) * N); memcpy(byy, cy, sizeof(int) * N); memcpy(bzz, cz, sizeof(int) * N); } } }
    FILE *o = fopen(argv[5], "w"); for (int i = 0; i < N; i++) fprintf(o, "%d %d %d\n", bxx[i], byy[i], bzz[i]); fclose(o);
    printf("N=%d bonds %d dangling %d (%d restarts)\n", N, bestB, 4 * N - 2 * bestB, restarts); return 0; }
  return 2; }
