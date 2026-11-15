/* golomb_scan.c: are all differences of a set of marks distinct? (the helper of golomb_check.py for many marks;
   golomb_check.py reads, sorts and shifts the marks first)

     golomb_scan < MARKS

   MARKS: "M", then M distinct non-negative integers in increasing order, the first 0. Every difference is marked in a
   bit array of L + 1 bits (L the largest mark); prints "repeat d i j" (a repeated difference, with the 1-based
   positions of a pair giving it) or "distinct P" with the number of differences. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    long m;
    if (scanf("%ld", &m) != 1 || m < 1) { fprintf(stderr, "golomb_scan: bad count\n"); return 1; }
    int64_t *a = malloc(m * sizeof(int64_t));
    if (!a) { fprintf(stderr, "golomb_scan: out of memory\n"); return 1; }
    for (long i = 0; i < m; i++)
        if (scanf("%lld", (long long *)&a[i]) != 1 || a[i] < 0 || (i && a[i] <= a[i - 1])) {
            fprintf(stderr, "golomb_scan: marks not increasing\n");
            return 1;
        }
    uint64_t L = (uint64_t)a[m - 1];
    uint64_t *bits = calloc(L / 64 + 1, sizeof(uint64_t));
    if (!bits) { fprintf(stderr, "golomb_scan: out of memory for %llu bits\n", (unsigned long long)L + 1); return 1; }
    uint64_t pairs = 0;
    for (long i = 0; i < m; i++)
        for (long j = i + 1; j < m; j++) {
            uint64_t d = (uint64_t)(a[j] - a[i]);
            uint64_t w = d >> 6, b = 1ULL << (d & 63);
            if (bits[w] & b) { printf("repeat %llu %ld %ld\n", (unsigned long long)d, i + 1, j + 1); return 0; }
            bits[w] |= b;
            pairs++;
        }
    printf("distinct %llu\n", (unsigned long long)pairs);
    return 0;
}
