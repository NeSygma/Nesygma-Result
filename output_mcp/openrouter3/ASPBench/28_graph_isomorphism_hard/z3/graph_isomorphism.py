from z3 import *

# Graph G1 data
g1_vertices = [1, 2, 3, 4, 5, 6, 7, 8]
g1_red = [1, 2, 5, 6]
g1_blue = [3, 4, 7, 8]
g1_special = [1]
g1_edges = [
    (1, 3, 10), (1, 4, 20), (2, 3, 20), (2, 4, 10),
    (5, 7, 10), (5, 8, 20), (6, 7, 20), (6, 8, 10),
    (1, 5, 30), (2, 6, 30), (3, 7, 40), (4, 8, 40)
]

# Graph G2 data
g2_vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
g2_red = ['a', 'b', 'e', 'f']
g2_blue = ['c', 'd', 'g', 'h']
g2_special = ['a']
g2_edges = [
    ('a', 'c', 10), ('a', 'd', 20), ('b', 'c', 20), ('b', 'd', 10),
    ('e', 'g', 10), ('e', 'h', 20), ('f', 'g', 20), ('f', 'h', 10),
    ('a', 'e', 30), ('b', 'f', 30), ('c', 'g', 40), ('d', 'h', 40)
]

# Create vertex index mappings for easier constraint building
g1_index = {v: i for i, v in enumerate(g1_vertices)}
g2_index = {v: i for i, v in enumerate(g2_vertices)}

# Create color and special status arrays
g1_color = [1 if v in g1_red else 0 for v in g1_vertices]  # 1=red, 0=blue
g2_color = [1 if v in g2_red else 0 for v in g2_vertices]
g1_special_arr = [1 if v in g1_special else 0 for v in g1_vertices]
g2_special_arr = [1 if v in g2_special else 0 for v in g2_vertices]

# Create edge weight matrices
g1_weight = [[0]*8 for _ in range(8)]
g2_weight = [[0]*8 for _ in range(8)]

for u, v, w in g1_edges:
    i, j = g1_index[u], g1_index[v]
    g1_weight[i][j] = w
    g1_weight[j][i] = w

for u, v, w in g2_edges:
    i, j = g2_index[u], g2_index[v]
    g2_weight[i][j] = w
    g2_weight[j][i] = w

# Create solver
solver = Solver()

# Mapping variables: f[i] = j means G1 vertex i maps to G2 vertex j
f = [Int(f'f_{i}') for i in range(8)]

# Bijection constraints: each G1 vertex maps to exactly one G2 vertex
for i in range(8):
    solver.add(And(f[i] >= 0, f[i] <= 7))

# All different constraint (bijection)
solver.add(Distinct(f))

# Color preservation
for i in range(8):
    # If G1 vertex i is red, then f(i) must be red in G2
    solver.add(Implies(g1_color[i] == 1, g2_color[f[i]] == 1))
    # If G1 vertex i is blue, then f(i) must be blue in G2
    solver.add(Implies(g1_color[i] == 0, g2_color[f[i]] == 0))

# Special vertex preservation
for i in range(8):
    solver.add(Implies(g1_special_arr[i] == 1, g2_special_arr[f[i]] == 1))
    solver.add(Implies(g1_special_arr[i] == 0, g2_special_arr[f[i]] == 0))

# Edge and weight preservation
for i in range(8):
    for j in range(8):
        if i != j:
            # Edge (i,j) exists in G1 with weight w iff edge (f(i),f(j)) exists in G2 with weight w
            # We need to check all possible weights
            for w in [10, 20, 30, 40]:
                # If G1 has edge (i,j) with weight w, then G2 must have edge (f(i),f(j)) with weight w
                solver.add(Implies(g1_weight[i][j] == w, g2_weight[f[i]][f[j]] == w))
                # If G2 has edge (f(i),f(j)) with weight w, then G1 must have edge (i,j) with weight w
                solver.add(Implies(g2_weight[f[i]][f[j]] == w, g1_weight[i][j] == w))

# Forbidden 3-cycle constraint
# A 3-cycle involves 3 distinct vertices x, y, z in G2
# where at least one is special (a), and total weight = 60
# We need to ensure no such cycle exists in the mapped graph

# First, let's find all possible 3-cycles in G2 with total weight 60
# We'll check all combinations of 3 vertices
for i in range(8):
    for j in range(i+1, 8):
        for k in range(j+1, 8):
            # Check if vertices i, j, k form a triangle in G2
            w_ij = g2_weight[i][j]
            w_jk = g2_weight[j][k]
            w_ki = g2_weight[k][i]
            
            # If all three edges exist (non-zero weight)
            if w_ij > 0 and w_jk > 0 and w_ki > 0:
                total_weight = w_ij + w_jk + w_ki
                # If total weight is 60 and involves a special vertex
                if total_weight == 60 and (g2_special_arr[i] == 1 or g2_special_arr[j] == 1 or g2_special_arr[k] == 1):
                    # This is a forbidden pattern in G2
                    # We need to ensure that in the mapping, we don't create this pattern
                    # That means: we cannot have f^{-1}(i), f^{-1}(j), f^{-1}(k) forming a triangle in G1
                    # with the same weights (which would be preserved)
                    
                    # Actually, since we're preserving edges exactly, if G2 has this forbidden triangle,
                    # then G1 must also have the corresponding triangle (with same weights)
                    # So we need to check if G1 has the corresponding triangle
                    
                    # Find which G1 vertices map to i, j, k
                    # We need to ensure that if G2 has this forbidden triangle,
                    # then G1 doesn't have the corresponding triangle (or we reject the mapping)
                    
                    # Actually, the constraint is: the mapping is invalid if it creates a 3-cycle in G2
                    # with special vertex and total weight 60. Since we're preserving edges exactly,
                    # if G2 has such a triangle, then G1 must have the corresponding triangle.
                    # So we need to check if G1 has any triangle with total weight 60 involving special vertex 1.
                    
                    # Let's check all triangles in G1
                    pass

# Let's check all triangles in G1 to see if any are forbidden
g1_forbidden_triangles = []
for i in range(8):
    for j in range(i+1, 8):
        for k in range(j+1, 8):
            w_ij = g1_weight[i][j]
            w_jk = g1_weight[j][k]
            w_ki = g1_weight[k][i]
            if w_ij > 0 and w_jk > 0 and w_ki > 0:
                total_weight = w_ij + w_jk + w_ki
                if total_weight == 60 and (g1_special_arr[i] == 1 or g1_special_arr[j] == 1 or g1_special_arr[k] == 1):
                    g1_forbidden_triangles.append((i, j, k))

# Similarly for G2
g2_forbidden_triangles = []
for i in range(8):
    for j in range(i+1, 8):
        for k in range(j+1, 8):
            w_ij = g2_weight[i][j]
            w_jk = g2_weight[j][k]
            w_ki = g2_weight[k][i]
            if w_ij > 0 and w_jk > 0 and w_ki > 0:
                total_weight = w_ij + w_jk + w_ki
                if total_weight == 60 and (g2_special_arr[i] == 1 or g2_special_arr[j] == 1 or g2_special_arr[k] == 1):
                    g2_forbidden_triangles.append((i, j, k))

print(f"G1 forbidden triangles: {g1_forbidden_triangles}")
print(f"G2 forbidden triangles: {g2_forbidden_triangles}")

# If G2 has forbidden triangles, then any mapping that maps G1 vertices to these G2 vertices
# would create the forbidden pattern. But since we're preserving edges exactly,
# if G2 has a forbidden triangle, then G1 must have the corresponding triangle.
# So we need to ensure that the mapping doesn't map a non-forbidden triangle in G1
# to a forbidden triangle in G2.

# Actually, let's think differently: The constraint says "must not create any 3-cycle involving 
# a special vertex with total edge weight of exactly 60" in G2.
# Since we're preserving edges exactly, if G2 has such a triangle, then G1 must have it too.
# So the mapping is valid only if either:
# 1. G2 has no forbidden triangles, OR
# 2. G1 has the same forbidden triangles (in terms of structure)

# Let's check if G1 and G2 have the same forbidden triangle structure
# If they do, then any isomorphism would preserve this structure
# If they don't, then no isomorphism can exist

# Actually, let's just solve and see what happens
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Isomorphism found:")
    
    # Create mapping dictionary
    mapping = {}
    for i in range(8):
        g1_v = g1_vertices[i]
        g2_v_index = m[f[i]].as_long()
        g2_v = g2_vertices[g2_v_index]
        mapping[g1_v] = g2_v
        print(f"  {g1_v} -> {g2_v}")
    
    # Verify edge preservation
    print("\nEdge preservation verification:")
    preserved_edges = []
    for u, v, w in g1_edges:
        g1_u_idx = g1_index[u]
        g1_v_idx = g1_index[v]
        g2_u = mapping[u]
        g2_v = mapping[v]
        g2_u_idx = g2_index[g2_u]
        g2_v_idx = g2_index[g2_v]
        
        # Check if edge exists in G2 with same weight
        if g2_weight[g2_u_idx][g2_v_idx] == w:
            preserved_edges.append([[u, v], [g2_u, g2_v]])
            print(f"  Edge ({u},{v}) weight {w} -> ({g2_u},{g2_v}) weight {w} ✓")
        else:
            print(f"  Edge ({u},{v}) weight {w} -> ({g2_u},{g2_v}) weight {g2_weight[g2_u_idx][g2_v_idx]} ✗")
    
    # Check for forbidden triangles in the mapped graph
    print("\nChecking for forbidden triangles in mapped graph:")
    has_forbidden = False
    for i in range(8):
        for j in range(i+1, 8):
            for k in range(j+1, 8):
                # Get mapped vertices
                v1 = mapping[g1_vertices[i]]
                v2 = mapping[g1_vertices[j]]
                v3 = mapping[g1_vertices[k]]
                
                v1_idx = g2_index[v1]
                v2_idx = g2_index[v2]
                v3_idx = g2_index[v3]
                
                w12 = g2_weight[v1_idx][v2_idx]
                w23 = g2_weight[v2_idx][v3_idx]
                w31 = g2_weight[v3_idx][v1_idx]
                
                if w12 > 0 and w23 > 0 and w31 > 0:
                    total = w12 + w23 + w31
                    is_special = (g2_special_arr[v1_idx] == 1 or g2_special_arr[v2_idx] == 1 or g2_special_arr[v3_idx] == 1)
                    if total == 60 and is_special:
                        print(f"  FORBIDDEN: Triangle ({v1},{v2},{v3}) with total weight {total}")
                        has_forbidden = True
    
    if not has_forbidden:
        print("  No forbidden triangles found ✓")
    
    # Output for downstream processing
    print(f"\nField 'is_isomorphic': True")
    print(f"Field 'mapping': {mapping}")
    print(f"Field 'preserved_weighted_edges': {preserved_edges}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid isomorphism exists")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")