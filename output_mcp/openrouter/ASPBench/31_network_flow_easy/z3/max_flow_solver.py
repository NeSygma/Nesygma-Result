from z3 import *

# Define edges and capacities
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

# Create flow variables for each edge
flows = [Real(f"f_{i}") for i in range(len(edges))]

opt = Optimize()

# Capacity and non-negativity constraints
for f, (_, _, cap) in zip(flows, edges):
    opt.add(f >= 0)
    opt.add(f <= cap)

# Flow conservation for intermediate nodes (2,3,4,5)
# Compute incoming and outgoing sums for each node
node_ids = [2,3,4,5]
for node in node_ids:
    incoming = Sum([f for f, (u, v, _) in zip(flows, edges) if v == node])
    outgoing = Sum([f for f, (u, v, _) in zip(flows, edges) if u == node])
    opt.add(incoming == outgoing)

# Define max_flow variable
max_flow = Real('max_flow')
# Source node 1: out - in = max_flow
source_out = Sum([f for f, (u, v, _) in zip(flows, edges) if u == 1])
source_in = Sum([f for f, (u, v, _) in zip(flows, edges) if v == 1])
opt.add(source_out - source_in == max_flow)
# Sink node 6: in - out = max_flow
sink_in = Sum([f for f, (u, v, _) in zip(flows, edges) if v == 6])
sink_out = Sum([f for f, (u, v, _) in zip(flows, edges) if u == 6])
opt.add(sink_in - sink_out == max_flow)

# Objective: maximize max_flow
opt.maximize(max_flow)

result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    # Extract max_flow value
    mf_val = m.eval(max_flow, model_completion=True)
    # If it's a rational, convert to float if denominator != 1
    if mf_val.is_int():
        print(f"max_flow = {mf_val.as_long()}")
    else:
        # Print as a decimal
        print(f"max_flow = {mf_val.as_decimal(10)}")
    # Print each flow
    for i, (u, v, _) in enumerate(edges):
        f_val = m.eval(flows[i], model_completion=True)
        if f_val.is_int():
            val_str = str(f_val.as_long())
        else:
            val_str = str(f_val.as_decimal(10))
        print(f"flow_{u}_{v} = {val_str}")
else:
    print("STATUS: unsat")