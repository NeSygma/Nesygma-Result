from z3 import *

# Solver instance
solver = Solver()

# Number of vertices
N = 36

# Colors variables: 1-indexed list
colors = [Int(f"c{i}") for i in range(1, N+1)]

# Domain constraints: colors in [1,5]
for c in colors:
    solver.add(c >= 1, c <= 5)

# Weights per vertex (index 0..35)
weights = []
# vertices 1-5 weight 10
weights += [10]*5
# vertices 6-15 weight 3
weights += [3]*10
# vertices 16-25 weight 5
weights += [5]*10
# vertices 26-36 weight 7
weights += [7]*11

# Edge list
edges = []
# Core clique (vertices 1-5)
core = [1,2,3,4,5]
for i in range(len(core)):
    for j in range(i+1, len(core)):
        edges.append((core[i], core[j]))

# Cluster A edges
# Ring
ring = [(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,6)]
edges += ring
# Diagonals
diags = [(6,9),(7,10),(8,11),(9,12),(10,13),(11,14),(12,15),(13,6),(14,7),(15,8)]
edges += diags
# Connections to core
edges += [(6,1),(6,2),(9,2),(9,3),(12,3),(12,4),(15,4),(15,5)]

# Cluster B edges
# Horizontal
horiz = [(16,17),(17,18),(18,19),(19,20),(21,22),(22,23),(23,24),(24,25)]
edges += horiz
# Vertical
vert = [(16,21),(17,22),(18,23),(19,24),(20,25)]
edges += vert
# Diagonal
diagB = [(16,22),(17,23),(18,24),(19,25)]
edges += diagB
# Connections to core
edges += [(16,1),(20,5)]
# Connections to Cluster A
edges += [(18,8),(23,13)]

# Cluster C edges
# Cycle
cycle = [(26,27),(27,28),(28,29),(29,30),(30,31),(31,32),(32,33),(33,34),(34,35),(35,36),(36,26)]
edges += cycle
# Chords (3 steps apart)
chords = [(26,29),(27,30),(28,31),(29,32),(30,33),(31,34),(32,35),(33,36),(34,26),(35,27),(36,28)]
edges += chords
# Connections to core
edges += [(26,1),(26,5),(31,3)]
# Connections to Cluster B
edges += [(28,19),(33,24)]

# Add adjacency constraints
for (u,v) in edges:
    solver.add(colors[u-1] != colors[v-1])

# All 5 colors must be used at least once
for col in range(1,6):
    solver.add(Or([c == col for c in colors]))

# Weighted cost constraint
weighted_cost = Sum([colors[i]*weights[i] for i in range(N)])
solver.add(weighted_cost <= 850)

# Check satisfiability
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print each vertex color
    for i in range(1, N+1):
        val = m[colors[i-1]]
        if val is None:
            # Should not happen due to domain constraints
            val = 1
        print(f"{i} = {val.as_long()}")
    # Print weighted cost
    cost_val = sum(m[colors[i]].as_long() * weights[i] for i in range(N))
    print(f"weighted_cost = {cost_val}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")