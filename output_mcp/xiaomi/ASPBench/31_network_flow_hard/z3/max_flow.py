from z3 import *

# Edge data: (from, to, capacity, cost, type)
edges = [
    (1, 2, 10, 2, 'standard'),
    (1, 3, 12, 4, 'premium'),
    (2, 4, 8, 1, 'standard'),
    (2, 5, 4, 3, 'premium'),
    (3, 4, 5, 3, 'standard'),
    (3, 6, 10, 5, 'premium'),
    (4, 7, 10, 2, 'standard'),
    (5, 7, 7, 4, 'premium'),
    (6, 8, 12, 2, 'premium'),
    (7, 8, 15, 1, 'standard'),
]

nodes = [1, 2, 3, 4, 5, 6, 7, 8]
source = 1
sink = 8
budget = 100
priority_nodes = [3, 5]

# Create flow variables for each edge
flows = [Int(f'flow_{i}') for i in range(len(edges))]

opt = Optimize()

# 1. Capacity constraints: 0 <= flow <= capacity
for i, (u, v, cap, cost, typ) in enumerate(edges):
    opt.add(flows[i] >= 0)
    opt.add(flows[i] <= cap)

# 2. Flow conservation for intermediate nodes
for node in nodes:
    if node == source or node == sink:
        continue
    # Incoming flow
    incoming = Sum([flows[i] for i, (u, v, cap, cost, typ) in enumerate(edges) if v == node])
    # Outgoing flow
    outgoing = Sum([flows[i] for i, (u, v, cap, cost, typ) in enumerate(edges) if u == node])
    opt.add(incoming == outgoing)

# 3. Budget constraint: total cost <= 100
total_cost = Sum([flows[i] * edges[i][3] for i in range(len(edges))])
opt.add(total_cost <= budget)

# 4. Priority node rule: for priority nodes, >=75% of outgoing flow must be premium
for pnode in priority_nodes:
    # Outgoing premium flow
    out_premium = Sum([flows[i] for i, (u, v, cap, cost, typ) in enumerate(edges) if u == pnode and typ == 'premium'])
    # Total outgoing flow
    out_total = Sum([flows[i] for i, (u, v, cap, cost, typ) in enumerate(edges) if u == pnode])
    # If there is outgoing flow, at least 75% must be premium
    # out_premium >= 0.75 * out_total  =>  4 * out_premium >= 3 * out_total
    opt.add(Implies(out_total > 0, 4 * out_premium >= 3 * out_total))

# 5. Flow balancing: total standard flow >= 50% of total premium flow
# std >= 0.5 * prem  =>  2 * std >= prem
total_standard = Sum([flows[i] for i, (u, v, cap, cost, typ) in enumerate(edges) if typ == 'standard'])
total_premium = Sum([flows[i] for i, (u, v, cap, cost, typ) in enumerate(edges) if typ == 'premium'])
opt.add(2 * total_standard >= total_premium)

# Objective: maximize total flow from source to sink
# Total flow = sum of outgoing from source = sum of incoming to sink
total_out_source = Sum([flows[i] for i, (u, v, cap, cost, typ) in enumerate(edges) if u == source])
total_in_sink = Sum([flows[i] for i, (u, v, cap, cost, typ) in enumerate(edges) if v == sink])
# They should be equal by flow conservation, but let's be explicit
opt.add(total_out_source == total_in_sink)

opt.maximize(total_out_source)

result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    max_flow = m.evaluate(total_out_source)
    print(f"max_flow = {max_flow}")
    print("flows:")
    for i, (u, v, cap, cost, typ) in enumerate(edges):
        f_val = m.evaluate(flows[i])
        print(f"  ({u}, {v}): flow = {f_val} (capacity={cap}, cost={cost}, type={typ})")
    # Verify budget
    total_cost_val = sum(m.evaluate(flows[i]).as_long() * edges[i][3] for i in range(len(edges)))
    print(f"Total cost = {total_cost_val}")
    # Verify standard/premium balance
    std_total = sum(m.evaluate(flows[i]).as_long() for i, (u, v, cap, cost, typ) in enumerate(edges) if typ == 'standard')
    prem_total = sum(m.evaluate(flows[i]).as_long() for i, (u, v, cap, cost, typ) in enumerate(edges) if typ == 'premium')
    print(f"Total standard flow = {std_total}")
    print(f"Total premium flow = {prem_total}")
    print(f"Standard >= 50% of premium: {std_total >= 0.5 * prem_total}")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")