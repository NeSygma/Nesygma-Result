from z3 import *

# ============================================================
# Instance Data
# ============================================================
num_vertices = 12
vertices = list(range(num_vertices))

# Vertex levels
level = {0: 2, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}

# Vertex resource costs
cost = {0: 10, 1: 10, 2: 8, 3: 5, 4: 7, 5: 6, 6: 2, 7: 2, 8: 3, 9: 3, 10: 4, 11: 4}

# Edges: (u, v, weight, type)
edges_data = [
    (0, 2, 5, 'fiber'),
    (1, 3, 4, 'fiber'),
    (2, 3, 3, 'fiber'),
    (2, 4, 6, 'copper'),
    (2, 6, 2, 'copper'),
    (3, 5, 2, 'fiber'),
    (3, 7, 8, 'copper'),
    (4, 8, 5, 'fiber'),
    (5, 9, 4, 'copper'),
    (5, 10, 3, 'fiber'),
    (6, 7, 1, 'copper'),
    (9, 10, 7, 'fiber'),
    (10, 11, 2, 'copper'),
]
num_edges = len(edges_data)

# Terminal groups
group_A = [6, 7]
group_B = [10, 11]
all_terminals = set(group_A + group_B)

# Constraints
resource_budget = 20
copper_limit = 3

# Build adjacency list for quick lookup
adj = {v: [] for v in vertices}
for i, (u, v, w, etype) in enumerate(edges_data):
    adj[u].append((v, i))
    adj[v].append((u, i))

# ============================================================
# Z3 Model
# ============================================================
opt = Optimize()

# --- Decision Variables ---
in_tree = {v: Bool(f'in_tree_{v}') for v in vertices}
edge_sel = {i: Bool(f'edge_{i}') for i in range(num_edges)}

# --- Basic Constraints ---
# All terminals must be in the tree
for t in all_terminals:
    opt.add(in_tree[t] == True)

# An edge can only be selected if both endpoints are in the tree
for i, (u, v, w, etype) in enumerate(edges_data):
    opt.add(Implies(edge_sel[i], And(in_tree[u], in_tree[v])))

# --- Hierarchy Constraint ---
# A Steiner vertex at level L cannot connect to a vertex at level > L
for i, (u, v, w, etype) in enumerate(edges_data):
    if u not in all_terminals and level[u] < level[v]:
        opt.add(Not(edge_sel[i]))
    if v not in all_terminals and level[v] < level[u]:
        opt.add(Not(edge_sel[i]))

# --- Resource Budget ---
steiner_vertices = [v for v in vertices if v not in all_terminals]
opt.add(Sum([If(in_tree[v], cost[v], 0) for v in steiner_vertices]) <= resource_budget)

# --- Copper Edge Limit ---
copper_edges = [i for i, (_, _, _, etype) in enumerate(edges_data) if etype == 'copper']
opt.add(Sum([If(edge_sel[i], 1, 0) for i in copper_edges]) <= copper_limit)

# --- Tree Structure: edges = vertices - 1 ---
n_selected = Sum([If(in_tree[v], 1, 0) for v in vertices])
n_edges_selected = Sum([If(edge_sel[i], 1, 0) for i in range(num_edges)])
opt.add(n_edges_selected == n_selected - 1)

# --- Connectivity via flow from root (vertex 6) ---
root = 6
flow_fwd = {i: Int(f'flow_fwd_{i}') for i in range(num_edges)}
flow_bwd = {i: Int(f'flow_bwd_{i}') for i in range(num_edges)}

for i in range(num_edges):
    opt.add(flow_fwd[i] >= 0, flow_bwd[i] >= 0)
    opt.add(Implies(Not(edge_sel[i]), And(flow_fwd[i] == 0, flow_bwd[i] == 0)))
    opt.add(flow_fwd[i] <= num_vertices, flow_bwd[i] <= num_vertices)

for v in vertices:
    incoming = []
    outgoing = []
    for i, (u, w_v, _, _) in enumerate(edges_data):
        if u == v:
            incoming.append(flow_bwd[i])
            outgoing.append(flow_fwd[i])
        elif w_v == v:
            incoming.append(flow_fwd[i])
            outgoing.append(flow_bwd[i])
    
    net_in = Sum(incoming) - Sum(outgoing)
    
    if v == root:
        opt.add(net_in == -(n_selected - 1))
    else:
        opt.add(Implies(in_tree[v], net_in == 1))
        opt.add(Implies(Not(in_tree[v]), net_in == 0))

# --- Gateway Requirement ---
gw_A = {v: Bool(f'gw_A_{v}') for v in vertices}
gw_B = {v: Bool(f'gw_B_{v}') for v in vertices}

for v in vertices:
    if v in all_terminals:
        opt.add(gw_A[v] == False)
        opt.add(gw_B[v] == False)
    else:
        opt.add(Implies(gw_A[v], in_tree[v]))
        opt.add(Implies(gw_B[v], in_tree[v]))
    
    # Gateway for A: must have an edge to a terminal in group A
    edges_to_A = []
    for i, (u, w_v, _, _) in enumerate(edges_data):
        if u == v and w_v in group_A:
            edges_to_A.append(edge_sel[i])
        elif w_v == v and u in group_A:
            edges_to_A.append(edge_sel[i])
    
    if edges_to_A:
        opt.add(Implies(gw_A[v], Or(edges_to_A)))
    else:
        opt.add(gw_A[v] == False)
    
    # Gateway for B: must have an edge to a terminal in group B
    edges_to_B = []
    for i, (u, w_v, _, _) in enumerate(edges_data):
        if u == v and w_v in group_B:
            edges_to_B.append(edge_sel[i])
        elif w_v == v and u in group_B:
            edges_to_B.append(edge_sel[i])
    
    if edges_to_B:
        opt.add(Implies(gw_B[v], Or(edges_to_B)))
    else:
        opt.add(gw_B[v] == False)

# At least one gateway per group
opt.add(Or([gw_A[v] for v in vertices]))
opt.add(Or([gw_B[v] for v in vertices]))

# --- Gateway Connectivity ---
# All gateways must be connected through Steiner-only paths.
# We use a second flow network on Steiner vertices only.
# We pick a "virtual root" among Steiner vertices and ensure all gateways are reachable.

# Identify Steiner-only edges (both endpoints are Steiner and in tree)
steiner_edge = {i: Bool(f'steiner_edge_{i}') for i in range(num_edges)}
for i, (u, v, _, _) in enumerate(edges_data):
    u_is_steiner = u not in all_terminals
    v_is_steiner = v not in all_terminals
    if u_is_steiner and v_is_steiner:
        opt.add(steiner_edge[i] == edge_sel[i])
    else:
        opt.add(steiner_edge[i] == False)

# Steiner connectivity flow
# We need all gateways connected. Let's use a flow from a designated Steiner root.
# We'll try vertex 2 as the Steiner root (it's at level 1, connects to many things).
# But we need to handle the case where vertex 2 is not in tree.
# 
# Better: use a virtual super-source. Create a virtual node connected to all gateways.
# Then ensure all gateways are reachable from each other.
#
# Simplest: for each pair of gateways, ensure connectivity. But that's O(n^2).
# 
# Alternative: ensure the Steiner subgraph is connected by using flow from one gateway.
# We'll pick the gateway with the lowest index as the Steiner root.
# 
# Actually, let's use a different approach: 
# For each gateway g, there must be a path from g to some "central" Steiner vertex
# using only Steiner edges. If all gateways can reach the same central vertex, they're connected.
#
# We'll use vertex 2 or 3 as the central Steiner vertex (whichever is in tree).
# Let's use a conditional approach.

# Let's define: steiner_root is the Steiner vertex with the smallest index that is in tree.
# We'll use a flow from this root to all gateways.

# For simplicity, let's just ensure that for each gateway, there's a Steiner-only path
# to some other gateway. We'll use a flow model.

# Create Steiner flow variables
sflow_fwd = {i: Int(f'sflow_fwd_{i}') for i in range(num_edges)}
sflow_bwd = {i: Int(f'sflow_bwd_{i}') for i in range(num_edges)}

for i in range(num_edges):
    opt.add(sflow_fwd[i] >= 0, sflow_bwd[i] >= 0)
    opt.add(Implies(Not(steiner_edge[i]), And(sflow_fwd[i] == 0, sflow_bwd[i] == 0)))
    opt.add(sflow_fwd[i] <= num_vertices, sflow_bwd[i] <= num_vertices)

# Count gateways
n_gateways = Sum([If(Or(gw_A[v], gw_B[v]), 1, 0) for v in vertices])

# For each Steiner vertex, compute net Steiner flow
for v in vertices:
    if v in all_terminals:
        # Terminals don't participate in Steiner flow
        continue
    
    incoming_s = []
    outgoing_s = []
    for i, (u, w_v, _, _) in enumerate(edges_data):
        if u == v:
            incoming_s.append(sflow_bwd[i])
            outgoing_s.append(sflow_fwd[i])
        elif w_v == v:
            incoming_s.append(sflow_fwd[i])
            outgoing_s.append(sflow_bwd[i])
    
    net_in_s = Sum(incoming_s) - Sum(outgoing_s)
    
    # If v is a gateway, it's a source/sink in the Steiner flow
    is_gw = Or(gw_A[v], gw_B[v])
    
    # One gateway is the root (supplies flow), others consume
    # We'll use: if v is the "first" gateway (lowest index), it supplies; others consume
    # But we don't know which is first. Let's use a different approach.
    
    # Use: each gateway has net flow = -(n_gateways - 1) if it's the root, or 1 if it's a non-root gateway
    # We need exactly one root gateway.
    
    # Let's define is_gw_root[v]
    is_gw_root = Bool(f'is_gw_root_{v}')
    opt.add(Implies(is_gw_root, is_gw))
    opt.add(Implies(Not(in_tree[v]), Not(is_gw_root)))
    
    # Net flow: root supplies (n_gateways - 1), non-root gateways consume 1, non-gateways consume 0
    opt.add(Implies(And(in_tree[v], Not(all_terminals.__contains__(v)), is_gw_root), 
                    net_in_s == -(n_gateways - 1)))
    opt.add(Implies(And(in_tree[v], Not(all_terminals.__contains__(v)), is_gw, Not(is_gw_root)), 
                    net_in_s == 1))
    opt.add(Implies(And(in_tree[v], Not(all_terminals.__contains__(v)), Not(is_gw)), 
                    net_in_s == 0))
    opt.add(Implies(Not(in_tree[v]), net_in_s == 0))

# Exactly one gateway root
opt.add(Sum([If(Bool(f'is_gw_root_{v}'), 1, 0) for v in steiner_vertices]) == 1)

# --- Objective: Minimize total edge weight ---
total_weight = Sum([If(edge_sel[i], edges_data[i][2], 0) for i in range(num_edges)])
opt.minimize(total_weight)

# ============================================================
# Solve
# ============================================================
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    
    selected_edges = []
    total_w = 0
    copper_count = 0
    for i, (u, v, w, etype) in enumerate(edges_data):
        if m.evaluate(edge_sel[i], model_completion=True):
            selected_edges.append((u, v, w, etype))
            total_w += w
            if etype == 'copper':
                copper_count += 1
    
    tree_verts = [v for v in vertices if m.evaluate(in_tree[v], model_completion=True)]
    steiner_in_tree = [v for v in tree_verts if v not in all_terminals]
    steiner_cost = sum(cost[v] for v in steiner_in_tree)
    
    gateways_A = [v for v in vertices if v not in all_terminals and m.evaluate(gw_A[v], model_completion=True)]
    gateways_B = [v for v in vertices if v not in all_terminals and m.evaluate(gw_B[v], model_completion=True)]
    
    print("STATUS: sat")
    print(f"total_weight: {total_w}")
    print(f"tree_edges: {[(u, v, w) for u, v, w, _ in selected_edges]}")
    print(f"steiner_vertices: {steiner_in_tree}")
    print(f"terminals: {{'A': {group_A}, 'B': {group_B}}}")
    print(f"gateways: {{'A': {gateways_A}, 'B': {gateways_B}}}")
    print(f"copper_edge_count: {copper_count}")
    print(f"steiner_resource_cost: {steiner_cost}")
    print(f"vertices_in_tree: {tree_verts}")
    print(f"edge_details: {selected_edges}")
    
    print(f"\nVerification:")
    print(f"  Edges selected: {len(selected_edges)}")
    print(f"  Vertices in tree: {len(tree_verts)}")
    print(f"  Expected edges (V-1): {len(tree_verts) - 1}")
    print(f"  Total weight: {total_w}")
    print(f"  Copper edges: {copper_count} (limit: {copper_limit})")
    print(f"  Steiner cost: {steiner_cost} (budget: {resource_budget})")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")