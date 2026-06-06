from z3 import *

# Define data
edges = [
    # (from, to, capacity, cost, is_premium)
    (1, 2, 10, 2, False),
    (1, 3, 12, 4, True),
    (2, 4, 8, 1, False),
    (2, 5, 4, 3, True),
    (3, 4, 5, 3, False),
    (3, 6, 10, 5, True),
    (4, 7, 10, 2, False),
    (5, 7, 7, 4, True),
    (6, 8, 12, 2, True),
    (7, 8, 15, 1, False)
]

num_edges = len(edges)
flow = [Int(f'flow_{i}') for i in range(num_edges)]

opt = Optimize()

# Capacity constraints
for i, e in enumerate(edges):
    _, _, cap, _, _ = e
    opt.add(flow[i] >= 0, flow[i] <= cap)

# Flow conservation for intermediate nodes (2..7)
nodes = [2,3,4,5,6,7]
for n in nodes:
    incoming = Sum([If(e[1] == n, flow[i], 0) for i, e in enumerate(edges)])
    outgoing = Sum([If(e[0] == n, flow[i], 0) for i, e in enumerate(edges)])
    opt.add(incoming == outgoing)

# Budget constraint
budget = Sum([flow[i] * e[3] for i, e in enumerate(edges)])
opt.add(budget <= 100)

# Priority node rule for nodes 3 and 5
priority_nodes = [3,5]
for n in priority_nodes:
    incoming = Sum([If(e[1] == n, flow[i], 0) for i, e in enumerate(edges)])
    total_out = Sum([If(e[0] == n, flow[i], 0) for i, e in enumerate(edges)])
    premium_out = Sum([If(And(e[0] == n, e[4]), flow[i], 0) for i, e in enumerate(edges)])
    # If there is incoming flow, enforce premium_out * 4 >= 3 * total_out
    opt.add(Implies(incoming > 0, premium_out * 4 >= 3 * total_out))

# Flow balancing: standard >= 0.5 * premium  => 2*standard >= premium
standard_total = Sum([If(e[4] == False, flow[i], 0) for i, e in enumerate(edges)])
premium_total = Sum([If(e[4] == True, flow[i], 0) for i, e in enumerate(edges)])
opt.add(standard_total * 2 >= premium_total)

# Objective: maximize total flow from source (node 1)
source_out = Sum([If(e[0] == 1, flow[i], 0) for i, e in enumerate(edges)])
opt.maximize(source_out)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    max_flow = m.eval(source_out, model_completion=True).as_long()
    print("STATUS: sat")
    print("max_flow =", max_flow)
    for i, e in enumerate(edges):
        fval = m.eval(flow[i], model_completion=True).as_long()
        print(f"edge {e[0]}->{e[1]} flow = {fval}")
else:
    print("STATUS: unsat")