from z3 import *

# Vertices 0-15
vertices = list(range(16))

# Build edges list
edges = []
# Cluster edges: all pairs within each cluster of 4 vertices, weight 10
for start in [0,4,8,12]:
    for i in range(start, start+4):
        for j in range(i+1, start+4):
            edges.append((i,j,10))
# Inter-cluster edges
inter_edges = [
    (3,4,1), (7,8,2), (11,12,3), (15,0,1),
    (1,6,2), (5,10,3), (9,14,1)
]
edges.extend(inter_edges)

# Partition variables: each vertex assigned to partition 0-3
partition = [Int(f'p_{v}') for v in vertices]

solver = Optimize()
# Domain constraints
for v in vertices:
    solver.add(partition[v] >= 0, partition[v] <= 3)

# Balanced partitions: each partition has exactly 4 vertices
for p in range(4):
    solver.add(Sum([If(partition[v] == p, 1, 0) for v in vertices]) == 4)

# Cut weight variable
cut_weight = Int('cut_weight')
# Compute cut weight expression
cut_expr = Sum([If(partition[u] != partition[v], w, 0) for (u,v,w) in edges])
solver.add(cut_weight == cut_expr)

# Objective: minimize cut weight
solver.minimize(cut_weight)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    # Build partition lists
    part_lists = [[] for _ in range(4)]
    for v in vertices:
        pv = m[partition[v]].as_long()
        part_lists[pv].append(v)
    # Compute cut edges according to model
    cut_edges = []
    for (u,v,w) in edges:
        if m[partition[u]].as_long() != m[partition[v]].as_long():
            cut_edges.append((u,v,w))
    # Compute balance
    balance = [len(pl) for pl in part_lists]
    # Output
    print("STATUS: sat")
    for i, pl in enumerate(part_lists):
        print(f"partition_{i+1} = {pl}")
    print(f"cut_weight = {m[cut_weight].as_long()}")
    print(f"cut_edges = {cut_edges}")
    print(f"balance = {balance}")
else:
    print("STATUS: unsat")