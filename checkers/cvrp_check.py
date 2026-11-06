"""Exact check of a capacitated vehicle routing solution (CVRPLIB conventions; standard library only).

  python3 -I cvrp_check.py INSTANCE.vrp SOLUTION.sol

INSTANCE is a TSPLIB-format CVRP file with EDGE_WEIGHT_TYPE EUC_2D: the distance between two nodes is the Euclidean
distance rounded to the nearest integer, computed here in integers (m = isqrt(d2), plus one when 4 d2 > (2m + 1)^2),
so no rounding of floating point can change it. SOLUTION has one line per route, "Route #k: c1 c2 ...", customers
numbered 1..n-1 as on CVRPLIB (node c + 1 of the instance when the depot is node 1). Every customer must appear exactly
once and no route may carry more than CAPACITY. Prints "cost C" (depot to depot over every route) and exits 0 when the
solution is valid, exits 1 otherwise; a "Cost" line in the file, if any, is compared and reported."""
import math
import re
import sys


def read_instance(path):
    lines = [l.strip() for l in open(path) if l.strip()]
    head, sec = {}, None
    coords, demand, depots = {}, {}, []
    for l in lines:
        if ":" in l and sec is None or re.match(r"^[A-Z_]+\s*:", l):
            k, v = l.split(":", 1)
            head[k.strip()] = v.strip()
            continue
        if l in ("NODE_COORD_SECTION", "DEMAND_SECTION", "DEPOT_SECTION"):
            sec = l
            continue
        if l == "EOF":
            break
        parts = l.split()
        if sec == "NODE_COORD_SECTION":
            coords[int(parts[0])] = (int(float(parts[1])), int(float(parts[2])))
            assert float(parts[1]) == int(float(parts[1])) and float(parts[2]) == int(float(parts[2])), "integer coordinates expected"
        elif sec == "DEMAND_SECTION":
            demand[int(parts[0])] = int(parts[1])
        elif sec == "DEPOT_SECTION" and int(parts[0]) != -1:
            depots.append(int(parts[0]))
    assert head.get("EDGE_WEIGHT_TYPE") == "EUC_2D", "only EUC_2D instances"
    n = int(head["DIMENSION"])
    assert len(coords) == n and len(demand) == n and len(depots) == 1
    return n, int(head["CAPACITY"]), coords, demand, depots[0]


def dist(a, b):
    d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    m = math.isqrt(d2)
    return m + 1 if 4 * d2 > (2 * m + 1) ** 2 else m


def main():
    n, cap, coords, demand, depot = read_instance(sys.argv[1])
    assert depot == 1, "depot must be node 1 (CVRPLIB numbering)"
    routes, stated = [], None
    for l in open(sys.argv[2]):
        m = re.match(r"^\s*Route\s*#\s*\d+\s*:(.*)$", l)
        if m:
            routes.append([int(x) + 1 for x in m.group(1).split()])
        m = re.match(r"^\s*Cost\s+(\d+)", l)
        if m:
            stated = int(m.group(1))
    seen = [0] * (n + 1)
    total = 0
    for r in routes:
        if not r:
            continue
        for c in r:
            if not (2 <= c <= n):
                print(f"customer {c - 1} out of range")
                return 1
            seen[c] += 1
        load = sum(demand[c] for c in r)
        if load > cap:
            print(f"a route carries {load} > capacity {cap}")
            return 1
        path = [depot] + r + [depot]
        total += sum(dist(coords[a], coords[b]) for a, b in zip(path, path[1:]))
    missing = [c - 1 for c in range(2, n + 1) if seen[c] != 1]
    if missing:
        print(f"{len(missing)} customers not visited exactly once (first: {missing[:5]})")
        return 1
    print(f"routes {sum(1 for r in routes if r)}; every customer once; capacity {cap} respected")
    if stated is not None:
        print(f"the file states cost {stated}: {'equal' if stated == total else 'DIFFERENT'}")
    print(f"cost {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
