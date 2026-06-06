from z3 import *

# Create optimizer
opt = Optimize()

# Boolean variable for each vertex 1..7
d = [Bool(f'd{i}') for i in range(1, 8)]  # d[0] -> vertex 1, ..., d[6] -> vertex 7

# Adjacency list
adj = {
    1: [2, 3],
    2: [1, 3, 4],
    3: [1, 2, 5],
    4: [2, 6],
    5: [3, 6, 7],
    6: [4, 5, 7],
    7: [5, 6]
}

# Domination constraints: each vertex must be dominated by itself or a neighbor
for v in range(1, 8):
    neighbors = adj[v]
    # Build Or over the vertex and its neighbors
    vars_for_or = [d[v-1]] + [d[u-1] for u in neighbors]
    opt.add(Or(vars_for_or))

# Objective: minimize the size of the dominating set
opt.minimize(Sum([If(d[i], 1, 0) for i in range(7)]))

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    # Collect vertices that are True in the model
    selected = [i + 1 for i in range(7) if model[d[i]] == True]
    selected.sort()
    print("STATUS: sat")
    print(f"dominating_set = {selected}")
    print(f"size = {len(selected)}")
else:
    print("STATUS: unsat")