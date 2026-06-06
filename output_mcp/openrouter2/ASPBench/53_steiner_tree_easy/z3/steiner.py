from z3 import *

# Define graph edges: (u, v, weight)
edges = [
    (0,1,3), (0,2,5), (1,3,2), (1,4,4), (2,3,1), (2,5,6),
    (3,4,3), (3,5,3), (3,6,2), (4,5,2), (5,6,4)
]

num_edges = len(edges)
# Binary variable for each undirected edge
x = [Int(f"x_{i}") for i in range(num_edges)]

# Directed edges list: (u, v, weight, undirected_index)
directed_edges = []
for idx, (u,v,w) in enumerate(edges):
    directed_edges.append((u,v,w,idx))
    directed_edges.append((v,u,w,idx))

# Terminals and root
terminals = [0,5,6]
root = 0
other_terminals = [t for t in terminals if t != root]

# Flow variables: f_{u}_{v}_{t}
flow = {}
for (u,v,w,idx) in directed_edges:
    for t in other_terminals:
        flow[(u,v,t)] = Int(f"f_{u}_{v}_{t}")

solver = Optimize()

# Binary constraints for x
for xi in x:
    solver.add(xi >= 0, xi <= 1)

# Flow bounds and relation to x
for (u,v,w,idx) in directed_edges:
    for t in other_terminals:
        fuvt = flow[(u,v,t)]
        solver.add(fuvt >= 0, fuvt <= 1)
        # f <= x
        solver.add(fuvt <= x[idx])

# Flow conservation for each terminal t
for t in other_terminals:
    for v in set([u for (u,v,w,idx) in directed_edges] + [v for (u,v,w,idx) in directed_edges]):
        inflow = Sum([flow[(u,v,t)] for (u,v,w,idx) in directed_edges if v == v])
        outflow = Sum([flow[(v,w,t)] for (u,v,w,idx) in directed_edges if u == v])
        if v == root:
            solver.add(outflow - inflow == 1)
        elif v == t:
            solver.add(inflow - outflow == 1)
        else:
            solver.add(inflow - outflow == 0)

# Objective: minimize total weight of selected edges
objective = Sum([x[i] * edges[i][2] for i in range(num_edges)])
solver.minimize(objective)

# Check and get model
result = solver.check()
if result == sat:
    model = solver.model()
    # Compute total weight
    total_weight = sum(model[x[i]].as_long() * edges[i][2] for i in range(num_edges))
    # Tree edges
    tree_edges = []
    for i in range(num_edges):
        if model[x[i]].as_long() == 1:
            tree_edges.append((edges[i][0], edges[i][1]))
    # Steiner vertices
    steiner_vertices = set()
    for (u,v) in tree_edges:
        if u not in terminals:
            steiner_vertices.add(u)
        if v not in terminals:
            steiner_vertices.add(v)
    steiner_vertices = sorted(list(steiner_vertices))
    # Connected components via union-find
    parent = {}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a,b):
        pa, pb = find(a), find(b)
        if pa != pb:
            parent[pb] = pa
    # Initialize parent for vertices in tree
    vertices_in_tree = set()
    for (u,v) in tree_edges:
        vertices_in_tree.add(u)
        vertices_in_tree.add(v)
    for v in vertices_in_tree:
        parent[v] = v
    for (u,v) in tree_edges:
        union(u,v)
    components = {}
    for v in vertices_in_tree:
        rootv = find(v)
        components.setdefault(rootv, []).append(v)
    connected_components = list(components.values())
    # Print results
    print("STATUS: sat")
    print(f"total_weight = {total_weight}")
    print(f"tree_edges = {tree_edges}")
    print(f"steiner_vertices = {steiner_vertices}")
    print(f"terminals = {terminals}")
    print(f"connected_components = {connected_components}")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")