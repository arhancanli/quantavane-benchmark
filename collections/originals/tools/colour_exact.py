"""Second check of an exact colouring threshold (Quantavane Originals; python-sat; our own code).

  python3 colour_exact.py EQUATION K N

Builds, from the checker's own list of solutions (checkers/orig_colour.py), the formula 'every number gets one of K
colours, 1 gets colour 0, no solution is monochromatic' for 1..N and for 1..N+1, and solves both with three
different SAT solvers (CaDiCaL, Glucose, MiniSat). The threshold N is confirmed when all three find 1..N colourable
and 1..N+1 not."""
import importlib.util
import os
import sys

from pysat.solvers import Solver

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = importlib.util.spec_from_file_location("orig_colour", os.path.join(HERE, "checkers", "orig_colour.py"))
C = importlib.util.module_from_spec(_s)
_s.loader.exec_module(C)


def main():
    eq, k, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    var = lambda i, c: (i - 1) * k + c + 1
    verdict = {}
    for m in (n, n + 1):
        sols = list(C.EQUATIONS[eq](m))
        for name in ("cadical195", "glucose4", "minisat22"):
            with Solver(name=name) as s:
                s.add_clause([var(1, 0)])
                for i in range(1, m + 1):
                    s.add_clause([var(i, c) for c in range(k)])
                for q in sols:
                    for c in range(k):
                        s.add_clause([-var(i, c) for i in set(q)])
                verdict[(m, name)] = s.solve()
                print(f"{eq}, {k} colours, 1..{m}: {len(sols)} solutions, {name}: "
                      f"{'colourable' if verdict[(m, name)] else 'not colourable'}", flush=True)
    ok = all(verdict[(n, x)] for x in ("cadical195", "glucose4", "minisat22")) and \
        not any(verdict[(n + 1, x)] for x in ("cadical195", "glucose4", "minisat22"))
    print(f"threshold {n} {'confirmed' if ok else 'NOT confirmed'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
