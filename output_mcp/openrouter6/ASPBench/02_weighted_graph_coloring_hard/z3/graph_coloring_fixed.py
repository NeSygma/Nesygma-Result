from z3 import *

# Create solver
solver = Solver()

# Define vertices 1-36 (index 0 unused)
colors = [Int(f'v{i}') for i in range(37)]  # colors[1] to colors[36]

# Domain constraints: colors between 1 and 5
for i in range(1, 37):
    solver.add(colors[i] >= 1, colors[i] <= 5)

# Define weights
weights = [0] * 37
for i in range(1, 6):
    weights[i] = 10
for i in range(6, 16):
    weights[i] = 3
for i in range(16, 26):
    weights[i] = 5
for i in range(26, 37):
    weights[i] = 7

# Helper to add edge constraint
def add_edge(u, v):
    solver.add(colors[u] != colors[v])

# Core clique (K5): vertices 1-5, all pairs
core_vertices = [1,2,3,4,5]
for i in range(len(core_vertices)):
    for j in range(i+1, len(core_vertices)):
        add_edge(core_vertices[i], core_vertices[j])

# Cluster A (vertices 6-15)
# Ring edges
ring_edges = [(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,6)]
for u,v in ring_edges:
    add_edge(u,v)

# Diagonal chords
chord_edges = [(6,9),(7,10),(8,11),(9,12),(10,13),(11,14),(12,15),(13,6),(14,7),(15,8)]
for u,v in chord_edges:
    add_edge(u,v)

# Connections to core
core_connections_A = [(6,1),(6,2),(9,2),(9,3),(12,3),(12,4),(15,4),(15,5)]
for u,v in core_connections_A:
    add_edge(u,v)

# Cluster B (vertices 16-25)
# Horizontal edges
horizontal_edges = [(16,17),(17,18),(18,19),(19,20),(21,22),(22,23),(23,24),(24,25)]
for u,v in horizontal_edges:
    add_edge(u,v)

# Vertical edges
vertical_edges = [(16,21),(17,22),(18,23),(19,24),(20,25)]
for u,v in vertical_edges:
    add_edge(u,v)

# Diagonal edges
diagonal_edges = [(16,22),(17,23),(18,24),(19,25)]
for u,v in diagonal_edges:
    add_edge(u,v)

# Connections to core
core_connections_B = [(16,1),(20,5)]
for u,v in core_connections_B:
    add_edge(u,v)

# Connections to Cluster A
cluster_connections_B = [(18,8),(23,13)]
for u,v in cluster_connections_B:
    add_edge(u,v)

# Cluster C (vertices 26-36)
# Cycle edges
cycle_edges = [(26,27),(27,28),(28,29),(29,30),(30,31),(31,32),(32,33),(33,34),(34,35),(35,36),(36,26)]
for u,v in cycle_edges:
    add_edge(u,v)

# Chord edges (3 steps apart)
chord_edges_C = [(26,29),(27,30),(28,31),(29,32),(30,33),(31,34),(32,35),(33,36),(34,26),(35,27),(36,28)]
for u,v in chord_edges_C:
    add_edge(u,v)

# Connections to core
core_connections_C = [(26,1),(26,5),(31,3)]
for u,v in core_connections_C:
    add_edge(u,v)

# Connections to Cluster B
cluster_connections_C = [(28,19),(33,24)]
for u,v in cluster_connections_C:
    add_edge(u,v)

# Constraint: all 5 colors must be used (due to K5, but explicit)
# Since K5 forces all 5 colors, we can add constraint that each color appears at least once
# But we can also just rely on K5; however, to be safe, add explicit constraint
# We'll add that colors 1-5 each appear at least once among vertices 1-5
# Actually, K5 already forces all 5 colors, so we don't need extra constraint.
# But let's add it for completeness:
for c in range(1, 6):
    solver.add(Or([colors[i] == c for i in core_vertices]))

# Weighted cost constraint
# weighted_cost = sum over v of color(v) * weight(v) <= 850
cost_expr = Sum([colors[i] * weights[i] for i in range(1, 37)])
solver.add(cost_expr <= 850)

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Coloring found:")
    coloring = []
    total_cost = 0
    for i in range(1, 37):
        color_val = model[colors[i]]
        # color_val is a Z3 integer constant, convert to Python int
        color_int = int(color_val.as_string())
        coloring.append(color_int)
        contribution = color_int * weights[i]
        total_cost += contribution
        print(f"Vertex {i}: color {color_int}, weight {weights[i]}, contribution {contribution}")
    
    print(f"Total weighted cost: {total_cost}")
    if total_cost <= 850:
        print("Cost constraint satisfied.")
    else:
        print("ERROR: Cost constraint violated!")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No valid coloring exists with cost ≤ 850")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")