from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# ============================================================================
# Problem Data
# ============================================================================

# Network structure
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
source = 1
sink = 8
budget = 100

# Edges: (from, to, capacity, cost, type)
# type: 0 = standard, 1 = premium
edges = [
    (1, 2, 10, 2, 0),
    (1, 3, 12, 4, 1),
    (2, 4, 8, 1, 0),
    (2, 5, 4, 3, 1),
    (3, 4, 5, 3, 0),
    (3, 6, 10, 5, 1),
    (4, 7, 10, 2, 0),
    (5, 7, 7, 4, 1),
    (6, 8, 12, 2, 1),
    (7, 8, 15, 1, 0),
]

# Priority nodes
priority_nodes = [3, 5]

# ============================================================================
# Z3 Model
# ============================================================================
opt = Optimize()

# Flow variables for each edge
flow_vars = {}
for (u, v, cap, cost, typ) in edges:
    flow_vars[(u, v)] = Int(f"flow_{u}_{v}")

# ============================================================================
# Constraints
# ============================================================================

# 1. Capacity constraints
for (u, v, cap, cost, typ) in edges:
    opt.add(flow_vars[(u, v)] >= 0)
    opt.add(flow_vars[(u, v)] <= cap)

# 2. Flow conservation for intermediate nodes (not source/sink)
for node in nodes:
    if node == source or node == sink:
        continue
    
    # Total incoming flow
    in_flows = []
    for (u, v, cap, cost, typ) in edges:
        if v == node:
            in_flows.append(flow_vars[(u, v)])
    
    # Total outgoing flow
    out_flows = []
    for (u, v, cap, cost, typ) in edges:
        if u == node:
            out_flows.append(flow_vars[(u, v)])
    
    if in_flows and out_flows:
        opt.add(Sum(in_flows) == Sum(out_flows))

# 3. Budget constraint: total cost <= budget
# Total cost = sum(flow * cost for all edges)
total_cost = Sum([
    flow_vars[(u, v)] * cost for (u, v, cap, cost, typ) in edges
])
opt.add(total_cost <= budget)

# 4. Priority node rule: for nodes 3 and 5, if incoming flow > 0, then at least 75% of outgoing flow must be premium
for node in priority_nodes:
    # Total incoming flow
    in_flows = []
    for (u, v, cap, cost, typ) in edges:
        if v == node:
            in_flows.append(flow_vars[(u, v)])
    
    # Total outgoing flow and premium outgoing flow
    out_flows = []
    premium_out_flows = []
    for (u, v, cap, cost, typ) in edges:
        if u == node:
            out_flows.append(flow_vars[(u, v)])
            if typ == 1:  # premium type
                premium_out_flows.append(flow_vars[(u, v)])
    
    if out_flows:
        total_out = Sum(out_flows)
        total_premium_out = Sum(premium_out_flows)
        # If there is incoming flow, enforce the 75% premium rule
        if in_flows:
            opt.add(Implies(Sum(in_flows) > 0, total_premium_out >= 0.75 * total_out))

# 5. Global flow balancing: total standard flow >= 50% of total premium flow
# Compute total standard and premium flows across all edges
total_standard_flow = Sum([
    If(typ == 0, flow_vars[(u, v)], 0) for (u, v, cap, cost, typ) in edges
])

total_premium_flow = Sum([
    If(typ == 1, flow_vars[(u, v)], 0) for (u, v, cap, cost, typ) in edges
])

opt.add(total_standard_flow >= 0.5 * total_premium_flow)

# ============================================================================
# Objective: Maximize total flow from source (node 1)
# ============================================================================
total_flow_out_of_source = Sum([
    flow_vars[(u, v)] for (u, v, cap, cost, typ) in edges if u == source
])
opt.maximize(total_flow_out_of_source)

# ============================================================================
# Check and print result
# ============================================================================
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Maximum flow found!")
    print(f"Max flow value: {model.eval(total_flow_out_of_source)}")
    print("\nFlow assignments:")
    for (u, v, cap, cost, typ) in edges:
        flow_val = model.eval(flow_vars[(u, v)])
        print(f"Edge ({u},{v}): flow = {flow_val}, capacity = {cap}, cost = {cost}, type = {'standard' if typ == 0 else 'premium'}")
    print(f"\nTotal cost: {model.eval(total_cost)}")
    print(f"Total standard flow: {model.eval(total_standard_flow)}")
    print(f"Total premium flow: {model.eval(total_premium_flow)}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")