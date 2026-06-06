from z3 import *

solver = Solver()

# Vertices 1..36
N = 36
colors = [Int(f'c_{i}') for i in range(1, N+1)]

# Domain: each color in {1,2,3,4,5}
for i in range(N):
    solver.add(colors[i] >= 1, colors[i] <= 5)

# Weights
weights = {}
for v in range(1, 6):
    weights[v] = 10
for v in range(6, 16):
    weights[v] = 3
for v in range(16, 26):
    weights[v] = 5
for v in range(26, 37):
    weights[v] = 7

# Weighted cost <= 850
weighted_cost = Sum([colors[i] * weights[i+1] for i in range(N)])
solver.add(weighted_cost <= 850)

# Helper: add edge constraint
def add_edge(u, v):
    solver.add(colors[u-1] != colors[v-1])

# Core Clique K5: vertices 1-5 all pairwise different
for i in range(1, 6):
    for j in range(i+1, 6):
        add_edge(i, j)

# Cluster A (vertices 6-15)
# Ring edges
ring_a = [(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,6)]
for u,v in ring_a:
    add_edge(u,v)

# Diagonal chords
diag_a = [(6,9),(7,10),(8,11),(9,12),(10,13),(11,14),(12,15),(13,6),(14,7),(15,8)]
for u,v in diag_a:
    add_edge(u,v)

# Connections from Cluster A to core
core_a = [(6,1),(6,2),(9,2),(9,3),(12,3),(12,4),(15,4),(15,5)]
for u,v in core_a:
    add_edge(u,v)

# Cluster B (vertices 16-25)
# Horizontal edges
horiz_b = [(16,17),(17,18),(18,19),(19,20),(21,22),(22,23),(23,24),(24,25)]
for u,v in horiz_b:
    add_edge(u,v)

# Vertical edges
vert_b = [(16,21),(17,22),(18,23),(19,24),(20,25)]
for u,v in vert_b:
    add_edge(u,v)

# Diagonal edges
diag_b = [(16,22),(17,23),(18,24),(19,25)]
for u,v in diag_b:
    add_edge(u,v)

# Connections from Cluster B to core
core_b = [(16,1),(20,5)]
for u,v in core_b:
    add_edge(u,v)

# Connections from Cluster B to Cluster A
ab_conn = [(18,8),(23,13)]
for u,v in ab_conn:
    add_edge(u,v)

# Cluster C (vertices 26-36)
# Cycle edges
cycle_c = [(26,27),(27,28),(28,29),(29,30),(30,31),(31,32),(32,33),(33,34),(34,35),(35,36),(36,26)]
for u,v in cycle_c:
    add_edge(u,v)

# Chord edges (3 apart)
chord_c = [(26,29),(27,30),(28,31),(29,32),(30,33),(31,34),(32,35),(33,36),(34,26),(35,27),(36,28)]
for u,v in chord_c:
    add_edge(u,v)

# Connections from Cluster C to core
core_c = [(26,1),(26,5),(31,3)]
for u,v in core_c:
    add_edge(u,v)

# Connections from Cluster C to Cluster B
cb_conn = [(28,19),(33,24)]
for u,v in cb_conn:
    add_edge(u,v)

# All 5 colors must be used (due to K5 core, but add explicit constraint)
solver.add(And([Or([colors[i] == col for i in range(N)]) for col in range(1,6)]))

result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    coloring = [m.eval(colors[i]).as_long() for i in range(N)]
    print("Coloring:", coloring)
    # Compute weighted cost
    wc = sum(coloring[i] * weights[i+1] for i in range(N))
    print("weighted_cost =", wc)
    # Verify constraints
    print("Cost <= 850:", wc <= 850)
    # Verify no adjacent same color
    ok = True
    for u,v in ring_a+diag_a+core_a+horiz_b+vert_b+diag_b+core_b+ab_conn+cycle_c+chord_c+core_c+cb_conn:
        if coloring[u-1] == coloring[v-1]:
            print(f"ERROR: edge ({u},{v}) same color {coloring[u-1]}")
            ok = False
    # K5
    for i in range(1,6):
        for j in range(i+1,6):
            if coloring[i-1] == coloring[j-1]:
                print(f"ERROR: K5 edge ({i},{j}) same color {coloring[i-1]}")
                ok = False
    if ok:
        print("All adjacency constraints satisfied.")
else:
    print("STATUS: unsat")
    print("No solution found.")