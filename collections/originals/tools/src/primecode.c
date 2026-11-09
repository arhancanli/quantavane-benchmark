/* Codes made of primes: iterated local search with (1,2)-swaps (in the spirit of Andrade, Resende and Werneck's ILS
   for maximum independent set) on the conflict graph of the n-digit primes (an edge when two primes differ in fewer
   than D digits). Our own code, Quantavane Originals, problem prime-code.
     cc -O2 -o primecode primecode.c; ./primecode N D SECONDS SEED OUT */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define MAXP 70000
static int np, pr[MAXP], *adj[MAXP], deg[MAXP], ndig, D;
static unsigned char dg[MAXP][7];
static unsigned char *bits; static long long nb8;
static int conf(int a, int b) { long long k = (long long)a * np + b; return bits[k >> 3] >> (k & 7) & 1; }
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int in[MAXP], tight[MAXP], sol[MAXP], spos[MAXP], ns;
static void add(int v) { in[v] = 1; spos[v] = ns; sol[ns++] = v; for (int k = 0; k < deg[v]; k++) tight[adj[v][k]]++; }
static void del(int v) { in[v] = 0; int p = spos[v]; sol[p] = sol[--ns]; spos[sol[p]] = p; for (int k = 0; k < deg[v]; k++) tight[adj[v][k]]--; }
static int improve(void) { /* free vertices first, then (1,2)-swaps; returns 1 if anything changed */
  int changed = 0, again = 1;
  while (again) { again = 0;
    for (int v = 0; v < np; v++) if (!in[v] && tight[v] == 0) { add(v); again = changed = 1; }
    for (int i = 0; i < ns && !again; i++) { int x = sol[i]; static int L[4096]; int m = 0;
      for (int k = 0; k < deg[x]; k++) { int u = adj[x][k]; if (!in[u] && tight[u] == 1) L[m++] = u; }
      for (int a = 0; a < m && !again; a++) for (int b = a + 1; b < m; b++) if (!conf(L[a], L[b])) { del(x); add(L[a]); add(L[b]); again = changed = 1; break; } } }
  return changed;
}
int main(int argc, char **argv) {
  int n = atoi(argv[1]); D = atoi(argv[2]); double secs = atof(argv[3]); rs ^= (unsigned long long)atoll(argv[4]) * 2654435761ULL;
  ndig = n; int lo = 1, hi; for (int i = 1; i < n; i++) lo *= 10; hi = lo * 10;
  char *s = calloc(hi, 1); for (int i = 2; (long)i * i < hi; i++) if (!s[i]) for (int j = i * i; j < hi; j += i) s[j] = 1;
  for (int p = lo; p < hi; p++) if (p > 1 && !s[p]) { pr[np] = p; int x = p; for (int k = n - 1; k >= 0; k--) { dg[np][k] = x % 10; x /= 10; } np++; }
  nb8 = (long long)np * np / 8 + 1; bits = calloc(nb8, 1);
  /* neighbours: change up to D-1 digits; enumerate by index lookup */
  int *idx = malloc(sizeof(int) * hi); for (int i = 0; i < hi; i++) idx[i] = -1; for (int i = 0; i < np; i++) idx[pr[i]] = i;
  static int tmp[200000];
  int pw[8]; pw[n - 1] = 1; for (int k = n - 2; k >= 0; k--) pw[k] = pw[k + 1] * 10;
  for (int i = 0; i < np; i++) { int c = 0;
    for (int a = 0; a < n; a++) for (int da = 0; da < 10; da++) { if (da == dg[i][a] || (a == 0 && da == 0)) continue;
      int y = pr[i] + (da - dg[i][a]) * pw[a]; if (idx[y] >= 0) tmp[c++] = idx[y];
      if (D >= 3) for (int b = a + 1; b < n; b++) for (int db = 0; db < 10; db++) { if (db == dg[i][b]) continue; int z = y + (db - dg[i][b]) * pw[b]; if (idx[z] >= 0) tmp[c++] = idx[z]; } }
    adj[i] = malloc(sizeof(int) * (c + 1)); memcpy(adj[i], tmp, sizeof(int) * c); deg[i] = c;
    for (int k = 0; k < c; k++) { long long q = (long long)i * np + tmp[k]; bits[q >> 3] |= 1 << (q & 7); } }
  for (int v = 0; v < np; v++) if (!in[v] && tight[v] == 0) add(v);
  improve(); int best = ns; static int bestsol[MAXP]; memcpy(bestsol, sol, sizeof(int) * ns);
  clock_t st = clock(); long it = 0;
  while ((double)(clock() - st) / CLOCKS_PER_SEC < secs) { it++;
    /* perturb: force in one random non-solution vertex (two now and then), then improve */
    int k = (rnd() % 8 == 0) ? 2 : 1;
    for (int t = 0; t < k; t++) { int v; do v = rnd() % np; while (in[v]); for (int q = 0; q < deg[v]; q++) if (in[adj[v][q]]) del(adj[v][q]); add(v); }
    improve();
    if (ns > best) { best = ns; memcpy(bestsol, sol, sizeof(int) * ns); printf("best %d at %.1f s\n", best, (double)(clock() - st) / CLOCKS_PER_SEC); fflush(stdout); }
    else if (ns < best - 2 - (int)(rnd() % 3)) { /* restart from the best */ while (ns) del(sol[0]); for (int i = 0; i < best; i++) add(bestsol[i]); } }
  printf("n %d D %d primes %d best %d after %ld perturbations\n", n, D, np, best, it);
  FILE *o = fopen(argv[5], "w"); for (int i = 0; i < best; i++) fprintf(o, "%d\n", pr[bestsol[i]]); fclose(o);
  return 0; }
