/* ucode_scan.c: the least Hamming distance between two words of a code (the helper of ucode_check.py, which reads
   and checks the words first).

     ucode_scan D < WORDS

   WORDS: "M L", then M lines of L symbols 0..7. Each word is kept as three bit planes (bit j of plane b = bit b of
   symbol j), so two words differ in coordinate j exactly when some plane differs there. Every pair is compared;
   the program stops at the first pair closer than D and prints "close i j dist" (1-based), otherwise "ok P" with the
   number of pairs compared. L <= 64. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: ucode_scan D < WORDS\n"); return 1; }
    int D = atoi(argv[1]);
    long M; int L;
    if (scanf("%ld %d", &M, &L) != 2 || M < 1 || L < 1 || L > 64) { fprintf(stderr, "ucode_scan: bad header\n"); return 1; }
    uint64_t *w = calloc((size_t)M * 3, sizeof(uint64_t));
    if (!w) { fprintf(stderr, "ucode_scan: out of memory\n"); return 1; }
    for (long i = 0; i < M; i++)
        for (int j = 0; j < L; j++) {
            int x;
            if (scanf("%d", &x) != 1 || x < 0 || x > 7) { fprintf(stderr, "ucode_scan: bad symbol\n"); return 1; }
            for (int b = 0; b < 3; b++)
                if (x >> b & 1) w[i * 3 + b] |= 1ULL << j;
        }
    uint64_t pairs = 0;
    for (long i = 0; i < M; i++) {
        uint64_t a0 = w[i * 3], a1 = w[i * 3 + 1], a2 = w[i * 3 + 2];
        for (long j = i + 1; j < M; j++) {
            int d = __builtin_popcountll((a0 ^ w[j * 3]) | (a1 ^ w[j * 3 + 1]) | (a2 ^ w[j * 3 + 2]));
            pairs++;
            if (d < D) { printf("close %ld %ld %d\n", i + 1, j + 1, d); return 0; }
        }
    }
    printf("ok %llu\n", (unsigned long long)pairs);
    return 0;
}
