from z3 import *

# Create solver (using Optimize for maximization)
opt = Optimize()

# Network data
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
source = 1
sink = 8
budget = 100

# Edges: (from, to, capacity, cost, type)  type: 0=standard, 1=premium
edges_data = [
    (1, 2, 10, 2, 0),
    (1, 3, 12, 4, 1),
    (2, 4, 8, 1, 0),
    (2, 5, 4, 3, 1),
    (3, 4, 5, 3, 0),
    (3, 6, 10, 5, 1),
    (4, 7, 10, 2, 0),
    (5, 7, 7, 4, 1),
    (6, 8, 12, 2, 1),
    (7, 8, 15, 1, 0)
]

E = len(edges_data)

# Flow variables for each edge (integer, non-negative)
flow = [Int(f'flow_{i}') for i in range(E)]

# Add flow variables to optimization context
for i in range(E):
    opt.add(flow[i] >= 0)
    opt.add(flow[i] <= edges_data[i][2])  # capacity constraint

# Flow conservation: for each intermediate node, sum(incoming) = sum(outgoing)
# Build adjacency lists
in_edges = {n: [] for n in nodes}
out_edges = {n: [] for n in nodes}
for i, (f, t, cap, cost, typ) in enumerate(edges_data):
    out_edges[f].append(i)
    in_edges[t].append(i)

for n in nodes:
    if n == source or n == sink:
        continue
    # sum of flows on incoming edges = sum of flows on outgoing edges
    opt.add(Sum([flow[i] for i in in_edges[n]]) == Sum([flow[i] for i in out_edges[n]]))

# Budget constraint: total cost <= 100
total_cost = Sum([flow[i] * edges_data[i][3] for i in range(E)])
opt.add(total_cost <= budget)

# Priority Node Rule: For nodes 3 and 5, if there is incoming flow,
# at least 75% of outgoing flow must be premium type.
# Premium outgoing edges from node 3: edge index 4 (3->4, standard) and 5 (3->6, premium)
# Premium outgoing edges from node 5: edge index 3 (2->5, premium) -- wait, that's incoming to 5.
# Let me re-check: node 5 outgoing edges: (5,7) index 8, premium
# Node 3 outgoing edges: (3,4) index 4 standard, (3,6) index 5 premium
# Node 5 outgoing edges: (5,7) index 8 premium

priority_nodes = [3, 5]
for pn in priority_nodes:
    out_indices = out_edges[pn]
    in_indices = in_edges[pn]
    # Total outgoing flow
    total_out = Sum([flow[i] for i in out_indices])
    # Premium outgoing flow
    premium_out = Sum([flow[i] for i in out_indices if edges_data[i][4] == 1])
    # Incoming flow
    total_in = Sum([flow[i] for i in in_indices])
    # If there is incoming flow (total_in > 0), then premium_out >= 0.75 * total_out
    # Implies(total_in > 0, premium_out >= 0.75 * total_out)
    # Use a small epsilon to avoid issues with integer division
    opt.add(Implies(total_in > 0, 4 * premium_out >= 3 * total_out))

# Flow Balancing: total standard flow >= 0.5 * total premium flow
total_standard = Sum([flow[i] for i in range(E) if edges_data[i][4] == 0])
total_premium = Sum([flow[i] for i in range(E) if edges_data[i][4] == 1])
opt.add(2 * total_standard >= total_premium)

# Objective: maximize total flow from source to sink
# Total flow = sum of flows on edges leaving source (node 1)
source_out_flow = Sum([flow[i] for i in out_edges[source]])
opt.maximize(source_out_flow)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    max_flow_val = m.eval(source_out_flow)
    print("STATUS: sat")
    print(f"max_flow = {max_flow_val}")
    print("flows:")
    for i, (f, t, cap, cost, typ) in enumerate(edges_data):
        fv = m.eval(flow[i])
        if fv.as_long() > 0:
            print(f"  ({f} -> {t}): flow={fv}")
    # Also print total cost
    tc_val = m.eval(total_cost)
    print(f"total_cost = {tc_val}")
    # Print standard and premium totals
    ts_val = m.eval(total_standard)
    tp_val = m.eval(total_premium)
    print(f"total_standard = {ts_val}, total_premium = {tp_val}")
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found")
else:
    print("STATUS: unknown")