from z3 import *

# Create solver
solver = Solver()

# Number of vertices
n = 36
# Colors variables indexed 0..35 for vertices 1..36
colors = [Int(f'c{i+1}') for i in range(n)]

# Domain constraints: colors in 1..5
for c in colors:
    solver.add(c >= 1, c <= 5)

# Distinct colors for core K5 vertices 1-5
solver.add(Distinct(colors[0:5]))

# Weights per vertex
weights = []
for i in range(1, n+1):
    if 1 <= i <= 5:
        w = 10
    elif 6 <= i <= 15:
        w = 3
    elif 16 <= i <= 25:
        w = 5
    else:
        w = 7
    weights.append(w)

# Edge list (undirected)
edges = []
# Core K5 edges
for i in range(1,6):
    for j in range(i+1,6):
        edges.append((i,j))
# Cluster A ring
ringA = [(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,6)]
edges.extend(ringA)
# Cluster A chords
chordsA = [(6,9),(7,10),(8,11),(9,12),(10,13),(11,14),(12,15),(13,6),(14,7),(15,8)]
edges.extend(chordsA)
# Connections to core from A
edges.extend([(6,1),(6,2),(9,2),(9,3),(12,3),(12,4),(15,4),(15,5)])
# Cluster B horizontal
horizB = [(16,17),(17,18),(18,19),(19,20),(21,22),(22,23),(23,24),(24,25)]
edges.extend(horizB)
# Vertical B
vertB = [(16,21),(17,22),(18,23),(19,24),(20,25)]
edges.extend(vertB)
# Diagonal B
diagB = [(16,22),(17,23),(18,24),(19,25)]
edges.extend(diagB)
# Connections to core B
edges.extend([(16,1),(20,5)])
# Connections to Cluster A from B
edges.extend([(18,8),(23,13)])
# Cluster C cycle
cycleC = [(26,27),(27,28),(28,29),(29,30),(30,31),(31,32),(32,33),(33,34),(34,35),(35,36),(36,26)]
edges.extend(cycleC)
# Chords C (3 steps apart)
chordsC = [(26,29),(27,30),(28,31),(29,32),(30,33),(31,34),(32,35),(33,36),(34,26),(35,27),(36,28)]
edges.extend(chordsC)
# Connections to core C
edges.extend([(26,1),(26,5),(31,3)])
# Connections to Cluster B from C
edges.extend([(28,19),(33,24)])

# Add adjacency constraints
for (u,v) in edges:
    solver.add(colors[u-1] != colors[v-1])

# Weighted cost bound
cost = Sum([colors[i] * weights[i] for i in range(n)])
solver.add(cost <= 850)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Extract colors in order
    col_vals = [m.eval(colors[i]).as_long() for i in range(n)]
    print("colors =", col_vals)
    # Compute cost value
    cost_val = sum(col_vals[i] * weights[i] for i in range(n))
    print("weighted_cost =", cost_val)
else:
    print("STATUS: unsat" if result == unsat else "STATUS: unknown")