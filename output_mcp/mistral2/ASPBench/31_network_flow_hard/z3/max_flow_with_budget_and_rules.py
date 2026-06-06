from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

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

# Declare flow variables for each edge
flow_vars = [Int(f"flow_{i}") for i in range(len(edges))]

# Total flow (objective)
max_flow = Int("max_flow")

# Cost for each edge
costs = [cost for (_, _, _, cost, _) in edges]

# Edge types: 0=standard, 1=premium
types = [typ for (_, _, _, _, typ) in edges]

# Total cost constraint
total_cost = Sum([flow_vars[i] * costs[i] for i in range(len(edges))])

# Capacity constraints
capacity_constraints = [
    And(flow_vars[i] >= 0, flow_vars[i] <= edges[i][2])
    for i in range(len(edges))
]

# Flow conservation constraints
# For each node, sum of incoming flow = sum of outgoing flow
# Skip source and sink
flow_conservation = []
for node in nodes:
    if node == source or node == sink:
        continue
    incoming = []
    outgoing = []
    for i, (f, t, _, _, _) in enumerate(edges):
        if t == node:
            outgoing.append(flow_vars[i])
        if f == node:
            incoming.append(flow_vars[i])
    if incoming or outgoing:
        flow_conservation.append(Sum(incoming) == Sum(outgoing))

# Budget constraint
budget_constraint = total_cost <= budget

# Priority node rule:
# For priority nodes, if there is incoming flow, at least 75% of outgoing flow must be premium
priority_constraints = []
for node in priority_nodes:
    incoming = []
    outgoing = []
    outgoing_premium = []
    for i, (f, t, _, _, typ) in enumerate(edges):
        if t == node:
            incoming.append(flow_vars[i])
        if f == node:
            outgoing.append(flow_vars[i])
            if typ == 1:
                outgoing_premium.append(flow_vars[i])
    if incoming or outgoing:
        total_outgoing = Sum(outgoing)
        total_premium_outgoing = Sum(outgoing_premium)
        # If there is incoming flow, enforce the 75% premium rule
        priority_constraints.append(
            Implies(
                Sum(incoming) > 0,
                total_premium_outgoing >= 0.75 * total_outgoing
            )
        )

# Flow balancing: total standard flow >= 50% of total premium flow
total_standard_flow = Sum([
    If(types[i] == 0, flow_vars[i], 0)
    for i in range(len(edges))
])
total_premium_flow = Sum([
    If(types[i] == 1, flow_vars[i], 0)
    for i in range(len(edges))
])
flow_balancing = total_standard_flow >= 0.5 * total_premium_flow

# Total flow: sum of flows leaving the source
source_outgoing = []
for i, (f, t, _, _, _) in enumerate(edges):
    if f == source:
        source_outgoing.append(flow_vars[i])
flow_constraint = max_flow == Sum(source_outgoing)

# Objective: maximize max_flow
opt = Optimize()

# Add all constraints
for con in capacity_constraints:
    opt.add(con)
for con in flow_conservation:
    opt.add(con)
opt.add(budget_constraint)
for con in priority_constraints:
    opt.add(con)
opt.add(flow_balancing)
opt.add(flow_constraint)

# Maximize max_flow
opt.maximize(max_flow)

# Check and print result
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"max_flow = {model[max_flow]}")
    print("flows:")
    for i, (f, t, _, _, typ) in enumerate(edges):
        flow_val = model[flow_vars[i]]
        print(f"  ({f}, {t}): flow={flow_val}, type={'premium' if typ == 1 else 'standard'}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")