from z3 import *

# Problem data
vertices = list(range(12))
# Levels
level = {0:2, 1:2, 2:1, 3:1, 4:1, 5:1, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}
# Resource costs
cost = {0:10, 1:10, 2:8, 3:5, 4:7, 5:6, 6:2, 7:2, 8:3, 9:3, 10:4, 11:4}
# Edges: (u,v,weight,type)
edges = [
    (0,2,5,'fiber'),
    (1,3,4,'fiber'),
    (2,3,3,'fiber'),
    (2,4,6,'copper'),
    (2,6,2,'copper'),
    (3,5,2,'fiber'),
    (3,7,8,'copper'),
    (4,8,5,'fiber'),
    (5,9,4,'copper'),
    (5,10,3,'fiber'),
    (6,7,1,'copper'),
    (9,10,7,'fiber'),
    (10,11,2,'copper')
]
# Terminal groups
terminals = {
    'A': [6,7],
    'B': [10,11]
}
# All terminals set
all_terminals = set()
for group in terminals.values():
    all_terminals.update(group)

# Helper: terminal boolean array
is_terminal = {v: (v in all_terminals) for v in vertices}

# Solver
opt = Optimize()

# Variables
in_tree = {v: Bool(f'in_tree_{v}') for v in vertices}
edge_in = [Bool(f'edge_in_{i}') for i in range(len(edges))]
# Flow variables for directed edges
flow = {}
for i,(u,v,w,t) in enumerate(edges):
    flow[(u,v)] = Int(f'flow_{u}_{v}')
    flow[(v,u)] = Int(f'flow_{v}_{u}')

# Root (choose terminal 6)
root = 6

# Constraints
# Terminals must be in tree and leaves
for t in all_terminals:
    opt.add(in_tree[t] == True)
    # degree 1 constraint
    incident_edges = [i for i,(u,v,w,tt) in enumerate(edges) if t in (u,v)]
    opt.add(Sum([If(edge_in[i], 1, 0) for i in incident_edges]) == 1)

# Root in tree
opt.add(in_tree[root] == True)

# Edge implies both endpoints in tree
for i,(u,v,w,tt) in enumerate(edges):
    opt.add(Implies(edge_in[i], And(in_tree[u], in_tree[v])))

# Flow constraints: flow <= edge_in, flow <= 1, flow >= 0, flow sum == edge_in
for i,(u,v,w,tt) in enumerate(edges):
    opt.add(flow[(u,v)] <= If(edge_in[i], 1, 0))
    opt.add(flow[(v,u)] <= If(edge_in[i], 1, 0))
    opt.add(flow[(u,v)] >= 0)
    opt.add(flow[(v,u)] >= 0)
    opt.add(flow[(u,v)] <= 1)
    opt.add(flow[(v,u)] <= 1)
    opt.add(flow[(u,v)] + flow[(v,u)] == If(edge_in[i], 1, 0))

# Total vertices in tree
total_vertices_in_tree = Sum([If(in_tree[v], 1, 0) for v in vertices])

# Flow conservation
# Root: no incoming, outgoing = total_vertices_in_tree - 1
opt.add(Sum([flow[(root,v)] for v in vertices if (root,v) in flow]) == total_vertices_in_tree - 1)
opt.add(Sum([flow[(u,root)] for u in vertices if (u,root) in flow]) == 0)
# Other vertices: incoming flow = 1 if in_tree, else 0
for v in vertices:
    if v == root:
        continue
    opt.add(Sum([flow[(u,v)] for u in vertices if (u,v) in flow]) == If(in_tree[v], 1, 0))

# Hierarchy constraint: if a Steiner vertex is used, it cannot connect to a higher level vertex
for i,(u,v,w,tt) in enumerate(edges):
    # u is Steiner
    opt.add(Implies(And(edge_in[i], in_tree[u], Not(is_terminal[u]), level[u] < level[v]), Not(edge_in[i])))
    # v is Steiner
    opt.add(Implies(And(edge_in[i], in_tree[v], Not(is_terminal[v]), level[v] < level[u]), Not(edge_in[i])))

# Resource budget for Steiner vertices
steiner_cost = Sum([If(And(in_tree[v], Not(is_terminal[v])), cost[v], 0) for v in vertices])
opt.add(steiner_cost <= 20)

# Copper edge limit
copper_edges = Sum([If(And(edge_in[i], edges[i][3] == 'copper'), 1, 0) for i in range(len(edges))])
opt.add(copper_edges <= 3)

# Gateway requirement: each group must have at least one gateway
for group_name, group_vertices in terminals.items():
    gateway_candidates = []
    for v in vertices:
        if is_terminal[v]:
            continue
        # v must be in tree and not terminal
        # and must have an incident edge to a terminal in this group
        incident_to_group = []
        for i,(u,wgt,wt,tt) in enumerate(edges):
            if v == u and wgt in group_vertices:
                incident_to_group.append(edge_in[i])
            if v == wgt and u in group_vertices:
                incident_to_group.append(edge_in[i])
        if incident_to_group:
            gateway_candidates.append(And(in_tree[v], Not(is_terminal[v]), Or(incident_to_group)))
    # At least one gateway
    opt.add(Or(gateway_candidates))

# Objective: minimize total weight
total_weight = Sum([If(edge_in[i], edges[i][2], 0) for i in range(len(edges))])
opt.minimize(total_weight)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    # Extract solution
    used_edges = []
    for i,(u,v,w,tt) in enumerate(edges):
        if is_true(m[edge_in[i]]):
            used_edges.append((u,v,w))
    print("total_weight =", m.evaluate(total_weight))
    print("tree_edges =", used_edges)
    steiner_vertices = [v for v in vertices if is_true(m[in_tree[v]]) and not is_terminal[v]]
    print("steiner_vertices =", steiner_vertices)
    print("terminals =", terminals)
    # Gateways per group
    gateways = {}
    for group_name, group_vertices in terminals.items():
        gw = []
        for v in steiner_vertices:
            for i,(u,wgt,wt,tt) in enumerate(edges):
                if (v == u and wgt in group_vertices) or (v == wgt and u in group_vertices):
                    if is_true(m[edge_in[i]]):
                        gw.append(v)
                        break
        gateways[group_name] = gw
    print("gateways =", gateways)
    print("copper_edge_count =", m.evaluate(copper_edges))
    print("steiner_resource_cost =", m.evaluate(steiner_cost))
    comp = [v for v in vertices if is_true(m[in_tree[v]])]
    print("connected_components =", [comp])
else:
    print("STATUS: unsat")
    if True:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")