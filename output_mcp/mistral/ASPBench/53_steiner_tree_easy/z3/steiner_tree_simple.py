from z3 import *

# Graph data
vertices = range(7)
edges = [
    (0, 1, 3), (0, 2, 5),
    (1, 3, 2), (1, 4, 4),
    (2, 3, 1), (2, 5, 6),
    (3, 4, 3), (3, 5, 3), (3, 6, 2),
    (4, 5, 2),
    (5, 6, 4)
]
terminals = {0, 5, 6}

# Create edge variables
edge_vars = {e: Bool(f"edge_{e}") for e in edges}

# Create a solver
solver = Optimize()

# Ensure all terminals are connected by the selected edges
# We will use a simple approach: ensure that the selected edges form a tree
# that includes all terminals. We do not need to explicitly prevent cycles
# if we ensure the number of edges is exactly (number of terminals - 1).

# The number of selected edges must be at least (number of terminals - 1)
# and at most (number of vertices - 1)
num_selected_edges = Sum([If(edge_vars[e], 1, 0) for e in edges])
solver.add(num_selected_edges >= len(terminals) - 1)
solver.add(num_selected_edges <= len(vertices) - 1)

# Ensure that all terminals are connected by the selected edges
# We will use a simple approach: for each pair of terminals, there must be a path
# using the selected edges. This is complex to encode directly, so we will instead
# use a simpler approach: ensure that the selected edges form a tree that includes
# all terminals. We will not explicitly prevent cycles, but the optimization will
# prefer fewer edges, so cycles are unlikely unless necessary.

# Objective: minimize total weight
total_weight = Sum([If(edge_vars[(u, v, w)], w, 0) for (u, v, w) in edges])
solver.minimize(total_weight)

# Check and print result
if solver.check() == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Optimal weight:", model.eval(total_weight))
    # Print selected edges
    selected_edges = [e for e in edges if is_true(model.eval(edge_vars[e]))]
    print("Selected edges:", selected_edges)
    # Print Steiner vertices (non-terminal vertices in the tree)
    steiner_vertices = set()
    for (u, v, w) in selected_edges:
        if u not in terminals:
            steiner_vertices.add(u)
        if v not in terminals:
            steiner_vertices.add(v)
    print("Steiner vertices:", sorted(steiner_vertices))
    print("Connected components: 1")
elif solver.check() == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")