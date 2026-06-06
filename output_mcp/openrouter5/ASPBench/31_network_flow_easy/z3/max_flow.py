from z3 import *

# Create optimizer
opt = Optimize()

# Define edges with capacities
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

# Create flow variables for each edge (non-negative reals)
flow_vars = {}
for (u, v, cap) in edges:
    f = Real(f'flow_{u}_{v}')
    flow_vars[(u, v)] = f
    # Non-negativity and capacity constraints
    opt.add(f >= 0)
    opt.add(f <= cap)

# Flow conservation for intermediate nodes (2, 3, 4, 5)
# Node 2: incoming from 1, outgoing to 3 and 4
opt.add(flow_vars[(1, 2)] == flow_vars[(2, 3)] + flow_vars[(2, 4)])

# Node 3: incoming from 1 and 2, outgoing to 4 and 5
opt.add(flow_vars[(1, 3)] + flow_vars[(2, 3)] == flow_vars[(3, 4)] + flow_vars[(3, 5)])

# Node 4: incoming from 2 and 3, outgoing to 6
opt.add(flow_vars[(2, 4)] + flow_vars[(3, 4)] == flow_vars[(4, 6)])

# Node 5: incoming from 3, outgoing to 6
opt.add(flow_vars[(3, 5)] == flow_vars[(5, 6)])

# Objective: maximize total flow out of source (node 1)
total_flow = flow_vars[(1, 2)] + flow_vars[(1, 3)]
opt.maximize(total_flow)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    max_flow_val = m.eval(total_flow)
    print("STATUS: sat")
    print(f"max_flow = {max_flow_val}")
    print("flows:")
    for (u, v, cap) in edges:
        f_val = m.eval(flow_vars[(u, v)])
        print(f"  from {u} to {v}: flow = {f_val}")
else:
    print("STATUS: unsat")