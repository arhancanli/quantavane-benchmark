/* mols_scan.c: the C helper of mols_check.py for large files. Reads K Latin squares of order N from a text file (rows
   of N integers 0..N-1, or 1..N for every square of the file; '#' starts a comment; blank lines ignored; an optional
   first line "N K" as in the files of github.com/Constructive-Codes/MOLS), checks that every square is Latin and that
   every two squares are orthogonal (each ordered pair of symbols exactly once, marked in an array of N^2 stamps),
   and prints "OK K" (exit 0) or "FAIL reason" (exit 1).

     cc -O3 -o mols_scan mols_scan.c && ./mols_scan N FILE */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 3) { puts("FAIL usage: mols_scan N FILE"); return 2; }
    long n = atol(argv[1]);
    if (n < 2 || n > 65535) { puts("FAIL N must be 2..65535"); return 1; }
    FILE *f = fopen(argv[2], "rb");
    if (!f) { puts("FAIL cannot open the file"); return 1; }
    size_t cap = (size_t)n * n * 4, len = 0;
    uint32_t *v = malloc(cap * sizeof(uint32_t));
    long rows = 0, inrow = 0, line = 1, header = -1, hk = -1, lineitems = 0, first_line_items = 0;
    int c, incomment = 0, any_line = 0;
    uint64_t cur = 0;
    int innum = 0;
    long first_vals[3] = {0, 0, 0};
    /* tokenize: numbers per line; a line of N numbers is a row; the first non-comment line may be "N K" */
    for (;;) {
        c = fgetc(f);
        if (c == '#') incomment = 1;
        if (!incomment && c >= '0' && c <= '9') {
            cur = cur * 10 + (uint64_t)(c - '0');
            if (cur > 1000000000ull) { printf("FAIL a number too large on line %ld\n", line); return 1; }
            innum = 1;
            continue;
        }
        if (!incomment && !(c == ' ' || c == '\t' || c == ',' || c == '\r' || c == '\n' || c == EOF)) {
            printf("FAIL not a row of integers on line %ld\n", line);
            return 1;
        }
        if (innum) {
            if (!any_line && lineitems < 3) first_vals[lineitems] = (long)cur;
            if (len == cap) { cap *= 2; v = realloc(v, cap * sizeof(uint32_t)); }
            v[len++] = (uint32_t)cur;
            lineitems++;
            cur = 0;
            innum = 0;
        }
        if (c == '\n' || c == EOF) {
            if (lineitems) {
                if (!any_line && lineitems == 2 && n != 2) {      /* the header "N K" */
                    header = first_vals[0];
                    hk = first_vals[1];
                    len -= 2;
                    first_line_items = 2;
                } else if (lineitems != n) {
                    printf("FAIL line %ld has %ld numbers, expected %ld\n", line, lineitems, n);
                    return 1;
                } else rows++;
                any_line = 1;
            }
            lineitems = 0;
            incomment = 0;
            line++;
            if (c == EOF) break;
        }
    }
    fclose(f);
    (void)first_line_items; (void)inrow;
    if (header >= 0 && header != n) { printf("FAIL the file is for order %ld, not %ld\n", header, n); return 1; }
    if (rows == 0 || rows % n) { printf("FAIL %ld rows, expected a multiple of %ld\n", rows, n); return 1; }
    long k = rows / n;
    if (hk >= 0 && hk != k) { printf("FAIL the header announces %ld squares, the file has %ld\n", hk, k); return 1; }
    size_t nn = (size_t)n * n;
    /* symbols 0..N-1, or 1..N in the whole file */
    uint32_t mn = UINT32_MAX, mx = 0;
    for (size_t i = 0; i < len; i++) { if (v[i] < mn) mn = v[i]; if (v[i] > mx) mx = v[i]; }
    uint32_t base = (mn == 1 && mx == (uint32_t)n) ? 1 : 0;
    if (mx - base >= (uint32_t)n || mn < base) { puts("FAIL symbols must be 0..N-1 (or 1..N)"); return 1; }
    uint16_t *s = malloc(len * sizeof(uint16_t));
    for (size_t i = 0; i < len; i++) s[i] = (uint16_t)(v[i] - base);
    free(v);
    /* Latin: every symbol once in every row and every column */
    uint32_t *seen = calloc((size_t)n, sizeof(uint32_t)), stamp = 0;
    for (long a = 0; a < k; a++) {
        const uint16_t *L = s + (size_t)a * nn;
        for (long i = 0; i < n; i++) {
            stamp++;
            for (long j = 0; j < n; j++) {
                uint16_t x = L[(size_t)i * n + j];
                if (seen[x] == stamp) { printf("FAIL square %ld: symbol %u twice in row %ld\n", a + 1, x + base, i + 1); return 1; }
                seen[x] = stamp;
            }
            stamp++;
            for (long j = 0; j < n; j++) {
                uint16_t x = L[(size_t)j * n + i];
                if (seen[x] == stamp) { printf("FAIL square %ld: symbol %u twice in column %ld\n", a + 1, x + base, i + 1); return 1; }
                seen[x] = stamp;
            }
        }
    }
    /* orthogonal: every ordered pair of symbols once; stamps avoid clearing N^2 entries per pair */
    uint32_t *pairs = calloc(nn, sizeof(uint32_t));
    uint32_t pid = 0;
    for (long a = 0; a < k; a++)
        for (long b = a + 1; b < k; b++) {
            pid++;
            const uint16_t *A = s + (size_t)a * nn, *B = s + (size_t)b * nn;
            for (size_t i = 0; i < nn; i++) {
                size_t key = (size_t)A[i] * n + B[i];
                if (pairs[key] == pid) {
                    printf("FAIL squares %ld and %ld are not orthogonal (pair %u,%u repeated at cell %zu,%zu)\n", a + 1,
                           b + 1, A[i] + base, B[i] + base, i / n + 1, i % n + 1);
                    return 1;
                }
                pairs[key] = pid;
            }
        }
    printf("OK %ld\n", k);
    return 0;
}
