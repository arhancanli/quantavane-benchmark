/* covering_lotto.c: the exact search of covering_check.py for (v,k,t,m) coverings with m > t, in C (its helper for
   large designs; covering_check.py reads and checks the blocks first).

     covering_lotto V K T M [NODE_LIMIT] < BLOCKS

   BLOCKS: B, then B lines of K distinct points 0..V-1 in increasing order; V <= 128.

   It looks for a bad M-subset: one that meets every block in at most T-1 points. Points are added one at a time; a
   point stays a candidate until some block holding it already has T-1 chosen points (then the whole block is
   forbidden). A branch is cut when even the candidates cannot complete it: split along blocks, the candidates inside a
   block can add at most that block's room T-1-(chosen points in it). The blocks whose candidates exceed their room are
   taken most excess first (ties by block number) and each takes the candidates no earlier part took; the candidates
   left over form one more part with no cap. Points that lie in exactly the same blocks are interchangeable: once no
   bad set holds p, none holds a point of p's kind. This is the search of covering_check.py's find_bad_set, step for
   step, so the two visit the same nodes.

   Prints "bad p_1 ... p_M" (0-based points) or "none", then "nodes N"; with NODE_LIMIT, "limit" when the search
   visits more nodes than that before it ends (then nothing is decided). Exit status 0 in every case. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned __int128 mask_t;

static void die(const char *m) { fprintf(stderr, "covering_lotto: %s\n", m); exit(2); }

static inline int pc(mask_t x) {
    return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64));
}
static inline int low_bit(mask_t x) {
    uint64_t lo = (uint64_t)x;
    return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((uint64_t)(x >> 64));
}

static int v, k, t, m;
static long nb;
static mask_t *bmask;            /* points of block j */
static int *cnt;                 /* chosen points in block j */
static int **of, *ndeg;          /* blocks holding point p, in increasing order */
static int kind[128];
static mask_t same[128];         /* the points of each kind */
static int chosen[128];
static unsigned long long nodes, limit;
static int hit_limit;

/* scratch for the split, used only between the start of a node and its first branch */
static int *ex_of;               /* excess of block j over its room (0 if none) */
static long *order_buf;          /* the over-full blocks sorted by excess, descending */
static long bucket_start[130];

static int rec(mask_t cand, int s) {
    if (s >= m) return 1;
    if (s + pc(cand) < m) return 0;
    if (++nodes > limit) { hit_limit = 1; return 0; }
    /* split the candidates along blocks */
    int kmax = k;
    long counts[130];
    memset(counts, 0, sizeof(long) * (kmax + 2));
    long nover = 0;
    for (long j = 0; j < nb; j++) {
        int ov = pc(bmask[j] & cand);
        int room = t - 1 - cnt[j];
        int e = ov > room ? ov - room : 0;
        ex_of[j] = e;
        if (e) { counts[e]++; nover++; }
    }
    /* bucket order: excess kmax first ... excess 1 last, blocks in increasing order inside a bucket */
    long pos = 0;
    for (int e = kmax; e >= 1; e--) { bucket_start[e] = pos; pos += counts[e]; }
    for (long j = 0; j < nb; j++)
        if (ex_of[j]) order_buf[bucket_start[ex_of[j]]++] = j;
    mask_t pmask[130];
    int pcum[130];
    int np = 1;
    mask_t rem = cand;
    for (long i = 0; i < nover; i++) {
        long j = order_buf[i];
        mask_t part = bmask[j] & rem;
        if (part) {
            int room = t - 1 - cnt[j];
            if (pc(part) > room) {
                pmask[np] = part;
                pcum[np] = room;
                np++;
                rem &= ~part;
            }
        }
    }
    pmask[0] = rem;
    pcum[0] = pc(rem);
    for (int i = 1; i < np; i++) pcum[i] += pcum[i - 1];
    /* branch, last part first: at most pcum[i] points can still come from part i and the parts before it */
    for (int i = np - 1; i >= 0; i--) {
        mask_t c = pmask[i] & cand;
        while (c) {
            if (s + pcum[i] < m) return 0;
            int p = low_bit(c);
            mask_t bit = (mask_t)1 << p;
            c &= ~bit;
            if (!(cand & bit)) continue;
            cand &= ~bit;
            mask_t forbid = 0;
            for (int d = 0; d < ndeg[p]; d++) {
                int j = of[p][d];
                if (++cnt[j] >= t - 1) forbid |= bmask[j];
            }
            chosen[s] = p;
            if (rec(cand & ~forbid, s + 1)) return 1;
            for (int d = 0; d < ndeg[p]; d++) cnt[of[p][d]]--;
            if (hit_limit) return 0;
            /* no bad set holds p, so none holds a point of the same kind in place of p */
            cand &= ~same[kind[p]];
            c &= cand;
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 5 && argc != 6) die("usage: covering_lotto V K T M [NODE_LIMIT] < BLOCKS");
    v = atoi(argv[1]); k = atoi(argv[2]); t = atoi(argv[3]); m = atoi(argv[4]);
    limit = argc == 6 ? strtoull(argv[5], NULL, 10) : ~0ULL;
    if (v < 1 || v > 128 || k < 1 || k > v || t < 1 || t > k || m <= t || m > v) die("parameters out of range");
    if (scanf("%ld", &nb) != 1 || nb < 1) die("bad block count");
    bmask = calloc((size_t)nb, sizeof(mask_t));
    cnt = calloc((size_t)nb, sizeof(int));
    ex_of = calloc((size_t)nb, sizeof(int));
    order_buf = calloc((size_t)nb, sizeof(long));
    ndeg = calloc(128, sizeof(int));
    of = calloc(128, sizeof(int *));
    if (!bmask || !cnt || !ex_of || !order_buf || !ndeg || !of) die("out of memory");
    for (long j = 0; j < nb; j++) {
        int prev = -1;
        for (int i = 0; i < k; i++) {
            int x;
            if (scanf("%d", &x) != 1 || x < 0 || x >= v) die("bad point");
            if (x <= prev) die("points not increasing");
            prev = x;
            bmask[j] |= (mask_t)1 << x;
            ndeg[x]++;
        }
    }
    for (int p = 0; p < v; p++) {
        of[p] = malloc(sizeof(int) * (ndeg[p] ? ndeg[p] : 1));
        if (!of[p]) die("out of memory");
        ndeg[p] = 0;
    }
    for (long j = 0; j < nb; j++)
        for (int p = 0; p < v; p++)
            if (bmask[j] >> p & 1) of[p][ndeg[p]++] = (int)j;
    /* kinds: points with the same list of blocks */
    int nkinds = 0;
    for (int p = 0; p < v; p++) {
        int found = -1;
        for (int q = 0; q < p && found < 0; q++)
            if (ndeg[q] == ndeg[p] && memcmp(of[q], of[p], sizeof(int) * ndeg[p]) == 0) found = kind[q];
        kind[p] = found >= 0 ? found : nkinds++;
        same[kind[p]] |= (mask_t)1 << p;
    }
    mask_t start = v == 128 ? ~(mask_t)0 : (((mask_t)1 << v) - 1);
    if (t == 1)                  /* room 0 from the start: no point of any block can be chosen */
        for (long j = 0; j < nb; j++) start &= ~bmask[j];
    int found = rec(start, 0);
    if (found) {
        printf("bad");
        for (int i = 0; i < m; i++) printf(" %d", chosen[i]);
        printf("\n");
    } else if (hit_limit) printf("limit\n");
    else printf("none\n");
    printf("nodes %llu\n", nodes);
    return 0;
}
