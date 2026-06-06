from z3 import *

# Define data
vertices = list(range(16))
edges = [
    # Cluster 1
    (0,1,10),(0,2,10),(0,3,10),(1,2,10),(1,3,10),(2,3,10),
    # Cluster 2
    (4,5,10),(4,6,10),(4,7,10),(5,6,10),(5,7,10),(6,7,10),
    # Cluster 3
    (8,9,10),(8,10,10),(8,11,10),(9,10,10),(9,11,10),(10,11,10),
    # Cluster 4
    (12,13,10),(12,14,10),(12,15,10),(13,14,10),(13,15,10),(14,15,10),
    # Inter-cluster
    (3,4,1),(7,8,2),(11,12,3),(15,0,1),(1,6,2),(5,10,3),(9,14,1)
]

# Create optimizer
opt = Optimize()

# Partition variable for each vertex: 0..3
p = [Int(f'p_{i}') for i in vertices]
for var in p:
    opt.add(var >= 0, var < 4)

# Balanced partitions: exactly 4 vertices per partition
for k in range(4):
    opt.add(Sum([If(var == k, 1, 0) for var in p]) == 4)

# Cut weight expression
cut_expr = Sum([If(p[u] != p[v], w, 0) for (u,v,w) in edges])
opt.minimize(cut_expr)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    cut_weight = m.eval(cut_expr, model_completion=True).as_long()
    # Build partitions
    partitions = {k: [] for k in range(4)}
    for i in vertices:
        part = m.eval(p[i]).as_long()
        partitions[part].append(i)
    print("STATUS: sat")
    print(f"cut_weight = {cut_weight}")
    for k in range(4):
        print(f"partition_{k+1} = {partitions[k]}")
else:
    print("STATUS: unsat" if result == unsat else "STATUS: unknown")