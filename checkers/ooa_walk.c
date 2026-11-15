/* ooa_walk.c: method D of ooa_check.py in C, for GF(2^e), e = 1..8 (the helper of ooa_check.py, which reads and
   checks the matrix and the field first).

     ooa_walk < INPUT

   INPUT: "e m s t k", then the field: for each c = 0..2^e - 1 its inverse (0 for c = 0) and the e columns of the
   matrix of multiplication by c (column i = c x^i, an integer below 2^e); then the columns: for factor i = 0..s-1 and
   depth d = 0..t-1, the m entries of column d of factor i (integers below 2^e).

   A vector of m <= 64 field elements is kept as e bit planes (bit j of plane i = bit i of entry j). The walk is the
   one of ooa_check.py: factors in order, for each a depth d up to min(t, room) whose first d columns join a running
   echelon basis (each basis vector scaled so that its pivot, its first nonzero entry, is 1); a column that reduces to
   zero is dependent. Prints "independent L" (L depth vectors of weight k, all independent) or "dependent (i,d) ..."
   (1-based factor and depth of the chosen columns, the last one dependent), and "nodes N".

   15 Nov 2026: for e = 1 a vector is one word and the reduction is branch-free (v ^= b & -(bit of v at the pivot)),
   about 3.5 times faster; the same walk, the same nodes, the same answers
   (the environment variable OOA_WALK_PLAIN=1 forces the plain walk, for tests). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef struct { uint64_t p[8]; } vec;

static int e, m, s, t, k;
static int inv_[256];
static uint8_t mulm[256][8];         /* mulm[c][i] = c * x^i: the image of basis element i under multiplication by c */
static vec *cols;                    /* cols[i * t + d] */
static uint64_t leaves = 0, nodes = 0;
static int chosen_f[64], chosen_d[64];
static vec basis[64];
static int piv[64];

static void die(const char *msg) { fprintf(stderr, "ooa_walk: %s\n", msg); exit(1); }

static inline int entry(const vec *v, int j) {
    int c = 0;
    for (int i = 0; i < e; i++) c |= (int)((v->p[i] >> j) & 1) << i;
    return c;
}

/* w = c * v (c a field element), plane by plane: plane r of the product is the XOR of plane i of v over the i with
   bit r of c x^i set */
static inline void scale(vec *w, const vec *v, int c) {
    for (int r = 0; r < e; r++) w->p[r] = 0;
    for (int i = 0; i < e; i++) {
        int img = mulm[c][i];
        for (int r = 0; r < e; r++)
            if (img >> r & 1) w->p[r] ^= v->p[i];
    }
}

static inline uint64_t support(const vec *v) {
    uint64_t o = 0;
    for (int i = 0; i < e; i++) o |= v->p[i];
    return o;
}

static int rec(int start, int r, int depth) {
    for (int i = start; i < s; i++) {
        if ((s - i) * t < r) return 0;
        int added = 0;
        int lim = t < r ? t : r;
        for (int d = 1; d <= lim; d++) {
            vec v = cols[i * t + d - 1];
            nodes++;
            for (int b = 0; b < depth + added; b++) {           /* reduce against the basis, in order */
                int c = entry(&v, piv[b]);
                if (c) {
                    vec w;
                    if (e == 1) { for (int x = 0; x < e; x++) v.p[x] ^= basis[b].p[x]; continue; }
                    scale(&w, &basis[b], c);
                    for (int x = 0; x < e; x++) v.p[x] ^= w.p[x];
                }
            }
            uint64_t sup = support(&v);
            chosen_f[depth + added] = i + 1;
            chosen_d[depth + added] = d;
            if (!sup) {
                printf("dependent");
                for (int x = 0; x <= depth + added; x++) printf(" (%d,%d)", chosen_f[x], chosen_d[x]);
                printf("\n");
                return 1;
            }
            int p = __builtin_ctzll(sup);
            int c = entry(&v, p);
            if (c != 1) { vec w; scale(&w, &v, inv_[c]); v = w; }
            basis[depth + added] = v;
            piv[depth + added] = p;
            added++;
            if (r - d == 0) leaves++;
            else if (rec(i + 1, r - d, depth + added)) return 1;
        }
    }
    return 0;
}

/* e = 1: one word per vector */
static uint64_t *c1, b1[64];
static int p1[64];

static void print_dep(int nb) {
    printf("dependent");
    for (int x = 0; x <= nb; x++) printf(" (%d,%d)", chosen_f[x], chosen_d[x]);
    printf("\n");
}

static int rec1(int start, int r, int depth) {
    for (int i = start; i < s; i++) {
        if ((s - i) * t < r) return 0;
        int added = 0;
        int lim = t < r ? t : r;
        for (int d = 1; d <= lim; d++) {
            uint64_t v = c1[i * t + d - 1];
            nodes++;
            int nb = depth + added;
            for (int b = 0; b < nb; b++) v ^= b1[b] & (0 - ((v >> p1[b]) & 1));
            chosen_f[nb] = i + 1;
            chosen_d[nb] = d;
            if (!v) { print_dep(nb); return 1; }
            b1[nb] = v;
            p1[nb] = __builtin_ctzll(v);
            added++;
            if (r - d == 0) leaves++;
            else if (rec1(i + 1, r - d, depth + added)) return 1;
        }
    }
    return 0;
}

int main(void) {
    if (scanf("%d %d %d %d %d", &e, &m, &s, &t, &k) != 5) die("bad header");
    if (e < 1 || e > 8 || m < 1 || m > 64 || s < 1 || t < 1 || k < 1 || k > 64 || s * t > 100000000) die("header out of range");
    int q = 1 << e;
    for (int c = 0; c < q; c++) {
        if (scanf("%d", &inv_[c]) != 1) die("bad field");
        for (int i = 0; i < e; i++) {
            int x;
            if (scanf("%d", &x) != 1 || x < 0 || x >= q) die("bad field");
            mulm[c][i] = (uint8_t)x;
        }
    }
    cols = calloc((size_t)s * t, sizeof(vec));
    if (!cols) die("out of memory");
    for (int i = 0; i < s; i++)
        for (int d = 0; d < t; d++)
            for (int j = 0; j < m; j++) {
                int x;
                if (scanf("%d", &x) != 1 || x < 0 || x >= q) die("bad entry");
                for (int b = 0; b < e; b++)
                    if (x >> b & 1) cols[i * t + d].p[b] |= 1ULL << j;
            }
    int bad;
    if (e == 1 && !getenv("OOA_WALK_PLAIN")) {
        c1 = malloc((size_t)s * t * sizeof(uint64_t));
        if (!c1) die("out of memory");
        for (int x = 0; x < s * t; x++) c1[x] = cols[x].p[0];
        bad = rec1(0, k, 0);
    } else bad = rec(0, k, 0);
    if (!bad) printf("independent %llu\n", (unsigned long long)leaves);
    printf("nodes %llu\n", (unsigned long long)nodes);
    return 0;
}
