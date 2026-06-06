from z3 import *

# Instance data
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
    'A': ((2, 2), 100),
    'B': ((4, 4), 120),
    'C': ((6, 2), 110),
    'D': ((3, 5), 90),
    'E': ((7, 3), 130)
}

# Convert to lists for indexing
customer_list = list(customers.keys())
facility_list = list(facilities.keys())
N = len(customer_list)  # 8 customers
M = len(facility_list)  # 5 facilities

# Calculate Manhattan distances
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Distance matrix: dist[i][j] = distance from customer i to facility j
dist = [[0]*M for _ in range(N)]
for i, cust_id in enumerate(customer_list):
    for j, fac_id in enumerate(facility_list):
        dist[i][j] = manhattan(customers[cust_id], facilities[fac_id][0])

# Coverage radius
R = 3

# Service cost per unit distance
SERVICE_COST = 5

# Create optimization solver
opt = Optimize()

# Decision variables
# open_f[j] = 1 if facility j is opened
open_f = [Bool(f'open_{facility_list[j]}') for j in range(M)]

# assign[i][j] = 1 if customer i is assigned to facility j
assign = [[Bool(f'assign_{customer_list[i]}_{facility_list[j]}') for j in range(M)] for i in range(N)]

# Constraints

# 1. Each customer must be served by at least one facility
for i in range(N):
    opt.add(Sum([If(assign[i][j], 1, 0) for j in range(M)]) >= 1)

# 2. A facility can only serve customers within coverage radius
for i in range(N):
    for j in range(M):
        if dist[i][j] > R:
            opt.add(Not(assign[i][j]))  # Cannot assign if outside radius

# 3. Facilities can only serve customers if they are opened
for i in range(N):
    for j in range(M):
        opt.add(Implies(assign[i][j], open_f[j]))

# Objective: minimize total cost
# Opening costs
opening_cost = Sum([If(open_f[j], facilities[facility_list[j]][1], 0) for j in range(M)])

# Service costs: sum over all assignments of distance * SERVICE_COST
service_cost = Sum([If(assign[i][j], dist[i][j] * SERVICE_COST, 0) for i in range(N) for j in range(M)])

total_cost = opening_cost + service_cost
opt.minimize(total_cost)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract opened facilities
    opened = []
    for j in range(M):
        if is_true(model[open_f[j]]):
            opened.append(facility_list[j])
    
    # Extract assignments
    assignments = {}
    for i in range(N):
        cust_id = customer_list[i]
        for j in range(M):
            if is_true(model[assign[i][j]]):
                assignments[str(cust_id)] = facility_list[j]
                break  # Each customer assigned to exactly one facility (though could be multiple)
    
    # Calculate total cost from model
    total_cost_val = model.eval(total_cost)
    
    print(f"facilities: {opened}")
    print(f"assignments: {assignments}")
    print(f"total_cost: {total_cost_val}")
    print(f"feasible: True")
    
    # Verify expected optimal cost
    if total_cost_val == 380:
        print("Expected optimal cost achieved!")
    else:
        print(f"Note: Expected optimal cost is 380, got {total_cost_val}")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")