from z3 import *

# Map G2 vertices to indices for Z3
# G1: 1,2,3,4,5,6,7,8 -> indices 0,1,2,3,4,5,6,7
# G2: a,b,c,d,e,f,g,h -> indices 0,1,2,3,4,5,6,7

# Vertex index mapping
g1_vertices = [1, 2, 3, 4, 5, 6, 7, 8]
g2_vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
g2_to_idx = {v: i for i, v in enumerate(g2_vertices)}

# Colors: 0 = Red, 1 = Blue
g1_color = {1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0, 7: 1, 8: 1}
g2_color = {'a': 0, 'b': 0, 'c': 1, 'd': 1, 'e': 0, 'f': 0, 'g': 1, 'h': 1}

# Special vertices
g1_special = {1}
g2_special = {'a'}

# Edges with weights (undirected) - store as (min_idx, max_idx, weight)
# G1 edges (using 0-indexed)
g1_edges = {}
g1_edge_list = [
    (1,3,10), (1,4,20), (2,3,20), (2,4,10),
    (5,7,10), (5,8,20), (6,7,20), (6,8,10),
    (1,5,30), (2,6,30), (3,7,40), (4,8,40)
]
for u, v, w in g1_edge_list:
    ui, vi = u - 1, v - 1  # convert to 0-indexed
    g1_edges[(min(ui, vi), max(ui, vi))] = w

# G2 edges (using 0-indexed)
g2_edges = {}
g2_edge_list = [
    ('a','c',10), ('a','d',20), ('b','c',20), ('b','d',10),
    ('e','g',10), ('e','h',20), ('f','g',20), ('f','h',10),
    ('a','e',30), ('b','f',30), ('c','g',40), ('d','h',40)
]
for u, v, w in g2_edge_list:
    ui, vi = g2_to_idx[u], g2_to_idx[v]
    g2_edges[(min(ui, vi), max(ui, vi))] = w

# Z3 solver
solver = Solver()

# Mapping variables: f[i] = which G2 vertex (0-7) G1 vertex i maps to
f = [Int(f'f_{i}') for i in range(8)]

# Constraint 1: Bijection - each f[i] in [0,7] and all distinct
for i in range(8):
    solver.add(f[i] >= 0, f[i] <= 7)
solver.add(Distinct(f))

# Constraint 2: Color preservation
for i in range(8):
    g1_v = g1_vertices[i]
    c1 = g1_color[g1_v]
    # f[i] must map to a G2 vertex with the same color
    solver.add(Or([And(f[i] == j, g2_color[g2_vertices[j]] == c1) for j in range(8)]))

# Constraint 3: Special vertex preservation
for i in range(8):
    g1_v = g1_vertices[i]
    is_special_g1 = g1_v in g1_special
    if is_special_g1:
        # Must map to a special vertex in G2
        solver.add(Or([And(f[i] == j, g2_vertices[j] in g2_special) for j in range(8)]))
    else:
        # Must NOT map to a special vertex in G2
        for j in range(8):
            if g2_vertices[j] in g2_special:
                solver.add(f[i] != j)

# Constraint 4: Edge and weight preservation
# For every pair (i,j) in G1: edge exists iff edge (f[i], f[j]) exists with same weight
for i in range(8):
    for j in range(i+1, 8):
        g1_key = (i, j)
        g1_has_edge = g1_key in g1_edges
        
        # For each possible mapping pair (mi, mj), check if G2 has corresponding edge
        for mi in range(8):
            for mj in range(mi+1, 8):
                g2_key = (mi, mj)
                g2_has_edge = g2_key in g2_edges
                
                if g1_has_edge and g2_has_edge:
                    # Both have edges - weights must match
                    solver.add(Implies(
                        And(f[i] == mi, f[j] == mj),
                        g1_edges[g1_key] == g2_edges[g2_key]
                    ))
                elif g1_has_edge and not g2_has_edge:
                    # G1 has edge but G2 doesn't - this mapping is invalid
                    solver.add(Not(And(f[i] == mi, f[j] == mj)))
                elif not g1_has_edge and g2_has_edge:
                    # G1 doesn't have edge but G2 does - this mapping is invalid
                    solver.add(Not(And(f[i] == mi, f[j] == mj)))
                # If neither has edge, no constraint needed

# Constraint 5: Forbidden subgraph - no 3-cycle with special vertex and total weight 60
# First, identify all triangles in G2 that involve a special vertex (vertex 0 = 'a')
# and have total weight 60
# Then ensure our mapping doesn't create such a triangle

# Find all triangles in G2 involving vertex 0 ('a')
forbidden_triangles = []
for j in range(1, 8):
    for k in range(j+1, 8):
        e1 = (min(0,j), max(0,j))
        e2 = (min(0,k), max(0,k))
        e3 = (min(j,k), max(j,k))
        if e1 in g2_edges and e2 in g2_edges and e3 in g2_edges:
            total_w = g2_edges[e1] + g2_edges[e2] + g2_edges[e3]
            if total_w == 60:
                forbidden_triangles.append((0, j, k))

print(f"Forbidden triangles in G2 (special vertex + weight 60): {forbidden_triangles}")
for t in forbidden_triangles:
    print(f"  Triangle: {g2_vertices[t[0]]}, {g2_vertices[t[1]]}, {g2_vertices[t[2]]}")
    print(f"  Weights: {g2_edges[(min(t[0],t[1]),max(t[0],t[1]))]}, {g2_edges[(min(t[0],t[2]),max(t[0],t[2]))]}, {g2_edges[(min(t[1],t[2]),max(t[1],t[2]))]}")

# For each forbidden triangle, ensure our mapping doesn't create it
# A triangle (0, j, k) in G2 is "created" if there exist G1 vertices u, v, w
# such that f(u)=0, f(v)=j, f(w)=k AND (u,v), (u,w), (v,w) are all edges in G1
for tri in forbidden_triangles:
    a2, b2, c2 = tri  # G2 triangle vertices
    # Find all triples in G1 that could map to this triangle
    for u in range(8):
        for v in range(u+1, 8):
            for w in range(v+1, 8):
                # Check if (u,v), (u,w), (v,w) are all edges in G1
                e_uv = (min(u,v), max(u,v))
                e_uw = (min(u,w), max(u,w))
                e_vw = (min(v,w), max(v,w))
                if e_uv in g1_edges and e_uw in g1_edges and e_vw in g1_edges:
                    # This triple forms a triangle in G1
                    # Forbid mapping to the forbidden G2 triangle
                    # The mapping could be any permutation of (a2, b2, c2)
                    from itertools import permutations
                    for perm in permutations([a2, b2, c2]):
                        solver.add(Not(And(
                            f[u] == perm[0],
                            f[v] == perm[1],
                            f[w] == perm[2]
                        )))

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Graphs are isomorphic!")
    
    # Build mapping
    mapping = {}
    for i in range(8):
        g1_v = str(g1_vertices[i])
        g2_idx = model.evaluate(f[i]).as_long()
        g2_v = g2_vertices[g2_idx]
        mapping[g1_v] = g2_v
    
    print(f"is_isomorphic: True")
    print(f"mapping: {mapping}")
    
    # Show preserved edges
    preserved = []
    for (i, j), w in g1_edges.items():
        mi = model.evaluate(f[i]).as_long()
        mj = model.evaluate(f[j]).as_long()
        g2_key = (min(mi, mj), max(mi, mj))
        if g2_key in g2_edges:
            g1_edge = [str(g1_vertices[i]), str(g1_vertices[j])]
            g2_edge = [g2_vertices[mi], g2_vertices[mj]]
            preserved.append([sorted(g1_edge), sorted(g2_edge)])
    
    print(f"preserved_weighted_edges: {preserved}")
    
    # Verify no forbidden triangle is created
    print("\nVerification - checking for forbidden triangles in mapping:")
    for tri in forbidden_triangles:
        a2, b2, c2 = tri
        # Find which G1 vertices map to these
        mapped = {}
        for i in range(8):
            idx = model.evaluate(f[i]).as_long()
            if idx in [a2, b2, c2]:
                mapped[g2_vertices[idx]] = g1_vertices[i]
        if len(mapped) == 3:
            print(f"  G2 triangle ({g2_vertices[a2]},{g2_vertices[b2]},{g2_vertices[c2]}) maps to G1 vertices: {mapped}")
            # Check if these form a triangle in G1
            verts = list(mapped.values())
            all_edges = True
            for x in range(3):
                for y in range(x+1, 3):
                    key = (min(verts[x]-1, verts[y]-1), max(verts[x]-1, verts[y]-1))
                    if key not in g1_edges:
                        all_edges = False
            print(f"    Forms triangle in G1: {all_edges}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
    print("No valid isomorphism exists under the given constraints.")
else:
    print("STATUS: unknown")