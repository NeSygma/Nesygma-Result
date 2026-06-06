from z3 import *

# Solver configuration
BENCHMARK_MODE = True

# Vertex indices for G1 (1-8) and G2 (a-h)
# Mapping from G1 vertex index (0-7) to G2 vertex index (0-7)
mapping_vars = [Int(f'map_{i}') for i in range(8)]

solver = Solver()

# Domain constraints
for mv in mapping_vars:
    solver.add(mv >= 0, mv <= 7)

# Bijection
solver.add(Distinct(mapping_vars))

# Special vertex preservation: G1 vertex 1 (index 0) maps to G2 vertex a (index 0)
solver.add(mapping_vars[0] == 0)
# No other G1 vertex maps to a
for i in range(1,8):
    solver.add(mapping_vars[i] != 0)

# Color sets
red_G1 = {0,1,4,5}   # vertices 1,2,5,6
blue_G1 = {2,3,6,7}  # vertices 3,4,7,8
red_G2 = {0,1,4,5}   # a,b,e,f
blue_G2 = {2,3,6,7}  # c,d,g,h

for i in range(8):
    if i in red_G1:
        solver.add(Or([mapping_vars[i] == idx for idx in red_G2]))
    else:
        solver.add(Or([mapping_vars[i] == idx for idx in blue_G2]))

# Weight matrix for G1 (IntVal constants)
weight_G1 = [[IntVal(0) for _ in range(8)] for _ in range(8)]
# Helper to set symmetric edges
edges_G1 = [
    (0,2,10), (0,3,20), (1,2,20), (1,3,10),
    (4,6,10), (4,7,20), (5,6,20), (5,7,10),
    (0,4,30), (1,5,30), (2,6,40), (3,7,40)
]
for u,v,w in edges_G1:
    weight_G1[u][v] = IntVal(w)
    weight_G1[v][u] = IntVal(w)

# Weight matrix for G2 as a function
weight_G2_func = Function('weight_G2', IntSort(), IntSort(), IntSort())
# Define all pairs
edges_G2 = [
    (0,2,10), (0,3,20), (1,2,20), (1,3,10),
    (4,6,10), (4,7,20), (5,6,20), (5,7,10),
    (0,4,30), (1,5,30), (2,6,40), (3,7,40)
]
for i in range(8):
    for j in range(8):
        # default 0
        weight_G2_func(i,j) == 0

for u,v,w in edges_G2:
    solver.add(weight_G2_func(u,v) == w)
    solver.add(weight_G2_func(v,u) == w)
# Ensure symmetry for all pairs (already set by above, but add explicit)
for i in range(8):
    for j in range(8):
        solver.add(weight_G2_func(i,j) == weight_G2_func(j,i))

# Edge and weight preservation
for i in range(8):
    for j in range(i+1,8):
        solver.add(weight_G1[i][j] == weight_G2_func(mapping_vars[i], mapping_vars[j]))

# Forbidden subgraph: no triangle involving special vertex a with total weight 60
for i in range(8):
    for j in range(i+1,8):
        # Ensure not all three edges exist and sum to 60
        solver.add(Or(
            weight_G2_func(0, mapping_vars[i]) == 0,
            weight_G2_func(0, mapping_vars[j]) == 0,
            weight_G2_func(mapping_vars[i], mapping_vars[j]) == 0,
            weight_G2_func(0, mapping_vars[i]) + weight_G2_func(0, mapping_vars[j]) + weight_G2_func(mapping_vars[i], mapping_vars[j]) != 60
        ))

# Check satisfiability
result = solver.check()

if result == sat:
    m = solver.model()
    # Mapping from G1 vertex names to G2 vertex names
    names_G2 = ['a','b','c','d','e','f','g','h']
    mapping_dict = {}
    for i in range(8):
        mapped_idx = m.evaluate(mapping_vars[i], model_completion=True).as_long()
        mapping_dict[str(i+1)] = names_G2[mapped_idx]
    # Preserve weighted edges
    preserved_edges = []
    for u,v,w in edges_G1:
        mapped_u = names_G2[m.evaluate(mapping_vars[u], model_completion=True).as_long()]
        mapped_v = names_G2[m.evaluate(mapping_vars[v], model_completion=True).as_long()]
        # sort pairs
        g1_pair = sorted([u+1, v+1])
        g2_pair = sorted([mapped_u, mapped_v])
        preserved_edges.append([g1_pair, g2_pair])
    print("STATUS: sat")
    print("mapping:", mapping_dict)
    print("preserved_weighted_edges:", preserved_edges)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")