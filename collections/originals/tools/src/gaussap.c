/* Arithmetic progressions of Gaussian primes with the smallest largest norm (our own code, Quantavane Originals,
   problem gauss-prime-ap).
   cc -O2 -o gaussap gaussap.c
   ./gaussap exact K MMAX        for M = 2, 3, ..., MMAX: is there a K-term progression a + j d (j = 0..K-1, d != 0)
                                 of Gaussian primes all of norm <= M? Prints the least such M and one progression
                                 (exhaustive over first and second terms in the disc of norm M).
   ./gaussap fast K MMAX STEP    only common differences d that are multiples of STEP (a Gaussian integer "x,y"),
                                 one d per orbit of the 8 symmetries (units and conjugation: 0 <= arg d <= pi/4), every
                                 first term a: the least largest norm found up to MMAX (an upper bound unless every
                                 K-term progression must have such a d).
   ./gaussap big K MMAX STEP     as fast, without a list of primes (bit tables only, for large MMAX): every Gaussian
                                 prime a of norm <= MMAX is tried as first term with every d in the fundamental domain.
   ./gaussap through K MMAX STEP Q  progressions that contain the prime Q ("x,y") as a term, every common difference
                                 d that is a multiple of STEP (all directions), every position of Q: the least largest
                                 norm up to MMAX. With Q = 3,2 this covers, up to symmetry, every progression through a
                                 prime of norm 13 (one orbit under units and conjugation).
   A Gaussian integer x + yi is prime when xy != 0 and x^2 + y^2 is a prime, or when one of x, y is 0 and the other is
   +-p with p a prime congruent to 3 mod 4. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int R; static unsigned char *isp, *gp;   /* bit arrays: isp[n] for n <= 2R^2 + 2, gp[(x+R)*(2R+1)+(y+R)] */
#define BIT(a, i) ((a[(i) >> 3] >> ((i) & 7)) & 1)
#define SET(a, i) (a[(i) >> 3] |= (unsigned char)(1 << ((i) & 7)))
#define CLR(a, i) (a[(i) >> 3] &= (unsigned char)~(1 << ((i) & 7)))
static int G(int x, int y) { if (x < -R || x > R || y < -R || y > R) return 0; long i = (long)(x + R) * (2 * R + 1) + (y + R); return BIT(gp, i); }
int main(int argc, char **argv) {
  int K = atoi(argv[2]); long MMAX = atol(argv[3]); int sx = 1, sy = 0, restrict_d = 0;
  if (!strcmp(argv[1], "search") || !strcmp(argv[1], "fast") || !strcmp(argv[1], "big") || !strcmp(argv[1], "through")) { restrict_d = 1; sscanf(argv[4], "%d,%d", &sx, &sy); }
  R = 1; while ((long)R * R <= MMAX) R++;
  long PM = 2L * R * R + 2; isp = calloc(PM / 8 + 2, 1); for (long i = 2; i <= PM; i++) SET(isp, i);
  for (long i = 2; i * i <= PM; i++) if (BIT(isp, i)) for (long j = i * i; j <= PM; j += i) CLR(isp, j);
  gp = calloc((size_t)(2 * R + 1) * (2 * R + 1) / 8 + 2, 1);
  for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) { long nn = (long)x * x + (long)y * y; int p = 0;
    if (x != 0 && y != 0) p = BIT(isp, nn); else { long a = labs(x ? x : y); p = a > 0 && BIT(isp, a) && a % 4 == 3; }
    if (p) SET(gp, (long)(x + R) * (2 * R + 1) + (y + R)); }
  if (!strcmp(argv[1], "through")) {
    int qx, qy; sscanf(argv[5], "%d,%d", &qx, &qy); double rad = 2.0 * R / (K - 1) + 2; long bestM2 = -1; int A = 0, B = 0, DX = 0, DY = 0;
    for (int u = -(int)rad - 2; u <= (int)rad + 2; u++) for (int v = -(int)rad - 2; v <= (int)rad + 2; v++) {
      int dx = sx * u - sy * v, dy = sx * v + sy * u; if (dx == 0 && dy == 0) continue;
      if ((double)dx * dx + (double)dy * dy > rad * rad) continue;
      for (int p = 0; p < K; p++) { int ax = qx - p * dx, ay = qy - p * dy; long mx = 0; int ok = 1;
        for (int j = 0; j < K; j++) { int x = ax + j * dx, y = ay + j * dy; if (!G(x, y)) { ok = 0; break; }
          long nn = (long)x * x + (long)y * y; if (nn > mx) mx = nn; if (mx > MMAX || (bestM2 >= 0 && mx >= bestM2)) { ok = 0; break; } }
        if (ok) { bestM2 = mx; A = ax; B = ay; DX = dx; DY = dy; } } }
    if (bestM2 < 0) { printf("K=%d: no progression through %d%+di with norm <= %ld\n", K, qx, qy, MMAX); return 0; }
    printf("K=%d: through %d%+di: largest norm %ld: a = %d%+di, d = %d%+di\n", K, qx, qy, bestM2, A, B, DX, DY); return 0; }
  if (!strcmp(argv[1], "big")) {
    double rad = 2.0 * R / (K - 1) + 2; int nd = 0, *ddx = malloc(sizeof(int) * 4000000), *ddy = malloc(sizeof(int) * 4000000);
    for (int u = -(int)rad - 2; u <= (int)rad + 2; u++) for (int v = -(int)rad - 2; v <= (int)rad + 2; v++) {
      int dx = sx * u - sy * v, dy = sx * v + sy * u;
      if (dx <= 0 || dy < 0 || dy > dx || (double)dx * dx + (double)dy * dy > rad * rad) continue;
      if (nd < 4000000) { ddx[nd] = dx; ddy[nd] = dy; nd++; } }
    fprintf(stderr, "%d common differences\n", nd);
    long bestM2 = -1; int A = 0, B = 0, DX = 0, DY = 0;
    for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) { if (!G(x, y)) continue; long n0 = (long)x * x + (long)y * y; if (n0 > MMAX) continue;
      for (int t = 0; t < nd; t++) { int ok = 1; long mx = n0; if (bestM2 >= 0 && mx >= bestM2) break;
        for (int j = 1; j < K; j++) { int xx = x + j * ddx[t], yy = y + j * ddy[t]; if (!G(xx, yy)) { ok = 0; break; }
          long nn = (long)xx * xx + (long)yy * yy; if (nn > mx) mx = nn; if (mx > MMAX || (bestM2 >= 0 && mx >= bestM2)) { ok = 0; break; } }
        if (ok) { bestM2 = mx; A = x; B = y; DX = ddx[t]; DY = ddy[t]; fprintf(stderr, "  %ld\n", bestM2); } } }
    if (bestM2 < 0) { printf("K=%d: none found with norm <= %ld\n", K, MMAX); return 0; }
    printf("K=%d: largest norm %ld: a = %d%+di, d = %d%+di :", K, bestM2, A, B, DX, DY);
    for (int j = 0; j < K; j++) printf(" %d%+di", A + j * DX, B + j * DY); printf("\n"); return 0; }
  /* list of primes in the disc, sorted by norm (then by x, y) */
  int np = 0, cap = 1024, *px = malloc(sizeof(int) * cap), *py = malloc(sizeof(int) * cap);
  for (int x = -R; x <= R; x++) for (int y = -R; y <= R; y++) if (G(x, y) && (long)x * x + (long)y * y <= MMAX) {
    if (np == cap) { cap *= 2; px = realloc(px, sizeof(int) * cap); py = realloc(py, sizeof(int) * cap); } px[np] = x; py[np] = y; np++; }
  { long *key = malloc(sizeof(long) * np); int *ord = malloc(sizeof(int) * np), *qx = malloc(sizeof(int) * np), *qy = malloc(sizeof(int) * np);
    for (int i = 0; i < np; i++) { key[i] = ((long)px[i] * px[i] + (long)py[i] * py[i]) * 4000000L + (long)(px[i] + R) * 2000L + (py[i] + R); ord[i] = i; }
    /* heap sort of ord by key */
    for (int i = 1; i < np; i++) { int c = i; while (c > 0) { int p = (c - 1) / 2; if (key[ord[p]] < key[ord[c]]) { int t = ord[p]; ord[p] = ord[c]; ord[c] = t; c = p; } else break; } }
    for (int end = np - 1; end > 0; end--) { int t = ord[0]; ord[0] = ord[end]; ord[end] = t; int c = 0;
      while (1) { int l = 2 * c + 1, r = l + 1, m = c; if (l < end && key[ord[l]] > key[ord[m]]) m = l; if (r < end && key[ord[r]] > key[ord[m]]) m = r; if (m == c) break; t = ord[c]; ord[c] = ord[m]; ord[m] = t; c = m; } }
    for (int i = 0; i < np; i++) { qx[i] = px[ord[i]]; qy[i] = py[ord[i]]; } free(px); free(py); px = qx; py = qy; free(key); free(ord); }
  if (!strcmp(argv[1], "fast")) {
    long bestM2 = -1; int A = 0, B = 0, DX = 0, DY = 0; double rad = 2.0 * R / (K - 1) + 2;
    for (int u = -(int)rad - 2; u <= (int)rad + 2; u++) for (int v = -(int)rad - 2; v <= (int)rad + 2; v++) {
      int dx = sx * u - sy * v, dy = sx * v + sy * u;              /* d = (sx + sy i)(u + v i) */
      if (dx <= 0 || dy < 0 || dy > dx) continue;                   /* one d per symmetry orbit */
      if ((double)dx * dx + (double)dy * dy > rad * rad) continue;
      for (int i = 0; i < np; i++) { long mx = (long)px[i] * px[i] + (long)py[i] * py[i]; int ok = 1;
        if (bestM2 >= 0 && mx >= bestM2) continue;
        for (int j = 1; j < K; j++) { int x = px[i] + j * dx, y = py[i] + j * dy; if (!G(x, y)) { ok = 0; break; }
          long nn = (long)x * x + (long)y * y; if (nn > mx) mx = nn; if (mx > MMAX || (bestM2 >= 0 && mx >= bestM2)) { ok = 0; break; } }
        if (ok) { bestM2 = mx; A = px[i]; B = py[i]; DX = dx; DY = dy; } } }
    if (bestM2 < 0) { printf("K=%d: none found with norm <= %ld\n", K, MMAX); return 0; }
    printf("K=%d: largest norm %ld: a = %d%+di, d = %d%+di :", K, bestM2, A, B, DX, DY);
    for (int j = 0; j < K; j++) printf(" %d%+di", A + j * DX, B + j * DY); printf("\n"); return 0; }
  /* scan: for each M, the progressions whose largest norm is exactly M are found when the prime of norm M is the
     largest; simpler: grow M over the primes in norm order and test progressions within norm <= M */
  long bestM = -1; int ba = 0, bb = 0, bdx = 0, bdy = 0;
  for (int i = 0; i < np && bestM < 0; i++) { long M = (long)px[i] * px[i] + (long)py[i] * py[i];
    /* progressions containing prime i as their largest-norm term at position j0 */
    for (int t = 0; t <= i && bestM < 0; t++) { if (t == i) continue; int dx = px[t] - px[i], dy = py[t] - py[i];
      /* d' = (other - this): treat this prime as an end or interior term: the progression is this + s*d for s in a
         window; try every step d that is (other - this)/m for m = 1..K-1 */
      for (int m = 1; m < K && bestM < 0; m++) { if (dx % m || dy % m) continue; int ex = dx / m, ey = dy / m;
        if (restrict_d) { /* (ex + ey i) / (sx + sy i) must be a Gaussian integer */ long nn = (long)sx * sx + (long)sy * sy;
          long re = (long)ex * sx + (long)ey * sy, im = (long)ey * sx - (long)ex * sy; if (re % nn || im % nn) continue; }
        for (int start = -(K - 1); start <= 0 && bestM < 0; start++) { /* this prime is term -start */
          int ok = 1; for (int j = 0; j < K; j++) { int x = px[i] + (start + j) * ex, y = py[i] + (start + j) * ey;
            if (!G(x, y) || (long)x * x + (long)y * y > M) { ok = 0; break; } }
          if (ok) { bestM = M; ba = px[i] + start * ex; bb = py[i] + start * ey; bdx = ex; bdy = ey; } } } } }
  if (bestM < 0) { printf("K=%d: none with norm <= %ld\n", K, MMAX); return 0; }
  printf("K=%d: least largest norm %ld: a = %d%+di, d = %d%+di :", K, bestM, ba, bb, bdx, bdy);
  for (int j = 0; j < K; j++) printf(" %d%+di", ba + j * bdx, bb + j * bdy); printf("\n"); return 0; }
