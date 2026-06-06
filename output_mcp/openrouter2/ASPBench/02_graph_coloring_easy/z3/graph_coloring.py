from z3 import *

# Define vertices and edges
vertices = [1, 2, 3, 4, 5, 6]
edges = [
    (1, 2), (1, 3),
    (2, 3), (2, 4),
    (3, 4), (3, 5),
    (4, 5), (4, 6),
    (5, 6)
]

# Solver
solver = Optimize()

# Number of colors variable
num_colors = Int('num_colors')
solver.add(num_colors >= 1, num_colors <= len(vertices))

# Color assignment for each vertex
color = {v: Int(f'color_{v}') for v in vertices}
for v in vertices:
    solver.add(color[v] >= 1, color[v] <= num_colors)

# Adjacent vertices must have different colors
for (u, v) in edges:
    solver.add(color[u] != color[v])

# Objective: minimize number of colors
solver.minimize(num_colors)

# Check and output
result = solver.check()
if result == sat:
    m = solver.model()
    num_val = m[num_colors].as_long()
    coloring = [(v, m[color[v]].as_long()) for v in vertices]
    print("STATUS: sat")
    print("num_colors =", num_val)
    print("coloring =", coloring)
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")