from z3 import *

# Define edges with (from, to, capacity, cost, type)
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
    (7, 8, 15, 1, 'standard')
]

# Create flow variables
flow_vars = [Int(f'f{i}') for i in range(len(edges))]

solver = Solver()

# Capacity constraints
for i, (u, v, cap, cost, typ) in enumerate(edges):
    solver.add(flow_vars[i] >= 0)
    solver.add(flow_vars[i] <= cap)

# Flow conservation constraints
# Node 2: incoming f0, outgoing f2, f3
solver.add(flow_vars[0] == flow_vars[2] + flow_vars[3])
# Node 3: incoming f1, outgoing f4, f5
solver.add(flow_vars[1] == flow_vars[4] + flow_vars[5])
# Node 4: incoming f2 + f4, outgoing f6
solver.add(flow_vars[2] + flow_vars[4] == flow_vars[6])
# Node 5: incoming f3, outgoing f7
solver.add(flow_vars[3] == flow_vars[7])
# Node 6: incoming f5, outgoing f8
solver.add(flow_vars[5] == flow_vars[8])
# Node 7: incoming f6 + f7, outgoing f9
solver.add(flow_vars[6] + flow_vars[7] == flow_vars[9])

# Budget constraint: total cost <= 100
total_cost = Sum([flow_vars[i] * edges[i][3] for i in range(len(edges))])
solver.add(total_cost <= 100)

# Priority node rule for node 3 (edge indices 4 and 5 are outgoing from node 3)
# f5 (premium) >= 3 * f4 (standard)  (derived from f6 >= 0.75*(f5+f6))
solver.add(flow_vars[5] >= 3 * flow_vars[4])

# For node 5, outgoing premium flow is f7 (premium), total outgoing is f7, so always satisfied.

# Global flow balancing: total standard flow >= 0.5 * total premium flow
standard_edges = [0, 2, 4, 6, 9]  # indices of standard edges
premium_edges = [1, 3, 5, 7, 8]  # indices of premium edges
total_standard = Sum([flow_vars[i] for i in standard_edges])
total_premium = Sum([flow_vars[i] for i in premium_edges])
solver.add(total_standard >= total_premium * 0.5)

# Objective: maximize total flow from source (node 1) to sink (node 8)
# Total flow from source = f0 + f1
total_flow = flow_vars[0] + flow_vars[1]
# We'll maximize using Optimize
opt = Optimize()
# Add all constraints to opt
for c in solver.assertions():
    opt.add(c)
# Maximize total flow
opt.maximize(total_flow)

# Check
result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"Maximum flow: {m[total_flow]}")
    print("Flows:")
    for i, (u, v, cap, cost, typ) in enumerate(edges):
        f = m[flow_vars[i]]
        print(f"  Edge ({u},{v}): flow = {f}, capacity = {cap}, cost = {cost}, type = {typ}")
    # Also print total cost and flow balance
    total_cost_val = sum(m[flow_vars[i]] * edges[i][3] for i in range(len(edges)))
    print(f"Total cost: {total_cost_val}")
    total_std = sum(m[flow_vars[i]] for i in standard_edges)
    total_prem = sum(m[flow_vars[i]] for i in premium_edges)
    print(f"Total standard flow: {total_std}, total premium flow: {total_prem}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")