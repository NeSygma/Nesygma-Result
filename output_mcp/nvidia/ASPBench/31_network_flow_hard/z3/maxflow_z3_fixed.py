from z3 import *

# Define the network edges: (from, to, capacity, cost per unit, type)
edges = [
    (1,2,10,2,'standard'),
    (1,3,12,4,'premium'),
    (2,4,8,1,'standard'),
    (2,5,4,3,'premium'),
    (3,4,5,3,'standard'),
    (3,6,10,5,'premium'),
    (4,7,10,2,'standard'),
    (5,7,7,4,'premium'),
    (6,8,12,2,'premium'),
    (7,8,15,1,'standard')
]

# Create integer flow variables for each directed edge
flow = {}
for (u,v,cap,cost,typ) in edges:
    flow[(u,v)] = Int(f'f_{u}_{v}')

solver = Optimize()

# 1. Capacity constraints
for (u,v,cap,_,_) in edges:
    solver.add(flow[(u,v)] >= 0)
    solver.add(flow[(u,v)] <= cap)

# 2. Flow conservation for intermediate nodes (not source 1, not sink 8)
nodes = set()
for (u,_,_,_,_) in edges:
    nodes.add(u)
    nodes.add(v)
intermediate_nodes = [n for n in nodes if n not in (1,8)]

for n in intermediate_nodes:
    # incoming flow to n
    inc = [flow[(src,n)] for (src,dst,_,_,_) in edges if dst == n]
    # outgoing flow from n
    out = [flow[(n,dst)] for (src,dst,_,_,_) in edges if src == n]
    solver.add(Sum(inc) == Sum(out))

# 3. Budget constraint: total cost <= 100
solver.add(Sum([flow[(u,v)] * cost for (u,v,_,cost,_) in edges]) <= 100)

# 4. Priority node rule: nodes 3 and 5
priority_nodes = [3,5]
for p in priority_nodes:
    # outgoing edges from p
    out_edges = [(src,dst,cap,cost,typ) for (src,dst,cap,cost,typ) in edges if src == p]
    # premium outgoing flow
    premium_out = [flow[(p,dst)] for (src,dst,cap,cost,typ) in out_edges if typ == 'premium']
    total_out = [flow[(p,dst)] for (src,dst,cap,cost,typ) in out_edges]
    # at least 75% of outgoing flow must be premium: 4 * premium >= 3 * total
    solver.add(4 * Sum(premium_out) >= 3 * Sum(total_out))

# 5. Flow balancing: total standard flow >= 0.5 * total premium flow
std_flows = [flow[(u,v)] for (u,v,_,_,typ) in edges if typ == 'standard']
premium_flows = [flow[(u,v)] for (u,v,_,_,typ) in edges if typ == 'premium']
solver.add(2 * Sum(std_flows) >= Sum(premium_flows))

# 6. Objective: maximize total flow into sink (node 8)
sink_flows = [flow[(u,8)] for (u,v,_,_,_) in edges if v == 8]
solver.maximize(Sum(sink_flows))

# Solve and print results
if solver.check() == sat:
    print("STATUS: sat")
    m = solver.model()
    max_flow_val = m.eval(Sum(sink_flows))
    print(f"max_flow = {max_flow_val}")
    # Print each edge flow
    for (u,v,_,_,_) in edges:
        fval = m.eval(flow[(u,v)])
        print(f"from {u} to {v} flow {fval}")
else:
    print("STATUS: unsat")