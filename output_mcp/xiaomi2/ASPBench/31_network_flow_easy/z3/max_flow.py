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
    (5, 6, 6),
]

nodes = [1, 2, 3, 4, 5, 6]
source = 1
sink = 6
intermediate = [n for n in nodes if n not in (source, sink)]

# Create flow variables for each edge
flow_vars = {}
for (u, v, cap) in edges:
    flow_vars[(u, v)] = Real(f'flow_{u}_{v}')

opt = Optimize()

# 1. Capacity constraints: 0 <= flow <= capacity
for (u, v, cap) in edges:
    opt.add(flow_vars[(u, v)] >= 0)
    opt.add(flow_vars[(u, v)] <= cap)

# 2. Flow conservation for intermediate nodes
for node in intermediate:
    incoming = Sum([flow_vars[(u, v)] for (u, v) in flow_vars if v == node])
    outgoing = Sum([flow_vars[(u, v)] for (u, v) in flow_vars if u == node])
    opt.add(incoming == outgoing)

# 3. Total flow out of source = total flow into sink = max_flow
total_out_source = Sum([flow_vars[(u, v)] for (u, v) in flow_vars if u == source])
total_in_sink = Sum([flow_vars[(u, v)] for (u, v) in flow_vars if v == sink])

# These should be equal by flow conservation (if we add a return edge conceptually)
opt.add(total_out_source == total_in_sink)

max_flow = total_out_source
opt.maximize(max_flow)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract max flow value
    mf = m.evaluate(max_flow)
    print(f"max_flow = {mf}")
    
    # Extract individual flows
    print("flows:")
    for (u, v, cap) in edges:
        f = m.evaluate(flow_vars[(u, v)])
        print(f"  {u} -> {v}: flow = {f} (capacity = {cap})")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")