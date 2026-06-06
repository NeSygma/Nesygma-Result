from z3 import *

solver = Solver()

# Colors: 1 through 5
# Vertices: 1 through 36
N = 36
colors = [Int(f'c_{i}') for i in range(1, N+1)]

# Domain: each vertex gets a color from {1, 2, 3, 4, 5}
for i in range(N):
    solver.add(1 <= colors[i])
    solver.add(colors[i] <= 5)

# Weights
weights = {}
for i in range(1, 6):
    weights[i] = 10
for i in range(6, 16):
    weights[i] = 3
for i in range(16, 26):
    weights[i] = 5
for i in range(26, 37):
    weights[i] = 7

# Build adjacency list
edges = set()

# Core Clique K5: vertices 1-5
for i in range(1, 6):
    for j in range(i+1, 6):
        edges.add((i, j))

# Cluster A (6-15): Ring structure
ring_a = [(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,6)]
for u,v in ring_a:
    edges.add((u,v))

# Cluster A: Diagonal chords
diag_a = [(6,9),(7,10),(8,11),(9,12),(10,13),(11,14),(12,15),(13,6),(14,7),(15,8)]
for u,v in diag_a:
    edges.add((u,v))

# Cluster A: Connections to core
core_a = [(6,1),(6,2),(9,2),(9,3),(12,3),(12,4),(15,4),(15,5)]
for u,v in core_a:
    edges.add((u,v))

# Cluster B (16-25): Grid structure
# Horizontal
h_b = [(16,17),(17,18),(18,19),(19,20),(21,22),(22,23),(23,24),(24,25)]
for u,v in h_b:
    edges.add((u,v))
# Vertical
v_b = [(16,21),(17,22),(18,23),(19,24),(20,25)]
for u,v in v_b:
    edges.add((u,v))
# Diagonal
d_b = [(16,22),(17,23),(18,24),(19,25)]
for u,v in d_b:
    edges.add((u,v))

# Cluster B: Connections to core
core_b = [(16,1),(20,5)]
for u,v in core_b:
    edges.add((u,v))

# Cluster B: Connections to Cluster A
b_a = [(18,8),(23,13)]
for u,v in b_a:
    edges.add((u,v))

# Cluster C (26-36): 11-cycle
cycle_c = [(26,27),(27,28),(28,29),(29,30),(30,31),(31,32),(32,33),(33,34),(34,35),(35,36),(36,26)]
for u,v in cycle_c:
    edges.add((u,v))

# Cluster C: Chords 3 steps apart
chords_c = [(26,29),(27,30),(28,31),(29,32),(30,33),(31,34),(32,35),(33,36),(34,26),(35,27),(36,28)]
for u,v in chords_c:
    edges.add((u,v))

# Cluster C: Connections to core
core_c = [(26,1),(26,5),(31,3)]
for u,v in core_c:
    edges.add((u,v))

# Cluster C: Connections to Cluster B
c_b = [(28,19),(33,24)]
for u,v in c_b:
    edges.add((u,v))

# Add adjacency constraints
for (u,v) in edges:
    solver.add(colors[u-1] != colors[v-1])

# All 5 colors must be used (due to K5, this is implicit but let's add explicit constraint)
# The K5 already forces all 5 colors, but let's add a redundant constraint for safety
solver.add(Or([colors[i] == 1 for i in range(N)]))
solver.add(Or([colors[i] == 2 for i in range(N)]))
solver.add(Or([colors[i] == 3 for i in range(N)]))
solver.add(Or([colors[i] == 4 for i in range(N)]))
solver.add(Or([colors[i] == 5 for i in range(N)]))

# Weighted cost constraint: sum(color(v) * weight(v)) <= 850
weighted_cost = Sum([colors[i] * weights[i+1] for i in range(N)])
solver.add(weighted_cost <= 850)

print("Solving...")
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Extract coloring
    coloring = [m.eval(colors[i]).as_long() for i in range(N)]
    
    # Calculate weighted cost
    total_cost = sum(coloring[i] * weights[i+1] for i in range(N))
    
    print(f"Coloring: {coloring}")
    print(f"Weighted cost: {total_cost}")
    
    # Print in a formatted way
    print("\nVertex | Color | Weight | Cost Contribution")
    print("-" * 45)
    for i in range(N):
        v = i + 1
        print(f"{v:6d} | {coloring[i]:5d} | {weights[v]:6d} | {coloring[i] * weights[v]:3d}")
    print(f"\nTotal weighted cost: {total_cost}")
    
    # Verify cost bound
    if total_cost <= 850:
        print("Cost bound satisfied (<= 850)")
    else:
        print(f"WARNING: Cost bound NOT satisfied ({total_cost} > 850)")
        
    # Verify no adjacent same colors
    violations = []
    for (u,v) in edges:
        if coloring[u-1] == coloring[v-1]:
            violations.append((u,v))
    if violations:
        print(f"WARNING: Adjacency violations: {violations}")
    else:
        print("All adjacency constraints satisfied")
        
    # Verify all colors used
    used_colors = set(coloring)
    print(f"Colors used: {sorted(used_colors)}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found with cost <= 850")
else:
    print("STATUS: unknown")