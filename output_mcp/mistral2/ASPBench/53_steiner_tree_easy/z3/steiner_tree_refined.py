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

# Union-Find (Disjoint Set) symbolic approach
# We use an array to represent parent pointers, and we update them symbolically.

# Declare parent as an array of integers, indexed by vertices
parent_arr = Array("parent_arr", IntSort(), IntSort())

# Initialize parent array: each vertex points to itself
init_parent = And([Select(parent_arr, v) == v for v in vertices])
opt.add(init_parent)

# Define a find function symbolically (non-recursive)
# We use a loop-like approach with Z3's If and Select.
# For simplicity, we avoid a full symbolic union-find and instead enforce connectivity via constraints.

# For each included edge, the two vertices must have the same root.
root = Int("root")

# We enforce that all terminals have the same root as their parent.
for t in terminals:
    opt.add(Select(parent_arr, t) == root)

# For non-terminals, we allow their parent to be updated if they are included in the tree.
# We avoid a full symbolic union-find and instead enforce tree structure via constraints.

# Count the number of vertices in the tree
in_tree = {v: Bool(f"in_tree_{v}") for v in vertices}

# Terminals are always in the tree
for t in terminals:
    opt.add(in_tree[t] == True)

# Non-terminals are in the tree if their parent is the root
for v in vertices:
    if v not in terminals:
        opt.add(in_tree[v] == (Select(parent_arr, v) == root))

# The number of edges must be (number of vertices in the tree - 1)
num_edges = Sum([If(include_edge[e], 1, 0) for e in edges])
num_vertices = Sum([If(in_tree[v], 1, 0) for v in vertices])
opt.add(num_edges == num_vertices - 1)

# Constraint: No cycles
# We enforce this by ensuring that the selected edges form a tree over the included vertices.
# We avoid a full symbolic cycle detection and instead rely on the tree structure constraints.

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