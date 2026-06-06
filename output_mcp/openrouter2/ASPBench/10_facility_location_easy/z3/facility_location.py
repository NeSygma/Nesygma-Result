from z3 import *

# Problem data
customers = [
    (1, 1),
    (2, 4),
    (4, 2),
    (5, 5),
    (7, 1),
    (8, 3),
    (3, 6),
    (6, 4),
]
facilities = [
    (2, 2, 100),  # A
    (4, 4, 120),  # B
    (6, 2, 110),  # C
    (3, 5, 90),   # D
    (7, 3, 130),  # E
]

# Precompute Manhattan distances
n_cust = len(customers)
n_fac = len(facilities)
# dist[j][i] = distance from customer j to facility i
dist = [[abs(customers[j][0]-facilities[i][0]) + abs(customers[j][1]-facilities[i][1]) for i in range(n_fac)] for j in range(n_cust)]

# Variables
open_f = [Bool(f'open_{i}') for i in range(n_fac)]
assign = [Int(f'assign_{j}') for j in range(n_cust)]

opt = Optimize()

# Constraints
# Each customer must be assigned to a facility within radius 3 and that facility must be open
for j in range(n_cust):
    feasible_indices = [i for i in range(n_fac) if dist[j][i] <= 3]
    # At least one feasible facility
    opt.add(Or([assign[j] == i for i in feasible_indices]))
    for i in feasible_indices:
        opt.add(Implies(assign[j] == i, open_f[i]))
        opt.add(Implies(assign[j] == i, dist[j][i] <= 3))

# Objective: minimize total cost
opening_costs = [facilities[i][2] for i in range(n_fac)]
service_cost_expr = Sum([Sum([If(assign[j] == i, dist[j][i]*5, 0) for i in range(n_fac)]) for j in range(n_cust)])
opening_cost_expr = Sum([If(open_f[i], opening_costs[i], 0) for i in range(n_fac)])
total_cost_expr = opening_cost_expr + service_cost_expr
opt.minimize(total_cost_expr)

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    # Extract facilities
    fac_letters = ['A', 'B', 'C', 'D', 'E']
    opened = [fac_letters[i] for i in range(n_fac) if is_true(model[open_f[i]])]
    # Extract assignments
    assignments = {}
    for j in range(n_cust):
        val = model[assign[j]]
        if val is None:
            # Should not happen
            assigned_fac = None
        else:
            assigned_fac = fac_letters[val.as_long()]
        assignments[str(j+1)] = assigned_fac
    # Compute total cost from model
    total_cost_val = model.evaluate(total_cost_expr, model_completion=True).as_long()
    print("STATUS: sat")
    print("facilities =", opened)
    print("assignments =", assignments)
    print("total_cost =", total_cost_val)
    print("feasible = True")
else:
    print("STATUS: unsat")
    if result == unknown:
        print("RAW_RESULT: unknown")