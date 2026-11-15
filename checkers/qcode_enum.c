/* qcode_enum.c: the weight distribution of the F_p-span of a few vectors whose coordinates are groups of D digits
   in F_p (the helper of qcode_check.py, which reads and checks the code and does everything else).

     qcode_enum < BASIS

   BASIS (text): "p n D r" and then r lines of n*D digits 0..p-1 (coordinate 0's D digits, then coordinate 1's, ...).
   The weight of a vector is the number of coordinates with a nonzero digit. Prints "A w count" for w = 0..n (every
   vector of the span, the zero vector included, counted once; the r vectors must be independent, which qcode_check.py
   ensures) and "visits V".

   p = 2: every vector of the span is visited once. The combinations of the last L <= 10 vectors are tabulated once
   (2^L entries of packed bit planes); the other r - L vectors are stepped through in Gray-code order (one XOR per
   step), and at each step the weights of the 2^L sums with the table are taken in one loop the compiler vectorizes
   (XOR, OR of the planes, popcount), then counted into four interleaved histograms (15 Nov 2026; before, one Gray
   step per vector).
   p = 3: bit-sliced, with a table of the combinations of the last generators (15 Nov 2026; see the code), unless the
   environment variable QCODE_ENUM_PLAIN is set.
   p odd (or QCODE_ENUM_PLAIN): every line through the origin is visited once (the vectors whose first nonzero coefficient is 1, stepped
   through like an odometer), and its weight counted p - 1 times (all nonzero multiples have the same weight). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static void die(const char *m) { fprintf(stderr, "qcode_enum: %s\n", m); exit(1); }

static void add_mod(unsigned char *restrict cur, const unsigned char *restrict v, int L, unsigned char p) {
    for (int c = 0; c < L; c++) {
        unsigned char t = (unsigned char)(cur[c] + v[c]);
        cur[c] = (unsigned char)(t - (t >= p ? p : 0));
    }
}

static int weight2(const unsigned char *restrict x, const unsigned char *restrict z, int n) {
    int w = 0;
    for (int i = 0; i < n; i++) w += (x[i] | z[i]) != 0;
    return w;
}

int main(void) {
    int p, n, D, r;
    if (scanf("%d %d %d %d", &p, &n, &D, &r) != 4) die("bad header");
    if (p < 2 || p > 7 || n < 1 || n > 4096 || D < 1 || D > 16 || r < 0 || r > 62) die("header out of range");
    int L = n * D;
    unsigned char *g = malloc((size_t)(r ? r : 1) * L);
    if (!g) die("out of memory");
    for (int j = 0; j < r; j++)
        for (int c = 0; c < L; c++) {
            int x;
            if (scanf("%d", &x) != 1 || x < 0 || x >= p) die("bad digit");
            g[(size_t)j * L + c] = (unsigned char)x;
        }
    uint64_t *A = calloc((size_t)n + 1, sizeof(uint64_t));
    uint64_t visits = 0;
    if (p == 2) {
        int W = (n + 63) / 64;                     /* plane d of vector j: words gp[(j*D + d)*W ...] */
        int PW = D * W;
        uint64_t *gp = calloc((size_t)(r ? r : 1) * PW, sizeof(uint64_t));
        for (int j = 0; j < r; j++)
            for (int i = 0; i < n; i++)
                for (int d = 0; d < D; d++)
                    if (g[(size_t)j * L + (size_t)i * D + d]) gp[((size_t)j * D + d) * W + i / 64] |= 1ULL << (i % 64);
        int LO = r < 10 ? r : 10, HI = r - LO;     /* the last LO vectors are tabulated */
        size_t T = (size_t)1 << LO;
        /* table, entry-major by word: tab[(d*W + x) * T + i] = word x of plane d of the i-th combination */
        uint64_t *tab = calloc((size_t)PW * T, sizeof(uint64_t));
        uint64_t *cur = calloc((size_t)PW, sizeof(uint64_t));
        uint16_t *wt = malloc(T * sizeof(uint16_t));
        uint64_t *H4 = calloc((size_t)4 * (n + 1), sizeof(uint64_t));
        if (!gp || !tab || !cur || !wt || !H4) die("out of memory");
        for (size_t i = 1; i < T; i++) {
            int j = HI + __builtin_ctzll(i);
            size_t prev = i & (i - 1);
            for (int y = 0; y < PW; y++) tab[(size_t)y * T + i] = tab[(size_t)y * T + prev] ^ gp[(size_t)j * PW + y];
        }
        uint64_t steps = (uint64_t)1 << HI;
        for (uint64_t s = 0; s < steps; s++) {
            if (s) {
                int j = __builtin_ctzll(s);
                for (int y = 0; y < PW; y++) cur[y] ^= gp[(size_t)j * PW + y];
            }
            if (PW == 2) {                         /* qubits, n <= 64: the common case, written out */
                const uint64_t cx = cur[0], cz = cur[1], *tx = tab, *tz = tab + T;
                for (size_t i = 0; i < T; i++) wt[i] = (uint16_t)__builtin_popcountll((cx ^ tx[i]) | (cz ^ tz[i]));
            }
#define WEIGHTS(DD, WW)                                                                                          \
            else if (D == DD && W == WW) {                                                                       \
                for (size_t i = 0; i < T; i++) {                                                                 \
                    int w = 0;                                                                                   \
                    for (int x = 0; x < WW; x++) {                                                               \
                        uint64_t o = 0;                                                                          \
                        for (int d = 0; d < DD; d++) o |= cur[d * WW + x] ^ tab[(size_t)(d * WW + x) * T + i];   \
                        w += __builtin_popcountll(o);                                                            \
                    }                                                                                            \
                    wt[i] = (uint16_t)w;                                                                         \
                }                                                                                                \
            }
            WEIGHTS(2, 2) WEIGHTS(2, 3) WEIGHTS(2, 4) WEIGHTS(4, 1) WEIGHTS(4, 2) WEIGHTS(6, 1) WEIGHTS(6, 2)
            else {
                memset(wt, 0, T * sizeof(uint16_t));
                for (int x = 0; x < W; x++) {
                    uint64_t c0 = cur[x];
                    const uint64_t *t0 = tab + (size_t)x * T;
                    for (size_t i = 0; i < T; i++) {
                        uint64_t o = c0 ^ t0[i];
                        for (int d = 1; d < D; d++) o |= cur[d * W + x] ^ tab[((size_t)d * W + x) * T + i];
                        wt[i] = (uint16_t)(wt[i] + __builtin_popcountll(o));
                    }
                }
            }
            size_t i = 0;
            for (; i + 4 <= T; i += 4) {
                H4[wt[i]]++; H4[(n + 1) + wt[i + 1]]++; H4[2 * (n + 1) + wt[i + 2]]++; H4[3 * (n + 1) + wt[i + 3]]++;
            }
            for (; i < T; i++) H4[wt[i]]++;
        }
        for (int w = 0; w <= n; w++) A[w] = H4[w] + H4[(n + 1) + w] + H4[2 * (n + 1) + w] + H4[3 * (n + 1) + w];
        visits = steps * T;
    } else if (p == 3 && D == 2 && !getenv("QCODE_ENUM_PLAIN")) {
        /* GF(3), bit-sliced: a digit is kept as two bits (is 1, is 2) across 64 coordinates; the six planes of a
           vector are X==1, X==2, X==0, Z==1, Z==2, Z==0 (the "==0" planes are 1 beyond n, so padding never counts).
           a + b is zero where (a0 & b0) | (a1 & b2) | (a2 & b1). The combinations of the last LO <= 7 generators are
           tabulated (3^LO entries); the lines of the span of the others are stepped through as before (first
           nonzero coefficient 1, an odometer), and each is added to every table entry: a vector with a nonzero
           first part is counted p - 1 = 2 times (its multiples), the table entries themselves once. */
        int W = (n + 63) / 64, PW = 6 * W;
        uint64_t *gb = calloc((size_t)(r ? r : 1) * PW, sizeof(uint64_t));
        if (!gb) die("out of memory");
        for (int j = 0; j < r; j++) {
            uint64_t *v = gb + (size_t)j * PW;
            for (int x = 0; x < W; x++) { v[2 * W + x] = ~0ULL; v[5 * W + x] = ~0ULL; }
            for (int i = 0; i < n; i++) {
                int dx = g[(size_t)j * L + (size_t)i * 2], dz = g[(size_t)j * L + (size_t)i * 2 + 1];
                uint64_t bit = 1ULL << (i % 64);
                int x = i / 64;
                if (dx) { v[(dx - 1) * W + x] |= bit; v[2 * W + x] &= ~bit; }
                if (dz) { v[(3 + dz - 1) * W + x] |= bit; v[5 * W + x] &= ~bit; }
            }
        }
        int LO = r < 7 ? r : 7, HI = r - LO;
        size_t T = 1;
        for (int j = 0; j < LO; j++) T *= 3;
        uint64_t *tab = malloc((size_t)PW * T * sizeof(uint64_t));      /* plane-major: tab[y * T + i] */
        uint64_t *cur = malloc((size_t)PW * sizeof(uint64_t)), *tmp = malloc((size_t)PW * sizeof(uint64_t));
        uint16_t *wt = malloc(T * sizeof(uint16_t));
        uint64_t *H4 = calloc((size_t)4 * (n + 1), sizeof(uint64_t));
        int *dig = calloc(r ? r : 1, sizeof(int));
        if (!tab || !cur || !tmp || !wt || !H4 || !dig) die("out of memory");
#define ADD3(out, a, b, W_)                                                                                       \
        for (int h_ = 0; h_ < 2; h_++)                                                                            \
            for (int x = 0; x < (W_); x++) {                                                                      \
                uint64_t a1 = (a)[(3 * h_) * (W_) + x], a2 = (a)[(3 * h_ + 1) * (W_) + x], a0 = (a)[(3 * h_ + 2) * (W_) + x]; \
                uint64_t b1 = (b)[(3 * h_) * (W_) + x], b2 = (b)[(3 * h_ + 1) * (W_) + x], b0 = (b)[(3 * h_ + 2) * (W_) + x]; \
                uint64_t s1 = (a1 & b0) | (a0 & b1) | (a2 & b2), s2 = (a2 & b0) | (a0 & b2) | (a1 & b1);           \
                (out)[(3 * h_) * (W_) + x] = s1; (out)[(3 * h_ + 1) * (W_) + x] = s2;                             \
                (out)[(3 * h_ + 2) * (W_) + x] = ~(s1 | s2);                                                      \
            }
        for (int y = 0; y < PW; y++) tab[(size_t)y * T] = (y / W) % 3 == 2 ? ~0ULL : 0;   /* entry 0: the zero vector */
        for (size_t i = 1; i < T; i++) {          /* entry i = entry (i - 3^j) + generator HI + j, j its lowest nonzero digit */
            size_t pw = 1; int j = 0;
            while ((i / pw) % 3 == 0) { pw *= 3; j++; }
            for (int y = 0; y < PW; y++) tmp[y] = tab[(size_t)y * T + (i - pw)];
            ADD3(cur, tmp, gb + (size_t)(HI + j) * PW, W)
            for (int y = 0; y < PW; y++) tab[(size_t)y * T + i] = cur[y];
        }
        /* weights of cur + every table entry into wt */
#define WEIGHTS3(W_)                                                                                              \
        for (size_t i = 0; i < T; i++) {                                                                          \
            int w = 0;                                                                                            \
            for (int x = 0; x < (W_); x++) {                                                                      \
                uint64_t zx = (cur[2 * (W_) + x] & tab[(size_t)(2 * (W_) + x) * T + i])                           \
                            | (cur[x] & tab[(size_t)((W_) + x) * T + i]) | (cur[(W_) + x] & tab[(size_t)x * T + i]); \
                uint64_t zz = (cur[5 * (W_) + x] & tab[(size_t)(5 * (W_) + x) * T + i])                           \
                            | (cur[3 * (W_) + x] & tab[(size_t)(4 * (W_) + x) * T + i])                           \
                            | (cur[4 * (W_) + x] & tab[(size_t)(3 * (W_) + x) * T + i]);                          \
                w += __builtin_popcountll(~(zx & zz));                                                            \
            }                                                                                                     \
            wt[i] = (uint16_t)w;                                                                                  \
        }
#define COUNT3(mult)                                                                                              \
        {                                                                                                         \
            if (W == 1) { WEIGHTS3(1) } else if (W == 2) { WEIGHTS3(2) } else { WEIGHTS3(W) }                     \
            size_t i = 0;                                                                                         \
            for (; i + 4 <= T; i += 4) {                                                                          \
                H4[wt[i]] += mult; H4[(n + 1) + wt[i + 1]] += mult;                                               \
                H4[2 * (n + 1) + wt[i + 2]] += mult; H4[3 * (n + 1) + wt[i + 3]] += mult;                          \
            }                                                                                                     \
            for (; i < T; i++) H4[wt[i]] += mult;                                                                 \
            visits += T;                                                                                          \
        }
        for (int y = 0; y < PW; y++) cur[y] = (y / W) % 3 == 2 ? ~0ULL : 0;      /* first part zero: the table once */
        COUNT3(1)
        for (int lead = 0; lead < HI; lead++) {   /* first part nonzero, first nonzero coefficient 1 */
            memcpy(cur, gb + (size_t)lead * PW, (size_t)PW * sizeof(uint64_t));
            for (int j = lead + 1; j < HI; j++) dig[j] = 0;
            for (;;) {
                COUNT3(2)
                int j = lead + 1;
                for (; j < HI; j++) {
                    memcpy(tmp, cur, (size_t)PW * sizeof(uint64_t));
                    ADD3(cur, tmp, gb + (size_t)j * PW, W)
                    if (++dig[j] < 3) break;
                    dig[j] = 0;
                }
                if (j == HI) break;
            }
        }
        for (int w = 0; w <= n; w++) A[w] = H4[w] + H4[(n + 1) + w] + H4[2 * (n + 1) + w] + H4[3 * (n + 1) + w];
    } else {
        /* plane-major copy: digit d of coordinate i at d*n + i, so the weight loop runs over coordinates */
        unsigned char *gq = malloc((size_t)(r ? r : 1) * L);
        for (int j = 0; j < r; j++)
            for (int i = 0; i < n; i++)
                for (int d = 0; d < D; d++) gq[(size_t)j * L + (size_t)d * n + i] = g[(size_t)j * L + (size_t)i * D + d];
        unsigned char *cur = malloc(L);
        int *dig = calloc(r ? r : 1, sizeof(int));
        A[0] = 1;
        for (int lead = 0; lead < r; lead++) {
            memcpy(cur, gq + (size_t)lead * L, L);
            for (int j = lead + 1; j < r; j++) dig[j] = 0;
            for (;;) {
                int w = 0;
                if (D == 2) {                         /* the only case for odd p (GF(3), GF(5), GF(7)) */
                    w = weight2(cur, cur + n, n);
                } else {
                    for (int i = 0; i < n; i++) {
                        unsigned char o = 0;
                        for (int d = 0; d < D; d++) o |= cur[d * n + i];
                        w += o != 0;
                    }
                }
                A[w] += (uint64_t)(p - 1);
                visits++;
                int j = lead + 1;
                for (; j < r; j++) {                  /* odometer: add vector j once; carry when its digit wraps */
                    add_mod(cur, gq + (size_t)j * L, L, (unsigned char)p);
                    if (++dig[j] < p) break;
                    dig[j] = 0;
                }
                if (j == r) break;
            }
        }
    }
    for (int w = 0; w <= n; w++) printf("A %d %llu\n", w, (unsigned long long)A[w]);
    printf("visits %llu\n", (unsigned long long)visits);
    return 0;
}
