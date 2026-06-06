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

# Union-Find using Z3 arrays
parent = Array('parent', IntSort(), IntSort())
rank = Array('rank', IntSort(), IntSort())

# Initialize union-find
for v in vertices:
    solver.add(Select(parent, v) == v)
    solver.add(Select(rank, v) == 0)

# Iterative find function
def find(v):
    # Iteratively find the root
    root = v
    while True:
        p = Select(parent, root)
        if p == root:
            break
        root = p
    # Path compression: set parent of v to root
    solver.add(Select(parent, v) == root)
    return root

# Union function - returns a constraint
def make_union(u, v):
    fu = find(u)
    fv = find(v)
    rk_fu = Select(rank, fu)
    rk_fv = Select(rank, fv)
    return If(fu == fv,
               True,  # Already in the same set
               If(rk_fu < rk_fv,
                  Select(parent, fu) == fv,
                  If(rk_fu > rk_fv,
                     Select(parent, fv) == fu,
                     And(Select(parent, fv) == fu, Select(rank, fu) == rk_fu + 1))))

# For each selected edge, perform union
for (u, v, w) in edges:
    solver.add(Implies(edge_vars[(u, v, w)], make_union(u, v)))

# Ensure all terminals are in the same set
root = Int("root")
solver.add(root == find(0))
for t in terminals:
    solver.add(find(t) == root)

# Ensure the selected edges form a tree (no cycles)
# The number of selected edges must be at least (number of terminals - 1)
# And at most (number of vertices - 1)
num_selected_edges = Sum([If(edge_vars[e], 1, 0) for e in edges])
solver.add(num_selected_edges >= len(terminals) - 1)
solver.add(num_selected_edges <= len(vertices) - 1)

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