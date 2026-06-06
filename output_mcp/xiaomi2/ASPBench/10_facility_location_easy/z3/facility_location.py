from z3 import *

# Problem Data
customers = {
    1: (1, 1), 2: (2, 4), 3: (4, 2), 4: (5, 5),
    5: (7, 1), 6: (8, 3), 7: (3, 6), 8: (6, 4)
}

facilities_data = {
    'A': ((2, 2), 100),
    'B': ((4, 4), 120),
    'C': ((6, 2), 110),
    'D': ((3, 5), 90),
    'E': ((7, 3), 130)
}

facility_ids = ['A', 'B', 'C', 'D', 'E']
customer_ids = list(range(1, 9))

# Compute Manhattan distances
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Precompute distances and feasibility
dist = {}
feasible_assign = {}
for c in customer_ids:
    feasible_assign[c] = []
    for f in facility_ids:
        d = manhattan(customers[c], facilities_data[f][0])
        dist[(c, f)] = d
        if d <= 3:
            feasible_assign[c].append(f)

print("Feasible assignments (within radius 3):")
for c in customer_ids:
    print(f"  Customer {c}: {[(f, dist[(c,f)]) for f in feasible_assign[c]]}")

# Z3 Model
opt = Optimize()

# Decision variables
open_fac = {f: Bool(f'open_{f}') for f in facility_ids}
assign = {(c, f): Bool(f'assign_{c}_{f}') for c in customer_ids for f in facility_ids}

# Constraints
for c in customer_ids:
    # Each customer must be served by at least one facility
    opt.add(Or([assign[(c, f)] for f in feasible_assign[c]]))
    
    for f in facility_ids:
        # Can only assign to feasible facilities (within radius)
        if f not in feasible_assign[c]:
            opt.add(Not(assign[(c, f)]))
        else:
            # Can only assign if facility is open
            opt.add(Implies(assign[(c, f)], open_fac[f]))

# Objective: minimize total cost
opening_costs = Sum([If(open_fac[f], facilities_data[f][1], 0) for f in facility_ids])
service_costs = Sum([If(assign[(c, f)], dist[(c, f)] * 5, 0) 
                     for c in customer_ids for f in feasible_assign[c]])
total_cost = opening_costs + service_costs

opt.minimize(total_cost)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("\nSTATUS: sat")
    
    # Extract solution
    opened = []
    for f in facility_ids:
        if is_true(m.evaluate(open_fac[f])):
            opened.append(f)
    
    assignments = {}
    total_opening = 0
    total_service = 0
    
    for c in customer_ids:
        for f in feasible_assign[c]:
            if is_true(m.evaluate(assign[(c, f)])):
                assignments[str(c)] = f
                total_opening_contrib = 0  # counted separately
                service_cost = dist[(c, f)] * 5
                total_service += service_cost
                break
    
    for f in opened:
        total_opening += facilities_data[f][1]
    
    total = total_opening + total_service
    
    print(f"\nOpened facilities: {opened}")
    print(f"Opening costs: {total_opening}")
    print(f"Service costs: {total_service}")
    print(f"Total cost: {total}")
    
    print(f"\nAssignments:")
    for c in customer_ids:
        f = assignments[str(c)]
        d = dist[(c, f)]
        sc = d * 5
        print(f"  Customer {c} -> Facility {f} (dist={d}, service_cost={sc})")
    
    print(f"\nfacilities: {opened}")
    print(f"assignments: {assignments}")
    print(f"total_cost: {total}")
    print(f"feasible: True")
    
    # Verify expected optimal
    if total == 380:
        print("\nMatches expected optimal cost of 380!")
    else:
        print(f"\nNote: Got {total}, expected 380")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")