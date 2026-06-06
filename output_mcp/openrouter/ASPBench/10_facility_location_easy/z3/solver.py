from z3 import *

# Data
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
service_per_dist = 5

# Precompute Manhattan distances
dist = {}
for c_id, (cx, cy) in customers.items():
    for f_id, ((fx, fy), _) in facilities.items():
        d = abs(cx - fx) + abs(cy - fy)
        dist[(c_id, f_id)] = d

# Solver
opt = Optimize()
# Bool vars for opening facilities
open_f = {fid: Bool(f"open_{fid}") for fid in facilities}
# Bool vars for assignments
assign = {(c, f): Bool(f"assign_{c}_{f}") for c in customers for f in facilities}

# Constraints: each customer assigned to exactly one facility
for c in customers:
    opt.add(Sum([If(assign[(c, f)], 1, 0) for f in facilities]) == 1)

# Assignment feasibility constraints
for c in customers:
    for f in facilities:
        d = dist[(c, f)]
        # If assigned then facility must be open and distance within coverage (<=3)
        opt.add(Implies(assign[(c, f)], And(open_f[f], d <= 3)))
        # Also, if distance > 3 then cannot assign (redundant but ensures Bool false)
        if d > 3:
            opt.add(assign[(c, f)] == False)

# Total cost expression
opening_cost_expr = Sum([If(open_f[f], facilities[f][1], 0) for f in facilities])
service_cost_expr = Sum([If(assign[(c, f)], dist[(c, f)] * service_per_dist, 0) for c in customers for f in facilities])
total_cost = opening_cost_expr + service_cost_expr
opt.minimize(total_cost)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    # Gather opened facilities
    opened = [f for f in facilities if m.eval(open_f[f])]
    # Assignments mapping
    assignments = {}
    for c in customers:
        for f in facilities:
            if m.eval(assign[(c, f)]):
                assignments[str(c)] = f
                break
    # Compute total cost value
    total_val = m.eval(total_cost).as_long()
    print("STATUS: sat")
    print("facilities:", opened)
    print("assignments:", assignments)
    print("total_cost:", total_val)
    print("feasible:", True)
else:
    print("STATUS: unsat")