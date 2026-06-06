from z3 import *

# ============================================================
# DATA
# ============================================================

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

facilities_data = {
    'A': (2, 2, 100),
    'B': (4, 4, 120),
    'C': (6, 2, 110),
    'D': (3, 5, 90),
    'E': (7, 3, 130)
}

facility_ids = ['A', 'B', 'C', 'D', 'E']
customer_ids = list(range(1, 9))

COVERAGE_RADIUS = 3
SERVICE_COST_PER_UNIT = 5

# Precompute Manhattan distances
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# dist[c][f] = Manhattan distance between customer c and facility f
dist = {}
for c in customer_ids:
    for f in facility_ids:
        dist[(c, f)] = manhattan(customers[c], facilities_data[f][:2])

# ============================================================
# Z3 MODEL
# ============================================================

opt = Optimize()

# Decision variables
# open[f] = 1 if facility f is opened, 0 otherwise
open_fac = {f: Int(f'open_{f}') for f in facility_ids}
for f in facility_ids:
    opt.add(Or(open_fac[f] == 0, open_fac[f] == 1))

# assign[c][f] = 1 if customer c is served by facility f, 0 otherwise
assign = {}
for c in customer_ids:
    for f in facility_ids:
        assign[(c, f)] = Int(f'assign_{c}_{f}')
        opt.add(Or(assign[(c, f)] == 0, assign[(c, f)] == 1))

# Constraint 1: Each customer must be served by at least one facility
for c in customer_ids:
    opt.add(Sum([assign[(c, f)] for f in facility_ids]) >= 1)

# Constraint 2: A facility can only serve customers within its coverage radius
for c in customer_ids:
    for f in facility_ids:
        if dist[(c, f)] > COVERAGE_RADIUS:
            opt.add(assign[(c, f)] == 0)

# Constraint 3: Facilities can only serve customers if they are opened
for c in customer_ids:
    for f in facility_ids:
        opt.add(Implies(assign[(c, f)] == 1, open_fac[f] == 1))

# Objective: Minimize total cost
# Opening cost
opening_cost = Sum([If(open_fac[f] == 1, facilities_data[f][2], 0) for f in facility_ids])

# Service cost = sum over all assignments of (distance * 5)
service_cost = Sum([If(assign[(c, f)] == 1, dist[(c, f)] * SERVICE_COST_PER_UNIT, 0) for c in customer_ids for f in facility_ids])

total_cost = opening_cost + service_cost
opt.minimize(total_cost)

# ============================================================
# SOLVE
# ============================================================

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    
    # Extract opened facilities
    opened = [f for f in facility_ids if m.eval(open_fac[f]).as_long() == 1]
    
    # Extract assignments (each customer assigned to exactly one facility ideally)
    # We'll pick the first assigned facility for each customer
    assignments = {}
    for c in customer_ids:
        for f in facility_ids:
            if m.eval(assign[(c, f)]).as_long() == 1:
                assignments[str(c)] = f
                break
    
    # Compute total cost from model
    total_cost_val = m.eval(total_cost).as_long()
    
    print("STATUS: sat")
    print(f"facilities: {opened}")
    print(f"assignments: {assignments}")
    print(f"total_cost: {total_cost_val}")
    
    # Verify manually
    opening_cost_val = sum(facilities_data[f][2] for f in opened)
    service_cost_val = 0
    for c_str, f in assignments.items():
        c = int(c_str)
        service_cost_val += dist[(c, f)] * SERVICE_COST_PER_UNIT
    manual_total = opening_cost_val + service_cost_val
    print(f"Verification - opening: {opening_cost_val}, service: {service_cost_val}, total: {manual_total}")
    
    # Check feasibility
    feasible = True
    for c in customer_ids:
        served = False
        for f in opened:
            if dist[(c, f)] <= COVERAGE_RADIUS:
                served = True
                break
        if not served:
            feasible = False
            break
    print(f"feasible: {feasible}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")