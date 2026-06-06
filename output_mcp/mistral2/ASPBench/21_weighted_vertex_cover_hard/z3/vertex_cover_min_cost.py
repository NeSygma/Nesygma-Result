from z3 import *

# Define the vertices and their costs
vertices = range(16)
high_cost_vertices = {2, 10, 14}
cost = {v: 3 if v in high_cost_vertices else 1 for v in vertices}

# Master vertices
master_vertices = {0, 15}

# Standard edges
standard_edges = [(1, 3), (1, 4), (2, 6), (3, 7), (4, 8), (5, 11), (6, 7), (7, 12), (8, 12), (11, 13), (12, 13), (13, 14)]

# Heavy edges
heavy_edges = [(0, 5), (9, 10), (14, 15)]

# Antagonistic pairs
antagonistic_pairs = [(1, 2), (8, 9)]

# Declare boolean variables for each vertex
selected = [Bool(f"selected_{i}") for i in vertices]

# Create an optimizer instance
opt = Optimize()

# Add constraints for standard edge coverage
for u, v in standard_edges:
    opt.add(Or(selected[u], selected[v]))

# Add constraints for heavy edge coverage
for u, v in heavy_edges:
    # If both are not master vertices, both must be selected
    if u not in master_vertices and v not in master_vertices:
        opt.add(selected[u])
        opt.add(selected[v])
    # If one is a master vertex, selecting only the master vertex is sufficient
    elif u in master_vertices:
        opt.add(Or(selected[u], And(selected[u], selected[v])))
    elif v in master_vertices:
        opt.add(Or(selected[v], And(selected[u], selected[v])))

# Add constraints for antagonistic pairs
for u, v in antagonistic_pairs:
    opt.add(Not(And(selected[u], selected[v])))

# Define the objective: minimize the total cost
total_cost = Sum([If(selected[i], cost[i], 0) for i in vertices])
opt.minimize(total_cost)

# Check for a solution
result = opt.check()

if result == sat:
    model = opt.model()
    selected_vertices = [i for i in vertices if is_true(model[selected[i]])]
    total_cost_value = sum(cost[i] for i in selected_vertices)
    print("STATUS: sat")
    print("vertex_cover =", sorted(selected_vertices))
    print("total_cost =", total_cost_value)
elif result == unsat:
    print("STATUS: unsat")
    print("No solution exists.")
else:
    print("STATUS: unknown")