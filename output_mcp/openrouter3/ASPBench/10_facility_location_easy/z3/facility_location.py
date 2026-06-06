from z3 import *

# Problem data
customers = {
    1: (1, 1),
    2: (2, 4),
    3: (4, 2),
    4: (5, 5),
    5: (7, 1),
    6: (8, 3),
    7: (3, 6),
    8: (6, 4)
}

facilities = {
    'A': {'coords': (2, 2), 'cost': 100},
    'B': {'coords': (4, 4), 'cost': 120},
    'C': {'coords': (6, 2), 'cost': 110},
    'D': {'coords': (3, 5), 'cost': 90},
    'E': {'coords': (7, 3), 'cost': 130}
}

coverage_radius = 3
service_cost_per_unit = 5

# Create solver
solver = Solver()

# Decision variables
open_facility = {f: Bool(f'open_{f}') for f in facilities}
assign = {}
for c in customers:
    for f in facilities:
        assign[(c, f)] = Bool(f'assign_{c}_{f}')

# Helper function for Manhattan distance
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Constraint 1: Each customer must be served by at least one facility
for c in customers:
    # Only consider facilities within coverage radius
    valid_assignments = []
    for f in facilities:
        dist = manhattan_distance(customers[c], facilities[f]['coords'])
        if dist <= coverage_radius:
            valid_assignments.append(assign[(c, f)])
    if valid_assignments:
        solver.add(Or(valid_assignments))

# Constraint 2: Facilities can only serve customers within coverage radius
for c in customers:
    for f in facilities:
        dist = manhattan_distance(customers[c], facilities[f]['coords'])
        if dist > coverage_radius:
            # Cannot assign if distance > coverage radius
            solver.add(Not(assign[(c, f)]))

# Constraint 3: Assignment only possible if facility is opened
for c in customers:
    for f in facilities:
        solver.add(Implies(assign[(c, f)], open_facility[f]))

# Constraint 4: Each customer can be served by multiple facilities (but we'll minimize cost)
# Actually, we don't need to enforce single assignment - the cost minimization will handle it

# Calculate total cost
# Opening costs
opening_cost = Sum([If(open_facility[f], facilities[f]['cost'], 0) for f in facilities])

# Service costs
service_cost = 0
for c in customers:
    for f in facilities:
        dist = manhattan_distance(customers[c], facilities[f]['coords'])
        # Only add service cost if assignment is made
        service_cost += If(assign[(c, f)], dist * service_cost_per_unit, 0)

total_cost = opening_cost + service_cost

# Objective: minimize total cost
opt = Optimize()
opt.add([solver.assertions()[i] for i in range(len(solver.assertions()))])
opt.minimize(total_cost)

# Check for optimal solution
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract opened facilities
    opened = [f for f in facilities if is_true(model[open_facility[f]])]
    
    # Extract assignments
    assignments = {}
    for c in customers:
        for f in facilities:
            if is_true(model[assign[(c, f)]]):
                assignments[str(c)] = f
    
    # Calculate total cost from model
    total_cost_val = 0
    for f in opened:
        total_cost_val += facilities[f]['cost']
    for c, f in assignments.items():
        c_int = int(c)
        dist = manhattan_distance(customers[c_int], facilities[f]['coords'])
        total_cost_val += dist * service_cost_per_unit
    
    print(f"facilities: {opened}")
    print(f"assignments: {assignments}")
    print(f"total_cost: {total_cost_val}")
    print(f"feasible: True")
    
    # Verify expected optimal cost
    if total_cost_val == 380:
        print("Optimal cost matches expected: 380")
    else:
        print(f"Note: Found cost {total_cost_val}, expected 380")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")