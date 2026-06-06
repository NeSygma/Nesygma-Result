from z3 import *

# Create an optimizer for maximum flow
opt = Optimize()

# Define the edges with their capacities
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

# Create a flow variable for each edge
flow_vars = {}
capacities = {}
for u, v, cap in edges:
    flow_vars[(u, v)] = Int(f"flow_{u}_{v}")
    capacities[(u, v)] = cap

# Add capacity constraints: flow <= capacity
for (u, v), f in flow_vars.items():
    cap = capacities[(u, v)]
    opt.add(f >= 0)
    opt.add(f <= cap)

# Add flow conservation constraints for intermediate nodes (2, 3, 4, 5)
# For each node, inflow = outflow
nodes = [1, 2, 3, 4, 5, 6]
for node in nodes:
    if node == 1 or node == 6:  # Skip source and sink
        continue
    
    # Calculate inflow: sum of flows where 'to' is the node
    inflow = Sum([flow_vars[(u, v)] for (u, v, _) in edges if v == node])
    
    # Calculate outflow: sum of flows where 'from' is the node
    outflow = Sum([flow_vars[(u, v)] for (u, v, _) in edges if u == node])
    
    # Flow conservation: inflow == outflow
    opt.add(inflow == outflow)

# The total flow is the sum of flows leaving the source (node 1)
total_flow = Sum([flow_vars[(1, v)] for (u, v, _) in edges if u == 1])

# Maximize the total flow
opt.maximize(total_flow)

# Check for a solution
result = opt.check()

if result == sat:
    model = opt.model()
    max_flow_value = model.eval(total_flow)
    print("STATUS: sat")
    print(f"max_flow = {max_flow_value}")
    
    # Print the flows for each edge
    print("flows = [")
    for (u, v), f in flow_vars.items():
        flow_val = model.eval(f)
        print(f"  {{'from': {u}, 'to': {v}, 'flow': {flow_val}}},")
    print("]")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (no solution found)")
else:
    print("STATUS: unknown")