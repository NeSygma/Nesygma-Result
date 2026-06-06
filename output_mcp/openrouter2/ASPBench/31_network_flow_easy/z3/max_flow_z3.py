from z3 import *

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

# Create flow variables
flow_vars = {}
for u, v, cap in edges:
    var = Int(f"f_{u}_{v}")
    flow_vars[(u, v)] = var

# Optimize solver
opt = Optimize()

# Capacity and non-negativity constraints
for (u, v, cap), var in flow_vars.items():
    opt.add(var >= 0)
    opt.add(var <= cap)

# Flow conservation for intermediate nodes 2,3,4,5
nodes = [2, 3, 4, 5]
for n in nodes:
    incoming = [var for (u, v), var in flow_vars.items() if v == n]
    outgoing = [var for (u, v), var in flow_vars.items() if u == n]
    opt.add(Sum(incoming) == Sum(outgoing))

# Define max_flow variable
max_flow = Int("max_flow")
# Source 1 outgoing
source_out = [var for (u, v), var in flow_vars.items() if u == 1]
# Sink 6 incoming
sink_in = [var for (u, v), var in flow_vars.items() if v == 6]
opt.add(max_flow == Sum(source_out))
opt.add(max_flow == Sum(sink_in))

# Objective: maximize max_flow
opt.maximize(max_flow)

# Check and print results
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"max_flow = {model[max_flow]}")
    for (u, v), var in flow_vars.items():
        print(f"f_{u}_{v} = {model[var]}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")