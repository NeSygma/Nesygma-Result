from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Graph data
vertices = [0, 1, 2, 3, 4, 5, 6]
edges = [
    (0, 1, 3), (0, 2, 5),
    (1, 3, 2), (1, 4, 4),
    (2, 3, 1), (2, 5, 6),
    (3, 4, 3), (3, 5, 3), (3, 6, 2),
    (4, 5, 2),
    (5, 6, 4)
]
terminals = [0, 5, 6]

# Create an Optimize instance for minimization
opt = Optimize()

# Decision variables: include_edge[e] = True if edge e is in the tree
# e is a tuple (u, v, weight)
include_edge = {e: Bool(f"include_{e[0]}_{e[1]}") for e in edges}

# Total weight of the tree
total_weight = Int("total_weight")

# Constraint: total_weight is the sum of weights of included edges
opt.add(total_weight == Sum([
    If(include_edge[e], e[2], 0) for e in edges
]))

# Constraint: All terminals must be connected
# We enforce connectivity by ensuring that the selected edges form a spanning tree over the terminals and any included Steiner vertices.
# We use a union-find (disjoint set) approach to ensure connectivity.

# We define a function to find the root of a vertex in the union-find structure.
def find(u, parent):
    return If(parent[u] == u, u, find(parent[u], parent))

# Initialize parent array for union-find
parent = {v: Int(f"parent_{v}") for v in vertices}
for v in vertices:
    opt.add(parent[v] == v)  # Initially, each vertex is its own parent

# For each edge, if it is included, union the two vertices
for (u, v, _) in edges:
    opt.add(Implies(include_edge[(u, v, _)], 
                    parent[find(u, parent)] == find(v, parent)))

# After processing all edges, all terminals must have the same root
root = Int("root")
opt.add(root == parent[terminals[0]])
for t in terminals[1:]:
    opt.add(parent[t] == root)

# Constraint: The selected edges must form a tree (no cycles, connected)
# We enforce this by ensuring that the number of edges is exactly (number of vertices in the tree - 1).

# Count the number of vertices in the tree
# We define a variable for each vertex indicating whether it is in the tree.
in_tree = {v: Bool(f"in_tree_{v}") for v in vertices}

# A vertex is in the tree if it is a terminal or if it is connected to the root via included edges.
# We enforce this by ensuring that if a vertex is a terminal, it is in the tree.
for t in terminals:
    opt.add(in_tree[t] == True)

# For non-terminals, a vertex is in the tree if it is connected to the root via included edges.
# We use the parent array to determine connectivity.
for v in vertices:
    if v not in terminals:
        opt.add(in_tree[v] == (parent[v] == root))

# The number of edges must be (number of vertices in the tree - 1)
num_edges = Sum([If(include_edge[e], 1, 0) for e in edges])
num_vertices = Sum([If(in_tree[v], 1, 0) for v in vertices])
opt.add(num_edges == num_vertices - 1)

# Objective: Minimize total_weight
opt.minimize(total_weight)

# Check and print result
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Optimal total weight:", model[total_weight])
    
    # Extract the tree edges
    tree_edges = []
    for e in edges:
        if model[include_edge[e]]:
            tree_edges.append(e)
    print("Tree edges:", tree_edges)
    
    # Extract Steiner vertices (non-terminals in the tree)
    steiner_vertices = []
    for v in vertices:
        if v not in terminals and model[in_tree[v]]:
            steiner_vertices.append(v)
    print("Steiner vertices:", steiner_vertices)
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")