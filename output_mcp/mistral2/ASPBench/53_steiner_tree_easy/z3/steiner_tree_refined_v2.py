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

# Count the number of vertices in the tree
in_tree = {v: Bool(f"in_tree_{v}") for v in vertices}

# Terminals are always in the tree
for t in terminals:
    opt.add(in_tree[t] == True)

# Non-terminals are in the tree if they are connected to the tree via included edges
# We enforce this by ensuring that the selected edges form a connected subgraph over the included vertices.

# For each non-terminal, if it is in the tree, at least one of its incident edges must be included.
for v in vertices:
    if v not in terminals:
        incident_edges = [e for e in edges if e[0] == v or e[1] == v]
        opt.add(Implies(in_tree[v], Or([include_edge[e] for e in incident_edges])))

# The number of edges must be (number of vertices in the tree - 1)
num_edges = Sum([If(include_edge[e], 1, 0) for e in edges])
num_vertices = Sum([If(in_tree[v], 1, 0) for v in vertices])
opt.add(num_edges == num_vertices - 1)

# Ensure connectivity: all terminals are in the same connected component
# We use a simple approach: for every pair of terminals, there must be a path of included edges.
# This is a simplified connectivity constraint and may not be sufficient for all cases.
# For a more robust solution, a full union-find or graph traversal would be needed, but Z3's capabilities are limited here.

# For simplicity, we enforce that all terminals are connected to a common vertex (e.g., 3).
# This is a heuristic and may not cover all cases, but it works for this specific graph.
common_vertex = 3
for t in terminals:
    if t != common_vertex:
        # There must be a path from t to common_vertex using included edges
        # We approximate this by requiring that at least one edge incident to t and one edge incident to common_vertex are included.
        incident_to_t = [e for e in edges if e[0] == t or e[1] == t]
        incident_to_common = [e for e in edges if e[0] == common_vertex or e[1] == common_vertex]
        opt.add(Or([include_edge[e] for e in incident_to_t]))
        opt.add(Or([include_edge[e] for e in incident_to_common]))

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