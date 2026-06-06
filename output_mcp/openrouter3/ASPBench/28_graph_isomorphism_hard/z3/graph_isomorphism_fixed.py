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

# Create vertex index mappings
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

# Color preservation - using Or-Loop pattern to avoid indexing with Z3 variables
for i in range(8):
    # For each G1 vertex i, we need to ensure that if it's red, then f(i) is red
    # We'll use Or-Loop to check all possible mappings
    red_constraint = Or([And(f[i] == j, g2_color[j] == 1) for j in range(8)])
    blue_constraint = Or([And(f[i] == j, g2_color[j] == 0) for j in range(8)])
    
    if g1_color[i] == 1:  # G1 vertex i is red
        solver.add(red_constraint)
    else:  # G1 vertex i is blue
        solver.add(blue_constraint)

# Special vertex preservation
for i in range(8):
    special_constraint = Or([And(f[i] == j, g2_special_arr[j] == 1) for j in range(8)])
    not_special_constraint = Or([And(f[i] == j, g2_special_arr[j] == 0) for j in range(8)])
    
    if g1_special_arr[i] == 1:  # G1 vertex i is special
        solver.add(special_constraint)
    else:  # G1 vertex i is not special
        solver.add(not_special_constraint)

# Edge and weight preservation
# For each edge in G1, we need to ensure the mapped edge in G2 has the same weight
for i in range(8):
    for j in range(8):
        if i != j:
            # Get the weight of edge (i,j) in G1
            w1 = g1_weight[i][j]
            if w1 > 0:  # Only if edge exists in G1
                # The mapped edge (f(i), f(j)) in G2 must have the same weight
                # We need to ensure: if f(i)=a and f(j)=b, then g2_weight[a][b] == w1
                for a in range(8):
                    for b in range(8):
                        if a != b:
                            solver.add(Implies(And(f[i] == a, f[j] == b), g2_weight[a][b] == w1))

# Also ensure that if an edge exists in G2, it must exist in G1 with same weight
for a in range(8):
    for b in range(8):
        if a != b:
            w2 = g2_weight[a][b]
            if w2 > 0:  # Only if edge exists in G2
                # Find which G1 vertices map to a and b
                for i in range(8):
                    for j in range(8):
                        if i != j:
                            solver.add(Implies(And(f[i] == a, f[j] == b), g1_weight[i][j] == w2))

# Forbidden 3-cycle constraint
# We need to ensure that in the mapped graph, there's no triangle with total weight 60 involving special vertex
# Let's check all possible triangles in the mapped graph

# First, let's find all triangles in G2 with total weight 60 involving special vertex
forbidden_g2_triangles = []
for i in range(8):
    for j in range(i+1, 8):
        for k in range(j+1, 8):
            w_ij = g2_weight[i][j]
            w_jk = g2_weight[j][k]
            w_ki = g2_weight[k][i]
            if w_ij > 0 and w_jk > 0 and w_ki > 0:
                total = w_ij + w_jk + w_ki
                if total == 60 and (g2_special_arr[i] == 1 or g2_special_arr[j] == 1 or g2_special_arr[k] == 1):
                    forbidden_g2_triangles.append((i, j, k))

print(f"Found {len(forbidden_g2_triangles)} forbidden triangles in G2")

# For each forbidden triangle in G2, we need to ensure that the mapping doesn't create it
# That is, we cannot have three G1 vertices mapping to these three G2 vertices
# while preserving the edge structure
for (i, j, k) in forbidden_g2_triangles:
    # Check if G1 has the corresponding triangle
    # We need to find all triples of G1 vertices that could map to (i,j,k)
    for a in range(8):
        for b in range(a+1, 8):
            for c in range(b+1, 8):
                # Check if G1 has triangle (a,b,c) with same weights
                w_ab = g1_weight[a][b]
                w_bc = g1_weight[b][c]
                w_ca = g1_weight[c][a]
                if w_ab > 0 and w_bc > 0 and w_ca > 0:
                    # Check if weights match the forbidden triangle in G2
                    w_ij = g2_weight[i][j]
                    w_jk = g2_weight[j][k]
                    w_ki = g2_weight[k][i]
                    if w_ab == w_ij and w_bc == w_jk and w_ca == w_ki:
                        # This G1 triangle could map to the forbidden G2 triangle
                        # We need to prevent this mapping
                        # Constraint: NOT (f[a]==i AND f[b]==j AND f[c]==k) OR permutations
                        # Actually, we need to consider all permutations of mapping
                        permutations = [
                            (a, b, c, i, j, k),
                            (a, b, c, i, k, j),
                            (a, b, c, j, i, k),
                            (a, b, c, j, k, i),
                            (a, b, c, k, i, j),
                            (a, b, c, k, j, i)
                        ]
                        forbidden_mappings = []
                        for (va, vb, vc, ta, tb, tc) in permutations:
                            forbidden_mappings.append(And(f[va] == ta, f[vb] == tb, f[vc] == tc))
                        solver.add(Or([Not(fm) for fm in forbidden_mappings]))

# Check for solution
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