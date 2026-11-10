"""Graph invariants of the regular 4-polytopes and the E8 polytopes: the search behind the polytope-invariant
problems of the Quantavane Originals (OR-Tools CP-SAT models and local search; our own code; run with a Python that
has ortools).

  python3 polytope_sets.py PROBLEM KIND SECONDS OUT.txt [SEED]

PROBLEM and KIND as in checkers/orig_graphs.py (the graphs are built by that checker, so the search and the checker
agree). Writes the best certificate found to OUT.txt and prints one JSON line: the value, whether it was proved
optimal (an exhaustive search: CP-SAT proved the bound, or the fort cuts closed the gap) and the best bound proved.

  zero-forcing, power-domination  (graphs of at most 24 vertices: every vertex set, by size) integer programs over
      forts: a set Z forces the graph exactly when it meets every
      fort (a nonempty set F of vertices such that no vertex outside F has exactly one neighbour in F; Brimkov,
      Fast and Hicks 2019). Forts are generated lazily: the white vertices left when a candidate set stops forcing
      form a fort. The optimum of the relaxed program over the forts found so far is a lower bound; a candidate
      that forces everything is an upper bound; the loop stops when they meet or time runs out (the best forcing
      set found, completed greedily, is kept). For power domination the constraint for a fort F is that the set
      meets N[F].
  locating-dom, induced-matching, bisection, l21, burning, resolving, bandwidth, total-dom, independent-dom,
      induced-bipartite, distance2-colouring, code-D (a code of minimum distance D)  direct CP-SAT models (bandwidth
      by a decision model for each width, started from the best Cuthill-McKee numbering).
  max-leaf  a connected dominating set (exhaustive up to 24 vertices; greedy growth and pruning beyond), made the
      internal vertices of a spanning tree."""
import importlib.util
import itertools
import json
import os
import random
import sys
import time
from collections import deque

from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = importlib.util.spec_from_file_location("orig_graphs", os.path.join(HERE, "checkers", "orig_graphs.py"))
G = importlib.util.module_from_spec(_s)
_s.loader.exec_module(G)


def solver(seconds):
    s = cp_model.CpSolver()
    s.parameters.max_deterministic_time = max(1.0, seconds)    # work-based, so pauses of the process do not cut it
    s.parameters.num_workers = 1
    return s


def dist_all(adj):
    return [G.bfs(adj, v) for v in range(len(adj))]


def chrono_model(n, adj, seconds, power):
    """Exact model of a chronological list of forces (Brimkov, Fast and Hicks): every vertex is either in the
    starting set (for power domination: observed at time 0, i.e. in N[S]) or forced by exactly one neighbour u at a
    time after u and all of u's other neighbours."""
    m = cp_model.CpModel()
    x = [m.NewBoolVar("") for _ in range(n)]
    z = [m.NewBoolVar("") for _ in range(n)] if power else x
    t = [m.NewIntVar(0, n, "") for _ in range(n)]
    y = {}
    for u in range(n):
        for v in adj[u]:
            y[u, v] = m.NewBoolVar("")
    for v in range(n):
        m.Add(z[v] + sum(y[u, v] for u in adj[v]) == 1)
        if power:
            m.AddBoolOr([x[v]] + [x[u] for u in adj[v]]).OnlyEnforceIf(z[v])
            m.Add(t[v] == 0).OnlyEnforceIf(z[v])
    for u in range(n):
        m.Add(sum(y[u, v] for v in adj[u]) <= 1)
        for v in adj[u]:
            for w in (adj[u] - {v}) | {u}:
                m.Add(t[v] >= t[w] + 1).OnlyEnforceIf(y[u, v])
    m.Minimize(sum(x))
    s = solver(seconds)
    st = s.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, 0, False
    return [v for v in range(n) if s.Value(x[v])], int(round(s.BestObjectiveBound())), st == cp_model.OPTIMAL


def forts_search(n, adj, seconds, power, rng):
    """Lazy fort cuts. Returns (best set, lower bound, proved). Graphs with at most 24 vertices are searched
    exhaustively instead (at most 16 vertices): every vertex set of size 0, 1, 2, ... until one forces (or observes)
    the graph. Each fort found is shrunk to a minimal fort before it becomes a cut."""
    t0 = time.time()
    nb = [adj[v] | {v} for v in range(n)]
    def closure(z):
        obs = set(z)
        if power:
            for v in z:
                obs |= adj[v]
        return G.force(adj, obs)
    if n <= 16:
        for k in range(n + 1):
            for z in itertools.combinations(range(n), k):
                if len(closure(z)) == n:
                    return list(z), k, True
    if n <= 60:
        z, lb, ok = chrono_model(n, adj, seconds, power)
        if z is not None and len(closure(z)) == n:
            return z, lb, ok
    def complete(z):
        z = list(z)
        while len(closure(z)) < n:
            c = closure(z)
            left = [v for v in range(n) if v not in c]
            best = max(rng.sample(left, min(40, len(left))), key=lambda v: (len(closure(z + [v])), rng.random()))
            z.append(best)
        return z
    def prune(z):
        z = list(z)
        rng.shuffle(z)
        for v in list(z):
            w = [u for u in z if u != v]
            if len(closure(w)) == n:
                z = w
        return z
    forts = []
    best = prune(complete([]))
    for _ in range(5):
        z = prune(complete([rng.randrange(n)]))
        if len(z) < len(best):
            best = z
    lb, proved = 0, False
    while time.time() - t0 < seconds:
        m = cp_model.CpModel()
        x = [m.NewBoolVar("") for _ in range(n)]
        for f in forts:
            cover = set()
            for v in f:
                cover |= nb[v] if power else {v}
            m.AddBoolOr([x[v] for v in cover])
        m.Minimize(sum(x))
        for v in range(n):
            m.AddHint(x[v], v in best)
        s = solver(seconds - (time.time() - t0))
        st = s.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break
        z = [v for v in range(n) if s.Value(x[v])]
        if st == cp_model.OPTIMAL:
            lb = max(lb, len(z))
        c = closure(z)
        if len(c) == n:
            if len(z) < len(best):
                best = z
            if st == cp_model.OPTIMAL:
                proved = True
                break
            continue
        f = set(range(n)) - c
        for v in rng.sample(sorted(f), len(f)):          # shrink to a minimal fort: no outside vertex sees exactly one
            g = f - {v}
            if g and all(len(adj[u] & g) != 1 for u in range(n) if u not in g):
                f = g
        forts.append(frozenset(f))
        zz = prune(complete(z))
        if len(zz) < len(best):
            best = zz
        if lb >= len(best):
            proved = True
            break
    return best, lb, proved or lb >= len(best)


def cpsat(problem, n, edges, adj, seconds, hint=None):
    m = cp_model.CpModel()
    if problem == "locating-dom":
        x = [m.NewBoolVar("") for _ in range(n)]
        for v in range(n):
            m.AddBoolOr([x[v]] + [x[w] for w in adj[v]])
        for u, v in itertools.combinations(range(n), 2):
            m.AddBoolOr([x[u], x[v]] + [x[w] for w in adj[u] ^ adj[v] if w not in (u, v)])
        m.Minimize(sum(x))
        sense = "min"
    elif problem == "resolving":
        D = dist_all(adj)
        x = [m.NewBoolVar("") for _ in range(n)]
        for u, v in itertools.combinations(range(n), 2):
            m.AddBoolOr([x[w] for w in range(n) if D[w][u] != D[w][v]])
        m.Minimize(sum(x))
        sense = "min"
    elif problem == "induced-matching":
        x = [m.NewBoolVar("") for _ in edges]
        inc = [[] for _ in range(n)]
        for i, (a, b) in enumerate(edges):
            inc[a].append(i)
            inc[b].append(i)
        for a, b in edges:
            m.AddAtMostOne([x[i] for i in set(inc[a]) | set(inc[b])])
        m.Maximize(sum(x))
        sense = "max"
    elif problem == "bisection":
        x = [m.NewBoolVar("") for _ in range(n)]
        m.Add(sum(x) == n // 2)
        m.AddHint(x[0], 0)
        m.Add(x[0] == 0)
        cut = []
        for a, b in edges:
            c = m.NewBoolVar("")
            m.Add(c >= x[a] - x[b])
            m.Add(c >= x[b] - x[a])
            cut.append(c)
        m.Minimize(sum(cut))
        sense = "min"
    elif problem == "l21":
        ub = 2 * max(len(a) for a in adj) + max(len(a) for a in adj) ** 2
        x = [m.NewIntVar(0, ub, "") for _ in range(n)]
        for a, b in edges:
            o = m.NewBoolVar("")
            m.Add(x[a] - x[b] >= 2).OnlyEnforceIf(o)
            m.Add(x[b] - x[a] >= 2).OnlyEnforceIf(o.Not())
        for v in range(n):
            if len(adj[v]) >= 2:
                m.AddAllDifferent([x[w] for w in adj[v]])
        span = m.NewIntVar(0, ub, "")
        m.AddMaxEquality(span, x)
        m.Add(x[0] == 0)
        m.Minimize(span)
        sense = "min"
    elif problem == "total-dom":
        x = [m.NewBoolVar("") for _ in range(n)]
        for v in range(n):
            m.AddBoolOr([x[w] for w in adj[v]])
        m.Minimize(sum(x))
        sense = "min"
    elif problem == "ising":
        x = [m.NewBoolVar("") for _ in range(n)]
        m.Add(x[0] == 0)
        cut = []
        for a, b in edges:
            c = m.NewBoolVar("")
            m.Add(c <= x[a] + x[b])
            m.Add(c <= 2 - x[a] - x[b])
            cut.append(c)
        m.Maximize(sum(cut))
        sense = "max"
    elif problem == "domination":
        x = [m.NewBoolVar("") for _ in range(n)]
        for v in range(n):
            m.AddBoolOr([x[v]] + [x[w] for w in adj[v]])
        m.Minimize(sum(x))
        sense = "min"
    elif problem == "independent":
        x = [m.NewBoolVar("") for _ in range(n)]
        for a, b in edges:
            m.AddBoolOr([x[a].Not(), x[b].Not()])
        m.Maximize(sum(x))
        sense = "max"
    elif problem == "roman":
        one = [m.NewBoolVar("") for _ in range(n)]
        two = [m.NewBoolVar("") for _ in range(n)]
        for v in range(n):
            m.AddBoolOr([one[v].Not(), two[v].Not()])
            m.AddBoolOr([one[v], two[v]] + [two[w] for w in adj[v]])
        m.Minimize(sum(one) + 2 * sum(two))
        x = one + two
        sense = "min"
    elif problem == "2-domination":
        x = [m.NewBoolVar("") for _ in range(n)]
        for v in range(n):
            m.Add(2 * x[v] + sum(x[w] for w in adj[v]) >= 2)
        m.Minimize(sum(x))
        sense = "min"
    elif problem == "independent-dom":
        x = [m.NewBoolVar("") for _ in range(n)]
        for a, b in edges:
            m.AddBoolOr([x[a].Not(), x[b].Not()])
        for v in range(n):
            m.AddBoolOr([x[v]] + [x[w] for w in adj[v]])
        m.Minimize(sum(x))
        sense = "min"
    elif problem == "induced-bipartite":
        x = [m.NewBoolVar("") for _ in range(n)]
        side = [m.NewBoolVar("") for _ in range(n)]
        m.Add(side[0] == 0)
        for a, b in edges:
            m.AddBoolOr([x[a].Not(), x[b].Not(), side[a], side[b]])
            m.AddBoolOr([x[a].Not(), x[b].Not(), side[a].Not(), side[b].Not()])
        m.Maximize(sum(x))
        sense = "max"
    elif problem == "distance2-colouring":
        ub = max(len(a) for a in adj) ** 2 + 1
        x = [m.NewIntVar(0, ub, "") for _ in range(n)]
        for v in range(n):
            m.AddAllDifferent([x[v]] + [x[w] for w in adj[v]])
        near = [adj[v] | {w for u in adj[v] for w in adj[u]} - {v} for v in range(n)]
        clique = []                          # a greedy clique of the square: all its colours differ (a redundant cut)
        for v in sorted(range(n), key=lambda v: -len(near[v])):
            if all(u in near[v] for u in clique):
                clique.append(v)
        m.AddAllDifferent([x[v] for v in clique])
        top = m.NewIntVar(0, ub, "")
        m.AddMaxEquality(top, x)
        m.Add(x[0] == 0)
        m.Minimize(top)
        sense = "min"
    elif problem.startswith("code-"):
        d = int(problem.split("-")[1])
        D = dist_all(adj)
        x = [m.NewBoolVar("") for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                if D[u][v] < d:
                    m.AddBoolOr([x[u].Not(), x[v].Not()])
        m.Maximize(sum(x))
        sense = "max"
    else:
        raise ValueError(problem)
    if hint is not None:
        for v, h in zip(x, hint):
            m.AddHint(v, h)
    s = solver(seconds)
    st = s.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    val = int(round(s.ObjectiveValue()))
    bound = int(round(s.BestObjectiveBound()))
    if problem == "ising":                           # energy = -(edges cut) + (edges not cut)
        val, bound = len(edges) - 2 * val, len(edges) - 2 * bound
    if problem == "distance2-colouring":
        val, bound = val + 1, bound + 1              # colours 0..top: top + 1 of them
    if problem == "induced-matching":
        cert = [edges[i] for i in range(len(edges)) if s.Value(x[i])]
    elif problem in ("bisection", "l21", "distance2-colouring"):
        cert = [s.Value(v) for v in x]
    elif problem == "roman":
        cert = [2 if s.Value(x[n + v]) else 1 if s.Value(x[v]) else 0 for v in range(n)]
    elif problem == "ising":
        cert = "".join("+" if s.Value(x[v]) == 0 else "-" for v in range(n))
    elif problem == "induced-bipartite":
        cert = "".join(("1" if s.Value(side[v]) else "0") if s.Value(x[v]) else "." for v in range(n))
    else:
        cert = [v for v in range(n) if s.Value(x[v])]
    return cert, val, bound, st == cp_model.OPTIMAL


def resolving_greedy(n, adj, seconds, rng):
    """Greedy resolving set (add the vertex that splits the classes most), then pruning; restarts until time is up."""
    D = dist_all(adj)
    t0 = time.time()
    best = None
    def resolves(w):
        return len({tuple(D[x][v] for x in w) for v in range(n)}) == n
    while time.time() - t0 < seconds:
        w = []
        cls = {(): list(range(n))}
        while len(cls) < n:
            def score(x):
                return len({tuple(k) + (D[x][v],) for k, vs in cls.items() for v in vs})
            cand = rng.sample(range(n), min(n, 60))
            x = max(cand, key=lambda x: (score(x), rng.random()))
            w.append(x)
            new = {}
            for k, vs in cls.items():
                for v in vs:
                    new.setdefault(k + (D[x][v],), []).append(v)
            cls = new
        rng.shuffle(w)
        for x in list(w):
            ww = [y for y in w if y != x]
            if resolves(ww):
                w = ww
        if best is None or len(w) < len(best):
            best = w
    return best


def max_leaf(n, adj, seconds, rng):
    """A spanning tree whose internal vertices form a small connected dominating set (max leaves = n - the connected
    domination number). Up to 24 vertices: every vertex set by size, the first connected dominating set found is
    optimal. Larger graphs: greedy growth (add the neighbour of the set that dominates the most new vertices), then
    pruning of removable vertices, repeated from random starts until time is up."""
    t0 = time.time()
    def connected(S):
        S = set(S)
        if not S:
            return False
        start = next(iter(S))
        seen, q = {start}, deque([start])
        while q:
            u = q.popleft()
            for w in adj[u] & S:
                if w not in seen:
                    seen.add(w)
                    q.append(w)
        return len(seen) == len(S)
    def dominating(S):
        dom = set(S)
        for v in S:
            dom |= adj[v]
        return len(dom) == n
    best, proved = None, False
    if n <= 24:
        for k in range(1, n + 1):
            best = next((list(S) for S in itertools.combinations(range(n), k) if dominating(S) and connected(S)), None)
            if best:
                proved = True
                break
    else:
        while time.time() - t0 < seconds:
            v0 = rng.randrange(n)
            S, dom = [v0], adj[v0] | {v0}
            while len(dom) < n:
                cand = {w for u in S for w in adj[u]} - set(S)
                w = max(cand, key=lambda w: (len((adj[w] | {w}) - dom), rng.random()))
                S.append(w)
                dom |= adj[w] | {w}
            for v in rng.sample(S, len(S)):
                T = [u for u in S if u != v]
                if dominating(T) and connected(T):
                    S = T
            if best is None or len(S) < len(best):
                best = S
    S = set(best)
    tree, seen = [], {best[0]}
    q = deque([best[0]])
    while q:                                  # a BFS tree of the dominating set, then every other vertex as a leaf
        u = q.popleft()
        for w in sorted(adj[u] & S):
            if w not in seen:
                seen.add(w)
                tree.append((u, w))
                q.append(w)
    for v in range(n):
        if v not in S:
            tree.append((min(adj[v] & S), v))
    deg = [0] * n
    for a, b in tree:
        deg[a] += 1
        deg[b] += 1
    return tree, sum(1 for x in deg if x == 1), proved


def colour_search(problem, n, edges, adj, seconds):
    """grundy (maximize the largest colour of a Grundy colouring), b-colouring and domatic (largest K for which the
    decision model is satisfiable, trying K downwards from the bound d + 1), strong-edge (minimize the largest edge
    colour). Returns (certificate lines, value, proved)."""
    t0 = time.time()
    d = max(len(a) for a in adj)
    if problem == "grundy":
        K = d + 1
        m = cp_model.CpModel()
        y = [[m.NewBoolVar("") for _ in range(K)] for _ in range(n)]
        for v in range(n):
            m.AddExactlyOne(y[v])
            for k in range(K):
                for j in range(k):
                    m.AddBoolOr([y[w][j] for w in adj[v]]).OnlyEnforceIf(y[v][k])
        for a, b in edges:
            for k in range(K):
                m.AddBoolOr([y[a][k].Not(), y[b][k].Not()])
        used = [m.NewBoolVar("") for _ in range(K)]        # a Grundy colouring uses colours 1..k, all of them
        for k in range(K):
            m.AddBoolOr([y[v][k] for v in range(n)]).OnlyEnforceIf(used[k])
        m.Maximize(sum(used))
        s = solver(seconds)
        st = s.Solve(m)
        col = [next(k + 1 for k in range(K) if s.Value(y[v][k])) for v in range(n)]
        return " ".join(map(str, col)), max(col), st == cp_model.OPTIMAL and max(col) == round(s.ObjectiveValue())
    if problem == "strong-edge":
        m = cp_model.CpModel()
        E = [tuple(sorted(e)) for e in edges]
        idx = {e: i for i, e in enumerate(E)}
        K = 2 * d * d
        c = [m.NewIntVar(0, K, "") for _ in E]
        for i, (a, b) in enumerate(E):
            near = set()
            for x in (a, b):
                for y in adj[x] | {x}:
                    for z in adj[y]:
                        near.add(idx[tuple(sorted((y, z)))])
            near.discard(i)
            for j in near:
                if j > i:
                    m.Add(c[i] != c[j])
        for v in range(n):                    # the edges at a vertex pairwise conflict: a redundant all-different
            m.AddAllDifferent([c[idx[tuple(sorted((v, w)))]] for w in adj[v]])
        top = m.NewIntVar(0, K, "")
        m.AddMaxEquality(top, c)
        m.Minimize(top)
        s = solver(seconds)
        st = s.Solve(m)
        lines = "\n".join(f"{a} {b} {s.Value(c[i])}" for i, (a, b) in enumerate(E))
        return lines, len({s.Value(x) for x in c}), st == cp_model.OPTIMAL
    # b-colouring and domatic: decision models for K = d + 1, d, ...
    best = None
    for K in range(d + 1, 0, -1):
        left = seconds - (time.time() - t0)
        if left <= 0:
            break
        m = cp_model.CpModel()
        y = [[m.NewBoolVar("") for _ in range(K)] for _ in range(n)]
        for v in range(n):
            m.AddExactlyOne(y[v])
        if problem == "b-colouring":
            for a, b in edges:
                for k in range(K):
                    m.AddBoolOr([y[a][k].Not(), y[b][k].Not()])
            for k in range(K):
                z = [m.NewBoolVar("") for _ in range(n)]
                m.AddBoolOr(z)
                for v in range(n):
                    m.AddImplication(z[v], y[v][k])
                    for j in range(K):
                        if j != k:
                            m.AddBoolOr([y[w][j] for w in adj[v]]).OnlyEnforceIf(z[v])
        else:
            for v in range(n):
                for k in range(K):
                    m.AddBoolOr([y[v][k]] + [y[w][k] for w in adj[v]])
        s = solver(left)
        st = s.Solve(m)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            col = [next(k for k in range(K) if s.Value(y[v][k])) for v in range(n)]
            return " ".join(map(str, col)), K, best is None or best == "infeasible-above"
        if st == cp_model.INFEASIBLE:
            best = "infeasible-above"
            continue
        best = "unknown-above"
    return None, None, False


def linear_arrangement(n, edges, adj, seconds, rng):
    """Spectral and breadth-first numberings, then adjacent swaps and short moves that lower the total edge length,
    restarted until time is up (a heuristic: the value is an upper bound)."""
    t0 = time.time()
    def cost(order):
        pos = {v: i for i, v in enumerate(order)}
        return sum(abs(pos[a] - pos[b]) for a, b in edges)
    if n <= 8:                                   # every numbering (its reverse has the same length)
        best = min((p for p in itertools.permutations(range(n)) if p[0] < p[-1]), key=cost)
        return list(best), cost(best), True
    starts = []
    for s0 in rng.sample(range(n), min(n, 8)):
        order, seen = [], {s0}
        q = deque([s0])
        while q:
            u = q.popleft()
            order.append(u)
            for w in sorted(adj[u]):
                if w not in seen:
                    seen.add(w)
                    q.append(w)
        starts.append(order)
    best = min(starts, key=cost)
    bestc = cost(best)
    while time.time() - t0 < seconds:
        order = list(rng.choice(starts))
        pos = {v: i for i, v in enumerate(order)}
        improved = True
        while improved and time.time() - t0 < seconds:
            improved = False
            for i in range(n - 1):
                a, b = order[i], order[i + 1]
                # swapping neighbours in the order changes only the edges at a and b
                delta = 0
                for w in adj[a]:
                    if w != b:
                        delta += abs(pos[w] - (i + 1)) - abs(pos[w] - i)
                for w in adj[b]:
                    if w != a:
                        delta += abs(pos[w] - i) - abs(pos[w] - (i + 1))
                if delta < 0:
                    order[i], order[i + 1] = b, a
                    pos[a], pos[b] = i + 1, i
                    improved = True
        c = cost(order)
        if c < bestc:
            best, bestc = order, c
        starts.append(order)
    return best, bestc, False


def burning(n, adj, seconds):
    """Starts at the ball-counting bound: b >= the least k with |B_0| + ... + |B_(k-1)| >= n, |B_r| the largest ball
    of radius r in the graph."""
    D = dist_all(adj)
    t0 = time.time()
    diam = max(max(r) for r in D)
    ball = [0] * (diam + 1)
    for v in range(n):
        h = [0] * (diam + 1)
        for d in D[v]:
            h[d] += 1
        c = 0
        for r in range(diam + 1):
            c += h[r]
            ball[r] = max(ball[r], c)
    ball += [n] * n
    k = next(k for k in range(1, n + 1) if sum(ball[:k]) >= n)
    best = None
    lower = k
    while time.time() - t0 < seconds:
        m = cp_model.CpModel()
        x = [[m.NewBoolVar("") for _ in range(n)] for _ in range(k)]
        for i in range(k):
            m.AddExactlyOne(x[i])
        for v in range(n):
            m.AddAtMostOne([x[i][v] for i in range(k)])
        for u in range(n):
            m.AddBoolOr([x[i][v] for i in range(k) for v in range(n) if D[u][v] <= k - 1 - i])
        s = solver(seconds - (time.time() - t0))
        st = s.Solve(m)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            best = [next(v for v in range(n) if s.Value(x[i][v])) for i in range(k)]
            return best, k, lower == k
        if st == cp_model.INFEASIBLE:
            lower = k + 1
            k += 1
            continue
        break
    return None, None, False


def bandwidth(n, edges, adj, seconds):
    t0 = time.time()
    def width(order):
        pos = {v: i for i, v in enumerate(order)}
        return max(abs(pos[a] - pos[b]) for a, b in edges)
    best = None
    for s0 in range(n):
        order, seen = [], {s0}
        q = deque([s0])
        while q:
            u = q.popleft()
            order.append(u)
            for w in sorted(adj[u], key=lambda w: len(adj[w])):
                if w not in seen:
                    seen.add(w)
                    q.append(w)
        if best is None or width(order) < width(best):
            best = order
    bw = width(best)
    lower, proved = 0, False
    while bw > 1 and time.time() - t0 < seconds:
        target = bw - 1
        m = cp_model.CpModel()
        p = [m.NewIntVar(0, n - 1, "") for _ in range(n)]
        m.AddAllDifferent(p)
        for a, b in edges:
            m.Add(p[a] - p[b] <= target)
            m.Add(p[b] - p[a] <= target)
        s = solver(seconds - (time.time() - t0))
        st = s.Solve(m)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            pos = [s.Value(v) for v in p]
            best = sorted(range(n), key=lambda v: pos[v])
            bw = width(best)
            continue
        if st == cp_model.INFEASIBLE:
            lower, proved = bw, True
        break
    return best, bw, lower, proved


def maximize(problem):
    return problem in ("induced-matching", "induced-bipartite", "max-leaf", "grundy", "b-colouring", "domatic",
                       "independent") or problem.startswith("code-")


def main():
    problem, kind, seconds, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    rng = random.Random(int(sys.argv[5]) if len(sys.argv) > 5 else 1)
    n, edges, adj = G.graph(kind)
    t = time.time()
    if problem in ("zero-forcing", "power-domination"):
        cert, lb, proved = forts_search(n, adj, seconds, problem == "power-domination", rng)
        val, bound = len(cert), lb
        text = " ".join(map(str, sorted(cert)))
    elif problem == "resolving" and n > 300:
        cert = resolving_greedy(n, adj, seconds, rng)
        val, bound, proved = len(cert), None, False
        text = " ".join(map(str, sorted(cert)))
    elif problem in ("grundy", "b-colouring", "domatic", "strong-edge"):
        text, val, proved = colour_search(problem, n, edges, adj, seconds)
        bound = val if proved else None
    elif problem == "linear-arrangement":
        cert, val, proved = linear_arrangement(n, edges, adj, seconds, rng)
        bound = val if proved else None
        text = " ".join(map(str, cert))
    elif problem == "max-leaf":
        cert, val, proved = max_leaf(n, adj, seconds, rng)
        bound = val if proved else None
        text = "\n".join(f"{a} {b}" for a, b in cert)
    elif problem == "burning":
        cert, val, proved = burning(n, adj, seconds)
        bound = val if proved else None
        text = " ".join(map(str, cert))
    elif problem == "bandwidth":
        cert, val, bound, proved = bandwidth(n, edges, adj, seconds)
        text = " ".join(map(str, cert))
    else:
        r = cpsat(problem, n, edges, adj, seconds)
        cert, val, bound, proved = r
        if problem == "induced-matching":
            text = "\n".join(f"{a} {b}" for a, b in cert)
        elif problem in ("bisection", "l21", "distance2-colouring", "roman"):
            text = " ".join(map(str, cert))
        elif problem in ("induced-bipartite", "ising"):
            text = cert
        else:
            text = " ".join(map(str, sorted(cert)))
    if os.path.exists(out):              # never replace a better certificate, or an equal one already proved optimal
        old = open(out).read().splitlines()
        try:
            oldv = int(old[0].split(": ")[1].split(" ")[0])
            oldp = "(optimal)" in old[0]
            better = oldv < val if maximize(problem) else oldv > val
            if not better and (oldv != val or not proved or oldp):
                print(json.dumps({"problem": problem, "kind": kind, "n": n, "value": oldv, "exact": oldp,
                                  "bound": oldv if oldp else bound, "kept": "the earlier certificate"}), flush=True)
                return
        except (IndexError, ValueError):
            pass
    with open(out, "w") as f:
        f.write(f"# {problem} on polytope {kind}: {val} ({'optimal' if proved else 'best found'})\n{text}\n")
    print(json.dumps({"problem": problem, "kind": kind, "n": n, "value": val, "exact": bool(proved), "bound": bound,
                      "seconds": round(time.time() - t, 1)}), flush=True)


if __name__ == "__main__":
    main()
