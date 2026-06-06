from z3 import *

vertices = [0,1,2,3,4,5,6]
edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(1,4),(2,3),(2,5),(3,4),(3,5),(4,5),(4,6),(5,6)]

# adjacency set
adj = {i:set() for i in vertices}
for u,v in edges:
    adj[u].add(v)
    adj[v].add(u)

# boolean selector for each vertex
sel = [Bool(f"sel_{i}") for i in vertices]

solver = Optimize()

# add constraints: no non-edge can be simultaneously selected
for i in vertices:
    for j in vertices:
        if i < j and j not in adj[i]:
            # cannot select both i and j
            solver.add(Or(Not(sel[i]), Not(sel[j])))

# objective: maximize number of selected vertices
solver.maximize(Sum([If(sel[i], 1, 0) for i in vertices]))

# solve
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # collect selected vertices
    selected = [i for i in vertices if model[sel[i]]]
    print("selected_vertices =", selected)
    print("max_clique_size =", len(selected))
    # optionally print the clique edges
    clique_edges = []
    for u in selected:
        for v in selected:
            if u < v and v in adj[u]:
                clique_edges.append((u,v))
    print("clique_edges =", clique_edges)
else:
    print("STATUS: unsat")