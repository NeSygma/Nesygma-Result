from z3 import *

# Define edges: (from, to, capacity)
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

# Create flow variables for each edge
flows = {}
for (u, v, cap) in edges:
    flows[(u, v)] = Int(f'flow_{u}_{v}')

opt = Optimize()

# 1. Capacity constraints and non-negativity
for (u, v, cap) in edges:
    opt.add(flows[(u, v)] >= 0)
    opt.add(flows[(u, v)] <= cap)

# 2. Flow conservation for intermediate nodes (2, 3, 4, 5)
intermediate_nodes = [2, 3, 4, 5]
source = 1
sink = 6

for node in intermediate_nodes:
    # Incoming flow: sum of flows on edges where 'to' == node
    incoming = Sum([flows[(u, v)] for (u, v, cap) in edges if v == node])
    # Outgoing flow: sum of flows on edges where 'from' == node
    outgoing = Sum([flows[(u, v)] for (u, v, cap) in edges if u == node])
    opt.add(incoming == outgoing)

# 3. Maximize total flow out of source (which equals total flow into sink by conservation)
total_out_source = Sum([flows[(u, v)] for (u, v, cap) in edges if u == source])
opt.maximize(total_out_source)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    max_flow_val = m.evaluate(total_out_source, model_completion=True)
    print("STATUS: sat")
    print(f"max_flow = {max_flow_val}")
    print("flows:")
    for (u, v, cap) in edges:
        f_val = m.evaluate(flows[(u, v)], model_completion=True)
        print(f"  from={u}, to={v}, flow={f_val}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")