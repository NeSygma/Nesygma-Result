from z3 import *

# Initialize solver
solver = Solver()

# Declare color variables for vertices 1 to 36 (1-based indexing)
color = [Int(f"color_{i}") for i in range(1, 37)]

# Weights for vertices 1 to 36 (1-based indexing)
weight = [0]  # dummy for 1-based indexing
for i in range(1, 6):
    weight.append(10)
for i in range(6, 16):
    weight.append(3)
for i in range(16, 26):
    weight.append(5)
for i in range(26, 37):
    weight.append(7)

# Constraint: Each color is in [1, 5]
for i in range(1, 37):
    solver.add(And(color[i-1] >= 1, color[i-1] <= 5))

# Core Clique (K5): Vertices 1-5 form a complete graph
# All colors must be distinct and cover 1-5
solver.add(Distinct(color[0:5]))

# Adjacency constraints for Core Clique (all pairs connected)
for i in range(0, 4):
    for j in range(i+1, 5):
        solver.add(color[i] != color[j])

# Cluster A: Vertices 6-15 (indices 5 to 14)
# Ring edges
for i in range(5, 14):
    solver.add(color[i] != color[i+1])
solver.add(color[14] != color[5])

# Chord edges
chords_A = [(6,9), (7,10), (8,11), (9,12), (10,13), (11,14), (12,15), (13,6), (14,7), (15,8)]
for u, v in chords_A:
    solver.add(color[u-1] != color[v-1])

# Connections to core
core_connections_A = [(6,1), (6,2), (9,2), (9,3), (12,3), (12,4), (15,4), (15,5)]
for u, v in core_connections_A:
    solver.add(color[u-1] != color[v-1])

# Cluster B: Vertices 16-25 (indices 15 to 24)
# Grid structure: 2 rows x 5 columns
# Row 1: 16-20 (indices 15-19), Row 2: 21-25 (indices 20-24)
# Horizontal edges
for i in range(15, 19):
    solver.add(color[i] != color[i+1])
for i in range(20, 24):
    solver.add(color[i] != color[i+1])

# Vertical edges
for i in range(15, 20):
    solver.add(color[i] != color[i+5])

# Diagonal edges
for i in range(15, 19):
    solver.add(color[i] != color[i+6])

# Connections to core
core_connections_B = [(16,1), (20,5)]
for u, v in core_connections_B:
    solver.add(color[u-1] != color[v-1])

# Connections to Cluster A
cluster_connections_B = [(18,8), (23,13)]
for u, v in cluster_connections_B:
    solver.add(color[u-1] != color[v-1])

# Cluster C: Vertices 26-36 (indices 25 to 35)
# Cycle edges
for i in range(25, 35):
    solver.add(color[i] != color[i+1])
solver.add(color[35] != color[25])

# Chord edges (3 steps apart)
chords_C = [(26,29), (27,30), (28,31), (29,32), (30,33), (31,34), (32,35), (33,36), (34,26), (35,27), (36,28)]
for u, v in chords_C:
    solver.add(color[u-1] != color[v-1])

# Connections to core
core_connections_C = [(26,1), (26,5), (31,3)]
for u, v in core_connections_C:
    solver.add(color[u-1] != color[v-1])

# Connections to Cluster B
cluster_connections_C = [(28,19), (33,24)]
for u, v in cluster_connections_C:
    solver.add(color[u-1] != color[v-1])

# Weighted cost constraint: sum(color[i] * weight[i] for i in 1..36) <= 850
weighted_cost_expr = []
for i in range(1, 37):
    c = color[i-1]
    w = weight[i]
    weighted_cost_expr.append(If(c == 1, w * 1, \
                            If(c == 2, w * 2, \
                            If(c == 3, w * 3, \
                            If(c == 4, w * 4, \
                            w * 5)))))
weighted_cost = Sum(weighted_cost_expr)
solver.add(weighted_cost <= 850)

# Check for a solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print the coloring for vertices 1 to 36
    coloring = [model[color[i]].as_long() for i in range(36)]
    for i in range(36):
        print(f"vertex_{i+1} = {coloring[i]}")
    # Print the weighted cost
    cost = sum(coloring[i] * weight[i+1] for i in range(36))
    print(f"weighted_cost = {cost}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")