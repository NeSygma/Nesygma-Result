from z3 import *

# Graph definitions
# G1 vertices: 0, 1, 2, 3, 4
# G2 vertices: a=0, b=1, c=2, d=3, e=4
g2_names = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}

# G1 edges (undirected)
g1_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]
# G2 edges (undirected)
g2_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]

# Build adjacency sets for both graphs
g1_adj = set()
for u, v in g1_edges:
    g1_adj.add((u, v))
    g1_adj.add((v, u))

g2_adj = set()
for u, v in g2_edges:
    g2_adj.add((u, v))
    g2_adj.add((v, u))

n = 5  # number of vertices

solver = Solver()

# f[i] = the G2 vertex that G1 vertex i maps to
f = [Int(f'f_{i}') for i in range(n)]

# Bijection: each f[i] is in range [0, n-1] and all are distinct
for i in range(n):
    solver.add(f[i] >= 0, f[i] < n)
solver.add(Distinct(f))

# Adjacency preservation: for every pair (u,v), 
# (u,v) is an edge in G1 iff (f(u),f(v)) is an edge in G2
for u in range(n):
    for v in range(u+1, n):
        g1_has_edge = (u, v) in g1_adj
        # We need: g1_has_edge <=> (f(u),f(v)) is edge in g2
        # Build the condition that (f(u),f(v)) is an edge in g2
        # Using Or over all possible mappings
        g2_edge_conds = []
        for (a, b) in g2_edges:
            g2_edge_conds.append(Or(
                And(f[u] == a, f[v] == b),
                And(f[u] == b, f[v] == a)
            ))
        
        if g1_has_edge:
            # Must be an edge in G2
            solver.add(Or(g2_edge_conds))
        else:
            # Must NOT be an edge in G2
            solver.add(Not(Or(g2_edge_conds)))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("is_isomorphic: true")
    
    # Build mapping
    mapping = {}
    for i in range(n):
        g2_val = m.evaluate(f[i]).as_long()
        mapping[str(i)] = g2_names[g2_val]
    
    print("mapping:", mapping)
    
    # Build preserved edges
    preserved = []
    for u, v in g1_edges:
        fu = m.evaluate(f[u]).as_long()
        fv = m.evaluate(f[v]).as_long()
        preserved.append([f"{u},{v}", f"{g2_names[fu]},{g2_names[fv]}"])
    
    print("preserved_edges:", preserved)
    
elif result == unsat:
    print("STATUS: unsat")
    print("is_isomorphic: false")
    print("mapping: null")
    print("preserved_edges: []")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (graphs may not be isomorphic)")
else:
    print("STATUS: unknown")