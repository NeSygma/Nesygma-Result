from z3 import *

# Define the network
edges = [
    {'from': 1, 'to': 2, 'cap': 10, 'cost': 2, 'type': 'standard'},
    {'from': 1, 'to': 3, 'cap': 12, 'cost': 4, 'type': 'premium'},
    {'from': 2, 'to': 4, 'cap': 8, 'cost': 1, 'type': 'standard'},
    {'from': 2, 'to': 5, 'cap': 4, 'cost': 3, 'type': 'premium'},
    {'from': 3, 'to': 4, 'cap': 5, 'cost': 3, 'type': 'standard'},
    {'from': 3, 'to': 6, 'cap': 10, 'cost': 5, 'type': 'premium'},
    {'from': 4, 'to': 7, 'cap': 10, 'cost': 2, 'type': 'standard'},
    {'from': 5, 'to': 7, 'cap': 7, 'cost': 4, 'type': 'premium'},
    {'from': 6, 'to': 8, 'cap': 12, 'cost': 2, 'type': 'premium'},
    {'from': 7, 'to': 8, 'cap': 15, 'cost': 1, 'type': 'standard'}
]

# Create flow variables
flow_vars = {}
for i, edge in enumerate(edges):
    flow_vars[i] = Int(f"f_{edge['from']}_{edge['to']}")

opt = Optimize()

# 1. Capacity Constraint
for i, edge in enumerate(edges):
    opt.add(flow_vars[i] >= 0)
    opt.add(flow_vars[i] <= edge['cap'])

# 2. Flow Conservation
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
for node in nodes:
    if node == 1 or node == 8:
        continue
    
    incoming = Sum([flow_vars[i] for i, edge in enumerate(edges) if edge['to'] == node])
    outgoing = Sum([flow_vars[i] for i, edge in enumerate(edges) if edge['from'] == node])
    opt.add(incoming == outgoing)

# 3. Budget Constraint
total_cost = Sum([flow_vars[i] * edges[i]['cost'] for i in range(len(edges))])
opt.add(total_cost <= 100)

# 4. Priority Node Rule (3, 5)
# For priority nodes (3, 5), if there is incoming flow, at least 75% of outgoing flow must be premium type
# Note: The problem says "if there is incoming flow". 
# Let's assume it means if outgoing flow > 0.
for node in [3, 5]:
    outgoing_edges = [i for i, edge in enumerate(edges) if edge['from'] == node]
    total_outgoing = Sum([flow_vars[i] for i in outgoing_edges])
    premium_outgoing = Sum([flow_vars[i] for i in outgoing_edges if edges[i]['type'] == 'premium'])
    
    # premium_outgoing >= 0.75 * total_outgoing
    # To avoid floating point, multiply by 4: 4 * premium_outgoing >= 3 * total_outgoing
    opt.add(Implies(total_outgoing > 0, 4 * premium_outgoing >= 3 * total_outgoing))

# 5. Flow Balancing
# Total standard flow >= 0.5 * Total premium flow
# 2 * total_standard >= total_premium
total_standard = Sum([flow_vars[i] for i in range(len(edges)) if edges[i]['type'] == 'standard'])
total_premium = Sum([flow_vars[i] for i in range(len(edges)) if edges[i]['type'] == 'premium'])
opt.add(2 * total_standard >= total_premium)

# Objective: Maximize total flow from source (1) to sink (8)
total_flow = Sum([flow_vars[i] for i, edge in enumerate(edges) if edge['from'] == 1])
opt.maximize(total_flow)

result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"max_flow: {m.evaluate(total_flow)}")
    for i, edge in enumerate(edges):
        print(f"Edge ({edge['from']}, {edge['to']}): {m.evaluate(flow_vars[i])}")
else:
    print("STATUS: unsat")