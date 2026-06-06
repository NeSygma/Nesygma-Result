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

# ============================================================
# Z3 Model
# ============================================================
opt = Optimize()

# --- Decision Variables ---

# Vertex inclusion: True if vertex is in the tree
in_tree = [Bool(f'in_tree_{v}') for v in vertices]

# Edge selection: True if edge is in the tree
edge_sel = [Bool(f'edge_{i}') for i in range(num_edges)]

# --- Basic Constraints ---

# All terminals must be in the tree
for t in all_terminals:
    opt.add(in_tree[t] == True)

# An edge can only be selected if both endpoints are in the tree
for i, (u, v, w, etype) in enumerate(edges_data):
    opt.add(Implies(edge_sel[i], And(in_tree[u], in_tree[v])))

# --- Hierarchy Constraint ---
# A Steiner vertex at level L cannot connect to a vertex at level > L
# This means: if edge (u,v) is selected, then neither endpoint can be a Steiner vertex
# at a lower level than the other endpoint.
# More precisely: if u is Steiner (not terminal) and level[u] < level[v], edge (u,v) cannot be used.
# Similarly for v.
for i, (u, v, w, etype) in enumerate(edges_data):
    # If u is a Steiner vertex and level[u] < level[v], edge cannot be selected
    if u not in all_terminals and level[u] < level[v]:
        opt.add(Not(edge_sel[i]))
    # If v is a Steiner vertex and level[v] < level[u], edge cannot be selected
    if v not in all_terminals and level[v] < level[u]:
        opt.add(Not(edge_sel[i]))

# --- Resource Budget ---
# Sum of resource costs for all Steiner vertices in tree <= 20
steiner_vertices = [v for v in vertices if v not in all_terminals]
opt.add(Sum([If(in_tree[v], cost[v], 0) for v in steiner_vertices]) <= resource_budget)

# --- Copper Edge Limit ---
copper_edges = [i for i, (_, _, _, etype) in enumerate(edges_data) if etype == 'copper']
opt.add(Sum([If(edge_sel[i], 1, 0) for i in copper_edges]) <= copper_limit)

# --- Tree Structure (Connectivity + Acyclicity) ---
# We use a flow-based approach: pick a root, ensure every selected vertex has exactly one
# parent edge (except root), and all selected vertices are reachable.
# Root: pick vertex 0 if in tree, else some other. We'll use a symbolic root approach.
# Actually, let's use a simpler approach: 
# For a tree with N selected vertices, we need exactly N-1 edges, and the graph is connected.
# We enforce connectivity via a flow model.

# Number of selected vertices
n_selected = Sum([If(in_tree[v], 1, 0) for v in vertices])
n_edges_selected = Sum([If(edge_sel[i], 1, 0) for i in range(num_edges)])

# Tree property: edges = vertices - 1
opt.add(n_edges_selected == n_selected - 1)

# Connectivity via flow: pick a root among selected vertices.
# We'll use vertex 6 (a terminal) as the root since it must be in the tree.
root = 6

# For each selected vertex v != root, there must be a flow of 1 from root to v.
# We model flow on each edge (bidirectional since undirected).
# flow_fwd[i] = flow from u to v on edge i
# flow_bwd[i] = flow from v to u on edge i
flow_fwd = [Int(f'flow_fwd_{i}') for i in range(num_edges)]
flow_bwd = [Int(f'flow_bwd_{i}') for i in range(num_edges)]

for i in range(num_edges):
    opt.add(flow_fwd[i] >= 0)
    opt.add(flow_bwd[i] >= 0)
    # Flow only on selected edges
    opt.add(Implies(Not(edge_sel[i]), And(flow_fwd[i] == 0, flow_bwd[i] == 0)))
    # Flow bounded by number of selected vertices (upper bound)
    opt.add(flow_fwd[i] <= num_vertices)
    opt.add(flow_bwd[i] <= num_vertices)

# Net flow at each vertex
for v in vertices:
    # Incoming flow: sum of flow from edges where v is destination
    incoming = []
    outgoing = []
    for i, (u, w_v, _, _) in enumerate(edges_data):
        if u == v:
            incoming.append(flow_bwd[i])  # flow from w_v to u=v
            outgoing.append(flow_fwd[i])  # flow from u=v to w_v
        elif w_v == v:
            incoming.append(flow_fwd[i])  # flow from u to v
            outgoing.append(flow_bwd[i])  # flow from v to u
    
    net_in = Sum(incoming) - Sum(outgoing)
    
    if v == root:
        # Root supplies flow to all other selected vertices
        opt.add(net_in == -(n_selected - 1))
    else:
        # Each non-root selected vertex consumes 1 unit
        opt.add(Implies(in_tree[v], net_in == 1))
        opt.add(Implies(Not(in_tree[v]), net_in == 0))

# --- Gateway Requirement ---
# For each terminal group, at least one Steiner vertex must connect directly to a terminal in that group.
# A gateway for group A: a Steiner vertex in the tree that has an edge to at least one terminal in group A.
# Similarly for group B.

# Gateway variables
gw_A = [Bool(f'gw_A_{v}') for v in vertices]  # v is a gateway for group A
gw_B = [Bool(f'gw_B_{v}') for v in vertices]  # v is a gateway for group B

for v in vertices:
    # A gateway must be a Steiner vertex in the tree
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
        # If v is in tree, Steiner, and connected to a terminal in A, it could be a gateway
        # (but we don't force it to be one - we just need at least one)
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
# All gateway vertices must be connected to each other through a path that only uses Steiner vertices.
# This means: the subgraph induced by Steiner vertices in the tree must connect all gateways.
# We enforce this by: for each pair of gateways, there exists a path through Steiner vertices.
# 
# Simpler approach: the Steiner subgraph (vertices that are Steiner and in tree) must be connected,
# and all gateways are part of it. Since gateways are Steiner vertices, if the Steiner subgraph
# is connected, all gateways are connected through Steiner vertices.
#
# Actually, we need: all gateways connected through Steiner-only paths. 
# The Steiner vertices in the tree form a subgraph. We need this subgraph to be connected
# (at least the part containing gateways).
#
# We can enforce this with another flow model on the Steiner subgraph.
# Pick one gateway as root (say the first one found), and ensure all other gateways
# can be reached via Steiner-only edges.

# We need to identify which edges connect two Steiner vertices (both in tree)
# steiner_edge[i] = True if edge i connects two Steiner vertices both in tree
steiner_edge = [Bool(f'steiner_edge_{i}') for i in range(num_edges)]
for i, (u, v, _, _) in enumerate(edges_data):
    opt.add(steiner_edge[i] == And(edge_sel[i], 
                                    Not(BoolVal(u in all_terminals)), 
                                    Not(BoolVal(v in all_terminals))))

# Gateway connectivity via flow on Steiner subgraph
# We'll use a symbolic approach: pick a "gateway root" and ensure connectivity
# Since we don't know which vertices are gateways, we'll use a different approach:
# 
# For each pair of gateways (g1, g2), there must be a path through Steiner vertices.
# This is complex. Instead, let's ensure the Steiner subgraph is connected.
# 
# Alternative simpler approach: use a second flow network on Steiner vertices only.
# Pick vertex 2 as the Steiner root (it's a Steiner vertex that could connect things).
# But we don't know if it's in the tree. Let's use a different approach.
#
# We'll add flow variables for Steiner connectivity and ensure all gateways have flow.

# Actually, let's simplify: we'll check gateway connectivity post-hoc or use a 
# constraint that for each gateway, there's a path to some "central" Steiner vertex.
# 
# Let's use: pick a designated Steiner root (we'll try vertex 2 or 3).
# For each gateway g, there must be a path from the Steiner root to g using only Steiner edges.
# If the Steiner root is not in tree, we need another approach.
#
# Better: use a universal flow approach. Create a virtual super-source connected to all gateways
# for group A, and ensure all gateways for group B are reachable via Steiner-only paths.
#
# Simplest correct approach: ensure the Steiner-induced subgraph is connected.
# We do this by: for each Steiner vertex in the tree, it must be reachable from 
# some fixed Steiner vertex via Steiner-only edges.

# Let's pick the Steiner vertex with the lowest index that's in the tree.
# We'll use a conditional root approach.

# For simplicity and correctness, let's use a different strategy:
# Add flow variables for Steiner-only connectivity.
# Root = first Steiner vertex in tree (we'll try each and use implications).

# Actually, let's just use a direct approach:
# For each pair of gateways, encode that they're connected via Steiner path.
# With at most ~6 Steiner vertices, this is manageable.

# Let's use a Steiner connectivity flow with a fixed root.
# We'll try vertex 2 as the Steiner root. If it's not in tree, the constraint is vacuous
# for flow, but we need to handle it.

# Better approach: use a spanning tree on Steiner vertices.
# For each Steiner vertex v in tree (v != some root), it has exactly one "parent" 
# Steiner vertex connected by a Steiner edge.

# Let's use parent variables for Steiner vertices
steiner_verts_list = [v for v in vertices if v not in all_terminals]

# For each Steiner vertex, define a parent (another Steiner vertex or -1 if root)
parent = [Int(f'parent_{v}') for v in steiner_verts_list]
is_steiner_root = [Bool(f'is_steiner_root_{v}') for v in steiner_verts_list]

for idx, v in enumerate(steiner_verts_list):
    opt.add(parent[v] >= -1)
    opt.add(parent[v] < num_vertices)
    
    # If not in tree, parent is -1 and not root
    opt.add(Implies(Not(in_tree[v]), And(parent[v] == -1, Not(is_steiner_root[v]))))
    
    # If in tree, either it's the root (parent = -1) or parent is another Steiner vertex in tree
    # Exactly one root among Steiner vertices in tree
    # Parent must be a Steiner vertex that is in tree and connected by an edge
    
    # Parent must be a valid Steiner vertex
    for p_val in steiner_verts_list:
        if p_val != v:
            # Check if there's an edge between v and p_val
            has_edge = False
            for i, (u, w_v, _, _) in enumerate(edges_data):
                if (u == v and w_v == p_val) or (u == p_val and w_v == v):
                    has_edge = True
                    opt.add(Implies(And(in_tree[v], Not(is_steiner_root[v]), parent[v] == p_val),
                                   And(in_tree[p_val], edge_sel[i])))
            if not has_edge:
                opt.add(Implies(in_tree[v], parent[v] != p_val))
    
    # If in tree and not root, parent must be one of the valid Steiner neighbors
    valid_parents = []
    for p_val in steiner_verts_list:
        if p_val != v:
            for i, (u, w_v, _, _) in enumerate(edges_data):
                if (u == v and w_v == p_val) or (u == p_val and w_v == v):
                    valid_parents.append(p_val)
                    break
    if valid_parents:
        opt.add(Implies(And(in_tree[v], Not(is_steiner_root[v])), 
                        Or([parent[v] == p for p in valid_parents])))
    else:
        # No valid Steiner neighbors -> must be root if in tree
        opt.add(Implies(in_tree[v], is_steiner_root[v]))

# Exactly one Steiner root among Steiner vertices in tree
opt.add(Sum([If(And(in_tree[v], is_steiner_root[v]), 1, 0) for v in steiner_verts_list]) == 1)

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
    
    # Extract solution
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
    
    # Verify tree property
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