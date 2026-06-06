from z3 import *

solver = Optimize()

# Edge data: (from, to, capacity, cost, type)
edges = [
    (1, 2, 10, 2, 'standard'),
    (1, 3, 12, 4, 'premium'),
    (2, 4, 8, 1, 'standard'),
    (2, 5, 4, 3, 'premium'),
    (3, 4, 5, 3, 'standard'),
    (3, 6, 10, 5, 'premium'),
    (4, 7, 10, 2, 'standard'),
    (5, 7, 7, 4, 'premium'),
    (6, 8, 12, 2, 'premium'),
    (7, 8, 15, 1, 'standard')
]

n_edges = len(edges)
flows = [Int(f'f_{i}') for i in range(n_edges)]

# Capacity constraints
for i, (u, v, cap, cost, typ) in enumerate(edges):
    solver.add(flows[i] >= 0, flows[i] <= cap)

# Build incoming and outgoing lists per node
incoming = {node: [] for node in range(1, 9)}
outgoing = {node: [] for node in range(1, 9)}
for i, (u, v, cap, cost, typ) in enumerate(edges):
    outgoing[u].append(i)
    incoming[v].append(i)

# Flow conservation for intermediate nodes (2..7)
for node in range(2, 8):
    solver.add(Sum([flows[i] for i in incoming[node]]) == Sum([flows[i] for i in outgoing[node]]))

# Budget constraint
budget = 100
solver.add(Sum([flows[i] * edges[i][3] for i in range(n_edges)]) <= budget)

# Priority node rule for node 3 (at least 75% premium outgoing)
# Node 3 outgoing edges: 4 (standard), 5 (premium)
solver.add(4 * flows[5] >= 3 * (flows[4] + flows[5]))
# Node 5 rule (trivial but added for completeness)
solver.add(4 * flows[7] >= 3 * flows[7])

# Flow balancing: total standard >= 50% of total premium
standard_edges = [i for i, e in enumerate(edges) if e[4] == 'standard']
premium_edges = [i for i, e in enumerate(edges) if e[4] == 'premium']
standard_sum = Sum([flows[i] for i in standard_edges])
premium_sum = Sum([flows[i] for i in premium_edges])
solver.add(2 * standard_sum >= premium_sum)

# Max flow variable
max_flow = Int('max_flow')
solver.add(max_flow == Sum([flows[i] for i in outgoing[1]]))
solver.maximize(max_flow)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"max_flow = {m[max_flow]}")
    for i, (u, v, cap, cost, typ) in enumerate(edges):
        print(f"f_{i} = {m[flows[i]]} (from {u} to {v})")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")