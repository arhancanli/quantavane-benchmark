/* ca_trie.c: is an array a covering array of strength t? (the fast helper of ca_check.py for large arrays;
   ca_check.py reads and checks the rows first).

     ca_trie < ARRAY

   ARRAY: "t k v n" (and an optional fifth word "all", for timing only: go on after a gap), then n rows of k symbols
   0..v-1, v <= 64.

   The rows are split by their symbols in the first t-1 chosen columns c_1 < ... < c_(t-1) (a trie: each level is the
   previous one split by one more column, in a counting sort, so the v^(t-1) groups of the last level hold the rows
   showing each (t-1)-tuple). Every group must be nonempty. Then, for EVERY last column c > c_(t-1) at once, the
   symbols each group shows in column c are collected as a bit mask: each row of the array is stored once as k one-hot
   masks (1 << symbol, in 8, 16, 32 or 64 bits by v), and a group's masks are OR-ed row by row over the columns
   c_(t-1)+1 .. k-1 (a plain loop that the compiler vectorizes). The t-set {c_1, ..., c_(t-1), c} shows every tuple
   exactly when every group's mask for c is full. So each row is visited once per t-set, as in ca_scan.c, but as one
   lane of a vector operation on contiguous memory, and no array of v^t bits is needed.

   Prints "covered S t-sets" when every t-set shows every tuple, or "gap c_1 ... c_j : s_1 ... s_j" (0-based columns
   and a tuple of symbols they never show together; j < t when fewer columns already miss a tuple) for the first gap
   found, then "work W" (rows visited in t-sets, C(k,t) x n for a covering array). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static void die(const char *m) { fprintf(stderr, "ca_trie: %s\n", m); exit(1); }

static int t, k, v, all_mode = 0;
static long n;
static uint8_t *col;                 /* col[c * n + r], the symbol of row r in column c */
static void *H;                      /* H[r * k + c] = 1 << symbol, lanes of LB bytes */
static int LB;
static uint32_t *perm[65];           /* perm[j]: the rows ordered by their symbols in cols[0..j-1] */
static uint32_t *off[65];            /* off[j][g]: start of group g at level j (v^j groups), off[j][v^j] = n */
static uint64_t ngroups[65];
static void *acc;
static int cols[65];
static uint64_t sets = 0, work = 0, gaps = 0;
static uint32_t cnt[64], posn[64];

static void report_gap(int j, uint64_t g, int lastcol, int lastsym) {
    gaps++;
    if (all_mode) return;
    int tup[66], nt = j;
    for (int i = j - 1; i >= 0; i--) { tup[i] = (int)(g % (uint64_t)v); g /= (uint64_t)v; }
    printf("gap");
    for (int i = 0; i < j; i++) printf(" %d", cols[i]);
    if (lastcol >= 0) printf(" %d", lastcol);
    printf(" :");
    for (int i = 0; i < nt; i++) printf(" %d", tup[i]);
    if (lastcol >= 0) printf(" %d", lastsym);
    printf("\n");
}

/* split level j by column c into level j + 1; 1 when a group comes out empty (a j+1-tuple never shown) */
static int refine(int j, int c) {
    const uint32_t *src = perm[j], *o = off[j];
    uint32_t *dst = perm[j + 1], *o2 = off[j + 1];
    const uint8_t *cc = col + (size_t)c * n;
    uint64_t ng = ngroups[j];
    int empty = 0;
    for (uint64_t g = 0; g < ng; g++) {
        uint32_t a = o[g], b = o[g + 1];
        memset(cnt, 0, sizeof(uint32_t) * v);
        for (uint32_t x = a; x < b; x++) cnt[cc[src[x]]]++;
        uint32_t p = a;
        for (int s = 0; s < v; s++) {
            o2[g * v + s] = p; posn[s] = p; p += cnt[s];
            if (!cnt[s] && !empty) {
                cols[j] = c;
                report_gap(j + 1, g * v + s, -1, 0);
                empty = 1;
                if (!all_mode) return 1;
            }
        }
        for (uint32_t x = a; x < b; x++) { uint32_t r = src[x]; dst[posn[cc[r]]++] = r; }
    }
    o2[ng * v] = (uint32_t)n;
    return empty && !all_mode;
}

/* level j = t - 2 (t >= 2): for each group of rows (equal symbols in cols[0..j-1]) and each column c1 >= start, the
   rows are sorted by their symbol s in c1 on the fly: the one-hot masks of each row in the columns after c1 are OR-ed
   into the accumulator of s. A group's rows are first copied into one contiguous block (they are then read once for
   every c1). For t = 1 the single group of all rows is checked column by column. */
#define LEAF2(T)                                                                                                 \
    {                                                                                                            \
        const T full = (T)fullmask;                                                                              \
        T *A = (T *)acc;                                                                                         \
        for (uint64_t g = 0; g < ng; g++) {                                                                      \
            uint32_t a = o[g], b = o[g + 1], gs = b - a;                                                         \
            if (a == b) { report_gap(j, g, -1, 0); if (!all_mode) return 1; continue; }                          \
            const T *Bk; const uint8_t *Sk;                                                                      \
            size_t W;                                     /* row width in the block: columns start .. k-1 */     \
            if (j == 0) { Bk = (const T *)H + start; Sk = S + start; W = (size_t)k; }                            \
            else {                                                                                               \
                T *bb = (T *)blk; uint8_t *ss = blks;                                                            \
                W = (size_t)(k - start);                                                                         \
                for (uint32_t x = 0; x < gs; x++) {                                                              \
                    uint32_t r = P[a + x];                                                                       \
                    memcpy(bb + (size_t)x * W, (const T *)H + (size_t)r * k + start, W * sizeof(T));             \
                    memcpy(ss + (size_t)x * W, S + (size_t)r * k + start, W);                                    \
                }                                                                                                \
                Bk = bb; Sk = ss;                                                                                \
            }                                                                                                    \
            for (int c1 = start; c1 <= (t == 1 ? start : k - 2); c1++) {                                        \
                int L = t == 1 ? k : k - c1 - 1, base = t == 1 ? 0 : c1 + 1;                                     \
                if (L <= 0) continue;                                                                            \
                int nv = t == 1 ? 1 : v;                                                                         \
                for (int s = 0; s < nv; s++) memset(A + (size_t)s * k, 0, (size_t)L * sizeof(T));               \
                memset(cnt, 0, sizeof(cnt));                                                                     \
                for (uint32_t x = 0; x < gs; x++) {                                                              \
                    int s = t == 1 ? 0 : Sk[(size_t)x * W + (c1 - start)];                                       \
                    cnt[s]++;                                                                                    \
                    T *As = A + (size_t)s * k;                                                                   \
                    const T *rw = Bk + (size_t)x * W + (base - start);                                           \
                    for (int i = 0; i < L; i++) As[i] |= rw[i];                                                  \
                }                                                                                                \
                for (int s = 0; s < nv; s++) {                                                                   \
                    if (!cnt[s]) { cols[j] = c1; report_gap(j + 1, g * v + s, -1, 0); if (!all_mode) return 1; continue; } \
                    const T *As = A + (size_t)s * k;                                                             \
                    T m = full;                                                                                  \
                    for (int i = 0; i < L; i++) m &= As[i];                                                      \
                    if (m != full && all_mode) { gaps++; continue; }                                             \
                    if (m != full) {                                                                             \
                        for (int i = 0; i < L; i++)                                                              \
                            if (As[i] != full) {                                                                 \
                                int sy = 0;                                                                      \
                                while ((As[i] >> sy) & 1) sy++;                                                  \
                                if (t == 1) report_gap(0, 0, base + i, sy);                                      \
                                else { cols[j] = c1; report_gap(j + 1, g * v + s, base + i, sy); }              \
                                if (!all_mode) return 1;                                                         \
                                break;                                                                           \
                            }                                                                                    \
                    }                                                                                            \
                }                                                                                                \
                if (g == 0) { sets += (uint64_t)L; work += (uint64_t)L * (uint64_t)n; }                          \
            }                                                                                                    \
        }                                                                                                        \
    }

static void *blk;
static uint8_t *S, *blks;
static uint64_t blkcap = 0;

static int leaf(int j, int start) {
    const uint32_t *P = perm[j], *o = off[j];
    uint64_t ng = ngroups[j];
    uint64_t fullmask = v == 64 ? ~0ULL : ((1ULL << v) - 1);
    if (t == 1) start = 0;
    if (j > 0) {                                     /* room for the largest group's rows */
        uint64_t mx = 0;
        for (uint64_t g = 0; g < ng; g++) if (o[g + 1] - o[g] > mx) mx = o[g + 1] - o[g];
        if (mx > blkcap) {
            free(blk); free(blks);
            blk = malloc((size_t)mx * k * LB); blks = malloc((size_t)mx * k);
            if (!blk || !blks) die("out of memory");
            blkcap = mx;
        }
    }
    if (LB == 1) LEAF2(uint8_t)
    else if (LB == 2) LEAF2(uint16_t)
    else if (LB == 4) LEAF2(uint32_t)
    else LEAF2(uint64_t)
    return 0;
}

static int rec(int j, int start) {
    if (j == (t >= 2 ? t - 2 : 0)) return leaf(j, start);
    for (int c = start; c <= k - (t - j); c++) {
        cols[j] = c;
        if (refine(j, c)) return 1;
        if (rec(j + 1, c + 1)) return 1;
    }
    return 0;
}

static unsigned char *buf;
static size_t blen, bpos;

static int next_int(long *out) {
    while (bpos < blen && (buf[bpos] == ' ' || buf[bpos] == '\n' || buf[bpos] == '\r' || buf[bpos] == '\t')) bpos++;
    if (bpos >= blen || buf[bpos] < '0' || buf[bpos] > '9') return 0;
    long x = 0;
    while (bpos < blen && buf[bpos] >= '0' && buf[bpos] <= '9') { x = x * 10 + (buf[bpos] - '0'); if (x > 1L << 40) return 0; bpos++; }
    *out = x;
    return 1;
}

int main(void) {
    size_t cap = 1 << 20;
    buf = malloc(cap);
    if (!buf) die("out of memory");
    size_t got;
    while ((got = fread(buf + blen, 1, cap - blen, stdin)) > 0) {
        blen += got;
        if (blen == cap) { cap *= 2; buf = realloc(buf, cap); if (!buf) die("out of memory"); }
    }
    long a[4];
    for (int i = 0; i < 4; i++) if (!next_int(&a[i])) die("bad header");
    t = (int)a[0]; k = (int)a[1]; v = (int)a[2]; n = a[3];
    while (bpos < blen && buf[bpos] == ' ') bpos++;
    if (bpos + 3 <= blen && memcmp(buf + bpos, "all", 3) == 0) { all_mode = 1; bpos += 3; }
    if (t < 1 || t > 64 || k < t || v < 2 || v > 64 || n < 1 || n >= 4294967295L) die("header out of range");
    LB = v <= 8 ? 1 : v <= 16 ? 2 : v <= 32 ? 4 : 8;
    uint64_t ng = 1;
    for (int j = 0; j < t; j++) {
        ngroups[j] = ng;
        if (j < t - 1 && ng > (uint64_t)n) die("more groups than rows");   /* then v^t > n: not a covering array */
        ng *= (uint64_t)v;
    }
    col = malloc((size_t)k * n);
    H = malloc((size_t)k * n * LB);
    acc = malloc((size_t)v * k * LB);
    S = malloc((size_t)k * n);
    if (!col || !H || !acc || !S) die("out of memory");
    for (long r = 0; r < n; r++)
        for (int c = 0; c < k; c++) {
            long x;
            if (!next_int(&x) || x >= v) die("bad symbol");
            col[(size_t)c * n + r] = (uint8_t)x;
            S[(size_t)r * k + c] = (uint8_t)x;
            uint64_t bit = 1ULL << x;
            size_t at = (size_t)r * k + c;
            if (LB == 1) ((uint8_t *)H)[at] = (uint8_t)bit;
            else if (LB == 2) ((uint16_t *)H)[at] = (uint16_t)bit;
            else if (LB == 4) ((uint32_t *)H)[at] = (uint32_t)bit;
            else ((uint64_t *)H)[at] = bit;
        }
    long extra;
    if (next_int(&extra)) die("more symbols than n rows of k");
    free(buf);
    for (int j = 0; j < t; j++) {
        perm[j] = malloc((size_t)n * sizeof(uint32_t));
        off[j] = malloc((size_t)(ngroups[j] + 1) * sizeof(uint32_t));
        if (!perm[j] || !off[j]) die("out of memory");
    }
    for (long r = 0; r < n; r++) perm[0][r] = (uint32_t)r;
    off[0][0] = 0; off[0][1] = (uint32_t)n;
    int gap = rec(0, 0);
    if (!gap && !gaps) printf("covered %llu t-sets\n", (unsigned long long)sets);
    else if (all_mode) printf("gaps %llu\n", (unsigned long long)gaps);
    printf("work %llu\n", (unsigned long long)work);
    return 0;
}
