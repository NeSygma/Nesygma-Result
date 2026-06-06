from z3 import *

# Define nodes and edges
nodes = [1,2,3,4,5,6]
source = 1
sink = 6

# Edge list with capacities
edges = [
    (1,2,10),
    (1,3,8),
    (2,3,5),
    (2,4,7),
    (3,4,3),
    (3,5,9),
    (4,6,8),
    (5,6,6)
]

# Create flow variables for each edge
flow_vars = {}
for (u,v,cap) in edges:
    flow_vars[(u,v)] = Real(f'f_{u}_{v}')

# Initialize optimizer
opt = Optimize()

# Add capacity and non-negativity constraints
for (u,v,cap) in edges:
    f = flow_vars[(u,v)]
    opt.add(f >= 0)
    opt.add(f <= cap)

# Flow conservation for intermediate nodes (2,3,4,5)
# Node 2: incoming from 1, outgoing to 3 and 4
opt.add(flow_vars[(1,2)] == flow_vars[(2,3)] + flow_vars[(2,4)])
# Node 3: incoming from 1 and 2, outgoing to 4 and 5
opt.add(flow_vars[(1,3)] + flow_vars[(2,3)] == flow_vars[(3,4)] + flow_vars[(3,5)])
# Node 4: incoming from 2 and 3, outgoing to 6
opt.add(flow_vars[(2,4)] + flow_vars[(3,4)] == flow_vars[(4,6)])
# Node 5: incoming from 3, outgoing to 6
opt.add(flow_vars[(3,5)] == flow_vars[(5,6)])

# Objective: maximize total flow from source (sum of flows out of source)
total_flow = flow_vars[(1,2)] + flow_vars[(1,3)]
opt.maximize(total_flow)

# Check
result = opt.check()
if result == sat:
    model = opt.model()
    max_flow_val = model.eval(total_flow)
    print("STATUS: sat")
    print(f"max_flow = {max_flow_val}")
    print("flows = [")
    for (u,v,cap) in edges:
        f_val = model.eval(flow_vars[(u,v)])
        print(f"    ({u}, {v}, {f_val}),")
    print("]")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")