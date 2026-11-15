/* lexiarc.c: the complete lexiarc of PG(2,q), q prime, built by the algorithm FOP with the lexicographical order of
   points of D. Bartoli, A. A. Davydov, G. Faina, A. A. Kreshchuk, S. Marcugini and F. Pambianco (arXiv:1404.0469,
   Section 2): the points (x0, x1, x2), first nonzero coordinate 1, are ordered by x0 q^2 + x1 q + x2; starting from
   the empty set, the first point in this order that lies on no line through two points already chosen is added,
   until every point is covered. For prime q the arc depends on q only, and its size is the paper's t^L_2(2,q).
   Used by the tests and fetch-free controls of the family complete-arc.

     cc -O3 -o lexiarc tools/lexiarc.c && ./lexiarc Q > arc.txt      (one point "x y z" per line) */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint64_t u64;
static u64 Q;

static u64 inv(u64 a) { u64 r = 1, e = Q - 2; while (e) { if (e & 1) r = r * a % Q; a = a * a % Q; e >>= 1; } return r; }
/* compact index in the lexicographical order: (0,0,1) -> 0, (0,1,z) -> 1 + z, (1,y,z) -> q + 1 + y q + z */
static u64 idx(u64 x, u64 y, u64 z) { return x ? Q + 1 + y * Q + z : y ? 1 + z : 0; }

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: lexiarc Q (Q prime)\n"); return 2; }
    Q = strtoull(argv[1], 0, 10);
    for (u64 d = 2; d * d <= Q; d++) if (Q % d == 0) { fprintf(stderr, "Q must be prime\n"); return 2; }
    u64 N = Q * Q + Q + 1;
    unsigned char *sat = calloc(N / 8 + 1, 1);
    u64 cap = 4 * 1024, n = 0;
    u64 (*K)[3] = malloc(cap * sizeof *K);
#define MARK(i) (sat[(i) >> 3] |= (unsigned char)(1u << ((i) & 7)))
    for (u64 pos = 0; pos < N; pos++) {
        if (sat[pos >> 3] >> (pos & 7) & 1) continue;
        u64 a[3];
        if (pos == 0) { a[0] = 0; a[1] = 0; a[2] = 1; }
        else if (pos <= Q) { a[0] = 0; a[1] = 1; a[2] = pos - 1; }
        else { a[0] = 1; a[1] = (pos - Q - 1) / Q; a[2] = (pos - Q - 1) % Q; }
        MARK(pos);
        for (u64 j = 0; j < n; j++) {          /* mark the line through a and K[j] */
            const u64 *b = K[j];
            u64 l0 = (a[1] * b[2] % Q + Q - a[2] * b[1] % Q) % Q, l1 = (a[2] * b[0] % Q + Q - a[0] * b[2] % Q) % Q,
                l2 = (a[0] * b[1] % Q + Q - a[1] * b[0] % Q) % Q;
            if (l2) {
                u64 i2 = inv(l2), c = (Q - l0) * i2 % Q, d = (Q - l1) * i2 % Q, z = c;   /* z = c + d y */
                for (u64 y = 0; y < Q; y++) { MARK(idx(1, y, z)); z += d; if (z >= Q) z -= Q; }
                MARK(idx(0, 1, (Q - l1) * i2 % Q));
            } else if (l1) {
                u64 y = (Q - l0) * inv(l1) % Q;
                for (u64 z = 0; z < Q; z++) MARK(idx(1, y, z));
                MARK(0);
            } else {
                for (u64 z = 0; z < Q; z++) MARK(idx(0, 1, z));
                MARK(0);
            }
        }
        if (n == cap) { cap *= 2; K = realloc(K, cap * sizeof *K); }
        K[n][0] = a[0]; K[n][1] = a[1]; K[n][2] = a[2]; n++;
    }
    for (u64 j = 0; j < n; j++) printf("%llu %llu %llu\n", (unsigned long long)K[j][0], (unsigned long long)K[j][1],
                                       (unsigned long long)K[j][2]);
    fprintf(stderr, "lexiarc of PG(2,%llu): %llu points\n", (unsigned long long)Q, (unsigned long long)n);
    return 0;
}
