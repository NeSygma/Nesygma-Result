from z3 import *

# BENCHMARK_MODE: OFF (since we are solving a maximization problem and expect a concrete answer)

# Initialize the solver
opt = Optimize()

# Define the nodes and edges with capacities
nodes = [1, 2, 3, 4, 5, 6]
source = 1
sink = 6

edges = [
    (1, 2, 10),
    (1, 3, 8),
    (2, 3, 5),
    (2, 4, 7),
    (3, 4, 3),
    (3, 5, 9),
    (4, 6, 8),
    (5, 6, 6)
]

# Create a dictionary to hold the flow variables for each edge
flow_vars = {}
for (u, v, cap) in edges:
    flow_vars[(u, v)] = Int(f'flow_{u}_{v}')

# Add capacity constraints: flow <= capacity for each edge
for (u, v, cap) in edges:
    opt.add(flow_vars[(u, v)] >= 0)
    opt.add(flow_vars[(u, v)] <= cap)

# Add flow conservation constraints for intermediate nodes
for node in nodes:
    if node != source and node != sink:
        incoming_flows = []
        outgoing_flows = []
        for (u, v, cap) in edges:
            if v == node:
                incoming_flows.append(flow_vars[(u, v)])
            if u == node:
                outgoing_flows.append(flow_vars[(u, v)])
        opt.add(Sum(incoming_flows) == Sum(outgoing_flows))

# Define the total flow from source to sink
total_flow = Int('total_flow')
outgoing_flows_from_source = [flow_vars[(source, v)] for (u, v, cap) in edges if u == source]
opt.add(total_flow == Sum(outgoing_flows_from_source))

# Maximize the total flow
opt.maximize(total_flow)

# Check and print the result
result = opt.check()
if result == sat:
    model = opt.model()
    max_flow_value = model[total_flow]
    flows = []
    for (u, v, cap) in edges:
        flow_val = model[flow_vars[(u, v)]]
        flows.append((u, v, flow_val))
    print("STATUS: sat")
    print(f"max_flow = {max_flow_value}")
    for (u, v, flow_val) in flows:
        print(f"flow_{u}_{v} = {flow_val}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")