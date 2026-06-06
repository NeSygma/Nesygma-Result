from z3 import *

# Edge data: (from, to, capacity, cost, type)
# type: 0 = standard, 1 = premium
edges = [
    (1, 2, 10, 2, 0),  # e0
    (1, 3, 12, 4, 1),  # e1
    (2, 4,  8, 1, 0),  # e2
    (2, 5,  4, 3, 1),  # e3
    (3, 4,  5, 3, 0),  # e4
    (3, 6, 10, 5, 1),  # e5
    (4, 7, 10, 2, 0),  # e6
    (5, 7,  7, 4, 1),  # e7
    (6, 8, 12, 2, 1),  # e8
    (7, 8, 15, 1, 0),  # e9
]

nodes = [1, 2, 3, 4, 5, 6, 7, 8]
source = 1
sink = 8
budget = 100
priority_nodes = [3, 5]

num_edges = len(edges)

# Create flow variables for each edge
flow = [Int(f'flow_{i}') for i in range(num_edges)]

opt = Optimize()

# 1. Capacity constraints: 0 <= flow[i] <= capacity
for i, (u, v, cap, cost, etype) in enumerate(edges):
    opt.add(flow[i] >= 0)
    opt.add(flow[i] <= cap)

# 2. Flow conservation for intermediate nodes
for node in nodes:
    if node == source or node == sink:
        continue
    incoming = Sum([flow[i] for i in range(num_edges) if edges[i][1] == node])
    outgoing = Sum([flow[i] for i in range(num_edges) if edges[i][0] == node])
    opt.add(incoming == outgoing)

# 3. Total flow from source = total flow into sink = max_flow
flow_out_source = Sum([flow[i] for i in range(num_edges) if edges[i][0] == source])
flow_in_sink = Sum([flow[i] for i in range(num_edges) if edges[i][1] == sink])
max_flow = Int('max_flow')
opt.add(max_flow == flow_out_source)
opt.add(max_flow == flow_in_sink)

# 4. Budget constraint: sum(flow[i] * cost[i]) <= budget
total_cost = Sum([flow[i] * edges[i][3] for i in range(num_edges)])
opt.add(total_cost <= budget)

# 5. Priority node rule: for priority nodes, >= 75% of outgoing flow must be premium
#    i.e., 4 * premium_outgoing >= 3 * total_outgoing
for pnode in priority_nodes:
    outgoing_premium = Sum([flow[i] for i in range(num_edges)
                            if edges[i][0] == pnode and edges[i][4] == 1])
    outgoing_total = Sum([flow[i] for i in range(num_edges) if edges[i][0] == pnode])
    # 4 * premium >= 3 * total  (equivalent to premium >= 0.75 * total)
    opt.add(4 * outgoing_premium >= 3 * outgoing_total)

# 6. Flow balancing: total standard flow >= 50% of total premium flow
#    i.e., 2 * standard >= premium
total_standard = Sum([flow[i] for i in range(num_edges) if edges[i][4] == 0])
total_premium = Sum([flow[i] for i in range(num_edges) if edges[i][4] == 1])
opt.add(2 * total_standard >= total_premium)

# Objective: maximize total flow
opt.maximize(max_flow)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    mf = m[max_flow].as_long()
    print("STATUS: sat")
    print(f"max_flow = {mf}")
    print(f"total_cost = {m.eval(total_cost)}")
    print(f"total_standard = {m.eval(total_standard)}")
    print(f"total_premium = {m.eval(total_premium)}")
    print()
    print("flows:")
    for i, (u, v, cap, cost, etype) in enumerate(edges):
        fval = m[flow[i]].as_long()
        etype_str = "premium" if etype == 1 else "standard"
        print(f"  ({u},{v}): flow={fval}, capacity={cap}, cost_per_unit={cost}, type={etype_str}")
    print()
    # Verify priority node constraints
    for pnode in priority_nodes:
        out_prem = sum(m[flow[i]].as_long() for i in range(num_edges)
                       if edges[i][0] == pnode and edges[i][4] == 1)
        out_total = sum(m[flow[i]].as_long() for i in range(num_edges)
                        if edges[i][0] == pnode)
        if out_total > 0:
            pct = 100.0 * out_prem / out_total
            print(f"  Priority node {pnode}: premium_out={out_prem}, total_out={out_total}, premium%={pct:.1f}%")
        else:
            print(f"  Priority node {pnode}: no outgoing flow")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")