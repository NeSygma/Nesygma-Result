from z3 import *

# Vertices 1..8
verts = list(range(1, 9))
# Boolean variable for each vertex: True if vertex is in the independent set
selected = [Bool(f"x{i}") for i in verts]

# Create an Optimize instance for maximization
solver = Optimize()

# Graph edges (undirected)
edges = [
    (1, 2), (1, 3), (1, 4),
    (2, 5),
    (3, 6), (3, 7),
    (4, 8),
    (5, 6),
    (6, 7),
    (7, 8)
]

# Add independence constraints: for each edge (u,v), at most one endpoint can be selected
for u, v in edges:
    # At most one of u, v can be selected
    solver.add(Implies(selected[u-1], Not(selected[v-1])))
    solver.add(Implies(selected[v-1], Not(selected[u-1])))

# Objective: maximize the number of selected vertices
solver.maximize(Sum(selected))

# Check the optimization problem
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Collect the vertices that are selected (True) in the optimal model
    chosen = [i+1 for i in range(len(verts)) if model[selected[i]]]
    print("Independent set size:", len(chosen))
    print("Vertices in the independent set:", chosen)
else:
    print("STATUS: unsat")