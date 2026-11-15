/* circulant_bfs.c: the eccentricity of vertex 0 in the Cayley graph of Z_n with the given steps (the helper of
   circulant_check.py for large n; circulant_check.py reads and checks the jumps first).

     circulant_bfs N LIMIT < STEPS

   STEPS: the distinct nonzero steps (each jump and its negative) modulo N. Breadth-first search from 0 one layer at
   a time on bit sets of N bits: the next layer is the union over the steps s of the frontier rotated by s, minus the
   vertices already reached. Prints "ecc E", or "ecc -1" when some vertex is farther than LIMIT or unreachable. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static inline uint64_t get64(const uint64_t *a, uint64_t p) {     /* 64 bits starting at bit p (a padded by 1 word) */
    uint64_t w = p >> 6, o = p & 63;
    return o ? (a[w] >> o) | (a[w + 1] << (64 - o)) : a[w];
}

static inline void or64(uint64_t *a, uint64_t q, uint64_t x) {    /* a[q .. q+63] |= x */
    uint64_t w = q >> 6, o = q & 63;
    a[w] |= x << o;
    if (o) a[w + 1] |= x >> (64 - o);
}

/* dst[q + i] |= src[p + i] for 0 <= i < len */
static void copy_or(uint64_t *dst, const uint64_t *src, uint64_t p, uint64_t q, uint64_t len) {
    uint64_t i = 0;
    for (; i + 64 <= len; i += 64) or64(dst, q + i, get64(src, p + i));
    if (i < len) or64(dst, q + i, get64(src, p + i) & ((1ULL << (len - i)) - 1));
}

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: circulant_bfs N LIMIT < STEPS\n"); return 2; }
    uint64_t n = strtoull(argv[1], NULL, 10);
    int limit = atoi(argv[2]);
    if (n < 2 || n > (1ULL << 36)) { fprintf(stderr, "circulant_bfs: bad n\n"); return 2; }
    uint64_t st[4096];
    int ns = 0;
    long long x;
    while (ns < 4096 && scanf("%lld", &x) == 1) {
        if (x <= 0 || (uint64_t)x >= n) { fprintf(stderr, "circulant_bfs: bad step\n"); return 2; }
        st[ns++] = (uint64_t)x;
    }
    uint64_t words = n / 64 + 2;
    uint64_t *seen = calloc(words, 8), *fr = calloc(words, 8), *nx = calloc(words, 8);
    if (!seen || !fr || !nx) { fprintf(stderr, "circulant_bfs: out of memory\n"); return 2; }
    seen[0] = fr[0] = 1;
    uint64_t reached = 1;
    int r = 0;
    while (reached < n) {
        if (r == limit) { printf("ecc -1\n"); return 0; }
        memset(nx, 0, words * 8);
        for (int j = 0; j < ns; j++) {             /* vertex i of the frontier reaches i + s modulo n */
            uint64_t s = st[j];
            copy_or(nx, fr, 0, s, n - s);
            copy_or(nx, fr, n - s, 0, s);
        }
        uint64_t got = 0;
        for (uint64_t w = 0; w < words; w++) {
            nx[w] &= ~seen[w];
            seen[w] |= nx[w];
            got += __builtin_popcountll(nx[w]);
        }
        if (!got) { printf("ecc -1\n"); return 0; }
        reached += got;
        uint64_t *t = fr; fr = nx; nx = t;
        r++;
    }
    printf("ecc %d\n", r);
    return 0;
}
