/* cayley_sdp.c: the C helper of cayley_check.py for groups given as semidirect products of cyclic groups.
   G = Z_m x|_a Z_n: the pairs [x, y], 0 <= x < m, 0 <= y < n, with [x, y][u, v] = [x + u mod m, y a^u + v mod n]
   (the convention of the Combinatorics Wiki's and F. Comellas's tables, after M. J. Dinneen and P. Hafner); it is a
   group exactly when a is a unit mod n and a^m = 1 mod n, which this program checks again. [x, y] is the integer
   x n + y. Breadth-first search from the identity [0, 0] of the Cayley graph g ~ g s (s in S), level by level over a
   byte array of distances (no queue), gives the order of <S> and the eccentricity of the identity. Prints "OK order
   diameter", or "FAIL ...".

   Input on stdin: "m n a k limit", then k pairs x y. The caller checks the pairs (range, identity, inverses). */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static uint64_t gcd(uint64_t a, uint64_t b) { while (b) { uint64_t t = a % b; a = b; b = t; } return a; }

int main(void) {
    unsigned long long m, n, a, limit;
    int k;
    if (scanf("%llu %llu %llu %d %llu", &m, &n, &a, &k, &limit) != 5 || m < 1 || n < 1 || k < 1 || k > 1000) {
        puts("FAIL bad header");
        return 1;
    }
    if (m > limit / n) { printf("FAIL the group has more than %llu elements\n", limit); return 1; }
    if (a >= n && !(n == 1 && a <= 1)) { puts("FAIL a must be below n"); return 1; }
    a %= n;
    if (gcd(a, n) != 1 && n > 1) { puts("FAIL a is not a unit mod n"); return 1; }
    uint64_t *pw = malloc(m * sizeof(uint64_t));
    if (!pw) { puts("FAIL out of memory"); return 1; }
    pw[0] = 1 % n;
    for (uint64_t u = 1; u < m; u++) pw[u] = (pw[u - 1] * a) % n;
    if ((pw[m - 1] * a) % n != 1 % n) { puts("FAIL a^m is not 1 mod n: not a group"); return 1; }
    uint64_t *gu = malloc(k * sizeof(uint64_t)), *gv = malloc(k * sizeof(uint64_t));
    for (int s = 0; s < k; s++) {
        unsigned long long x, y;
        if (scanf("%llu %llu", &x, &y) != 2 || x >= m || y >= n) { puts("FAIL bad generator"); return 1; }
        gu[s] = x; gv[s] = y;
    }
    uint64_t N = m * n;
    uint8_t *dist = malloc(N);
    if (!dist) { puts("FAIL out of memory"); return 1; }
    for (uint64_t i = 0; i < N; i++) dist[i] = 255;
    dist[0] = 0;
    uint64_t order = 1;
    int level = 0;
    for (;;) {
        uint64_t added = 0;
        for (uint64_t i = 0; i < N; i++) {
            if (dist[i] != level) continue;
            uint64_t x = i / n, y = i % n;
            for (int s = 0; s < k; s++) {
                uint64_t nx = x + gu[s];
                if (nx >= m) nx -= m;
                uint64_t ny = (y * pw[gu[s]] + gv[s]) % n;
                uint64_t j = nx * n + ny;
                if (dist[j] == 255) { dist[j] = (uint8_t)(level + 1); added++; }
            }
        }
        if (!added) break;
        order += added;
        level++;
        if (level >= 254) { puts("FAIL diameter above 253"); return 1; }
    }
    printf("OK %llu %d\n", (unsigned long long)order, level);
    return 0;
}
