from z3 import *

# Declare boolean variables for each vertex 0..15
selected = [Bool(f's_{i}') for i in range(16)]

# Vertex costs: 3 for high-cost vertices 2,10,14; 1 otherwise
cost = [3 if i in (2,10,14) else 1 for i in range(16)]

# Total cost as sum of costs of selected vertices
total_cost = Sum([If(selected[i], cost[i], 0) for i in range(16)])

# Create optimizer
opt = Optimize()

# Standard edges: at least one endpoint selected
standard_edges = [(1,3), (1,4), (2,6), (3,7), (4,8), (5,11), (6,7), (7,12), (8,12), (11,13), (12,13), (13,14)]
for u,v in standard_edges:
    opt.add(Or(selected[u], selected[v]))

# Heavy edges with master vertex exception
heavy_edges = [(0,5), (9,10), (14,15)]
masters = {0,15}
for u,v in heavy_edges:
    if u in masters:
        opt.add(selected[u])
    elif v in masters:
        opt.add(selected[v])
    else:
        opt.add(And(selected[u], selected[v]))

# Antagonistic pairs: at most one selected
antagonistic = [(1,2), (8,9)]
for u,v in antagonistic:
    opt.add(selected[u] + selected[v] <= 1)

# Objective: minimize total cost
opt.minimize(total_cost)

# Solve
if opt.check() == sat:
    model = opt.model()
    # Status line
    print('STATUS: sat')
    # Collect selected vertices
    vertices = [i for i in range(16) if model[selected[i]]]
    vertices.sort()
    print(f'vertex_cover: {vertices}')
    # Compute total cost from model
    cost_val = model.eval(total_cost)
    print(f'total_cost: {cost_val}')