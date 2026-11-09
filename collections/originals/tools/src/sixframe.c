/* DNA sequences whose six reading frames each encode all 20 amino acids and contain no stop codon (our own code,
   Quantavane Originals, problem six-frame). Standard genetic code; forward frames start at positions 0, 1, 2, the
   reverse frames are the forward frames of the reverse complement; a frame reads every full codon.
   cc -O2 -o sixframe sixframe.c -lm ; ./sixframe LMIN LMAX SECONDS SEED OUT.txt
   For L = LMIN, LMIN+1, ...: simulated annealing on sequences of length L (single-letter changes), cost = number of
   stop codons in all frames + number of (frame, amino acid) pairs missing; stops at the first L reaching cost 0 and
   writes that sequence. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
static const char *AA = "KNKNTTTTRSRSIIMIQHQHPPPPRRRRLLLLEDEDAAAAGGGGVVVV*Y*YSSSS*CWCLFLF";  /* index 16a + 4b + c, order ACGT */
static int L; static char s[512];
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double ur(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static int code(int a, int b, int c) { return 16 * a + 4 * b + c; }
static int cost(void) { int tot = 0; static int rc[512]; for (int i = 0; i < L; i++) rc[i] = 3 - s[L - 1 - i];
  for (int strand = 0; strand < 2; strand++) { const int *q = 0; int seq[512]; for (int i = 0; i < L; i++) seq[i] = strand ? rc[i] : s[i]; (void)q;
    for (int f = 0; f < 3; f++) { int seen[26] = {0}, stops = 0;
      for (int i = f; i + 2 < L; i += 3) { char a = AA[code(seq[i], seq[i + 1], seq[i + 2])]; if (a == '*') stops++; else seen[a - 'A'] = 1; }
      int have = 0; for (int k = 0; k < 26; k++) have += seen[k]; tot += stops + (20 - have); } }
  return tot; }
int main(int argc, char **argv) { int LMIN = atoi(argv[1]), LMAX = atoi(argv[2]); double secs = atof(argv[3]); rs ^= (unsigned long long)atoi(argv[4]) * 2654435761ULL;
  for (L = LMIN; L <= LMAX; L++) { clock_t st = clock(); int best = 1 << 30;
    while ((double)(clock() - st) / CLOCKS_PER_SEC < secs && best > 0) {
      for (int i = 0; i < L; i++) s[i] = rnd() & 3; int c = cost(); double T = 2.0;
      for (long it = 0; it < 2000000 && c > 0; it++) { int p = rnd() % L, old = s[p]; s[p] = (old + 1 + rnd() % 3) & 3; int c2 = cost();
        if (c2 <= c || ur() < exp((c - c2) / T)) c = c2; else s[p] = old; T *= 0.999995; if (T < 0.05) T = 0.05; if (c < best) best = c; }
      if (c == 0) { FILE *o = fopen(argv[5], "w"); for (int i = 0; i < L; i++) fputc("ACGT"[(int)s[i]], o); fputc('\n', o); fclose(o);
        printf("L=%d: found ", L); for (int i = 0; i < L; i++) putchar("ACGT"[(int)s[i]]); printf("\n"); return 0; } }
    printf("L=%d: best cost %d\n", L, best); fflush(stdout); }
  return 0; }
