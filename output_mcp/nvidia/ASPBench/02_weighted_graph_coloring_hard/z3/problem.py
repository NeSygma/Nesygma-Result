from z3 import *

# Declare color variables for vertices 1..36
colors = [Int(f'c{i}') for i in range(1, 37)]

# Weight per vertex
weights = []
for i in range(1, 6):
    weights.append(10)  # vertices 1-5
for i in range(6, 16):
    weights.append(3)   # vertices 6-15
for i in range(16, 26):
    weights.append(5)   # vertices 16-25
for i in range(26, 37):
    weights.append(7)   # vertices 26-36

solver = Solver()

# 1. Each color is in 1..5
for i in range(36):
    solver.add(colors[i] >= 1, colors[i] <= 5)

# 2. Adjacency constraints (no same color for adjacent vertices)
def add_ne(u, v):
    # u, v are 1-indexed
    solver.add(colors[u-1] != colors[v-1])

# Core K5: all pairs among 1..5
for i in range(1, 6):
    for j in range(i+1, 6):
        add_ne(i, j)

# Cluster A edges
# ring
add_ne(6,7); add_ne(7,8); add_ne(8,9); add_ne(9,10); add_ne(10,11); add_ne(11,12); add_ne(12,13); add_ne(13,14); add_ne(14,15); add_ne(15,6)
# diagonal chords
add_ne(6,9); add_ne(7,10); add_ne(8,11); add_ne(9,12); add_ne(10,13); add_ne(11,14); add_ne(12,15); add_ne(13,6); add_ne(14,7); add_ne(15,8)
# connections to core
add_ne(6,1); add_ne(6,2)
add_ne(9,2); add_ne(9,3)
add_ne(12,3); add_ne(12,4)
add_ne(15,4); add_ne(15,5)

# Cluster B edges
# horizontal
add_ne(16,17); add_ne(17,18); add_ne(18,19); add_ne(19,20)
add_ne(21,22); add_ne(22,23); add_ne(23,24); add_ne(24,25)
# vertical
add_ne(16,21); add_ne(17,22); add_ne(18,23); add_ne(19,24); add_ne(20,25)
# diagonal
add_ne(16,22); add_ne(17,23); add_ne(18,24); add_ne(19,25)
# connections to core
add_ne(16,1); add_ne(20,5)
# connections to Cluster A
add_ne(18,8); add_ne(23,13)

# Cluster C edges
# cycle
add_ne(26,27); add_ne(27,28); add_ne(28,29); add_ne(29,30); add_ne(30,31); add_ne(31,32); add_ne(32,33); add_ne(33,34); add_ne(34,35); add_ne(35,36); add_ne(36,26)
# chords (3 steps apart)
add_ne(26,29); add_ne(27,30); add_ne(28,31); add_ne(29,32); add_ne(30,33); add_ne(31,34); add_ne(32,35); add_ne(33,36); add_ne(34,26); add_ne(35,27); add_ne(36,28)
# connections to core
add_ne(26,1); add_ne(26,5); add_ne(31,3)
# connections to Cluster B
add_ne(28,19); add_ne(33,24)

# 3. Weighted cost constraint: sum(color_i * weight_i) <= 850
cost_expr = Sum([colors[i] * weights[i] for i in range(36)])
solver.add(cost_expr <= 850)

# Check for satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print each color variable
    for i in range(1, 37):
        print(f"c{i} = {model[colors[i-1]]}")
    # Compute and print weighted cost
    cost_val = model.eval(cost_expr)
    print(f"weighted_cost = {cost_val}")
elif result == unsat:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE is effectively True for model finding
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")