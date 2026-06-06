from z3 import *

# Problem data
vertices = list(range(16))
partitions = [1, 2, 3, 4]

# Edge list with weights
edges = [
    # Cluster 1 (0-3)
    (0, 1, 10), (0, 2, 10), (0, 3, 10),
    (1, 2, 10), (1, 3, 10),
    (2, 3, 10),
    # Cluster 2 (4-7)
    (4, 5, 10), (4, 6, 10), (4, 7, 10),
    (5, 6, 10), (5, 7, 10),
    (6, 7, 10),
    # Cluster 3 (8-11)
    (8, 9, 10), (8, 10, 10), (8, 11, 10),
    (9, 10, 10), (9, 11, 10),
    (10, 11, 10),
    # Cluster 4 (12-15)
    (12, 13, 10), (12, 14, 10), (12, 15, 10),
    (13, 14, 10), (13, 15, 10),
    (14, 15, 10),
    # Inter-cluster edges
    (3, 4, 1), (7, 8, 2), (11, 12, 3), (15, 0, 1),
    (1, 6, 2), (5, 10, 3), (9, 14, 1)
]

# Create solver
solver = Solver()

# Variables: partition assignment for each vertex
vertex_partition = [Int(f'v_{i}_part') for i in vertices]

# Each vertex assigned to a partition 1-4
for v in vertices:
    solver.add(vertex_partition[v] >= 1)
    solver.add(vertex_partition[v] <= 4)

# Each partition must have exactly 4 vertices
for p in partitions:
    solver.add(Sum([If(vertex_partition[v] == p, 1, 0) for v in vertices]) == 4)

# Cut weight calculation
# For each edge, if endpoints are in different partitions, add weight to cut
cut_weight = Int('cut_weight')
edge_crossing = []
for (u, v, w) in edges:
    # Create a boolean variable indicating if this edge crosses partitions
    is_crossing = Bool(f'cross_{u}_{v}')
    solver.add(is_crossing == (vertex_partition[u] != vertex_partition[v]))
    edge_crossing.append((is_crossing, w))

# Sum of weights of crossing edges
solver.add(cut_weight == Sum([If(is_crossing, w, 0) for (is_crossing, w) in edge_crossing]))

# Objective: minimize cut weight
opt = Optimize()
opt.add([solver.assertions()[i] for i in range(len(solver.assertions()))])
opt.minimize(cut_weight)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"Minimum cut weight: {model[cut_weight]}")
    print("\nPartition assignments:")
    for p in partitions:
        partition_vertices = [v for v in vertices if model.evaluate(vertex_partition[v] == p)]
        print(f"Partition {p}: {partition_vertices}")
    
    # Verify expected minimum
    if model[cut_weight] == 13:
        print("\n✓ Achieved expected minimum cut weight of 13")
    else:
        print(f"\n⚠ Cut weight {model[cut_weight]} differs from expected 13")
    
    # List crossing edges
    print("\nCrossing edges:")
    for (u, v, w) in edges:
        if model.evaluate(vertex_partition[u] != vertex_partition[v]):
            print(f"  ({u}, {v}, weight={w})")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")