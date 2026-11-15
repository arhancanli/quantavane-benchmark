/* symmetrization_enum.c (research name sym2.c) - surjectivity of the symmetrization Phi of Delgado, Suer and Yesil (arXiv 2611.14268), program 2 of 2,
   written separately from sym1.py.
   Part A (source side): every almost symmetric (AS) numerical semigroup with Frobenius number F <= FMAX, by a search
     over the pairs {x, F-x} with forced elements propagated; at every leaf the pseudo-Frobenius numbers are recomputed
     from the definition and 2g = F + t is tested; Phi(S) by the formula of the proof of Theorem 4.2,
     s' = s - #{f in PF(S) : f < s, f != F}; the image is filed under ITS OWN Frobenius number G = F - t + 1.
     The image for Frobenius number G is complete when FMAX >= 2G - 3 (a lemma of ours: for G >= 3 every image has a preimage with F <= 2G - 3), which is also tested here
     on every leaf, together with the multiplicity bound m(S) <= 2 mu - 2 (mu = multiplicity of Phi(S)).
   Part B (target side, no AS enumeration): for every symmetric numerical set T with Frobenius G <= GB and every
     F = G .. 2G + 3, every symmetric set of t - 1 = F - G inserted rows (positions P with F - P = P) is tried; the
     resulting set S is kept when it is a numerical semigroup whose pseudo-Frobenius numbers (from the definition) are
     exactly P u {F}.  This decides T in Im(Phi) directly, beyond the lemma's bound, and is compared with Part A.
   Build: cc -O2 -o sym2 symmetrization_enum.c   Run: ./sym2 FMAX GB   Control: ./sym2 control FMAX GB
   (CONTROL: Phi replaced by deleting the rows of all gaps below F/2; Part B then inserts rows only below G/2.) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
#define ONE ((u128)1)
static int CONTROL = 0;

/* ---------- image store: per G, a hash set of 64-bit lower-half patterns (bit j-1 = [j in T], j = 1..k-1) ---------- */
#define MAXG 128
typedef struct { unsigned long long *key; int *minF; int *minT; long cap, n; } hset;
static hset IM[MAXG];
static long hfind(hset *h, unsigned long long k) {
    if (!h->cap) return -1;
    unsigned long long x = (k + 1) * 0x9E3779B97F4A7C15ULL; long i = (long)(x >> 20) & (h->cap - 1);
    while (h->key[i] != ~0ULL) { if (h->key[i] == k) return i; i = (i + 1) & (h->cap - 1); }
    return -1;
}
static void hadd(hset *h, unsigned long long k, int F, int t) {
    if (h->cap == 0 || 2 * (h->n + 1) > h->cap) {
        long nc = h->cap ? 2 * h->cap : 1024; hset nh = { malloc(nc * 8), malloc(nc * 4), malloc(nc * 4), nc, 0 };
        memset(nh.key, 0xff, nc * 8);
        for (long i = 0; i < h->cap; i++) if (h->key[i] != ~0ULL) {
            unsigned long long x = (h->key[i] + 1) * 0x9E3779B97F4A7C15ULL; long j = (long)(x >> 20) & (nc - 1);
            while (nh.key[j] != ~0ULL) j = (j + 1) & (nc - 1);
            nh.key[j] = h->key[i]; nh.minF[j] = h->minF[i]; nh.minT[j] = h->minT[i]; nh.n++; }
        free(h->key); free(h->minF); free(h->minT); *h = nh;
    }
    unsigned long long x = (k + 1) * 0x9E3779B97F4A7C15ULL; long i = (long)(x >> 20) & (h->cap - 1);
    while (h->key[i] != ~0ULL) { if (h->key[i] == k) { if (F < h->minF[i]) { h->minF[i] = F; h->minT[i] = t; } return; } i = (i + 1) & (h->cap - 1); }
    h->key[i] = k; h->minF[i] = F; h->minT[i] = t; h->n++;
}

/* membership of v in S given by mask over 0..F (all v > F are in S) */
static inline int in(u128 S, int F, int v) { return v > F || (v >= 0 && ((S >> v) & 1)); }
/* pseudo-Frobenius numbers from the definition */
static int pfs(u128 S, int F, int *pf) {
    int t = 0;
    for (int g = 1; g <= F; g++) { if (in(S, F, g)) continue; int ok = 1;
        for (int s = 1; s <= F && ok; s++) if (in(S, F, s) && !in(S, F, g + s)) ok = 0;
        if (ok) pf[t++] = g; }
    return t;
}
static int is_semigroup_mask(u128 S, int F) {
    for (int a = 1; a < F; a++) if (in(S, F, a)) for (int b = a; a + b <= F; b++) if (in(S, F, b) && !in(S, F, a + b)) return 0;
    return 1;
}

/* ---------- Part A ---------- */
static int F0; static signed char st[130];      /* 1 element, 0 gap, -1 undecided */
static int pfl[130], npf;                       /* gaps declared pseudo-Frobenius (both members of a pair) */
static long nAS[130], nImgF[130], bad_def[130], bad_lemma, bad_mult, nonsym;
static unsigned long long *seenF; static long seenCap, seenN;    /* per-F image set (to compare with |S_F|) */
static int addel(int s);
static int need(int c) { if (c > F0) return 1; if (c == F0) return 0; if (st[c] == 1) return 1; if (st[c] == 0) return 0; return addel(c); }
static int addel(int s) {
    st[s] = 1;
    for (int a = 1; a < F0; a++) if (st[a] == 1 && !need(a + s)) return 0;
    for (int i = 0; i < npf; i++) if (!need(pfl[i] + s)) return 0;
    return 1;
}
static int addpf(int g) { pfl[npf++] = g; for (int a = 1; a < F0; a++) if (st[a] == 1 && !need(a + g)) return 0; return 1; }
static int seen_insert(unsigned long long k) {
    unsigned long long x = (k + 7) * 0xC2B2AE3D27D4EB4FULL; long i = (long)(x >> 17) & (seenCap - 1);
    while (seenF[i] != ~0ULL) { if (seenF[i] == k) return 0; i = (i + 1) & (seenCap - 1); }
    seenF[i] = k; seenN++; return 1;
}
static void leaf(void) {
    int F = F0; u128 S = 0; for (int v = 0; v <= F; v++) if (st[v] == 1) S |= ONE << v;
    int pf[130], t = pfs(S, F, pf), g = 0; for (int v = 1; v <= F; v++) if (!in(S, F, v)) g++;
    /* the leaf must be AS and its PF must be exactly the declared pairs plus F */
    int ok = (2 * g == F + t) && (t == npf + 1);
    for (int i = 0; i < npf && ok; i++) { int f = 0; for (int j = 0; j < t; j++) if (pf[j] == pfl[i]) f = 1; if (!f) ok = 0; }
    if (!ok) bad_def[F]++;
    nAS[F]++;
    /* Phi: delete the rows of PF \ {F} (CONTROL: rows of all gaps below F/2), by the formula s' = s - #{deleted < s} */
    int del[130], nd = 0;
    if (CONTROL) { for (int v = 1; 2 * v < F; v++) if (!in(S, F, v)) del[nd++] = v; }
    else for (int j = 0; j < t; j++) if (pf[j] != F) del[nd++] = pf[j];
    u128 T = 0;
    for (int s = 0; s <= F + 1; s++) if (in(S, F, s)) { int sh = 0; for (int i = 0; i < nd; i++) if (del[i] < s) sh++; T |= ONE << (s - sh); }
    int G = F - nd;                                  /* the gap F moves to F - nd */
    while (G >= 0 && ((T >> G) & 1)) G--;
    int sym = (T & 1) != 0;
    for (int a = 0; a <= G && sym; a++) if (((T >> a) & 1) == ((T >> (G - a)) & 1)) sym = 0;
    unsigned long long key = 0; int k = (G + 1) / 2;
    for (int j = 1; j < k; j++) if ((T >> j) & 1) key |= 1ULL << (j - 1);
    if (!sym) { nonsym++; key = 0; for (int j = 1; j <= G && j < 50; j++) if ((T >> j) & 1) key |= 1ULL << (j - 1); }
    if (seen_insert(key ^ ((unsigned long long)G << 50) ^ (sym ? 0 : 1ULL << 58))) nImgF[F]++;   /* key < 2^49, G < 128 */
    if (!sym) return;
    hadd(&IM[G], key, F, t);
    /* lemma: F <= 2G - 3 unless the lower half of Phi(S) has no element (then Phi(S) = {0,k,...,2k-2,2k,->}) */
    if (G >= 3 && key != 0 && F > 2 * G - 3) bad_lemma++;
    /* multiplicity bound: m(S) <= 2 mu - 2, mu = multiplicity of Phi(S), when mu < G/2 */
    if (key != 0) { int mu = __builtin_ctzll(key) + 1, m = 1; while (!in(S, F, m)) m++; if (m > 2 * mu - 2) bad_mult++; }
}
static void pairs(int x) {
    int F = F0, y = F - x;
    if (x > y) { leaf(); return; }
    signed char sv[130]; int svn = npf; memcpy(sv, st, sizeof st);
    if (x == y) { if (st[x] != 1) { st[x] = 0; if (addpf(x)) pairs(x + 1); } memcpy(st, sv, sizeof st); npf = svn; return; }
    /* x element, y gap */
    if (st[y] != 1 && st[x] != 0) { st[y] = 0; if (st[x] == 1 || addel(x)) pairs(x + 1); }
    memcpy(st, sv, sizeof st); npf = svn;
    /* y element, x gap */
    if (st[x] != 1 && st[y] != 0) { st[x] = 0; if (st[y] == 1 || addel(y)) pairs(x + 1); }
    memcpy(st, sv, sizeof st); npf = svn;
    /* both gaps, both pseudo-Frobenius */
    if (st[x] != 1 && st[y] != 1) { st[x] = 0; st[y] = 0; if (addpf(x) && addpf(y)) pairs(x + 1); }
    memcpy(st, sv, sizeof st); npf = svn;
}

/* ---------- Part B: target side ---------- */
static int GB;
static int Tsym[MAXG];
/* does the symmetric set with lower-half pattern pat and Frobenius G have a preimage with Frobenius F? */
static int choose_and_test(int G, unsigned long long pat, int F, int need_ins, int lo, int *ins, int nins) {
    /* choose the inserted positions below F/2 (and their mirrors); F/2 itself if F is even */
    int half = (F - 1) / 2;
    if (nins == need_ins) {
        /* build S: walk positions 0..F; inserted positions are gaps, the others read T in order */
        char isP[130] = {0};
        for (int i = 0; i < nins; i++) { isP[ins[i]] = 1; isP[F - ins[i]] = 1; }
        if (F % 2 == 0 && ((F - G) % 2 == 1)) isP[F / 2] = 1;
        int cnt = 0; for (int v = 1; v < F; v++) cnt += isP[v];
        if (cnt != F - G) return 0;
        u128 S = 0; int j = 0;
        for (int v = 0; v <= F; v++) {
            if (isP[v]) continue;
            int inT;
            if (j == 0) inT = 1; else if (j == G) inT = 0;
            else if (2 * j < G) inT = (pat >> (j - 1)) & 1; else inT = !((pat >> (G - j - 1)) & 1);
            if (inT) S |= ONE << v;
            j++;
        }
        if (j != G + 1) return 0;
        if (!is_semigroup_mask(S, F)) return 0;
        int pf[130], t = pfs(S, F, pf);
        if (t != F - G + 1) return 0;
        for (int i = 0; i < t; i++) if (pf[i] != F && !isP[pf[i]]) return 0;
        return 1;
    }
    for (int p = lo; p <= half; p++) {
        if (CONTROL && 2 * p >= G) break;
        ins[nins] = p;
        if (choose_and_test(G, pat, F, need_ins, p + 1, ins, nins + 1)) return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    int ai = 1, FMAX = 60; GB = 15;
    if (argc > 1 && !strcmp(argv[1], "control")) { CONTROL = 1; ai = 2; }
    if (argc > ai) FMAX = atoi(argv[ai]); if (argc > ai + 1) GB = atoi(argv[ai + 1]);
    if (FMAX > 124) FMAX = 124;
    printf("sym2.c%s, FMAX = %d, GB = %d\n", CONTROL ? " [CONTROL: rows of all gaps below F/2 deleted]" : "", FMAX, GB);
    seenCap = 1L << 22; seenF = malloc(seenCap * 8);
    printf("Part A per F: F | |AS_F| |S_F| | leaves failing the PF/AS re-derivation\n");
    for (int F = 1; F <= FMAX; F++) {
        memset(seenF, 0xff, seenCap * 8); seenN = 0;
        F0 = F; memset(st, -1, sizeof st); st[0] = 1; st[F] = 0; npf = 0;
        pairs(1);
        printf("%d | %ld %ld | %ld\n", F, nAS[F], nImgF[F], bad_def[F]); fflush(stdout);
    }
    printf("non-symmetric images: %ld | lemma failures (F > 2G-3): %ld | multiplicity-bound failures (m > 2mu-2): %ld\n", nonsym, bad_lemma, bad_mult);
    printf("\nPart A per G (complete when 2G - 3 <= FMAX): G | symmetric sets 2^((G-1)/2) | symmetric semigroups | in image | image non-semigroups | missing | missing with 1 | missing with 2 (not <2,G+2>) | other missing | max over image of the least F of a preimage | max least t | image by multiplicity mu = 1,2,3,4,5\n");
    for (int G = 1; G < MAXG; G += 2) {
        if (G >= 3 && 2 * G - 3 > FMAX) break;
        int k = (G + 1) / 2; long tot = 1L << (k - 1), sg = 0, img = 0, nsimg = 0, m1 = 0, m2 = 0, oth = 0, bymu[6] = {0}; int worstF = 0, worstT = 0;
        for (long p = 0; p < tot; p++) {
            u128 T = 1; for (int j = 1; j < k; j++) if ((p >> (j - 1)) & 1) T |= ONE << j; else T |= ONE << (G - j);
            int s = is_semigroup_mask(T, G); sg += s;
            long h = hfind(&IM[G], (unsigned long long)p);
            if (h >= 0) { img++; if (!s) nsimg++; { int mu = p ? __builtin_ctzll((unsigned long long)p) + 1 : (k >= 2 ? k : 2); if (mu <= 5) bymu[mu]++; } if (IM[G].minF[h] > worstF) worstF = IM[G].minF[h]; if (IM[G].minT[h] > worstT) worstT = IM[G].minT[h]; }
            else { if (p & 1) m1++; else if (p & 2) m2++; else oth++; }
        }
        printf("%d | %ld | %ld | %ld | %ld | %ld | %ld | %ld | %ld | %d | %d | %ld %ld %ld %ld %ld\n", G, tot, sg, img, nsimg, tot - img, m1, m2, oth, worstF, worstT, bymu[1], bymu[2], bymu[3], bymu[4], bymu[5]);
        Tsym[G] = 1;
        fflush(stdout);
    }
    /* first missing sets (no 1, no 2) for G <= 25 */
    printf("\nfirst missing sets with multiplicity >= 3 (up to 4 per G, lexicographic by small elements):\n");
    for (int G = 7; G <= 25 && Tsym[G]; G += 2) {
        int k = (G + 1) / 2; long tot = 1L << (k - 1); int shown = 0;
        /* lexicographic order of small elements = order of the pattern read from j = 1 upwards with 1 first */
        for (long r = 0; r < tot && shown < 4; r++) {
            long p = 0; for (int j = 1; j < k; j++) if (!((r >> (k - 1 - j)) & 1)) p |= 1L << (j - 1);   /* r = 0 -> all elements */
            if ((p & 1) || (p & 2)) continue;
            if (hfind(&IM[G], (unsigned long long)p) >= 0) continue;
            printf("  G = %d: {0", G); for (int v = 1; v <= G + 1; v++) { int e = v > G ? 1 : (v == G ? 0 : (2 * v < G ? (int)((p >> (v - 1)) & 1) : !((p >> (G - v - 1)) & 1))); if (e) printf(",%d", v); } printf(",->}\n");
            shown++;
        }
    }
    /* Part B */
    printf("\nPart B (target side, F = G .. 2G+3): G | symmetric sets | with a preimage | agrees with Part A\n");
    for (int G = 1; G <= GB; G += 2) {
        int k = (G + 1) / 2; long tot = 1L << (k - 1), have = 0, agree = 1, beyond = 0;
        for (long p = 0; p < tot; p++) {
            int found = 0, ins[130], foundF = 0;
            for (int F = G; F <= 2 * G + 3 && F <= 124 && !found; F++) {
                int r = F - G;                 /* rows to insert */
                int need_ins = r / 2;          /* pairs below F/2 (+ the middle when r is odd, F even) */
                if (r % 2 == 1 && F % 2 == 1) continue;
                if (choose_and_test(G, (unsigned long long)p, F, need_ins, 1, ins, 0)) { found = 1; foundF = F; }
            }
            have += found;
            if (found && G >= 3 && p != 0 && foundF > 2 * G - 3) beyond++;
            if (Tsym[G]) { int inA = hfind(&IM[G], (unsigned long long)p) >= 0; if (inA != found) agree = 0; }
        }
        printf("%d | %ld | %ld | %s%s\n", G, tot, have, Tsym[G] ? (agree ? "yes" : "NO") : "(Part A incomplete)", beyond ? " LEMMA VIOLATED" : "");
        fflush(stdout);
    }
    return 0;
}
