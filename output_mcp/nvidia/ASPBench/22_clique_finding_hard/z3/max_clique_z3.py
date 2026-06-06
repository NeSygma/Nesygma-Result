from z3 import *
from collections import defaultdict, Counter

# Data
vertices = range(20)
edges = [
    (0,1),(0,3),(0,4),(0,6),(0,7),(0,9),(0,10),
    (1,3),(1,4),(1,6),(1,7),(1,9),
    (2,5),(2,8),(2,11),(2,14),(2,17),(2,18),
    (3,4),(3,6),(3,7),(3,9),
    (4,6),(4,7),(4,9),
    (5,8),(5,11),(5,14),(5,17),(5,19),
    (6,7),(6,9),
    (7,9),
    (8,11),(8,14),(8,17),
    (11,14),(11,17),
    (12,13),
    (14,17),
    (15,16)
]

# Normalize edges to (u,v) with u<v
edge_set = set()
for u,v in edges:
    if u>v: u,v=v,u
    edge_set.add((u,v))

# Types and weights
type_of = {
    0:'alpha',1:'alpha',2:'alpha',3:'alpha',4:'beta',5:'alpha',6:'beta',7:'beta',8:'beta',9:'delta',10:'delta',
    11:'beta',12:'gamma',13:'gamma',14:'gamma',15:'delta',16:'delta',17:'gamma',18:'alpha',19:'beta'
}
weight = {
    0:20,1:20,2:15,3:20,4:30,5:15,6:30,7:30,8:18,9:10,10:10,11:12,12:25,13:25,14:20,15:5,16:5,17:19,18:40,19:40
}

# Boolean selectors
sel = [Bool(f'sel_{i}') for i in range(20)]

solver = Optimize()

# Clique property: no two selected vertices may be a non-edge
for i in range(20):
    for j in range(i+1,20):
        if (i,j) not in edge_set:
            solver.add(sel[i] + sel[j] <= 1)

# Type diversity: at most 2 per type
type_to_vertices = defaultdict(list)
for i,t in type_of.items():
    type_to_vertices[t].append(i)

for t,lst in type_to_vertices.items():
    solver.add(Sum([sel[v] for v in lst]) <= 2)

# Weight limit
solver.add(Sum([If(sel[i], weight[i], 0) for i in range(20)]) <= 100)

# Objective: maximize clique size
clique_size = Sum([sel[i] for i in range(20)])
solver.maximize(clique_size)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    clique = [i for i in range(20) if m[sel[i]]]
    clique.sort()
    # compute edges within clique
    clique_edges = [(clique[a], clique[b]) for a in range(len(clique)) for b in range(a+1, len(clique))
                    if (clique[a], clique[b]) in edge_set]
    clique_edges.sort()
    total_weight = sum(weight[i] for i in clique)
    type_dist = Counter(type_of[i] for i in clique)
    type_dist_items = sorted(type_dist.items())
    print("STATUS: sat")
    print(f"clique = {clique}")
    print(f"clique_size = {len(clique)}")
    print(f"clique_edges = {clique_edges}")
    print(f"clique_total_weight = {total_weight}")
    print(f"clique_type_distribution = {type_dist_items}")
else:
    print("STATUS: unsat")