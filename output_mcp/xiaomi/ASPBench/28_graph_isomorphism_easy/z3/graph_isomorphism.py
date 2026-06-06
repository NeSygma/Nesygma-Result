from z3 import *

# Graph definitions
# G1 vertices: 0,1,2,3,4
# G2 vertices: a,b,c,d,e (mapped to 0,1,2,3,4 internally)

# G1 edges (undirected)
g1_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]

# G2 edges (undirected) - map a=0, b=1, c=2, d=3, e=4
g2_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]

# G2 vertex names for output
g2_names = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}

n = 5  # number of vertices

solver = Solver()

# f[i] = the G2 vertex (0-4) that G1 vertex i maps to
f = [Int(f'f_{i}') for i in range(n)]

# Constraint 1: Bijection - each f[i] is in range [0, n-1] and all distinct
for i in range(n):
    solver.add(f[i] >= 0, f[i] < n)
solver.add(Distinct(f))

# Build adjacency sets for quick lookup
g1_adj = set()
for u, v in g1_edges:
    g1_adj.add((min(u,v), max(u,v)))

g2_adj = set()
for u, v in g2_edges:
    g2_adj.add((min(u,v), max(u,v)))

# Constraint 2: Adjacency preservation - for all edges (u,v) in G1, (f(u),f(v)) must be an edge in G2
for u, v in g1_edges:
    # (f[u], f[v]) must be an edge in G2
    edge_constraints = []
    for a, b in g2_adj:
        edge_constraints.append(Or(And(f[u] == a, f[v] == b), And(f[u] == b, f[v] == a)))
    solver.add(Or(edge_constraints))

# Constraint 3: Reverse preservation - for all edges (a,b) in G2, there must be an edge (u,v) in G1 with f(u)=a, f(v)=b
for a, b in g2_adj:
    edge_constraints = []
    for u, v in g1_adj:
        edge_constraints.append(Or(And(f[u] == a, f[v] == b), And(f[u] == b, f[v] == a)))
    solver.add(Or(edge_constraints))

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    mapping = {}
    for i in range(n):
        g2_val = model.evaluate(f[i]).as_long()
        mapping[str(i)] = g2_names[g2_val]
    
    # Build preserved edges
    preserved = []
    for u, v in g1_edges:
        fu = model.evaluate(f[u]).as_long()
        fv = model.evaluate(f[v]).as_long()
        preserved.append([f"{u},{v}", f"{g2_names[fu]},{g2_names[fv]}"])
    
    print("STATUS: sat")
    print(f"is_isomorphic: True")
    print(f"mapping: {mapping}")
    print(f"preserved_edges: {preserved}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("is_isomorphic: False")
    print("mapping: null")
    print("preserved_edges: []")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")