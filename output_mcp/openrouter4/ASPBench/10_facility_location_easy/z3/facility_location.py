from z3 import *

# Data
customers = list(range(8))  # 0-7
facilities = list(range(5))  # 0-4 (A-E)

cust_coords = [(1,1), (2,4), (4,2), (5,5), (7,1), (8,3), (3,6), (6,4)]
fac_coords = [(2,2), (4,4), (6,2), (3,5), (7,3)]
fac_opening_costs = [100, 120, 110, 90, 130]
fac_names = ['A', 'B', 'C', 'D', 'E']

R = 3
service_cost_per_unit = 5

# Precompute Manhattan distances
dist = [[abs(cust_coords[c][0] - fac_coords[f][0]) + abs(cust_coords[c][1] - fac_coords[f][1]) for f in facilities] for c in customers]

# Precompute which facilities can serve which customers
can_serve = [[dist[c][f] <= R for f in facilities] for c in customers]

# Print coverage info for debugging
print("=== Coverage Matrix (Manhattan distances) ===")
print("      A(2,2) B(4,4) C(6,2) D(3,5) E(7,3)")
for c in customers:
    row = f"C{c+1}{str(cust_coords[c]):>8s}: "
    for f in facilities:
        row += f" {dist[c][f]:2d}" + ("*" if can_serve[c][f] else " ")
    print(row)

print()

# Decision variables
open_fac = [Bool(f'open_{fac_names[f]}') for f in facilities]
serve = [[Bool(f'serve_c{c+1}_{fac_names[f]}') for f in facilities] for c in customers]

solver = Optimize()

# Each customer must be served by at least one facility
for c in customers:
    solver.add(Sum([serve[c][f] for f in facilities]) >= 1)

# A facility can only serve customers within its coverage radius
for c in customers:
    for f in facilities:
        if not can_serve[c][f]:
            solver.add(Not(serve[c][f]))

# A facility can only serve customers if it is opened
for c in customers:
    for f in facilities:
        solver.add(Implies(serve[c][f], open_fac[f]))

# Objective: minimize total cost
opening_cost = Sum([If(open_fac[f], fac_opening_costs[f], 0) for f in facilities])
service_cost = Sum([If(serve[c][f], dist[c][f] * service_cost_per_unit, 0) for c in customers for f in facilities])
total_cost = opening_cost + service_cost

solver.minimize(total_cost)

# Solve
BENCHMARK_MODE = True  # ON
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    opened = [fac_names[f] for f in facilities if is_true(m[open_fac[f]])]
    print(f"\nOpened facilities: {opened}")
    
    print("\nAssignments (Customer -> Facility):")
    total_svc_cost = 0
    for c in customers:
        for f in facilities:
            if is_true(m[serve[c][f]]):
                d = dist[c][f]
                cost = d * service_cost_per_unit
                total_svc_cost += cost
                print(f"  C{c+1}{str(cust_coords[c]):>8s} -> {fac_names[f]}{str(fac_coords[f]):>8s}, distance={d}, service_cost={cost}")
    
    total_open_cost = sum(fac_opening_costs[f] for f in facilities if is_true(m[open_fac[f]]))
    print(f"\nOpening cost: {total_open_cost}")
    print(f"Service cost: {total_svc_cost}")
    print(f"Total cost: {total_open_cost + total_svc_cost}")
else:
    print(f"STATUS: {result}")