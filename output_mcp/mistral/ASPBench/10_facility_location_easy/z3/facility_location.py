from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# ============================================================================
# DATA
# ============================================================================

# Customers: (id, (x, y))
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

# Facilities: (id, (x, y), opening_cost)
facilities = {
    'A': ((2, 2), 100),
    'B': ((4, 4), 120),
    'C': ((6, 2), 110),
    'D': ((3, 5), 90),
    'E': ((7, 3), 130)
}

# Parameters
coverage_radius = 3
service_cost_per_unit = 5

# ============================================================================
# MODEL
# ============================================================================

solver = Optimize()

# Decision variables
# - facility_opened[f]: whether facility f is opened
facility_opened = {f: Bool(f"opened_{f}") for f in facilities.keys()}

# - assignment[c]: which facility serves customer c
# We'll use integer variables representing facility indices
facility_ids = list(facilities.keys())
assignment = {c: Int(f"assign_{c}") for c in customers.keys()}

# ============================================================================
# CONSTRAINTS
# ============================================================================

# Helper: Manhattan distance between customer c and facility f
def manhattan(c, f):
    cx, cy = customers[c]
    fx, fy = facilities[f][0]
    return Abs(cx - fx) + Abs(cy - fy)

# Constraint 1: Each customer must be served by at least one facility
# We'll enforce: assignment[c] == facility index of the serving facility
for c in customers.keys():
    # assignment[c] must be one of the facility indices
    solver.add(Or([assignment[c] == i for i in range(len(facility_ids))]))

# Constraint 2: A facility can only serve customers within coverage radius
# and only if it is opened
for c in customers.keys():
    for idx, f in enumerate(facility_ids):
        dist = manhattan(c, f)
        # If assigned to this facility, then distance <= coverage_radius and facility is opened
        solver.add(Implies(assignment[c] == idx, And(dist <= coverage_radius, facility_opened[f])))

# Constraint 3: Facilities can only serve customers if opened (enforced above)

# ============================================================================
# OBJECTIVE
# ============================================================================

# Total opening cost
total_opening_cost = Sum([
    If(facility_opened[f], facilities[f][1], 0) for f in facility_ids
])

# Total service cost
total_service_cost = Sum([
    If(assignment[c] == idx, service_cost_per_unit * manhattan(c, facility_ids[idx]), 0)
    for c in customers.keys()
    for idx in range(len(facility_ids))
])

# Minimize total cost
solver.minimize(total_opening_cost + total_service_cost)

# ============================================================================
# SOLVE
# ============================================================================

result = solver.check()

# ============================================================================
# OUTPUT
# ============================================================================

if result == sat:
    model = solver.model()
    
    # Extract opened facilities
    opened_facilities = [f for f in facility_ids if is_true(model[facility_opened[f]])]
    
    # Extract assignments
    assignments_dict = {}
    for c in customers.keys():
        assigned_idx = model[assignment[c]].as_long()
        assigned_facility = facility_ids[assigned_idx]
        assignments_dict[str(c)] = assigned_facility
    
    # Extract total cost
    total_cost = model.eval(total_opening_cost + total_service_cost).as_long()
    
    print("STATUS: sat")
    print(f"facilities: {opened_facilities}")
    print(f"assignments: {assignments_dict}")
    print(f"total_cost: {total_cost}")
    print(f"feasible: True")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")