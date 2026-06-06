from z3 import *

# Create optimizer
opt = Optimize()

# Vertices
n_vertices = 16
n_partitions = 4
partition_size = 4

# Decision variables: partition[v] = which partition (0-3) vertex v belongs to
partition = [Int(f'partition_{v}') for v in range(n_vertices)]

# Constraint: each vertex assigned to exactly one partition (0-3)
for v in range(n_vertices):
    opt.add(And(partition[v] >= 0, partition[v] < n_partitions))

# Constraint: each partition has exactly 4 vertices
for p in range(n_partitions):
    opt.add(Sum([If(partition[v] == p, 1, 0) for v in range(n_vertices)]) == partition_size)

# Define edges with weights
# Intra-cluster edges (weight 10)
intra_edges = []
# Cluster 1 (0-3)
for i in range(4):
    for j in range(i+1, 4):
        intra_edges.append((i, j, 10))
# Cluster 2 (4-7)
for i in range(4, 8):
    for j in range(i+1, 8):
        intra_edges.append((i, j, 10))
# Cluster 3 (8-11)
for i in range(8, 12):
    for j in range(i+1, 12):
        intra_edges.append((i, j, 10))
# Cluster 4 (12-15)
for i in range(12, 16):
    for j in range(i+1, 16):
        intra_edges.append((i, j, 10))

# Inter-cluster edges
inter_edges = [
    (3, 4, 1), (7, 8, 2), (11, 12, 3), (15, 0, 1),
    (1, 6, 2), (5, 10, 3), (9, 14, 1)
]

all_edges = intra_edges + inter_edges

# Objective: minimize total cut weight
# An edge (u, v, w) crosses if partition[u] != partition[v]
cut_weight = Sum([If(partition[u] != partition[v], w, 0) for (u, v, w) in all_edges])
opt.minimize(cut_weight)

# Check and extract solution
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract partition assignments
    assignments = {}
    for v in range(n_vertices):
        p = model[partition[v]].as_long()
        if p not in assignments:
            assignments[p] = []
        assignments[p].append(v)
    
    # Calculate actual cut weight and cut edges
    actual_cut_weight = 0
    cut_edges = []
    for (u, v, w) in all_edges:
        pu = model[partition[u]].as_long()
        pv = model[partition[v]].as_long()
        if pu != pv:
            actual_cut_weight += w
            cut_edges.append((u, v, w))
    
    print("STATUS: sat")
    print(f"\nOptimal cut weight: {actual_cut_weight}")
    print(f"\nPartition assignments:")
    for p in sorted(assignments.keys()):
        print(f"  Partition {p+1}: {sorted(assignments[p])}")
    
    print(f"\nCut edges (u, v, weight):")
    for (u, v, w) in cut_edges:
        print(f"  ({u}, {v}, {w})")
    
    print(f"\nBalance check:")
    for p in sorted(assignments.keys()):
        print(f"  Partition {p+1} size: {len(assignments[p])}")
    
    # Verify expected answer
    if actual_cut_weight == 13:
        print(f"\nExpected minimum cut weight (13) achieved!")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")