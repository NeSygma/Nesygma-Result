from z3 import *

# Data
customers = {
    1: (1, 1), 2: (2, 4), 3: (4, 2), 4: (5, 5),
    5: (7, 1), 6: (8, 3), 7: (3, 6), 8: (6, 4)
}
facilities = {
    'A': {'pos': (2, 2), 'cost': 100},
    'B': {'pos': (4, 4), 'cost': 120},
    'C': {'pos': (6, 2), 'cost': 110},
    'D': {'pos': (3, 5), 'cost': 90},
    'E': {'pos': (7, 3), 'cost': 130}
}

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Optimization
opt = Optimize()

# Variables
# opened[f] is True if facility f is opened
opened = {f: Bool(f'opened_{f}') for f in facilities}
# assigned[c][f] is True if customer c is served by facility f
assigned = {c: {f: Bool(f'assigned_{c}_{f}') for f in facilities} for c in customers}

# Constraints
# 1. Each customer must be served by at least one facility
for c in customers:
    opt.add(Or([assigned[c][f] for f in facilities]))

# 2. A facility can only serve customers within its coverage radius (distance <= 3)
# 3. Facilities can only serve customers if they are opened
for c in customers:
    for f in facilities:
        dist = manhattan(customers[c], facilities[f]['pos'])
        if dist > 3:
            opt.add(Not(assigned[c][f]))
        else:
            opt.add(Implies(assigned[c][f], opened[f]))

# Objective: Minimize total cost
# Total cost = sum(opening costs) + sum(service costs)
opening_cost = Sum([If(opened[f], facilities[f]['cost'], 0) for f in facilities])
service_cost = Sum([
    If(assigned[c][f], manhattan(customers[c], facilities[f]['pos']) * 5, 0)
    for c in customers for f in facilities
])

opt.minimize(opening_cost + service_cost)

# Solve
if opt.check() == sat:
    m = opt.model()
    print("STATUS: sat")
    
    opened_list = [f for f in facilities if is_true(m[opened[f]])]
    print(f"facilities: {opened_list}")
    
    assignments = {}
    for c in customers:
        for f in facilities:
            if is_true(m[assigned[c][f]]):
                assignments[c] = f
                break
    print(f"assignments: {assignments}")
    
    total_cost = m.evaluate(opening_cost + service_cost)
    print(f"total_cost: {total_cost}")
    print("feasible: True")
else:
    print("STATUS: unsat")