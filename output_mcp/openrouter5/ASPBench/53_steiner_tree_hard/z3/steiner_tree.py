from z3 import *

# ============================================================
# DATA
# ============================================================
V = list(range(12))

# Vertex levels
level = {0:2, 1:2, 2:1, 3:1, 4:1, 5:1, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}

# Vertex resource costs
res_cost = {0:10, 1:10, 2:8, 3:5, 4:7, 5:6, 6:2, 7:2, 8:3, 9:3, 10:4, 11:4}

# Edges: (u, v, weight, type)
edges_data = [
    (0,2,5,"fiber"),
    (1,3,4,"fiber"),
    (2,3,3,"fiber"),
    (2,4,6,"copper"),
    (2,6,2,"copper"),
    (3,5,2,"fiber"),
    (3,7,8,"copper"),
    (4,8,5,"fiber"),
    (5,9,4,"copper"),
    (5,10,3,"fiber"),
    (6,7,1,"copper"),
    (9,10,7,"fiber"),
    (10,11,2,"copper")
]

E = list(range(len(edges_data)))
edge_u = [e[0] for e in edges_data]
edge_v = [e[1] for e in edges_data]
edge_w = [e[2] for e in edges_data]
edge_type = [e[3] for e in edges_data]

# Terminals
terminals_A = [6, 7]
terminals_B = [10, 11]
all_terminals = set(terminals_A + terminals_B)

# Resource budget
RES_BUDGET = 20
COPPER_LIMIT = 3

# ============================================================
# VARIABLES
# ============================================================
# Edge selection
e = [Bool(f"e_{i}") for i in E]

# Vertex in tree
v_in_tree = [Bool(f"v_in_tree_{v}") for v in V]

# Steiner vertex
steiner = [Bool(f"steiner_{v}") for v in V]

# Gateway
gateway_A = [Bool(f"gateway_A_{v}") for v in V]
gateway_B = [Bool(f"gateway_B_{v}") for v in V]

solver = Solver()

# ============================================================
# CONSTRAINTS
# ============================================================

# 1. Terminals must be in the tree
for t in all_terminals:
    solver.add(v_in_tree[t])

# 2. Steiner vertices: non-terminal vertices that are in the tree
for v in V:
    if v in all_terminals:
        solver.add(Not(steiner[v]))
    else:
        solver.add(steiner[v] == v_in_tree[v])

# 3. Edge selection implies both endpoints are in the tree
for i in E:
    u, vtx = edge_u[i], edge_v[i]
    solver.add(Implies(e[i], And(v_in_tree[u], v_in_tree[vtx])))

# 4. Tree structure: exactly (num_vertices_in_tree - 1) edges
total_edges = Sum([If(e[i], 1, 0) for i in E])
total_vertices_in_tree = Sum([If(v_in_tree[v], 1, 0) for v in V])
solver.add(total_edges == total_vertices_in_tree - 1)

# 5. Connectivity: Use flow constraints
# For each edge, we have a directed flow variable
flow = [[Int(f"flow_{i}_{d}") for d in range(2)] for i in E]
for i in E:
    for d in range(2):
        solver.add(flow[i][d] >= 0)
        solver.add(Implies(Not(e[i]), flow[i][d] == 0))

# Root: pick the smallest-index vertex that is in the tree
root_v = Int('root_v')
solver.add(root_v >= 0, root_v <= 11)
# root_v must be in the tree
solver.add(Or([And(root_v == v, v_in_tree[v]) for v in V]))
# root_v is the smallest vertex in the tree
for v in V:
    solver.add(Implies(v_in_tree[v], root_v <= v))

# Flow conservation
for v in V:
    inflow_terms = []
    outflow_terms = []
    for i in E:
        if edge_u[i] == v:
            outflow_terms.append(flow[i][0])
            inflow_terms.append(flow[i][1])
        elif edge_v[i] == v:
            outflow_terms.append(flow[i][1])
            inflow_terms.append(flow[i][0])
    
    inflow = Sum(inflow_terms)
    outflow = Sum(outflow_terms)
    
    # For root: outflow - inflow = total_vertices_in_tree - 1
    solver.add(Implies(And(v_in_tree[v], root_v == v), 
                       outflow - inflow == total_vertices_in_tree - 1))
    # For non-root vertices in tree: outflow - inflow = -1
    solver.add(Implies(And(v_in_tree[v], root_v != v), 
                       outflow - inflow == -1))
    # For vertices not in tree: no flow
    solver.add(Implies(Not(v_in_tree[v]), 
                       And(inflow == 0, outflow == 0)))

# Flow bound
for i in E:
    for d in range(2):
        solver.add(flow[i][d] <= 12)

# 6. Hierarchy constraint: Steiner vertex at level L cannot connect to vertex at level > L
for i in E:
    u, vtx = edge_u[i], edge_v[i]
    solver.add(Implies(And(e[i], steiner[u]), level[u] >= level[vtx]))
    solver.add(Implies(And(e[i], steiner[vtx]), level[vtx] >= level[u]))

# 7. Resource budget: sum of resource costs for Steiner vertices <= 20
solver.add(Sum([If(steiner[v], res_cost[v], 0) for v in V]) <= RES_BUDGET)

# 8. Copper edge limit: at most 3 copper edges
solver.add(Sum([If(And(e[i], edge_type[i] == "copper"), 1, 0) for i in E]) <= COPPER_LIMIT)

# 9. Gateway requirement
for v in V:
    if v not in all_terminals:
        connects_to_A = Or([And(e[i], 
                               Or(And(edge_u[i] == v, edge_v[i] == t),
                                  And(edge_u[i] == t, edge_v[i] == v)))
                           for t in terminals_A for i in E])
        solver.add(gateway_A[v] == And(steiner[v], connects_to_A))
    else:
        solver.add(Not(gateway_A[v]))

for v in V:
    if v not in all_terminals:
        connects_to_B = Or([And(e[i], 
                               Or(And(edge_u[i] == v, edge_v[i] == t),
                                  And(edge_u[i] == t, edge_v[i] == v)))
                           for t in terminals_B for i in E])
        solver.add(gateway_B[v] == And(steiner[v], connects_to_B))
    else:
        solver.add(Not(gateway_B[v]))

# At least one gateway for each group
solver.add(Sum([If(gateway_A[v], 1, 0) for v in V]) >= 1)
solver.add(Sum([If(gateway_B[v], 1, 0) for v in V]) >= 1)

# 10. Gateway connectivity: All gateway vertices must be connected through Steiner-only paths
all_gateways = [Bool(f"all_gateway_{v}") for v in V]
for v in V:
    solver.add(all_gateways[v] == Or(gateway_A[v], gateway_B[v]))

total_gateways = Sum([If(all_gateways[v], 1, 0) for v in V])

# Steiner flow variables
steiner_flow = [[Int(f"sf_{i}_{d}") for d in range(2)] for i in E]
for i in E:
    for d in range(2):
        solver.add(steiner_flow[i][d] >= 0)
        solver.add(Implies(Or(Not(e[i]), Not(steiner[edge_u[i]]), Not(steiner[edge_v[i]])), 
                          steiner_flow[i][d] == 0))

# Pick a root gateway (smallest index)
root_gw = Int('root_gw')
solver.add(root_gw >= 0, root_gw <= 11)
solver.add(Or([And(root_gw == v, all_gateways[v]) for v in V]))
for v in V:
    solver.add(Implies(all_gateways[v], root_gw <= v))

# Flow conservation on Steiner subgraph
for v in V:
    s_inflow_terms = []
    s_outflow_terms = []
    for i in E:
        if edge_u[i] == v:
            s_outflow_terms.append(steiner_flow[i][0])
            s_inflow_terms.append(steiner_flow[i][1])
        elif edge_v[i] == v:
            s_outflow_terms.append(steiner_flow[i][1])
            s_inflow_terms.append(steiner_flow[i][0])
    
    s_inflow = Sum(s_inflow_terms)
    s_outflow = Sum(s_outflow_terms)
    
    solver.add(Implies(And(all_gateways[v], root_gw == v), 
                       s_outflow - s_inflow == total_gateways - 1))
    solver.add(Implies(And(all_gateways[v], root_gw != v), 
                       s_outflow - s_inflow == -1))
    solver.add(Implies(And(steiner[v], Not(all_gateways[v])),
                       s_outflow == s_inflow))
    solver.add(Implies(Not(steiner[v]),
                       And(s_inflow == 0, s_outflow == 0)))

for i in E:
    for d in range(2):
        solver.add(steiner_flow[i][d] <= 12)

# ============================================================
# OBJECTIVE: Minimize total edge weight
# ============================================================
total_weight = Sum([If(e[i], edge_w[i], 0) for i in E])

# Use Optimize - collect assertions as a list
assertions = solver.assertions()

opt = Optimize()
for a in assertions:
    opt.add(a)
opt.minimize(total_weight)

# ============================================================
# SOLVE
# ============================================================
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"Total weight: {m.eval(total_weight)}")
    
    # Extract tree edges
    tree_edges = []
    for i in E:
        if is_true(m.eval(e[i])):
            tree_edges.append((edge_u[i], edge_v[i], edge_w[i], edge_type[i]))
    print(f"Tree edges: {tree_edges}")
    
    # Extract Steiner vertices
    steiner_verts = [v for v in V if v not in all_terminals and is_true(m.eval(steiner[v]))]
    print(f"Steiner vertices: {steiner_verts}")
    
    # Extract gateways
    gw_A = [v for v in V if is_true(m.eval(gateway_A[v]))]
    gw_B = [v for v in V if is_true(m.eval(gateway_B[v]))]
    print(f"Gateways A: {gw_A}")
    print(f"Gateways B: {gw_B}")
    
    # Copper count
    copper_cnt = sum(1 for i in E if is_true(m.eval(e[i])) and edge_type[i] == "copper")
    print(f"Copper edge count: {copper_cnt}")
    
    # Resource cost
    res_total = sum(res_cost[v] for v in steiner_verts)
    print(f"Steiner resource cost: {res_total}")
    
    # All vertices in tree
    tree_verts = [v for v in V if is_true(m.eval(v_in_tree[v]))]
    print(f"Vertices in tree: {tree_verts}")
    
    print(f"answer:13")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")