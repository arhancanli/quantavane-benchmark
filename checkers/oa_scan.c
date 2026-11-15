/* oa_scan.c: is an array an ordered orthogonal array of strength k? (the helper of oa_check.py, which reads and checks
   the array first)

     oa_scan < INPUT

   INPUT: "b N s D t k", then N runs, each s * D symbols 0..b-1 (factor after factor, D coordinates per factor in order
   of depth). For every depth vector (d_1, ..., d_s), 0 <= d_i <= t, d_1 + ... + d_s = k, the runs' symbols in the
   first d_i coordinates of each factor are read as a number below b^k (factors in order, sharing the part of the
   chosen factors so far), and each of the b^k values must occur exactly N / b^k times. Prints "uniform L" (L depth
   vectors, all uniform) or "skewed (i,d) ..." (1-based factor and depth of a non-uniform depth vector) and "work W". */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int b, s, D, t, k;
static long N;
static uint8_t *a;              /* a[run * s * D + factor * D + coordinate] */
static uint32_t *part;          /* part[level * N + run] */
static uint32_t *cnt;
static uint64_t bk, want, leaves = 0, work = 0;
static int cf[64], cd[64];

static int rec(int start, int r, int level) {
    for (int f = start; f < s; f++) {
        if ((long)(s - f) * t < r) return 0;
        const uint32_t *p = part + (size_t)level * N;
        uint32_t *q = part + (size_t)(level + 1) * N;
        int lim = t < r ? t : r;
        for (int d = 1; d <= lim; d++) {
            const uint32_t *src = d == 1 ? p : q;
            for (long run = 0; run < N; run++)
                q[run] = src[run] * (uint32_t)b + a[(size_t)run * s * D + (size_t)f * D + d - 1];
            work += (uint64_t)N;
            cf[level] = f + 1;
            cd[level] = d;
            if (r - d == 0) {
                memset(cnt, 0, bk * sizeof(uint32_t));
                for (long run = 0; run < N; run++) cnt[q[run]]++;
                leaves++;
                for (uint64_t x = 0; x < bk; x++)
                    if (cnt[x] != want) {
                        printf("skewed");
                        for (int l = 0; l <= level; l++) printf(" (%d,%d)", cf[l], cd[l]);
                        printf("\n");
                        return 1;
                    }
            } else if (rec(f + 1, r - d, level + 1)) {   /* deeper calls write only above level + 1: q stays */
                return 1;
            }
        }
    }
    return 0;
}

int main(void) {
    if (scanf("%d %ld %d %d %d %d", &b, &N, &s, &D, &t, &k) != 6) { fprintf(stderr, "oa_scan: bad header\n"); return 1; }
    if (b < 2 || b > 256 || N < 1 || s < 1 || D < 1 || t < 1 || t > D || k < 1 || k > 64) { fprintf(stderr, "oa_scan: header out of range\n"); return 1; }
    double bkd = 1;
    for (int i = 0; i < k; i++) bkd *= b;
    if (bkd > 4294967295.0 || bkd > (double)N) { fprintf(stderr, "oa_scan: b^k too large\n"); return 1; }
    bk = (uint64_t)bkd;
    if ((uint64_t)N % bk) { printf("skewed: N is not a multiple of b^k\nwork 0\n"); return 0; }
    want = (uint64_t)N / bk;
    a = malloc((size_t)N * s * D);
    part = calloc((size_t)(k + 2) * N, sizeof(uint32_t));
    cnt = malloc(bk * sizeof(uint32_t));
    if (!a || !part || !cnt) { fprintf(stderr, "oa_scan: out of memory\n"); return 1; }
    for (long run = 0; run < N; run++)
        for (long c = 0; c < (long)s * D; c++) {
            int x;
            if (scanf("%d", &x) != 1 || x < 0 || x >= b) { fprintf(stderr, "oa_scan: bad symbol\n"); return 1; }
            a[(size_t)run * s * D + c] = (uint8_t)x;
        }
    int bad = rec(0, k, 0);
    if (!bad) printf("uniform %llu\n", (unsigned long long)leaves);
    printf("work %llu\n", (unsigned long long)work);
    return 0;
}
