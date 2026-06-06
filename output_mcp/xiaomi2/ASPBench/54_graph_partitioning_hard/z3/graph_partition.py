from z3 import *

# Create optimizer
opt = Optimize()

# Decision variables: partition assignment for each vertex (0-3)
n_vertices = 16
n_partitions = 4
partition_size = 4

part = [Int(f'part_{v}') for v in range(n_vertices)]

# Each vertex assigned to exactly one partition (0..3)
for v in range(n_vertices):
    opt.add(part[v] >= 0, part[v] < n_partitions)

# Each partition has exactly 4 vertices
for p in range(n_partitions):
    opt.add(Sum([If(part[v] == p, 1, 0) for v in range(n_vertices)]) == partition_size)

# Define all edges with weights
# Intra-cluster edges (weight 10)
intra_edges = []
# Cluster 1: 0-3
for i in range(4):
    for j in range(i+1, 4):
        intra_edges.append((i, j, 10))
# Cluster 2: 4-7
for i in range(4, 8):
    for j in range(i+1, 8):
        intra_edges.append((i, j, 10))
# Cluster 3: 8-11
for i in range(8, 12):
    for j in range(i+1, 12):
        intra_edges.append((i, j, 10))
# Cluster 4: 12-15
for i in range(12, 16):
    for j in range(i+1, 16):
        intra_edges.append((i, j, 10))

# Inter-cluster edges
inter_edges = [
    (3, 4, 1), (7, 8, 2), (11, 12, 3), (15, 0, 1),
    (1, 6, 2), (5, 10, 3), (9, 14, 1)
]

all_edges = intra_edges + inter_edges

# For each edge, define whether it crosses partition boundaries
# An edge (u,v,w) crosses if part[u] != part[v]
# Cut weight contribution: w if part[u] != part[v], else 0
cut_weight = Sum([
    If(part[u] != part[v], w, 0) for (u, v, w) in all_edges
])

# Minimize cut weight
opt.minimize(cut_weight)

# Check
result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract partition assignments
    assignments = {}
    for v in range(n_vertices):
        p = m[part[v]].as_long()
        assignments.setdefault(p, []).append(v)
    
    print(f"cut_weight = {m.eval(cut_weight)}")
    print()
    for p in range(n_partitions):
        print(f"partition_{p+1} = {sorted(assignments[p])}")
    
    print()
    print(f"balance = {[len(assignments[p]) for p in range(n_partitions)]}")
    
    # Identify cut edges
    print()
    print("cut_edges = [")
    for (u, v, w) in all_edges:
        pu = m[part[u]].as_long()
        pv = m[part[v]].as_long()
        if pu != pv:
            print(f"  ({u}, {v}, weight={w}), partitions=({pu},{pv})")
    print("]")
    
    # Count cut edges
    cut_count = sum(1 for (u,v,w) in all_edges if m[part[u]].as_long() != m[part[v]].as_long())
    print(f"\nTotal cut edges: {cut_count}")
    print(f"Total intra-cluster edges: {len(intra_edges)}")
    print(f"Total inter-cluster edges: {len(inter_edges)}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid partition found")
else:
    print("STATUS: unknown")