/* qcode_low.c: the low-weight search of qcode_check.py for qubit codes whose stabilizer is too large to list.

   Finds the least weight w of a Pauli operator E on n qubits that commutes with every generator of S (E in S', the
   symplectic complement) and lies outside I (the isotropic part: S for a stabilizer code, S n S' for an
   entanglement-assisted one), or, when ANY is set (codes with K = 0), the least weight of a nonzero E in S'. Weights
   are tried in increasing order; weight w is searched by meeting in the middle: E = E1 E2 where E1 holds the first
   a = ceil(w/2) qubits of the support of E and E2 the other b = w - a, so E1 and E2 have the same syndrome (the
   vector of commutation signs with the generators) and every qubit of E1 comes before every qubit of E2. All E1 of
   weight a are put in a hash table keyed by a linear 64-bit hash of the syndrome (random keys per generator, fixed
   seed), in passes over parts of the hash space so that a pass holds at most MEM entries; every E2 of weight b is
   looked up; every hash match is checked exactly (the two syndromes compared bit by bit, the order of the qubits),
   and E = E1 E2 is tested for membership in I by reduction against an echelon basis of I. A weight is searched only
   if a = ceil(w/2) <= 4 and the number of E1 and E2, C(n,a) 3^a + C(n,b) 3^b, is at most LIMIT; otherwise the
   search stops.

   Input on stdin: "n r s any limit mem", then r generator rows and s rows of a basis of I, each 2n characters 0/1
   (the n X bits, then the n Z bits). Output, last line: "FOUND w" (the least weight; exit 0), or "NONE w" (no such E
   of weight below w; the search stopped at weight w, or w = n + 1 when every weight was searched; exit 0); "FAIL ..."
   (exit 1) for bad input. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t u64;
static int n, r, s, R, NW;          /* R words per syndrome, NW words per 2n-bit operator */
static u64 *colsyn;                 /* syndrome of P_i (P = X, Z, Y): colsyn[((i * 3) + P - 1) * R + word] */
static u64 *colh;                   /* hash of the same: colh[i * 3 + P - 1] */
static u64 *ech; static int *piv; static int ns;   /* echelon basis of I */

static u64 sm(u64 *x) { u64 z = (*x += 0x9E3779B97F4A7C15ull); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull;
                        z = (z ^ (z >> 27)) * 0x94D049BB133111EBull; return z ^ (z >> 31); }
static double pow3(int a) { double x = 1; while (a-- > 0) x *= 3; return x; }
static double comb(int a, int b) { double c = 1; for (int i = 0; i < b; i++) c = c * (a - i) / (i + 1); return c; }

/* an operator of weight <= 4: positions and types packed in 64 bits, 11 bits per qubit (9 position, 2 type) */
typedef struct { u64 h, code; } entry;
static int wt(u64 code) { int w = 0; while (code) { w++; code >>= 11; } return w; }
static int pos_of(u64 code, int j) { return (int)((code >> (11 * j)) & 511); }
static int typ_of(u64 code, int j) { return (int)((code >> (11 * j + 9)) & 3); }

static int in_I(const u64 *v) {      /* reduce v by the echelon basis of I */
    u64 t[64]; memcpy(t, v, NW * sizeof(u64));
    for (int i = 0; i < ns; i++) if (t[piv[i] >> 6] >> (piv[i] & 63) & 1) for (int w = 0; w < NW; w++) t[w] ^= ech[i * NW + w];
    for (int w = 0; w < NW; w++) if (t[w]) return 0;
    return 1;
}
static void op_bits(u64 code, u64 *v) {
    for (int j = 0; j < 4 && (code >> (11 * j)); j++) {
        int p = pos_of(code, j), t = typ_of(code, j);
        if (t & 1) v[p >> 6] ^= 1ull << (p & 63);                     /* X part (X = 1, Y = 3) */
        if (t & 2) v[(n + p) >> 6] ^= 1ull << ((n + p) & 63);         /* Z part (Z = 2, Y = 3) */
    }
}
static void syn(u64 code, u64 *out) {
    memset(out, 0, R * sizeof(u64));
    for (int j = 0; j < 4 && (code >> (11 * j)); j++) {
        const u64 *c = colsyn + ((size_t)pos_of(code, j) * 3 + typ_of(code, j) - 1) * R;
        for (int w = 0; w < R; w++) out[w] ^= c[w];
    }
}

/* enumerate operators of weight exactly k with positions in [lo, n): callback per operator */
typedef void (*cb_t)(u64 h, u64 code);
static void enumerate(int k, int lo, u64 h, u64 code, int depth, cb_t cb) {
    if (depth == k) { cb(h, code); return; }
    for (int p = lo; p <= n - (k - depth); p++)
        for (int t = 1; t <= 3; t++)
            enumerate(k, p + 1, h ^ colh[p * 3 + t - 1], code | ((u64)(p | (t << 9)) << (11 * depth)), depth + 1, cb);
}

static entry *tab; static u64 tmask, part, nparts; static long found_w = 0; static int any_mode, cur_w;
static u64 synA[16], synB[16];
static void ins(u64 h, u64 code) {
    if ((h % nparts) != part) return;
    u64 i = (h * 0x9E3779B97F4A7C15ull) >> 1 & tmask;
    while (tab[i].code) i = (i + 1) & tmask;
    tab[i].h = h; tab[i].code = code;
}
static void probe(u64 h, u64 code) {
    if (found_w || (h % nparts) != part) return;
    int minp = code ? pos_of(code, 0) : n;
    u64 i = (h * 0x9E3779B97F4A7C15ull) >> 1 & tmask;
    for (; tab[i].code; i = (i + 1) & tmask) {
        if (tab[i].h != h) continue;
        u64 c1 = tab[i].code;
        int k1 = wt(c1);
        if (code && pos_of(c1, k1 - 1) >= minp) continue;   /* every qubit of E1 before every qubit of E2 */
        syn(c1, synA); syn(code, synB);
        if (memcmp(synA, synB, R * sizeof(u64))) continue;  /* a hash collision */
        u64 v[64]; memset(v, 0, sizeof v);
        op_bits(c1, v); op_bits(code, v);
        if (any_mode || !in_I(v)) { found_w = cur_w; return; }
    }
}

int main(void) {
    double limit; long mem;
    if (scanf("%d %d %d %d %lf %ld", &n, &r, &s, &any_mode, &limit, &mem) != 6 || n < 1 || n > 511 || r < 0 ||
        r > 2 * n || s < 0 || s > 2 * n) { puts("FAIL bad header"); return 1; }
    R = (r + 63) / 64 ? (r + 63) / 64 : 1; NW = (2 * n + 63) / 64;
    char *buf = malloc(2 * n + 2);
    u64 *rows = calloc((size_t)(r + s) * NW, sizeof(u64));
    for (int i = 0; i < r + s; i++) {
        if (scanf("%s", buf) != 1 || (int)strlen(buf) != 2 * n) { puts("FAIL bad row"); return 1; }
        for (int b = 0; b < 2 * n; b++) {
            if (buf[b] != '0' && buf[b] != '1') { puts("FAIL bad row"); return 1; }
            if (buf[b] == '1') rows[(size_t)i * NW + (b >> 6)] |= 1ull << (b & 63);
        }
    }
    /* syndromes and hashes of the 3n single-qubit operators */
    colsyn = calloc((size_t)3 * n * R, sizeof(u64)); colh = calloc((size_t)3 * n, sizeof(u64));
    u64 seed = 2026, *key = malloc((r + 1) * sizeof(u64));
    for (int j = 0; j < r; j++) key[j] = sm(&seed);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < r; j++) {
            const u64 *row = rows + (size_t)j * NW;
            int x = row[i >> 6] >> (i & 63) & 1, z = row[(n + i) >> 6] >> ((n + i) & 63) & 1;
            /* X_i anticommutes with the row when the row has a Z part at i; Z_i when it has an X part */
            int bits[3] = {z, x, x ^ z};
            for (int t = 0; t < 3; t++) if (bits[t]) {
                colsyn[((size_t)i * 3 + t) * R + (j >> 6)] |= 1ull << (j & 63);
                colh[i * 3 + t] ^= key[j];
            }
        }
    /* echelon basis of I */
    ech = calloc((size_t)(s + 1) * NW, sizeof(u64)); piv = calloc(s + 1, sizeof(int)); ns = 0;
    for (int i = 0; i < s; i++) {
        u64 t[64]; memcpy(t, rows + (size_t)(r + i) * NW, NW * sizeof(u64));
        for (int j = 0; j < ns; j++) if (t[piv[j] >> 6] >> (piv[j] & 63) & 1) for (int w = 0; w < NW; w++) t[w] ^= ech[j * NW + w];
        int p = -1;
        for (int b = 0; b < 2 * n && p < 0; b++) if (t[b >> 6] >> (b & 63) & 1) p = b;
        if (p < 0) continue;
        for (int j = 0; j < ns; j++) if (ech[j * NW + (p >> 6)] >> (p & 63) & 1) for (int w = 0; w < NW; w++) ech[j * NW + w] ^= t[w];
        memcpy(ech + (size_t)ns * NW, t, NW * sizeof(u64)); piv[ns++] = p;
    }
    printf("generators %d, basis of I %d (rank %d)\n", r, s, ns);
    for (int w = 1; w <= n; w++) {
        int a = (w + 1) / 2, b = w - a;
        double na = comb(n, a) * pow3(a), nb = comb(n, b) * pow3(b);
        if (a > 4 || na + nb > limit) { printf("NONE %d\n", w); return 0; }
        cur_w = w;
        nparts = (u64)(na / (double)mem) + 1;
        u64 slots = 1; while (slots < 2 * (na / nparts) + 16) slots <<= 1;
        tab = calloc(slots, sizeof(entry)); tmask = slots - 1;
        for (part = 0; part < nparts && !found_w; part++) {
            memset(tab, 0, slots * sizeof(entry));
            enumerate(a, 0, 0, 0, 0, ins);
            if (b == 0) probe(0, 0); else enumerate(b, 0, 0, 0, 0, probe);
        }
        free(tab);
        printf("weight %d searched (%.3g + %.3g operators, %llu passes)\n", w, na, nb, (unsigned long long)nparts);
        fflush(stdout);
        if (found_w) { printf("FOUND %ld\n", found_w); return 0; }
    }
    printf("NONE %d\n", n + 1);
    return 0;
}
