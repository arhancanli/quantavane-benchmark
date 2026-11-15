/* ca_scan.c: is an array a covering array of strength t? (the helper of ca_check.py for large arrays; ca_check.py
   reads and checks the rows first).

     ca_scan < ARRAY

   ARRAY: "t k v n", then n rows of k symbols 0..v-1. The t-sets of columns are taken in lexicographic order; for each,
   every row's tuple of symbols in those columns is numbered (the first t-1 columns' part is shared by all the sets
   that begin with them) and marked in a bit array of v^t bits, which must end up full. Prints "covered S t-sets" when
   every t-set shows every tuple, or "gap c_1 ... c_t : s_1 ... s_t" (0-based columns and a missing tuple) for the
   first t-set that does not, and "work W" (rows visited at the last column). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static void die(const char *m) { fprintf(stderr, "ca_scan: %s\n", m); exit(1); }

static int t, k, v;
static long n;
static uint16_t *col;          /* col[c * n + r] */
static uint32_t *part;         /* part[d * n + r]: the number of row r's tuple in the first d chosen columns */
static uint64_t *seen, nbits, nwords, sets = 0, work = 0;
static int cols[32];

static int scan(int d, int start) {
    for (int c = start; c <= k - (t - d); c++) {
        cols[d] = c;
        const uint16_t *cc = col + (size_t)c * n;
        const uint32_t *p = part + (size_t)d * n;
        if (d + 1 < t) {
            uint32_t *q = part + (size_t)(d + 1) * n;
            for (long r = 0; r < n; r++) q[r] = p[r] * (uint32_t)v + cc[r];
            if (scan(d + 1, c + 1)) return 1;
        } else {
            memset(seen, 0, nwords * sizeof(uint64_t));
            for (long r = 0; r < n; r++) {
                uint32_t x = p[r] * (uint32_t)v + cc[r];
                seen[x >> 6] |= 1ULL << (x & 63);
            }
            work += (uint64_t)n;
            sets++;
            uint64_t cnt = 0;
            for (uint64_t w = 0; w < nwords; w++) cnt += __builtin_popcountll(seen[w]);
            if (cnt != nbits) {
                uint64_t miss = 0;
                while (seen[miss >> 6] >> (miss & 63) & 1) miss++;
                int tup[32];
                for (int i = t - 1; i >= 0; i--) { tup[i] = (int)(miss % v); miss /= v; }
                printf("gap");
                for (int i = 0; i < t; i++) printf(" %d", cols[i]);
                printf(" :");
                for (int i = 0; i < t; i++) printf(" %d", tup[i]);
                printf("\n");
                return 1;
            }
        }
    }
    return 0;
}

int main(void) {
    if (scanf("%d %d %d %ld", &t, &k, &v, &n) != 4) die("bad header");
    if (t < 1 || t > 31 || k < t || v < 2 || v > 65535 || n < 1) die("header out of range");
    double vt = 1;
    for (int i = 0; i < t; i++) vt *= v;
    if (vt > 4294967295.0) die("v^t does not fit in 32 bits");
    nbits = (uint64_t)vt;
    nwords = (nbits + 63) / 64;
    col = malloc((size_t)k * n * sizeof(uint16_t));
    part = calloc((size_t)t * n, sizeof(uint32_t));
    seen = malloc(nwords * sizeof(uint64_t));
    if (!col || !part || !seen) die("out of memory");
    for (long r = 0; r < n; r++)
        for (int c = 0; c < k; c++) {
            int x;
            if (scanf("%d", &x) != 1 || x < 0 || x >= v) die("bad symbol");
            col[(size_t)c * n + r] = (uint16_t)x;
        }
    int gap = scan(0, 0);
    if (!gap) printf("covered %llu t-sets\n", (unsigned long long)sets);
    printf("work %llu\n", (unsigned long long)work);
    return 0;
}
