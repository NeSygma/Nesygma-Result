from z3 import *

# Data
warehouses = ['W1', 'W2', 'W3']
customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
capacity = {'W1': 100, 'W2': 150, 'W3': 120}
demand = {'C1': 25, 'C2': 30, 'C3': 20, 'C4': 35, 'C5': 15, 'C6': 25}
# distance matrix: warehouse -> customer
distance = {
    'W1': {'C1':10, 'C2':15, 'C3':25, 'C4':20, 'C5':30, 'C6':12},
    'W2': {'C1':18, 'C2':8,  'C3':12, 'C4':15, 'C5':10, 'C6':20},
    'W3': {'C1':22, 'C2':25, 'C3':8,  'C4':18, 'C5':12, 'C6':15}
}

# Create Optimize solver
opt = Optimize()

# Variables
open_w = {w: Bool(f'open_{w}') for w in warehouses}
assign = {(c,w): Bool(f'assign_{c}_{w}') for c in customers for w in warehouses}

# Constraints
# 1. Each customer assigned to exactly one warehouse
for c in customers:
    opt.add(Sum([If(assign[(c,w)], 1, 0) for w in warehouses]) == 1)

# 2. Assignment implies warehouse is open
for c in customers:
    for w in warehouses:
        opt.add(Implies(assign[(c,w)], open_w[w]))

# 3. Capacity constraints
for w in warehouses:
    total_demand = Sum([If(assign[(c,w)], demand[c], 0) for c in customers])
    opt.add(total_demand <= capacity[w])

# Objective: minimize total transportation cost
total_cost_expr = Sum([If(assign[(c,w)], demand[c] * distance[w][c], 0) for c in customers for w in warehouses])
opt.minimize(total_cost_expr)

# Solve
if opt.check() == sat:
    m = opt.model()
    # Determine selected warehouses
    selected = [w for w in warehouses if is_true(m.eval(open_w[w]))]
    # Determine assignments
    assign_map = {}
    for c in customers:
        for w in warehouses:
            if is_true(m.eval(assign[(c,w)])):
                assign_map[c] = w
                break
    # Compute total cost from model (should match objective)
    total_cost = sum(demand[c] * distance[assign_map[c]][c] for c in customers)
    print('STATUS: sat')
    print('selected_warehouses =', selected)
    print('assignments =', assign_map)
    print('total_cost =', total_cost)
else:
    print('STATUS: unsat')