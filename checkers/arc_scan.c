/* arc_scan.c: the C helper of arc_check.py. Decides exactly whether a set of points of PG(2,q) is a complete arc (no
   three points on a line, and every other point of the plane on a line through two of them) or, in saturating mode,
   a 1-saturating set (every point of the plane on the set or on a line through two of its points).

   Input on stdin (written by arc_check.py, which has already checked the field and the coordinates):
     q p h mode n          mode 0 = complete arc, 1 = saturating set
     [h > 1: q-1 integers, g^0 .. g^(q-2) for a primitive element g, elements written as integers whose base-p digits
      are the coefficients of a polynomial modulo the irreducible polynomial chosen in the submission]
     n lines "x y z"       homogeneous coordinates, 0 <= x, y, z < q, not all 0
   Output: a few lines, the last "OK n" (exit 0) or "FAIL reason" (exit 1).

   Method. Every point is scaled so that its first nonzero coordinate is 1, and the points must be distinct. The line
   through every pair is computed (cross product, scaled the same way) and kept in a hash table: in an arc no line can
   come from two pairs. Completeness: fix the first point x0. A point P off the set that lies on no secant (a line
   through two points of the set) lies on a line through x0 that holds no other point of the set, a tangent at x0.
   So only the points of the tangents at x0 need checking: with a basis x0, e1, e2 the points other than x0 on the
   line through x0 in direction (1 : b) are e1 + b e2 + t x0 (t in GF(q)), and in direction (0 : 1) e2 + t x0. A
   secant l not through x0 meets that line where t = c + d b (c = -l.e1 / l.x0, d = -l.e2 / l.x0), or t = d on the
   direction (0 : 1). For each tangent the q values of t are marked in a bit array, which must fill. This takes
   (number of tangents) x (number of secants not through x0) steps, about q n^2 / 2 for n points. For prime q the
   value t of every secant is advanced by d from one direction b to the next (one addition and one comparison), eight
   directions per pass over the secants, each marked in its own byte array; for
   q = p^h, h > 1, products come from the tables of powers and logarithms and sums from Zech's logarithms. With the
   environment variable ARC_SCAN_ALL set, the scan goes on after an uncovered point and counts them all (for timing
   and diagnosis; the verdict is the same). */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint32_t u32;
typedef uint64_t u64;
#ifndef DIRS
#define DIRS 8u
#endif

static u32 Q, P, H, QM1, NEG1;      /* NEG1: log of -1 */
static u32 *EXP, *LOG;               /* EXP has 4(q-1) + 1 entries: g^k for k < 2(q-1), then zeros */
static int32_t *ZECH;                /* ZECH[k] = log(1 + g^k), or -1 when 1 + g^k = 0 */
static u32 ZLOG;                     /* stands for the logarithm of 0: EXP[ZLOG + anything < 2(q-1)] = 0 */

static inline u32 fadd(u32 a, u32 b) {
    if (H == 1) { u32 s = a + b; return s >= Q ? s - Q : s; }
    if (P == 2) return a ^ b;
    if (!a) return b;
    if (!b) return a;
    u32 la = LOG[a], lb = LOG[b], k = lb >= la ? lb - la : lb + QM1 - la;
    int32_t z = ZECH[k];
    return z < 0 ? 0 : EXP[la + (u32)z];
}
static inline u32 fneg(u32 a) {
    if (!a) return 0;
    if (H == 1) return Q - a;
    if (P == 2) return a;
    return EXP[LOG[a] + NEG1];
}
static inline u32 fsub(u32 a, u32 b) { return fadd(a, fneg(b)); }
static inline u32 fmul(u32 a, u32 b) {
    if (H == 1) return (u32)((u64)a * b % Q);
    if (!a || !b) return 0;
    return EXP[LOG[a] + LOG[b]];
}
static u32 finv(u32 a) {
    if (H == 1) {
        int64_t r0 = Q, r1 = a, s0 = 0, s1 = 1;
        while (r1) { int64_t qq = r0 / r1, t = r0 - qq * r1; r0 = r1; r1 = t; t = s0 - qq * s1; s0 = s1; s1 = t; }
        return (u32)((s0 % (int64_t)Q + Q) % Q);
    }
    return EXP[(QM1 - LOG[a]) % QM1];
}
static void normalize(u32 *v) {
    int k = v[0] ? 0 : v[1] ? 1 : 2;
    u32 inv = finv(v[k]);
    for (int j = 0; j < 3; j++) v[j] = fmul(v[j], inv);
}
static u64 key(const u32 *v) { return ((u64)v[0] * Q + v[1]) * Q + v[2]; }
static int cmp64(const void *a, const void *b) {
    u64 x = *(const u64 *)a, y = *(const u64 *)b;
    return x < y ? -1 : x > y;
}

int main(void) {
    int mode;
    long n;
    if (scanf("%u %u %u %d %ld", &Q, &P, &H, &mode, &n) != 5 || Q < 2 || n < 1) { puts("FAIL bad header"); return 1; }
    QM1 = Q - 1;
    if (H > 1) {
        EXP = calloc((size_t)4 * QM1 + 1, sizeof(u32));
        LOG = calloc(Q, sizeof(u32));
        ZECH = malloc((size_t)QM1 * sizeof(int32_t));
        for (u32 k = 0; k < QM1; k++) {
            if (scanf("%u", &EXP[k]) != 1 || EXP[k] == 0 || EXP[k] >= Q) { puts("FAIL bad table"); return 1; }
            EXP[k + QM1] = EXP[k];
            LOG[EXP[k]] = k;
        }
        for (u32 k = 1; k < QM1; k++) if (LOG[EXP[k]] != k || EXP[k] == EXP[0]) { puts("FAIL not a primitive element"); return 1; }
        ZLOG = 2 * QM1;
        for (u32 k = 0; k < QM1; k++) {             /* 1 + g^k: add 1 to the constant digit */
            u32 e = EXP[k], d0 = e % P, f = e - d0 + (d0 + 1) % P;
            ZECH[k] = f ? (int32_t)LOG[f] : -1;
        }
        NEG1 = P == 2 ? 0 : QM1 / 2;
    }
    u32 *pt = malloc((size_t)n * 3 * sizeof(u32));
    u64 *keys = malloc((size_t)n * sizeof(u64));
    for (long i = 0; i < n; i++) {
        u32 *v = pt + 3 * i;
        if (scanf("%u %u %u", &v[0], &v[1], &v[2]) != 3 || v[0] >= Q || v[1] >= Q || v[2] >= Q || !(v[0] | v[1] | v[2])) {
            printf("FAIL bad point %ld\n", i + 1);
            return 1;
        }
        normalize(v);
        keys[i] = key(v);
    }
    qsort(keys, n, sizeof(u64), cmp64);
    for (long i = 1; i < n; i++)
        if (keys[i] == keys[i - 1]) { puts("FAIL two points are the same point of PG(2,q)"); return 1; }
    free(keys);

    /* lines through pairs, in a hash table of keys (line) and the pair that gave it */
    u64 npairs = (u64)n * (n - 1) / 2, cap = 1;
    while (cap < 2 * npairs + 2) cap <<= 1;
    u64 *hk = malloc(cap * sizeof(u64));
    u32 *hi = malloc(cap * sizeof(u32)), *hj = malloc(cap * sizeof(u32));
    memset(hk, 0xff, cap * sizeof(u64));
    u64 nlines = 0;
    for (long i = 0; i < n; i++) {
        const u32 *a = pt + 3 * i;
        for (long j = i + 1; j < n; j++) {
            const u32 *b = pt + 3 * j;
            u32 l[3] = {fsub(fmul(a[1], b[2]), fmul(a[2], b[1])), fsub(fmul(a[2], b[0]), fmul(a[0], b[2])),
                        fsub(fmul(a[0], b[1]), fmul(a[1], b[0]))};
            normalize(l);
            u64 k = key(l), h = (k * 0x9E3779B97F4A7C15ull) & (cap - 1);
            while (hk[h] != ~0ull && hk[h] != k) h = (h + 1) & (cap - 1);
            if (hk[h] == k) {
                if (mode == 0) {
                    long c = hi[h] == (u32)i || hi[h] == (u32)j ? hj[h] : hi[h];
                    printf("FAIL points %ld, %ld and %ld (in the order given) are on one line\n", i + 1, j + 1, c + 1);
                    return 1;
                }
                continue;
            }
            hk[h] = k; hi[h] = (u32)i; hj[h] = (u32)j;
            nlines++;
        }
    }
    printf("points %ld, lines through two of them %llu\n", n, (unsigned long long)nlines);

    /* basis x0, e1 = unit vector A, e2 = unit vector B, where position K holds the first 1 of x0 */
    const u32 *x0 = pt;
    int K = x0[0] ? 0 : x0[1] ? 1 : 2, A = K == 0 ? 1 : 0, B = K == 2 ? 1 : 2;
    /* directions of the other points seen from x0: (1 : b) as b, (0 : 1) as q */
    unsigned char *secdir = calloc((size_t)Q + 1, 1);
    for (long i = 1; i < n; i++) {
        const u32 *y = pt + 3 * i;
        u32 g = y[K], al = fsub(y[A], fmul(g, x0[A])), be = fsub(y[B], fmul(g, x0[B]));
        secdir[al ? fmul(be, finv(al)) : Q] = 1;
    }
    u32 ntan = 0;
    for (u32 b = 0; b <= Q; b++) ntan += !secdir[b];
    /* the secants not through x0, as t = c + d b */
    u32 *C = malloc(nlines * sizeof(u32)), *D = malloc(nlines * sizeof(u32));
    u64 m = 0;
    for (u64 h = 0; h < cap; h++) {
        if (hk[h] == ~0ull) continue;
        u64 k = hk[h];
        u32 l[3] = {(u32)(k / ((u64)Q * Q)), (u32)(k / Q % Q), (u32)(k % Q)};
        u32 w = fadd(fadd(fmul(l[0], x0[0]), fmul(l[1], x0[1])), fmul(l[2], x0[2]));
        if (!w) continue;
        u32 iw = fneg(finv(w));
        C[m] = fmul(l[A], iw);
        D[m] = fmul(l[B], iw);
        m++;
    }
    free(hk); free(hi); free(hj);
    printf("tangents at the first point %u, secants not through it %llu, steps %llu\n", ntan, (unsigned long long)m,
           (unsigned long long)((u64)ntan * m));
    fflush(stdout);
    u64 words = (Q + 63) / 64, full_last = (Q % 64) ? ((1ull << (Q % 64)) - 1) : ~0ull;
    u64 *bm = malloc(words * sizeof(u64)), uncovered = 0;
    int all = getenv("ARC_SCAN_ALL") != NULL;     /* timing and diagnosis: count every uncovered point */
    u32 *T = NULL, *LD = NULL;
    if (H == 1) { T = malloc(m * sizeof(u32)); memcpy(T, C, m * sizeof(u32)); }
    else { LD = malloc(m * sizeof(u32)); for (u64 i = 0; i < m; i++) LD[i] = D[i] ? LOG[D[i]] : ZLOG; }
    u32 *LC = NULL, *E = NULL, *Z2 = NULL;
    if (H > 1 && P != 2) {                         /* odd q = p^h: Zech's logarithms, doubled; 0 as 3(q - 1) */
        LC = malloc(m * sizeof(u32)); E = malloc(m * sizeof(u32)); Z2 = malloc((size_t)2 * QM1 * sizeof(u32));
        for (u32 k = 0; k < 2 * QM1; k++) Z2[k] = ZECH[k % QM1] < 0 ? 3 * QM1 : (u32)ZECH[k % QM1];
        for (u64 i = 0; i < m; i++) {
            LC[i] = C[i] ? LOG[C[i]] : ZLOG;
            E[i] = (LC[i] == ZLOG || LD[i] == ZLOG) ? 0 : (LD[i] + QM1 - LC[i]) % QM1;
        }
    }
    if (H == 1) {
        /* prime q: DIRS directions b0, b0 + 1, ... per pass over the secants, marks as bytes (stores only) */
        unsigned char *by = malloc((size_t)DIRS * Q);
        for (u32 b0 = 0; b0 < Q; b0 += DIRS) {
            u32 kk = Q - b0 < DIRS ? Q - b0 : DIRS;
            int any = 0;
            for (u32 k = 0; k < kk; k++) any |= !secdir[b0 + k];
            if (!any) {                            /* no tangent among them: only advance t = c + d b */
                for (u64 i = 0; i < m; i++) {
                    u32 t = T[i], d = D[i];
                    for (u32 k = 0; k < kk; k++) { t += d; t = t >= Q ? t - Q : t; }
                    T[i] = t;
                }
                continue;
            }
            memset(by, 0, (size_t)kk * Q);
            if (kk == DIRS) {
                for (u64 i = 0; i < m; i++) {
                    u32 t = T[i], d = D[i];
                    for (u32 k = 0; k < DIRS; k++) { by[(size_t)k * Q + t] = 1; t += d; t = t >= Q ? t - Q : t; }
                    T[i] = t;
                }
            } else {
                for (u64 i = 0; i < m; i++) {
                    u32 t = T[i], d = D[i];
                    for (u32 k = 0; k < kk; k++) { by[(size_t)k * Q + t] = 1; t += d; t = t >= Q ? t - Q : t; }
                    T[i] = t;
                }
            }
            for (u32 k = 0; k < kk; k++) {
                if (secdir[b0 + k]) continue;
                const unsigned char *y = by + (size_t)k * Q;
                for (u32 t = 0; t < Q; t++) {
                    if (y[t]) continue;
                    if (all) { uncovered++; continue; }
                    u32 v[3], b = b0 + k;                 /* the point e1 + b e2 + t x0 */
                    for (int j = 0; j < 3; j++) v[j] = fmul(t, x0[j]);
                    v[A] = fadd(v[A], 1); v[B] = fadd(v[B], b);
                    normalize(v);
                    printf("FAIL the point (%u, %u, %u) is %s\n", v[0], v[1], v[2],
                           mode == 0 ? "on no line through two points of the arc: the arc is not complete"
                                     : "neither in the set nor on a line through two of its points");
                    return 1;
                }
            }
        }
        free(by);
    }
    for (u32 b = H == 1 ? Q : 0; b <= Q; b++) {
        int tangent = !secdir[b];
        if (H == 1 && b < Q && !tangent) {        /* not a tangent: only advance t = c + d b to b + 1 */
            for (u64 i = 0; i < m; i++) { u32 t = T[i] + D[i]; T[i] = t >= Q ? t - Q : t; }
            continue;
        }
        if (!tangent) continue;
        memset(bm, 0, words * sizeof(u64));
        if (b == Q) {                              /* direction (0 : 1): t = d */
            for (u64 i = 0; i < m; i++) bm[D[i] >> 6] |= 1ull << (D[i] & 63);
        } else if (H == 1) {
            for (u64 i = 0; i < m; i++) {
                u32 t = T[i];
                bm[t >> 6] |= 1ull << (t & 63);
                t += D[i];
                T[i] = t >= Q ? t - Q : t;
            }
        } else {
            u32 lb = b ? LOG[b] : ZLOG;
            if (P == 2) {
                for (u64 i = 0; i < m; i++) { u32 t = C[i] ^ EXP[LD[i] + lb]; bm[t >> 6] |= 1ull << (t & 63); }
            } else if (!b) {
                for (u64 i = 0; i < m; i++) { u32 t = C[i]; bm[t >> 6] |= 1ull << (t & 63); }
            } else {
                /* marks by logarithm (code q - 1 for 0): log(c + d b) = log c + Z(log d + log b - log c); secants
                   with c = 0 or d = 0 (rare) go through fadd */
                for (u64 i = 0; i < m; i++) {
                    u32 code;
                    if (LC[i] == ZLOG || LD[i] == ZLOG) {
                        u32 t = fadd(C[i], EXP[LD[i] + lb]);
                        code = t ? LOG[t] : QM1;
                    } else {
                        u32 z = Z2[E[i] + lb], r = LC[i] + z;
                        code = r >= 2 * QM1 ? QM1 : r >= QM1 ? r - QM1 : r;
                    }
                    bm[code >> 6] |= 1ull << (code & 63);
                }
            }
        }
        for (u64 w = 0; w < words; w++) {
            u64 want = w == words - 1 ? full_last : ~0ull;
            if ((bm[w] & want) != want && all) { uncovered += (u64)__builtin_popcountll(~bm[w] & want); continue; }
            if ((bm[w] & want) != want) {
                u32 t = (u32)(w * 64 + __builtin_ctzll(~bm[w] & want));
                if (H > 1 && P != 2 && b && b < Q) t = t == QM1 ? 0 : EXP[t];   /* a logarithm: back to the element */
                u32 v[3];                           /* the point e1 + b e2 + t x0, or e2 + t x0 */
                for (int j = 0; j < 3; j++) v[j] = fmul(t, x0[j]);
                if (b < Q) { v[A] = fadd(v[A], 1); v[B] = fadd(v[B], b); }
                else v[B] = fadd(v[B], 1);
                normalize(v);
                printf("FAIL the point (%u, %u, %u) is %s\n", v[0], v[1], v[2],
                       mode == 0 ? "on no line through two points of the arc: the arc is not complete"
                                 : "neither in the set nor on a line through two of its points");
                return 1;
            }
        }
    }
    if (uncovered) {
        printf("FAIL %llu points are %s\n", (unsigned long long)uncovered,
               mode == 0 ? "on no line through two points of the arc" : "not covered");
        return 1;
    }
    printf("OK %ld\n", n);
    return 0;
}
