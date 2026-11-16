/* cayley_bfs.c: the C helper of cayley_check.py. Breadth-first search of a permutation group from the identity:
   every element found is multiplied by every generator (h = g then s, h(x) = s(g(x))), and kept in a hash table
   (open addressing on a 64-bit hash of the permutation, the permutation itself compared on a hash match). Prints
   "OK order diameter" (the group's order and the eccentricity of the identity in its Cayley graph), or "FAIL ..."
   when the order would pass the limit.

   Input on stdin: "m k limit", then k permutations of 0..m-1 (images, m <= 65535). */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint16_t pt;
static int m;
static pt *elems;            /* element i at elems[i * m] */
static uint32_t *table;      /* hash table of element indices + 1 (0 = empty) */
static uint64_t tmask;

static uint64_t hashp(const pt *p) {
    uint64_t h = 1469598103934665603ull;
    for (int i = 0; i < m; i++) { h ^= p[i]; h *= 1099511628211ull; }
    return h ^ (h >> 29);
}

int main(void) {
    int k;
    double limit;
    if (scanf("%d %d %lf", &m, &k, &limit) != 3 || m < 1 || m > 65535 || k < 1) { puts("FAIL bad header"); return 1; }
    pt *gens = malloc((size_t)k * m * sizeof(pt));
    for (int j = 0; j < k * m; j++) {
        int x;
        if (scanf("%d", &x) != 1 || x < 0 || x >= m) { puts("FAIL bad generator"); return 1; }
        gens[j] = (pt)x;
    }
    uint64_t cap = 1 << 16, n = 0, slots = 1 << 17;
    elems = malloc(cap * m * sizeof(pt));
    table = calloc(slots, sizeof(uint32_t)); tmask = slots - 1;
    for (int i = 0; i < m; i++) elems[i] = (pt)i;
    table[hashp(elems) & tmask] = 1; n = 1;
    uint64_t level_start = 0, level_end = 1;
    int diam = 0;
    pt *h = malloc(m * sizeof(pt));
    while (level_start < level_end) {
        for (uint64_t g = level_start; g < level_end; g++) {
            for (int s = 0; s < k; s++) {
                const pt *gp = elems + g * m, *sp = gens + (size_t)s * m;
                for (int x = 0; x < m; x++) h[x] = sp[gp[x]];
                uint64_t i = hashp(h) & tmask;
                int found = 0;
                while (table[i]) {
                    if (!memcmp(elems + (uint64_t)(table[i] - 1) * m, h, m * sizeof(pt))) { found = 1; break; }
                    i = (i + 1) & tmask;
                }
                if (found) continue;
                if (n + 1 > (uint64_t)limit) { printf("FAIL the group has more than %.0f elements\n", limit); return 1; }
                if (n == cap) {
                    cap *= 2;
                    elems = realloc(elems, cap * m * sizeof(pt));
                    if (!elems) { puts("FAIL out of memory"); return 1; }
                }
                memcpy(elems + n * m, h, m * sizeof(pt));
                table[i] = (uint32_t)(n + 1);
                n++;
                if (2 * n > slots) {                   /* grow and rehash */
                    slots *= 2; tmask = slots - 1;
                    free(table); table = calloc(slots, sizeof(uint32_t));
                    for (uint64_t e = 0; e < n; e++) {
                        uint64_t j = hashp(elems + e * m) & tmask;
                        while (table[j]) j = (j + 1) & tmask;
                        table[j] = (uint32_t)(e + 1);
                    }
                }
            }
        }
        if (n > level_end) diam++;
        level_start = level_end;
        level_end = n;
    }
    printf("OK %llu %d\n", (unsigned long long)n, diam);
    return 0;
}
