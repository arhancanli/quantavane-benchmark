/* ooa_walk_p.c: method D of ooa_check.py in C for GF(p^e) with p = 3, 5 or 7 and e = 1..4 (GF(3), GF(5), GF(7),
   GF(9), GF(25), GF(27), GF(49), GF(81)); the helper of ooa_check.py, which reads and checks the matrix and the
   field first. ooa_walk.c does the same for p = 2.

     ooa_walk_p < INPUT

   INPUT: "p e m s t k", then the field: for each c = 0..p^e - 1 its inverse (0 for c = 0) and the e columns of the
   matrix of multiplication by c (column i = c x^i, an integer below p^e whose base-p digits are its coefficients);
   then the columns: for factor i = 0..s-1 and depth d = 0..t-1, the m entries of column d of factor i.

   A vector of m <= 64 field elements is kept as e digit planes (plane r holds digit r of every entry) and every
   operation is done digit-wise modulo p. The walk is the one of ooa_check.py and ooa_walk.c. Prints "independent L"
   or "dependent (i,d) ...", and "nodes N". */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define W 64
typedef struct { uint8_t d[4][W]; } vec;

static int P, e, m, s, t, k, q;
static int inv_[81];
static uint8_t M[81][4][4];          /* M[c][r][i] = digit r of c x^i: multiplication by c as a matrix over GF(p) */
static vec *cols;
static uint64_t leaves = 0, nodes = 0;
static int chosen_f[64], chosen_d[64];
static vec basis[64];
static int piv[64];

static void die(const char *msg) { fprintf(stderr, "ooa_walk_p: %s\n", msg); exit(1); }

/* v += f * b (mod p), on one plane; written once per p so that the compiler sees a constant modulus */
#define AXPY(PP) static void axpy##PP(uint8_t *restrict v, const uint8_t *restrict b, unsigned f) { \
    for (int j = 0; j < W; j++) v[j] = (uint8_t)((v[j] + f * b[j]) % PP); }
AXPY(3)
AXPY(5)
AXPY(7)

static inline void axpy(uint8_t *v, const uint8_t *b, unsigned f) {
    if (!f) return;
    if (P == 3) axpy3(v, b, f); else if (P == 5) axpy5(v, b, f); else axpy7(v, b, f);
}

static inline int entry(const vec *v, int j) {
    int c = 0, pw = 1;
    for (int r = 0; r < e; r++) { c += v->d[r][j] * pw; pw *= P; }
    return c;
}

/* v += c * b for a field element c: plane r of c b is sum_i M[c][r][i] b_i */
static inline void add_scaled(vec *v, const vec *b, int c) {
    for (int r = 0; r < e; r++)
        for (int i = 0; i < e; i++) axpy(v->d[r], b->d[i], M[c][r][i]);
}

static inline int first_nonzero(const vec *v) {
    for (int j = 0; j < m; j++)
        for (int r = 0; r < e; r++)
            if (v->d[r][j]) return j;
    return -1;
}

static int neg(int c) {                       /* -c, digit by digit */
    int out = 0, pw = 1;
    for (int r = 0; r < e; r++) { int dgt = (c / pw) % P; out += ((P - dgt) % P) * pw; pw *= P; }
    return out;
}

static int rec(int start, int r, int depth) {
    for (int i = start; i < s; i++) {
        if ((s - i) * t < r) return 0;
        int added = 0;
        int lim = t < r ? t : r;
        for (int d = 1; d <= lim; d++) {
            vec v = cols[i * t + d - 1];
            nodes++;
            for (int b = 0; b < depth + added; b++) {
                int c = entry(&v, piv[b]);
                if (c) add_scaled(&v, &basis[b], neg(c));        /* basis[b] has 1 at its pivot */
            }
            chosen_f[depth + added] = i + 1;
            chosen_d[depth + added] = d;
            int p = first_nonzero(&v);
            if (p < 0) {
                printf("dependent");
                for (int x = 0; x <= depth + added; x++) printf(" (%d,%d)", chosen_f[x], chosen_d[x]);
                printf("\n");
                return 1;
            }
            int c = entry(&v, p);
            if (c != 1) {
                vec w;
                memset(&w, 0, sizeof w);
                add_scaled(&w, &v, inv_[c]);
                v = w;
            }
            basis[depth + added] = v;
            piv[depth + added] = p;
            added++;
            if (r - d == 0) leaves++;
            else if (rec(i + 1, r - d, depth + added)) return 1;
        }
    }
    return 0;
}

int main(void) {
    if (scanf("%d %d %d %d %d %d", &P, &e, &m, &s, &t, &k) != 6) die("bad header");
    if ((P != 3 && P != 5 && P != 7) || e < 1 || e > 4 || m < 1 || m > W || s < 1 || t < 1 || k < 1 || k > 64 ||
        (long)s * t > 10000000L) die("header out of range");
    q = 1;
    for (int r = 0; r < e; r++) q *= P;
    if (q > 81) die("field too large");
    for (int c = 0; c < q; c++) {
        if (scanf("%d", &inv_[c]) != 1) die("bad field");
        for (int i = 0; i < e; i++) {
            int x;
            if (scanf("%d", &x) != 1 || x < 0 || x >= q) die("bad field");
            for (int r = 0; r < e; r++) { M[c][r][i] = (uint8_t)(x % P); x /= P; }
        }
    }
    cols = calloc((size_t)s * t, sizeof(vec));
    if (!cols) die("out of memory");
    for (int i = 0; i < s; i++)
        for (int d = 0; d < t; d++)
            for (int j = 0; j < m; j++) {
                int x;
                if (scanf("%d", &x) != 1 || x < 0 || x >= q) die("bad entry");
                for (int r = 0; r < e; r++) { cols[i * t + d].d[r][j] = (uint8_t)(x % P); x /= P; }
            }
    int bad = rec(0, k, 0);
    if (!bad) printf("independent %llu\n", (unsigned long long)leaves);
    printf("nodes %llu\n", (unsigned long long)nodes);
    return 0;
}
