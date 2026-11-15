/* ds_scan.c: count the differences of a subset of an abelian group (the helper of ds_check.py for large sets;
   ds_check.py reads and checks the elements first).

     ds_scan LAMBDA [plain] < INPUT

   INPUT: r, then n_1 ... n_r (the group Z_n1 x ... x Z_nr, at most 2^31 elements), then k, then k elements, each r
   integers 0 <= a_c < n_c. For every ordered pair i != j the difference d_i - d_j is counted, in an array indexed by
   its mixed-radix rank. Prints "pairs P" (k(k-1)), "zero Z" (pairs whose difference is 0, that is, repeated
   elements), "bad B" (nonzero elements not hit exactly LAMBDA times) and "first F" (the rank of the first such
   element in Z_n1 x ... x Z_nr, or -1), and "method M".

   Methods. The group is first rewritten by the Chinese remainder theorem as Z_f1 x ... x Z_fs with f_1 | ... | f_s
   (its invariant factors; s is the largest number of cyclic factors of one prime). Then
     xor     every f_i = 2: the difference of two ranks is their XOR;
     cyclic  s = 1: the difference of two ranks modulo f_1;
     padded  each element x gets the rank P(x) = sum x_i W_i with the radices 2 f_i - 1, so that P(a) - P(b) + O
             (O = sum (f_i - 1) W_i) is, digit by digit and with no borrow, the rank of a_i - b_i + f_i - 1 in
             [0, 2 f_i - 2]: one subtraction per pair into a table of prod (2 f_i - 1) entries (at most 2^26), folded
             onto the group at the end;
     plain   otherwise (or when asked): each difference digit by digit.
   Every method counts the same multiset of differences; the tests compare them with each other and with Python. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static void die(const char *m) { fprintf(stderr, "ds_scan: %s\n", m); exit(2); }

static long long egcd_inv(long long a, long long m) {          /* a^-1 mod m, gcd(a, m) = 1 */
    long long g = m, x = 0, x1 = 1, a1 = a % m;
    if (a1 < 0) a1 += m;
    long long b = a1;
    while (b) { long long q = g / b, t = g - q * b; g = b; b = t; t = x - q * x1; x = x1; x1 = t; }
    if (g != 1) die("not invertible");
    x %= m;
    return x < 0 ? x + m : x;
}

int main(int argc, char **argv) {
    if (argc != 2 && argc != 3) die("usage: ds_scan LAMBDA [plain] < INPUT");
    long long lambda = atoll(argv[1]);
    int force_plain = argc == 3 && strcmp(argv[2], "plain") == 0;
    int r;
    if (scanf("%d", &r) != 1 || r < 1 || r > 64) die("bad rank");
    long long n[64], w[64], v = 1;
    for (int c = 0; c < r; c++) {
        if (scanf("%lld", &n[c]) != 1 || n[c] < 1) die("bad order");
        v *= n[c];
        if (v > (1LL << 31)) die("group too large");
    }
    long long acc = 1;
    for (int c = r - 1; c >= 0; c--) { w[c] = acc; acc *= n[c]; }
    long k;
    if (scanf("%ld", &k) != 1 || k < 1 || k > v) die("bad k");
    long long *in = malloc(sizeof(long long) * (size_t)k * r);
    if (!in) die("out of memory");
    for (long i = 0; i < k; i++)
        for (int c = 0; c < r; c++) {
            long long a;
            if (scanf("%lld", &a) != 1 || a < 0 || a >= n[c]) die("bad element");
            in[i * r + c] = a;
        }
    /* invariant factors: split each n_c into prime powers; the i-th factor takes the i-th largest power of each prime */
    long long pp[64 * 32]; int ppc[64 * 32], ppk[64 * 32]; long long prm[64 * 32]; int npp = 0;
    for (int c = 0; c < r; c++) {
        long long x = n[c];
        for (long long p = 2; p * p <= x; p++)
            if (x % p == 0) { long long q = 1; while (x % p == 0) { x /= p; q *= p; } prm[npp] = p; pp[npp] = q; ppc[npp++] = c; }
        if (x > 1) { prm[npp] = x; pp[npp] = x; ppc[npp++] = c; }
    }
    for (int i = 0; i < npp; i++) {                     /* rank of this power among the powers of its prime */
        int rk = 0;
        for (int j = 0; j < npp; j++)
            if (prm[j] == prm[i] && (pp[j] > pp[i] || (pp[j] == pp[i] && j < i))) rk++;
        ppk[i] = rk;
    }
    int s = 0;
    for (int i = 0; i < npp; i++) if (ppk[i] + 1 > s) s = ppk[i] + 1;
    long long f[64];
    for (int i = 0; i < s; i++) f[i] = 1;
    for (int i = 0; i < npp; i++) f[ppk[i]] *= pp[i];
    /* element coordinates in Z_f: x_i = sum over the powers q in factor i of (a mod q) M (M^-1 mod q), M = f_i / q */
    long long *el = malloc(sizeof(long long) * (size_t)k * (s ? s : 1));
    if (!el) die("out of memory");
    long long coef[64 * 32];
    for (int i = 0; i < npp; i++) { long long M = f[ppk[i]] / pp[i]; coef[i] = (M % f[ppk[i]]) * egcd_inv(M, pp[i]) % f[ppk[i]]; }
    for (long e = 0; e < k; e++) {
        for (int i = 0; i < s; i++) el[e * s + i] = 0;
        for (int i = 0; i < npp; i++) {
            long long fi = f[ppk[i]];
            __int128 t = (__int128)(in[e * r + ppc[i]] % pp[i]) * coef[i] + el[e * s + ppk[i]];
            el[e * s + ppk[i]] = (long long)(t % fi);
        }
    }
    long long wf[64];
    acc = 1;
    for (int i = s - 1; i >= 0; i--) { wf[i] = acc; acc *= f[i]; }
    if (acc != v) die("invariant factors");
    uint32_t *cnt = calloc((size_t)v, sizeof(uint32_t));
    uint32_t *rank = malloc(sizeof(uint32_t) * (size_t)k);
    if (!cnt || !rank) die("out of memory");
    for (long e = 0; e < k; e++) {
        long long x = 0;
        for (int i = 0; i < s; i++) x += el[e * s + i] * wf[i];
        rank[e] = (uint32_t)x;
    }
    int all2 = 1;
    for (int i = 0; i < s; i++) all2 &= f[i] == 2;
    long long padsize = 1;
    for (int i = 0; i < s; i++) { padsize *= 2 * f[i] - 1; if (padsize > (1LL << 26)) break; }
    const char *method;
    if (force_plain) method = "plain";
    else if (all2) method = "xor";
    else if (s == 1) method = "cyclic";
    else if (padsize <= (1LL << 26)) method = "padded";
    else method = "plain";
    if (!strcmp(method, "xor")) {
        for (long i = 0; i < k; i++)
            for (long j = 0; j < k; j++)
                if (i != j) cnt[rank[i] ^ rank[j]]++;
    } else if (!strcmp(method, "cyclic")) {
        uint32_t vv = (uint32_t)v;
        for (long i = 0; i < k; i++) {
            uint32_t a = rank[i];
            for (long j = 0; j < k; j++) {
                if (i == j) continue;
                uint32_t b = rank[j];
                cnt[a >= b ? a - b : a + vv - b]++;
            }
        }
    } else if (!strcmp(method, "padded")) {
        long long W[64], off = 0;
        acc = 1;
        for (int i = s - 1; i >= 0; i--) { W[i] = acc; off += (f[i] - 1) * acc; acc *= 2 * f[i] - 1; }
        uint32_t *T = calloc((size_t)padsize, sizeof(uint32_t));
        int64_t *P = malloc(sizeof(int64_t) * (size_t)k);
        if (!T || !P) die("out of memory");
        for (long e = 0; e < k; e++) { int64_t x = 0; for (int i = 0; i < s; i++) x += el[e * s + i] * W[i]; P[e] = x; }
        for (long i = 0; i < k; i++) {
            uint32_t *base = T + (P[i] + off);
            for (long j = 0; j < k; j++)
                if (i != j) base[-P[j]]++;
        }
        /* fold: padded digit t_i in [0, 2 f_i - 2] stands for (t_i - f_i + 1) mod f_i */
        int dgt[64];
        for (int i = 0; i < s; i++) dgt[i] = 0;
        for (long long x = 0; x < padsize; x++) {
            if (T[x]) {
                long long g = 0;
                for (int i = 0; i < s; i++) {
                    long long d = dgt[i] - (f[i] - 1);
                    if (d < 0) d += f[i];
                    g += d * wf[i];
                }
                cnt[g] += T[x];
            }
            for (int i = s - 1; i >= 0; i--) { if (++dgt[i] < 2 * f[i] - 1) break; dgt[i] = 0; }
        }
        free(T); free(P);
    } else {                                           /* plain, in the input's own coordinates */
        memset(cnt, 0, sizeof(uint32_t) * (size_t)v);
        for (long i = 0; i < k; i++) {
            const long long *a = in + i * r;
            for (long j = 0; j < k; j++) {
                if (i == j) continue;
                const long long *b = in + j * r;
                long long x = 0;
                for (int c = 0; c < r; c++) {
                    long long d = a[c] - b[c];
                    if (d < 0) d += n[c];
                    x += d * w[c];
                }
                cnt[x]++;
            }
        }
    }
    /* report in the input's coordinates: the first bad element is searched in input rank order */
    long long bad = 0, first = -1, zero = 0;
    int plain = !strcmp(method, "plain");
    if (plain) {
        zero = cnt[0];
        for (long long x = 1; x < v; x++) if (cnt[x] != (uint64_t)lambda) { bad++; if (first < 0) first = x; }
    } else {
        zero = cnt[0];
        int dg[64];
        for (int c = 0; c < r; c++) dg[c] = 0;
        for (long long x = 0; x < v; x++) {               /* x = input rank; map to the invariant rank */
            if (x) {
                long long g = 0;
                for (int i = 0; i < s; i++) {
                    long long t = 0;
                    for (int q = 0; q < npp; q++)
                        if (ppk[q] == i) t = (long long)(((__int128)(dg[ppc[q]] % pp[q]) * coef[q] + t) % f[i]);
                    g += t * wf[i];
                }
                if (cnt[g] != (uint64_t)lambda) { bad++; if (first < 0) first = x; }
            }
            for (int c = r - 1; c >= 0; c--) { if (++dg[c] < n[c]) break; dg[c] = 0; }
        }
    }
    printf("pairs %lld\nzero %lld\nbad %lld\nfirst %lld\nmethod %s\n", (long long)k * (k - 1), zero, bad, first, method);
    return 0;
}
