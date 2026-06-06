from z3 import *

# Problem data
n = 20
vertices = list(range(n))
# Types and weights
vertex_type = {
    0: 'alpha', 1: 'alpha', 2: 'alpha', 3: 'alpha', 4: 'beta', 5: 'alpha', 6: 'beta', 7: 'beta', 8: 'beta', 9: 'delta',
    10: 'delta', 11: 'beta', 12: 'gamma', 13: 'gamma', 14: 'gamma', 15: 'delta', 16: 'delta', 17: 'gamma', 18: 'alpha', 19: 'beta'
}
vertex_weight = {
    0: 20, 1: 20, 2: 15, 3: 20, 4: 30, 5: 15, 6: 30, 7: 30, 8: 18, 9: 10,
    10: 10, 11: 12, 12: 25, 13: 25, 14: 20, 15: 5, 16: 5, 17: 19, 18: 40, 19: 40
}
# Edge list
edge_list = [
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
]
# Build set of undirected edges for quick lookup
edge_set = set()
for u,v in edge_list:
    if u>v: u,v=v,u
    edge_set.add((u,v))

# Solver
opt = Optimize()
# Variables: x_i indicates if vertex i is in clique
x = [Int(f'x_{i}') for i in vertices]
for xi in x:
    opt.add(xi >= 0, xi <= 1)

# Clique property: for any non-edge pair, cannot both be selected
for i in range(n):
    for j in range(i+1, n):
        if (i,j) not in edge_set:
            opt.add(x[i] + x[j] <= 1)

# Type diversity: at most 2 per type
from collections import defaultdict
vertices_by_type = defaultdict(list)
for v in vertices:
    vertices_by_type[vertex_type[v]].append(v)
for t, verts in vertices_by_type.items():
    opt.add(Sum([x[v] for v in verts]) <= 2)

# Weight limit
opt.add(Sum([x[i]*vertex_weight[i] for i in vertices]) <= 100)

# Objective: maximize clique size
opt.maximize(Sum(x))

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    clique = [i for i in vertices if is_true(model[x[i]])]
    clique_size = len(clique)
    # Compute clique edges
    clique_edges = []
    for i in range(len(clique)):
        for j in range(i+1, len(clique)):
            u, v = clique[i], clique[j]
            if u>v: u,v=v,u
            if (u,v) in edge_set:
                clique_edges.append((u,v))
    clique_edges.sort()
    clique_total_weight = sum(vertex_weight[i] for i in clique)
    clique_type_distribution = {t: sum(1 for v in clique if vertex_type[v]==t) for t in vertices_by_type}
    # Output
    print("STATUS: sat")
    print("clique:", clique)
    print("clique_size:", clique_size)
    print("clique_edges:", clique_edges)
    print("clique_total_weight:", clique_total_weight)
    print("clique_type_distribution:", clique_type_distribution)
else:
    print("STATUS: unsat")
    if result == unknown:
        print("STATUS: unknown")