/* qcode_enum.c: the weight distribution of the F_p-span of a few vectors whose coordinates are groups of D digits
   in F_p (the helper of qcode_check.py, which reads and checks the code and does everything else).

     qcode_enum < BASIS

   BASIS (text): "p n D r" and then r lines of n*D digits 0..p-1 (coordinate 0's D digits, then coordinate 1's, ...).
   The weight of a vector is the number of coordinates with a nonzero digit. Prints "A w count" for w = 0..n (every
   vector of the span, the zero vector included, counted once; the r vectors must be independent, which qcode_check.py
   ensures) and "visits V".

   p = 2: every vector of the span is visited once in Gray-code order (one XOR of the packed planes per step).
   p odd: every line through the origin is visited once (the vectors whose first nonzero coefficient is 1, stepped
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
        uint64_t *gp = calloc((size_t)(r ? r : 1) * D * W, sizeof(uint64_t));
        uint64_t *cur = calloc((size_t)D * W, sizeof(uint64_t));
        for (int j = 0; j < r; j++)
            for (int i = 0; i < n; i++)
                for (int d = 0; d < D; d++)
                    if (g[(size_t)j * L + (size_t)i * D + d]) gp[((size_t)j * D + d) * W + i / 64] |= 1ULL << (i % 64);
        A[0] = 1;
        uint64_t total = r ? (1ULL << r) : 1;
        for (uint64_t s = 1; s < total; s++) {
            int j = __builtin_ctzll(s);
            const uint64_t *v = gp + (size_t)j * D * W;
            for (int x = 0; x < D * W; x++) cur[x] ^= v[x];
            int w = 0;
            for (int x = 0; x < W; x++) {
                uint64_t o = 0;
                for (int d = 0; d < D; d++) o |= cur[d * W + x];
                w += __builtin_popcountll(o);
            }
            A[w]++;
        }
        visits = total;
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
