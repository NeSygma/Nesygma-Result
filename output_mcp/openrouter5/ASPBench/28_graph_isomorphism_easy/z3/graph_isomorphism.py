from z3 import *

# Graph 1 vertices: 0, 1, 2, 3, 4
# Graph 2 vertices: a, b, c, d, e (we'll map to indices 0..4)
# G2 vertex names as strings for output
g2_names = ['a', 'b', 'c', 'd', 'e']

# Edges of G1 (as pairs of vertex indices)
g1_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]

# Edges of G2 (as pairs of vertex indices 0..4)
g2_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]

# Build adjacency sets for quick checking
g1_adj = {i: set() for i in range(5)}
for u,v in g1_edges:
    g1_adj[u].add(v)
    g1_adj[v].add(u)

g2_adj = {i: set() for i in range(5)}
for u,v in g2_edges:
    g2_adj[u].add(v)
    g2_adj[v].add(u)

# Degree of each vertex
g1_deg = [len(g1_adj[i]) for i in range(5)]
g2_deg = [len(g2_adj[i]) for i in range(5)]

solver = Solver()

# f[i] = the G2 vertex (0..4) that G1 vertex i maps to
f = [Int(f'f_{i}') for i in range(5)]

# Domain: each f[i] is a G2 vertex index
for i in range(5):
    solver.add(f[i] >= 0, f[i] <= 4)

# Bijection: all f[i] are distinct (injective + same cardinality = bijective)
solver.add(Distinct(f))

# Degree preservation: degree of G1 vertex i must equal degree of G2 vertex f[i]
for i in range(5):
    # Use Or-loop to constrain degree
    solver.add(Or([And(f[i] == j, g1_deg[i] == g2_deg[j]) for j in range(5)]))

# Adjacency preservation: for every edge (u,v) in G1, (f(u), f(v)) must be an edge in G2
for u, v in g1_edges:
    # (f[u], f[v]) must be an edge in G2
    # Build a constraint that checks all possible pairs
    edge_constraints = []
    for j in range(5):
        for k in range(5):
            if (j, k) in g2_edges or (k, j) in g2_edges:
                edge_constraints.append(And(f[u] == j, f[v] == k))
    solver.add(Or(edge_constraints))

# Reverse preservation: for every edge (j,k) in G2, there must be an edge (u,v) in G1
# such that f(u)=j and f(v)=k (or f(u)=k and f(v)=j)
for j, k in g2_edges:
    reverse_constraints = []
    for u, v in g1_edges:
        # Either (f[u]=j and f[v]=k) or (f[u]=k and f[v]=j)
        reverse_constraints.append(Or(And(f[u] == j, f[v] == k), And(f[u] == k, f[v] == j)))
    solver.add(Or(reverse_constraints))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("is_isomorphic: true")
    
    # Build mapping
    mapping = {}
    for i in range(5):
        g2_idx = m.eval(f[i]).as_long()
        mapping[str(i)] = g2_names[g2_idx]
    print(f"mapping: {mapping}")
    
    # Build preserved edges
    preserved = []
    for u, v in g1_edges:
        fu = g2_names[m.eval(f[u]).as_long()]
        fv = g2_names[m.eval(f[v]).as_long()]
        preserved.append([f"{u},{v}", f"{fu},{fv}"])
    print(f"preserved_edges: {preserved}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")