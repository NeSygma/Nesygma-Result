from z3 import *

# BENCHMARK_MODE: ON (since the problem is guaranteed solvable)
BENCHMARK_MODE = True

# --- Graph G1 ---
# Vertices: 1, 2, 3, 4, 5, 6, 7, 8
G1_vertices = [1, 2, 3, 4, 5, 6, 7, 8]

# Colors: 0=Red, 1=Blue
G1_color = {
    1: 0, 2: 0, 3: 1, 4: 1,
    5: 0, 6: 0, 7: 1, 8: 1
}

# Special vertices
G1_special = {1}

# Edges: (u, v, weight)
G1_edges = [
    (1, 3, 10), (1, 4, 20), (2, 3, 20), (2, 4, 10),
    (5, 7, 10), (5, 8, 20), (6, 7, 20), (6, 8, 10),
    (1, 5, 30), (2, 6, 30), (3, 7, 40), (4, 8, 40)
]

# --- Graph G2 ---
# Vertices: 1, 2, 3, 4, 5, 6, 7, 8 (mapped from 'a','b','c','d','e','f','g','h')
G2_vertices = [1, 2, 3, 4, 5, 6, 7, 8]

# Colors: 0=Red, 1=Blue
G2_color = {
    1: 0, 2: 0, 3: 1, 4: 1,
    5: 0, 6: 0, 7: 1, 8: 1
}

# Special vertices
G2_special = {1}

# Edges: (u, v, weight)
G2_edges = [
    (1, 3, 10), (1, 4, 20), (2, 3, 20), (2, 4, 10),
    (5, 7, 10), (5, 8, 20), (6, 7, 20), (6, 8, 10),
    (1, 5, 30), (2, 6, 30), (3, 7, 40), (4, 8, 40)
]

# --- Mapping ---
f = Function('f', IntSort(), IntSort())

# --- Solver ---
solver = Solver()

# 1. Bijection constraints
# Injective: f(x) != f(y) for x != y
for i in range(len(G1_vertices)):
    for j in range(i+1, len(G1_vertices)):
        solver.add(f(G1_vertices[i]) != f(G1_vertices[j]))

# Surjective: for all v in G2_vertices, there exists u in G1_vertices such that f(u) = v
for v in G2_vertices:
    solver.add(Or([f(u) == v for u in G1_vertices]))

# 2. Color preservation
for u in G1_vertices:
    solver.add(G1_color[u] == G2_color[f(u)])

# 3. Special vertex preservation
for u in G1_vertices:
    is_special_G1 = u in G1_special
    is_special_G2 = f(u) in G2_special
    solver.add(is_special_G1 == is_special_G2)

# 4. Edge and weight preservation
# For each edge (u,v,w) in G1, there must be an edge (f(u),f(v),w) in G2
for (u, v, w) in G1_edges:
    solver.add(Or(
        And(f(u) == G2_edges[i][0], f(v) == G2_edges[i][1], G2_edges[i][2] == w)
        for i in range(len(G2_edges))
    ))
    solver.add(Or(
        And(f(u) == G2_edges[i][1], f(v) == G2_edges[i][0], G2_edges[i][2] == w)
        for i in range(len(G2_edges))
    ))

# For each edge (u,v,w) in G2, there must be an edge (x,y,w) in G1 such that f(x)=u and f(y)=v
for (u, v, w) in G2_edges:
    for x in G1_vertices:
        for y in G1_vertices:
            solver.add(Implies(
                And(f(x) == u, f(y) == v),
                Or(
                    And(x == G1_edges[i][0], y == G1_edges[i][1], G1_edges[i][2] == w)
                    for i in range(len(G1_edges))
                )
            ))
            solver.add(Implies(
                And(f(x) == u, f(y) == v),
                Or(
                    And(x == G1_edges[i][1], y == G1_edges[i][0], G1_edges[i][2] == w)
                    for i in range(len(G1_edges))
                )
            ))

# 5. Forbidden subgraph: no 3-cycle in G2 involving special vertex (1) with total weight 60
# Enumerate all possible 3-cycles in G2 involving vertex 1
# A 3-cycle is a set of edges (1,a,w1), (a,b,w2), (b,1,w3) where a,b are distinct vertices
# Total weight: w1 + w2 + w3 == 60
# We need to ensure that for the mapping f, no such 3-cycle exists in G2

# Collect all edges in G2 incident to vertex 1
edges_from_1 = [(v, w) for (u, v, w) in G2_edges if u == 1]
edges_to_1 = [(u, w) for (u, v, w) in G2_edges if v == 1]

# For each edge (1,a,w1) and (b,1,w3), check if there is an edge (a,b,w2) such that w1+w2+w3 == 60
for (a, w1) in edges_from_1:
    for (b, w3) in edges_to_1:
        if a != b:
            # Check if there is an edge (a,b,w2) or (b,a,w2) in G2
            for (u, v, w2) in G2_edges:
                if (u == a and v == b) or (u == b and v == a):
                    solver.add(Not(And(
                        f(1) == 1,  # Special vertex in G1 maps to special vertex in G2 (1)
                        w1 + w2 + w3 == 60
                    )))

# --- Check ---
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract the mapping
    mapping = {}
    for u in G1_vertices:
        mapping[str(u)] = str(model.eval(f(u)))
    print("mapping:", mapping)
    # Extract preserved weighted edges
    preserved_edges = []
    for (u, v, w) in G1_edges:
        f_u = model.eval(f(u))
        f_v = model.eval(f(v))
        # Find the corresponding edge in G2
        for (x, y, w2) in G2_edges:
            if (x == f_u and y == f_v and w2 == w) or (x == f_v and y == f_u and w2 == w):
                preserved_edges.append(((u, v, w), (f_u, f_v, w2)))
                break
    print("preserved_weighted_edges:", preserved_edges)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")