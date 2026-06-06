from z3 import *

# Graph data
g1_vertices = [0, 1, 2, 3, 4]
g2_vertices = ['a', 'b', 'c', 'd', 'e']

g1_edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]
g2_edges = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e')]

# Create mapping from G1 vertex indices to G2 vertex strings
# We'll use an array where f[i] represents the mapping of G1 vertex i
f = [Int(f'f_{i}') for i in range(len(g1_vertices))]

solver = Solver()

# Constraint 1: Bijection - each G1 vertex maps to a unique G2 vertex
# f[i] should be in range 0..4 (representing indices of g2_vertices)
for i in range(len(g1_vertices)):
    solver.add(f[i] >= 0)
    solver.add(f[i] < len(g2_vertices))

# All f[i] must be distinct (bijection)
solver.add(Distinct(f))

# Constraint 2: Adjacency preservation
# For each edge (u,v) in G1, (f(u), f(v)) must be an edge in G2
# We need to check if the mapped vertices form an edge in G2
for (u, v) in g1_edges:
    # Check if (f[u], f[v]) is an edge in G2
    edge_exists = False
    for (g2_u, g2_v) in g2_edges:
        # Map G2 vertex strings to indices
        g2_u_idx = g2_vertices.index(g2_u)
        g2_v_idx = g2_vertices.index(g2_v)
        # Add constraint: if f[u] == g2_u_idx and f[v] == g2_v_idx, then this edge is preserved
        # We need to ensure that for each G1 edge, there exists some G2 edge that matches
        # Actually, we need to ensure that the specific mapping produces an edge in G2
        # So we need: (f[u] == g2_u_idx AND f[v] == g2_v_idx) OR (f[u] == g2_v_idx AND f[v] == g2_u_idx)
        # But we need this to be true for at least one G2 edge
        # Better approach: For each G1 edge, the pair (f[u], f[v]) must equal some G2 edge pair
        pass

# Let's use a different approach: For each G1 edge, create a constraint that
# the mapped vertices form an edge in G2
for (u, v) in g1_edges:
    # Create disjunction over all G2 edges
    edge_preserved = []
    for (g2_u, g2_v) in g2_edges:
        g2_u_idx = g2_vertices.index(g2_u)
        g2_v_idx = g2_vertices.index(g2_v)
        # The edge can be in either direction
        edge_preserved.append(And(f[u] == g2_u_idx, f[v] == g2_v_idx))
        edge_preserved.append(And(f[u] == g2_v_idx, f[v] == g2_u_idx))
    solver.add(Or(edge_preserved))

# Constraint 3: Reverse preservation - every G2 edge must correspond to some G1 edge
# For each G2 edge, there must exist some G1 edge (u,v) such that f[u] and f[v] map to the G2 vertices
for (g2_u, g2_v) in g2_edges:
    g2_u_idx = g2_vertices.index(g2_u)
    g2_v_idx = g2_vertices.index(g2_v)
    # Create disjunction over all G1 edges
    corresponding_g1_edge = []
    for (u, v) in g1_edges:
        # The G1 edge can map to the G2 edge in either direction
        corresponding_g1_edge.append(And(f[u] == g2_u_idx, f[v] == g2_v_idx))
        corresponding_g1_edge.append(And(f[u] == g2_v_idx, f[v] == g2_u_idx))
    solver.add(Or(corresponding_g1_edge))

# Constraint 4: Degree preservation
# Calculate degrees for G1
g1_degrees = {}
for v in g1_vertices:
    g1_degrees[v] = 0
for (u, v) in g1_edges:
    g1_degrees[u] += 1
    g1_degrees[v] += 1

# Calculate degrees for G2
g2_degrees = {}
for v in g2_vertices:
    g2_degrees[v] = 0
for (u, v) in g2_edges:
    g2_degrees[u] += 1
    g2_degrees[v] += 1

# For each G1 vertex, its degree must equal the degree of its image in G2
for v in g1_vertices:
    # Create constraint: degree of v equals degree of f[v]
    # We need to express this using the mapping f[v]
    degree_constraint = []
    for g2_v_idx, g2_v in enumerate(g2_vertices):
        # If f[v] maps to g2_v_idx, then g1_degrees[v] must equal g2_degrees[g2_v]
        degree_constraint.append(Implies(f[v] == g2_v_idx, g1_degrees[v] == g2_degrees[g2_v]))
    solver.add(Or(degree_constraint))

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract mapping
    mapping = {}
    for i, v in enumerate(g1_vertices):
        g2_idx = model[f[i]].as_long()
        mapping[str(v)] = g2_vertices[g2_idx]
    
    print("is_isomorphic: True")
    print("mapping:", mapping)
    
    # Extract preserved edges
    preserved_edges = []
    for (u, v) in g1_edges:
        g2_u_idx = model[f[u]].as_long()
        g2_v_idx = model[f[v]].as_long()
        g2_u = g2_vertices[g2_u_idx]
        g2_v = g2_vertices[g2_v_idx]
        preserved_edges.append([f"{u},{v}", f"{g2_u},{g2_v}"])
    
    print("preserved_edges:", preserved_edges)
    
elif result == unsat:
    print("STATUS: unsat")
    print("is_isomorphic: False")
    print("mapping: null")
    print("preserved_edges: []")
else:
    print("STATUS: unknown")
    print("is_isomorphic: unknown")
    print("mapping: null")
    print("preserved_edges: []")