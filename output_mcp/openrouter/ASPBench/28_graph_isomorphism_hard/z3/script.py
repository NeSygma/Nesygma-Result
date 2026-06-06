from z3 import *

# Define data
G1_vertices = [1,2,3,4,5,6,7,8]
G2_vertices = ['a','b','c','d','e','f','g','h']
# Index mapping: 0..7
n = 8
# Colors: 0 red, 1 blue
color1 = [0,0,1,1,0,0,1,1]
color2 = [0,0,1,1,0,0,1,1]
# Special vertices
special1 = [True, False, False, False, False, False, False, False]
special2 = [True, False, False, False, False, False, False, False]
# Edge weight matrices (undirected, symmetric, 0 if no edge)
weight1 = [[0]*n for _ in range(n)]
edges1 = [ (1,3,10), (1,4,20), (2,3,20), (2,4,10),
           (5,7,10), (5,8,20), (6,7,20), (6,8,10),
           (1,5,30), (2,6,30), (3,7,40), (4,8,40) ]
# map vertex numbers to indices (1->0,2->1,...)
idx1 = {v:i for i,v in enumerate(G1_vertices)}
for u,v,w in edges1:
    i,j = idx1[u], idx1[v]
    weight1[i][j] = w
    weight1[j][i] = w

weight2 = [[0]*n for _ in range(n)]
edges2 = [ ('a','c',10), ('a','d',20), ('b','c',20), ('b','d',10),
           ('e','g',10), ('e','h',20), ('f','g',20), ('f','h',10),
           ('a','e',30), ('b','f',30), ('c','g',40), ('d','h',40) ]
idx2 = {v:i for i,v in enumerate(G2_vertices)}
for u,v,w in edges2:
    i,j = idx2[u], idx2[v]
    weight2[i][j] = w
    weight2[j][i] = w

# Z3 variables: mapping from G1 index to G2 index
map_vars = [Int(f"m_{i}") for i in range(n)]
solver = Solver()
# Bijection constraints
for mv in map_vars:
    solver.add(mv >= 0, mv < n)
solver.add(Distinct(map_vars))
# Color preservation
for i in range(n):
    solver.add(color1[i] == Select(Array('color2_arr', IntSort(), IntSort()), map_vars[i]))
# Instead of array, we can directly encode using Or of equalities
# Simpler: add equality via piecewise
color2_arr = Array('color2_arr', IntSort(), IntSort())
# Initialize array with known values
for i,val in enumerate(color2):
    color2_arr = Store(color2_arr, i, val)
# Add constraints using this array
solver.add([color1[i] == Select(color2_arr, map_vars[i]) for i in range(n)])
# Special preservation
special2_arr = Array('special2_arr', IntSort(), BoolSort())
for i,val in enumerate(special2):
    special2_arr = Store(special2_arr, i, val)
for i in range(n):
    solver.add(special1[i] == Select(special2_arr, map_vars[i]))
# Edge weight preservation
# For each unordered pair i<j
for i in range(n):
    for j in range(i+1, n):
        w1 = weight1[i][j]
        # weight in G2 after mapping
        w2_ij = Select(Array('w2_arr', IntSort(), IntSort()), map_vars[i]*n + map_vars[j])
        # We'll instead create a 2D array for weights
# Build 2D array for weight2
w2_arr = Array('w2_arr', IntSort(), IntSort())
for i in range(n):
    for j in range(n):
        w2_arr = Store(w2_arr, i*n + j, weight2[i][j])
# Now add constraints
for i in range(n):
    for j in range(i+1, n):
        w1 = weight1[i][j]
        w2 = Select(w2_arr, map_vars[i]*n + map_vars[j])
        solver.add(w1 == w2)
# Forbidden triangle involving a special vertex with total weight 60
for i in range(n):
    for j in range(i+1, n):
        for k in range(j+1, n):
            # if any of i,j,k is special in G1
            special_cond = Or(special1[i], special1[j], special1[k])
            # edges existence in G2 after mapping (weight > 0)
            w_ij = Select(w2_arr, map_vars[i]*n + map_vars[j])
            w_jk = Select(w2_arr, map_vars[j]*n + map_vars[k])
            w_ki = Select(w2_arr, map_vars[k]*n + map_vars[i])
            edge_exists = And(w_ij > 0, w_jk > 0, w_ki > 0)
            total60 = w_ij + w_jk + w_ki == 60
            # forbid this configuration
            solver.add(Implies(And(special_cond, edge_exists, total60), False))

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    mapping = {str(G1_vertices[i]): G2_vertices[m.eval(map_vars[i]).as_long()] for i in range(n)}
    print("STATUS: sat")
    print("mapping =", mapping)
else:
    print("STATUS: unsat")