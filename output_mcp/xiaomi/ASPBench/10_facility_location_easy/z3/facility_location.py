from z3 import *

# Data
customers = {
    1: (1, 1), 2: (2, 4), 3: (4, 2), 4: (5, 5),
    5: (7, 1), 6: (8, 3), 7: (3, 6), 8: (6, 4)
}

facilities_data = {
    'A': {'pos': (2, 2), 'cost': 100},
    'B': {'pos': (4, 4), 'cost': 120},
    'C': {'pos': (6, 2), 'cost': 110},
    'D': {'pos': (3, 5), 'cost': 90},
    'E': {'pos': (7, 3), 'cost': 130},
}

facility_names = ['A', 'B', 'C', 'D', 'E']
customer_ids = list(range(1, 9))

# Precompute Manhattan distances
dist = {}
for c_id, (cx, cy) in customers.items():
    for f_name, f_data in facilities_data.items():
        fx, fy = f_data['pos']
        dist[(c_id, f_name)] = abs(cx - fx) + abs(cy - fy)

RADIUS = 3
SERVICE_COST_PER_UNIT = 5

# Z3 Model
opt = Optimize()

# Decision variables
# opened[f] = True if facility f is opened
opened = {f: Bool(f'opened_{f}') for f in facility_names}

# assigned[c, f] = True if customer c is served by facility f
assigned = {}
for c in customer_ids:
    for f in facility_names:
        assigned[(c, f)] = Bool(f'assigned_{c}_{f}')

# Constraints

# 1. Each customer must be served by at least one facility
for c in customer_ids:
    opt.add(Or([assigned[(c, f)] for f in facility_names]))

# 2. A facility can only serve customers within coverage radius
for c in customer_ids:
    for f in facility_names:
        if dist[(c, f)] > RADIUS:
            opt.add(Not(assigned[(c, f)]))

# 3. Facilities can only serve customers if they are opened
for c in customer_ids:
    for f in facility_names:
        opt.add(Implies(assigned[(c, f)], opened[f]))

# Objective: minimize total cost
# Opening costs
opening_cost = Sum([If(opened[f], facilities_data[f]['cost'], 0) for f in facility_names])

# Service costs
service_cost = Sum([
    If(assigned[(c, f)], dist[(c, f)] * SERVICE_COST_PER_UNIT, 0)
    for c in customer_ids
    for f in facility_names
])

total_cost = opening_cost + service_cost
opt.minimize(total_cost)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract opened facilities
    opened_facilities = [f for f in facility_names if is_true(m[opened[f]])]
    print(f"facilities: {opened_facilities}")
    
    # Extract assignments
    assignments = {}
    for c in customer_ids:
        for f in facility_names:
            if is_true(m[assigned[(c, f)]]):
                assignments[str(c)] = f
                break
    print(f"assignments: {assignments}")
    
    # Compute total cost
    total_opening = sum(facilities_data[f]['cost'] for f in opened_facilities)
    total_service = sum(dist[(int(c), f)] * SERVICE_COST_PER_UNIT for c, f in assignments.items())
    total = total_opening + total_service
    print(f"total_cost: {total}")
    print(f"feasible: True")
    
    # Verify
    print(f"\nVerification:")
    print(f"Opening costs: {total_opening}")
    print(f"Service costs: {total_service}")
    print(f"Total: {total}")
    
    for c in customer_ids:
        f = assignments[str(c)]
        d = dist[(c, f)]
        print(f"Customer {c} -> Facility {f}, dist={d}, cost={d*5}")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")