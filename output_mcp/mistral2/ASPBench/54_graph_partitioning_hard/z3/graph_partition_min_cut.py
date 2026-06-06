from z3 import *

# BENCHMARK_MODE: ON (since the problem is guaranteed solvable)
BENCHMARK_MODE = True

# Create the solver
opt = Optimize()

# Declare the partition assignment variables for each vertex
# partition[i] = p means vertex i is assigned to partition p (0, 1, 2, or 3)
partition = [Int(f'partition_{i}') for i in range(16)]

# Each partition must be assigned exactly 4 vertices
for p in range(4):
    opt.add(Sum([If(partition[i] == p, 1, 0) for i in range(16)]) == 4)

# Each vertex must be assigned to exactly one partition
for i in range(16):
    opt.add(partition[i] >= 0, partition[i] < 4)

# Define the edges and their weights
edges = [
    (0, 1, 10), (0, 2, 10), (0, 3, 10),
    (1, 2, 10), (1, 3, 10),
    (2, 3, 10),
    (4, 5, 10), (4, 6, 10), (4, 7, 10),
    (5, 6, 10), (5, 7, 10),
    (6, 7, 10),
    (8, 9, 10), (8, 10, 10), (8, 11, 10),
    (9, 10, 10), (9, 11, 10),
    (10, 11, 10),
    (12, 13, 10), (12, 14, 10), (12, 15, 10),
    (13, 14, 10), (13, 15, 10),
    (14, 15, 10),
    (3, 4, 1), (7, 8, 2), (11, 12, 3), (15, 0, 1),
    (1, 6, 2), (5, 10, 3), (9, 14, 1)
]

# Calculate the cut weight: sum of weights of edges crossing partitions
cut_weight = Int('cut_weight')
opt.add(cut_weight == Sum(
    [If(partition[u] != partition[v], weight, 0) for (u, v, weight) in edges]
))

# Minimize the cut weight
opt.minimize(cut_weight)

# Check for a solution
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    # Extract the partition assignments
    partition_assignments = [model[partition[i]] for i in range(16)]
    # Extract the cut weight
    cut_weight_value = model[cut_weight]
    # Extract the cut edges
    cut_edges = []
    for (u, v, weight) in edges:
        pu = model.eval(partition[u], model_completion=True)
        pv = model.eval(partition[v], model_completion=True)
        if pu.as_long() != pv.as_long():
            cut_edges.append((u, v, weight))
    # Print the results
    print("partition_1 =", [i for i in range(16) if model[partition[i]] == 0])
    print("partition_2 =", [i for i in range(16) if model[partition[i]] == 1])
    print("partition_3 =", [i for i in range(16) if model[partition[i]] == 2])
    print("partition_4 =", [i for i in range(16) if model[partition[i]] == 3])
    print("cut_weight =", cut_weight_value)
    print("cut_edges =", cut_edges)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")