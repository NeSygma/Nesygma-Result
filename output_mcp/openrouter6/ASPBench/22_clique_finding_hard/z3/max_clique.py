from z3 import *

# Define vertices 0..19
n = 20
vertices = list(range(n))

# Types and weights
types = ['alpha', 'alpha', 'alpha', 'alpha', 'beta', 'alpha', 'beta', 'beta', 'beta', 'delta',
         'delta', 'beta', 'gamma', 'gamma', 'gamma', 'delta', 'delta', 'gamma', 'alpha', 'beta']
weights = [20, 20, 15, 20, 30, 15, 30, 30, 18, 10,
           10, 12, 25, 25, 20, 5, 5, 19, 40, 40]

# Edges as set of tuples (undirected)
edges_set = set([
    (0,1), (0,3), (0,4), (0,6), (0,7), (0,9), (0,10),
    (1,3), (1,4), (1,6), (1,7), (1,9),
    (2,5), (2,8), (2,11), (2,14), (2,17), (2,18),
    (3,4), (3,6), (3,7), (3,9),
    (4,6), (4,7), (4,9),
    (5,8), (5,11), (5,14), (5,17), (5,19),
    (6,7), (6,9),
    (7,9),
    (8,11), (8,14), (8,17),
    (11,14), (11,17),
    (12,13),
    (14,17),
    (15,16)
])

# Ensure edges are undirected: add both directions
edges = set()
for (u,v) in edges_set:
    edges.add((u,v))
    edges.add((v,u))

# Create solver
opt = Optimize()

# Boolean variables for vertex selection
selected = [Bool(f'selected_{i}') for i in range(n)]

# Clique property: for any non-edge, cannot have both selected
for i in range(n):
    for j in range(i+1, n):
        if (i,j) not in edges:
            opt.add(Not(And(selected[i], selected[j])))

# Type diversity constraint: for each type, count <= 2
# Get unique types
unique_types = list(set(types))
for t in unique_types:
    # indices of vertices with this type
    indices = [i for i, typ in enumerate(types) if typ == t]
    # sum of selected for these indices <= 2
    opt.add(Sum([If(selected[i], 1, 0) for i in indices]) <= 2)

# Weight limit constraint: total weight <= 100
total_weight = Sum([If(selected[i], weights[i], 0) for i in range(n)])
opt.add(total_weight <= 100)

# Objective: maximize clique size (number of selected vertices)
clique_size = Sum([If(selected[i], 1, 0) for i in range(n)])
opt.maximize(clique_size)

# Check
result = opt.check()
print(f"Solver result: {result}")

if result == sat:
    model = opt.model()
    # Extract selected vertices
    clique_vertices = []
    for i in range(n):
        if is_true(model[selected[i]]):
            clique_vertices.append(i)
    clique_vertices.sort()
    clique_size_val = len(clique_vertices)
    
    # Compute edges within clique
    clique_edges = []
    for i in range(clique_size_val):
        for j in range(i+1, clique_size_val):
            u = clique_vertices[i]
            v = clique_vertices[j]
            if (u,v) in edges:
                clique_edges.append((u,v))
    clique_edges.sort()
    
    # Total weight
    total_weight_val = sum(weights[i] for i in clique_vertices)
    
    # Type distribution
    type_counts = {}
    for i in clique_vertices:
        t = types[i]
        type_counts[t] = type_counts.get(t, 0) + 1
    
    # Output
    print("STATUS: sat")
    print(f"clique: {clique_vertices}")
    print(f"clique_size: {clique_size_val}")
    print(f"clique_edges: {clique_edges}")
    print(f"clique_total_weight: {total_weight_val}")
    print(f"clique_type_distribution: {type_counts}")
elif result == unsat:
    print("STATUS: unsat")
    print("No clique satisfies constraints")
else:
    print("STATUS: unknown")