/* covering_mark.c: count the t-subsets of {0..v-1} that lie in at least one block (the helper of covering_check.py
   for large (v,k,t) coverings; covering_check.py reads and checks the blocks first).

     covering_mark V K T < BLOCKS

   BLOCKS: B, then B lines of K distinct points 0..V-1 in increasing order. Every t-subset of every block is marked,
   one largest point x at a time, in a bit array indexed by the colex rank of the other t-1 points (the sum of
   C(x_i, i)), and the program prints "covered C of N", where N = C(V,T), and "marks M" (the number of t-subsets of
   blocks visited, B x C(K,T)). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static void die(const char *m) { fprintf(stderr, "covering_mark: %s\n", m); exit(1); }

int main(int argc, char **argv) {
    if (argc != 4) die("usage: covering_mark V K T < BLOCKS");
    int v = atoi(argv[1]), k = atoi(argv[2]), t = atoi(argv[3]);
    if (v < 1 || v > 200 || k < 1 || k > v || t < 1 || t > k || t > 32) die("parameters out of range");
    static uint64_t C[201][33];                       /* C[x][i] = binomial(x, i), checked against overflow */
    for (int x = 0; x <= 200; x++)
        for (int i = 0; i <= 32; i++) {
            if (i == 0) C[x][i] = 1;
            else if (x == 0) C[x][i] = 0;
            else {
                uint64_t a = C[x - 1][i - 1], b = C[x - 1][i];
                C[x][i] = (a > UINT64_MAX - b) ? UINT64_MAX : a + b;
            }
        }
    uint64_t total = C[v][t];
    if (total == UINT64_MAX) die("C(V,T) too large");
    long nb;
    if (scanf("%ld", &nb) != 1 || nb < 0) die("bad block count");
    int *blk = malloc((size_t)(nb ? nb : 1) * k * sizeof(int));
    if (!blk) die("out of memory");
    for (long j = 0; j < nb; j++)
        for (int i = 0; i < k; i++) {
            int x;
            if (scanf("%d", &x) != 1 || x < 0 || x >= v) die("bad point");
            if (i && x <= blk[j * k + i - 1]) die("points not increasing");
            blk[j * k + i] = x;
        }
    /* The t-subsets whose largest point is x are {x} plus a (t-1)-subset of {0..x-1}: C(x, t-1) of them, ranked in
       colex order. They are marked one x at a time in a bit array of that size (it stays in the cache), from the
       blocks that hold x, and must all be marked. */
    uint64_t slice_max = C[v - 1][t - 1];
    if (slice_max == UINT64_MAX || slice_max > (1ULL << 40)) die("C(V-1,T-1) too large for the bit array");
    uint64_t *bits = malloc(((slice_max + 63) / 64) * sizeof(uint64_t) + 8);
    if (!bits) die("out of memory");
    uint64_t marks = 0, covered = 0;
    int below[200], idx[33];
    for (int x = t - 1; x < v; x++) {
        uint64_t size = C[x][t - 1], words = (size + 63) / 64;
        memset(bits, 0, words * sizeof(uint64_t));
        for (long j = 0; j < nb; j++) {
            const int *b = blk + j * k;
            int nbelow = 0, has = 0;
            for (int i = 0; i < k; i++) {
                if (b[i] < x) below[nbelow++] = b[i];
                else if (b[i] == x) has = 1;
            }
            if (!has || nbelow < t - 1) continue;
            if (t == 1) { bits[0] |= 1; marks++; continue; }
            int s = t - 1;
            for (int i = 0; i < s; i++) idx[i] = i;
            for (;;) {
                uint64_t r = 0;
                for (int i = 0; i < s; i++) r += C[below[idx[i]]][i + 1];
                bits[r >> 6] |= 1ULL << (r & 63);
                marks++;
                int i = s - 1;
                while (i >= 0 && idx[i] == nbelow - s + i) i--;
                if (i < 0) break;
                idx[i]++;
                for (int l = i + 1; l < s; l++) idx[l] = idx[l - 1] + 1;
            }
        }
        for (uint64_t w = 0; w < words; w++) covered += __builtin_popcountll(bits[w]);
    }
    printf("covered %llu of %llu\n", (unsigned long long)covered, (unsigned long long)total);
    printf("marks %llu\n", (unsigned long long)marks);
    return 0;
}
