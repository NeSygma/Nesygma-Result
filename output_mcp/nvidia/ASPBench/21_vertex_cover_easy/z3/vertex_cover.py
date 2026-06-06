from z3 import *

edges = [(0,1),(0,2),(1,3),(2,3),(2,4),(3,5),(4,5),(1,5)]

# boolean var for each vertex
selected = [Bool(f"selected_{i}") for i in range(6)]

opt = Optimize()

# cover each edge
for u,v in edges:
    opt.add(Or(selected[u], selected[v]))

# objective: minimize number of selected vertices
opt.minimize(Sum([selected[i] for i in range(6)]))

# solve
result = opt.check()
if result == sat:
    m = opt.model()
    selected_vertices = [i for i in range(6) if m[selected[i]]]
    cover_size = len(selected_vertices)
    covered_edges = []
    for u,v in edges:
        if m[selected[u]] or m[selected[v]]:
            covered_edges.append([u,v])
    print("STATUS: sat")
    print("cover_size =", cover_size)
    print("vertex_cover =", selected_vertices)
    print("covered_edges =", covered_edges)
else:
    print("STATUS: unsat")