from z3 import *

# Define vertices and edges
vertices = [1,2,3,4,5,6]
edges = [(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,5),(4,6),(5,6)]

solver = Optimize()

# Variables: color for each vertex
color = {v: Int(f'color_{v}') for v in vertices}
# Variable for number of colors used
num_colors = Int('num_colors')

# Constraints: colors are between 1 and num_colors
solver.add(num_colors >= 1)
for v in vertices:
    solver.add(color[v] >= 1, color[v] <= num_colors)

# Edge constraints: adjacent vertices have different colors
for (u,v) in edges:
    solver.add(color[u] != color[v])

# Objective: minimize number of colors
solver.minimize(num_colors)

result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("num_colors =", m.eval(num_colors))
    for v in vertices:
        print(f"vertex {v} =", m.eval(color[v]))
else:
    print("STATUS: unsat" if result == unsat else "STATUS: unknown")